import mysql.connector
import os
password = os.environ.get("MYSQL_PASSWORD")
if not password:
    raise SystemExit("Set MYSQL_PASSWORD first, e.g.\n  export MYSQL_PASSWORD='your_lab_password'")

config = {
    "host": "localhost",
    "user": "root",                 # replace with lab user
    "password": password,    # replace with lab password
    "database": "PYTHON_TRAINING_KSR_DB",
    "port": 3306,
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()
cursor.execute("select * from customers")
print("Current DB:", cursor.fetchone()[0])
cursor.close()
conn.close()
print("Closed cleanly")