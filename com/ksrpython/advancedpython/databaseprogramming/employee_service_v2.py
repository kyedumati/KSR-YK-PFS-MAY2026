import mysql.connector
import os

from com.ksrpython.advancedpython.databaseprogramming.db_connection import query_string
from com.ksrpython.corepython.datatypes.string_datatype import student

password = os.environ.get("db_password")
username = os.environ.get("db_user")

# add/register a new student
config = {
    "host": "localhost", "port": 3306, "user": username, "password": password, "database": "PYTHON_TRAINING_KSR_DB"
}

def get_db_connection():
    return mysql.connector.connect(**config)

def add_employee(name,age,student_id,marks):
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    student_id = input("Enter your student ID: ")
    marks = input("Enter your marks: ")
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        # insert into students values(1,2,34,)
        # insert into students(col1, col2, col3) values(val1, val2, val3)
        query_string = "insert into students(age, student_id, marks, name) values (%s, %s, %s, %s)"
        values = [(age, student_id, marks, name),
                  (age, student_id, "xyz", name),
                  (age, student_id, marks, name)]

        cursor.executemany(query_string, values)

    except mysql.connector.Error as error:
        connection.rollback()
    else:
        # cursor.rowcount
        connection.commit()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_employees():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query_string = "select * from students"
    cursor.execute(query_string)
    # students = cursor.fetchall()
    students = cursor.fetchmany(3)
    print(students)
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

if __name__ == '__main__':
    get_employees()
    # update_employee()

