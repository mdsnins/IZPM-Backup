#-*- coding: utf-8 -*-
import json
import sys

def main():
	if len(sys.argv) != 2:
		return

	f = open(sys.argv[1], "r", encoding="UTF-8")
	raw = f.read()[14:]
	pm_data = json.loads(raw)
	
	for pm in pm_data:
		pm.pop("subject")
		pm.pop("preview")
		pm.pop("body")


	f = open("pm_upload.json", "w", encoding="UTF-8")
	f.write(json.dumps(pm_data))
	f.close()

if __name__ == "__main__":
	main()
