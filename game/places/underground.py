# -*- coding: utf-8 -*-

from .. import Place
from ..creatures import Unit, animals, humans, monsters, mutants
from ..creatures.adventurers import Party
from ..dice import d3, d4, d6, d8, d10, d20
from ..objects import Quantifiable, containers, valuables
from random import choice, randint, random
from typing import Callable


class Dungeon(Place):

    # TODO door/passage trap?
    # TODO flee
    # TODO rest
    # TODO search

    class Area(Place):

        def __init__(self, dungeon: 'Dungeon', y: int, z: int) -> None:
            super().__init__(dungeon)
            self.__y = y
            self.__z = z

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

        def actions(self, party: Party) -> dict[str, Callable]:
            actions = {}
            if party.lost:
                actions['wander'] = lambda: self.wander(party)
            elif self.y > 1:
                actions['back'] = lambda: self.back(party)
            return actions

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

    class DeadEnd(Area):
        pass

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

        def actions(self, party: Party) -> dict[str, Callable]:
            actions = super().actions(party)
            if self.open:
                actions['next'] = lambda: self.next(party)
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

        def actions(self, party: Party) -> dict[str, Callable]:
            actions = super().actions(party)
            if self.ahead and not party.lost:
                actions['next'] = lambda: self.next(party)
            if self.branch:
                actions['turn'] = lambda: self.turn(party)
            return actions

        def turn(self, party: Party) -> None:
            if 'turn' not in self.actions(party):
                raise RuntimeError('Cannot turn')
            area = self.location.discover(self, self.y, True)
            party.move(area)

    class Room(Area):

        def actions(self, party: Party) -> dict[str, Callable]:
            actions = super().actions(party)
            if self.y < self.location.MAXY and not party.lost:
                actions['next'] = lambda: self.next(party)
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

        def actions(self, party: Party) -> dict[str, Callable]:
            actions = super().actions(party)
            if self.ascend:
                actions['up'] = lambda: self.up(party)
            if self.descend:
                actions['down'] = lambda: self.down(party)
            if self.y < self.location.MAXY and not party.lost:
                actions['next'] = lambda: self.next(party)
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
        (mutants.FireBeetle, 1*d8),
        # (demihumans.Dwarf, 1*d6),
        # (demihumans.Gnome, 1*d6),
        # (demihumans.Goblin, 2*d4),
        (monsters.GreenSlime, 1*d4),
        # (demihumans.Halfling, 3*d6),
        (mutants.KillerBee, 3*d6),
        # (demihumans.Kobold, 4*d4),
        (mutants.Gecko, 1*d3),
        # (demihumans.Orc, 2*d4),
        (mutants.Shrew, 1*d10),
        # (Skeleton, 3*d4),
        (animals.Cobra, 1*d6),
        (mutants.CrabSpider, 1*d4),
        # (demihumans.Sprite, 3*d6),
        (monsters.Stirge, 1*d10),
        (humans.Trader, 1*d8),
        (animals.Wolf, 2*d6),
    ]

    ROOM_TREASURE_LV1 = [
        (1.00, {valuables.Silver: 1*d6 * 100}),
        (0.50, {valuables.Gold: 1*d6 * 10}),
        # TODO (0.05, {valuables.Gems: 1*d6}), -- types
        (0.02, {valuables.Jewellery: 1*d6}),
        # TODO (0.02, {valuables.SpecialItem: 1}),
    ]

    MAXY = 10
    MAXZ = 10

    def __init__(self, location: Place) -> None:
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
            return self.DeadEnd(self, y, area.z)

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
            return self.DeadEnd(self, y, z)

    def __discoverRoom(self, y: int, z: int, roll: int) -> Room:
        if roll <= 2:
            room = self.Room(self, y, z)
            if d6() <= 1:
                room.add(self.__randomTreasure(room))
        elif roll <= 4:
            room = self.Room(self, y, z)
            room.add(self.__randomEncounter(room))
            # TODO 3-in-6 treasure based on encounter TT
        elif roll <= 5:
            room = self.Room(self, y, z)
            # TODO special
        else:
            room = self.Room(self, y, z)
            # TODO trap
            if d6() <= 2:
                room.add(self.__randomTreasure(room))
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
        return creature_type.encounter(location, sum(number_appearing))

    def __randomTreasure(self, location: Area) -> containers.Pile:
        pile = containers.Pile()
        # TODO room treature by level
        for chance, items in self.ROOM_TREASURE_LV1:
            if chance == 1 or random() <= chance:
                for item_type, quantity in items.items():
                    if issubclass(item_type, Quantifiable):
                        pile.add(item_type(sum(quantity)))
                    else:
                        for _ in range(0, sum(quantity)):
                            pile.add(item_type())
        return pile
