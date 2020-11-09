'''The code for the backend and all the logics lives here'''
from datetime import datetime
from .driver_functions import BASE_DIR, DATABASE_PATH, create_dirs
import sqlite3
import hashlib


class User:
    '''All opertions realted to a user are handled here'''

    def __init__(self, *args, **kwargs):
        self.id = args[0]
        self.name = args[1]
        self.email = args[2]
        self.password = args[3]


class Schema:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_table(self, table_name: str, fields_list: list) -> None:
        '''Create a table'''
        fields = ""

        for field in fields_list:
            fields += (str(field) + ", ")

        fields = fields[:-2]

        self.conn.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({fields});")

    def insert_data(self, table_name: str, fields: str, values: str) -> None:
        '''performs the INSERT query and returns a list'''
        self.conn.execute(
            f"INSERT INTO  {table_name} ({fields}) VALUES ({values}) ")
        self.conn.commit()

    def select_data(self, table_name: str, fields: str, condition: str) -> None:
        '''performs the SELECT query and returns a list'''
        rows = self.conn.execute(
            f"SELECT {fields}  from {table_name} {condition};")
        return rows.fetchall()

    def insert_and_select(self, table_name: str, fields: str, values: str):
        '''Insert amd return the inserted value'''
        self.insert_data(table_name, fields, values)

        condition = "WHERE "

        for key, value in zip(fields.split(","), values.split(",")):
            condition += f"{key}={value} and "
        condition = condition[:-5]

        res = self.select_data(table_name, "*", condition)
        return res


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

    def get_all_data(self):
        return self.schema.select_data("User", "*", "")

    def close_db(self):
        self.conn.close()


class Authentication:
    '''Class to handle Login and Signup'''

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.schema = Schema(self.conn)
        self.user = None

    def authenticate(self, email: str, password: str) -> User:
        '''handle's authentication and returns the user if exists otherwise returns None'''
        print("\nlogging in...")
        password = self.generate_hash(password)
        self.user = self.schema.select_data(
            "User", "*", f"where email='{email}' and password='{password}'")
        if len(self.user) == 0:
            return None
        return User(*self.user[0])

    def unique_email(self, email: str) -> bool:
        '''check for unique email'''
        res = self.schema.select_data("User", "id", f"where email='{email}'")
        if len(res):
            return False
        return True

    def generate_hash(self, string: str) -> str:
        string = string.encode("utf-8")
        return hashlib.sha256(string).hexdigest()

    def register(self, name: str, email: str, password: str) -> User:
        '''handles the registration'''
        try:
            password = self.generate_hash(password)
            user = self.schema.insert_and_select(
                "User", "name, email, password", f"'{name}', '{email}', '{password}'")
            return User(*user[0])

        except Exception as e:
            create_dirs()
            with open('logs/register.errors.log', 'a') as log_file:
                log_file.write(f"\n[{str(datetime.now())}]: {str(e)}")
        return None
