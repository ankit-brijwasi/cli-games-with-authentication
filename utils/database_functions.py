'''The code for the backend and all the logics lives here'''
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'sqlite3.db')


class Schema:
    def __init__(self, conn):
        self.conn = conn

    def create_table(self, table_name: str, fields_list: list):
        '''Create a table
        table_name = "Dummy"
        field_list = [
            {"id": "INT PRIMARY KEY NOT NULL"},
            {"name": "TEXT NOT NULL"},
        ]
        '''
        fields = ""

        for field in fields_list:
            for key, value in field.items():
                fields += (str(key) + " " + str(value) + ", ")

        fields = fields[:-2]

        try:
            self.conn.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ({fields});")
        except Exception as e:
            raise str(e)


class Database:
    '''All the functions regarding Database connectivity lives in this class'''

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.schema = Schema(self.conn)

    def migrate_db(self):
        self.schema.create_table()

    def close_db(self):
        self.conn.close()
