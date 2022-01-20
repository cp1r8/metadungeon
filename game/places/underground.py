# -*- coding: utf-8 -*-

from .. import Place
from ..creatures import Creature, animals, humans, monsters, mutants
from ..dice import d3, d4, d6, d8, d10, d20
from random import choice, randint


class Dungeon(Place):

    # TODO door/passage trap?

    class Area(Place):

        def __init__(self, dungeon: 'Dungeon', contents: list = []) -> None:
            super().__init__(dungeon)
            self.__contents = contents

        @property
        def contents(self) -> list:
            return self.__contents.copy()

    class Door(Area):

        def __init__(self, dungeon: 'Dungeon', locked: bool = False, stuck: bool = False) -> None:
            super().__init__(dungeon)
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

        def __init__(self, dungeon: 'Dungeon', ahead: bool = False, branch: bool = False) -> None:
            super().__init__(dungeon)
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

        def __init__(self, dungeon: 'Dungeon', down: int = 0, up: int = 0) -> None:
            super().__init__(dungeon)
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
        self.__area = self.Stairway(self, up=1)
        self.__lost = False
        self.__y = 1
        self.__z = 1

    @property
    def area(self) -> Area:
        return self.__area

    @property
    def lost(self) -> bool:
        return self.__lost

    @property
    def y(self) -> int:
        return self.__y

    @property
    def z(self) -> int:
        return self.__z

    def actions(self) -> list:
        actions = []
        if self.lost:
            actions.append('wander')
        else:
            if self.y > 1:
                actions.append('back')
            if self.y < self.MAXY:
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
        if roll < self.y:
            self.__y = roll
            self.__area = self.__discover()
            self.__lost = True
        else:
            self.__y = max(1, self.y - distance)
            self.__area = self.__discover()
        return self

    def down(self) -> Place:
        if 'down' not in self.actions():
            raise RuntimeError('Cannot descend')
        self.__area = self.Stairway(self, up=1)
        self.__y = randint(1, self.MAXY) if self.lost else 1
        self.__z += 1
        return self

    def forth(self) -> Place:
        if 'forth' not in self.actions():
            raise RuntimeError('Cannot advance')
        self.__y += 1
        self.__area = self.__discover(next=isinstance(self.area, self.Door))
        return self

    def side(self) -> Place:
        if 'side' not in self.actions():
            raise RuntimeError('Cannot divert')
        self.__area = self.__discover(next=True)
        return self

    def up(self) -> Place:
        if 'up' not in self.actions():
            raise RuntimeError('Cannot ascend')
        if self.z <= 1:
            # TODO return to town
            exit()
        self.__area = self.Stairway(self, down=1)
        # if not self.flee:
        #     self.__lost = False
        self.__y = self.MAXY
        self.__z -= 1
        return self

    def wander(self) -> Place:
        if 'wander' not in self.actions():
            raise RuntimeError('Cannot wander')
        if isinstance(self.area, self.Passage) and self.area.ahead and not self.area.branch:
            self.__y = randint(1, self.MAXY)
        else:
            self.__y -= 1
        self.__area = self.__discover()
        if self.y <= 1:
            self.__lost = False
        return self

    def __discover(self, next: bool = False) -> Area:
        if self.y <= 1:
            return self.Stairway(self, up=1)
        elif self.y < self.MAXY:
            # TODO tunable probabilities
            return self.__discoverArea(d4() if next else d6())
        elif self.z < self.MAXZ:
            return self.Stairway(self, down=1)
        else:
            return self.Passage(self, ahead=False)  #  dead end

    def __discoverArea(self, roll: int) -> Area:
        if roll <= 3:
            return self.__discoverPassage(d6())
        elif roll == 4:
            return self.__discoverRoom(d6())
        elif roll == 5:
            return self.__discoverObstacle(d6())
        else:
            return self.__discoverStairway(d6())

    def __discoverPassage(self, roll: int) -> Passage:
        if roll <= 3:
            return self.Passage(self, ahead=True)
        elif roll <= 5:
            return self.Passage(self, ahead=True, branch=True)
        else:
            return self.Passage(self, ahead=False, branch=True)

    def __discoverObstacle(self, roll: int) -> Area:
        if roll <= 2:
            return self.Door(self)
        # elif roll <= 4:
        #     return self.Door(self, stuck=True)
        # elif roll == 5:
        #     return self.Door(self, locked=True)
        else:
            return self.Passage(self, ahead=False)  #  dead end

    def __discoverRoom(self, roll: int) -> Room:
        if roll <= 2:
            # TODO 1-in-6 treasure
            content = []
        elif roll <= 4:
            # TODO 3-in-6 treasure
            content = self.__randomEncounter()
        elif roll <= 5:
            # TODO special
            content = []
        else:
            # TODO trap
            # TODO 2-in-6 treasure
            content = []
        return self.Room(self, content)

    def __discoverStairway(self, roll: int) -> Stairway:
        if roll <= 4:
            return self.Stairway(self, down=1)
        elif roll == 5:
            return self.Stairway(self, down=2)
        else:
            return self.Stairway(self, up=1)

    def __randomEncounter(self) -> list[Creature]:
        # TODO encounters by level
        creature_type, number_appearing = choice(self.ENCOUNTERS_LV1)
        return creature_type.encounter(sum(number_appearing))
