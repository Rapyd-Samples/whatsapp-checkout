import json
import random
import string
import hmac
import base64
import hashlib
import time
import requests
from datetime import datetime
from uuid import uuid4 as uuid

secret_key = '{{get-secret-key-from-rapyd-client-portal}}'
access_key = '{{get-access-key-from-rapyd-client-portal}}'
http_method = 'post'
base_url = 'https://sandboxapi.rapyd.net' # This is for testing only. 
                                          # Use https://api.rapyd.net for production.

our_customers = [
    ('John Doe', 'cus_4c3208b339a2c99c16ac71ff6fb5fd60', '14155551234'),
    ('Jane Doe', 'cus_9d8e26822d6dec790d3b152f446fc032', '14155551235'),
    ('Deedee Doe', 'cus_b2f9848bcd71bf604d7b5abf5a13600d', '14155551236'),
    ('Didee Doe', 'cus_bd94c06e97939d14eaee2cb86e8d4a22', '14155551237')
]

# Calculate signature for message header

def generate_salt(length=12):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def get_unix_time(days=0, hours=0, minutes=0, seconds=0):
    return int(time.time())


def update_timestamp_salt_sig(http_method, path, body):
    if path.startswith('http'):
        path = path[path.find(f'/v1'):]
    salt = generate_salt()
    timestamp = get_unix_time()
    to_sign = (http_method, path, salt, str(timestamp), access_key, secret_key, body)
    h = hmac.new(secret_key.encode('utf-8'), ''.join(to_sign).encode('utf-8'), hashlib.sha256)
    signature = base64.urlsafe_b64encode(str.encode(h.hexdigest()))
    return salt, timestamp, signature


def current_sig_headers(salt, timestamp, signature):
    sig_headers = {'access_key': access_key,
                   'salt': salt,
                   'timestamp': str(timestamp),
                   'signature': signature,
                   'idempotency': str(get_unix_time()) + salt}
    return sig_headers


def pre_call(http_method, path, body=None):
    str_body = json.dumps(body, separators=(',', ':'), ensure_ascii=False) if body else ''
    salt, timestamp, signature = update_timestamp_salt_sig(http_method=http_method, path=path, body=str_body)
    return str_body.encode('utf-8'), salt, timestamp, signature


def create_headers(http_method, url, body=None):
    body, salt, timestamp, signature = pre_call(http_method=http_method, path=url, body=body)
    return body, current_sig_headers(salt, timestamp, signature)


def make_request(method, path, body=''):
    body, headers = create_headers(method, base_url + path, body)
    if method == 'get':
        response = requests.get(base_url + path, headers=headers)
    elif method == 'put':
        response = requests.put(base_url + path, data=body, headers=headers)
    elif method == 'delete':
        response = requests.delete(base_url + path, data=body, headers=headers)
    else:
        response = requests.post(base_url + path, data=body, headers=headers)
    if response.status_code != 200:
        print(response.url)
        print(response.content)
        raise TypeError(response, method, base_url + path)
    return json.loads(response.content)


def generate_payment_url(whatsapp_number, amount_value, amount_currency):
    req_body = {
        "amount": amount_value,
        "country": "is",
        "currency": amount_currency,
        "merchant_reference_id": f"{whatsapp_number}-{datetime.now().isoformat(timespec='minutes')}",
        "metadata": {
            "pay_session": str(uuid())
        }
    }

    for name, customer_id, customer_number in our_customers:
        if whatsapp_number == customer_number:
            req_body['customer'] = customer_id

    return (req_body['metadata']['pay_session'],
            make_request(method='post', path='/v1/checkout', body=req_body)['data']['redirect_url'])
