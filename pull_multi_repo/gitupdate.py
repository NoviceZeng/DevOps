#!/root/.pyenv/shims/python
import threading,os,subprocess

class MyThread(threading.Thread):
    def __init__(self, dir2_path):
        super(MyThread, self).__init__()  # 重构run函数必须要写
        self.dir2_path = dir2_path

    def run(self):
        os.chdir(dir2_path)
        print("="*40)
        print(os.getcwd())
        subprocess.call('git pull', shell=True)
        subprocess.call('git reset --hard origin/master', shell=True)
        subprocess.call('git pull', shell=True)


if __name__ == "__main__":
    for dir in os.listdir('/root/gitlab'):
        dir1_path = os.path.join('/root/gitlab',dir)
        if os.path.isdir(dir1_path):
            dir1 = os.listdir(dir1_path)
            for dir2 in dir1:
                dir2_path = os.path.join(dir1_path,dir2)
                MyThread(dir2_path).start()
