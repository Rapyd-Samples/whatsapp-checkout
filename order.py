################################################
#                  order.py                    #
#          Defines the business logic          #
#                                              #
################################################


import responder
from menu import *
from config import *
from persistence import *


def getOrderSelected(userId):
    order = getOrderSelection(userId)
    aslist = list(order)

    response = {"selection": [
        {"name": json.loads(getMenuStarters())["options"][int(aslist[0])]["name"],
         "price": json.loads(getMenuStarters())["options"][int(aslist[0])]["price"]},
        {"name": json.loads(getMenuMainCourses())["options"][int(aslist[1])]["name"],
         "price": json.loads(getMenuMainCourses())["options"][int(aslist[1])]["price"]},
        {"name": json.loads(getMenuDesserts())["options"][int(aslist[2])]["name"],
         "price": json.loads(getMenuDesserts())["options"][int(aslist[2])]["price"]},
        {"name": json.loads(getMenuDrinks())["options"][int(aslist[3])]["name"],
         "price": json.loads(getMenuDrinks())["options"][int(aslist[3])]["price"]},
    ]}
    return json.dumps(response)


def getOrderTotal(userId):
    print("getting total amount")
    total = 0
    jsonItems = json.loads(getOrderSelected(userId))["selection"]
    for item in jsonItems:
        print(item)
        total += int(item["price"])

    return total


def processOrderSelection(userId, selectionId):
    interactionstatus = getInteractionStatus(userId)

    if (interactionstatus == INTERACTION_WAITING_FOR_STARTER_SELECTION):
        storeOrderSelection(userId, 0, selectionId[-1])
        responder.sendTextMessage(userId, "Nice selection! Let's continue with the order.")
        responder.sendPlateSelection(userId, "What would you like for your main course?",
                                      "Made with love and the best ingredients.",
                                      getMenuMainCourses())
        storeInteractionStatus(userId, INTERACTION_WAITING_FOR_MAINCOURSE_SELECTION)
        return

    if (interactionstatus == INTERACTION_WAITING_FOR_MAINCOURSE_SELECTION):
        storeOrderSelection(userId, 1, selectionId[-1])
        responder.sendTextMessage(userId, "That's a good choice. Any room left for dessert?")
        responder.sendPlateSelection(userId, "Choose your dessert:", "Your sweet dreams came true.", getMenuDesserts())
        storeInteractionStatus(userId, INTERACTION_WAITING_FOR_DESSERT_SELECTION)
        return

    if (interactionstatus == INTERACTION_WAITING_FOR_DESSERT_SELECTION):
        storeOrderSelection(userId, 2, selectionId[-1])
        responder.sendTextMessage(userId, "Awesome! What do you want to drink?")
        responder.sendPlateSelection(userId, "Choose your beverage:", "Liquids are cool. Especially with ice.",
                                      getMenuDrinks())
        storeInteractionStatus(userId, INTERACTION_WAITING_FOR_DRINK_SELECTION)
        return

    if (interactionstatus == INTERACTION_WAITING_FOR_DRINK_SELECTION):
        storeOrderSelection(userId, 3, selectionId[-1])
        responder.sendTextMessage(userId, "Your order is complete.")
        responder.showOrder(userId)
        responder.sendYesNo(userId, "Are you ready to proceed to checkout?")
        storeInteractionStatus(userId, INTERACTION_READY_FOR_CHECKOUT)
        return
