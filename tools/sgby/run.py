"""Run code in the sgby daemon: run.py 'code' | run.py -f file.py"""
import os, socket, sys

SOCK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work", "sgby", "daemon.sock")
code = open(sys.argv[2]).read() if sys.argv[1] == "-f" else sys.argv[1]
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(SOCK)
s.sendall(code.encode() + b"\0")
data = b""
while not data.endswith(b"\0"):
    chunk = s.recv(65536)
    if not chunk:
        break
    data += chunk
sys.stdout.write(data.rstrip(b"\0").decode())
