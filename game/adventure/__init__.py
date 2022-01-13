# -*- coding: utf-8 -*-

from ..creatures.adventurers import Adventurer
from datetime import datetime
from random import choice


class Location:

    def actions(self, party: 'Party') -> list:
        return []


class Party:

    def __init__(self, location: Location) -> None:
        self.__location = location
        # TODO marching order
        self.__members = []

    @property
    def location(self) -> Location:
        return self.__location

    @property
    def members(self) -> list[Adventurer]:
        return self.__members.copy()

    def add(self, member: Adventurer) -> None:
        self.__members.append(member)

    def remove(self, member: Adventurer) -> None:
        self.__members.remove(member)

    @classmethod
    def basic(cls, location: Location, members: int) -> 'Party':
        return cls.random(range(1, 4), location, members)

    @classmethod
    def expert(cls, location: Location, members: int) -> 'Party':
        return cls.random(range(4, 10), location, members)

    @classmethod
    def funnel(cls, location: Location, members: int) -> 'Party':
        return cls.random(range(0, 1), location, members)

    @classmethod
    def random(cls, levels: range, location: Location, members: int) -> 'Party':
        party = cls(location)
        for _ in range(0, members):
            member = Adventurer.random(choice(levels))
            member.auto_equip()
            party.add(member)
        return party


class World:

    EPOCH = datetime(1001, 1, 1, 0, 0)

    def __init__(self, party: Party, time: datetime = EPOCH) -> None:
        self.__party = party
        self.__time = time

    @property
    def party(self) -> Party:
        return self.__party

    @property
    def time(self) -> datetime:
        return self.__time