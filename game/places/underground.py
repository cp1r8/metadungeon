# -*- coding: utf-8 -*-

from .. import Place
from ..creatures import Unit, animals, humans, monsters, mutants
from ..dice import d3, d4, d6, d8, d10, d20
from random import choice, randint


class Dungeon(Place):

    # TODO door/passage trap?

    class Area(Place):

        def __init__(self, dungeon: 'Dungeon', y: int, z: int) -> None:
            super().__init__(dungeon)
            self.__contents = []
            self.__y = y
            self.__z = z

        @property
        def contents(self) -> list:
            return self.__contents.copy()

        @property
        def place(self) -> 'Dungeon':
            place = super().place
            if isinstance(place, Dungeon):
                return place
            raise TypeError()

        @property
        def y(self) -> int:
            return self.__y

        @property
        def z(self) -> int:
            return self.__z

        def add(self, item) -> None:
            self.__contents.append(item)

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

    class Room(Area):
        pass

    class Stairway(Area):

        def __init__(self, dungeon: 'Dungeon', y: int, z: int, down: int = 0, up: int = 0) -> None:
            super().__init__(dungeon, y, z)
            self.__down = down
            self.__up = up

        @property
        def down(self) -> int:
            return self.__down

        @property
        def up(self) -> int:
            return self.__up

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

    def __init__(self, place: Place) -> None:
        super().__init__(place)
        self.__area = self.Stairway(self, 1, 1, up=1)
        self.__lost = False

    @property
    def area(self) -> Area:
        return self.__area

    @property
    def lost(self) -> bool:
        return self.__lost

    def actions(self) -> list:
        actions = []
        if self.lost:
            actions.append('wander')
        else:
            if self.area.y > 1:
                actions.append('back')
            if self.area.y < self.MAXY:
                if isinstance(self.area, self.Door):
                    if self.area.open:
                        actions.append('forth')
                elif isinstance(self.area, self.Passage):
                    if self.area.ahead:
                        actions.append('forth')
                else:
                    actions.append('forth')
        if isinstance(self.area, self.Passage):
            if self.area.branch:
                actions.append('side')
        if isinstance(self.area, self.Stairway):
            if self.area.down > 0:
                actions.append('down')
            if self.area.up > 0:
                actions.append('up')
        # TODO flee
        # TODO force (door)
        # TODO listen (door) ???
        # TODO rest
        # TODO search
        # TODO unlock (door) -- key or Lockpicks
        return actions

    def back(self, distance: int = 1) -> Place:
        if 'back' not in self.actions():
            raise RuntimeError('Cannot backtrack')
        # TODO INT bonus?
        roll = d20()
        if roll < self.area.y:
            self.__area = self.__discover(roll, self.area.z)
            self.__lost = True
        else:
            self.__area = self.__discover(
                max(1, self.area.y - distance),
                self.area.z,
            )
        return self

    def down(self) -> Place:
        if 'down' not in self.actions():
            raise RuntimeError('Cannot descend')
        y = randint(1, self.MAXY) if self.lost else 1
        z = self.area.z + 1
        self.__area = self.Stairway(self, y, z, up=1)
        return self

    def forth(self) -> Place:
        if 'forth' not in self.actions():
            raise RuntimeError('Cannot advance')
        self.__area = self.__discover(
            self.area.y + 1,
            self.area.z,
            next=isinstance(self.area, self.Door),
        )
        return self

    def side(self) -> Place:
        if 'side' not in self.actions():
            raise RuntimeError('Cannot divert')
        self.__area = self.__discover(self.area.y, self.area.z, next=True)
        return self

    def up(self) -> Place:
        if 'up' not in self.actions():
            raise RuntimeError('Cannot ascend')
        if self.area.z <= 1:
            # TODO return to town
            exit()
        self.__area = self.Stairway(self, self.MAXY, self.area.z - 1, down=1)
        # if not self.flee:
        #     self.__lost = False
        return self

    def wander(self) -> Place:
        if 'wander' not in self.actions():
            raise RuntimeError('Cannot wander')
        if isinstance(self.area, self.Passage) and self.area.ahead and not self.area.branch:
            y = randint(1, self.MAXY)
        else:
            y = self.area.y - 1
        self.__area = self.__discover(y, self.area.z)
        # TODO should on level where they got lost
        if y <= 1:
            self.__lost = False
        return self

    def __discover(self, y: int, z: int, next: bool = False) -> Area:
        if self.area.y <= 1:
            return self.Stairway(self, y, z, up=1)
        elif self.area.y < self.MAXY:
            # TODO tunable probabilities
            return self.__discoverArea(y, z, d4() if next else d6())
        elif self.area.z < self.MAXZ:
            return self.Stairway(self, y, z, down=1)
        else:
            return self.Passage(self, y, z, ahead=False)  #  dead end

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
            return self.Stairway(self, y, z, down=1)
        elif roll == 5:
            return self.Stairway(self, y, z, down=2)
        else:
            return self.Stairway(self, y, z, up=1)

    def __randomEncounter(self, place: Place) -> Unit:
        # TODO encounters by level
        creature_type, number_appearing = choice(self.ENCOUNTERS_LV1)
        return creature_type.encounter(sum(number_appearing), place)
