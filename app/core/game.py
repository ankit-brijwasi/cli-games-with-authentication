import random

from utils.driver_functions import clear
from utils.database_functions import User


def game_screen() -> None:
    clear()
    print(" What's inside the box? ".center(50, "-"))
    print('''
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
    except Exception as e:
        print("Characters and floating numbers are not allowed")
        return _get_user_number()


def game(user: User) -> None:
    user.entered_match()
    computer_number = random.randint(1, 100)
    i = 1
    print(computer_number)
    while True:
        if i >= 6:
            user.lost_game()
            print("You are out of life's")
            print("Number was: {}".format(computer_number))
            break
        if i == 5:
            print("This is your last life for defeating the computer\n")

        if i == 4:
            print("Carefull! you have only {} lifes left\n".format(6 - i))

        user_number = _get_user_number()

        if user_number == computer_number:
            user.won_game()
            print("Yippee! This was a correct guess")
            print("You defeated the computer!")
            break

        if user_number >= computer_number - 10 and user_number <= computer_number:
            if i == 5:
                pass
            else:
                print("This number is low, but you are getting close to the number")

        elif user_number >= computer_number and user_number <= computer_number + 10:
            if i == 5:
                pass
            else:
                print("This number is high, but you are getting close to the number")

        elif user_number > computer_number:
            print("This number is too high")

        elif user_number < computer_number:
            print("This number is too low")

        i += 1
