#!/bin/python
#
# Это небольшой скрипт для пользования chromedriver,
# используя w3c webdriver протокол.
# Сам по себе w3c webdrier реализован по http
# Следовательно, мы легко сможем работать с ним через requests
#
# Source: https://www.w3.org/TR/webdriver2/#commands
#

import requests
import os
import time

host="localhost"
port="9515"
address=f"http://{host}:{port}/"

log_path="/tmp/chromedriver.log"
log_level="INFO"

def run_program(app, **kwargs):
    print(f"RUNNING \"{app.upper()}\"")
    cmdline = []
    for key in kwargs:
        value = str(kwargs[key])
        arg = key.replace("_", "-")
        cmdline.append(f"--{arg}={value}")
    pid = os.fork()
    if (pid != 0):
        os.execvp(app, cmdline)
    return pid

run_program("chromedriver", port=port, log_path=log_path, log_level=log_level)

time.sleep(1)
print("=========================")
print("  CODE                   ")
print("=========================")
def get_status():
    global address
    print("GETTING_STATUS")
    r = requests.get(address + "status")
    response = r.json()
    if (200 <= r.status_code < 300):
        response = response["value"]
        print("VERSION: %s" % response["build"]["version"])
        print("OS: %s %s %s" % (response["os"]["name"], response["os"]["version"], response["os"]["arch"]))
        return response
    print("Got error at 'get_status'")
    return response

def new_session(**params):
    print("CREATING_SESSION")
    r = requests.post(address + "session", json=params)
    response = r.json()
    if (200 <= r.status_code < 300):
        response = response["value"]
        print("SESSION ID: %s" % response["sessionId"])
        return response
    print("Got error at 'new_session'")
    return response

def get_current_url(sessionid):
    print("GETTING CURRENT URL")
    r = requests.get(address + "session/%s/url" % sessionid)
    response = r.json()
    if (200 <= r.status_code < 300):
        response = response["value"]
        print("CURRENT URL: %s" % response)
        return response
    print("Got error at 'get_current_url'")
    return response

response = get_status()
session = new_session(name="me", password="mypassword", capabilities={})
get_current_url(session["sessionId"])

print("=========================")
print("  END                    ")
print("=========================")

