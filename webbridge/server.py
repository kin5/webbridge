import shlex, subprocess

class Server:
    
    def __init__(self, cmd):
        
        self.cmd = shlex.split(cmd)
        self.process = None
        
    def run(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        self.process = subprocess.Popen(self.cmd, startupinfo=startupinfo)
        
    def kill(self):
        if self.process != None:
            self.process.kill()