#-*- coding: utf-8 -*-
import os
import re
import json
import requests

#Private Mail Credentials
PM_USERID = ""
PM_ACCESSTOKEN = "" 

PM_APPVER = ""
PM_DEVICE = ""
PM_OSTYPE = ""
PM_OSVERSION = ""
PM_USERAGENT = ""

pm_headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Application-Version": PM_APPVER,
	"User-Id": PM_USERID,
	"Accept-Language": "ko-kr",
	"Accept-Encoding": "gzip, deflate, br",
	"Device-Version": PM_DEVICE,
	"Os-Type": PM_OSTYPE,
	"Os-Version": PM_OSVERSION,
	"Application-Language": "ko",
	"Access-Token": PM_ACCESSTOKEN,
	"User-Agent": PM_USERAGENT,
	"Connection": "keep-alive",
	"Accept": "*/*",
	"Terms-Version": "1",
}

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
	input("\nPress Enter to continue...")
	for x in pm_list:
		x.writeOut()

	print("[*] Writing local database")
	wroteBack(pm_list)
	print("[*] Writing done")

