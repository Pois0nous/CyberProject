import psycopg2
import base64
import os
from passlib.hash import bcrypt

# Connect to the PostgreSQL database.
conn = psycopg2.connect(user = "postgres",
                        password = "2546",
                        host = "localhost",
                        port = 5432,
                        database = "test2")
cur = conn.cursor()

# Generate a key.
key = os.urandom(16)

# Define a function to sign up a user.
def signup():
    # Get the username and password from the user.
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    # Encrypt the password.
    encrypted_password = bcrypt.hash(password)

    # Save the user to the database.
    cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, encrypted_password))
    conn.commit()

    print('User created successfully!')

# Define a function to sign in a user.
def signin():
    # Get the username and password from the user.
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    # Get the encrypted password from the database.
    cur.execute('SELECT password FROM users WHERE username = %s', (username,))
    row = cur.fetchone()

    # Check if the row is None.
    if row is None:
        print('Invalid username or password.')
    else:
        encrypted_password = row[0]
        # Check if the password is correct.
        if bcrypt.verify(password, encrypted_password):
            print('Login successful!')
        else:
            print('Invalid username or password.')


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