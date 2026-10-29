from .employee_repository import get_employees_data, add_employee_data
from models.employee_model import EmployeeModel

def get_employees():
    return get_employees_data()


def add_employee(employee_obj:EmployeeModel):
    print("inside employee service, trying to add employee")
    add_employee_data(employee_obj)