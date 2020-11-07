'''The code for the backend and all the logics lives here'''
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'sqlite3.db')

class Database:
    '''All the functions regarding Database connectivity lives in this class'''

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)

    def close_db(self):
        self.connection.close()
