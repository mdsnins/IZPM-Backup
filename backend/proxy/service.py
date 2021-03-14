import json
import redis

from time import time
from os import getenv
from random import sample, randrange
from base64 import b64encode
from mitmproxy import http

NAME = ['은비', '쿠라', '혜원', '예나', '채연', '채원', '민주', '나코', '토미', '유리', '유진', '원영']
REDIS_HOST = getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(getenv('REDIS_PORT', '6379'))

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)

# Serialize & Convert dictionary to base64 string 
def serialize_dict(d):
    return b64encode(json.dumps(d))

# Generate redis user key
def gen_key():
    rd = redis.Redis(connection_pool=pool)
    while True:
        rnum = radnrange(1000, 10000)
        [r1, r2] = sample(NAME, 2)
        rkey = '{}{}{}'.format(r1, r2, rnum)
        if rd.get(rkey) == None:
            return rkey

# Set data with respect to user key in redis server, and returns ser pin code
def reg_data(key, data):
    pin = '{:04d}'.format(randrange(0, 10000))
    rd = redis.Redis(connection_pool=pool)
    rd.set('{}'.format(key), data)
    rd.set('P_{}'.format(key), pin, time() + (60 * 30)) # Expires in 30 minutees
    return pin


def request(flow: http.HTTPFlow) -> None:
    if 'izone-mail.com' in flow.request.pretty_url:
        #TODO: Dump cookie and redis communication here
        pass