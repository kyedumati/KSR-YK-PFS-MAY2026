import enum
from datetime import date, datetime, time
from decimal import Decimal

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    Time,
    false,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base

MYSQL_TABLE = {
    "mysql_engine": "InnoDB",
    "mysql_charset": "utf8mb4",
    "mysql_collate": "utf8mb4_unicode_ci",
}


def _enum_values(enum_cls: type[enum.Enum]) -> list[str]:
    return [member.value for member in enum_cls]


def _enum_column(enum_cls: type[enum.Enum], length: int):
    return Enum(enum_cls, native_enum=False, length=length, values_callable=_enum_values)


def _file_name_check(column_name: str, *, nullable: bool) -> CheckConstraint:
    safe = (
        f"{column_name} NOT LIKE '%/%' "
        f"AND {column_name} NOT LIKE '%..%' "
        f"AND char_length({column_name}) > 0"
    )
    expression = f"{column_name} IS NULL OR ({safe})" if nullable else safe
    return CheckConstraint(expression, name=f"{column_name}_file")


class Role(enum.Enum):
    SYSTEM_ADMINISTRATOR = "System Administrator"
    HR_ADMINISTRATOR = "HR Administrator"
    MANAGER = "Manager"
    EMPLOYEE = "Employee"


class DocumentType(enum.Enum):
    ID_PROOF = "ID Proof"
    ADDRESS_PROOF = "Address Proof"
    EDUCATIONAL_CERTIFICATES = "Educational Certificates"
    EMPLOYMENT_AGREEMENTS = "Employment Agreements"
    TAX_DOCUMENTS = "Tax Documents"


class LeaveType(enum.Enum):
    CASUAL = "Casual Leave"
    SICK = "Sick Leave"
    EARNED = "Earned Leave"
    MATERNITY = "Maternity Leave"
    PATERNITY = "Paternity Leave"
    LOSS_OF_PAY = "Loss of Pay"


