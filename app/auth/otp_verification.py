from utils.database_functions import Authentication, User
from utils.driver_functions import get_user_credentails, clear, error, primary, success

from app.auth.login import try_login
from time import sleep


def otp_verification() -> User:
    clear()
    primary("OTP VERIFICATION".center(50, "-"))
    authentication = Authentication()
    email, otp = get_user_credentails("otp")

    user = authentication.verify_email(otp=otp, email=email)
    if not user:
        error("Invalid OTP or e-mail")
        sleep(2)
        return otp_verification()
    success("e-mail verified")
    sleep(0.4)
    success("Redirecting to login screen...")
    sleep(1)
    return try_login()
