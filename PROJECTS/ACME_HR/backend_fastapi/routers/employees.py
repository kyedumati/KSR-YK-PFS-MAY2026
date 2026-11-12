from fastapi import APIRouter

from connection import get_db_connection
from employee_profile.employee_service import EmployeeService

from models.employee_model import EmployeeModel, EmployeeResponseModel
from fastapi import Depends

from routers.auth import validate_token_and_get_user, require_role

# employee/add
# employee/update
#employee/delete

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/getEmployees", response_model=list[EmployeeResponseModel])
def getEmployees(employee = Depends(validate_token_and_get_user), conn = Depends(get_db_connection), hr = Depends(require_role("hr_admin"))):

    return EmployeeService(conn).get_employees()

@router.post("/addEmployee", status_code=201, response_model=EmployeeResponseModel)
def addEmployee(employee_dict: EmployeeModel, employee = Depends(validate_token_and_get_user), conn = Depends(get_db_connection)):
    EmployeeService(conn).add_employee(employee_dict)
    return employee_dict

# we need to accept the token and we need decode and validate the token
@router.get("/getEmployee/{employee_code}", response_model=EmployeeResponseModel)
def getEmployee(employee_code: str, employee = Depends(validate_token_and_get_user), conn = Depends(get_db_connection)):
    return EmployeeService(conn).get_employee_by_id(employee_code)