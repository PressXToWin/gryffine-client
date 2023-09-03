#!/usr/bin/python3
import requests
from os import environ, uname
from sys import argv
from syslog import syslog, LOG_ERR

endpoint = argv[1]

record = {
    'hostname': uname()[1],
    'service': environ['PAM_SERVICE'],
    'user': environ['PAM_USER'],
    'rhost': environ.get('PAM_RHOST')
}
if argv[2] == 'success':
    record['is_successful'] = True
elif argv[2] == 'fail':
    record['is_successful'] = False

try:
    requests.post(endpoint, json=record)
except Exception as err:
    error_message = 'Gryffine monitoring system error: '
    error_message += str(err)
    syslog(LOG_ERR, error_message)
