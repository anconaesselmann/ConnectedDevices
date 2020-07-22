#!/usr/bin/env python

import os
import getpass
import base64
import requests
import demjson
from HTMLParser import HTMLParser

def split_ip(ip):
    return tuple(int(part) for part in ip.split('.'))

def auth_header():
    auth = os.getenv('ROUTER_ACCESS')

    if auth is None:
        user = raw_input("Enter username: ")
        password = getpass.getpass()
        auth = base64.b64encode(user + ':' + password)
    return auth

def fetch_devices(auth):
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
        return None

    json_string = response.content
    
    devices = filter(None, demjson.decode(json_string)['device'])

    # device names are html encoded and need to be cleaned
    for i in range(len(devices)):
        devices[i]['name'] = HTMLParser().unescape(devices[i].get('name', "NONE"))

    return devices

def sort_by_ip(devices):
    return sorted(devices, key = lambda i: split_ip(i['ip']))

def devices_list(devices):
    result = ""
    for device in devices:
        if result != "":
            result += "\n"
        result += device.get('ip', 'NONE') + ': ' + device.get('name')
    return result

auth = auth_header()

devices = fetch_devices(auth)
devices = sort_by_ip(devices)

if devices is None:
    print("Could not retrieve connected devices")
    exit(-1)

print(devices_list(devices))
