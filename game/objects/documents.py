# -*- coding: utf-8 -*-

from . import DualHanded, Holdable, Stowable
from .. import Entity
from ..scripts import Script
from .containers import Container


class ScriptContainer(Entity, Container[Script]):

    def __init__(self) -> None:
        Entity.__init__(self)
        Container.__init__(self)


class Codex(ScriptContainer, DualHanded, Stowable):
    CAPACITY = 24


class Scroll(ScriptContainer, Holdable, Stowable):
    CAPACITY = 3
