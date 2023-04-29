from termcolor import colored
import getInput
import getCars
import userInfo
import transactions
import stats

def greeting(cursor, title, userid):# Greeting with customers and staff.
    if title == "Customer":
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [userid])#Query.(SELECT FROM WHERE)
        data = cursor.fetchone()
        print(colored(f'### Welcome {data[1]} {data[2]}\n', 'green'))
        customerMenu(cursor, title, userid)
    else:
        cursor.execute("SELECT * FROM staff WHERE staffid = %s", [userid])# Query, (SELECT FROM WHERE)
        data = cursor.fetchone()
        print(colored(f'### Welcome {data[1]} {data[2]}\n', 'green'))
        staffMenu(cursor, title, userid)

def customerMenu(cursor, title, userid):# Customer menu.
    while True:
        print("1) list all cars\n2) Rent a car\n3) Return a car\n4) Change your information\n0) Exit")
        userInput = getInput.getInt("\n-- Your choice: ")
        match userInput:
            case 1:
                getCars.getAllCars(cursor)
            case 2:
                getCars.rentCar(cursor, userid)
            case 3:
                getCars.returnCar(cursor, userid)
            case 4:
                userInfo.userChange(cursor, userid, title)
            case 0:
                print(colored('\nThank you for using our system!\nHope to see you again soon!\n', 'green'))
                cursor.close()
                quit()
            case _:
                print(colored('\n! Invalid input, please try again.\n', 'red'))

def staffMenu(cursor, title, userid):# Staff menu.
    while True:
        print("1) list all cars\n2) Add or update car\n3) Find a customer\n4) View transactions\n5) View earnings\n6) Change your information\n7) See the stats\n0) Exit")
        userInput = getInput.getInt("\n-- Your choice: ")
        match userInput:
            case 1:
                getCars.getAllCars(cursor)
            case 2:
                getCars.addCar(cursor)
            case 3:
                userInfo.findCustomer(cursor)
            case 4:
                transactions.viewTransactions(cursor)
            case 5:
                transactions.viewEarnings(cursor)
            case 6:
                userInfo.userChange(cursor, userid, title)
            case 7:
                stats.stats(cursor)
            case 0:
                print(colored('\nThank you for using our system!\nHope to see you again soon!\n', 'green'))
                cursor.close()
                quit()
            case _:
                print(colored('\n! Invalid input, please try again.\n', 'red'))
