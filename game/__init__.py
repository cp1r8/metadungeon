# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from typing import Callable, Optional

import itertools


class Entity:

    __identity = itertools.count(1)
    __id_max = 0
    __index = {}

    def __init__(self) -> None:
        self.__id = next(Entity.__identity)
        self.__index[self.id] = self

    @property
    def id(self) -> int:
        return self.__id

    def __setstate__(self, state):
        self.__dict__.update(state)
        if self.id > Entity.__id_max:
            Entity.__id_max = self.id
            Entity.__identity = itertools.count(self.id + 1)
        self.__index[self.id] = self

    def __str__(self) -> str:
        return f"{type(self).__name__}:{self.id:06X}"

    def actions(self, actor: 'Entity') -> dict[str, Callable]:
        return {}

    @classmethod
    def find(cls, id: int) -> Optional['Entity']:
        return cls.__index.get(id)


class Motile(Entity):

    def __init__(self, location: 'Place') -> None:
        super().__init__()
        self.__location = location

    @property
    def location(self) -> 'Place':
        return self.__location

    def move(self, location: 'Place') -> None:
        self.__location.remove(self)
        self.__location = location
        self.__location.add(self)


class Place(Motile):

    def __init__(self, location: 'Place') -> None:
        super().__init__(location)
        self.__entities = set()

    @property
    def entities(self) -> set[Entity]:
        return self.__entities.copy()

    def add(self, entity: Entity) -> None:
        self.__entities.add(entity)

    def remove(self, entity: Entity) -> None:
        self.__entities.remove(entity)


class World(Place):

    EPOCH = datetime(1, 1, 1, 0, 0)

    def __init__(self, now: datetime = EPOCH) -> None:
        super().__init__(self)
        self.__now = now

    @property
    def now(self) -> datetime:
        return self.__now

    def age(self, **kwargs) -> None:
        self.__now += timedelta(**kwargs)
