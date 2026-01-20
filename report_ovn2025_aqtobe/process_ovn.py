import json
import csv

data = []

with open("ovn.json", "r", encoding="utf-8") as f:
	data = json.load(f)

for strazh in data:
	for ovn in strazh["cameras"]:
		print("{};{};{};{}".format(ovn["id"], ovn["name"], strazh["name"], strazh["host"]))	
