from wsgiref.simple_server import make_server
import subprocess,os,sys

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    root_dir = '/imgserver/'
    for site_name in os.listdir(root_dir):
        sync_path = root_dir + site_name + '/upload'
        os.chdir(sync_path)
        with open('/root/pic_sync/log/git_pull.log', 'a+') as f:
            #git_pull = subprocess.Popen('git reset --hard origin/master', shell=True, stdout=subprocess.PIPE)
            git_pull = subprocess.Popen('git pull origin master', shell=True, stdout=subprocess.PIPE)
            for line in iter(git_pull.stdout.readline, ''):
                sys.stdout.write(line)
                f.write(line)

httpd = make_server('0.0.0.0', 8009, application)
print('Serving HTTP on port 8009...')
httpd.serve_forever()
