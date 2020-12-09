from utils.database_functions import Authentication, User
from utils.driver_functions import get_user_credentails, clear

from app.auth.login import try_login
from time import sleep


def otp_verification() -> User:
    clear()
    print("OTP VERIFICATION".center(50, "-"))
    authentication = Authentication()
    email, otp = get_user_credentails("otp")

    user = authentication.verify_email(otp=otp, email=email)
    if not user:
        print("Invalid OTP or e-mail")
        sleep(2)
        return otp_verification()
    print("e-mail verified")
    sleep(0.4)
    print("Redirecting to login screen...")
    sleep(1)
    return try_login()
