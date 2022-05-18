import mysql.connector

class database:
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        self.__mydb =  mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        self.__cursor = self.__mydb.cursor()

    def insert(self):
        pass
    
    def read(self):
        pass
    
    def update(self):
        pass
    
    def delete(self):
        pass