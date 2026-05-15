import sys
import re
import time
import json
from egsvapi import egsv
from pprint import pprint
from workwtime import workwtime

eapi = egsv()

class initial_data():
	@classmethod
	@staticmethod	
	def __specify_cameras(cls, taxonomies: list) -> dict:
		return eapi.method("camera.list", {\
			"filter": {\
               "_taxonomies": {\
                    "$in": taxonomies
                 }
            }
		})["cameras"]

	@classmethod
	@staticmethod	
	def __specify_events(cls, camera: list):
		f = workwtime.mongo_filter(24)
		f["filter"]["camera"] = {"$in": [camera["id"]]}
		pprint(f)

		return eapi.method("rtms.number.list", f)["numbers"]

	@classmethod
	@staticmethod	
	def get(cls):
		buf = ""
		taxonomies = []
		cameras = []
		events = []
		res = []
	
		with open("./subjects.json", "r") as f:
			buf = f.read()

		taxonomies = (json.loads(buf))["egsv"]["taxonomies"]
		cameras = cls.__specify_cameras(taxonomies)

		for c in cameras:
			res.append({\
				"id": c["id"],
				"name": c["name"],
				"rtms": cls.__specify_events(c)
			})
		
		return res
	
def info():
	msgs = "EGSV:\n"

	for r in initial_data.get():
		if len(r["rtms"]) == 0:
			msgs += f"{r["name"]}:\nНет событий\n"
		else:
			msgs += f"{r["name"]}:\n`{r["rtms"][-1]['datetime']}`\n"
	
	return msgs
