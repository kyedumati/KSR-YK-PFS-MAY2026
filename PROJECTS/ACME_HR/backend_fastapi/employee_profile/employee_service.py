from fastapi import HTTPException

from .employee_repository import EmployeeRepository
from models.employee_model import EmployeeModel
from collections.abc import Mapping

class EmployeeNotFoundException(HTTPException):
     def __init__(self, status_code: int, detail: str | None = "Employee not found", headers: Mapping[str, str] | None = None):
         super.__init__(status_code, detail, headers)


class EmployeeService:
    def __init__(self):
        self.employee_repo = EmployeeRepository()

    def get_employees(self):
        return self.employee_repo.get_employees_data()


    def add_employee(self, employee_obj:EmployeeModel):
        print("inside employee service, trying to add employee")
        self.employee_repo.add_employee_data(employee_obj)

    def get_employee_by_id(self, employee_id: int) -> EmployeeModel:
        row = self.employee_repo.get_employee_by_id(employee_id)
        if row is None:
            raise EmployeeNotFoundException()
            # raise HTTPException(status_code=404, detail="Employee not found")
        return self.employee_repo.get_employee_by_id(employee_id)