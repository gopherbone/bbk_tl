# bbkemu JSON-lines protocol

`bbkemu` is a headless BBK A-series (A4980/A4988) emulator built on a vendored
BBKEmu core. It reads one JSON request per line on stdin and writes exactly one
JSON response per line on stdout; logs go to stderr (`RUST_LOG=info` for more).
`bbkemu --script file.jsonl` replays a file instead. The envelope and command
names follow gbemu-cli (`~/sameboy-cli/cli/PROTOCOL.md`).

```json
{"id": 1, "cmd": "mem.read", "params": {"addr": "$1aae", "len": 16}}
{"id": 1, "ok": true, "result": {"addr": "1aae", "len": 16, "data": "fb04..."}}
{"id": 1, "ok": false, "error": "no game loaded (load_gam first)"}
```

## Conventions

- Numbers may be JSON numbers or strings: `"$1aae"`, `"0x1aae"`, `"6830"`.
- Hex output is lowercase without `0x`.
- Three address spaces:
  - `addr`: 16-bit CPU address through the current bank mapping.
  - `phys`: physical address. RAM is `0x0000-0x7fff`, flash `0x200000-0x3fffff`,
    font ROM (8.BIN) `0x800000-0x9fffff`, OS ROM (E.BIN) `0xe00000-0xffffff`.
  - `gam`: offset in the loaded `.gam` file, which sits in flash at
    `phys = 0x20d000 + gam`.
- Reads through the DMA data ports (`$00-$03`) report the physical address the
  port actually read, so font and flash reads made through them show up in
  watchpoints and traces.
- Runs are deterministic: no host clock is used, and the RTC advances once per
  60 frames.
- A frame is 66,666 CPU cycles (4 MHz, 60 fps). Input events apply at frame
  starts.

## Commands

### Session
| cmd | params | result |
|---|---|---|
| `ping` | — | `{pong, version}` |
| `load_gam` | `path`, `model` (`4988` default, or `4980`), `rom_dir` (holds `8.BIN`, `E.BIN`) or `rom8`/`rome` | session info. Resets all analysis state |
| `info` | — | path, size, entry, data offset, archive offset/size, model, frame, instructions |
| `quit` | — | `{bye}` |

### CPU and execution
| cmd | params | result |
|---|---|---|
| `regs.get` | — | pc, a, x, y, sp, p, `pc_phys`, 16 bank mappings, halted, frame, cycles |
| `regs.set` | any of `pc,a,x,y,sp` | as `regs.get` |
| `step` | `n` (1) | run result |
| `run.frames` | `n` (1) | run result |
| `run.until` | `addr`, `max_instructions` (50M) | run result; reason `until` |
| `disasm` | `addr` (pc), `n` (16) | `{listing}`, each line `cpu [phys] bytes op` |

A run result is `{ran_instructions, ran_frames, pc, frame, instructions_total,
stopped}`. A stopped run also has `reason`, one of `breakpoint`, `watchpoint`,
`until`, `max_instructions` or `exited`, plus `detail`. Breakpoints fire
before the instruction runs, and resuming does not immediately fire the same
one again. Watchpoints fire after the accessing instruction has run.
Instruction fetches never trigger read watchpoints.

### Breakpoints
| cmd | params | result |
|---|---|---|
| `break.add` | `addr` and/or `phys`/`gam` (pc must map there; `phys` alone matches any CPU address), `stop` (true), `capture` | `{id}` |
| `break.list` / `break.del` (`id`) / `break.clear` | | |
| `break.log` | `max` (1000), `clear` | `{total, entries}` |

Every hit is appended to `break.log` (ring of 100k) with pc, phys, frame,
a/x/y and any captures. `stop:false` makes a silent logger. Each `capture`
item is one of:
- `{addr, len}`: bytes at a CPU address
- `{addr, deref:true, len, cstr?}`: bytes where the pointer at `addr` points.
  With `cstr`, capture stops at NUL.
- `{addr, deref:true, phys:true}`: the physical address the pointer resolves to
- `{stack:true, len}`: bytes above the stack pointer (return addresses)

### Watchpoints
| cmd | params | result |
|---|---|---|
| `watch.add` | one of `addr`/`phys`/`gam`, `end` (inclusive, same space), `access` (`r`/`w`/`rw`, default `w`), `value` (write match), `stop` (true), `log` (false) | `{id}` |
| `watch.list` / `watch.del` / `watch.clear` | | |

With `log:true`, every hit is appended to `break.log` (`{id, access, addr,
phys, value, pc, pc_phys}`). With `stop:false, log:true` you get a silent
access logger.

