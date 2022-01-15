# -*- coding: utf-8 -*-

from ..creatures import Creature
from ..creatures.adventurers import Adventurer
from ..dice import d3, d6
from datetime import datetime
from random import choice


class Location:

    def actions(self, party: 'Party') -> list:
        return []


class Party:

    def __init__(self, location: Location, members: list[Creature] = []) -> None:
        self.__location = location
        # TODO marching order
        self.__members = members

    @property
    def location(self) -> Location:
        return self.__location

    @property
    def members(self) -> list[Creature]:
        return self.__members.copy()

    def add(self, member: Creature) -> None:
        self.__members.append(member)

    def remove(self, member: Creature) -> None:
        self.__members.remove(member)


class World:

    EPOCH = datetime(1001, 1, 1, 0, 0)

    def __init__(self, time: datetime = EPOCH) -> None:
        self.__parties = []
        self.__time = time

    @property
    def parties(self) -> list[Party]:
        return self.__parties.copy()

    @property
    def time(self) -> datetime:
        return self.__time

    def assemble(self, location: Location, members: list[Creature]) -> Party:
        party = Party(location, members)
        self.__parties.append(party)
        return party

    def basic_party(self, location: Location, members: int, auto_equip: bool = True) -> Party:
        return self.assemble(location, [
            Adventurer.random(d3(), auto_equip) for _ in range(0, members)
        ])

    def disband(self, party: Party) -> None:
        self.parties.remove(party)

    def funnel_party(self, location: Location, members: int, auto_equip: bool = True) -> Party:
        return self.assemble(location, [
            Adventurer.random(0, auto_equip) for _ in range(0, members)
        ])

    def expert_party(self, location: Location, members: int, auto_equip: bool = True) -> Party:
        return self.assemble(location, [
            Adventurer.random(d6() + 3, auto_equip) for _ in range(0, members)
        ])
