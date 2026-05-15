#!/usr/bin/python3

import sys
import re
import time
import json
sys.path.append("../vms-scripts/http")
sys.path.append("../vms-scripts/modules")
from zabbixapi import zabbix
from pprint import pprint
from workwtime import workwtime
from tgapi import bot

zapi = zabbix()
tapi = bot()

class initial_data():
	@classmethod
	@staticmethod
	def __specify_hostgroup_names(cls, data: list):
		for elem in data:
			elem["name"] = zapi.method("hostgroup.get", {\
				"groupids": [elem["groupid"]]
			})[0]["name"] 
		
	@classmethod
	@staticmethod	
	def __specify_hosts(cls, data: list):
		for elem in data:
			elem["hosts"] = zapi.method("host.get", {\
				"groupids": [elem["groupid"]]
			})	
	
	@classmethod
	@staticmethod	
	def __specify_events(cls, data: list):
		for group in data:
			for host in group["hosts"]:	
				host["problems"] = zapi.method("problem.get", {\
					"output": "extend",
					"hostids": [host["hostid"]]
				})	

	@classmethod
	@staticmethod	
	def get(cls):
		buf = ""
		data = []

		with open("./subjects.json", "r") as f:
			buf = f.read()

		for g in (json.loads(buf))["groupids"]:
			data.append({"groupid": g})

		cls.__specify_hostgroup_names(data)
		cls.__specify_hosts(data)
		cls.__specify_events(data)	
		return data
			

class zbx_host_group():
	def __init__(self, g: dict):
		self.name = g["name"]
		self.id = g["groupid"]
		self.hosts = g["hosts"]
	
	def find_router(self) -> dict:
		for host in self.hosts:
			if "router" in host["host"]:
				return host

		return None

def formatted_hostgroup_data() -> list:
	data = []
	for hg in initial_data.get():
		data.append(zbx_host_group(hg))			
	return data

def find_problem(pl: list, pn: str):
	for p in pl:
		if p["name"] == pn:
			return p

	return None

def report() -> str:
	msgs = []
	tmp = None
	fhgd = formatted_hostgroup_data()
	res = ""
	i = 1

	for hg in fhgd:
		tmp = find_problem(hg.find_router()["problems"], "ICMP: Unavailable by ICMP ping")

		if (tmp != None):
			msgs.insert(0, "Группа узлов {} недоступна.\n`{}`".format(hg.name, workwtime.epoch_to_iso(int(tmp["clock"]))))
		else:
			for host in hg.hosts:
				tmp = find_problem(host["problems"], "ICMP: Unavailable by ICMP ping")
				if (tmp != None):
					msgs.append("{} недоступен.\n`{}`".format(host["name"], workwtime.epoch_to_iso(int(tmp["clock"]))))

	for i in range(0, len(msgs)):
		msgs[i] = '{}) {}'.format(i+1, msgs[i])

	return '\n'.join(msgs)


if __name__ == "__main__":
	tapi.sendMessage(report())
