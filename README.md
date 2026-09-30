# Unity Zoo

Live tracker for the Unity SMP "catch every mob" stream (Minecraft Java 26.3).

- `docs/` is the public site on GitHub Pages: `index.html` (mob list), `overlay.html` (OBS overlay), `zoo.json` (catch state).
- `tools/` runs locally during the stream: `zoo_server.py` (control panel + overlay server), `build_mobs.py` (resets the mob list).

## During the stream

```
python tools/zoo_server.py --push
```

| What | Where |
|------|-------|
| Control panel (click a mob = caught; search + Enter works too) | http://localhost:8765/ |
| OBS browser source (1920×1080) | http://localhost:8765/overlay.html |
| Site preview | http://localhost:8765/index.html |

With `--push`, every catch is committed and pushed to GitHub (batched every 20 s). The public site updates about 1 minute later.

OBS: Sources → + → Browser → URL `http://localhost:8765/overlay.html`, width 1920, height 1080. Add `?scale=0.8` to the URL to shrink it.

## Reset the list (clears all catches)

```
python tools/build_mobs.py --force
```
