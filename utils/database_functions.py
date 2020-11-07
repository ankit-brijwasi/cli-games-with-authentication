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
