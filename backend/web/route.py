#-*- coding: utf-8 -*-
import redis
import json
import requests

from os import getenv
from base64 import b64decode
from flask import Flask, render_template, request, Response

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

def download_runner(data):
    py_code = '''#-*- coding: utf-8 -*-
import os
import re
import json
import requests

pm_headers = json.loads(\'''' +  b64decode(data).decode() + '''\')

def pmGet(url):
	return requests.get(url, headers=pm_headers)

img_ptn = re.compile('img/.*?\\.(?:jpeg|jpg|png|gif)')

class PrivateMail:
	def __init__(self):
		self.id = ""

		self.member = ""
		self.image = False
		self.time = ""
		self.subject = ""
		self.body = ""
		self.body_preview = ""

	def fetch(self):
		if self.id == "":
			raise Exception("PrivateMail ID cannot be null")

		url = "https://app-web.izone-mail.com/mail/%s" % self.id
		res = pmGet(url).text

		# resolve relative path
		res = res.replace("/css/starship.css", "../static/starship.css")

		#found all image
		if self.image:
			print("[*] Processing image of mail %s" % self.id)
			imgs = img_ptn.findall(res)
			print(imgs)
			for img in imgs:
				output_path = "output/" + img
				remote_path = "https://img.izone-mail.com/upload/" + img
				if not os.path.exists(os.path.dirname(output_path)):
					os.makedirs(os.path.dirname(output_path))

				with open(output_path, "wb") as f:
					resp = pmGet(remote_path)
					f.write(resp.content)

			res = res.replace("https://img.izone-mail.com/upload/", "../")

		self.body = res

	def writeOut(self):
		if self.body == "":
			self.fetch()

		if not os.path.exists("output/mail/"):
			os.makedirs("output/mail/")

		with open("output/mail/%s.html" % self.id, "w", encoding="UTF-8") as f:
			f.write(self.body)

def getPMList():
	pm_list = []
	idx = 1
	target = "https://app-api.izone-mail.com/v1/inbox?is_star=0&is_unread=0&page=%d"
	
	while True:
		whole_data = json.loads(pmGet(target % idx).text)
		print("[+] Fetching page %d" % idx)
		for pm_data in whole_data["mails"]:
			pm = PrivateMail()
			
			pm.id = pm_data["id"]

			pm.member = pm_data["member"]["name"]
			pm.image = pm_data["is_image"]
			pm.time = pm_data["receive_time"]
			pm.subject = pm_data["subject"]
			pm.body_preview = pm_data["content"][:45]

			pm_list.append(pm)

		if not whole_data["has_next_page"]:
			break
		idx += 1
	print("[*] Fetching done - %d mails loaded" % len(pm_list))
	return pm_list

def wroteBack(pmlist):
	with open("output/pm.js", "w", encoding="UTF-8") as f:
		f.write("var pm_list = Array();")
		for pm in pmlist:
			fmt = 'pm_list.push({"id": "%s", "member": "%s", "time": "%s", "subject": "%s", "preview": "%s", "time": "%s"});'
			f.write(fmt % (pm.id, pm.member, pm.time, pm.subject.replace("\"", "\\\""), pm.body_preview.replace("\"", "\\\""), pm.time))

if __name__ == "__main__":
	pm_list = getPMList()
	input("\\nPress Enter to continue...")
	for x in pm_list:
		x.writeOut()

	print("[*] Writing local database")
	wroteBack(pm_list)
	print("[*] Writing done")
'''
    return Response(
        py_code,
        mimetype = "text/x-python",
        headers = {
            "Content-Disposition": "attachment; filename=IZPM.py"
        }
    )


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

    return download_runner(dt)


