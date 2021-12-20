# -*- coding: utf-8 -*-

from . import d3, d4, d6, d20
from .characters import Adventurer
from random import randint


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
        party = cls(location)
        for _ in range(0, members):
            member = Adventurer.random(d3())
            member.auto_equip()
            party.add(member)
        return party

    @classmethod
    def expert(cls, location: Location, members: int) -> 'Party':
        party = cls(location)
        for _ in range(0, members):
            member = Adventurer.random(d6() + 3)
            member.auto_equip()
            party.add(member)
        return party


class Area:
    pass


class Door(Area):

    def __init__(self, locked: bool = False, stuck: bool = False) -> None:
        self.__locked = locked
        self.__stuck = stuck

    @property
    def locked(self) -> bool:
        return self.__locked

    @property
    def open(self) -> bool:
        if self.locked:
            return False
        return not self.stuck

    @property
    def stuck(self) -> bool:
        return self.__stuck

    # TODO trap?


class Passage(Area):

    def __init__(self, ahead: bool = False, branch: bool = False) -> None:
        self.__ahead = ahead
        self.__branch = branch

    @property
    def ahead(self) -> bool:
        return self.__ahead

    @property
    def branch(self) -> bool:
        return self.__branch


class Room(Area):
    # TODO monster, special, trap, treasure
    pass


class Stairway(Area):

    def __init__(self, down: int = 0, up: int = 0) -> None:
        self.__down = down
        self.__up = up

    @property
    def down(self) -> int:
        return self.__down

    @property
    def up(self) -> int:
        return self.__up


class Dungeon(Location):

    MAXX = 10
    MAXY = 10

    def __init__(self) -> None:
        self.__area = Stairway(up=1)
        self.__flee = False
        self.__lost = False
        self.__x = 1
        self.__y = 1

    @property
    def area(self) -> Area:
        return self.__area

    @property
    def flee(self) -> bool:
        return self.__flee

    @property
    def lost(self) -> bool:
        return self.__lost

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    def actions(self, party: Party) -> list:
        actions = []
        if self.lost:
            actions.append('wander')
        else:
            if self.x > 1:
                actions.append('backtrack')
            if self.x < self.MAXX:
                if isinstance(self.area, Door):
                    if self.area.open:
                        actions.append('advance')
                elif isinstance(self.area, Passage):
                    if self.area.ahead:
                        actions.append('advance')
                else:
                    actions.append('advance')
        if isinstance(self.area, Passage):
            if self.area.branch:
                actions.append('divert')
        if isinstance(self.area, Stairway):
            if self.area.down > 0:
                actions.append('descend')
            if self.area.up > 0:
                actions.append('ascend')
        # TODO flee
        # TODO force (door)
        # TODO listen (door) ???
        # TODO rest
        # TODO search
        # TODO unlock (door) -- key or Lockpicks
        return actions

    def advance(self, party: Party) -> 'Dungeon':
        if 'advance' not in self.actions(party):
            raise RuntimeError('Cannot advance')
        self.__x += 1
        self.__area = self.__discover(next=isinstance(self.area, Door))
        return self

    def ascend(self, party: Party) -> 'Dungeon':
        if 'ascend' not in self.actions(party):
            raise RuntimeError('Cannot ascend')
        if self.y <= 1:
            exit()  # TODO return to town
        self.__area = Stairway(down=1)
        if not self.flee:
            self.__lost = False
        self.__x = self.MAXX
        self.__y -= 1
        return self

    def backtrack(self, party: Party, distance: int = 1) -> 'Dungeon':
        if 'backtrack' not in self.actions(party):
            raise RuntimeError('Cannot backtrack')
        # TODO INT bonus?
        roll = d20()
        if roll < self.x:
            self.__x = roll
            self.__area = self.__discover()
            self.__lost = True
        else:
            self.__x = max(1, self.x - distance)
            self.__area = self.__discover()
        return self

    def descend(self, party: Party) -> 'Dungeon':
        if 'descend' not in self.actions(party):
            raise RuntimeError('Cannot descend')
        self.__area = Stairway(up=1)
        self.__x = randint(1, self.MAXX) if self.lost else 1
        self.__y += 1
        return self

    def divert(self, party: Party) -> 'Dungeon':
        if 'divert' not in self.actions(party):
            raise RuntimeError('Cannot divert')
        self.__area = self.__discover(next=True)
        return self

    def wander(self, party: Party) -> 'Dungeon':
        if 'wander' not in self.actions(party):
            raise RuntimeError('Cannot wander')
        if isinstance(self.area, Passage) and self.area.ahead and not self.area.branch:
            self.__x = randint(1, self.MAXX)
        else:
            self.__x -= 1
        self.__area = self.__discover()
        if self.x <= 1:
            self.__lost = False
        return self

    def __discover(self, next: bool = False) -> Area:
        if self.x <= 1:
            return Stairway(up=1)
        elif self.x < self.MAXX:
            # TODO tunable probabilities
            return self.__discoverArea(d4() if next else d6())
        elif self.y < self.MAXY:
            return Stairway(down=1)
        else:
            return Passage(ahead=False)  #  dead end

    def __discoverArea(self, roll: int) -> Area:
        if roll <= 3:
            return self.__discoverPassage(d6())
        elif roll == 4:
            return Room()
        elif roll == 5:
            return self.__discoverObstacle(d6())
        else:
            return self.__discoverStairway(d6())

    def __discoverPassage(self, roll: int) -> Passage:
        if roll <= 3:
            return Passage(ahead=True)
        elif roll <= 5:
            return Passage(ahead=True, branch=True)
        else:
            return Passage(ahead=False, branch=True)

    def __discoverObstacle(self, roll: int) -> Area:
        if roll <= 2:
            return Door()
        # elif roll <= 4:
        #     return Door(stuck=True)
        # elif roll == 5:
        #     return Door(locked=True)
        else:
            return Passage(ahead=False)  #  dead end

    def __discoverStairway(self, roll: int) -> Stairway:
        if roll <= 4:
            return Stairway(down=1)
        elif roll == 5:
            return Stairway(down=2)
        else:
            return Stairway(up=1)
