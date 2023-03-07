#!/usr/bin/python3
import json
import requests
from os import environ
from sys import argv

ENDPOINT = ''

record = {
    'hostname': environ['HOSTNAME'],
    'service': environ['PAM_SERVICE'],
    'user': environ['PAM_USER']
}
if 'PAM_RHOST' not in environ or environ['PAM_RHOST'] == '':
    record['rhost'] = None
else:
    record['rhost'] = environ['PAM_RHOST']
if argv[1] == 'success':
    record['is_successful'] = True
elif argv[1] == 'fail':
    record['is_successful'] = False

json_object = json.dumps(record)

try:
    requests.post(ENDPOINT, json=json_object)
except:
    pass
