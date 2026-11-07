from datetime import date, datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.audit import record_audit
from app.deps import get_current_account, get_session, is_hr, require_roles
from app.models import (
    Account,
    AttendanceRecord,
    ChecklistPurpose,
    ChecklistTemplate,
    ChecklistTemplateItem,
    Employee,
    EmployeeChecklist,
    EmployeeChecklistItem,
    Goal,
    IntegrationRegistration,
    LeavePolicy,
    LeaveRequest,
    LeaveStatus,
    Location,
    Notification,
    PerformanceReview,
    PeriodType,
    RatingLevel,
    RatingScale,
    Role,
    Shift,
    ShiftAssignment,
)
from app.rules import available_days, ensure_balance, is_late, overlap_day_count

router = APIRouter(tags=["operations"])
hr_roles = require_roles(Role.SYSTEM_ADMINISTRATOR, Role.HR_ADMINISTRATOR)
system_admin = require_roles(Role.SYSTEM_ADMINISTRATOR)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class TemplateItemIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    sort_order: int = Field(ge=0)


class TemplateIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    purpose: ChecklistPurpose
    items: list[TemplateItemIn]


class TemplateItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    sort_order: int


class TemplateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    purpose: ChecklistPurpose
    items: list[TemplateItemOut]


class ChecklistItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    sort_order: int
    completed: bool


class ChecklistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    purpose: ChecklistPurpose
    items: list[ChecklistItemOut]


class AssignChecklistIn(BaseModel):
    template_id: int


class RatingLevelIn(BaseModel):
    label: str = Field(min_length=1, max_length=80)
    sort_order: int = Field(ge=0)


class RatingScaleIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    levels: list[RatingLevelIn]


class RatingLevelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    label: str
    sort_order: int


class RatingScaleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    levels: list[RatingLevelOut]


class GoalIn(BaseModel):
    employee_id: int
    period_type: PeriodType
    year_number: int = Field(ge=2000, le=2100)
    quarter_number: int = Field(ge=0, le=4)
    title: str = Field(min_length=1, max_length=200)


class GoalProgress(BaseModel):
    progress: str = Field(min_length=1)


class GoalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    assigned_by_employee_id: int
    period_type: PeriodType
    year_number: int
    quarter_number: int
    title: str
    progress: str | None


class SelfReviewIn(BaseModel):
    period_type: PeriodType
    year_number: int = Field(ge=2000, le=2100)
    quarter_number: int = Field(ge=0, le=4)
    self_review: str = Field(min_length=1)


class ManagerReviewIn(BaseModel):
    manager_review: str = Field(min_length=1)
    rating_level_id: int


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    manager_employee_id: int
    period_type: PeriodType
    year_number: int
    quarter_number: int
    self_review: str | None
    manager_review: str | None
    rating_level_id: int | None


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    body: str
    created_at: datetime
    read_at: datetime | None


class IntegrationIn(BaseModel):
    system_name: str = Field(min_length=1, max_length=120)
    endpoint: str = Field(min_length=1, max_length=500)


class IntegrationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    system_name: str
    endpoint: str
    is_connected: bool


class CountReport(BaseModel):
    count: int


class DaysReport(BaseModel):
    days: Decimal


def _direct_report(session: Session, manager_id: int, employee_id: int) -> Employee:
    employee = session.get(Employee, employee_id)
    if employee is None or employee.reporting_manager_id != manager_id:
        raise HTTPException(status_code=403, detail="That employee is not one of your direct reports.")
    return employee


def _validate_period(period_type: PeriodType, quarter_number: int) -> None:
    if period_type == PeriodType.ANNUAL and quarter_number != 0:
        raise HTTPException(status_code=422, detail="An annual period uses quarter 0.")
    if period_type == PeriodType.QUARTERLY and quarter_number not in {1, 2, 3, 4}:
        raise HTTPException(status_code=422, detail="A quarterly period uses quarter 1, 2, 3, or 4.")


@router.post("/checklist-templates", response_model=TemplateOut, status_code=201)
def create_template(
    body: TemplateIn,
    session: Session = Depends(get_session),
    account: Account = Depends(hr_roles),
) -> ChecklistTemplate:
    template = ChecklistTemplate(name=body.name.strip(), purpose=body.purpose)
    session.add(template)
    session.flush()
    for item in body.items:
        session.add(
            ChecklistTemplateItem(
                template_id=template.id,
                title=item.title.strip(),
                sort_order=item.sort_order,
            )
        )
    session.flush()
    record_audit(session, actor_employee_id=account.employee_id, action="create", entity_name="checklist_templates", entity_id=str(template.id))
    return session.scalar(
        select(ChecklistTemplate).options(selectinload(ChecklistTemplate.items)).where(ChecklistTemplate.id == template.id)
    )


