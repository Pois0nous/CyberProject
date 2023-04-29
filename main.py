import psycopg2
import base64
import os
from passlib.hash import bcrypt
import getpass
import re
from termcolor import colored


# Connect to the PostgreSQL database.
conn = psycopg2.connect(user = "postgres",
                        password = "hacker123",
                        host = "localhost",
                        port = 5432,
                        database = "test4")
cur = conn.cursor()

# Generate a key.
key = os.urandom(16)

# Define a function to sign up a user.
def signup():
    # Get the username and password from the user.
    username = input('Enter your username: ')
    
    #Validate the username
    while not validate_username_unique(username):
        print(colored("\n!The username has been used.", 'red'))
        print(colored(" Please type a different username", 'red'))
        username = input('Enter your username: ')
    
    password = getpass.getpass(prompt='Enter your password: ')

    # Validate the password.
    while not validate_password(password):
        print(colored("\n!Invalid password.", 'red'))
        print(colored("Please enter a password that is longer than 8 characters and has at least one small letter, one capital, one number, and one special character.\n", 'red'))
        password = getpass.getpass(prompt='Enter your password: ')

    # Encrypt the password.
    encrypted_password = bcrypt.hash(password)

    # Save the user to the database.
    cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, encrypted_password))
    conn.commit()

    print('Registration Successful')

# Define a function to sign in a user.
def signin():
    # Get the username and password from the user.
    username = input('Enter your username: ')
    password = getpass.getpass(prompt='Enter your password: ')

    # Get the encrypted password from the database.
    cur.execute('SELECT password FROM users WHERE username = %s', (username,))
    row = cur.fetchone()

    # Check if the row is None.
    if row is None:
        print('Please enter correct username password')
    else:
        encrypted_password = row[0]
        # Check if the password is correct.
        if bcrypt.verify(password, encrypted_password):
            print('You are authenticated, Welcome %s', (username))
        else:
            print('Please enter correct username password')


def validate_username_unique(username):
    cur.execute('SELECT username FROM users')
    users = cur.fetchall()
    for user in users:
        if user[0] == username:
            return False
    return True

def validate_password(password):
    # Check if the password is longer than 8 characters.
    if len(password) < 8:
        return False

    # Check if the password has at least one small letter.
    if not re.search(r'[a-z]', password):
        return False

    # Check if the password has at least one capital letter.
    if not re.search(r'[A-Z]', password):
        return False

    # Check if the password has at least one number.
    if not re.search(r'\d', password):
        return False

    # Check if the password has at least one special character.
    if not re.search(r'[!@#$%^&*()_+{}:"<>?]', password):
        return False

    return True

# Display the menu.
while True:
    print('1. Sign up')
    print('2. Sign in')
    print('3. Exit')

    # Get the user's choice.
    choice = input('Enter your choice: ')

    # Execute the corresponding function.
    if choice == '1':
        signup()
    elif choice == '2':
        signin()
    elif choice == '3':
        break

# Close the connection to the PostgreSQL database.
conn.close()