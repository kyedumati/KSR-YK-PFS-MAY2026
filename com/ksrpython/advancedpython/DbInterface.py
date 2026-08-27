from abc import ABC, abstractmethod

class DBInterface(ABC):# this is an interface which has only abstract methods
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

class MySQLDB(DBInterface):
    def connect(self):
        print("Connecting to MySQL")
        # will write logic to connect to mysql

    def disconnect(self):
        print("Disconnecting from MySQL")

class PostgreSQL(DBInterface):
    def connect(self):
        print("Connecting to PostgreSQL")

    def disconnect(self):
        print("Disconnecting from PostgreSQL")

engines = {"mysql": MySQLDB(), "postgresql":PostgreSQL()}
# for engine in engines:
#     engine.connect()
#     engine.disconnect()

db = engines["mysql"]
db.connect()
db.disconnect()
