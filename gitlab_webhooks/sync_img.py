#coding:utf-8
from wsgiref.simple_server import make_server
import subprocess,os,sys
def RunServer(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    os.chdir("/data/work/live_oss_img");
    git_reset = subprocess.Popen('git reset --hard origin/master', shell=True, stdout=subprocess.PIPE)
    git_pull = subprocess.Popen('git pull origin master', shell=True, stdout=subprocess.PIPE)
    return '<h1>pull live_php_admin code now......</h1>'

if __name__ == '__main__':
    httpd = make_server('0.0.0.0', 9991, RunServer)
    print ("Serving HTTP on port 9991...")
    httpd.serve_forever()
