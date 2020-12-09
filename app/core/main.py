import time

from app.core.game import game, game_screen
from utils.database_functions import User
from utils.driver_functions import clear, get_user_choice


def get_choice(message: str) -> str:
    print("\n{} (y/n)".format(message))
    return input(">> ")


def play_game(user: User) -> None:
    clear()
    game_screen()
    game(user)
    choice = get_choice(message="Play again ?")
    if choice == "y" or choice == "Y":
        return play_game(user)
    else:
        return welcome_screen(user)


def show_profile(user: User, profile: dict) -> None:
    print("Profile Information".center(50, '-'))
    print("Name: ", user.name)
    print("E-mail: ", user.email)
    print("Matches Played: ", profile.get('games_played', 0))
    print("Matches Won: ", profile.get('games_woned', 0))
    print("Matches Lost: ", profile.get('games_losed', 0))


def welcome_screen(user: User) -> None:
    clear()
    print("Welcome to the Application".center(50, "-"))
    print("Select your choice\n")
    print("1 Play the Game \n2 Check your info\n3 Logout\n")

    choice = get_user_choice()

    if choice == 1:
        play_game(user)

    elif choice == 2:
        clear()
        profile_info = user.get_user_profile()
        show_profile(user, profile=profile_info)
        key = input("Press ENTER key to go back...")
        return welcome_screen(user)

    elif choice == 3:
        print("Logging out...")
        time.sleep(2)

    else:
        print("You pressed wrong key")
        time.sleep(2)
        return welcome_screen(user)
