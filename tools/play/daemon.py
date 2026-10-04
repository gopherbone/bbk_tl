"""Persistent Python namespace holding a live bbkemu session.

    python3 tools/play/daemon.py &            # starts, listens on work/playthrough/daemon.sock
    python3 tools/play/run.py 'print(e.call("info"))'   # exec code in the namespace
    python3 tools/play/run.py -f snippet.py

The namespace starts with `from play import *` (tools/play/play.py).
Code is exec'd; stdout/stderr are captured and returned.
"""
import contextlib, io, os, socket, sys, traceback

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOCK = os.path.join(ROOT, "work", "playthrough", "daemon.sock")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

ns = {"__name__": "__play__"}
exec("from play import *\nimport importlib, play as _play\ndef rl():\n    import sys as _s; _s.modules.get('maps') and importlib.reload(_s.modules['maps'])\n    importlib.reload(_play)\n    exec('from play import *', globals())\n", ns)

def main():
    if os.path.exists(SOCK):
        os.unlink(SOCK)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(SOCK)
    s.listen(1)
    while True:
        c, _ = s.accept()
        data = b""
        while not data.endswith(b"\0"):
            chunk = c.recv(65536)
            if not chunk:
                break
            data += chunk
        code = data.rstrip(b"\0").decode()
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                exec(compile(code, "<run>", "exec"), ns)
            except SystemExit:
                pass
            except BaseException:
                traceback.print_exc()
        c.sendall(out.getvalue().encode() + b"\0")
        c.close()
        if ns.get("_quit"):
            break

if __name__ == "__main__":
    main()
