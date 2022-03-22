################################################
#                   menu.py                    #
# Defines menu options offered to the customer.#
#                                              #
################################################

################################################
#                    json                      #
# Standard library methods for processing JSON #
# requests and responses.                      #
#                                              #
################################################

import json


def getMenuStarters():
    response = {"options": [
        {"name": "Chicken Wings", "price": 1895},
        {"name": "Lamb Samosas", "price": 1295},
        {"name": "Onion Rings", "price": 1495}]
    }
    return json.dumps(response)


def getMenuMainCourses():
    response = {"options": [
        {"name": "BaconBurguer", "price": 2590},
        {"name": "Cesar Salad", "price": 2290},
        {"name": "Fish & Chips", "price": 2355}]
    }
    return json.dumps(response)


def getMenuDesserts():
    response = {"options": [
        {"name": "Ice Cream", "price": 1295},
        {"name": "Tiramisú", "price": 1495},
        {"name": "Brownie", "price": 1590}]
    }
    return json.dumps(response)


def getMenuDrinks():
    response = {"options": [
        {"name": "Bottled water", "price": 595},
        {"name": "Coke", "price": 795},
        {"name": "Blood", "price": 19995}]
    }
    return json.dumps(response)
