#!/usr/bin/python3
import os
import sys
from subprocess import Popen, PIPE, STDOUT, call
from wsgiref.simple_server import make_server

def application(enviro, start_response):
    start_response('200 OK', [('content-type', 'text/html')])
    os.chdir('/opt/nginx-whitelist')
    #call('git reset --hard origin/main', shell=True)
    #call('git pull origin main', shell=True)
    with open('/opt/git_pull/logs/git_pull.log', 'a+') as f:
        Popen('git reset --hard origin/main', shell=True, stdout=PIPE)
        git_stdout = Popen('git pull origin main', shell=True, stdout=PIPE)
        for line in iter(git_stdout.stdout.readline, ''):
            f.write(line.decode('utf-8'))
    return ['<h3>Hey I`m hook! Who are you?</h3>'.encode('utf-8')]

httpd = make_server('', 8000, application)
print("Serving HTTP on port 8000...")
httpd.serve_forever()
