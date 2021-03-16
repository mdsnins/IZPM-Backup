#-*- coding: utf-8 -*-
import redis
import json
import requests

from os import getenv
from base64 import b64decode
from flask import Flask, render_template, request, Response, send_file

REDIS_HOST  = getenv('REDIS_HOST', 'localhost')
REDIS_PORT  = int(getenv('REDIS_POST', '6379'))
RCP_KEY     = getenv('RECAPTCHA_KEY', '')
RCP_SECRET  = getenv('RECAPTCHA_SECRET', '')

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)

app = Flask(__name__, template_folder='page')

def query_data(key, pin):
    rd = redis.Redis(connection_pool = pool)
    r_pin = rd.get('P_{}'.format(key)).decode()
    if r_pin == None or r_pin != pin:
        return None
    
    r_data = rd.get(key).decode()
    if r_data == None:
        return None

    rd.delete('P_{}'.format(key)) # Expire redis data here
    rd.delete(key)

    return r_data

def verify_recaptcha(answer):
    response = requests.post('https://www.google.com/recaptcha/api/siteverify',
        data = {
            'secret': RCP_SECRET,
            'response': answer,
        })
    r = json.loads(response.text)
    return r['success']

def download_config(data):
    return Response(
        b64decode(data).decode(),
        mimetype = "text/javascript",
        headers = {
            "Content-Disposition": "attachment; filename=config.json"
        }
    )

@app.route('/runner')
def runner():
	return send_file('page/pm_runner.py',
		mimetype = "text/x-python",
        attachment_filename = 'izpm_run.py',
        as_attachment = True
	)

@app.route('/apk')
def apk():
    return send_file('page/izonemail.apk',
            mimetype = 'application/vnd.android.pacakage-archive',
            attachment_filename = 'izonemail.apk',
            as_attachment = True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', recaptcha_key = RCP_KEY)
    
    u_key = request.form.get('key')
    u_pin = request.form.get('pin')
    u_answer = request.form.get('g-recaptcha-response')

    if not u_key or not u_pin or not u_answer:
        return render_template('index.html', recaptcha_key = RCP_KEY, msg = "정상적인 경로로 접근하여 주세요.")
    
    if not verify_recaptcha(u_answer):
        return render_template('index.html', recaptcha_key = RCP_KEY, msg = "정상적인 경로로 접근하여 주세요.")

    dt = query_data(u_key, u_pin)
    if dt == None: 
        return render_template('index.html', recaptcha_key = RCP_KEY, msg = "유효하지 않은 키/PIN 혹은 만료된 키입니다.")

    return download_config(dt)


