################################################
#                waparser.py                   #
#       Reads inbound customer messages.       #
#                                              #
################################################

from config import *
from responder import *
from menu import *
from order import *
from persistence import *
import checkoutService


def parseWhatsappPayload(waPayload):
    if ("messages" in waPayload):
        userId = waPayload["contacts"][0]["wa_id"]
        message = waPayload["messages"][0]
        conversationStatus = getInteractionStatus(userId)

        if "contacts" in message:
            if (getInteractionStatus(userId)==INTERACTION_CHECKOUT_WAITING_FOR_CONTACT_INFO):
                print("A contact was shared")
                print(message["contacts"][0]["name"]["formatted_name"])
                if ("wa_id" in message["contacts"][0]["phones"][0]):
                    deferredTo = message["contacts"][0]["phones"][0]["wa_id"]
                    print("Checkout deferred to" + deferredTo)
                    storeDeferredCheckout(userId, deferredTo)
                    responder.sendDeferredCheckout(deferredTo, "Your friend is asking you to pay an order for " + str(getOrderTotal(userId)) + ". Do you accept?")
                    storeInteractionStatus(userId, INTERACTION_CHECKOUT_WAITING_FOR_CONTACT_RESPONSE)
                    storeInteractionStatus(deferredTo, INTERACTION_CHECKOUT_DEFERRED_PAYMENT_REQUESTED)
                    sendTextMessage(userId, "I have contacted your friend and I am waiting for an answer.")
                else:
                    responder.sendTextMessage(userId, "That contact is not in WhatsApp.")

            return

        if ("interactive" in message):
            buttonId = message["interactive"]["button_reply"]["id"]

            if buttonId.startswith("plate-"):
                processOrderSelection(userId, message["interactive"]["button_reply"]["id"])

            if buttonId == "checkout-ready-yes":
                print("order confirmed")
                responder.sendPaymentSelection(userId)
                storeInteractionStatus(userId, INTERACTION_CHECKOUT_WAITING_FOR_PAYMENT_MODE)

            if buttonId == "payment-id-0" and getInteractionStatus(
                    userId) == INTERACTION_CHECKOUT_WAITING_FOR_PAYMENT_MODE:
                print("user will pay")
                responder.sendTextMessage(userId, "Visit this page to finish the process: " + checkoutService.generateCheckoutLink(userId, getOrderTotal(userId)))
                storeInteractionStatus(userId, INTERACTION_CHECKOUT_WAITING_FOR_PAYMENT_RESULT)

            if buttonId == "payment-id-1" and getInteractionStatus(
                    userId) == INTERACTION_CHECKOUT_WAITING_FOR_PAYMENT_MODE:
                print("another person will pay")
                responder.sendTextMessage(userId, "Sure. Use the paperclip button below to send the contact information of the person that will pay the order. I will start a chat with that person to confirm the transaction.")
                storeInteractionStatus(userId, INTERACTION_CHECKOUT_WAITING_FOR_CONTACT_INFO)

            if buttonId == "deferred-id-accepted" and getInteractionStatus(userId) == INTERACTION_CHECKOUT_DEFERRED_PAYMENT_REQUESTED:
                requestingUserId = getDeferredCheckoutToUser(userId)
                print("deferred checkout from user " + requestingUserId + "accepted")
                responder.sendTextMessage(userId, "I will let your friend know that you agreed to pay.")
                responder.sendTextMessage(requestingUserId, "Your friend has agreed to pay. I am waiting for the transaction to be confirmed.")
                responder.sendTextMessage(userId, "Visit this page to finish the process: " + checkoutService.generateCheckoutLink(userId, getOrderTotal(requestingUserId)))
                storeInteractionStatus(userId, INTERACTION_CHECKOUT_WAITING_FOR_PAYMENT_RESULT)
                storeInteractionStatus(requestingUserId, INTERACTION_CHECKOUT_WAITING_FOR_PAYMENT_RESULT)


            if buttonId == "deferred-id-rejected" and getInteractionStatus(userId) == INTERACTION_CHECKOUT_DEFERRED_PAYMENT_REQUESTED:
                requestingUserId = getDeferredCheckoutToUser(userId)
                print("deferred checkout from user " + requestingUserId + " rejected")
                responder.sendTextMessage(userId, "I will let your friend know that you declined to pay.")
                responder.sendTextMessage(requestingUserId, "Your friend has declined to pay. You can select another contact.")
                storeInteractionStatus(userId, INTERACTION_CHECKOUT_WAITING_FOR_CONTACT_INFO)

            return


        else:
            print("waparser - parseWhatsappPayload:")
            print(waPayload)
            messageBody = waPayload["messages"][0]["text"]["body"]

            if (messageBody.lower() == "restart"):
                deleteInteractionStatus(userId)
                deleteAllDeferredCheckouts()
                sendTextMessage(userId, "REDIS key deleted")
                return

            if (messageBody.lower() == "debug"):
                sendTextMessage(userId, str(getInteractionStatus(userId)))
                sendTextMessage(userId, str(getOrderSelection(userId)))
                return

            if (messageBody.lower() == "help"):
                sendTextMessage(userId, "restart - Resets the conversation. Say something to start again.")
                sendTextMessage(userId, "debug - Displays current conversation status and order string")
                return

            if (messageBody.lower() == "defer test"):
                return
                storeOrderSelection(userId, 0, 3)
                storeOrderSelection(userId, 1, 2)
                storeOrderSelection(userId, 2, 1)
                storeOrderSelection(userId, 3, 0)
                storeInteractionStatus(INTERACTION_CHECKOUT_WAITING_FOR_CONTACT_INFO)
                sendTextMessage(userId, "Choose contact to test defer to")
                return

            if (conversationStatus == INTERACTION_NOT_STARTED or messageBody.lower() == "order"):
                sendWelcomeMessage(waPayload["contacts"][0]["profile"]["name"], waPayload["contacts"][0]["wa_id"])
                sendPlatesSelection(userId, "Choose your starter:", "Yummy selection of appetizers", getMenuStarters())
                conversationStatus = INTERACTION_WAITING_FOR_STARTER_SELECTION
                storeInteractionStatus(userId, conversationStatus)
