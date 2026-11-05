import os
import mysql.connector
from mysql.connector.pooling import PooledMySQLConnection
from pydantic import NonNegativeInt

password = os.environ.get("db_password")
username = os.environ.get("db_user")

# add/register a new student
config = {
    "host": "localhost", "port": 3306, "user": username, "password": password, "database": "acemehr_db"
}

def get_db_connection():
    conn = mysql.connector.connect(**config)
    try :
        yield conn
    except mysql.connector.Error as error :
        print("Error while connecting to MySQL", error)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    db = get_db_connection()  # paused; connect() has not run yet
    conn = next(db)           # runs until yield, then pauses with conn open
    try:
        cursor = conn.cursor()
        cursor.execute("select * from employee")
        print(cursor.fetchall())
    finally:
        next(db, None)        # resumes after yield; the generator's finally closes conn ; we are discarding db