import requests
import json
import time
import sys

BASE = "http://127.0.0.1:5000/"

u_id = 'default01'
pw = 'pw01'
port = '4999'

response = requests.post(BASE + "/login", files={'u_id': u_id.encode(encoding='UTF-8'), 'pw': pw.encode(encoding='UTF-8'), 'port': port.encode(encoding='UTF-8')})
print(response.json())

response = requests.get(BASE + "/online_list", files={'u_id': u_id.encode(encoding='UTF-8'), 'pw': pw.encode(encoding='UTF-8')})
print(response.json())

response = requests.post(BASE + "/logout", files={'u_id': u_id.encode(encoding='UTF-8'), 'pw': pw.encode(encoding='UTF-8')})
print(response.json())

response = requests.get(BASE + "/online_list", files={'u_id': u_id.encode(encoding='UTF-8'), 'pw': pw.encode(encoding='UTF-8')})
print(response.json())

    

