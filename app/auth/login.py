from utils.database_functions import Authentication, User
from utils.driver_functions import get_user_credentails
from utils.driver_functions import clear

from time import sleep

def try_login() -> User:
    clear()
    print("LOGIN".center(50, "-"))
    email, password = get_user_credentails("login")
    authentication = Authentication()
    user = authentication.authenticate(email, password)
    if not user:
        print("Incorrect email or password!")
        sleep(1)
        return try_login()
    if not user.verified:
        print("Please verify your e-mail first.")
        sleep(1)
        return try_login()

    return user