class LeaveStatus(enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class DayPortion(enum.Enum):
    FULL = "Full"
    HALF = "Half"


class ShiftType(enum.Enum):
    FIXED = "Fixed"
    ROTATIONAL = "Rotational"
    FLEXIBLE = "Flexible"


class ChecklistPurpose(enum.Enum):
    ONBOARDING = "Onboarding"
    OFFBOARDING = "Offboarding"


class PeriodType(enum.Enum):
    ANNUAL = "Annual"
    QUARTERLY = "Quarterly"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.current_timestamp(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp(),
        nullable=False,
    )


class BusinessUnit(TimestampMixin, Base):
    __tablename__ = "business_units"
    __table_args__ = (
        CheckConstraint("char_length(trim(name)) > 0", name="name_present"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))

    departments: Mapped[list["Department"]] = relationship(back_populates="business_unit")


class Department(TimestampMixin, Base):
    __tablename__ = "departments"
    __table_args__ = (
        CheckConstraint("char_length(trim(name)) > 0", name="name_present"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    business_unit_id: Mapped[int] = mapped_column(
        ForeignKey("business_units.id", ondelete="RESTRICT")
    )

    business_unit: Mapped[BusinessUnit] = relationship(back_populates="departments")
    employees: Mapped[list["Employee"]] = relationship(back_populates="department")


class Location(TimestampMixin, Base):
    __tablename__ = "locations"
    __table_args__ = (
        CheckConstraint("char_length(trim(name)) > 0", name="name_present"),
        CheckConstraint("char_length(trim(region)) > 0", name="region_present"),
        CheckConstraint("char_length(trim(timezone)) > 0", name="timezone_present"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    region: Mapped[str] = mapped_column(String(120))
    timezone: Mapped[str] = mapped_column(String(64))

    employees: Mapped[list["Employee"]] = relationship(back_populates="location")


class Designation(TimestampMixin, Base):
    __tablename__ = "designations"
    __table_args__ = (
        CheckConstraint("char_length(trim(title)) > 0", name="title_present"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))

    employees: Mapped[list["Employee"]] = relationship(back_populates="designation")


class Employee(TimestampMixin, Base):
    __tablename__ = "employees"
    __table_args__ = (
        CheckConstraint("char_length(trim(employee_code)) > 0", name="employee_code_present"),
        CheckConstraint("char_length(trim(name)) > 0", name="name_present"),
        CheckConstraint("locate('@', work_email) > 1", name="work_email_has_at"),
        _file_name_check("photo_stored_file_name", nullable=True),
        Index("ix_employees_name", "name"),
        Index("ix_employees_archived_activated", "archived", "activated"),
        Index("ix_employees_archived_at", "archived_at"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_code: Mapped[str] = mapped_column(String(60), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    work_email: Mapped[str] = mapped_column(String(254), unique=True)
    phone: Mapped[str | None] = mapped_column(String(32))
    address: Mapped[str | None] = mapped_column(Text())
    emergency_contact: Mapped[str | None] = mapped_column(Text())
    gender: Mapped[str | None] = mapped_column(String(32))
    date_of_birth: Mapped[date | None] = mapped_column(Date())
    employment_details: Mapped[str | None] = mapped_column(Text())
    department_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id", ondelete="RESTRICT"))
    designation_id: Mapped[int | None] = mapped_column(ForeignKey("designations.id", ondelete="RESTRICT"))
    location_id: Mapped[int | None] = mapped_column(ForeignKey("locations.id", ondelete="RESTRICT"))
    reporting_manager_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    photo_stored_file_name: Mapped[str | None] = mapped_column(String(255))
    activated: Mapped[bool] = mapped_column(Boolean(), default=False, server_default=false())
    activated_at: Mapped[datetime | None] = mapped_column(DateTime())
    archived: Mapped[bool] = mapped_column(Boolean(), default=False, server_default=false())
    archived_at: Mapped[datetime | None] = mapped_column(DateTime())

    department: Mapped[Department | None] = relationship(back_populates="employees")
    designation: Mapped[Designation | None] = relationship(back_populates="employees")
    location: Mapped[Location | None] = relationship(back_populates="employees")
    reporting_manager: Mapped["Employee | None"] = relationship(
        remote_side="Employee.id",
        back_populates="direct_reports",
        foreign_keys="Employee.reporting_manager_id",
    )
    direct_reports: Mapped[list["Employee"]] = relationship(
        back_populates="reporting_manager",
        foreign_keys="Employee.reporting_manager_id",
    )
    account: Mapped["Account | None"] = relationship(back_populates="employee")
    documents: Mapped[list["Document"]] = relationship(back_populates="employee")


class Account(TimestampMixin, Base):
    __tablename__ = "accounts"
    __table_args__ = (
        CheckConstraint("char_length(password_hash) >= 60", name="password_hash_length"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"), unique=True)
    role: Mapped[Role] = mapped_column(_enum_column(Role, 32))
    password_hash: Mapped[str] = mapped_column(String(255))

    employee: Mapped[Employee] = relationship(back_populates="account")


class Document(TimestampMixin, Base):
    __tablename__ = "documents"
    __table_args__ = (
        _file_name_check("stored_file_name", nullable=False),
        CheckConstraint("char_length(trim(original_file_name)) > 0", name="original_file_name_present"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    document_type: Mapped[DocumentType] = mapped_column(_enum_column(DocumentType, 40))
    stored_file_name: Mapped[str] = mapped_column(String(255))
    original_file_name: Mapped[str] = mapped_column(String(255))

    employee: Mapped[Employee] = relationship(back_populates="documents")


class LeavePolicy(TimestampMixin, Base):
    __tablename__ = "leave_policies"
    __table_args__ = (
        CheckConstraint("days_granted_per_year >= 0", name="days_granted_nonnegative"),
        CheckConstraint("carry_forward_maximum >= 0", name="carry_forward_nonnegative"),
        CheckConstraint("expiry_months >= 0", name="expiry_months_nonnegative"),
        CheckConstraint("grant_month BETWEEN 1 AND 12", name="grant_month_range"),
        CheckConstraint("grant_day BETWEEN 1 AND 31", name="grant_day_range"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    leave_type: Mapped[LeaveType] = mapped_column(_enum_column(LeaveType, 20), unique=True)
    days_granted_per_year: Mapped[Decimal] = mapped_column(Numeric(6, 1))
    carry_forward_maximum: Mapped[Decimal] = mapped_column(Numeric(6, 1))
    expiry_months: Mapped[int] = mapped_column(Integer())
    grant_month: Mapped[int] = mapped_column(Integer())
    grant_day: Mapped[int] = mapped_column(Integer())


class LeaveBalance(TimestampMixin, Base):
    __tablename__ = "leave_balances"
    __table_args__ = (
        CheckConstraint("granted_days >= 0", name="granted_days_nonnegative"),
        CheckConstraint("carried_days >= 0", name="carried_days_nonnegative"),
        CheckConstraint("used_days >= 0", name="used_days_nonnegative"),
        Index(
            "uq_leave_balances_employee_type_cycle",
            "employee_id",
            "leave_type",
            "cycle_start",
            unique=True,
        ),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    leave_type: Mapped[LeaveType] = mapped_column(_enum_column(LeaveType, 20))
    cycle_start: Mapped[date] = mapped_column(Date())
    granted_days: Mapped[Decimal] = mapped_column(Numeric(6, 1))
    carried_days: Mapped[Decimal] = mapped_column(Numeric(6, 1), default=Decimal("0.0"), server_default="0.0")
    carried_expires_on: Mapped[date | None] = mapped_column(Date())
    used_days: Mapped[Decimal] = mapped_column(Numeric(6, 1), default=Decimal("0.0"), server_default="0.0")


class LeaveRequest(TimestampMixin, Base):
    __tablename__ = "leave_requests"
    __table_args__ = (
        CheckConstraint("to_date >= from_date", name="date_order"),
        CheckConstraint("day_count > 0", name="day_count_positive"),
        CheckConstraint(
            "(day_portion = 'Full') OR (day_portion = 'Half' AND from_date = to_date)",
            name="half_day_same_date",
        ),
        CheckConstraint(
            "(status = 'Pending' AND decided_by_employee_id IS NULL AND decided_at IS NULL) "
            "OR (status <> 'Pending' AND decided_by_employee_id IS NOT NULL AND decided_at IS NOT NULL)",
            name="decision_matches_status",
        ),
        _file_name_check("supporting_stored_file_name", nullable=True),
        Index("ix_leave_requests_employee_dates", "employee_id", "from_date", "to_date"),
        Index("ix_leave_requests_status_from_date", "status", "from_date"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    leave_type: Mapped[LeaveType] = mapped_column(_enum_column(LeaveType, 20))
    from_date: Mapped[date] = mapped_column(Date())
    to_date: Mapped[date] = mapped_column(Date())
    day_portion: Mapped[DayPortion] = mapped_column(_enum_column(DayPortion, 8))
    day_count: Mapped[Decimal] = mapped_column(Numeric(6, 1))
    reason: Mapped[str | None] = mapped_column(Text())
    status: Mapped[LeaveStatus] = mapped_column(
        _enum_column(LeaveStatus, 16), default=LeaveStatus.PENDING, server_default=LeaveStatus.PENDING.value
    )
    supporting_stored_file_name: Mapped[str | None] = mapped_column(String(255))
    supporting_original_file_name: Mapped[str | None] = mapped_column(String(255))
    decided_by_employee_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    decided_at: Mapped[datetime | None] = mapped_column(DateTime())


class Shift(TimestampMixin, Base):
    __tablename__ = "shifts"
    __table_args__ = (
        CheckConstraint("char_length(trim(name)) > 0", name="name_present"),
        CheckConstraint("late_after_minutes >= 0", name="late_threshold_nonnegative"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    shift_type: Mapped[ShiftType] = mapped_column(_enum_column(ShiftType, 16))
    start_time: Mapped[time] = mapped_column(Time())
    end_time: Mapped[time] = mapped_column(Time())
    late_after_minutes: Mapped[int] = mapped_column(Integer())


class ShiftAssignment(TimestampMixin, Base):
    __tablename__ = "shift_assignments"
    __table_args__ = (
        Index("uq_shift_assignments_employee_date", "employee_id", "work_date", unique=True),
        Index("ix_shift_assignments_work_date", "work_date"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    shift_id: Mapped[int] = mapped_column(ForeignKey("shifts.id", ondelete="RESTRICT"))
    work_date: Mapped[date] = mapped_column(Date())


class AttendanceRecord(TimestampMixin, Base):
    __tablename__ = "attendance_records"
    __table_args__ = (
        CheckConstraint(
            "check_out_at IS NULL OR check_out_at >= check_in_at",
            name="checkout_after_checkin",
        ),
        Index("uq_attendance_records_employee_date", "employee_id", "work_date", unique=True),
        Index("ix_attendance_records_work_date", "work_date"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    work_date: Mapped[date] = mapped_column(Date())
    check_in_at: Mapped[datetime] = mapped_column(DateTime())
    check_out_at: Mapped[datetime | None] = mapped_column(DateTime())


class ChecklistTemplate(TimestampMixin, Base):
    __tablename__ = "checklist_templates"
    __table_args__ = (
        CheckConstraint("char_length(trim(name)) > 0", name="name_present"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    purpose: Mapped[ChecklistPurpose] = mapped_column(_enum_column(ChecklistPurpose, 16))

    items: Mapped[list["ChecklistTemplateItem"]] = relationship(back_populates="template")


class ChecklistTemplateItem(Base):
    __tablename__ = "checklist_template_items"
    __table_args__ = (
        CheckConstraint("char_length(trim(title)) > 0", name="title_present"),
        CheckConstraint("sort_order >= 0", name="sort_order_nonnegative"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("checklist_templates.id", ondelete="RESTRICT"))
    title: Mapped[str] = mapped_column(String(200))
    sort_order: Mapped[int] = mapped_column(Integer())

    template: Mapped[ChecklistTemplate] = relationship(back_populates="items")


class EmployeeChecklist(TimestampMixin, Base):
    __tablename__ = "employee_checklists"
    __table_args__ = (MYSQL_TABLE,)

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    template_id: Mapped[int | None] = mapped_column(ForeignKey("checklist_templates.id", ondelete="RESTRICT"))
    purpose: Mapped[ChecklistPurpose] = mapped_column(_enum_column(ChecklistPurpose, 16))

    items: Mapped[list["EmployeeChecklistItem"]] = relationship(back_populates="checklist")


class EmployeeChecklistItem(Base):
    __tablename__ = "employee_checklist_items"
    __table_args__ = (
        CheckConstraint("char_length(trim(title)) > 0", name="title_present"),
        CheckConstraint("sort_order >= 0", name="sort_order_nonnegative"),
        CheckConstraint(
            "(completed = 0 AND completed_at IS NULL AND completed_by_employee_id IS NULL) "
            "OR (completed = 1 AND completed_at IS NOT NULL AND completed_by_employee_id IS NOT NULL)",
            name="completion_fields",
        ),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    checklist_id: Mapped[int] = mapped_column(ForeignKey("employee_checklists.id", ondelete="RESTRICT"))
    title: Mapped[str] = mapped_column(String(200))
    sort_order: Mapped[int] = mapped_column(Integer())
    completed: Mapped[bool] = mapped_column(Boolean(), default=False, server_default=false())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime())
    completed_by_employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="RESTRICT")
    )

    checklist: Mapped[EmployeeChecklist] = relationship(back_populates="items")


class RatingScale(TimestampMixin, Base):
    __tablename__ = "rating_scales"
    __table_args__ = (
        CheckConstraint("char_length(trim(name)) > 0", name="name_present"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))

    levels: Mapped[list["RatingLevel"]] = relationship(back_populates="scale")


class RatingLevel(Base):
    __tablename__ = "rating_levels"
    __table_args__ = (
        CheckConstraint("char_length(trim(label)) > 0", name="label_present"),
        CheckConstraint("sort_order >= 0", name="sort_order_nonnegative"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    scale_id: Mapped[int] = mapped_column(ForeignKey("rating_scales.id", ondelete="RESTRICT"))
    label: Mapped[str] = mapped_column(String(80))
    sort_order: Mapped[int] = mapped_column(Integer())

    scale: Mapped[RatingScale] = relationship(back_populates="levels")


class Goal(TimestampMixin, Base):
    __tablename__ = "goals"
    __table_args__ = (
        CheckConstraint("char_length(trim(title)) > 0", name="title_present"),
        CheckConstraint("year_number BETWEEN 2000 AND 2100", name="year_range"),
        CheckConstraint(
            "(period_type = 'Annual' AND quarter_number = 0) "
            "OR (period_type = 'Quarterly' AND quarter_number BETWEEN 1 AND 4)",
            name="period_shape",
        ),
        Index("ix_goals_employee_period", "employee_id", "year_number", "quarter_number"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    assigned_by_employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    period_type: Mapped[PeriodType] = mapped_column(_enum_column(PeriodType, 16))
    year_number: Mapped[int] = mapped_column(Integer())
    quarter_number: Mapped[int] = mapped_column(Integer())
    title: Mapped[str] = mapped_column(String(200))
    progress: Mapped[str | None] = mapped_column(Text())


class PerformanceReview(TimestampMixin, Base):
    __tablename__ = "performance_reviews"
    __table_args__ = (
        CheckConstraint("year_number BETWEEN 2000 AND 2100", name="year_range"),
        CheckConstraint(
            "(period_type = 'Annual' AND quarter_number = 0) "
            "OR (period_type = 'Quarterly' AND quarter_number BETWEEN 1 AND 4)",
            name="period_shape",
        ),
        Index(
            "uq_performance_reviews_employee_period",
            "employee_id",
            "period_type",
            "year_number",
            "quarter_number",
            unique=True,
        ),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    manager_employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    period_type: Mapped[PeriodType] = mapped_column(_enum_column(PeriodType, 16))
    year_number: Mapped[int] = mapped_column(Integer())
    quarter_number: Mapped[int] = mapped_column(Integer())
    self_review: Mapped[str | None] = mapped_column(Text())
    manager_review: Mapped[str | None] = mapped_column(Text())
    rating_level_id: Mapped[int | None] = mapped_column(ForeignKey("rating_levels.id", ondelete="RESTRICT"))
    self_submitted_at: Mapped[datetime | None] = mapped_column(DateTime())
    manager_submitted_at: Mapped[datetime | None] = mapped_column(DateTime())


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (
        CheckConstraint("char_length(trim(body)) > 0", name="body_present"),
        Index("ix_notifications_recipient_created", "recipient_employee_id", "created_at"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    recipient_employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    body: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.current_timestamp(), nullable=False
    )
    read_at: Mapped[datetime | None] = mapped_column(DateTime())


class IntegrationRegistration(TimestampMixin, Base):
    __tablename__ = "integration_registrations"
    __table_args__ = (
        CheckConstraint("char_length(trim(system_name)) > 0", name="system_name_present"),
        CheckConstraint("char_length(trim(endpoint)) > 0", name="endpoint_present"),
        Index("ix_integration_registrations_system_name", "system_name"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    system_name: Mapped[str] = mapped_column(String(120))
    endpoint: Mapped[str] = mapped_column(String(500))
    is_connected: Mapped[bool] = mapped_column(Boolean(), default=False, server_default=false())


class AuditEvent(Base):
    __tablename__ = "audit_events"
    __table_args__ = (
        CheckConstraint("char_length(trim(action)) > 0", name="action_present"),
        CheckConstraint("char_length(trim(entity_name)) > 0", name="entity_name_present"),
        Index("ix_audit_events_entity", "entity_name", "entity_id"),
        Index("ix_audit_events_occurred_at", "occurred_at"),
        MYSQL_TABLE,
    )

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.current_timestamp(), nullable=False
    )
    actor_employee_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id", ondelete="RESTRICT"))
    action: Mapped[str] = mapped_column(String(80))
    entity_name: Mapped[str] = mapped_column(String(80))
    entity_id: Mapped[str | None] = mapped_column(String(64))
    detail: Mapped[dict | None] = mapped_column(JSON())
