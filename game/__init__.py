# -*- coding: utf-8 -*-

from datetime import datetime


class Place:

    def __init__(self, place: 'Place') -> None:
        self.__place = place

    @property
    def place(self) -> 'Place':
        return self.__place

    def actions(self) -> list:
        return []


class World(Place):

    EPOCH = datetime(1001, 1, 1, 0, 0)

    def __init__(self, time: datetime = EPOCH) -> None:
        super().__init__(self)
        self.__time = time

    @property
    def time(self) -> datetime:
        return self.__time
