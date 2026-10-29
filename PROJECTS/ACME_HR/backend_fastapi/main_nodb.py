from fastapi import FastAPI, HTTPException, Response

from models.employee_model import EmployeeModel, EmployeeUpdateModel, EmployeeResponseModel

# created the fastapi application instance/obj
fastapi_obj = FastAPI(title="Acme HR Backend API")

# intialise list of students dummy data for api testing
students = [
    {"id": 1, "name": "Pallavi", "email": "pallavi@gmail.com", "course": "python", "status": "absent"},
    {"id": 2, "name": "Ravi", "email": "ravi@gmail.com", "course": "python", "status": "present"},
    {"id": 3, "name": "Ramesh", "email": "ramesh@gmail.com", "course": "java", "status": "absent"}
]

employees = [
    {"employee_id": 1, "name": "Ananya", "email": "ananya@gmail.com", "designation": "Software Engineer", "department": "IT"},
    {"employee_id": 2, "name": "Karthik", "email": "karthik@gmail.com", "designation": "Software Engineer", "department": "IT"},
    {"employee_id": 3, "name": "Meena", "email": "meena@gmail.com",  "designation": "Software Engineer", "department": "IT"},
    {"employee_id": 4, "name": "NTR", "email": "ntr@gmail.com",  "designation": "Software Engineer", "department": "IT"},
    {"employee_id": 5, "name": "Ram Charan", "email": "ramcharan@gmail.com",  "designation": "Software Engineer", "department": "IT"}
]

@fastapi_obj.get("/")
def home():
    return {"messsage": "welcome to Acme HR"}

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


@fastapi_obj.get("/getEmployeeById/{employee_id}") # /getEmployeeById/101 /getEmployeeById/102
def get_employee_by_id(employee_id: int):
    return {"id": employee_id, "name": "Pallavi", "email": ""}


# def create_employee(name, email, mobile):
@fastapi_obj.get("/getStudents")
def get_students(course: str, status: str = "present"):
    # filtered_students = [student for student in students if (course == student["course"] and status == student["status"])]
    filtered_students = []
    for student in students:
        if course is None:
            if student["status"] == status:
                filtered_students.append(student)
        elif student["course"] == course and student["status"] == status:
            filtered_students.append(student)

    return filtered_students

def find_employee(employee_id: int):
    for employee in employees:
        if employee["employee_id"] == employee_id:
            return employee

'''
@fastapi_obj.post("/addEmployee", status_code=201)
def create_employee(employee_dict: EmployeeModel): #snake case names for methods are highly recommended
    if "employee_id" not in employee_dict or "name" not in employee_dict:
        raise HTTPException(status_code=400, detail= "employee_id and name are required")

    employees.append(employee_dict)
    return employee_dict
'''

@fastapi_obj.post("/addEmployee", status_code=201)
def create_employee(employee_dict: EmployeeModel): #snake case names for methods are highly recommended
    # if "employee_id" not in employee_dict or "name" not in employee_dict:
    #     raise HTTPException(status_code=400, detail= "employee_id and name are required")
    print(employee_dict)
    employees.append(employee_dict)
    return employee_dict

@fastapi_obj.put("/updateEmployee/{employee_id}", response_model=EmployeeResponseModel)
def update_employee(employee_id: int, employee: EmployeeUpdateModel):
    current_employee = find_employee(employee_id)
    current_employee.update(employee)
    current_employee["employee_id"] = employee_id

    return current_employee

@fastapi_obj.delete("/deleteEmployee/{employee_id}", status_code=204)
def delete_employee(employee_id: int):
    current_employee = find_employee(employee_id)
    if current_employee is None:
        raise HTTPException(status_code=404, detail= "employee_id is not found")
    employees.remove(current_employee)
    return Response(status_code=204)


# path means for reading single item from the server
# query means for searching itesm and you may expect one or more records from the server
