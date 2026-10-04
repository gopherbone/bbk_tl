# Playing and recording routes

Three ways to run `bbkplay`:

```sh
P=bbkemu/target/release/bbkplay; ROMS=gam4980/retroarch/system/gam4980
$P <game.gam> --roms $ROMS                                # just play (any build)
$P <game.gam> --roms $ROMS --from routes/fmj.agent.route.jsonl  # watch/continue the agent's route, unrecorded
$P <game.gam> --roms $ROMS --route routes/mine.route.jsonl      # record (resumes if it exists)
```

A route only replays on the `.gam` it was recorded on; bbkplay refuses others.


`bbkplay` is BBKEmu's desktop window running on the same core as `bbkemu`.
It records every key press to a route file as you play, and `bbkemu`'s
`input.replay` plays that route back frame for frame. That replay is how QA
reaches every line of dialogue in each translated build.

```sh
cd ~/bbk_tl/bbkemu && cargo build --release      # once
cd ~/bbk_tl
bbkemu/target/release/bbkplay gam4980/retroarch/downloads/bbk/伏魔记.gam \
    --roms gam4980/retroarch/system/gam4980 --route routes/fmj.route.jsonl
```

| Key | Does |
| --- | --- |
| Arrows | Move / menu |
| Enter | Confirm, advance dialogue |
| Backspace | Back / cancel (the dictionary's EXIT key) |
| Space, PageUp/PageDown, letters, digits | The dictionary's own keys, if the game asks |
| Tab (hold) | Fast-forward 4x |
| F2 | Drop a numbered marker in the route (note what it was for) |
| F12 | Screenshot (`bbkplay-<frame>.pgm`) |
| Esc | Quit (the route is already saved) |

- Run the same command again to continue. The route replays at about 20x speed,
  so an hour of play takes about 3 minutes to catch up. Then you're back where
  you stopped, still recording.
- Save in-game whenever you like; that's part of the route too. There are no
  emulator save states, because loading one would break the replay.
- Dying and reloading an in-game save is fine. Every key press is kept.
- Try to see as much text as you can: talk to every NPC, open shops, read
  item descriptions, use each kind of item and magic once, and lose a fight
  once if it's cheap. QA can only check lines the route draws.
- No sound (this player has no audio).
- The window title shows play time and frame. If something looks broken, press
  F2 and jot down the marker number.

Check a route replays (headless, prints the end frame and a screen hash):

```sh
bbkemu/target/release/bbkplay <game.gam> --roms <dir> --route <route> --verify
```
