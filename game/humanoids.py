# -*- coding: utf-8 -*-

from .containers import StorageContainer
from .creatures import Creature
from .objects import DualHanded, Holdable, Wearable


class HoldError(ValueError):
    pass


class WearError(ValueError):
    pass


class Humanoid(Creature):

    def __init__(self) -> None:
        super().__init__()
        self.__main_hand = None
        self.__off_hand = None
        self.__shoulders = None
        self.__torso = None
        self.__waist = None

    @property
    def main_hand(self):
        return self.__main_hand

    @property
    def off_hand(self):
        return self.__off_hand

    @property
    def shoulders(self):
        return self.__shoulders

    @property
    def torso(self):
        return self.__torso

    @property
    def waist(self):
        return self.__waist

    def doff(self, item: Wearable) -> None:
        # TODO takes time…
        if self.__shoulders is item:
            self.__shoulders = None
        elif self.__torso is item:
            self.__torso = None
        elif self.__waist is item:
            self.__waist = None
        raise WearError()

    def don(self, item: Wearable) -> None:
        # TODO takes time…
        if item.on == 'shoulders':
            if self.__shoulders:
                raise WearError()
            self.__shoulders = item
        elif item.on == 'torso':
            if self.__torso:
                raise WearError()
            self.__torso = item
        elif item.on == 'waist':
            if self.__waist:
                raise WearError()
            self.__waist = item

    def drop(self, item: Holdable) -> None:
        if self.__main_hand is item:
            self.__main_hand = None
            if self.__off_hand is item:
                self.__off_hand = None
        elif self.__off_hand is item:
            self.__off_hand = None
        else:
            raise HoldError()

    def hold(self, item: Holdable, hand: str = 'any') -> None:
        if hand not in ('main', 'off'):
            hand = 'off' if self.main_hand else 'main'
        if hand == 'main':
            if self.main_hand:
                raise HoldError()
            if isinstance(item, DualHanded):
                if self.off_hand:
                    raise HoldError()
                self.__off_hand = item
            self.__main_hand = item
        if hand == 'off':
            if self.off_hand:
                raise HoldError()
            if isinstance(item, DualHanded):
                if self.main_hand:
                    raise HoldError()
                self.__main_hand = item
            self.__off_hand = item


class Human(Humanoid):
    '''Normal human'''
    HD = 1/2
    TH = 20
    SV = 16
    AC = 9
    MV = 12
    ML = 6
