"""Send code to the play daemon. Usage: run.py 'code' | run.py -f file.py"""
import os, socket, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOCK = os.path.join(ROOT, "work", "playthrough", "daemon.sock")
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
