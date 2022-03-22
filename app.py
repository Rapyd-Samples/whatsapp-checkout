import os
import hjson
from flask import Flask, request, jsonify
from rejson import Client, Path
from flask import jsonify
import requests

redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_pass = os.environ.get('REDIS_PASS')
bot_endpoint = os.environ.get('REDIS_PORT')

rj = Client(host='localhost' if not redis_host else redis_host,
            port=6379 if not redis_port else int(redis_port),
            decode_responses=True, password='somekindofapassword' if not redis_pass else redis_pass)

app = Flask(__name__)


@app.route("/", methods=['POST'])
def listen_for_hook():
    req_json = hjson.loads(request.data)

    hook_id = req_json.get('id')
    hook_type = req_json.get('type')
    rj.jsonset(f"webhook:{ hook_type if hook_type else 'UNKNOWN' }:{hook_id if hook_id else '0000'}", Path.rootPath(), req_json)
    hook_data = req_json.get('data')

    meta_data = hook_data.get('metadata') if hook_data else {}
    if meta_data:
        pay_session = meta_data.get('pay_session') if meta_data else '0000'

    whatsapp_number = (hook_data.get('merchant_reference_id') if hook_data else '0000').split('-')[0]

    if hook_data.get('status') and hook_data['status'] == 'CLO':
        requests.post(url='https://56f72bab060a.ngrok.io/rapyd-webhook' if not bot_endpoint else bot_endpoint, json={
            'paysession_id': pay_session if pay_session else '0000',
            'whatsapp_number': whatsapp_number,
            'status': 'rejected' if hook_type not in ['PAYMENT_COMPLETED', 'PAYMENT_SUCCEEDED'] else 'approved'
        })

    return jsonify(success=True)


@app.route('/<redis_id>', methods=['GET'])
def get_json(redis_id):
    return jsonify(rj.jsonget(redis_id))
