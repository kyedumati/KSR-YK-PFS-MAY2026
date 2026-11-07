from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Account, Employee, Role
from app.security import decode_access_token

bearer = HTTPBearer(auto_error=False)


def get_session(request: Request) -> Session:
    session = getattr(request.state, "session", None)
    if session is None:
        raise RuntimeError("Database session is not available.")
    return session


def get_current_account(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    session: Session = Depends(get_session),
) -> Account:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Sign-in is required.")
    payload = decode_access_token(credentials.credentials)
    try:
        employee_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Sign-in is required.")
    account = session.scalar(
        select(Account)
        .options(selectinload(Account.employee))
        .where(Account.employee_id == employee_id)
    )
    if account is None or account.employee.archived:
        raise HTTPException(status_code=401, detail="This account is archived.")
    return account


def require_roles(*roles: Role):
    def checker(account: Account = Depends(get_current_account)) -> Account:
        if account.role not in roles:
            raise HTTPException(status_code=403, detail="You do not have access to this action.")
        return account

    return checker


def is_hr(account: Account) -> bool:
    return account.role in {Role.SYSTEM_ADMINISTRATOR, Role.HR_ADMINISTRATOR}


def require_active_employee(employee: Employee) -> None:
    if employee.archived or not employee.activated:
        raise HTTPException(
            status_code=403,
            detail="Check-in and leave are available after the employee is activated.",
        )
