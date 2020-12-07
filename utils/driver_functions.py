'''The Driver code and all the user interaction lives here'''
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content
from datetime import datetime
from pathlib import Path
import getpass
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / 'sqlite3.db'


def get_os() -> str:
    '''function to get the operating system'''
    return "windows" if os.name == "nt" else "linux"


def create_dirs() -> None:
    '''function to create dirs'''
    try:
        Path(BASE_DIR / 'logs').mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass


def clear() -> None:
    '''functoin to clear the screen'''
    os.system("cls") if get_os() == "windows" else os.system("clear")


def get_user_choice() -> int:
    '''fuction to get the user's choice'''
    return int(input(">> "))


def valid_email(email: str) -> bool:
    # check for valid syntax
    return True if "@" in email and "." in email else False


def valid_password(password: str) -> tuple:
    if len(password) < 6 or len(password) > 15:
        return False, "Password should be 6 - 15 characters long."
    elif password.isalpha():
        return False, "Password contains only alphabets."
    elif password.isnumeric():
        return False, "Password contains only numbers."
    else:
        return True, None


def get_user_credentails(screen: str) -> tuple:
    '''gets the user credentials'''
    if screen == "login":
        email = input("Enter e-mail: ")
        if valid_email(email):
            password = getpass.getpass(prompt="Enter password: ")
            return email, password
        print("InvalidEmail: Please enter a valid email address")
        return get_user_credentails("login")

    elif screen == "signup":
        email = input("Enter e-mail: ")
        if not valid_email(email):
            print("InvalidEmail: Please enter a valid email address\n")
            return get_user_credentails("signup")
        name = input("Enter your name: ")
        password = getpass.getpass(prompt="Enter password: ")
        is_valid, reason = valid_password(password)
        if not is_valid:
            print(f"InvalidPassword: {reason}\n")
            return get_user_credentails("signup")
        return name, email, password

    elif screen == "otp":
        email = input("Enter e-mail: ")
        if not valid_email(email):
            print("InvalidEmail: Please enter a valid email address\n")
            return get_user_credentails("otp")
        otp = input("Enter OTP: ")
        return email, otp

def send_mail(email_to: str, subject: str, message: str):
    '''function to send emails'''
    message = Mail(
        from_email='cli-games@patmui.com',
        to_emails=email_to,
        # PASSWORD: pobraphcifuymisv
        subject=subject,
        html_content=message)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
    except Exception as e:
        create_dirs()
        print("error occurred! Please check the logs")
        with open('logs/email.errors.log', 'a') as log_file:
            log_file.write(f"\n[{str(datetime.now())}]: {str(e)}")
