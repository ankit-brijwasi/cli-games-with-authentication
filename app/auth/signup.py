from utils.database_functions import Authentication, User
from utils.driver_functions import get_user_credentails

from utils.driver_functions import clear

def try_register() -> User:
    clear()
    print("SIGNUP".center(50, "-"))
    authentication = Authentication()
    name, email, password = get_user_credentails("signup")

    if not authentication.unique_email(email):
        print("InvalidEmail: This email is already registerd")
        try_register()

    user = authentication.register(name, email, password)
    if not user:
        print("Incorrect email or password!")
        return try_register()
    return user
