'''The Driver code and all the user interaction lives here'''
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content
from datetime import datetime
from pathlib import Path
import getpass
import os
import smtplib


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
        email = email.lower()
        if valid_email(email):
            password = getpass.getpass(prompt="Enter password: ")
            return email, password
        print("InvalidEmail: Please enter a valid email address")
        return get_user_credentails("login")

    elif screen == "signup":
        name = input("Enter your name: ")
        email = input("Enter e-mail: ")
        email = email.lower()
        if not valid_email(email):
            print("InvalidEmail: Please enter a valid email address\n")
            return get_user_credentails("signup")
        password = getpass.getpass(prompt="Enter password: ")
        is_valid, reason = valid_password(password)
        if not is_valid:
            print(f"InvalidPassword: {reason}\n")
            return get_user_credentails("signup")
        return name, email, password

    elif screen == "otp":
        email = input("Enter e-mail: ")
        email = email.lower()
        if not valid_email(email):
            print("InvalidEmail: Please enter a valid email address\n")
            return get_user_credentails("otp")
        otp = input("Enter OTP: ")
        return email, otp

def send_mail(**kwargs):
    '''function to send emails'''

    gmail_user = 'joshirajesh448@gmail.com'
    gmail_password = 'pobraphcifuymisv'

    sent_from = gmail_user
    
    email_text = str(f"From:{sent_from}\nTo:{kwargs.get('email_to')}\nSubject:{kwargs.get('subject')}\n\n{kwargs.get('body')}")

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)

    try:
        server.sendmail(sent_from, kwargs.get('email_to'), email_text)
        server.close()

        return True, None
    except Exception as e:
        create_dirs()
        with open('logs/email.errors.log', 'a') as log_file:
            log_file.write(f"\n[{str(datetime.now())}]: {str(e)}")
        return False, e