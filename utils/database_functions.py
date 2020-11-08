'''The code for the backend and all the logics lives here'''
from datetime import datetime
import os, sqlite3, hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'sqlite3.db')


class Schema:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_table(self, table_name: str, fields_list: list) -> None:
        '''Create a table'''
        fields = ""

        for field in fields_list:
            fields += (str(field) + ", ")

        fields = fields[:-2]

        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({fields});")

    def select_data(self, table_name: str, fields: str, condition: str) -> None:
        '''performs the SELECT query and returns a list'''
        rows = self.conn.execute(f"SELECT {fields}  from {table_name} {condition};")
        return rows.fetchall()

    def insert_data(self, table_name: str, fields: str, values: str) -> None:
        '''performs the INSERT query and returns a list'''
        self.conn.execute(f"INSERT INTO  {table_name} ({fields}) VALUES ({values}) ")
        self.conn.commit()


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
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.schema = Schema(self.conn)
        self.user = None

    def authenticate(self, **kwargs):
        '''handle authentication'''
        email = kwargs.get("email")
        password = kwargs.get("password")

        password = self.generate_hash(password)

        self.user = self.schema.select_data("User", "*", f"where email='{email}' and password='{password}'")
        return self.user
        
    def unique_email(self, email: str) -> bool:
        '''check for unique email'''
        res = self.schema.select_data("User", "id", f"where email='{email}'")
        if len(res):
            return False
        return True

    def generate_hash(self, string: str) -> str:
        string = string.encode("utf-8")
        return hashlib.sha256(string).hexdigest()

        
    def register(self, **kwargs) -> bool:
        '''handles the registration'''
        name = kwargs.get("name")
        email = kwargs.get("email")
        password = kwargs.get("password")

        if self.unique_email(email):
            try:
                password = self.generate_hash(password) 
                self.schema.insert_data("User", "name, email, password", f"'{name}', '{email}', '{password}'")
                return True
            
            except Exception as e:
                with open(os.path.join(BASE_DIR, 'logs/register.errors.log'), 'a') as log_file:
                    log_file.write(f"\n[{str(datetime.now())}]: {str(e)}")
        
        return False