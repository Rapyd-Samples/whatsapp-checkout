################################################
#               responder.py                   #
# Defines specific outbound customer messages. #
#                                              #
################################################


from config import *
from order import *
import json
import requests


def sendWelcomeMessage(name, phone):
    payload = json.dumps({
        "recipient_type": "individual",
        "to": phone,
        "type": "text",
        "text": {
            "body": "Hello, " + name + "Welcome to SoftRock Café! I am ready to take your order."
        }
    })
    response = requests.request("POST", WHATSAPP_API_SERVER + "/messages", headers=headers, data=payload)


def sendTextMessage(userId, text):
    payload = json.dumps({
        "recipient_type": "individual",
        "to": userId,
        "type": "text",
        "text": {
            "body": text
        }
    })
    response = requests.request("POST", WHATSAPP_API_SERVER + "/messages", headers=headers, data=payload)


def sendPlateSelection(userId, text, footer, plates):
    jsonresults = json.loads(plates)

    payload = json.dumps({
        "recipient_type": "individual",
        "to": userId,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": text
            },
            "footer": {
                "text": footer
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "plate-id-0",
                            "title": jsonresults["options"][0]["name"] + " - " + str(jsonresults["options"][0]["price"])
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "plate-id-1",
                            "title": jsonresults["options"][1]["name"] + " - " + str(jsonresults["options"][1]["price"])
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "plate-id-2",
                            "title": jsonresults["options"][2]["name"] + " - " + str(jsonresults["options"][2]["price"])
                        }
                    }
                ]
            }
        }
    })
    response = requests.request("POST", WHATSAPP_API_SERVER + "/messages", headers=headers, data=payload)
    print(response.text)


def sendYesNo(userId, text):
    payload = json.dumps({
        "recipient_type": "individual",
        "to": userId,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": text
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "checkout-ready-yes",
                            "title": "Yes"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "checkout-ready-no",
                            "title": "No"
                        }
                    }
                ]
            }
        }
    })
    response = requests.request("POST", WHATSAPP_API_SERVER + "/messages", headers=headers, data=payload)
    print(response.text)


def sendDeferredCheckout(userId, text):
    payload = json.dumps({
        "recipient_type": "individual",
        "to": userId,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": text
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "deferred-id-accepted",
                            "title": "Yes"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "deferred-id-rejected",
                            "title": "No"
                        }
                    }
                ]
            }
        }
    })
    response = requests.request("POST", WHATSAPP_API_SERVER + "/messages", headers=headers, data=payload)
    print(response.text)


def sendPaymentSelection(userId):
    payload = json.dumps({
        "recipient_type": "individual",
        "to": userId,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "Select your payment method"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "payment-id-0",
                            "title": "I pay"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "payment-id-1",
                            "title": "Ask a friend"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "payment-id-2",
                            "title": "Split with friends"
                        }
                    }
                ]
            }
        }
    })
    response = requests.request("POST", WHATSAPP_API_SERVER + "/messages", headers=headers, data=payload)
    print(response.text)



def showOrder(userId):
    jsonOrder = json.loads(getOrderSelected(userId))
    total = 0
    for item in jsonOrder['selection']:
        responder.sendTextMessage(userId, item["name"] + " - " + str(item["price"]))
        total += item["price"]

    responder.sendTextMessage(userId, "Total: " + str(total))

