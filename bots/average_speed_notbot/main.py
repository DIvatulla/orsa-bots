#!/usr/bin/env python3 

import sys
import egsv_notification
import zbx_notification
sys.path.append("../modules")
sys.path.append("../modules/http")
from tgapi import bot

tapi = bot()

if __name__ == "__main__":
    message = egsv_notification.info()
    message += zbx_notification.info()
    tapi.sendMessage(message)
