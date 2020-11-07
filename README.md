# GUESSING GAME WITH AUTH

A guesssing game with authentication built using core python

Getting Started -

> Note: For windows users, You must have to download git bash to clone the project

> Download Git bash from here - https://github.com/git-for-windows/git/releases/download/v2.29.2.windows.2/Git-2.29.2.2-64-bit.exe

To get started with the repo, firstly clone the repo by copy this command to terminal/Git Bash-
`git clone https://www.github.com/ankit-brijwasi/cli-games-with-authentication`

After the cloning of project has been done, the below structure will be generated

Installing the required packages -

1. navigate to the root directory using terminal/Git Bash [To the place where the requirements.txt lives]
2. run this command -> `pip install -r requirements.txt`, optionally you can create virtual environment before running this command.
3. To run the application type this command -> `python main.py`

Git Commands -

> To track/stage the changes use the following command -

> `git add .`

> To commit your changes use the following command -

> `git commit -m "a short description of what you have done"`

> **Note that**, before commiting you must track/stage your changes

> To push/upload your changes use the following command -

> `git pull origin master`

> Execute the next 2 commands only if the origin master branch is ahead of your local master branch, skip to **push command** if you see **Everything is up to date** message-

> `git add .`

> `git commit -m "merged branches"`

> To publish your code -

> `git push origin master`

If you find any diffculties or errors, contact to the team members and we'll try to rectify your queries.

Structure -

    Note: D represents Directory/folder

    cli-games-with-authentication
    |-app [D]
        |-auth [D]
        |-game [D]
        |-__init__.py
        |-default_app.py
    |-utils [D]
        |-__init__.py
        |-database_functions.py
        |-driver_functions.py
    |-sqlite3.db
    |-main.py
    |-README.md
    |-requirements.txt

    The above diagram represents the folder scheme of how the project is divided.

    ** Some files or folders can differ **

    All the code, will come into their respected folders

    ** This structure can be altered in the future **

Modules -

    The project is divided in two parts -

    1. Backend and Databases -
        This module covers all the logics that will be going behind the scenes
        The persons assigned to this module will mainly work in the following folders/files-
            a. utils/database_functions.py [file, To get a biref idea on what this file does refer to the file]
            b. auth [Directory]
            c. game [Directory]
            d. app/default_app.py [file]
            e. main.py [file]

    Assigned to - Rajesh, Ankit

    2. Frontend -
        This module contains the functions, that are responsible for getting the data correctly from the user
        Please use the same names for the functions specified here and also,
        make sure that the function also returns the same thing which is specified here

        The persons assigned to this module will mainly work in the following folders/files-
            a. utils/driver_functions.py [file, To get a biref idea on what this file does refer to the file]
            b. main.py [file]

        Assigned to - Harshita, Deepti, Khushboo

        Functions -

        -> get_user_choice() --> returns the choice user has enterd, takes no arguments
        -> get_user_credentials() --> returns the email and password of the user, takes no arguments
        -> clear() --> clears the screen

        [More functionalities will be added as the project progresses]

        Also, we will be using colorama library to make the interface look different.
        So be sure that you have an idea of colorama.

        Go to this link to see what colorama is, and how can it be used

        https://www.geeksforgeeks.org/print-colors-python-terminal/
