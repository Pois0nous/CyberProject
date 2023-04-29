from tabulate import tabulate
from datetime import datetime
from termcolor import colored
import os
import getInput
import msvcrt

clear = lambda: os.system('cls')

def getAllCars(cursor):# Get the information of cars.
    clear()
    cursor.execute('SELECT regnr AS "Registry Number", brand AS "Brand", model AS "Model", priceperday AS "Price Per Day" FROM cars')# Query.(SELECT FROM)
    data = cursor.fetchall()
    data_with_rownum = [(i+1,) + row for i, row in enumerate(data)]
    headers = [f"\033[1;36m{i[0]}\033[0m" for i in cursor.description]
    print(tabulate(data_with_rownum, headers = headers, tablefmt='fancy_grid', numalign="center", stralign="center"))
    print(colored("\nPress any key to continue...", 'cyan'), end = '', flush = True)
    msvcrt.getch()
    clear()
    return

def rentCar(cursor, userid):# Customer rent a car.
    clear()
    isquit = False
    today = datetime.now().date()
    print("\nHere are all the cars available for rent:")
    #List the information of the cars and show the statue of the cars.
    try:
        cursor.execute("BEGIN")
        cursor.execute('''
            SELECT cars.regnr AS "Registry Number", 
                cars.brand AS "Brand", 
                cars.model AS "Model", 
                cars.priceperday AS "Price Per Day",
                CASE WHEN rentdetails.regnr IS NOT NULL THEN '\033[1;31mRented\033[0m' ELSE '\033[1;32mAvailable\033[0m' END AS "Status"
            FROM cars 
            LEFT JOIN rentdetails 
            ON cars.regnr = rentdetails.regnr
        ''')#Query.(SELECT FROM LEFT JOIN ON)
        data = cursor.fetchall()
        data_with_rownum = [(i+1,) + row for i, row in enumerate(data)]
        headers = [f"\033[1;36m{i[0]}\033[0m" for i in cursor.description]
        print(tabulate(data_with_rownum, headers = headers, tablefmt='fancy_grid', numalign="center", stralign="center"))

        while True:#After the customer chooses to inform whether the car can be rented.
            indexNum = getInput.getInt("\n-- Please enter the index number of the car you want to rent (0 to back): ")
            if indexNum == 0:
                isquit = True
                break
            elif indexNum > len(data_with_rownum):
                print(colored('\n! Invalid input, please try again.\n', 'red'))
            elif data_with_rownum[indexNum-1][5] == '\033[1;31mRented\033[0m':
                print(colored('\n! This car is already rented, please try again.\n', 'red'))
            else:
                regnr = data_with_rownum[indexNum-1][1]
                print("\nYou have selected the car with registry number: ", regnr)
                break
        
        if isquit:
            clear()
            return
        #Display rental vehicle information and give customer a notice.
        cursor.execute("""
            SELECT c.brand, c.model, c.priceperday, string_agg(f.featurename, ', ') as features
            FROM cars c
            JOIN carfeatures cf ON c.regnr = cf.regnr
            JOIN features f ON cf.featureid = f.featureid
            WHERE c.regnr = %s
            GROUP BY c.brand, c.model, c.priceperday;
        """, (regnr,))#Query.(SELECT FROM WHERE JOIN GROUP BY)
        data = cursor.fetchall()
        print(f"\nThe car you selected is a {data[0][0]} {data[0][1]}\nIt will cost {data[0][2]} Euros each day\nAnd it has the following features:\n{data[0][3]}")
        # let customer confirm
        userInput = input("\n-- Do you want to rent this car? (y/n): ").lower()
        if userInput == "y":
            cursor.execute("""
            INSERT INTO rentdetails (regnr, customerid, rentdate)
            VALUES (%s, %s, %s);
            """, (regnr, userid, today))#Query.(INSERT INTO VALUES)
            cursor.connection.commit()
            print(colored("\nYou have successfully rented the car!\n", 'green'))
            print(colored("\nPress any key to continue...", 'cyan'), end = '', flush = True)
            msvcrt.getch()
            clear()
        else:
            print(colored("\n! You have cancelled the rent.\n", 'red'))
            print(colored("\nPress any key to continue...", 'cyan'), end = '', flush = True)
            msvcrt.getch()
            clear()
    except:
        cursor.connection.rollback()
        raise
    finally:
        return


