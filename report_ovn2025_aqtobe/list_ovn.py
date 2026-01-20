import sys
import re
import time
import json
sys.path.append("../http")
sys.path.append("../modules")
from egsvapi import egsv
from pprint import pprint

eapi = egsv()

def get_tax() -> str:
	for tax in eapi.method("taxonomy.list")["taxonomies"]:
		if re.search("ОВН 2025", tax["name"]):
			return tax["id"]

def get_ovn() -> dict:
	return eapi.method("camera.list", {\
	"filter":{\
		"_taxonomies":{\
			"$in": [get_tax()]
		}	
	}})["cameras"]

def result() -> dict:
	ovn = get_ovn()
	tmp = {}
	res = []

	for s in eapi.method("server.list")["servers"]:
		tmp ={\
			"id": s["id"],
			"name": s["name"],
			"host": s["host"],
			"cameras":[]
		}

		for c in ovn:
			if c["server"] == tmp["id"]:
				tmp["cameras"].append({\
					"id": c["id"],
					"name": c["name"],
					"url": c["url"]\
				})	

		if len(tmp["cameras"]) > 0:
			res.append(tmp)

	return res


with open("ovn.json", "w") as f:
	f.write(json.dumps(result()))
