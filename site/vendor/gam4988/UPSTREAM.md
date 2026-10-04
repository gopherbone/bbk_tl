# gam4988 web core (vendored)

`gam4988.js`, `gam4988.wasm` and `src/` are copied unchanged from the `eebbk/`
module of [iuxt/bbk-games](https://github.com/iuxt/bbk-games/tree/main/eebbk),
commit `971b8301fa74d32d47ca7bbd5713a15fda820b25` (2026-09-22).

That module is a WebAssembly build of the libretro core
[gam4980](https://codeberg.org/iyzsong/gam4980) by iyzsong, which is based on the
[BA4988 simulator](https://gitee.com/BA4988/BBK-simulator) by 无云 and
[vrEmu6502](https://github.com/visrealm/vrEmu6502) by Troy Schrapel.

License: GNU GPL v3 (see `COPYING`). `src/` is the corresponding source of the
wasm build. Rebuild it with emsdk using `eebbk/web/CMakeLists.txt` from the
upstream repository.

We use the core's legacy firmware mode: `web_init` gets `8.BIN` followed by
`E.BIN` (4 MiB) instead of the full 27 MiB A4988 package. Games don't need the
dictionary banks.
