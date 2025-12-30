import sys
import re
sys.path.append("../vms-scripts/http")
sys.path.append("../vms-scripts/modules")
from zabbixapi import zabbix
from pprint import pprint
from datetime import datetime, timezone, timedelta
from workwtime import kztimezone
from tgapi import bot

def mdformat(s: str) -> str:
	return re.sub(r'(\W)', r'\\\1', s)	

zapi = zabbix()
groupids = ["183","168","169","170","171","172","173","174","175","176","177","157","158","155"]
message = ""
botapi = bot()
eventids = []
hostids = []
problems = zapi.method("problem.get", {"output": "extend", "groupids": groupids})
for problem in problems:
	eventids.append(problem["eventid"])
		
events = zapi.method("event.get", {"output": "extend", "eventids": eventids, "selectHosts": "extend"})

for i in range(0, len(events)):
	if events[i]["severity"] == "4":
		message = ""
		message += f"{i+1}\\.\n*{mdformat(events[i]["hosts"][0]["name"])}\\({mdformat(events[i]["hosts"][0]["host"])}\\)*\n"
		message += f"*{mdformat(events[i]["name"])}*\n"
		message += f"since\\: `{mdformat(str(datetime.fromtimestamp(int(events[i]["clock"]), tz=kztimezone())))}`\n"
		botapi.send_msg(message)