### Memory
| cmd | params | result |
|---|---|---|
| `mem.read` | `addr`/`phys`/`gam`, `len` (≤ 64 KiB) | `{data}` |
| `mem.write` | `addr`/`phys`/`gam`, `data` (hex). Phys and gam writes go straight into RAM or flash, bypassing flash commands | `{written}` |
| `mem.search` | `filter` over `new`/`old` (e.g. `"new != old && new == 5"`), `lo`/`hi` (RAM range), `max` | progressive, like gbemu |
| `mem.search.reset` | — | |
| `rom.search` / `gam.search` | `bytes` (hex), `max` | matches in the loaded `.gam` (`off`, `phys`) |

### Input
Key names are BBKEmu's: `ENTER`, `EXIT`, `UP`, `DOWN`, `LEFT`, `RIGHT`,
`SPACE`, `PGUP`, `PGDN`, `HELP`, letters, digits, and so on.

| cmd | params | result |
|---|---|---|
| `input.tap` | `key`, `hold` (4 frames), `wait` (4), `run` (true) | run result for hold + wait frames |
| `input.script` | `steps: [{key?, hold, wait}]` (no key = wait), `run` (true) | run result |
| `input.press` / `input.release` | `key` | holds until released |
| `input.replay` | `path` (bbkplay route), `until_frame`, `run` (true), `any_gam` (false: refuse a route recorded on another .gam) | `{events, last_frame, marks, run}`. Applies events exactly as bbkplay does; run it right after `load_gam` |

### Route recording
| cmd | params | result |
|---|---|---|
| `route.record` | `path`, `resume` (true) | starts recording every applied input as a bbkplay route. If `path` exists, it is first replayed up to where that session ended (fresh `load_gam` only), then recording continues |
| `route.mark` | `text` | adds a note at the next frame start |
| `route.status` | — | `{recording, path, events}` |
| `route.stop` | — | writes the session's end marker |

`snapshot.load` and `rewind.pop` truncate the recorded route back to the
snapshot, so the route always describes one straight path from boot. That
makes retries and save-scumming safe. `input.press`/`input.release` take
effect at the next frame start, like every other input.

A key is pressed once (`key_down`) and stays down until released, as in
BBKEmu's frontend. It is not re-pressed every frame.

### Screen
| cmd | params | result |
|---|---|---|
| `screen.capture` | `path` (else base64 PNG), `scale` (1-16) | `{width, height, hash, frame}`. The 159×96 LCD as grayscale. `hash` is FNV-1a of the pixels, a cheap way to detect change |

### Snapshots and rewind
| cmd | params | result |
|---|---|---|
| `snapshot.save` / `snapshot.load` / `snapshot.delete` | `name` | full emulator state, in memory |
| `snapshot.list` | — | |
| `rewind.set` | `frames` or `seconds` | keeps one state per frame |
| `rewind.pop` | `frames` (1) | |

File snapshots are not implemented yet.

### Trace and coverage
| cmd | params | result |
|---|---|---|
| `trace.start` | `max` (64k, max 4M), `with_regs`, `with_mem` (up to 4 accesses per instruction) | |
| `trace.stop` | — | keeps the ring for dumping |
| `trace.dump` | `limit` (1000), `tail`, `offset` | `{entries: [{pc, phys, op, regs?, mem?}]}` |
| `coverage.get` | `arm`, `max_ranges` | executed instruction starts inside the `.gam` image, as `.gam` offset ranges |
| `coverage.reset` | — | |

### BBKRPG archive
| cmd | params | result |
|---|---|---|
| `lib.map` | one of `addr`/`phys`/`gam`/`lib` | region (`header`, `engine`, `archive`); in the archive also `resource` (`GUT/1-1-1`), `offset` within it and, for scripts, `script_addr` (the address space of bbkrpg row ids) |
| `flash.load_lib` | `path` (archive file) | swaps the archive in the running game's flash and updates the game size. For quick checks only; reboot with `load_gam` for real runs |

## Hooks (伏魔记 engine build `c81b80…`)

`cli/py/bbkemu.py` has a `Hooks` class that turns two silent breakpoints into
`text.log` and `script.where`:
- `TEXT_DRAW_PHYS = 0xE94843`: the OS draw-string handler (OS call `0x2E`), hit
  once per call. It is in the OS ROM, so it is the same for every game. The
  string is at `($2f)`; args at `($28)`, where `[0]` is y.
- `SCRIPT_FETCH_PHYS = 0x211134`: the engine's script interpreter fetching an
  opcode through `($20)`. It is engine-specific, so other builds need it
  re-found. Mapped with `lib.map`, it gives `gut/<key>@<addr>`, which is exactly
  the bbkrpg string-table row id.
