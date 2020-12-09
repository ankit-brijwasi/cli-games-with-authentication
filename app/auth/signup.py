from utils.database_functions import Authentication, User
from utils.driver_functions import get_user_credentails, error, primary, success
from app.auth.otp_verification import otp_verification

from utils.driver_functions import clear

from time import sleep

def try_register() -> User:
    clear()
    primary("SIGNUP".center(50, "-"))
    authentication = Authentication()
    name, email, password = get_user_credentails("signup")

    if not authentication.unique_email(email):
        error("InvalidEmail: This email is already registerd")
        try_register()

    user = authentication.register(name, email, password)
    if not user:
        error("Incorrect email or password!")
        return try_register()
    success("OTP sent...")
    sleep(0.7)
    success("Switching to OTP screen...")
    sleep(1.2)
    clear()
    return otp_verification()