from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.audit import record_audit
from app.deps import get_current_account, get_session, is_hr, require_roles
from app.files import delete_stored, save_upload, stored_path
from app.models import (
    Account,
    BusinessUnit,
    Department,
    Designation,
    Document,
    DocumentType,
    Employee,
    Location,
    Role,
)
from app.security import hash_password

router = APIRouter(tags=["employees"])
hr_roles = require_roles(Role.SYSTEM_ADMINISTRATOR, Role.HR_ADMINISTRATOR)


class EmployeeCreate(BaseModel):
    employee_code: str = Field(min_length=1, max_length=60)
    name: str = Field(min_length=1, max_length=200)
    work_email: str = Field(min_length=3, max_length=254)
    password: str
    role: Role
    phone: str | None = Field(default=None, max_length=32)
    address: str | None = None
    emergency_contact: str | None = None
    gender: str | None = Field(default=None, max_length=32)
    date_of_birth: date | None = None
    employment_details: str | None = None
    department_id: int | None = None
    designation_id: int | None = None
    location_id: int | None = None
    reporting_manager_id: int | None = None


class EmployeeHrUpdate(BaseModel):
    employee_code: str | None = Field(default=None, min_length=1, max_length=60)
    name: str | None = Field(default=None, min_length=1, max_length=200)
    work_email: str | None = Field(default=None, min_length=3, max_length=254)
    role: Role | None = None
    phone: str | None = Field(default=None, max_length=32)
    address: str | None = None
    emergency_contact: str | None = None
    gender: str | None = Field(default=None, max_length=32)
    date_of_birth: date | None = None
    employment_details: str | None = None
    department_id: int | None = None
    designation_id: int | None = None
    location_id: int | None = None
    reporting_manager_id: int | None = None


class SelfUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    phone: str | None = Field(default=None, max_length=32)
    address: str | None = None
    emergency_contact: str | None = None


class EmployeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_code: str
    name: str
    work_email: str
    phone: str | None
    address: str | None
    emergency_contact: str | None
    gender: str | None
    date_of_birth: date | None
    employment_details: str | None
    department_id: int | None
    designation_id: int | None
    location_id: int | None
    reporting_manager_id: int | None
    role: str
    activated: bool
    archived: bool
    photo_url: str | None = None


class WorkCard(BaseModel):
    id: int
    employee_code: str
    name: str
    work_email: str
    designation: str | None
    department: str | None
    business_unit: str | None
    location: str | None
    photo_url: str | None


class ChartNode(WorkCard):
    reports: list["ChartNode"]


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    document_type: DocumentType
    original_file_name: str


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _load_employee(session: Session, employee_id: int) -> Employee:
    employee = session.scalar(
        select(Employee)
        .options(
            selectinload(Employee.account),
            selectinload(Employee.department).selectinload(Department.business_unit),
            selectinload(Employee.designation),
            selectinload(Employee.location),
        )
        .where(Employee.id == employee_id)
    )
    if employee is None or employee.account is None:
        raise HTTPException(status_code=404, detail="Employee not found.")
    return employee


def _can_read_profile(account: Account, employee: Employee) -> bool:
    if account.employee_id == employee.id or is_hr(account):
        return True
    return account.role == Role.MANAGER and employee.reporting_manager_id == account.employee_id


def _to_out(employee: Employee) -> EmployeeOut:
    return EmployeeOut(
        id=employee.id,
        employee_code=employee.employee_code,
        name=employee.name,
        work_email=employee.work_email,
        phone=employee.phone,
        address=employee.address,
        emergency_contact=employee.emergency_contact,
        gender=employee.gender,
        date_of_birth=employee.date_of_birth,
        employment_details=employee.employment_details,
        department_id=employee.department_id,
        designation_id=employee.designation_id,
        location_id=employee.location_id,
        reporting_manager_id=employee.reporting_manager_id,
        role=employee.account.role.value,
        activated=employee.activated,
        archived=employee.archived,
        photo_url=f"/employees/{employee.id}/photo" if employee.photo_stored_file_name else None,
    )


