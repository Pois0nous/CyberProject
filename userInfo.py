import os
import getInput
from termcolor import colored
import msvcrt
import time

clear = lambda: os.system('cls')

def userChange(cursor, userid, title):# User change information menu.
    clear()
    while True:
        print("1) Change your name\n2) Change your phone number\n3) Change your email\n4) Change your password\n0) Back")
        userInput = getInput.getInt("\n-- Your choice: ")
        match userInput:
            case 1:
                clear()
                while True:
                    print("\n1) Change your first name\n2) Change your lastname\n0) Back")
                    userInput = getInput.getInt("\n-- Your choice: ")
                    match userInput:
                        case 1:
                            changeFirst(cursor, userid, title)
                        case 2:
                            changeLast(cursor, userid, title)
                        case 0:
                            break
                        case _:
                            print(colored('\n! Invalid input, please try again.\n', 'red'))
            case 2:
                changePhone(cursor, userid, title)
            case 3:
                changeEmail(cursor, userid, title)
            case 4:
                changePassword(cursor, userid, title)
            case 0:
                break
            case _:
                print(colored('\n! Invalid input, please try again.\n', 'red'))
        clear()
    clear()
    return()

def changeFirst(cursor, userid, title):# User change first name.
    newFirst = input("\n-- New first name: ")
    try:
        cursor.execute("BEGIN;")
        if title == "Customer":
            cursor.execute(
                "UPDATE customers SET firstname = %s WHERE customerid = %s",
                (newFirst, userid)
            )# Query(UPDATE SET WHERE)
        else:
            cursor.execute(
                "UPDATE staff SET firstname = %s WHERE staffid = %s",
                (newFirst, userid)
            )# Query (UPDATE SET WHERE)
        cursor.connection.commit()
        print(colored('\nFirst name changed successfully!', 'green'))
        time.sleep(1)
    except:
        print(colored(f'\n! Error while changing first name\n', 'red'))
        cursor.connection.rollback()
    return

def changeLast(cursor, userid, title):# User change last name.
    newLast = input("\n-- New last name: ")
    try:
        cursor.execute("BEGIN;")
        if title == "Customer":
            cursor.execute(
                "UPDATE customers SET lastname = %s WHERE customerid = %s",
                (newLast, userid)
            )#Query (UPDATE SET WHERE)
        else:
            cursor.execute(
                "UPDATE staff SET lastname = %s WHERE staffid = %s",
                (newLast, userid)
            )#Query(UPDATE SET WHERE)
        cursor.connection.commit()
        print(colored('\nFirst name changed successfully!', 'green'))
        time.sleep(1)
    except:
        print(colored(f'\n! Error while changing last name\n', 'red'))
        cursor.connection.rollback()
    return
def changePhone(cursor, userid, title):# User change phone number.
    newPhone = getInput.getStringLength(12, "-- New phone number (xxxx-xxx-xxx): ")
    try:
        cursor.execute("BEGIN;")
        if title == "Customer":
            cursor.execute(
                "UPDATE customers SET phone = %s WHERE customerid = %s",
                (newPhone, userid)
            )#Query(UPDATE SET WHERE)
        else:
            cursor.execute(
                "UPDATE staff SET phone = %s WHERE staffid = %s",
                (newPhone, userid)
            )#Query(UPDATE SET WHERE)
        cursor.connection.commit()
        print(colored('\nPhone number changed successfully!\n', 'green'))
        time.sleep(1)
    except:
        print(colored(f'\n! Error while changing phone number\n', 'red'))
        cursor.connection.rollback()
    return

def changeEmail(cursor, userid, title):# User change the email.
    try:
        cursor.execute("BEGIN;")
        newEmail = getInput.getEmail("-- New email: ")
        if title == "Customer":
            cursor.execute(
                "UPDATE customers SET email = %s WHERE customerid = %s",
                (newEmail, userid)
            )# Query (UPDATE SET WHERE)
        else:
            cursor.execute(
            "UPDATE staff SET email = %s WHERE staffid = %s",
            (newEmail, userid)
            )#Query(UPDATE SET WHERE)
        cursor.connection.commit()
        print(colored('\nEmail changed successfully!\n', 'green'))
        time.sleep(1)
    except:
        print(colored(f'\n! Error while changing email\n', 'red'))
        cursor.connection.rollback()
    return

def changePassword(cursor, userid, title):# User change the password.
    while True:
        newPassword = getInput.getPass("-- New Password (Between 8 to 16 characters): ")
        newPasswordRepeat = getInput.getPass("-- Please input your password again: ")
        if newPassword == newPasswordRepeat:
            break
        else:
            print(colored('\n! Passwords do not match, please try again.\n', 'red'))
    try:
        cursor.execute("BEGIN;")
        if title == "Customer":
            cursor.execute(
                "UPDATE customers SET password = %s WHERE customerid = %s",
                (newPassword, userid)
            )#Query(UPDATE SET WHERE)
        else:
            cursor.execute(
                "UPDATE staff SET password = %s WHERE staffid = %s",
                (newPassword, userid)
            )#Query(UPDATE SET WHERE)
        cursor.connection.commit()
        print(colored('\nPassword changed successfully!\n', 'green'))
        time.sleep(1)
    except:
        print(colored(f'\n! Error while changing password\n', 'red'))
        cursor.connection.rollback()
    return

def findCustomer(cursor):#Check the customer information with email.
    clear()
    while True:
        userEmail = getInput.getEmail("\n-- Enter the email address: ")
        cursor.execute("SELECT * FROM customers WHERE email = %s", [userEmail])#Query(SELECT FROM WHERE)
        data = cursor.fetchone()
        if data is None:
            print(colored('\n! Customer not found, please try again.\n', 'red'))
            break
        else:
            print(colored(f'\n### Customer found: {data[1]} {data[2]}', 'green'))
            print(f'### Customer ID: {data[0]}')
            print(f'### Date of birth: {data[3]}')
            print(f'### Phone number: {data[4]}')
            if data[5] == 'M':
                print(f'### Gender: Male')
            else:
                print(f'### Gender: Female')
            print(f'### Email: {data[6]}')
            break
    print(colored("\nPress any key to continue...", 'cyan'), end = '', flush = True)
    msvcrt.getch()
    clear()
    return
