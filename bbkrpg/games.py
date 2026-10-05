"""Per-game profiles: which .gam, where its working files live, and the
engine-specific tables the build needs.

Tools pick the game from `--game KEY` (see `from_argv`) or the BBK_GAME
environment variable, defaulting to fmj. Paths are relative to the repo root.
伏魔记 keeps the paths it had before profiles existed; later games use
`<key>` directories (translations/<key>/parts, docs/<key>/, work/<key>/).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Callable

from . import engine_text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_DIR = "gam4980/retroarch/downloads/bbk"
ROMS = "gam4980/retroarch/system/gam4980"


def _fmj_images(res: dict, rows: list[dict]) -> None:
    from . import images_en
    images_en.apply(res)


def _yxts_images(res: dict, rows: list[dict]) -> None:
    from . import images_yxts
    images_yxts.apply(res, rows)


def _szzm_images(res: dict, rows: list[dict]) -> None:
    from . import images_szzm
    images_szzm.apply(res, rows)


def _xkx_images(res: dict, rows: list[dict]) -> None:
    from . import images_xkx
    images_xkx.apply(res, rows)


def _jy_images(res: dict, rows: list[dict]) -> None:
    from . import images_jy
    images_jy.apply(res, rows)


@dataclass(frozen=True)
class Game:
    key: str
    zh: str                                   # .gam file name without extension
    engine: list = field(default_factory=list)  # engine_text entries for this build
    images: Callable[[dict, list], None] | None = None  # (res, rows): redraws text inside images
    title_en: str | None = None               # release name; None = not releasable yet
    owner: str = "BBK"                        # rights holder named in release notes
    dialogue_top: int = 57                    # top of a say box's first English row (fontpatch)
    content_note: str = ""                    # for the release README and the site catalog
    strings: str = ""
    gut: str = ""
    parts: str = ""
    merged: str = ""
    glossary: str = ""
    route: str = ""
    playthrough: str = ""
    qa: str = ""
    en_gam: str = ""

    @property
    def gam(self) -> str:
        return f"{GAMES_DIR}/{self.zh}.gam"

    def path(self, name: str) -> str:
        """Absolute path of a profile path field (or of the .gam / ROM dir)."""
        rel = {"gam": self.gam, "roms": ROMS}.get(name) or getattr(self, name)
        return os.path.join(ROOT, rel)

    def read_gam(self) -> bytes:
        with open(self.path("gam"), "rb") as f:
            return f.read()


def _game(key: str, zh: str, **kw) -> Game:
    d = dict(strings=f"work/{key}.strings.jsonl", gut=f"work/{key}_gut",
             parts=f"translations/{key}/parts", merged=f"translations/{key}.en.jsonl",
             glossary=f"docs/{key}/glossary.jsonl", route=f"routes/{key}.agent.route.jsonl",
             playthrough=f"work/{key}/playthrough", qa=f"work/{key}/qa", en_gam=f"work/{key}_en.gam")
    d.update(kw)
    return Game(key, zh, **d)


XKX_NOTE = (
    "This fan game, written around 2005, has a side area on a \"Japan Island\" built on crude anti-Japanese "
    "jokes: the player spits on and kicks a Japanese official, and refusing ends the game for \"shaming China\". "
    "The jokes come from their moment. In spring 2005 Japan's bid for a permanent UN Security Council seat, "
    "together with Japanese history textbooks that played down wartime atrocities and prime-ministerial visits "
    "to the Yasukuni Shrine, set off mass protests across China, and that anger filled the Chinese teenage "
    "forums this game came from. Behind it lies the memory of Japan's invasion and occupation of China "
    "(1931-1945). The translation keeps these scenes as written but not the slur 小日本 (\"little Japan\"), "
    "which becomes \"the Japanese\". The game also has its teenage authors' swearing and crude humour.")

GAMES: dict[str, Game] = {g.key: g for g in [
    _game("fmj", "伏魔记", engine=engine_text.FMJ, images=_fmj_images,
          title_en="Demonbane Chronicle",
          parts="translations/parts", glossary="docs/glossary.jsonl",
          playthrough="work/playthrough", qa="work/qa"),
    _game("jy", "金庸群侠传", engine=engine_text.JY, images=_jy_images, title_en="Heroes of Jin Yong",
          owner="its authors, BOSS Studio (BOSS工作室)"),
    _game("yxts", "英雄坛说", engine=engine_text.FMJ, images=_yxts_images, title_en="Heroes' Altar",
          owner="its authors, Caizi Studio (才子工作室)"),
    _game("szzm", "十字之门", engine=engine_text.SZZM, images=_szzm_images, title_en="Cross Entry",
          owner="its author, 翼王 (Yiwang)", dialogue_top=59),   # its say box sits 2 px lower
    _game("xkx", "侠客行", engine=engine_text.XKX, images=_xkx_images, title_en="Ode to Gallantry",
          owner="its authors, Chunlan Studio (纯蓝工作室)", content_note=XKX_NOTE),
]}

DEFAULT = "fmj"


def get(key: str | None = None) -> Game:
    key = key or os.environ.get("BBK_GAME") or DEFAULT
    if key not in GAMES:
        raise SystemExit(f"unknown game {key!r}; known: {', '.join(GAMES)}")
    return GAMES[key]


def from_argv(argv: list[str] | None = None) -> Game:
    """Take `--game KEY` (or `--game=KEY`) out of argv and return that game,
    so scripts with their own argument parsing need no change."""
    argv = sys.argv if argv is None else argv
    key = None
    for i, a in enumerate(argv):
        if a == "--game" and i + 1 < len(argv):
            key = argv[i + 1]
            del argv[i:i + 2]
            break
        if a.startswith("--game="):
            key = a.split("=", 1)[1]
            del argv[i]
            break
    return get(key)
