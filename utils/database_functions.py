'''The code for the backend and all the logics lives here'''
from datetime import datetime
from .driver_functions import BASE_DIR, DATABASE_PATH, create_dirs, send_mail
import sqlite3
import hashlib
import random


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
        '''performs the INSERT query'''
        self.conn.execute(
            f"INSERT INTO  {table_name} ({fields}) VALUES ({values}) ")
        self.conn.commit()

    def select_data(self, table_name: str, fields: str, condition: str):
        '''performs the SELECT query and returns a list'''
        rows = self.conn.execute(
            f"SELECT {fields} from {table_name} {condition};")
        return rows.fetchall()

    def insert_and_select(self, table_name: str, fields: str, values: str):
        '''Insert and return the inserted value'''
        self.insert_data(table_name, fields, values)

        condition = "WHERE "

        for key, value in zip(fields.split(","), values.split(",")):
            condition += f"{key}={value} and "
        condition = condition[:-5]

        res = self.select_data(table_name, "*", condition)
        return res

    def update_data(self, table_name: str, fields_and_values: str, condition: str):
        '''performs the UPDATE query'''
        self.conn.execute(
            f"UPDATE {table_name} SET {fields_and_values} {condition}")
        self.conn.commit()

    def update_and_select(self, table_name: str, fields_and_values: str, condition: str):
        '''Updates data and returns the updated columns'''
        self.update_data(table_name, fields_and_values, condition)
        return self.select_data(table_name=table_name, fields="*", condition=condition)


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
            "UserVerification",
            [
                "id INTEGER PRIMARY KEY AUTOINCREMENT",
                "code TEXT NOT NULL",
                "verified INTEGER NOT NULL DEFAULT 0",
                "user INTEGER",
                "FOREIGN KEY (user) REFERENCES User(id)",
            ]
        )

        # Migrate User Profile
        self.schema.create_table(
            "UserProfile",
            [
                "id INTEGER PRIMARY KEY AUTOINCREMENT",
                "games_played INTEGER NOT NULL DEFAULT 0",
                "games_woned INTEGER NOT NULL DEFAULT 0",
                "games_losed INTEGER NOT NULL DEFAULT 0",
                "user INTEGER",
                "FOREIGN KEY (user) REFERENCES User(id)",
            ]
        )

    def get_all_data(self):
        users = self.schema.select_data("User", "*", "")
        user_verifications = self.schema.select_data(
            "UserVerification", "*", "")
        user_profile = self.schema.select_data(
            "UserProfile", "*", "")
        return users, user_verifications, user_profile

    def close_db(self):
        self.conn.close()


class User:
    '''All opertions realted to a user are handled here'''

    def __init__(self, *args, **kwargs):
        self.id = args[0]
        self.name = args[1]
        self.email = args[2]
        self.password = args[3]
        self.verified = True if kwargs.get('verified') == 1 else False

    def get_user_profile(self) -> dict:
        self.conn = sqlite3.connect(DATABASE_PATH)
        schema = Schema(conn=self.conn)
        user_profile = schema.select_data(
            table_name="UserProfile",
            fields="games_played, games_woned, games_losed",
            condition="WHERE user='{}'".format(self.id)
        )
        if len(user_profile) == 0:
            return {
                'games_played': 0,
                'games_woned': 0,
                'games_losed': 0,
            }
        return {
            'games_played': user_profile[0][0],
            'games_woned': user_profile[0][1],
            'games_losed': user_profile[0][2],
        }

    def won_game(self) -> None:
        games_woned = self.get_user_profile().get('games_woned')
        schema = Schema(conn=self.conn)
        won = games_woned + 1
        schema.update_data(
            table_name="UserProfile",
            fields_and_values="games_woned='{}'".format(won),
            condition="WHERE user={}".format(self.id)
        )

    def lost_game(self) -> None:
        games_losed = self.get_user_profile().get('games_losed')
        schema = Schema(conn=self.conn)
        lost = games_losed + 1
        schema.update_data(
            table_name="UserProfile",
            fields_and_values="games_losed='{}'".format(lost),
            condition="WHERE user={}".format(self.id)
        )

    def entered_match(self) -> None:
        games_played = self.get_user_profile().get('games_played')
        schema = Schema(conn=self.conn)
        played = games_played + 1
        schema.update_data(
            table_name="UserProfile",
            fields_and_values="games_played='{}'".format(played),
            condition="WHERE user={}".format(self.id)
        )


class Authentication:
    '''Class to handle Login and Signup'''

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.schema = Schema(self.conn)

    def authenticate(self, email: str, password: str) -> User:
        '''handle's authentication and returns the user if exists otherwise returns None'''
        print("\nlogging in...")
        password = self.generate_hash(password)
        user = self.schema.select_data(
            table_name="User",
            fields="*",
            condition=f"WHERE email='{email}' and password='{password}'"
        )
        if len(user) == 0:
            return None
        user = user[0]
        user_verified = self.schema.select_data(
            table_name="UserVerification",
            fields="verified",
            condition=f"WHERE user='{user[0]}'"
        )[0]
        return User(*user, verified=user_verified[0])

    def unique_email(self, email: str) -> bool:
        '''check for unique email'''
        res = self.schema.select_data("User", "id", f"WHERE email='{email}'")
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
                table_name="User",
                fields="name, email, password",
                values=f"'{name}', '{email}', '{password}'"
            )[0]

            otp = random.randint(1000, 9999)
            user_verfication = self.schema.insert_and_select(
                table_name="UserVerification",
                fields="code, user",
                values=f"'{otp}', '{user[0]}'"
            )[0]
            print("Sending OTP..")
            body = f"Hey, Thank you for showing your interese in our Application.\n\nYour One Time Password (OTP) is {otp}\n\nThank you\nTeam Pythonera"
            sent, err = send_mail(
                email_to=email, subject="Verify your email", body=body)

            if err:
                print("Error while sending OTP")
                print(err)

            return User(*user, verified=user_verfication[1])

        except Exception as e:
            create_dirs()
            print("error occurred! Please check the logs")
            with open('logs/register.errors.log', 'a') as log_file:
                log_file.write(f"\n[{str(datetime.now())}]: {str(e)}")
        return None

    def verify_email(self, otp: int, email: str) -> User:
        user = self.schema.select_data(
            table_name="User, UserVerification",
            fields="*",
            condition=f"WHERE User.email='{email}' and UserVerification.code='{otp}' and UserVerification.verified=0"
        )

        if len(user) == 0:
            return None
        user = user[0]
        self.schema.update_data(
            table_name="UserVerification",
            fields_and_values="verified=1",
            condition=f"WHERE user={user[0]} and code='{otp}'")

        self.schema.insert_data(
            table_name="UserProfile",
            fields="user",
            values=f"'{user[0]}'"
        )

        return User(*user, verified=1)
