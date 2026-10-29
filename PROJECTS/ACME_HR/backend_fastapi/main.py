from fastapi import FastAPI
from employee_profile.employee_service import get_employees, add_employee

from models.employee_model import EmployeeModel, EmployeeResponseModel


app = FastAPI(title="Acme HR Backend API")

@app.get("/")
def home():
    return {"Hello": "World, welcome to Acme HR Backend API"}

@app.get("/getEmployees")
def getEmployees():
    return get_employees()

@app.post("/addEmployee", status_code=201, response_model=EmployeeResponseModel)
def addEmployee(employee_dict: EmployeeModel):
    add_employee(employee_dict)
    return employee_dict




