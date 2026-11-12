from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import select
import jwt

from connection import get_db_connection
from models.auth_models import TokenResponseModel
from models.orm_model import Employee
from security.api_security import verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

def require_role(*roles: str): # "HR", "admin"
    def role_checker(employee = Depends(validate_token_and_get_user)):
        if employee.role not in roles:
            raise HTTPException(status_code=403, detail="Incorrect role provided")
        return employee
    return role_checker # it is returning the function, but not executing


def validate_token_and_get_user(token = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token")), conn = Depends(get_db_connection)) -> Employee:
    try:
        claims_dict = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    employee = conn.scalars(select(Employee).where(Employee.employee_code == claims_dict.get("sub"))).first()

    return employee






# step1: token call with happen
# step2: get_db_connection will be called, until yield statment
# step3: all the statment under route function will be executed
# step4: execute or continue all the other thing in get_db_connection after yield
# step5: now return the output to endpoint


@router.post("/token", response_model=TokenResponseModel)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], conn = Depends(get_db_connection)):
    print("login request started")
    # step1: get the user information with username
    employee = conn.scalars(select(Employee).where(Employee.employee_code == form_data.username)).first()

    if employee is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, employee.account.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"access_token": create_access_token(employee.employee_code, "admin"), "token_type": "bearer", "expires_in": 1800}





