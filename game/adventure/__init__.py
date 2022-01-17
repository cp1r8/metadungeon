# -*- coding: utf-8 -*-

from ..creatures import Creature
from ..creatures.adventurers import Adventurer
from datetime import datetime


class Area:

    def __init__(self, contents: list = []) -> None:
        self.__contents = contents

    @property
    def content(self) -> list:
        return self.__contents


class Location:

    def actions(self, party: 'Party') -> list:
        return []


class Party:

    # TODO marching order

    def __init__(self, location: Location, members: list[Creature] = []) -> None:
        self.__location = location
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
        self.__locations = []
        self.__parties = []
        self.__time = time

    @property
    def locations(self) -> list[Location]:
        return self.__locations.copy()

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

    def disband(self, party: Party) -> None:
        self.__parties.remove(party)

    def establish(self, location: Location) -> None:
        self.__locations.append(location)
