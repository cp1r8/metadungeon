# -*- coding: utf-8 -*-

from datetime import datetime


class Place:

    def actions(self) -> list:
        return []


class World:

    EPOCH = datetime(1001, 1, 1, 0, 0)

    def __init__(self, time: datetime = EPOCH) -> None:
        self.__places = []
        self.__time = time

    @property
    def places(self) -> list[Place]:
        return self.__places.copy()

    @property
    def time(self) -> datetime:
        return self.__time

    def establish(self, place: Place) -> None:
        self.__places.append(place)
