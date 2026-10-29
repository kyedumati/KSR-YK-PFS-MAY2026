import mysql.connector
import os

from models.employee_model import EmployeeModel

password = os.environ.get("db_password")
username = os.environ.get("db_user")

# add/register a new student
config = {
    "host": "localhost", "port": 3306, "user": username, "password": password, "database": "acemehr_db"
}

class EmployeeCreateException(Exception):
    pass

def get_db_connection():
    return mysql.connector.connect(**config)

def add_employee_data(employee_obj:EmployeeModel):
    try:
        print("insdie repoisotyr, adding employee data")
        connection = get_db_connection()
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

def get_employees_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query_string = "select * from employee"
    cursor.execute(query_string)
    # students = cursor.fetchall()
    students = cursor.fetchmany(3)
    print(students)
    return students
    # for student in students:
    #     print(student)
        # print("studnetid",student[0])
        # print("name", student[1])
        # print("marks", student[2])
        # print("age", student[3])

def update_employee():
    age = input("Enter your age: ")
    student_id = input("Enter your student ID: ")
    marks = input("Enter your marks: ")

    connection = get_db_connection()
    cursor = connection.cursor()
    query_string = "update students set age = %s, marks = %s where student_id = %s"
    values = (age, marks, student_id)
    cursor.execute(query_string, values)
    print(cursor.rowcount, " record was updated")
    connection.commit()
    print("employee updated")
    cursor.close()
    connection.close()
