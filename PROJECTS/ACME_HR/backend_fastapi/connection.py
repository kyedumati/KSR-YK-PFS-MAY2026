import os
# import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
# from mysql.connector.pooling import PooledMySQLConnection
# from pydantic import NonNegativeInt

# password = os.environ.get("db_password")
# username = os.environ.get("db_user")
#
# # add/register a new student
# config = {
#     "host": "localhost", "port": 3306, "user": username, "password": password, "database": "acemehr_db"
# }

#DATABASE_URL = os.environ.get("DATABASE_URL", "mysql+mysqlconnector//root:root@localhost:3306/acemehr_db")
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/acmehr_db"
engine = create_engine(DATABASE_URL,
                       pool_size=5, # go and get 5 connections at the start of the application, kept open and ready
                       max_overflow = 10, # extra connections allowed during the overflow burst
                       pool_timeout=30, # these are the seconds a new request can wait before giving up
                       pool_recycle=180 # replace connections older than 3minutes
                       )

session = sessionmaker(bind=engine)


class Base(DeclarativeBase): # any python class that is going to inherit this Base is treated ORM model class
    pass

def get_db_connection():
    db = session()
    # mysql.connector.connect(**config)
    try :
        yield db
    except Exception as e :
        print("Exception while connecting to MySQL", e)
    finally:
        db.close()


if __name__ == "__main__":
    db = get_db_connection()  # paused; connect() has not run yet
    conn = next(db)           # runs until yield, then pauses with conn open
    try:
        cursor = conn.cursor()
        cursor.execute("select * from employee")
        print(cursor.fetchall())
    finally:
        next(db, None)        # resumes after yield; the generator's finally closes conn ; we are discarding db