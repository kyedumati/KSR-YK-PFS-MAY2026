from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import record_audit
from app.deps import get_current_account, get_session, require_roles
from app.models import Account, BusinessUnit, Department, Designation, Location, Role
from app.rules import require_timezone

router = APIRouter(tags=["organization"])
system_admin = require_roles(Role.SYSTEM_ADMINISTRATOR)


class NamedRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class NamedCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class DepartmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    business_unit_id: int


class DepartmentIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    business_unit_id: int


class LocationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    region: str
    timezone: str


class LocationIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    region: str = Field(min_length=1, max_length=120)
    timezone: str = Field(min_length=1, max_length=64)


class DesignationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str


class DesignationIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)


def _audit(session: Session, account: Account, action: str, entity: str, entity_id: int) -> None:
    record_audit(
        session,
        actor_employee_id=account.employee_id,
        action=action,
        entity_name=entity,
        entity_id=str(entity_id),
    )


@router.get("/business-units", response_model=list[NamedRecord])
def list_business_units(
    session: Session = Depends(get_session),
    _: Account = Depends(get_current_account),
) -> list[BusinessUnit]:
    return list(session.scalars(select(BusinessUnit).order_by(BusinessUnit.id)))


@router.post("/business-units", response_model=NamedRecord, status_code=201)
def create_business_unit(
    body: NamedCreate,
    session: Session = Depends(get_session),
    account: Account = Depends(system_admin),
) -> BusinessUnit:
    row = BusinessUnit(name=body.name.strip())
    session.add(row)
    session.flush()
    _audit(session, account, "create", "business_units", row.id)
    return row


@router.patch("/business-units/{business_unit_id}", response_model=NamedRecord)
def update_business_unit(
    business_unit_id: int,
    body: NamedCreate,
    session: Session = Depends(get_session),
    account: Account = Depends(system_admin),
) -> BusinessUnit:
    row = session.get(BusinessUnit, business_unit_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Business unit not found.")
    row.name = body.name.strip()
    _audit(session, account, "update", "business_units", row.id)
    return row


@router.get("/departments", response_model=list[DepartmentOut])
def list_departments(
    session: Session = Depends(get_session),
    _: Account = Depends(get_current_account),
) -> list[Department]:
    return list(session.scalars(select(Department).order_by(Department.id)))


@router.post("/departments", response_model=DepartmentOut, status_code=201)
def create_department(
    body: DepartmentIn,
    session: Session = Depends(get_session),
    account: Account = Depends(system_admin),
) -> Department:
    if session.get(BusinessUnit, body.business_unit_id) is None:
        raise HTTPException(status_code=422, detail="Business unit not found.")
    row = Department(name=body.name.strip(), business_unit_id=body.business_unit_id)
    session.add(row)
    session.flush()
    _audit(session, account, "create", "departments", row.id)
    return row


@router.patch("/departments/{department_id}", response_model=DepartmentOut)
def update_department(
    department_id: int,
    body: DepartmentIn,
    session: Session = Depends(get_session),
    account: Account = Depends(system_admin),
) -> Department:
    row = session.get(Department, department_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Department not found.")
    if session.get(BusinessUnit, body.business_unit_id) is None:
        raise HTTPException(status_code=422, detail="Business unit not found.")
    row.name = body.name.strip()
    row.business_unit_id = body.business_unit_id
    _audit(session, account, "update", "departments", row.id)
    return row


@router.get("/locations", response_model=list[LocationOut])
def list_locations(
    session: Session = Depends(get_session),
    _: Account = Depends(get_current_account),
) -> list[Location]:
    return list(session.scalars(select(Location).order_by(Location.id)))


@router.post("/locations", response_model=LocationOut, status_code=201)
def create_location(
    body: LocationIn,
    session: Session = Depends(get_session),
    account: Account = Depends(system_admin),
) -> Location:
    row = Location(
        name=body.name.strip(),
        region=body.region.strip(),
        timezone=require_timezone(body.timezone.strip()),
    )
    session.add(row)
    session.flush()
    _audit(session, account, "create", "locations", row.id)
    return row


@router.patch("/locations/{location_id}", response_model=LocationOut)
def update_location(
    location_id: int,
    body: LocationIn,
    session: Session = Depends(get_session),
    account: Account = Depends(system_admin),
) -> Location:
    row = session.get(Location, location_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Location not found.")
    row.name = body.name.strip()
    row.region = body.region.strip()
    row.timezone = require_timezone(body.timezone.strip())
    _audit(session, account, "update", "locations", row.id)
    return row


@router.get("/designations", response_model=list[DesignationOut])
def list_designations(
    session: Session = Depends(get_session),
    _: Account = Depends(get_current_account),
) -> list[Designation]:
    return list(session.scalars(select(Designation).order_by(Designation.id)))


@router.post("/designations", response_model=DesignationOut, status_code=201)
def create_designation(
    body: DesignationIn,
    session: Session = Depends(get_session),
    account: Account = Depends(system_admin),
) -> Designation:
    row = Designation(title=body.title.strip())
    session.add(row)
    session.flush()
    _audit(session, account, "create", "designations", row.id)
    return row


@router.patch("/designations/{designation_id}", response_model=DesignationOut)
def update_designation(
    designation_id: int,
    body: DesignationIn,
    session: Session = Depends(get_session),
    account: Account = Depends(system_admin),
) -> Designation:
    row = session.get(Designation, designation_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Designation not found.")
    row.title = body.title.strip()
    _audit(session, account, "update", "designations", row.id)
    return row
