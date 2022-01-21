# -*- coding: utf-8 -*-

from .. import Location
from ..creatures import Unit, animals, humans, monsters, mutants
from ..creatures.adventurers import Party
from ..dice import d3, d4, d6, d8, d10, d20
from random import choice, randint


class Dungeon(Location):

    # TODO door/passage trap?
    # TODO flee
    # TODO rest
    # TODO search

    class Area(Location):

        def __init__(self, dungeon: 'Dungeon', y: int, z: int) -> None:
            super().__init__(dungeon)
            self.__contents = []
            self.__y = y
            self.__z = z

        @property
        def contents(self) -> list:
            return self.__contents.copy()

        @property
        def location(self) -> 'Dungeon':
            location = super().location
            if isinstance(location, Dungeon):
                return location
            raise TypeError()

        @property
        def y(self) -> int:
            return self.__y

        @property
        def z(self) -> int:
            return self.__z

        def actions(self, party: Party) -> set:
            actions = set()
            if party.lost:
                actions.add('wander')
            elif self.y > 1:
                actions.add('back')
            return actions

        def add(self, item) -> None:
            self.__contents.append(item)

        def back(self, party: Party, distance: int = 1) -> None:
            if 'back' not in self.actions(party):
                raise RuntimeError('Cannot backtrack')
            # TODO INT bonus?
            roll = d20()
            if roll < self.y:
                party.lost = True
                area = self.location.discover(self, roll)
            else:
                area = self.location.discover(self, max(1, self.y - distance))
            party.move(area)

        def next(self, party: Party) -> None:
            if 'next' not in self.actions(party):
                raise RuntimeError('Cannot advance')
            area = self.location.discover(self, self.y + 1)
            party.move(area)

        def wander(self, party: Party) -> None:
            if 'wander' not in self.actions(party):
                raise RuntimeError('Cannot wander')
            if isinstance(self, Dungeon.Passage) and self.ahead and not self.branch:
                y = randint(1, self.location.MAXY)
            else:
                y = self.y - 1
            area = self.location.discover(self, y)
            # TODO should depend on the level where they got lost
            if y <= 1:
                party.lost = False
            party.move(area)

    class Door(Area):

        def __init__(self, dungeon: 'Dungeon', y: int, z: int, locked: bool = False, stuck: bool = False) -> None:
            super().__init__(dungeon, y, z)
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

        def actions(self, party: Party) -> set:
            actions = super().actions(party)
            if self.open:
                actions.add('next')
            return actions

        def next(self, party: Party) -> None:
            if 'next' not in self.actions(party):
                raise RuntimeError('Cannot next')
            area = self.location.discover(self, self.y, True)
            party.move(area)

        # TODO force
        # TODO listen ???
        # TODO unlock -- key or Lockpicks

    class Passage(Area):

        def __init__(self, dungeon: 'Dungeon', y: int, z: int, ahead: bool = False, branch: bool = False) -> None:
            super().__init__(dungeon, y, z)
            self.__ahead = ahead
            self.__branch = branch

        @property
        def ahead(self) -> bool:
            return self.__ahead

        @property
        def branch(self) -> bool:
            return self.__branch

        def actions(self, party: Party) -> set:
            actions = super().actions(party)
            if self.ahead and not party.lost:
                actions.add('next')
            if self.branch:
                actions.add('turn')
            return actions

        def turn(self, party: Party) -> None:
            if 'turn' not in self.actions(party):
                raise RuntimeError('Cannot turn')
            area = self.location.discover(self, self.y, True)
            party.move(area)

    class Room(Area):

        def actions(self, party: Party) -> set:
            actions = super().actions(party)
            if self.y < self.location.MAXY and not party.lost:
                actions.add('next')
            return actions

    class Stairway(Area):

        def __init__(self, dungeon: 'Dungeon', y: int, z: int, ascend: int = 0, descend: int = 0) -> None:
            super().__init__(dungeon, y, z)
            self.__ascend = ascend
            self.__descend = descend

        @property
        def ascend(self) -> int:
            return self.__ascend

        @property
        def descend(self) -> int:
            return self.__descend

        def actions(self, party: Party) -> set:
            actions = super().actions(party)
            if self.ascend:
                actions.add('up')
            if self.descend:
                actions.add('down')
            if self.y < self.location.MAXY and not party.lost:
                actions.add('next')
            return actions

        def down(self, party: Party) -> None:
            if 'down' not in self.actions(party):
                raise RuntimeError('Cannot descend')
            y = randint(1, self.location.MAXY) if party.lost else 1
            z = self.z + self.descend
            area = Dungeon.Stairway(self.location, y, z, ascend=self.descend)
            party.move(area)

        def up(self, party: Party) -> None:
            if 'up' not in self.actions(party):
                raise RuntimeError('Cannot ascend')
            if self.z <= 1:
                # TODO return to town/wilderness
                exit()
            area = Dungeon.Stairway(
                self.location,
                self.location.MAXY,
                self.z - self.ascend,
                descend=self.ascend,
            )
            if not party.flee:
                party.lost = False
            party.move(area)

    ENCOUNTERS_LV1 = [
        (humans.Acolyte, 1*d8),
        (humans.Bandit, 1*d8),
        (mutants.GiantFireBeetle, 1*d8),
        # (demihumans.Dwarf, 1*d6),
        # (demihumans.Gnome, 1*d6),
        # (demihumans.Goblin, 2*d4),
        (monsters.GreenSlime, 1*d4),
        # (demihumans.Halfling, 3*d6),
        (mutants.GiantKillerBee, 3*d6),
        # (demihumans.Kobold, 4*d4),
        (mutants.GiantGecko, 1*d3),
        # (demihumans.Orc, 2*d4),
        (mutants.GiantShrew, 1*d10),
        # (Skeleton, 3*d4),
        (animals.SpittingCobra, 1*d6),
        (mutants.GiantCrabSpider, 1*d4),
        # (demihumans.Sprite, 3*d6),
        (monsters.Stirge, 1*d10),
        (humans.Trader, 1*d8),
        (animals.Wolf, 2*d6),
    ]

    MAXY = 10
    MAXZ = 10

    def __init__(self, location: Location) -> None:
        super().__init__(location)
        self.__entrance = self.Stairway(self, 1, 1, ascend=1)

    @property
    def entrance(self) -> Area:
        return self.__entrance

    def discover(self, area: Area, y: int, limit: bool = False) -> Area:
        if y <= 1:
            return self.Stairway(self, y, area.z, ascend=1)
        elif y < self.MAXY:
            # TODO tunable probabilities
            return self.__discoverArea(y, area.z, d4() if limit else d6())
        elif area.z < self.MAXZ:
            return self.Stairway(self, y, area.z, descend=1)
        else:
            return self.Passage(self, y, area.z, ahead=False)  #  dead end

    def __discoverArea(self, y: int, z: int, roll: int) -> Area:
        if roll <= 3:
            return self.__discoverPassage(y, z, d6())
        elif roll == 4:
            return self.__discoverRoom(y, z, d6())
        elif roll == 5:
            return self.__discoverObstacle(y, z, d6())
        else:
            return self.__discoverStairway(y, z, d6())

    def __discoverPassage(self, y: int, z: int, roll: int) -> Passage:
        if roll <= 3:
            return self.Passage(self, y, z, ahead=True)
        elif roll <= 5:
            return self.Passage(self, y, z, ahead=True, branch=True)
        else:
            return self.Passage(self, y, z, ahead=False, branch=True)

    def __discoverObstacle(self, y: int, z: int, roll: int) -> Area:
        if roll <= 2:
            return self.Door(self, y, z)
        # elif roll <= 4:
        #     return self.Door(self, y, z, stuck=True)
        # elif roll == 5:
        #     return self.Door(self, y, z, locked=True)
        else:
            return self.Passage(self, y, z, ahead=False)  #  dead end

    def __discoverRoom(self, y: int, z: int, roll: int) -> Room:
        if roll <= 2:
            room = self.Room(self, y, z)
            # TODO 1-in-6 treasure
        elif roll <= 4:
            room = self.Room(self, y, z)
            room.add(self.__randomEncounter(room))
            # TODO 3-in-6 treasure
        elif roll <= 5:
            room = self.Room(self, y, z)
            # TODO special
        else:
            room = self.Room(self, y, z)
            # TODO trap
            # TODO 2-in-6 treasure
        return room

    def __discoverStairway(self, y: int, z: int, roll: int) -> Stairway:
        if roll <= 4:
            return self.Stairway(self, y, z, descend=1)
        elif roll == 5:
            return self.Stairway(self, y, z, descend=2)
        else:
            return self.Stairway(self, y, z, ascend=1)

    def __randomEncounter(self, location: Area) -> Unit:
        # TODO encounters by level
        creature_type, number_appearing = choice(self.ENCOUNTERS_LV1)
        return creature_type.encounter(sum(number_appearing), location)
