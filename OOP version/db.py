import mysql.connector

class Database:
    def __init__(self,host="localhost",user="root",password="",database="school_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="school_db"
        )