def _work_card(employee: Employee) -> WorkCard:
    department = employee.department
    return WorkCard(
        id=employee.id,
        employee_code=employee.employee_code,
        name=employee.name,
        work_email=employee.work_email,
        designation=employee.designation.title if employee.designation else None,
        department=department.name if department else None,
        business_unit=department.business_unit.name if department and department.business_unit else None,
        location=employee.location.name if employee.location else None,
        photo_url=f"/employees/{employee.id}/photo" if employee.photo_stored_file_name else None,
    )


def _require_fk(session: Session, model, record_id: int | None, label: str) -> None:
    if record_id is not None and session.get(model, record_id) is None:
        raise HTTPException(status_code=422, detail=f"{label} not found.")


def _assert_manager(session: Session, employee_id: int | None, manager_id: int | None) -> None:
    if manager_id is None:
        return
    if employee_id is not None and manager_id == employee_id:
        raise HTTPException(status_code=422, detail="An employee cannot report to themselves.")
    seen: set[int] = set()
    current = manager_id
    while current is not None:
        if employee_id is not None and current == employee_id:
            raise HTTPException(status_code=422, detail="That reporting manager creates a cycle.")
        if current in seen:
            break
        seen.add(current)
        manager = session.get(Employee, current)
        if manager is None:
            raise HTTPException(status_code=422, detail="Reporting manager not found.")
        current = manager.reporting_manager_id


def _apply_hr_fields(session: Session, employee: Employee, body: EmployeeHrUpdate | EmployeeCreate) -> None:
    data = body.model_dump(exclude_unset=True)
    _require_fk(session, Department, data.get("department_id", employee.department_id), "Department")
    _require_fk(session, Designation, data.get("designation_id", employee.designation_id), "Designation")
    _require_fk(session, Location, data.get("location_id", employee.location_id), "Location")
    if "reporting_manager_id" in data:
        _assert_manager(session, employee.id, data["reporting_manager_id"])
    for field in (
        "employee_code",
        "name",
        "work_email",
        "phone",
        "address",
        "emergency_contact",
        "gender",
        "employment_details",
        "department_id",
        "designation_id",
        "location_id",
        "reporting_manager_id",
    ):
        if field in data and data[field] is not None and isinstance(data[field], str):
            setattr(employee, field, data[field].strip())
        elif field in data:
            setattr(employee, field, data[field])
    if "date_of_birth" in data:
        employee.date_of_birth = data["date_of_birth"]


@router.post("/employees", response_model=EmployeeOut, status_code=201)
def create_employee(
    body: EmployeeCreate,
    session: Session = Depends(get_session),
    account: Account = Depends(hr_roles),
) -> EmployeeOut:
    employee = Employee(
        employee_code=body.employee_code.strip(),
        name=body.name.strip(),
        work_email=body.work_email.strip(),
        activated=False,
        archived=False,
    )
    _apply_hr_fields(session, employee, body)
    session.add(employee)
    session.flush()
    session.add(
        Account(
            employee_id=employee.id,
            role=body.role,
            password_hash=hash_password(body.password),
        )
    )
    session.flush()
    record_audit(
        session,
        actor_employee_id=account.employee_id,
        action="create",
        entity_name="employees",
        entity_id=str(employee.id),
        detail={"role": body.role.value},
    )
    return _to_out(_load_employee(session, employee.id))


