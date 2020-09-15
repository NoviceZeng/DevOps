from wsgiref.simple_server import make_server
import git_pull

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    git_pull.exec_pull() 
    return 'git pull finish'
httpd = make_server('0.0.0.0', 8009, application)
print('Serving HTTP on port 8009...')
httpd.serve_forever()
