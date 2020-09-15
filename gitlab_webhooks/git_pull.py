import subprocess,os,sys,threading

class MyThread(threading.Thread):
    def __init__(self, sync_path):
        super(MyThread, self).__init__()
        self.sync_path = sync_path

    def run(self):
        os.chdir(self.sync_path)
        with open('/root/pic_sync/log/git_pull.log', 'a+') as f:
            #git_pull = subprocess.Popen('git reset --hard origin/master', shell=True, stdout=subprocess.PIPE)
            git_pull = subprocess.Popen('git pull origin master', shell=True, stdout=subprocess.PIPE)
            for line in iter(git_pull.stdout.readline, ''):
                sys.stdout.write(line)
                f.write(line)

def exec_pull():
    root_dir = '/imgserver/'
    for site_name in os.listdir(root_dir):
        sync_path = root_dir + site_name + '/upload'
        MyThread(sync_path).start()

if __name__ == "__main__":
    exec_pull()
