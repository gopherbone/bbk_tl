"""Send code to the play daemon. Usage: run.py [--game fmj] 'code' | run.py [--game fmj] -f file.py"""
import os, socket, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from bbkrpg import games  # noqa: E402
SOCK = os.path.join(games.from_argv().path("playthrough"), "daemon.sock")
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
