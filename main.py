import os
import psycopg2 as pg
from termcolor import colored
import time
import login
import menu
import getpass

clear = lambda: os.system('cls')

def main():# Main program.
    clear()
    print(colored(f'### Welcome to the Car Rental System ###', 'green'))
    print("\nPlease connect to the database first:")
    cursor = dbConnect()
    title, userid = login.sign(cursor)
    print(title, userid)
    clear()
    menu.greeting(cursor, title, userid)

def dbConnect(): # Database connection.
        while True:
            try:
                dbName = input("-- Input the database name: ")
                dbPassword = getpass.getpass("-- Input the database password: ")

                connection = pg.connect(user = "postgres",
                                            password = dbPassword,
                                            host = "localhost",
                                            port = 5432,
                                            database = dbName)
                cursor = connection.cursor()
                print(colored('\nConnection successful!', 'green'))
                time.sleep(1)
                clear()
                return cursor
            except (Exception, pg.Error) as error:
                print(colored('\n! Error while connecting to the database. Please try again.\n', 'red'))

main()
