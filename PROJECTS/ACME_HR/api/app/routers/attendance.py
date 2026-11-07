from datetime import date, datetime, time
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import record_audit
from app.deps import get_current_account, get_session, is_hr, require_active_employee, require_roles
from app.models import (
    Account,
    AttendanceRecord,
    Employee,
    LeaveRequest,
    LeaveStatus,
    Location,
    Role,
    Shift,
    ShiftAssignment,
    ShiftType,
)
from app.rules import is_late, local_now, utc_now_naive

router = APIRouter(tags=["attendance"])
hr_roles = require_roles(Role.SYSTEM_ADMINISTRATOR, Role.HR_ADMINISTRATOR)


class ShiftIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    shift_type: ShiftType
    start_time: time
    end_time: time
    late_after_minutes: int = Field(ge=0)


class ShiftOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    shift_type: ShiftType
    start_time: time
    end_time: time
    late_after_minutes: int


class AssignmentIn(BaseModel):
    employee_id: int
    shift_id: int
    work_date: date


class AssignmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    shift_id: int
    work_date: date


class AttendanceOut(BaseModel):
    id: int | None
    employee_id: int
    work_date: date
    check_in_at: datetime | None
    check_out_at: datetime | None
    hours_worked: Decimal | None
    status: str


def _hours(record: AttendanceRecord) -> Decimal | None:
    if record.check_out_at is None or record.check_in_at is None:
        return None
    seconds = (record.check_out_at - record.check_in_at).total_seconds()
    return Decimal(str(round(seconds / 3600, 2)))


def _location_timezone(session: Session, employee: Employee) -> str:
    if employee.location_id is None:
        raise HTTPException(status_code=422, detail="Check-in requires an office location.")
    location = session.get(Location, employee.location_id)
    if location is None:
        raise HTTPException(status_code=422, detail="Check-in requires an office location.")
    return location.timezone


def _status_for(
    record: AttendanceRecord | None,
    *,
    on_leave: bool,
    shift: Shift | None,
    timezone_name: str,
    today: date,
) -> str:
    if on_leave:
        return "On leave"
    if record is None:
        return "No check-in"
    if shift is None:
        return "No shift"
    if record.check_out_at is None and record.work_date < today:
        return "Missing check-out"
    if is_late(record.check_in_at, record.work_date, shift.start_time, shift.late_after_minutes, timezone_name):
        return "Late"
    return "On time"


def _to_out(record: AttendanceRecord, status: str) -> AttendanceOut:
    return AttendanceOut(
        id=record.id,
        employee_id=record.employee_id,
        work_date=record.work_date,
        check_in_at=record.check_in_at,
        check_out_at=record.check_out_at,
        hours_worked=_hours(record),
        status=status,
    )


@router.get("/shifts", response_model=list[ShiftOut])
def list_shifts(
    session: Session = Depends(get_session),
    _: Account = Depends(get_current_account),
) -> list[Shift]:
    return list(session.scalars(select(Shift).order_by(Shift.id)))


@router.post("/shifts", response_model=ShiftOut, status_code=201)
def create_shift(
    body: ShiftIn,
    session: Session = Depends(get_session),
    account: Account = Depends(hr_roles),
) -> Shift:
    row = Shift(
        name=body.name.strip(),
        shift_type=body.shift_type,
        start_time=body.start_time,
        end_time=body.end_time,
        late_after_minutes=body.late_after_minutes,
    )
    session.add(row)
    session.flush()
    record_audit(session, actor_employee_id=account.employee_id, action="create", entity_name="shifts", entity_id=str(row.id))
    return row


@router.put("/shift-assignments", response_model=AssignmentOut)
def assign_shift(
    body: AssignmentIn,
    session: Session = Depends(get_session),
    account: Account = Depends(hr_roles),
) -> ShiftAssignment:
    if session.get(Employee, body.employee_id) is None:
        raise HTTPException(status_code=422, detail="Employee not found.")
    if session.get(Shift, body.shift_id) is None:
        raise HTTPException(status_code=422, detail="Shift not found.")
    row = session.scalar(
        select(ShiftAssignment).where(
            ShiftAssignment.employee_id == body.employee_id,
            ShiftAssignment.work_date == body.work_date,
        )
    )
    if row is None:
        row = ShiftAssignment(employee_id=body.employee_id, work_date=body.work_date, shift_id=body.shift_id)
        session.add(row)
    else:
        row.shift_id = body.shift_id
    session.flush()
    record_audit(
        session,
        actor_employee_id=account.employee_id,
        action="assign",
        entity_name="shift_assignments",
        entity_id=str(row.id),
    )
    return row


