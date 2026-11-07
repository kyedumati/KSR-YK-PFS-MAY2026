from datetime import date, datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import record_audit
from app.deps import get_current_account, get_session, is_hr, require_active_employee, require_roles
from app.files import save_upload
from app.models import (
    Account,
    DayPortion,
    Employee,
    LeavePolicy,
    LeaveRequest,
    LeaveStatus,
    LeaveType,
    Notification,
    Role,
)
from app.rules import assert_no_overlap, available_days, count_leave_days, ensure_balance, require_grant_date

router = APIRouter(tags=["leave"])
hr_roles = require_roles(Role.SYSTEM_ADMINISTRATOR, Role.HR_ADMINISTRATOR)


class LeavePolicyIn(BaseModel):
    leave_type: LeaveType
    days_granted_per_year: Decimal = Field(ge=0)
    carry_forward_maximum: Decimal = Field(ge=0)
    expiry_months: int = Field(ge=0)
    grant_month: int = Field(ge=1, le=12)
    grant_day: int = Field(ge=1, le=31)


class LeavePolicyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    leave_type: LeaveType
    days_granted_per_year: Decimal
    carry_forward_maximum: Decimal
    expiry_months: int
    grant_month: int
    grant_day: int


class LeaveRequestIn(BaseModel):
    leave_type: LeaveType
    from_date: date
    to_date: date
    day_portion: DayPortion = DayPortion.FULL
    reason: str | None = None


class LeaveRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    leave_type: LeaveType
    from_date: date
    to_date: date
    day_portion: DayPortion
    day_count: Decimal
    reason: str | None
    status: LeaveStatus


class DecisionIn(BaseModel):
    status: LeaveStatus


class BalanceOut(BaseModel):
    leave_type: LeaveType
    available_days: Decimal


def _notify(session: Session, recipient_id: int, body: str) -> None:
    session.add(Notification(recipient_employee_id=recipient_id, body=body))


def _visible_requests(session: Session, account: Account) -> list[LeaveRequest]:
    query = select(LeaveRequest).order_by(LeaveRequest.id.desc())
    if is_hr(account):
        return list(session.scalars(query))
    if account.role == Role.MANAGER:
        report_ids = select(Employee.id).where(Employee.reporting_manager_id == account.employee_id)
        return list(
            session.scalars(
                query.where(
                    (LeaveRequest.employee_id == account.employee_id)
                    | (LeaveRequest.employee_id.in_(report_ids))
                )
            )
        )
    return list(session.scalars(query.where(LeaveRequest.employee_id == account.employee_id)))


@router.get("/leave-policies", response_model=list[LeavePolicyOut])
def list_policies(
    session: Session = Depends(get_session),
    _: Account = Depends(get_current_account),
) -> list[LeavePolicy]:
    return list(session.scalars(select(LeavePolicy).order_by(LeavePolicy.leave_type)))


@router.put("/leave-policies", response_model=LeavePolicyOut)
def save_policy(
    body: LeavePolicyIn,
    session: Session = Depends(get_session),
    account: Account = Depends(hr_roles),
) -> LeavePolicy:
    require_grant_date(body.grant_month, body.grant_day)
    policy = session.scalar(select(LeavePolicy).where(LeavePolicy.leave_type == body.leave_type))
    if policy is None:
        policy = LeavePolicy(leave_type=body.leave_type)
        session.add(policy)
    policy.days_granted_per_year = body.days_granted_per_year
    policy.carry_forward_maximum = body.carry_forward_maximum
    policy.expiry_months = body.expiry_months
    policy.grant_month = body.grant_month
    policy.grant_day = body.grant_day
    session.flush()
    record_audit(
        session,
        actor_employee_id=account.employee_id,
        action="save",
        entity_name="leave_policies",
        entity_id=str(policy.id),
        detail={"leave_type": body.leave_type.value},
    )
    return policy


