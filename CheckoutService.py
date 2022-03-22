################################################
#            CheckoutServices.py               #
#          Defines the business logic          #
#                                              #
################################################


import rapyd
import responder
import persistence
import json
from config import *


def generateCheckoutLink(userId, amount):
    print("requesting checkout link for user " + userId + ". Amount: " + str(amount))
    response = rapyd.generate_payment_url(userId, amount, "ISK")
    return response[1]


def processCheckoutResult(json):
    payingUserId = json["whatsapp_number"]
    checkingoutUserId = getCheckingoutUser(payingUserId)
    print("checking out user: " + str(checkingoutUserId))
    successful = json["status"] == "approved"

    if (persistence.getInteractionStatus(checkingoutUserId) == INTERACTION_CHECKOUT_WAITING_FOR_PAYMENT_RESULT):
        if successful:
            responder.sendTextMessage(checkingoutUserId,
                                      "The payment has been accepted. Your food will arrive promptly. Enjoy!")
            if (payingUserId != checkingoutUserId):
                responder.sendTextMessage(payingUserId, "The payment has been accepted.")
            persistence.storeInteractionStatus(checkingoutUserId, INTERACTION_NOT_STARTED)

        else:
            responder.sendTextMessage(payingUserId,
                                      "The payment has been rejected. You can choose a different payment method")
            if (payingUserId != checkingoutUserId):
                responder.sendTextMessage(checkingoutUserId, "The payment has been rejected.")

            responder.sendPaymentSelection(checkingoutUserId)
            persistence.storeInteractionStatus(checkingoutUserId, INTERACTION_CHECKOUT_WAITING_FOR_PAYMENT_MODE)
    else:
        print("Weird... that user was not waiting for a payment...")


def getCheckingoutUser(payingUserId):
    if (persistence.existsDeferredCheckoutFor(payingUserId)):
        return persistence.getDeferredCheckoutToUser(payingUserId)
    else:
        return payingUserId
