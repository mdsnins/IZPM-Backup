#-*- coding: utf-8 -*-
import json
import redis

from time import time
from os import getenv
from random import sample, randrange
from base64 import b64encode
from mitmproxy import http

NAME        = ['은비', '쿠라', '혜원', '예나', '채연', '채원', '민주', '나코', '토미', '유리', '유진', '원영']
REDIS_HOST  = getenv('REDIS_HOST', 'localhost')
REDIS_PORT  = int(getenv('REDIS_PORT', '6379'))
WEB_HOST    = getenv('WEB_HOST', 'http://localhost/')

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)

# Serialize & Convert dictionary to base64 string 
def serialize_dict(d):
    return b64encode(json.dumps(d).encode())

# Generate redis user key
def gen_key():
    rd = redis.Redis(connection_pool=pool)
    while True:
        rnum = randrange(1000, 10000)
        [r1, r2] = sample(NAME, 2)
        rkey = '{}{}{}'.format(r1, r2, rnum)
        if rd.get(rkey) == None:
            return rkey

# Set data with respect to user key in redis server, and returns ser pin code
def reg_data(key, data):
    pin = '{:04d}'.format(randrange(0, 10000))
    rd = redis.Redis(connection_pool=pool)
    rd.set('{}'.format(key), data)
    rd.set('P_{}'.format(key), pin, int(time()) + (60 * 30)) # Expires in 30 minutees
    return pin


def request(flow: http.HTTPFlow) -> None:
    if 'app-web.izone-mail.com/mail/m' in flow.request.pretty_url:
        #TODO: Dump cookie and redis communication here
        hdr = dict(flow.request.headers)
        hdr.pop('If-None-Match', None)
        hdr.pop('if-none-match', None) #add lowercase
        hdr["terms-version"] = "5" #Add Terms-Version 
        hdr_str = serialize_dict(hdr)

        key = gen_key()
        pin = reg_data(key, hdr_str)

        flow.response = http.HTTPResponse.make(
            200,
            b'''<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, height=device-height, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no">
    </head>
    <body>
        <p>
            <strong>IZPM-Backup</strong>
            <br />
            ''' + \
            '컴퓨터에서 {} 에 접속 후<br /><b>키</b> {} / <b>PIN</b> {} 입력 후 <br />진행 해주세요.'.format(WEB_HOST, key, pin).encode() + \
            b'''</p>
    </body>
</html> ''',
            { "Content-Type": "text/html" }
        )