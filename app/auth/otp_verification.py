from utils.database_functions import Authentication, User
from utils.driver_functions import get_user_credentails

def otp_verification():
    authentication = Authentication()
    email, otp = get_user_credentails("otp")

    authentication.verify_email(otp=otp, email=email)