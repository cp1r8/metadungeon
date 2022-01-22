# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from typing import Callable

import itertools


class Entity:

    __identity = itertools.count(1)
    __last_id = 0

    def __init__(self) -> None:
        self.__id = next(Entity.__identity)

    @property
    def id(self) -> int:
        return self.__id

    def __setstate__(self, state):
        self.__dict__.update(state)
        if self.id > Entity.__last_id:
            Entity.__last_id = self.id
            Entity.__identity = itertools.count(self.id + 1)

    def __str__(self) -> str:
        if hasattr(self, 'name'):
            return getattr(self, 'name')
        if hasattr(self, 'handle'):
            return getattr(self, 'handle')
        return f"{type(self).__name__}-{self.id:04X}"

    def actions(self, actor: 'Entity') -> dict[str, Callable]:
        return {}


class Location(Entity):

    def __init__(self, location: 'Location') -> None:
        super().__init__()
        self.__contents = []
        self.__location = location

    @property
    def contents(self) -> list[Entity]:
        return self.__contents.copy()

    @property
    def location(self) -> 'Location':
        return self.__location

    def add(self, entity: Entity) -> None:
        self.__contents.append(entity)

    def remove(self, entity: Entity) -> None:
        self.__contents.remove(entity)


class World(Location):

    EPOCH = datetime(1001, 1, 1, 0, 0)

    def __init__(self, now: datetime = EPOCH) -> None:
        super().__init__(self)
        self.__now = now

    @property
    def now(self) -> datetime:
        return self.__now

    def advance(self, **kwargs) -> None:
        self.__now += timedelta(**kwargs)
