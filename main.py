################################################
#                   main.py                    #
# Handles the interface with the user.         #
# Waits for input and then produces responses. #
#                                              #
################################################

from waparser import *
from checkoutService import *

################################################
#                     flask                    #
# Handles interactions over the Internet.      #
#                                              #
################################################

from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/wa-webhook', methods=['POST'])
def parseWhatsapp():
    parseWhatsappPayload(request.json)
    return Response(status=200)


@app.route('/rapyd-webhook', methods=['POST'])
def respondRapyd():
    print(request.json)
    processCheckoutResult(request.json)
    return Response(status=200)