@router.get("/checklist-templates", response_model=list[TemplateOut])
def list_templates(
    session: Session = Depends(get_session),
    _: Account = Depends(hr_roles),
) -> list[ChecklistTemplate]:
    return list(session.scalars(select(ChecklistTemplate).options(selectinload(ChecklistTemplate.items)).order_by(ChecklistTemplate.id)))


@router.post("/employees/{employee_id}/checklists", response_model=ChecklistOut, status_code=201)
def assign_checklist(
    employee_id: int,
    body: AssignChecklistIn,
    session: Session = Depends(get_session),
    account: Account = Depends(hr_roles),
) -> EmployeeChecklist:
    if session.get(Employee, employee_id) is None:
        raise HTTPException(status_code=404, detail="Employee not found.")
    template = session.scalar(
        select(ChecklistTemplate).options(selectinload(ChecklistTemplate.items)).where(ChecklistTemplate.id == body.template_id)
    )
    if template is None:
        raise HTTPException(status_code=404, detail="Checklist template not found.")
    checklist = EmployeeChecklist(employee_id=employee_id, template_id=template.id, purpose=template.purpose)
    session.add(checklist)
    session.flush()
    for item in template.items:
        session.add(
            EmployeeChecklistItem(
                checklist_id=checklist.id,
                title=item.title,
                sort_order=item.sort_order,
                completed=False,
            )
        )
    session.flush()
    record_audit(session, actor_employee_id=account.employee_id, action="assign", entity_name="employee_checklists", entity_id=str(checklist.id))
    return session.scalar(
        select(EmployeeChecklist).options(selectinload(EmployeeChecklist.items)).where(EmployeeChecklist.id == checklist.id)
    )


