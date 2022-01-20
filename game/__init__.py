# -*- coding: utf-8 -*-

from datetime import datetime


class Place:

    def __init__(self, place: 'Place', contents: list = []) -> None:
        self.__contents = contents
        self.__place = place

    @property
    def contents(self) -> list:
        return self.__contents.copy()

    @property
    def place(self) -> 'Place':
        return self.__place

    # TODO move to party?
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
