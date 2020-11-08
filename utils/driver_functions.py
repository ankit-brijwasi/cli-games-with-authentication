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
