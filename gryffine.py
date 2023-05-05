#!/usr/bin/python3
import json
import requests
from os import environ
from sys import argv
from syslog import syslog, LOG_ERR

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

data = json.dumps(record)

try:
    requests.post(ENDPOINT, json=data)
except Exception as err:
    error_message = 'Gryffine monitoring system error: '
    error_message += str(err)
    syslog(LOG_ERR, error_message)
