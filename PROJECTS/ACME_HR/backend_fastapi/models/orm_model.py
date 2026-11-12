from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base, engine, session



class Location(Base):
    __tablename__ = "locations" # The mysql table this class is going to map

    id : Mapped[int] = mapped_column(primary_key=True) # columnoptions : primary key constraint, with int datatype
    name: Mapped[str] = mapped_column(String(60))
    city: Mapped[str] = mapped_column(String(60))
    region: Mapped[str] = mapped_column(String(60))


class Departments(Base):
    __tablename__ = "departments"

    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    is_active: Mapped[bool] = mapped_column(default=True)

    # relations
    employees: Mapped[list[Employee]] = relationship(back_populates="department") # I'm mapping employees to department table as one department to many employees

class Designation(Base):
    __tablename__ = "designations"

    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(60))
    level: Mapped[str] = mapped_column(String(20))


class Employee(Base):
    __tablename__ = "employees"   # mysql table this class is goiong to map to
    id : Mapped[int] = mapped_column(primary_key=True)
    employee_code: Mapped[str] = mapped_column(String(60), unique=True)
    first_name: Mapped[str] = mapped_column(String(60))
    last_name: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(60))
    phone: Mapped[str] = mapped_column(String(60))
    date_of_birth: Mapped[str] = mapped_column(String(60))
    hire_date: Mapped[str] = mapped_column(String(60))
    status: Mapped[str] = mapped_column(String(60))
    # salary: Mapped[str] = mapped_column(String(60))

    department_id : Mapped[int] = mapped_column(ForeignKey("departments.id"))
    designation_id: Mapped[int] = mapped_column(ForeignKey("designations.id"))

    # relationship
    department: Mapped[Departments] = relationship(back_populates="employees") # im mapping department information to employee table back as one to one mapping
    account: Mapped[UserAccount | None] = relationship(
        back_populates="employee",
        uselist=False,
        foreign_keys="UserAccount.employee_code",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"

class UserAccount(Base):
    __tablename__ = "user_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    # FK is required for Employee.account / UserAccount.employee to resolve their join
    employee_code: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("employees.employee_code"),
        unique=True,
    )
    password_hash: Mapped[str] = mapped_column(String(60))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    employee: Mapped[Employee] = relationship(
        back_populates="account",
        foreign_keys=[employee_code],
    )


PRACTICE_PASSWORD = "Acme@2026"


def seed_db():
    Base.metadata.create_all(engine, tables=[UserAccount.__table__])

    db_session = session()
    # select * from employees where status!= 'exited'
    # create account for all of them
    stmt_output = db_session.scalars(select(Employee).where(Employee.status != 'exited')) # select * from employees where status!='exited')
    try:
        counter = 0
        for employee in stmt_output:
            if employee.account is None:
                user_acount = UserAccount(employee_code=employee.employee_code, password_hash = hash_password(PRACTICE_PASSWORD))
                db_session.add(user_acount) #insert query
                counter += 1
        db_session.commit() # committing all transactions done before this lines
        print(counter, " users created")
            # print(employee)
    except Exception as e:
        print(e)
        db_session.rollback()


if __name__ == "__main__":
    seed_db()
