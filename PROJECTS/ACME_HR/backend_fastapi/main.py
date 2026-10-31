from fastapi import FastAPI
from employee_profile.employee_service import EmployeeService

from models.employee_model import EmployeeModel, EmployeeResponseModel


app = FastAPI(title="Acme HR Backend API")

@app.get("/")
def home():
    return {"Hello": "World, welcome to Acme HR Backend API"}

@app.get("/getEmployees", response_model=list[EmployeeResponseModel])
def getEmployees():
    return EmployeeService().get_employees()

@app.post("/addEmployee", status_code=201, response_model=EmployeeResponseModel)
def addEmployee(employee_dict: EmployeeModel):
    EmployeeService().add_employee(employee_dict)
    return employee_dict

@app.get("/getEmployee/{employee_id}", response_model=EmployeeResponseModel)
def getEmployee(employee_id: int):
    return EmployeeService().get_employee_by_id(employee_id)





