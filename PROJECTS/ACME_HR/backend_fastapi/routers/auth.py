from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from connection import get_db_connection
from models.orm_model import Employee
from security.api_security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], conn = Depends(get_db_connection)):
    print("login request started")
    # step1: get the user information with username
    employee = conn.scalars(select(Employee).where(Employee.employee_code == form_data.username)).first()

    if employee is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, employee.account.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"access_token": create_access_token(employee.employee_code, "admin"), "token_type": "bearer", "expires_in": 1800}





