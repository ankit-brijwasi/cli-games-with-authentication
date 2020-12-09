import time

from app.core.game import game, game_screen
from utils.database_functions import User
from utils.driver_functions import clear, get_user_choice, success, warning, primary


def get_choice(message: str) -> str:
    warning("\n{} (y/n)".format(message))
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
    primary("Profile Information".center(50, '-'))
    primary(f"Name: {user.name}")
    primary(f"E-mail: {user.email}")
    primary(f"Matches Played: {profile.get('games_played', 0)}")
    primary(f"Matches Won: {profile.get('games_woned', 0)}")
    primary(f"Matches Lost: {profile.get('games_losed', 0)}")


def welcome_screen(user: User) -> None:
    clear()
    primary("Welcome to the Application".center(50, "-"))
    primary("Select your choice\n")
    print("1 Play the Game \n2 Check your info\n3 Logout\n")

    choice = get_user_choice()

    if choice == 1:
        play_game(user)

    elif choice == 2:
        clear()
        profile_info = user.get_user_profile()
        show_profile(user, profile=profile_info)
        _ = input("Press any key to go back...")
        return welcome_screen(user)

    elif choice == 3:
        success("Logging out...")
        time.sleep(2)

    else:
        warning("You pressed wrong key")
        time.sleep(2)
        return welcome_screen(user)
