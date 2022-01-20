# -*- coding: utf-8 -*-

from .. import Place
from ..creatures import Creature
from ..creatures.adventurers import Adventurer


class Area:

    def __init__(self, contents: list = []) -> None:
        self.__contents = contents

    @property
    def content(self) -> list:
        return self.__contents

# TODO Region


class Site(Place):
    pass


class Party:

    # TODO marching order

    def __init__(self, place: Place, members: list[Creature] = []) -> None:
        self.__place = place
        self.__members = members

    @property
    def place(self) -> Place:
        return self.__place

    @property
    def members(self) -> list[Creature]:
        return self.__members.copy()

    def add(self, member: Creature) -> None:
        self.__members.append(member)

    def remove(self, member: Creature) -> None:
        self.__members.remove(member)
