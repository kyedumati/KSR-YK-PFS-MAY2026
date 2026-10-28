from pydantic import BaseModel, Field, EmailStr # basemodel is a class fastapi will give by default,


class EmployeeModel(BaseModel):
    employee_id: int
    name: str = Field(min_length=3) # name cannot be less than 3character and also name cannot be empty string
    designation: str
    department: str
    email: EmailStr
    phone_number: str | None = None # Optional, a missing phone is still works

class EmployeeUpdateModel(BaseModel):
    name: str = Field(min_length=3)
    designation: str
    department: str
    email: EmailStr
    phone_number: str | None = None


class EmployeeResponseModel(BaseModel):
    employee_id : int
    name: str
    designation: str
    department: str
    email: EmailStr
    phone_number: str | None = None