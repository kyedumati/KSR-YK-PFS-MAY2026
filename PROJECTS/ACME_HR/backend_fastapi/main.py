from fastapi import FastAPI

# created the fastapi application instance/obj
fastapi_obj = FastAPI(title="Acme HR Backend API")


@fastapi_obj.get("/getEmployees") # this is a decorator that registers a function to handle HTTP GET requests at /getEmployees path
def get_employees():
    return [{
        "id": 1,
        "name": "Employee 1",
        "email": ""
    }, {"id": 2, "name": "Pallavi", "email": "test@gmail.com"} ]


@fastapi_obj.get("/getEmployeeInfo") # this is a decorator that registers a function to handle HTTP GET requests at /getEmployees path
def get_employees_info():
    return {"id": 2, "name": "Pallavi", "email": "test@gmail.com"}


@fastapi_obj.get("/getEmployeeById/{employee_id}")
def get_employee_by_id(employee_id: int):
    return {"id": employee_id, "name": "Pallavi", "email": ""}

