'''The main application'''
from utils.driver_functions import clear, get_user_choice
from app.auth.login import try_login
from app.auth.signup import try_register


def app():
    while True:
        clear()
        print("Welcome to guessing game\n1 Login\n2 Sign up\n")

        choice = get_user_choice()
        clear()

        if choice == 1:
            user = try_login()
            print(user.name)
            print(user.id)
            break

        elif choice == 2:
            user = try_register()
            print(user.name)
            print(user.id)
            break

        else:
            break
