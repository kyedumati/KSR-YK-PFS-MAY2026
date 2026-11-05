from models.employee_model import EmployeeModel
import mysql.connector
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.orm_model import Employee, Departments


class EmployeeCreateException(Exception):
    pass

class EmployeeRepository:
    def __init__(self, conn: Session):
        self.db_connection = conn

    def add_employee_data(self, employee_obj:EmployeeModel):
        try:
            print("insdie repoisotyr, adding employee data")
            connection = self.db_connection
            cursor = connection.cursor(dictionary=True)
            query_string = "insert into employee(name, employee_id, designation, deparment, email, phone_number) values (%s, %s, %s, %s, %s, %s)"
            values = (employee_obj.name, employee_obj.employee_id, employee_obj.designation, employee_obj.department, employee_obj.email, employee_obj.phone_number)
            print("insdie repoisotyr, before execute")
            cursor.execute(query_string, values)
            print("insdie repoisotyr, after execute")
        except mysql.connector.Error as error:
            connection.rollback()
            raise EmployeeCreateException(error)
        else:
            # cursor.rowcount
            connection.commit()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_employees_data(self):
        connection = self.db_connection
        # cursor = connection.cursor(dictionary=True)
        # query_string = "select * from employee"
        # cursor.execute(query_string)
        # employees = cursor.fetchall()
        # # students = cursor.fetchmany(3)
        # print(employees)
        # print(employees[0].get("abc"))
        #stmt = select(Employee).order_by(Employee.first_name.desc(), Employee.last_name) # SELECT employees.id, employees.employee_code, employees.first_name, employees.last_name, employees.email, employees.phone_number, employees.date_of_birth, employees.hire_date, employees.salary, employees.department_id, employees.designation_id FROM employees
        stmt = (select(Employee).join(Employee.department).
                where(Employee.status == 'active', Departments.name == 'Engineering')).order_by(Employee.first_name)

        print("printing select query", stmt)
        return connection.scalars(stmt).all()

    def update_employee(self, employee_id: int, employee_obj: EmployeeModel):

        connection = self.db_connection
        cursor = connection.cursor()
        query_string = "update students set age = %s, marks = %s where student_id = %s"
        values = (age, marks, student_id)
        cursor.execute(query_string, values)
        print(cursor.rowcount, " record was updated")
        connection.commit()
        print("employee updated")
        cursor.close()
        connection.close()

    def get_employee_by_id(self, employee_code: str):
        connection = self.db_connection
        # cursor = connection.cursor(dictionary=True)
        # query_string = "select * from employee where employee_id = %s"
        # values = (employee_id,)
        # cursor.execute(query_string, values)
        # employee = cursor.fetchone()
        # print("employeedata in getemployee_by_id",employee)

        stmt = select(Employee).where(Employee.employee_code == employee_code, Employee.status == 'active')
        # select col1, col2, .. from employees where employee_code='E-10'
        print("printing select query by id", stmt)
        return connection.scalars(stmt).first()