@router.get("/employees", response_model=list[EmployeeOut])
def list_employees(
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> list[EmployeeOut]:
    query = select(Employee).options(selectinload(Employee.account))
    if is_hr(account):
        rows = session.scalars(query.order_by(Employee.id)).all()
    elif account.role == Role.MANAGER:
        rows = session.scalars(
            query.where(Employee.reporting_manager_id == account.employee_id).order_by(Employee.id)
        ).all()
    else:
        raise HTTPException(status_code=403, detail="You do not have access to this action.")
    return [_to_out(row) for row in rows if row.account is not None]


@router.get("/employees/me", response_model=EmployeeOut)
def read_me(
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> EmployeeOut:
    return _to_out(_load_employee(session, account.employee_id))


@router.patch("/employees/me", response_model=EmployeeOut)
def update_me(
    body: SelfUpdate,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> EmployeeOut:
    employee = _load_employee(session, account.employee_id)
    changes = body.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(employee, field, value.strip() if isinstance(value, str) else value)
    record_audit(
        session,
        actor_employee_id=account.employee_id,
        action="update_self",
        entity_name="employees",
        entity_id=str(employee.id),
        detail={"fields": sorted(changes)},
    )
    return _to_out(employee)


@router.get("/employees/{employee_id}", response_model=EmployeeOut)
def read_employee(
    employee_id: int,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> EmployeeOut:
    employee = _load_employee(session, employee_id)
    if not _can_read_profile(account, employee):
        raise HTTPException(status_code=403, detail="You do not have access to this profile.")
    return _to_out(employee)


@router.patch("/employees/{employee_id}", response_model=EmployeeOut)
def update_employee(
    employee_id: int,
    body: EmployeeHrUpdate,
    session: Session = Depends(get_session),
    account: Account = Depends(hr_roles),
) -> EmployeeOut:
    employee = _load_employee(session, employee_id)
    _apply_hr_fields(session, employee, body)
    if body.role is not None:
        employee.account.role = body.role
    record_audit(
        session,
        actor_employee_id=account.employee_id,
        action="update",
        entity_name="employees",
        entity_id=str(employee.id),
    )
    return _to_out(employee)


@router.post("/employees/{employee_id}/activate", response_model=EmployeeOut)
def activate_employee(
    employee_id: int,
    session: Session = Depends(get_session),
    account: Account = Depends(hr_roles),
) -> EmployeeOut:
    employee = _load_employee(session, employee_id)
    if not employee.activated:
        employee.activated = True
        employee.activated_at = _utcnow()
    record_audit(
        session,
        actor_employee_id=account.employee_id,
        action="activate",
        entity_name="employees",
        entity_id=str(employee.id),
    )
    return _to_out(employee)


@router.post("/employees/{employee_id}/archive", response_model=EmployeeOut)
def archive_employee(
    employee_id: int,
    session: Session = Depends(get_session),
    account: Account = Depends(hr_roles),
) -> EmployeeOut:
    employee = _load_employee(session, employee_id)
    if not employee.archived:
        employee.archived = True
        employee.archived_at = _utcnow()
    record_audit(
        session,
        actor_employee_id=account.employee_id,
        action="archive",
        entity_name="employees",
        entity_id=str(employee.id),
    )
    return _to_out(employee)


@router.post("/employees/{employee_id}/photo", response_model=EmployeeOut)
def upload_photo(
    employee_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    account: Account = Depends(hr_roles),
) -> EmployeeOut:
    employee = _load_employee(session, employee_id)
    stored, _original = save_upload(file)
    previous = employee.photo_stored_file_name
    employee.photo_stored_file_name = stored
    delete_stored(previous)
    record_audit(
        session,
        actor_employee_id=account.employee_id,
        action="upload_photo",
        entity_name="employees",
        entity_id=str(employee.id),
    )
    return _to_out(employee)


@router.get("/employees/{employee_id}/photo")
def download_photo(
    employee_id: int,
    session: Session = Depends(get_session),
    _: Account = Depends(get_current_account),
) -> FileResponse:
    employee = session.get(Employee, employee_id)
    if employee is None or not employee.photo_stored_file_name:
        raise HTTPException(status_code=404, detail="Photo not found.")
    return FileResponse(stored_path(employee.photo_stored_file_name))


@router.get("/directory", response_model=list[WorkCard])
def directory(
    q: str | None = Query(default=None, max_length=200),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
    _: Account = Depends(get_current_account),
) -> list[WorkCard]:
    query = (
        select(Employee)
        .options(
            selectinload(Employee.department).selectinload(Department.business_unit),
            selectinload(Employee.designation),
            selectinload(Employee.location),
        )
        .where(Employee.archived.is_(False))
        .order_by(Employee.name, Employee.id)
    )
    if q and q.strip():
        term = f"%{q.strip()}%"
        query = query.where(
            or_(
                Employee.name.ilike(term),
                Employee.work_email.ilike(term),
                Employee.department.has(Department.name.ilike(term)),
                Employee.designation.has(Designation.title.ilike(term)),
                Employee.location.has(Location.name.ilike(term)),
                Employee.department.has(Department.business_unit.has(BusinessUnit.name.ilike(term))),
            )
        )
    rows = session.scalars(query.offset(offset).limit(limit)).all()
    return [_work_card(row) for row in rows]


@router.get("/organization-chart", response_model=list[ChartNode])
def organization_chart(
    session: Session = Depends(get_session),
    _: Account = Depends(get_current_account),
) -> list[ChartNode]:
    rows = session.scalars(
        select(Employee)
        .options(
            selectinload(Employee.department).selectinload(Department.business_unit),
            selectinload(Employee.designation),
            selectinload(Employee.location),
        )
        .where(Employee.archived.is_(False))
    ).all()
    nodes = {row.id: ChartNode(**_work_card(row).model_dump(), reports=[]) for row in rows}
    parent = {row.id: row.reporting_manager_id for row in rows}
    roots: list[ChartNode] = []
    for row in rows:
        manager_id = row.reporting_manager_id
        seen: set[int] = set()
        current = manager_id
        cycle = False
        while current is not None and current not in seen:
            if current == row.id:
                cycle = True
                break
            seen.add(current)
            current = parent.get(current)
        if manager_id in nodes and manager_id != row.id and not cycle:
            nodes[manager_id].reports.append(nodes[row.id])
        else:
            roots.append(nodes[row.id])
    return roots


def _can_read_documents(account: Account, employee_id: int) -> bool:
    return account.employee_id == employee_id or is_hr(account)


@router.get("/employees/{employee_id}/documents", response_model=list[DocumentOut])
def list_documents(
    employee_id: int,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> list[Document]:
    if session.get(Employee, employee_id) is None:
        raise HTTPException(status_code=404, detail="Employee not found.")
    if not _can_read_documents(account, employee_id):
        raise HTTPException(status_code=403, detail="You do not have access to these documents.")
    return list(
        session.scalars(
            select(Document).where(Document.employee_id == employee_id).order_by(Document.id)
        )
    )


@router.post("/employees/{employee_id}/documents", response_model=DocumentOut, status_code=201)
def upload_document(
    employee_id: int,
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> Document:
    if session.get(Employee, employee_id) is None:
        raise HTTPException(status_code=404, detail="Employee not found.")
    if account.employee_id != employee_id and not is_hr(account):
        raise HTTPException(status_code=403, detail="You can upload documents only for your own record.")
    stored, original = save_upload(file)
    document = Document(
        employee_id=employee_id,
        document_type=document_type,
        stored_file_name=stored,
        original_file_name=original,
    )
    session.add(document)
    session.flush()
    record_audit(
        session,
        actor_employee_id=account.employee_id,
        action="upload_document",
        entity_name="documents",
        entity_id=str(document.id),
        detail={"employee_id": employee_id, "document_type": document_type.value},
    )
    return document


@router.get("/documents/{document_id}")
def download_document(
    document_id: int,
    session: Session = Depends(get_session),
    account: Account = Depends(get_current_account),
) -> FileResponse:
    document = session.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")
    if not _can_read_documents(account, document.employee_id):
        raise HTTPException(status_code=403, detail="You do not have access to this document.")
    return FileResponse(
        stored_path(document.stored_file_name),
        filename=document.original_file_name,
    )
