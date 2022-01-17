# -*- coding: utf-8 -*-

from . import Area, Location, Party
from ..dice import d4, d6, d20
from random import randint


class Dungeon(Location):

    # TODO door/passage trap?

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
        # TODO 1-2 empty, 1-in-6 treasure
        # TODO 3-4 monster, 3-in-6 treasure
        # TODO 5 special
        # TODO 6 trap, 2-in-6 treasure
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

    # MAXX = 10
    MAXY = 10
    MAXZ = 10

    def __init__(self) -> None:
        self.__area = self.Stairway(up=1)
        self.__flee = False
        self.__lost = False
        # self.__x = 1
        self.__y = 1
        self.__z = 1

    @property
    def area(self) -> Area:
        return self.__area

    @property
    def flee(self) -> bool:
        return self.__flee

    @property
    def lost(self) -> bool:
        return self.__lost

    # @property
    # def x(self) -> int:
    #     return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def z(self) -> int:
        return self.__z

    def actions(self, party: Party) -> list:
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

    def back(self, party: Party, distance: int = 1) -> Location:
        if 'back' not in self.actions(party):
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

    def down(self, party: Party) -> Location:
        if 'down' not in self.actions(party):
            raise RuntimeError('Cannot descend')
        self.__area = self.Stairway(up=1)
        self.__y = randint(1, self.MAXY) if self.lost else 1
        self.__z += 1
        return self

    def forth(self, party: Party) -> Location:
        if 'forth' not in self.actions(party):
            raise RuntimeError('Cannot advance')
        self.__y += 1
        self.__area = self.__discover(next=isinstance(self.area, self.Door))
        return self

    def side(self, party: Party) -> Location:
        if 'side' not in self.actions(party):
            raise RuntimeError('Cannot divert')
        self.__area = self.__discover(next=True)
        return self

    def up(self, party: Party) -> Location:
        if 'up' not in self.actions(party):
            raise RuntimeError('Cannot ascend')
        if self.z <= 1:
            # TODO return to town
            exit()
        self.__area = self.Stairway(down=1)
        if not self.flee:
            self.__lost = False
        self.__y = self.MAXY
        self.__z -= 1
        return self

    def wander(self, party: Party) -> Location:
        if 'wander' not in self.actions(party):
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
            return self.Stairway(up=1)
        elif self.y < self.MAXY:
            # TODO tunable probabilities
            return self.__discoverArea(d4() if next else d6())
        elif self.z < self.MAXZ:
            return self.Stairway(down=1)
        else:
            return self.Passage(ahead=False)  #  dead end

    def __discoverArea(self, roll: int) -> Area:
        if roll <= 3:
            return self.__discoverPassage(d6())
        elif roll == 4:
            return self.Room()
        elif roll == 5:
            return self.__discoverObstacle(d6())
        else:
            return self.__discoverStairway(d6())

    def __discoverPassage(self, roll: int) -> Passage:
        if roll <= 3:
            return self.Passage(ahead=True)
        elif roll <= 5:
            return self.Passage(ahead=True, branch=True)
        else:
            return self.Passage(ahead=False, branch=True)

    def __discoverObstacle(self, roll: int) -> Area:
        if roll <= 2:
            return self.Door()
        # elif roll <= 4:
        #     return self.Door(stuck=True)
        # elif roll == 5:
        #     return self.Door(locked=True)
        else:
            return self.Passage(ahead=False)  #  dead end

    def __discoverStairway(self, roll: int) -> Stairway:
        if roll <= 4:
            return self.Stairway(down=1)
        elif roll == 5:
            return self.Stairway(down=2)
        else:
            return self.Stairway(up=1)
