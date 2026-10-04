# BBK Games in English (web player)

A static site that plays the translated games in the browser. The player
uses the gam4988 WebAssembly core from
[iuxt/bbk-games](https://github.com/iuxt/bbk-games) (GPL v3, vendored unchanged
in `vendor/gam4988/`, see `UPSTREAM.md`). The pages, `js/` and `css/` are ours.

```
site/
  catalog.json        games and versions (source paths are relative to the repo root)
  src/                pages, scripts, styles, _headers, 404.html
  vendor/gam4988/     web core + its source and license
  wrangler.jsonc      Cloudflare Workers static-assets config
  dist/               build output (git-ignored: holds firmware and game files)
```

## Build and preview

```sh
python3 tools/site/build.py            # site/dist, with a boot smoke test + title shot per game
python3 -m http.server -d site/dist 8000
```

The build concatenates `8.BIN` + `E.BIN` from `gam4980/` into the 4 MiB
firmware the core's legacy mode takes, writes each catalog version as a
content-hashed `.gam` (a base file, plus a BPS patch from `dist/` for
translations), and copies the patches for download. The smoke test compiles
the same core natively (`tools/site/shot.c`, with a stub `emscripten.h`) and
fails the build if a game doesn't boot or shows a blank screen.

`node tools/site/cdp_shot.mjs <url> <out.png> [--mobile --w 390 --h 844 --dpr 3]
[--keys "Enter:3000,..."] [--eval "js"]` drives headless Chrome over the DevTools
protocol, for checking layouts and input on emulated phones.

## Deploy (Cloudflare Workers)

```sh
python3 tools/site/build.py
cd site && npx wrangler deploy
```

No Worker script is needed: `wrangler.jsonc` serves `dist/` as static assets.
The largest file is the 4 MiB firmware, well under the 25 MiB per-asset limit.
Hashed game and firmware files get immutable cache headers (`src/_headers`).

## Adding a game

1. Translate and release it like Demonbane: a `.bps` in `dist/` against the
   original `.gam`.
2. Add an entry to `catalog.json` with an `en` version (`base` + `patch`) and a
   `zh` version (`base` only), plus title, year, authors and blurb. `keys` lists
   the keys the game uses. The player always shows the d-pad and OK/Back; the
   other dictionary keys are behind "Extra dictionary keys" in the menu.
3. Rebuild. The smoke test catches games that don't boot on the web core.

Saves: the core keeps in-game saves in its Flash save area (0x14000 bytes),
which the player mirrors to IndexedDB under `flash/<game>/<lang>` whenever the
game writes it. Quick-save states (`state/<game>/<lang>`) are tied to the
translation version, since a state holds RAM that points into the game code.

## Notes

- The firmware is BBK's. Hosting it follows what iuxt/bbk-games already does.
  The project's `.bps` releases remain the firmware-free way to get the
  translation.
- The page discloses up front that the translation was made with AI. Keep that
  note on the home page and in the player menu.
