import random

from utils.driver_functions import clear, primary, warning, success, secondary
from utils.database_functions import User


def game_screen() -> None:
    clear()
    primary(" What's inside the box? ".center(50, "-"))
    primary('''
.
. . .
. . . . 
.. . . . . 
.. . . . . . .
. . . . . . . . .
. . . . . . . . . . . 
. . . . . . . . . . . . .
. . . . . . . . . . . . .   #
 . . . . . . . . . . .   #     #
   . . . . . . . . .  #           #
     . . . . . . .  #       ?       #
        . . . . . . # #           # #
          . . . . . #    #     #    #
             . . .  #       #       #
                . . #       #       #
                  . #       #       #
                     . #    #     # 
                        .#  #  #
                           .#

TASK:
    - There is a number inside this box. GUESS it.

RULES:
    - You have to guess the number
    - The number is between 1 - 100
    - You have 5 lifes 
''')


def _get_user_number() -> int:
    try:
        return int(input("Enter the number: "))
    except Exception:
        warning("Characters and floating numbers are not allowed")
        return _get_user_number()


def game(user: User) -> None:
    user.entered_match()
    computer_number = random.randint(1, 100)
    i = 1
    while True:
        if i >= 6:
            user.lost_game()
            secondary("You are out of life's")
            secondary("Number was: {}".format(computer_number))
            break
        if i == 5:
            secondary("This is your last life for defeating the computer\n")

        if i == 4:
            secondary("Carefull! you have only {} lifes left\n".format(6 - i))

        user_number = _get_user_number()

        if user_number == computer_number:
            user.won_game()
            success("Yippee! This was a correct guess")
            success("You defeated the computer!")
            break

        if user_number >= computer_number - 10 and user_number <= computer_number:
            if i == 5:
                pass
            else:
                primary("This number is low, but you are getting close to the number")

        elif user_number >= computer_number and user_number <= computer_number + 10:
            if i == 5:
                pass
            else:
                primary("This number is high, but you are getting close to the number")

        elif user_number > computer_number:
            primary("This number is too high")

        elif user_number < computer_number:
            primary("This number is too low")

        i += 1
