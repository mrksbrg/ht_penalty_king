"""Tiny runtime holder for the active language pack."""

from __future__ import annotations

import importlib


class _Lang:
    def __init__(self) -> None:
        self.code = "sv"
        self.name = "Svenska"
        self.S: dict = {}
        self.SKILLS: list = []

    def use(self, code: str) -> None:
        mod = importlib.import_module(f"{__package__}.languages.{code}")
        self.code = code
        self.name = getattr(mod, "NAME", code)
        self.S = mod.STRINGS
        self.SKILLS = mod.SKILL_LEVELS

    def skill(self, level: int) -> str:
        """Hattrick denomination for a skill level (e.g. 13 -> 'världsklass')."""
        if not self.SKILLS:
            return str(level)
        if level < 0:
            level = 0
        return self.SKILLS[min(level, len(self.SKILLS) - 1)]

    def ui(self, key: str, **kw) -> str:
        txt = self.S["ui"].get(key, key)
        return txt.format(**kw) if kw else txt


LANG = _Lang()
LANG.use("sv")  # default