def returnCar(cursor, userid):#Customer return a car.
    clear()
    isquit = False
    today = datetime.now().date()
    try:
        cursor.execute("BEGIN;")#Check if the user has a car that needs to be returned. 
        
        cursor.execute("""
            SELECT cars.regnr AS "Registry Number", cars.brand AS "Brand", cars.model AS "Model",
                cars.priceperday AS "Price Per Day", rentdetails.rentdate AS "Rent Date"
            FROM rentdetails
            INNER JOIN cars ON rentdetails.regnr = cars.regnr
            WHERE rentdetails.customerid = %s;
        """, (userid,))#Query.(SELECT FROM INNER JOIN WHERE)
        data = cursor.fetchall()
        if len(data) == 0:
            print(colored("\nYou don't have any cars to return", 'red'))
            print(colored("\nPress any key to continue...", 'cyan'), end = '', flush = True)
            msvcrt.getch()
            clear()
            return
        else:
            print("\nHere are all the cars you have rented:")
            data_with_rownum = [(i+1,) + row for i, row in enumerate(data)]
            headers = [f"\033[1;36m{i[0]}\033[0m" for i in cursor.description]
            print(tabulate(data_with_rownum, headers=headers, tablefmt='fancy_grid', numalign="center", stralign="center"))

            while True:
                indexNum = getInput.getInt("\n-- Please enter the index number of the car you want to return (0 to back): ")
                if indexNum == 0:
                    isquit = True
                    break
                elif indexNum > len(data_with_rownum):
                    print(colored('\n! Invalid input, please try again.\n', 'red'))
                elif indexNum < 0:
                    print(colored('\n! Invalid input, please try again.\n', 'red'))
                else:
                    regnr = data_with_rownum[indexNum-1][1]
                    print("\nYou have selected the car with registry number: ", regnr)
                    break

            if isquit:
                clear()
                return
            
            # Get the rent date.
            cursor.execute("SELECT rentdate FROM rentdetails WHERE regnr = %s AND customerid = %s;", (regnr, userid))#Query.(SELECT FROM WHERE)
            rental_details = cursor.fetchone()
            rentdate = rental_details[0]
            # Get the price per day of car.
            cursor.execute("SELECT priceperday FROM cars WHERE regnr = %s;", (regnr,))#Query.(SELECT FROM WHERE)
            rental_details = cursor.fetchone()
            priceperday = rental_details[0]
            # Calculate the rental period.
            rental_period = (today - rentdate).days + 1
            if rental_period < 30:# Get the total price.
                total_price = rental_period * priceperday
            else:
                print(colored("\nYou have rented the car for more than 30 days, you will get a 200 Euros fine!", 'yellow'))
                total_price = (rental_period * priceperday) + 200
            # Record the transaction.
            cursor.execute("INSERT INTO transactions (regnr, customerid, rentdate, returndate, priceperday, totalprice) VALUES (%s, %s, %s, %s, %s, %s);",
                    (regnr, userid, rentdate, today, priceperday, total_price))# Query.(INSERT INTO VALUES)
            # Delete the record from rentdetails table.
            cursor.execute("DELETE FROM rentdetails WHERE regnr = %s AND customerid = %s;",
                    (regnr, userid))

            cursor.connection.commit()
            print(colored(f"\nYou have successfully returned the car!\nYou have rented the car for {rental_period} days\nThe total price is {total_price} Euros\n", 'green'))
            print(colored("\nPress any key to continue...", 'cyan'), end='', flush=True)
            msvcrt.getch()
            clear()
    except:
        cursor.connection.rollback()
        raise


def addCar(cursor):# Staff add a car.
    clear()
    try:
        cursor.execute("BEGIN;")
        regnr = getInput.getStringLength(7, "\n-- Registry Number: ")
        cursor.execute("SELECT regnr FROM cars WHERE regnr = %s", (regnr,))#Query.(SELECT FROM WHERE)
        existing_car = cursor.fetchone()
        if existing_car is not None:
            print(colored("\n! This registry number already exists.\n", 'red'))
            while True:# Give the menu of delete or update the car.
                action = input("Do you want to (D)elete or (U)pdate the car? ")
                if action.upper() == "D":
                    cursor.execute("DELETE FROM cars WHERE regnr = %s", (regnr,))#Query.(DELETE FROM WHERE)
                    print(colored("\nThe car has been deleted.\n", 'green'))
                    cursor.connection.commit()
                    print(colored("\nPress any key to continue...", 'cyan'), end='', flush=True)
                    msvcrt.getch()
                    clear()
                    break
                elif action.upper() == "U":
                    brand = input("-- Brand: ")
                    model = input("-- Model: ")
                    priceperday = getInput.getInt("-- How much to charge for each day (Only whole numbers): ")
                    cursor.execute("UPDATE cars SET brand = %s, model = %s, priceperday = %s WHERE regnr = %s", 
                                (brand, model, priceperday, regnr)) #Query.(UPDATE SET WHERE)
                    print(colored("\nThe car has been updated.\n", 'green'))
                    cursor.connection.commit()
                    print(colored("\nPress any key to continue...", 'cyan'), end='', flush=True)
                    msvcrt.getch()
                    clear()
                    break
                else:
                    print(colored("\nPlease enter a valid action.\n", 'red'))
            cursor.connection.rollback()
            return
        brand = input("-- Brand: ")
        model = input("-- Model: ")
        priceperday = getInput.getInt("-- How much to charge for each day (Only whole numbers): ")
        cursor.execute("""
            INSERT INTO cars (regnr, brand, model, priceperday)
            VALUES (%s, %s, %s, %s);
        """, (regnr, brand, model, priceperday))# Query.(INSERT INTO VALUES)
        cursor.execute("SELECT regnr FROM cars WHERE regnr = %s", (regnr,))
        car = cursor.fetchone()
        features = input("-- Features (separated by commas): ")
        feature_list = [feature.strip() for feature in features.split(",")]
        for feature_name in feature_list:
            cursor.execute("SELECT featureid FROM features WHERE featurename = %s", (feature_name,))#Query.(SELECT FROM WHERE)
            feature = cursor.fetchone()
            if feature is None:
                cursor.execute("INSERT INTO features (featurename) VALUES (%s)", (feature_name,))#Query.(INSERT INTO VALUES)
                cursor.execute("SELECT featureid FROM features WHERE featurename = %s", (feature_name,))#Query.(SELECT FROM WHERE)
                feature = cursor.fetchone()
            cursor.execute("INSERT INTO carfeatures (regnr, featureid) VALUES (%s, %s)", (car[0], feature[0]))#Query.(INSERT INTO VALUES)
        cursor.connection.commit()
        print(colored("\nYou have successfully added a new car!\n", 'green'))
    except:
        cursor.connection.rollback()
        print(colored("\nAn error occurred, the transaction has been rolled back.\n", 'red'))
        raise
    print(colored("\nPress any key to continue...", 'cyan'), end = '', flush = True)
    msvcrt.getch()
    clear()
    return
