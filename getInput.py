from datetime import datetime
import re
from termcolor import colored
import getpass

def getInt(prompt):# Get integer.
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(colored("\n! That's not an integer. Try again.\n", 'red'))

def getDate(prompt):#Get the restricted date of birth format.
    while True:
        try:
            return datetime.strptime(input(prompt), '%Y-%m-%d')
        except ValueError:
            print(colored("\n! Wrong data format, should be YYYY-MM-DD. Try again.\n", 'red'))

def getStringLength(n, prompt):# Get the restricted length string.
    while True:
        userInput = input(prompt)
        if len(userInput) == n:
            return userInput
        else:
            print(colored(f"\n! Input must be of length {n}. Try again.\n", 'red'))

def getStringRange(n, m, prompt):# Get the restricted range string format,
    while True:
        userInput = input(prompt)
        if n <= len(userInput) <= m:
            return userInput
        else:
            print(colored(f"\n! Input must be between {n} and {m} characters long. Try again.\n", 'red'))

def getEmail(prompt):# Get the restricted format of email.
    while True:
        userInput = input(prompt)
        if re.match(r"[^@]+@[^@]+\.[^@]+", userInput):
            return userInput
        else:
            print(colored(f"\n! Invalid email address. Try again.\n", 'red'))

def getGender(prompt): # Get the gender in restricted gender format.
    while True:
        userInput = input(prompt)
        if userInput in ['M', 'F']:
            return userInput
        else:
            print(colored(f"\n! Gender must be either M or F. Try again.\n", 'red'))

def getPass(prompt): # Get the restricted password format.
    while True:
        userInput = getpass.getpass(prompt)
        if len(userInput) > 15:
            print(colored(f"\n! Password must be less than 15 characters long. Try again.\n", 'red'))
        elif len(userInput) < 8:
            print(colored(f"\n! Password must be longer than 8 characters. Try again.\n", 'red'))
        else:
            return userInput
