from sqlalchemy.testing.schema import mapped_column

from connection import Base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import String, ForeignKey


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
