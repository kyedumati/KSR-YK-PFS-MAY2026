from connection import get_db_connection
from models.employee_model import EmployeeModel
import mysql.connector


class EmployeeCreateException(Exception):
    pass

class EmployeeRepository:
    def __init__(self, conn):
        self.db_connection = conn

    def add_employee_data(self, employee_obj:EmployeeModel):
        try:
            print("insdie repoisotyr, adding employee data")
            connection = self.db_connection
            cursor = connection.cursor()
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
        cursor = connection.cursor(dictionary=True)
        query_string = "select * from employee"
        cursor.execute(query_string)
        employees = cursor.fetchall()
        # students = cursor.fetchmany(3)
        print(employees)
        return employees

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

    def get_employee_by_id(self, employee_id: int):
        connection = self.db_connection
        cursor = connection.cursor(dictionary=True)
        query_string = "select * from employee where employee_id = %s"
        values = (employee_id,)
        cursor.execute(query_string, values)
        employee = cursor.fetchone()
        print("employeedata in getemployee_by_id",employee)
        return employee
