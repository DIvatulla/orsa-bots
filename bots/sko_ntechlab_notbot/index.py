#!/usr/bin/python3

import sys
import re
import time
import json
sys.path.append("../vms-scripts/http")
sys.path.append("../vms-scripts/modules")
from egsvapi import egsv
from pprint import pprint
from datetime import datetime, timezone, timedelta
from workwtime import workwtime
from tgapi import bot

def subjects() -> dict:
	with open("./subjects.json", "r", encoding="utf-8") as f:
		return json.load(f)

def get_data() -> dict:
	res = subjects()
	(list(map(lambda x: x.setdefault("records", []), res["cameras"])))

	for cam in res["cameras"]:
		for rec in eapi.method("lvs2.record.list", workwtime.mongo_filter(24))["records"]:
			if rec["camera"] == cam["id"]:
				cam["records"].append(rec)	

	return res

def latest(rl: list) -> dict:
	l = rl[0]

	for rec in rl:
		if l["finished_at"] < rec["finished_at"]:
			l = rec

	return l
	
if __name__ == "__main__":
	eapi = egsv()
	botapi = bot()
	data = get_data()

	msg = ""
	tmp = {}
	for i in range(0, len(data["cameras"])):
		if len(data["cameras"][i]["records"]) == 0:
			msg += '{}) "{}":\nнет событий\n'.format(i+1, eapi.method("camera.get", {"id": data["cameras"][i]["id"]}))
			continue	
		else:
			tmp = latest(data["cameras"][i]["records"])
			msg += '{}) "{}":\n{}\n'.format(i+1, tmp["origin_name"], tmp["datetime"]) 

	botapi.sendMessage(msg)	
