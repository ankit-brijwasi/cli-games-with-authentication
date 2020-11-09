'''The Driver code and all the user interaction lives here'''
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / 'sqlite3.db'


def get_os() -> str:
    '''function to get the operating system'''
    return "windows" if os.name == "nt" else "linux"


def create_dirs() -> None:
    '''function to create dirs'''
    try:
        Path(BASE_DIR / 'logs').mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass


def clear() -> None:
    '''functoin to clear the screen'''
    os.system("cls") if get_os() == "windows" else os.system("clear")


def get_user_choice() -> int:
    '''fuction to get the user's choice'''
    return int(input(">> "))


def valid_email(email: str) -> bool:
    return True if "@" in email and "." in email else False


def valid_password(password: str) -> tuple:
    if len(password) >= 6 and len(password) <= 15:
        return False, "Password should be 6 - 15 characters long."
    elif password.isalpha():
        return False, "Password contains only alphabets."
    elif password.isnumeric():
        return False, "Password contains only numbers."
    else:
        return True, None


def get_user_credentails(screen: str) -> tuple:
    '''gets the user credentials'''
    if screen == "login":
        email = input("Enter e-mail: ")
        if valid_email(email):
            password = input("Enter password: ")
            return email, password
        print("InvalidEmail: Please enter a valid email address")
        return get_user_credentails("login")

    elif screen == "signup":
        name = input("Enter your name: ")
        email = input("Enter e-mail: ")
        if not valid_email(email):
            print("InvalidEmail: Please enter a valid email address")
            return get_user_credentails("signup")
        password = input("Enter password: ")
        is_valid, reason = valid_password(password)
        if not is_valid:
            print(f"InvalidPassword: {reason}")
            return get_user_credentails("signup")
        return name, email, password
