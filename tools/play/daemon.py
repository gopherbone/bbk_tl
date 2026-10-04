"""Persistent Python namespace holding a live bbkemu session.

    python3 tools/play/daemon.py [--game fmj] &   # listens on <playthrough>/daemon.sock
    python3 tools/play/run.py [--game fmj] 'print(e.call("info"))'   # exec code in the namespace
    python3 tools/play/run.py [--game fmj] -f snippet.py

<playthrough> is the game profile's directory (work/playthrough for fmj).

The namespace starts with `from play import *` (tools/play/play.py).
Code is exec'd; stdout/stderr are captured and returned.
"""
import contextlib, io, os, socket, sys, traceback

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from bbkrpg import games  # noqa: E402
GAME = games.from_argv()
os.environ["BBK_GAME"] = GAME.key      # play.py (and its reloads) read it
if "--en" in sys.argv:                 # play the English build (play.py BBK_PLAY_EN)
    os.environ["BBK_PLAY_EN"] = "1"
os.makedirs(GAME.path("playthrough"), exist_ok=True)
SOCK = os.path.join(GAME.path("playthrough"), "daemon.sock")
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
