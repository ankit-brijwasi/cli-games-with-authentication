from utils.database_functions import Authentication, User
from utils.driver_functions import get_user_credentails


def try_login() -> User:
    email, password = get_user_credentails("login")
    authentication = Authentication()
    user = authentication.authenticate(email, password)
    if not user:
        print("\Incorrect email or password!")
        return try_login()
    return user
