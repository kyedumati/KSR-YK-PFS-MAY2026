import calendar
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import LeaveBalance, LeavePolicy, LeaveRequest, LeaveStatus, LeaveType

ZERO = Decimal("0.0")
HALF = Decimal("0.5")


def require_timezone(value: str) -> str:
    try:
        ZoneInfo(value)
    except ZoneInfoNotFoundError:
        raise HTTPException(status_code=422, detail="Timezone must be an IANA name, such as Asia/Kolkata.")
    return value


def require_grant_date(month: int, day: int) -> None:
    try:
        date(2001, month, day)
    except ValueError:
        raise HTTPException(status_code=422, detail="The grant date must exist in every year.")


def cycle_start_for(policy: LeavePolicy, today: date) -> date:
    this_year = date(today.year, policy.grant_month, policy.grant_day)
    if today >= this_year:
        return this_year
    return date(today.year - 1, policy.grant_month, policy.grant_day)


def add_months(value: date, months: int) -> date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(value.day, last_day))


def available_days(balance: LeaveBalance, on_date: date) -> Decimal:
    carried = balance.carried_days
    if balance.carried_expires_on is not None and balance.carried_expires_on < on_date:
        carried = ZERO
    return balance.granted_days + carried - balance.used_days


def ensure_balance(session: Session, employee_id: int, leave_type: LeaveType, today: date) -> LeaveBalance:
    policy = session.scalar(select(LeavePolicy).where(LeavePolicy.leave_type == leave_type))
    if policy is None:
        raise HTTPException(status_code=422, detail="This leave type has no policy yet.")
    start = cycle_start_for(policy, today)
    current = session.scalar(
        select(LeaveBalance).where(
            LeaveBalance.employee_id == employee_id,
            LeaveBalance.leave_type == leave_type,
            LeaveBalance.cycle_start == start,
        )
    )
    if current is not None:
        return current
    previous_start = date(start.year - 1, start.month, start.day)
    previous = session.scalar(
        select(LeaveBalance).where(
            LeaveBalance.employee_id == employee_id,
            LeaveBalance.leave_type == leave_type,
            LeaveBalance.cycle_start == previous_start,
        )
    )
    carried = ZERO
    expires_on = None
    if previous is not None:
        unused = available_days(previous, start)
        if unused < ZERO:
            unused = ZERO
        carried = min(unused, policy.carry_forward_maximum)
        if carried > ZERO:
            expires_on = start if policy.expiry_months == 0 else add_months(start, policy.expiry_months)
    created = LeaveBalance(
        employee_id=employee_id,
        leave_type=leave_type,
        cycle_start=start,
        granted_days=policy.days_granted_per_year,
        carried_days=carried,
        carried_expires_on=expires_on,
        used_days=ZERO,
    )
    session.add(created)
    session.flush()
    return created


def count_leave_days(from_date: date, to_date: date, portion_value: str) -> Decimal:
    if to_date < from_date:
        raise HTTPException(status_code=422, detail="The end date is before the start date.")
    if portion_value == "Half":
        if from_date != to_date:
            raise HTTPException(status_code=422, detail="A half day is allowed only when the start and end dates are the same.")
        return HALF
    return Decimal((to_date - from_date).days + 1)


def dates_overlap(existing: LeaveRequest, from_date: date, to_date: date) -> bool:
    return existing.from_date <= to_date and existing.to_date >= from_date


def assert_no_overlap(
    session: Session,
    employee_id: int,
    from_date: date,
    to_date: date,
    *,
    ignore_request_id: int | None = None,
) -> None:
    rows = session.scalars(
        select(LeaveRequest).where(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.status.in_([LeaveStatus.PENDING, LeaveStatus.APPROVED]),
        )
    ).all()
    for row in rows:
        if row.id == ignore_request_id:
            continue
        if dates_overlap(row, from_date, to_date):
            raise HTTPException(status_code=422, detail="These dates overlap another pending or approved request.")


def local_now(timezone_name: str) -> datetime:
    return datetime.now(ZoneInfo(timezone_name))


def utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def as_local(utc_naive: datetime, timezone_name: str) -> datetime:
    aware = utc_naive.replace(tzinfo=timezone.utc).astimezone(ZoneInfo(timezone_name))
    return aware.replace(tzinfo=None)


def is_late(check_in_utc: datetime, work_date: date, start_time, late_after_minutes: int, timezone_name: str) -> bool:
    local_check_in = as_local(check_in_utc, timezone_name)
    threshold = datetime.combine(work_date, start_time) + timedelta(minutes=late_after_minutes)
    return local_check_in > threshold


def overlap_day_count(request: LeaveRequest, start: date, end: date) -> Decimal:
    first = max(request.from_date, start)
    last = min(request.to_date, end)
    if last < first:
        return ZERO
    if request.day_portion.value == "Half":
        return HALF
    return Decimal((last - first).days + 1)
