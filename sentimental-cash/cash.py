from cs50 import get_float
from math import trunc


def get_cents():
    while True:
        cents = get_float("Change owed: ")
        if cents > 0:
            break
    return cents


def calculate_quarters(cents):
    return trunc(cents / 25)


def calculate_dimes(cents):
    return trunc(cents / 10)


def calculate_nickels(cents):
    return trunc(cents / 5)


def calculate_pennies(cents):
    return trunc(cents / 1)


cents = get_cents()
cents = cents*100  # converting to cents format

quarters = calculate_quarters(cents)  # finding quarters
cents = cents - quarters * 25

dimes = calculate_dimes(cents)  # finding dimes
cents = cents - dimes * 10

nickels = calculate_nickels(cents)  # finding nickels
cents = cents - nickels * 5

pennies = calculate_pennies(cents)  # finding pennies
cents = cents - pennies * 1

coins = quarters + dimes + nickels + pennies
print(coins)