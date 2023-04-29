from tabulate import tabulate
from termcolor import colored
import os
import getInput
import msvcrt

clear = lambda: os.system('cls')

def stats(cursor):# Check the data situation.
    clear()
    while True:
        print("1) Show number of cars\n2) Show number of customers\n3) Show customers by gender\n4) Show cars rented by each customer\n5) Show average price per day by car brand\n6) Show customers by age group\n0) Back")
        userInput = getInput.getInt("\n-- Your choice: ")
        match userInput:
            case 1:
                totalCars(cursor)
            case 2:
                totalCustomers(cursor)
            case 3:
                customersByGender(cursor)
            case 4:
                carsRentedByCustomer(cursor)
            case 5:
                rentalPriceByBrand(cursor)
            case 6:
                customersByAgeRange(cursor)
            case 0:
                break
            case _:
                print(colored('\n! Invalid input, please try again.\n', 'red'))
        clear()
    clear()
    return

def totalCustomers(cursor):# Check the number of customers.
    clear()
    cursor.execute('''
        SELECT COUNT(*) AS "Total number of customers"
        FROM customers;
    ''')#Query.(SELECT COUNT() AS FROM)
    result = cursor.fetchone()

    # Format result as list of lists
    table = []
    headers = ["Total number of customers"]
    table.append([result[0]])

    # Display results using tabulate
    print(tabulate(table, headers=headers, tablefmt='fancy_grid'))
    print(colored("\nPress any key to continue...", 'cyan'), end = '', flush = True)
    msvcrt.getch()
    clear()
    return

def totalCars(cursor):
    clear()
    cursor.execute('''
        SELECT COUNT(*) AS "Total number of cars"
        FROM cars;
    ''')
    result = cursor.fetchone()

    # Format result as list of lists
    table = []
    headers = ["Total number of cars"]
    table.append([result[0]])

    # Display results using tabulate
    print(tabulate(table, headers=headers, tablefmt='fancy_grid'))
    print(colored("\nPress any key to continue...", 'cyan'), end = '', flush = True)
    msvcrt.getch()
    clear()
    return

def carsRentedByCustomer(cursor):# Check the situation of cars rented by customers.
    clear()
    cursor.execute('''
        SELECT customers.customerid, customers.firstname, customers.lastname, COUNT(rentdetails.regnr) AS "Number of cars rented" 
        FROM customers 
        LEFT JOIN rentdetails ON customers.customerid = rentdetails.customerid
        WHERE rentdetails.regnr IS NOT NULL
        GROUP BY customers.customerid, customers.firstname, customers.lastname
        ORDER BY "Number of cars rented" DESC;
    ''')# Query.(SELECT FROM LEFT JOIN WHERE GROUP BY ORDER BY DESC)
    results = cursor.fetchall()

    # Format results as list of lists
    table = []
    headers = ["Customer ID", "First Name", "Last Name", "Number of Cars Rented"]
    for row in results:
        table.append([row[0], row[1], row[2], row[3]])

    # Display results using tabulate
    print(tabulate(table, headers=headers, tablefmt='fancy_grid'))
    print(colored("\nPress any key to continue...", 'cyan'), end='', flush=True)
    msvcrt.getch()
    clear()
    return

def customersByGender(cursor):# Check the number of customers with gender.
    clear()
    cursor.execute('''
        SELECT gender, COUNT(*) AS "Number of customers" 
        FROM customers
        WHERE gender IS NOT NULL
        GROUP BY gender
        ORDER BY gender DESC;
    ''')#Query.(SELECT FROM WHERE IS NOT NULL GROUP BY ORDER BY)
    results = cursor.fetchall()

    # Format results as list of lists
    table = []
    headers = ["Gender", "Count"]
    for row in results:
        table.append([row[0], row[1]])

    # Display results using tabulate
    print(tabulate(table, headers=headers, tablefmt='fancy_grid'))
    print(colored("\nPress any key to continue...", 'cyan'), end = '', flush = True)
    msvcrt.getch()
    clear()
    return

def rentalPriceByBrand(cursor):# Check the car's average rental price with brand.
    clear()
    cursor.execute('''
        SELECT cars.brand, AVG(cars.priceperday) AS "Average rental price per day"
        FROM cars
        GROUP BY cars.brand
        ORDER BY cars.brand ASC;
    ''')# Query.(SELECT FROM GROUP BY ORDER BY)
    results = cursor.fetchall()

    # Format results as list of lists
    table = []
    headers = ["Car Brand", "Average Rental Price"]
    for row in results:
        table.append([row[0], round(row[1], 2)])

    # Display results using tabulate
    print(tabulate(table, headers=headers, tablefmt='fancy_grid'))
    print(colored("\nPress any key to continue...", 'cyan'), end='', flush=True)
    msvcrt.getch()
    clear()
    return

def customersByAgeRange(cursor):#Check the number of customers with the age period.
    clear()
    cursor.execute('''
        SELECT 
            CASE 
                WHEN EXTRACT(YEAR FROM age(CURRENT_DATE, dob)) BETWEEN 20 AND 25 THEN '20-25'
                WHEN EXTRACT(YEAR FROM age(CURRENT_DATE, dob)) BETWEEN 26 AND 35 THEN '26-35'
                WHEN EXTRACT(YEAR FROM age(CURRENT_DATE, dob)) BETWEEN 36 AND 45 THEN '36-45'
                WHEN EXTRACT(YEAR FROM age(CURRENT_DATE, dob)) BETWEEN 46 AND 55 THEN '46-55'
                ELSE '56+' 
            END AS "Age Range", 
            COUNT(*) AS "Number of customers"
        FROM customers
        WHERE dob IS NOT NULL
        GROUP BY "Age Range"
        ORDER BY MIN(EXTRACT(YEAR FROM age(CURRENT_DATE, dob))) ASC;
    ''')#Query. ( SELECT CASE WHEN EXTRACT FROM BETWEEN AND THEN END AS COUNT() FROM WHERE GROUP BY ORDER BY MIN() EXTRACT ASC)
    results = cursor.fetchall()

    # Format results as list of lists
    table = []
    headers = ["Age Range", "Number of Customers"]
    for row in results:
        table.append([row[0], row[1]])

    # Display results using tabulate
    print(tabulate(table, headers=headers, tablefmt='fancy_grid'))
    print(colored("\nPress any key to continue...", 'cyan'), end = '', flush = True)
    msvcrt.getch()
    clear()
    return
