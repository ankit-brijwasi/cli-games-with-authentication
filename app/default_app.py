'''The main application'''
import time

from utils.driver_functions import clear, get_user_choice

from app.auth.login import try_login
from app.auth.otp_verification import otp_verification
from app.auth.signup import try_register
from app.core.main import welcome_screen


def app():
    while True:
        clear()
        print("Select your choice")
        print("1 Login\n2 Sign up\n3 Verify Otp\n")

        choice = get_user_choice()
        clear()

        if choice == 1:
            user = try_login()
            welcome_screen(user)
            app()

        elif choice == 2:
            user = try_register()
            welcome_screen(user)

        elif choice == 3:
            user = otp_verification()
            welcome_screen(user)

        else:
            print("Invalid Choice")
            time.sleep(2)
            continue