@router.post("/attendance/check-in", response_model=AttendanceOut, status_code=201)
def check_in(
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> AttendanceOut:
    employee = account.employee
    require_active_employee(employee)
    timezone_name = _location_timezone(session, employee)
    work_date = local_now(timezone_name).date()
    existing = session.scalar(
        select(AttendanceRecord).where(
            AttendanceRecord.employee_id == employee.id,
            AttendanceRecord.work_date == work_date,
        )
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="You have already checked in for this date.")
    record = AttendanceRecord(
        employee_id=employee.id,
        work_date=work_date,
        check_in_at=utc_now_naive(),
    )
    session.add(record)
    session.flush()
    record_audit(
        session,
        actor_employee_id=employee.id,
        action="check_in",
        entity_name="attendance_records",
        entity_id=str(record.id),
    )
    shift = _shift_for(session, employee.id, work_date)
    return _to_out(record, _status_for(record, on_leave=False, shift=shift, timezone_name=timezone_name, today=work_date))


@router.post("/attendance/check-out", response_model=AttendanceOut)
def check_out(
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> AttendanceOut:
    employee = account.employee
    require_active_employee(employee)
    timezone_name = _location_timezone(session, employee)
    work_date = local_now(timezone_name).date()
    record = session.scalar(
        select(AttendanceRecord).where(
            AttendanceRecord.employee_id == employee.id,
            AttendanceRecord.work_date == work_date,
        )
    )
    if record is None:
        raise HTTPException(status_code=404, detail="Check in before checking out.")
    if record.check_out_at is not None:
        raise HTTPException(status_code=409, detail="You have already checked out for this date.")
    record.check_out_at = utc_now_naive()
    record_audit(
        session,
        actor_employee_id=employee.id,
        action="check_out",
        entity_name="attendance_records",
        entity_id=str(record.id),
    )
    shift = _shift_for(session, employee.id, work_date)
    return _to_out(record, _status_for(record, on_leave=False, shift=shift, timezone_name=timezone_name, today=work_date))


def _shift_for(session: Session, employee_id: int, work_date: date) -> Shift | None:
    assignment = session.scalar(
        select(ShiftAssignment).where(
            ShiftAssignment.employee_id == employee_id,
            ShiftAssignment.work_date == work_date,
        )
    )
    if assignment is None:
        return None
    return session.get(Shift, assignment.shift_id)


@router.get("/attendance/me", response_model=list[AttendanceOut])
def my_attendance(
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> list[AttendanceOut]:
    employee = account.employee
    location = session.get(Location, employee.location_id) if employee.location_id else None
    timezone_name = location.timezone if location else "UTC"
    today = local_now(timezone_name).date() if location else date.today()
    rows = session.scalars(
        select(AttendanceRecord)
        .where(AttendanceRecord.employee_id == employee.id)
        .order_by(AttendanceRecord.work_date.desc())
    ).all()
    results = []
    for row in rows:
        shift = _shift_for(session, employee.id, row.work_date)
        results.append(
            _to_out(row, _status_for(row, on_leave=False, shift=shift, timezone_name=timezone_name, today=today))
        )
    return results


@router.get("/attendance/daily", response_model=list[AttendanceOut])
def daily_attendance(
    work_date: date = Query(),
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> list[AttendanceOut]:
    if is_hr(account):
        employees = session.scalars(select(Employee).where(Employee.archived.is_(False)).order_by(Employee.name)).all()
    elif account.role == Role.MANAGER:
        employees = session.scalars(
            select(Employee)
            .where(Employee.reporting_manager_id == account.employee_id, Employee.archived.is_(False))
            .order_by(Employee.name)
        ).all()
    else:
        raise HTTPException(status_code=403, detail="You do not have access to this action.")
    results = []
    for employee in employees:
        location = session.get(Location, employee.location_id) if employee.location_id else None
        timezone_name = location.timezone if location else "UTC"
        today = local_now(timezone_name).date() if location else date.today()
        record = session.scalar(
            select(AttendanceRecord).where(
                AttendanceRecord.employee_id == employee.id,
                AttendanceRecord.work_date == work_date,
            )
        )
        on_leave = session.scalar(
            select(LeaveRequest.id).where(
                LeaveRequest.employee_id == employee.id,
                LeaveRequest.status == LeaveStatus.APPROVED,
                LeaveRequest.from_date <= work_date,
                LeaveRequest.to_date >= work_date,
            )
        ) is not None
        shift = _shift_for(session, employee.id, work_date)
        status = _status_for(record, on_leave=on_leave, shift=shift, timezone_name=timezone_name, today=today)
        if record is None:
            results.append(
                AttendanceOut(
                    id=None,
                    employee_id=employee.id,
                    work_date=work_date,
                    check_in_at=None,
                    check_out_at=None,
                    hours_worked=None,
                    status=status,
                )
            )
        else:
            results.append(_to_out(record, status))
    return results
