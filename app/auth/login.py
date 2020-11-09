from utils.database_functions import Authentication
from utils.driver_functions import get_user_credentails


def try_login() -> user:
    email, password = get_user_credentails("login")
    authentication = Authentication()
    user = authentication.authenticate(email, password)
    if not user:
        print("\nThis user doesn't exists!")
        return try_login()
    return user
