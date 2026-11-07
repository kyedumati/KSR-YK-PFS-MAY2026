import os

from sqlalchemy import func, select

from app.db import get_session_factory
from app.models import Account, Employee, Role
from app.security import hash_password


def bootstrap() -> None:
    email = os.environ.get("BOOTSTRAP_ADMIN_EMAIL")
    password = os.environ.get("BOOTSTRAP_ADMIN_PASSWORD")
    name = os.environ.get("BOOTSTRAP_ADMIN_NAME")
    employee_code = os.environ.get("BOOTSTRAP_ADMIN_EMPLOYEE_CODE")
    if not all([email, password, name, employee_code]):
        raise SystemExit("Set BOOTSTRAP_ADMIN_EMAIL, BOOTSTRAP_ADMIN_PASSWORD, BOOTSTRAP_ADMIN_NAME, and BOOTSTRAP_ADMIN_EMPLOYEE_CODE.")
    session = get_session_factory()()
    try:
        existing = session.scalar(select(func.count()).select_from(Account))
        if existing:
            print("An account already exists. Bootstrap did not create another one.")
            return
        employee = Employee(
            employee_code=employee_code.strip(),
            name=name.strip(),
            work_email=email.strip(),
            activated=True,
            archived=False,
        )
        session.add(employee)
        session.flush()
        session.add(
            Account(
                employee_id=employee.id,
                role=Role.SYSTEM_ADMINISTRATOR,
                password_hash=hash_password(password),
            )
        )
        session.commit()
        print(f"System Administrator created for {email.strip()}.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    bootstrap()
