import msvcrt
import psycopg2
import os
from passlib.hash import bcrypt
import getpass
import re
from termcolor import colored
import zxcvbn

clear = lambda: os.system('cls')

# Connect to the PostgreSQL database.
conn = psycopg2.connect(user = "postgres",
                        password = "2546",
                        host = "localhost",
                        port = 5432,
                        database = "test3")
cur = conn.cursor()

# Generate a key.
key = os.urandom(16)


def main():
    clear()
    while True:
        print(colored('### Welcome to the Cybersecurity forum!\n', 'blue'))
        print('1. Sign up')
        print('2. Sign in')
        print('3. Exit')

        # Get the user's choice.
        choice = input('\n-- Enter your choice: ')
        print()

        # Execute the corresponding function.
        if choice == '1':
            signup()
        elif choice == '2':
            signin()
        elif choice == '3':
            clear()
            print(colored('### Goodbye! ###\n', 'blue'))
            break
    # Close the connection to the PostgreSQL database.
    conn.close()


# Define a function to sign up a user.
def signup():
    clear()
    print(colored('### Please enter a unique username and a strong password to sign up!\n', 'blue'))
    # Get the username and password from the user.
    username = input('-- Enter your username: ')
    
    # Validate the username.
    while not validate_username_unique(username):
        print(colored("\n! The username already exists!\n", 'red'))
        username = input('-- Enter your username: ')

    password = getpass.getpass(prompt='-- Enter your password: ')

    # Validate the password.
    while not validate_password(password):
        password_strength(password)
        password = getpass.getpass(prompt='-- Enter your password: ')

    # Encrypt the password.
    encrypted_password = bcrypt.hash(password)

    # Save the user to the database.
    cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, encrypted_password))
    conn.commit()

    print(colored('\nRegistration Successful!', 'green'))
    print(colored("\nPress any key to continue...", 'cyan'), end = '', flush = True)
    msvcrt.getch()
    clear()

# Define a function to sign in a user.
def signin():
    clear()
    print(colored('### Please enter your username and password to sign in!\n', 'blue'))
    # Get the username and password from the user.
    username = input('-- Enter your username: ')
    password = getpass.getpass(prompt='-- Enter your password: ')

    # Get the encrypted password from the database.
    cur.execute('SELECT password FROM users WHERE username = %s', (username,))
    row = cur.fetchone()

    # Check if the row is None.
    if row is None:
        print(colored("\n! Wrong username or password. Try again.", 'red'))
    else:
        encrypted_password = row[0]
        # Check if the password is correct.
        if bcrypt.verify(password, encrypted_password):
            print(colored(f'\nYou are authenticated, Welcome {username}', 'green'))
        else:
            print(colored("\n! Wrong username or password. Try again.", 'red'))

    print(colored("\nPress any key to continue...", 'cyan'), end = '', flush = True)
    msvcrt.getch()
    clear()

# Define a function to validate the username.
def validate_username_unique(username):
    cur.execute('SELECT username FROM users')
    users = cur.fetchall()
    for user in users:
        if user[0] == username:
            return False
    return True

# Define a function to validate the password.
def validate_password(password):
    # Check if the password is longer than 8 characters.
    if len(password) < 8:
        print(colored("\n! Password should be longer than 8 characters.", 'red'))
        return False

    # Check if the password has at least one small letter.
    if not re.search(r'[a-z]', password):
        print(colored("\n! Password should contain at least one small letter.", 'red'))
        return False

    # Check if the password has at least one capital letter.
    if not re.search(r'[A-Z]', password):
        print(colored("\n! Password should contain at least one capital letter.", 'red'))
        return False

    # Check if the password has at least one number.
    if not re.search(r'\d', password):
        print(colored("\n! Password should contain at least one number.", 'red'))
        return False

    # Check if the password has at least one special character.
    if not re.search(r'[!@#$%^&*()_+{}:"<>?]', password):
        print(colored("\n! Password should contain at least one special character.", 'red'))
        return False

    return True

# Define a function to check the strength of a password.
def password_strength(password):
    result = zxcvbn.zxcvbn(password)
    score = result["score"]
    feedback = result["feedback"]["warning"] if "warning" in result["feedback"] else result["feedback"]["suggestions"][0]
    print(colored("\nPassword strength: " + str(score) + "/4", 'yellow'))
    if (feedback == ""):
        feedback = "No feedback"
    print(colored("Feedback: " + feedback + "\n", 'yellow'))

main()
