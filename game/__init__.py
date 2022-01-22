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
        if hasattr(self, 'name'):
            return getattr(self, 'name')
        if hasattr(self, 'handle'):
            return getattr(self, 'handle')
        return f"{type(self).__name__}.{self.id:04X}"

    def actions(self, actor: 'Entity') -> dict[str, Callable]:
        return {}

    @classmethod
    def find(cls, id: int) -> Optional['Entity']:
        return cls.__index.get(id)


class Location(Entity):

    def __init__(self, location: 'Location') -> None:
        super().__init__()
        self.__entities = []
        self.__location = location

    @property
    def entities(self) -> list[Entity]:
        return self.__entities.copy()

    @property
    def location(self) -> 'Location':
        return self.__location

    def add(self, entity: Entity) -> None:
        self.__entities.append(entity)

    def remove(self, entity: Entity) -> None:
        self.__entities.remove(entity)


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
