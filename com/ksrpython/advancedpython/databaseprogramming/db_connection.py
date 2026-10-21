import mysql.connector
import os
# connect to db
# host, port, username, dbname, password
password = os.environ.get("db_password")
username = os.environ.get("db_user")

config = {
"host":"localhost", "port":3306, "user":username, "password":password, "database":"PYTHON_TRAINING_KSR_DB"
}

connection = mysql.connector.connect(**config)
print(connection)
# create a session or cursor
cursor = connection.cursor()
query_string = "select database();"
cursor.execute(query_string)
print(cursor.fetchall())

# close
cursor.close()
connection.close()