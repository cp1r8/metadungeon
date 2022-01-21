# -*- coding: utf-8 -*-

from datetime import datetime, timedelta


class Actor:
    pass


class Location:

    def __init__(self, location: 'Location') -> None:
        self.__location = location

    @property
    def location(self) -> 'Location':
        return self.__location

    def actions(self, actor: Actor) -> set:
        return set()


class World(Location):

    EPOCH = datetime(1001, 1, 1, 0, 0)

    def __init__(self, moment: datetime = EPOCH) -> None:
        super().__init__(self)
        self.__moment = moment

    @property
    def moment(self) -> datetime:
        return self.__moment

    def advance(self, **kwargs) -> None:
        self.__moment += timedelta(**kwargs)
