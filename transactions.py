from tabulate import tabulate
from datetime import datetime, timedelta
from termcolor import colored
import os
import time
import getInput
import msvcrt

clear = lambda: os.system('cls')

def viewTransactions(cursor):# Get the view of transactions.
    clear()
    try:
        cursor.execute('BEGIN;')
        cursor.execute('SELECT * FROM full_transaction')
        cursor.execute('''
            SELECT regnr AS "Registry Number",
                brand AS "Brand",
                model AS "Model",
                firstname AS "First Name",
                lastname AS "Last Name",
                rentdate AS "Rent Date",
                returndate AS "Return Date",
                totalprice AS "Total Price"
            FROM full_transaction
        ''')#Query.(SELECT AS FROM)
        data = cursor.fetchall()
        data_with_rownum = [(i+1,) + row for i, row in enumerate(data)]
        headers = [f"\033[1;36m{i[0]}\033[0m" for i in cursor.description]
        print(tabulate(data_with_rownum, headers=headers, tablefmt='fancy_grid', numalign="center", stralign="center"))
        print(colored("\nPress any key to continue...", 'cyan'), end='', flush=True)
        cursor.connection.commit()
    except:
        cursor.connection.rollback()
        print(colored("\n! Error occurred while retrieving transactions. Please try again.\n", 'red'))

    msvcrt.getch()
    clear()
    return


def viewEarnings(cursor):# Get view of earnings.
    clear()
    today = datetime.now().date()
    try:
        cursor.execute("BEGIN;")
        # Get the earnings with different limit time.
        while True:
            userInput = getInput.getInt("1) All time\n2) Last month\n3) Last week\n4) Last day\n0) Back\n\n-- Please enter your choice: ")
            match userInput:
                case 1:
                    cursor.execute('''
                        SELECT SUM(totalprice) AS "Total Earnings"
                        FROM full_transaction
                    ''')# Query.(SELECT SUM() AS FROM)
                    data = cursor.fetchone()
                    print(colored(f"\nTotal Earnings: {data[0]} EUR\n", 'green'))
                case 2:
                    last_month = today.replace(month = today.month - 1)
                    cursor.execute('''
                        SELECT SUM(totalprice) AS "Total Earnings"
                        FROM full_transaction
                        WHERE returndate >= %s
                    ''', (last_month,))# Query.(SELECT SUM() AS FROM WHERE)
                    data = cursor.fetchone()
                    print(colored(f"\nTotal Earnings: {data[0]} EUR\n", 'green'))
                case 3:
                    last_week = today - timedelta(days = 7)
                    cursor.execute('''
                        SELECT SUM(totalprice) AS "Total Earnings"
                        FROM full_transaction
                        WHERE returndate >= %s
                    ''', (last_week,))#Query.(SELECT SUM() AS FROM  WHERE)
                    data = cursor.fetchone()
                    print(colored(f"\nTotal Earnings: {data[0]} EUR\n", 'green'))
                case 4:
                    cursor.execute('''
                        SELECT SUM(totalprice) AS "Total Earnings"
                        FROM full_transaction
                        WHERE returndate >= %s
                    ''', (today,))#Query.(SELECT SUM() AS FROM WHERE)
                    data = cursor.fetchone()
                    print(colored(f"\nTotal Earnings: {data[0]} EUR\n", 'green'))
                case 0:
                    cursor.connection.commit()
                    return
                case _:
                    print(colored("\n! Invalid input, please try again.\n", 'red'))
        
    except:
        cursor.connection.rollback()
        print(colored("\n! An error occurred, transaction rolled back.\n", 'red'))
    finally:
        clear()
