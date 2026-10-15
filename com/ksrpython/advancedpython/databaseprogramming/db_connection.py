import mysql.connector

# connect to db
# host, port, username, dbname, password
connection = mysql.connector.connect(host="localhost", port=3306, user="root", password="root", database="PYTHON_TRAINING_KSR_DB")
print(connection)
# create a session or cursor
cursor = connection.cursor()
query_string = "select database();"
cursor.execute(query_string)
print(cursor.fetchone())

# close
cursor.close()
connection.close()