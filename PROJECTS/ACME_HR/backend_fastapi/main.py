from fastapi import FastAPI

# created the fastapi application instance/obj
fastapi_obj = FastAPI(title="Acme HR Backend API")

# intialise list of students dummy data for api testing
students = [
    {"id": 1, "name": "Pallavi", "email": "pallavi@gmail.com", "course": "python", "status": "absent"},
    {"id": 2, "name": "Ravi", "email": "ravi@gmail.com", "course": "python", "status": "present"},
    {"id": 3, "name": "Ramesh", "email": "ramesh@gmail.com", "course": "java", "status": "absent"}
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
def get_students(course: str, status: str = "present" ):
    # filtered_students = [student for student in students if (course == student["course"] and status == student["status"])]
    filtered_students = []
    for student in students:
        if course is None:
            if student["status"] == status:
                filtered_students.append(student)
        elif student["course"] == course and student["status"] == status:
            filtered_students.append(student)

    return filtered_students

