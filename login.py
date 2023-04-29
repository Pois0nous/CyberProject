from termcolor import colored
from datetime import datetime
import time
import getInput
import getpass

def sign(cursor):# Create a menu when user enter the application.
    print("Please login or sign up to continue using our system!\n")
    print("1. I have an account, log me in.")
    print("2. I don't have an account, sign me up.")
    while True:
        userInput = input("\n-- Your choice: ")
        if userInput == "1":
            title, userid = login(cursor)
            return title, userid
        elif userInput == "2":
            userid = signUp(cursor)
            if userid == 0:
                continue
            title = "Customer"
            return title, userid
        else:
            print(colored('\n! Invalid input, please try again.\n', 'red'))


def login(cursor):# Customers and staff login in.
    title = ""
    print("\nPlease enter your username and password to log in.")
    while True:
        email = input("\n-- Email: ")
        password = getpass.getpass("-- Password: ")
        cursor.execute("BEGIN;")
        cursor.execute("SELECT * FROM customers WHERE email = %s AND password = %s FOR UPDATE", (email, password))#Query.(SELECT FROM WHERE AND FOR UPDATE)
        data = cursor.fetchone()
        if data:
            print(colored('\nCustomer login successful!\n', 'green'))
            title = "Customer"
            time.sleep(1)
            cursor.connection.commit()
            return title, data[0]
        else:
            cursor.execute("SELECT * FROM staff WHERE email = %s AND password = %s FOR UPDATE", (email, password))#Query.(SELECT FROM WHERE AND FRO UPDATE)
            data = cursor.fetchone()
            if data:
                title = "Staff"
                print(colored('\nStaff login successful!\n', 'green'))
                time.sleep(1)
                cursor.connection.commit()
                return title, data[0]
            else:
                cursor.connection.rollback()
                print(colored('\n! Invalid username or password, please try again.', 'red'))


def check_email(cursor, email): # Check the customers' number with the email.
    cursor.execute("SELECT COUNT(*) FROM customers WHERE email = %s", (email,))#Query.(SELECT COUNT() FROM WHERE)
    count = cursor.fetchone()[0]
    return count > 0


def signUp(cursor):# New user register.
    today = datetime.today()
    print("Please enter your information to sign up.")
    while True:
        firstname = input("\n-- First name: ")
        lastname = input("-- Last name: ")
        while True:# Age limit.
            dob = getInput.getDate("-- Date of birth (YYYY-MM-DD): ")
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 20:
                print(colored('\n! You must be at least 20 years old to sign up.\n', 'red'))
            elif age > 70:
                print(colored('\n! You must be less than 70 years old to sign up.\n', 'red'))
            else:
                break
        phone = getInput.getStringLength(12, "-- Phone number (xxxx-xxx-xxx): ")
        gender = getInput.getGender("-- Gender (M/F): ")
        while True:
            email = getInput.getEmail("-- Email: ")
            if check_email(cursor, email):
                print(colored('\n! Email address already exists. Please try again.\n', 'red'))
                return 0
            else:
                break
        
        while True:
            password = ""
            passwordRepeat = ""
            password = getInput.getPass("-- Password (Between 8 to 15 characters): ")
            passwordRepeat = getInput.getPass("-- Please input your password again: ")
            if password == passwordRepeat:
                break
            else:
                print(colored('\n! Passwords do not match, please try again.\n', 'red'))
        print(colored("\nPlease confirm your information.", 'cyan'))
        print("1. Yes, I confirm.")
        print("2. No, I want to change.")
        userInput = input("\n-- Your choice: ")
        if userInput == "1":
            try:
                cursor.execute("BEGIN;")
                cursor.execute("INSERT INTO customers (firstname, lastname, dob, phone, gender, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (firstname, lastname, dob, phone, gender, email, password))
                # Query.(INSERT INTO VALUES)
                cursor.execute("SELECT * FROM customers WHERE email = %s AND password = %s", (email, password))# Query.(SELECT FROM WHERE AND)
                data = cursor.fetchone()
                customer_id = data[0]
                print(colored('\nSign up successful!\n', 'green'))
                cursor.connection.commit()
                return customer_id
            except Exception as e:
                print(colored(f'\n! An error occurred while signing up.\n', 'red'))
                cursor.connection.rollback()
                return 0
        elif userInput == "2":
            continue
        else:
            print(colored('\n! Invalid input, please try again.\n', 'red'))
