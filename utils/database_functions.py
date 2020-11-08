'''The code for the backend and all the logics lives here'''
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'sqlite3.db')


class Schema:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self, table_name, fields_list):
        '''Create a table'''
        fields = ""

        for field in fields_list:
            fields += (str(field) + ", ")

        fields = fields[:-2]

        self.conn.execute("CREATE TABLE IF NOT EXISTS " +
                          table_name + " (" + fields + ");")

    def select_data(self, table_name, fields, condition):
        '''performs the SELECT query and returns a list'''
        rows = self.conn.execute(
            "SELECT " + fields + " from " + table_name + " " + condition + ";")
        return rows.fetchall()

    def insert_data(self, table_name, fields, values, condition):
        '''performs the INSERT query and returns a list'''
        self.conn.execute(
            "INSERT INTO" + table_name + " (" + fields + ") "
            "VALUES( " + values + ") ")


class Database:
    '''All the functions regarding Database connectivity lives in this class'''

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.schema = Schema(self.conn)

    def migrate_db(self):

        # Migrate User Table
        self.schema.create_table(
            "User",
            [
                "id INTEGER PRIMARY KEY AUTOINCREMENT",
                "name TEXT NOT NULL",
                "email TEXT NOT NULL UNIQUE",
                "password TEXT NOT NULL",
            ]
        )

        # Migrate User OTP
        self.schema.create_table(
            "UserVerfication",
            [
                "id INTEGER PRIMARY KEY AUTOINCREMENT",
                "code TEXT NOT NULL",
                "verified INTEGER NOT NULL DEFAULT 0",
                "user INTEGER",
                "FOREIGN KEY (user) REFERENCES User(id)",
            ]
        )

    def close_db(self):
        self.conn.close()


class Authentication:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.schema = Schema(self.conn)
        self.user = None

    def authenticate(self, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")

        self.user = self.schema.get(
            "User", "*", f"where email='{email}' and password='{password}'")
