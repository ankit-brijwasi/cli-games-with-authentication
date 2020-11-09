'''The main application'''
from utils.driver_functions import clear, get_user_choice
from app.auth.login import try_login


def app():
    while True:
        clear()
        print("Welcome to guessing game\n1 Login\n2 Sign up\n")

        choice = get_user_choice()
        clear()

        if choice == 1:
            user = try_login()
            print(user)
            break

        elif choice == 2:
            pass

        else:
            break
