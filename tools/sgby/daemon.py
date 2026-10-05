"""Persistent bbkemu session for 三国霸业 exploration.

    python3 tools/sgby/daemon.py [GAM] &          # listens on work/sgby/daemon.sock
    python3 tools/sgby/run.py 'k("ENTER"); shot("a")'

The namespace has `e` (BBKEmu), `k(key, n=1, wait=40)`, `shot(name)` ->
work/sgby/shots/<name>.png (3x), `boot()` and `S` (snapshot helpers).
"""
import contextlib, io, os, socket, sys, traceback

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "bbkemu", "cli", "py"))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
from bbkemu import BBKEmu  # noqa: E402

GAM = sys.argv[1] if len(sys.argv) > 1 else "gam4980/retroarch/downloads/bbk/三国霸业.gam"
SOCK = os.path.join(ROOT, "work", "sgby", "daemon.sock")
os.makedirs(os.path.join(ROOT, "work", "sgby", "shots"), exist_ok=True)

e = BBKEmu()


def boot(path=None):
    e.load_gam(path or GAM, rom_dir="gam4980/retroarch/system/gam4980")
    e.run_frames(600)


def k(key, n=1, wait=40, hold=4):
    for _ in range(n):
        e.tap(key, hold=hold, wait=wait)


def shot(name, scale=3):
    p = f"work/sgby/shots/{name}.png"
    e.screen(p, scale=scale)
    return p


boot()
ns = {"e": e, "k": k, "shot": shot, "boot": boot, "__name__": "__sgby__"}


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
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                exec(data.rstrip(b"\0").decode(), ns)
            except Exception:  # noqa: BLE001
                traceback.print_exc()
        c.sendall(out.getvalue().encode() + b"\0")
        c.close()


main()
