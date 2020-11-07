'''The main application'''
from utils.driver_functions import get_user_choice, clear
from utils.database_functions import Database

db = Database()

def app():
    print("Welcome to guessing game\n1 Login\n2 Sign up\n")
    choice = get_user_choice()
    clear()
    print(choice)
