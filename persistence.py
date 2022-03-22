################################################
#              persistence.py                  #
#       Defines the finite state machine.      #
#                                              #
################################################


import redis
from config import *

interactionPrefix = "interaction-"
orderPrefix = "order-"
deferredOrderPrefix = "deferred-"

password = "somekindofpassword"
port = 6379


def getInteractionStatus(userId):
    r = redis.Redis(host='localhost', port=port, db=0, password=password, decode_responses=True)
    if (r.exists(__getinteractiondbkey(userId))):
        return r.get(__getinteractiondbkey(userId))
    else:
        storeInteractionStatus(userId, INTERACTION_NOT_STARTED)
        return INTERACTION_NOT_STARTED


def storeInteractionStatus(userId, status):
    r = redis.Redis(host='localhost', port=port, db=0, password=password, decode_responses=True)
    r.set(__getinteractiondbkey(userId), status)


def deleteInteractionStatus(userId):
    r = redis.Redis(host='localhost', port=port, db=0, password=password, decode_responses=True)
    r.delete(__getinteractiondbkey(userId))


def getOrderSelection(userId):
    r = redis.Redis(host='localhost', port=port, db=0, password=password, decode_responses=True)
    if (r.exists(__getorderkey(userId))):
        return r.get(__getorderkey(userId))
    else:
        storeInteractionStatus(__getorderkey(userId), "----")
        return "----"


def storeOrderSelection(userId, position, selection):
    r = redis.Redis(host='localhost', port=port, db=0, password=password, decode_responses=True)
    currentOrder = getOrderSelection(userId)
    s = list(currentOrder)
    s[position] = selection
    r.set(__getorderkey(userId), "".join(s))


def storeDeferredCheckout(fromUser, toUser):
    print("Stored deferred checkout from " + fromUser + " to " + toUser)
    r = redis.Redis(host='localhost', port=port, db=0, password=password, decode_responses=True)
    r.set(__getdeferredkey(toUser), fromUser)


def getDeferredCheckoutToUser(userId):
    print("userid for deferred key " + str(userId))
    r = redis.Redis(host='localhost', port=port, db=0, password=password, decode_responses=True)
    return r.get(__getdeferredkey(userId))


def deleteDeferredCheckoutToUser(userId):
    r = redis.Redis(host='localhost', port=port, db=0, password=password, decode_responses=True)
    r.delete(__getdeferredkey(userId))


def existsDeferredCheckoutFor(userId):
    r = redis.Redis(host='localhost', port=port, db=0, password=password, decode_responses=True)
    return r.exists(__getdeferredkey(userId))


def deleteAllDeferredCheckouts():
    r = redis.Redis(host='localhost', port=port, db=0, password=password, decode_responses=True)
    r.delete(__getdeferredkey("*"))


def __getinteractiondbkey(userId):
    return interactionPrefix + userId


def __getorderkey(userId):
    return orderPrefix + userId


def __getdeferredkey(userId):
    return deferredOrderPrefix + userId