@router.get("/employees/{employee_id}/checklists", response_model=list[ChecklistOut])
def list_checklists(
    employee_id: int,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> list[EmployeeChecklist]:
    employee = session.get(Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found.")
    allowed = is_hr(account) or account.employee_id == employee_id
    if account.role == Role.MANAGER and employee.reporting_manager_id == account.employee_id:
        allowed = True
    if not allowed:
        raise HTTPException(status_code=403, detail="You do not have access to these checklists.")
    return list(
        session.scalars(
            select(EmployeeChecklist)
            .options(selectinload(EmployeeChecklist.items))
            .where(EmployeeChecklist.employee_id == employee_id)
            .order_by(EmployeeChecklist.id)
        )
    )


@router.post("/checklist-items/{item_id}/complete", response_model=ChecklistItemOut)
def complete_checklist_item(
    item_id: int,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> EmployeeChecklistItem:
    item = session.get(EmployeeChecklistItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Checklist item not found.")
    checklist = session.get(EmployeeChecklist, item.checklist_id)
    employee = session.get(Employee, checklist.employee_id) if checklist else None
    allowed = is_hr(account) or (
        account.role == Role.MANAGER and employee is not None and employee.reporting_manager_id == account.employee_id
    )
    if not allowed:
        raise HTTPException(status_code=403, detail="You do not have access to this checklist item.")
    item.completed = True
    item.completed_at = _utcnow()
    item.completed_by_employee_id = account.employee_id
    return item


@router.post("/rating-scales", response_model=RatingScaleOut, status_code=201)
def create_rating_scale(
    body: RatingScaleIn,
    session: Session = Depends(get_session),
    account: Account = Depends(hr_roles),
) -> RatingScale:
    scale = RatingScale(name=body.name.strip())
    session.add(scale)
    session.flush()
    for level in body.levels:
        session.add(RatingLevel(scale_id=scale.id, label=level.label.strip(), sort_order=level.sort_order))
    session.flush()
    record_audit(session, actor_employee_id=account.employee_id, action="create", entity_name="rating_scales", entity_id=str(scale.id))
    return session.scalar(select(RatingScale).options(selectinload(RatingScale.levels)).where(RatingScale.id == scale.id))


@router.get("/rating-scales", response_model=list[RatingScaleOut])
def list_rating_scales(
    session: Session = Depends(get_session),
    _: Account = Depends(get_current_account),
) -> list[RatingScale]:
    return list(session.scalars(select(RatingScale).options(selectinload(RatingScale.levels)).order_by(RatingScale.id)))


@router.post("/goals", response_model=GoalOut, status_code=201)
def assign_goal(
    body: GoalIn,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> Goal:
    if account.role != Role.MANAGER:
        raise HTTPException(status_code=403, detail="Only a manager can assign a goal.")
    _validate_period(body.period_type, body.quarter_number)
    _direct_report(session, account.employee_id, body.employee_id)
    goal = Goal(
        employee_id=body.employee_id,
        assigned_by_employee_id=account.employee_id,
        period_type=body.period_type,
        year_number=body.year_number,
        quarter_number=body.quarter_number,
        title=body.title.strip(),
    )
    session.add(goal)
    session.flush()
    record_audit(session, actor_employee_id=account.employee_id, action="create", entity_name="goals", entity_id=str(goal.id))
    return goal


@router.get("/goals", response_model=list[GoalOut])
def list_goals(
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> list[Goal]:
    query = select(Goal).order_by(Goal.id)
    if is_hr(account):
        return list(session.scalars(query))
    if account.role == Role.MANAGER:
        report_ids = select(Employee.id).where(Employee.reporting_manager_id == account.employee_id)
        return list(session.scalars(query.where((Goal.employee_id == account.employee_id) | Goal.employee_id.in_(report_ids))))
    return list(session.scalars(query.where(Goal.employee_id == account.employee_id)))


@router.patch("/goals/{goal_id}/progress", response_model=GoalOut)
def update_goal_progress(
    goal_id: int,
    body: GoalProgress,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> Goal:
    goal = session.get(Goal, goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found.")
    if goal.employee_id != account.employee_id:
        raise HTTPException(status_code=403, detail="You can update progress only on your own goal.")
    goal.progress = body.progress.strip()
    return goal


def _review_for_period(session: Session, employee_id: int, period_type: PeriodType, year_number: int, quarter_number: int) -> PerformanceReview | None:
    return session.scalar(
        select(PerformanceReview).where(
            PerformanceReview.employee_id == employee_id,
            PerformanceReview.period_type == period_type,
            PerformanceReview.year_number == year_number,
            PerformanceReview.quarter_number == quarter_number,
        )
    )


@router.post("/reviews/self", response_model=ReviewOut)
def submit_self_review(
    body: SelfReviewIn,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> PerformanceReview:
    _validate_period(body.period_type, body.quarter_number)
    employee = account.employee
    if employee.reporting_manager_id is None:
        raise HTTPException(status_code=422, detail="A reporting manager is required before a review.")
    review = _review_for_period(session, employee.id, body.period_type, body.year_number, body.quarter_number)
    if review is None:
        review = PerformanceReview(
            employee_id=employee.id,
            manager_employee_id=employee.reporting_manager_id,
            period_type=body.period_type,
            year_number=body.year_number,
            quarter_number=body.quarter_number,
        )
        session.add(review)
    review.self_review = body.self_review.strip()
    review.self_submitted_at = _utcnow()
    session.flush()
    return review


@router.post("/reviews/{review_id}/manager", response_model=ReviewOut)
def submit_manager_review(
    review_id: int,
    body: ManagerReviewIn,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> PerformanceReview:
    if account.role != Role.MANAGER:
        raise HTTPException(status_code=403, detail="Only a manager can submit this review.")
    review = session.get(PerformanceReview, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found.")
    _direct_report(session, account.employee_id, review.employee_id)
    if session.get(RatingLevel, body.rating_level_id) is None:
        raise HTTPException(status_code=422, detail="Rating level not found.")
    review.manager_employee_id = account.employee_id
    review.manager_review = body.manager_review.strip()
    review.rating_level_id = body.rating_level_id
    review.manager_submitted_at = _utcnow()
    record_audit(session, actor_employee_id=account.employee_id, action="rate", entity_name="performance_reviews", entity_id=str(review.id))
    return review


@router.get("/notifications", response_model=list[NotificationOut])
def list_notifications(
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> list[Notification]:
    return list(
        session.scalars(
            select(Notification)
            .where(Notification.recipient_employee_id == account.employee_id)
            .order_by(Notification.created_at.desc(), Notification.id.desc())
        )
    )


@router.post("/notifications/{notification_id}/read", response_model=NotificationOut)
def mark_notification_read(
    notification_id: int,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> Notification:
    row = session.get(Notification, notification_id)
    if row is None or row.recipient_employee_id != account.employee_id:
        raise HTTPException(status_code=404, detail="Notification not found.")
    if row.read_at is None:
        row.read_at = _utcnow()
    return row


@router.get("/integrations", response_model=list[IntegrationOut])
def list_integrations(
    session: Session = Depends(get_session),
    _: Account = Depends(system_admin),
) -> list[IntegrationRegistration]:
    return list(session.scalars(select(IntegrationRegistration).order_by(IntegrationRegistration.id)))


@router.post("/integrations", response_model=IntegrationOut, status_code=201)
def register_integration(
    body: IntegrationIn,
    session: Session = Depends(get_session),
    account: Account = Depends(system_admin),
) -> IntegrationRegistration:
    row = IntegrationRegistration(system_name=body.system_name.strip(), endpoint=body.endpoint.strip(), is_connected=False)
    session.add(row)
    session.flush()
    record_audit(session, actor_employee_id=account.employee_id, action="register", entity_name="integration_registrations", entity_id=str(row.id))
    return row


@router.get("/reports/headcount", response_model=CountReport)
def headcount(
    session: Session = Depends(get_session),
    _: Account = Depends(hr_roles),
) -> CountReport:
    count = session.scalar(
        select(func.count()).select_from(Employee).where(Employee.activated.is_(True), Employee.archived.is_(False))
    )
    return CountReport(count=int(count or 0))


@router.get("/reports/attrition", response_model=CountReport)
def attrition(
    start: date = Query(),
    end: date = Query(),
    session: Session = Depends(get_session),
    _: Account = Depends(hr_roles),
) -> CountReport:
    count = session.scalar(
        select(func.count())
        .select_from(Employee)
        .where(
            Employee.archived.is_(True),
            Employee.archived_at.is_not(None),
            func.date(Employee.archived_at) >= start,
            func.date(Employee.archived_at) <= end,
        )
    )
    return CountReport(count=int(count or 0))


@router.get("/reports/leave-utilization", response_model=DaysReport)
def leave_utilization(
    start: date = Query(),
    end: date = Query(),
    session: Session = Depends(get_session),
    _: Account = Depends(hr_roles),
) -> DaysReport:
    rows = session.scalars(
        select(LeaveRequest).where(
            LeaveRequest.status == LeaveStatus.APPROVED,
            LeaveRequest.from_date <= end,
            LeaveRequest.to_date >= start,
        )
    ).all()
    total = sum((overlap_day_count(row, start, end) for row in rows), Decimal("0.0"))
    return DaysReport(days=total)


@router.get("/reports/leave-liability", response_model=DaysReport)
def leave_liability(
    session: Session = Depends(get_session),
    _: Account = Depends(hr_roles),
) -> DaysReport:
    today = date.today()
    employees = session.scalars(select(Employee.id).where(Employee.archived.is_(False))).all()
    policies = session.scalars(select(LeavePolicy)).all()
    total = Decimal("0.0")
    for employee_id in employees:
        for policy in policies:
            balance = ensure_balance(session, employee_id, policy.leave_type, today)
            remaining = available_days(balance, today)
            if remaining > 0:
                total += remaining
    return DaysReport(days=total)


@router.get("/reports/late-arrivals", response_model=CountReport)
def late_arrivals(
    start: date = Query(),
    end: date = Query(),
    session: Session = Depends(get_session),
    _: Account = Depends(hr_roles),
) -> CountReport:
    rows = session.scalars(
        select(AttendanceRecord).where(AttendanceRecord.work_date >= start, AttendanceRecord.work_date <= end)
    ).all()
    count = 0
    for record in rows:
        employee = session.get(Employee, record.employee_id)
        location = session.get(Location, employee.location_id) if employee and employee.location_id else None
        if location is None:
            continue
        assignment = session.scalar(
            select(ShiftAssignment).where(
                ShiftAssignment.employee_id == record.employee_id,
                ShiftAssignment.work_date == record.work_date,
            )
        )
        if assignment is None:
            continue
        shift = session.get(Shift, assignment.shift_id)
        if shift and is_late(record.check_in_at, record.work_date, shift.start_time, shift.late_after_minutes, location.timezone):
            count += 1
    return CountReport(count=count)


@router.get("/reports/team-performance", response_model=list[ReviewOut])
def team_performance(
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> list[PerformanceReview]:
    if account.role != Role.MANAGER:
        raise HTTPException(status_code=403, detail="Only a manager can view this report.")
    report_ids = select(Employee.id).where(Employee.reporting_manager_id == account.employee_id)
    return list(session.scalars(select(PerformanceReview).where(PerformanceReview.employee_id.in_(report_ids)).order_by(PerformanceReview.id)))
