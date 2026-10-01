"""Local server for the Unity SMP "לתפוס את כולם" stream. Python standard library only.

    python tools/catch_server.py            # control panel + overlay, no GitHub push
    python tools/catch_server.py --push     # also commit + push docs/catch.json to GitHub after each catch

Open:
    http://localhost:8765/            control panel (click a mob = caught)
    http://localhost:8765/overlay.html   OBS browser source (1920x1080)
    http://localhost:8765/index.html     preview of the public site
"""
import json
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = DOCS / "catch.json"
CONTROL = Path(__file__).with_name("control.html")
PORT = 8765
PUSH = "--push" in sys.argv
PUSH_DELAY = 20  # seconds: batch several quick catches into one commit

lock = threading.Lock()
push_state = {"pending": [], "timer": None, "message": ""}


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def save(data):
    tmp = DATA.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(DATA)


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


def do_push():
    with lock:
        names = push_state["pending"][:]
        push_state["pending"].clear()
        push_state["timer"] = None
    if not names:
        return
    git("add", "docs/catch.json")
    msg = "catch: " + ", ".join(dict.fromkeys(names))
    c = git("commit", "-m", msg)
    if c.returncode != 0 and "nothing to commit" not in c.stdout:
        push_state["message"] = "commit נכשל: " + (c.stderr or c.stdout).strip()[:120]
        return
    p = git("push")
    push_state["message"] = (
        f"האתר עודכן ({time.strftime('%H:%M')})" if p.returncode == 0
        else "push נכשל: " + p.stderr.strip()[:120]
    )
    print(push_state["message"])


def schedule_push(name):
    if not PUSH:
        return
    with lock:
        push_state["pending"].append(name)
        if push_state["timer"] is None:
            t = threading.Timer(PUSH_DELAY, do_push)
            t.daemon = True
            push_state["timer"] = t
            t.start()
            push_state["message"] = f"האתר יתעדכן בעוד {PUSH_DELAY} שניות"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(DOCS), **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "/api/" in (args[0] if args else ""):
            super().log_message(fmt, *args)

    def send_json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/control"):
            body = CONTROL.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/api/state":
            self.send_json(load())
        elif path == "/api/push-status":
            self.send_json({"message": push_state["message"]})
        else:
            super().do_GET()

    def do_POST(self):
        if self.path != "/api/toggle":
            return self.send_json({"error": "not found"}, 404)
        # Only accept requests from this computer.
        if self.client_address[0] not in ("127.0.0.1", "::1"):
            return self.send_json({"error": "local only"}, 403)
        length = int(self.headers.get("Content-Length", 0))
        mob_id = json.loads(self.rfile.read(length) or b"{}").get("id")
        with lock:
            data = load()
            mob = next((m for m in data["mobs"] if m["id"] == mob_id), None)
            if not mob:
                return self.send_json({"error": f"unknown mob {mob_id}"}, 400)
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            mob["caught"] = not mob["caught"]
            mob["caught_at"] = now if mob["caught"] else None
            if mob["caught"]:
                data["last_caught"] = mob_id
            elif data.get("last_caught") == mob_id:
                latest = max((m for m in data["mobs"] if m["caught"]), key=lambda m: m["caught_at"], default=None)
                data["last_caught"] = latest["id"] if latest else None
            data["updated"] = now
            save(data)
        print(f"{'CAUGHT' if mob['caught'] else 'undo'}: {mob['en']}")
        schedule_push(mob["en"])
        self.send_json(data)


if __name__ == "__main__":
    if not DATA.exists():
        raise SystemExit("docs/catch.json missing. Run: python tools/build_mobs.py")
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Control panel:  http://localhost:{PORT}/")
    print(f"OBS overlay:    http://localhost:{PORT}/overlay.html")
    print(f"Site preview:   http://localhost:{PORT}/index.html")
    print("GitHub push:    " + ("ON (every catch, batched)" if PUSH else "OFF (run with --push to update the public site)"))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