@router.get("/leave-balances/me", response_model=list[BalanceOut])
def my_balances(
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> list[BalanceOut]:
    today = date.today()
    policies = session.scalars(select(LeavePolicy)).all()
    results = []
    for policy in policies:
        balance = ensure_balance(session, account.employee_id, policy.leave_type, today)
        results.append(
            BalanceOut(leave_type=policy.leave_type, available_days=available_days(balance, today))
        )
    return results


@router.get("/leave-requests", response_model=list[LeaveRequestOut])
def list_requests(
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> list[LeaveRequest]:
    return _visible_requests(session, account)


@router.post("/leave-requests", response_model=LeaveRequestOut, status_code=201)
def create_request(
    body: LeaveRequestIn,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> LeaveRequest:
    employee = account.employee
    require_active_employee(employee)
    if employee.reporting_manager_id is None:
        raise HTTPException(status_code=422, detail="A reporting manager is required before requesting leave.")
    day_count = count_leave_days(body.from_date, body.to_date, body.day_portion.value)
    assert_no_overlap(session, employee.id, body.from_date, body.to_date)
    balance = ensure_balance(session, employee.id, body.leave_type, body.from_date)
    if available_days(balance, body.from_date) < day_count:
        raise HTTPException(status_code=422, detail="The request is larger than the remaining balance.")
    request = LeaveRequest(
        employee_id=employee.id,
        leave_type=body.leave_type,
        from_date=body.from_date,
        to_date=body.to_date,
        day_portion=body.day_portion,
        day_count=day_count,
        reason=body.reason,
        status=LeaveStatus.PENDING,
    )
    session.add(request)
    session.flush()
    _notify(
        session,
        employee.reporting_manager_id,
        f"{employee.name} requested {body.leave_type.value} from {body.from_date.isoformat()} to {body.to_date.isoformat()}.",
    )
    record_audit(
        session,
        actor_employee_id=employee.id,
        action="create",
        entity_name="leave_requests",
        entity_id=str(request.id),
    )
    return request


@router.patch("/leave-requests/{request_id}", response_model=LeaveRequestOut)
def edit_request(
    request_id: int,
    body: LeaveRequestIn,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> LeaveRequest:
    request = session.get(LeaveRequest, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Leave request not found.")
    if request.employee_id != account.employee_id:
        raise HTTPException(status_code=403, detail="You can edit only your own request.")
    if request.status != LeaveStatus.PENDING:
        raise HTTPException(status_code=422, detail="Only a pending request can be edited.")
    day_count = count_leave_days(body.from_date, body.to_date, body.day_portion.value)
    assert_no_overlap(session, request.employee_id, body.from_date, body.to_date, ignore_request_id=request.id)
    balance = ensure_balance(session, request.employee_id, body.leave_type, body.from_date)
    if available_days(balance, body.from_date) < day_count:
        raise HTTPException(status_code=422, detail="The request is larger than the remaining balance.")
    request.leave_type = body.leave_type
    request.from_date = body.from_date
    request.to_date = body.to_date
    request.day_portion = body.day_portion
    request.day_count = day_count
    request.reason = body.reason
    manager_id = account.employee.reporting_manager_id
    if manager_id is not None:
        _notify(session, manager_id, f"{account.employee.name} updated a pending leave request.")
    return request


@router.delete("/leave-requests/{request_id}", status_code=204)
def cancel_request(
    request_id: int,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> None:
    request = session.get(LeaveRequest, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Leave request not found.")
    if request.employee_id != account.employee_id:
        raise HTTPException(status_code=403, detail="You can cancel only your own request.")
    if request.status != LeaveStatus.PENDING:
        raise HTTPException(status_code=422, detail="Only a pending request can be cancelled.")
    manager_id = account.employee.reporting_manager_id
    session.delete(request)
    if manager_id is not None:
        _notify(session, manager_id, f"{account.employee.name} cancelled a pending leave request.")


@router.post("/leave-requests/{request_id}/decision", response_model=LeaveRequestOut)
def decide_request(
    request_id: int,
    body: DecisionIn,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> LeaveRequest:
    if body.status == LeaveStatus.PENDING:
        raise HTTPException(status_code=422, detail="Choose approved or rejected.")
    request = session.get(LeaveRequest, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Leave request not found.")
    if request.status != LeaveStatus.PENDING:
        raise HTTPException(status_code=422, detail="This request has already been decided.")
    employee = session.get(Employee, request.employee_id)
    if employee is None or employee.reporting_manager_id != account.employee_id or account.role != Role.MANAGER:
        raise HTTPException(status_code=403, detail="Only the reporting manager can decide this request.")
    if body.status == LeaveStatus.APPROVED:
        balance = ensure_balance(session, request.employee_id, request.leave_type, request.from_date)
        if available_days(balance, request.from_date) < request.day_count:
            raise HTTPException(status_code=422, detail="The request is larger than the remaining balance.")
        balance.used_days += request.day_count
    request.status = body.status
    request.decided_by_employee_id = account.employee_id
    request.decided_at = datetime.now(timezone.utc).replace(tzinfo=None)
    outcome = "approved" if body.status == LeaveStatus.APPROVED else "rejected"
    _notify(session, request.employee_id, f"Your leave request was {outcome}.")
    record_audit(
        session,
        actor_employee_id=account.employee_id,
        action=outcome,
        entity_name="leave_requests",
        entity_id=str(request.id),
    )
    return request


@router.post("/leave-requests/{request_id}/supporting-document", response_model=LeaveRequestOut)
def upload_supporting_document(
    request_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> LeaveRequest:
    request = session.get(LeaveRequest, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Leave request not found.")
    if request.employee_id != account.employee_id:
        raise HTTPException(status_code=403, detail="You can attach a file only to your own request.")
    if request.status != LeaveStatus.PENDING:
        raise HTTPException(status_code=422, detail="Only a pending request can receive a file.")
    stored, original = save_upload(file)
    request.supporting_stored_file_name = stored
    request.supporting_original_file_name = original
    return request
