#!/usr/bin/env python

import os
import getpass
import base64
import requests
import demjson
from HTMLParser import HTMLParser

auth = os.getenv('ROUTER_ACCESS')

if auth is None:
    user = raw_input("Enter username: ")
    password = getpass.getpass()
    auth = base64.b64encode(user + ':' + password)

try:
    response = requests.get(
        'http://www.routerlogin.net/QOS_device_info.htm',
        headers={
            'Authorization': 'Basic ' + auth,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
    )
    response.raise_for_status()
except:
    print("Could not retrieve connected devices")
    exit(-1)

json_string = response.content

devices = demjson.decode(json_string)
for device in devices['device']:
    encoded = device.get('name')
    if encoded is not None:
        print(device.get('ip', 'NONE') + ': ' + HTMLParser().unescape(encoded))
