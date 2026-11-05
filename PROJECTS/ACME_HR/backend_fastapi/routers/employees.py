from fastapi import APIRouter

from connection import get_db_connection
from employee_profile.employee_service import EmployeeService

from models.employee_model import EmployeeModel, EmployeeResponseModel
from fastapi import Depends

# employee/add
# employee/update
#employee/delete

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/getEmployees", response_model=list[EmployeeResponseModel])
def getEmployees(conn = Depends(get_db_connection)):
    return EmployeeService(conn).get_employees()

@router.post("/addEmployee", status_code=201, response_model=EmployeeResponseModel)
def addEmployee(employee_dict: EmployeeModel, conn = Depends(get_db_connection)):
    EmployeeService(conn).add_employee(employee_dict)
    return employee_dict

@router.get("/getEmployee/{employee_code}", response_model=EmployeeResponseModel)
def getEmployee(employee_code: str, conn = Depends(get_db_connection)):
    return EmployeeService(conn).get_employee_by_id(employee_code)