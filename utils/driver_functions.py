'''The Driver code and all the user interaction lives here'''
import os


def clear():
    '''functoin to clear the screen'''
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def get_user_choice():
    '''fuction to get the user's choice'''
    return int(input(">> "))
