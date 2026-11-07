from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.deps import get_session
from app.models import Account, Employee
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    work_email: str = Field(min_length=3, max_length=254)
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    employee_id: int


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, session: Session = Depends(get_session)) -> LoginResponse:
    account = session.scalar(
        select(Account)
        .options(selectinload(Account.employee))
        .join(Employee, Account.employee_id == Employee.id)
        .where(Employee.work_email == body.work_email)
    )
    if account is None or not verify_password(body.password, account.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    if account.employee.archived:
        raise HTTPException(status_code=401, detail="This account is archived.")
    token = create_access_token(employee_id=account.employee_id, role=account.role.value)
    return LoginResponse(access_token=token, role=account.role.value, employee_id=account.employee_id)
