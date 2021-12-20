# -*- coding: utf-8 -*-

from .objects import Heavy, Stowable
from .supplies import Supply


class Valuable:

    @property
    def value_in_copper(self) -> int:
        return 0


class Cash(Heavy, Supply, Valuable):

    # ITEMS_PER_SLOT = 1000
    ITEMS_PER_SLOT = 100
    VALUE_IN_COPPER = 0

    @property
    def value_in_copper(self) -> int:
        return int(self.quantity * self.VALUE_IN_COPPER)


class Copper(Cash):
    VALUE_IN_COPPER = 1


class Silver(Cash):
    # VALUE_IN_COPPER = 5
    VALUE_IN_COPPER = 10


class Electrum(Cash):
    # VALUE_IN_COPPER = 25
    VALUE_IN_COPPER = 50


class Gold(Cash):
    # VALUE_IN_COPPER = 50
    VALUE_IN_COPPER = 100


class Platinum(Cash):
    # VALUE_IN_COPPER = 100
    VALUE_IN_COPPER = 500


class Gems(Heavy, Supply, Valuable):

    # ITEMS_PER_SLOT = 1000
    ITEMS_PER_SLOT = 100
    VALUE_IN_COPPER = 0

    @property
    def value_in_copper(self) -> int:
        return int(self.quantity * self.VALUE_IN_COPPER)

    # TODO 20% Pearl, 25% Sapphire, 30% Emerald, 20% Ruby, 5% Diamond


class Pearls(Gems):
    VALUE_IN_COPPER = 10 * Gold.VALUE_IN_COPPER


class Sapphires(Gems):
    VALUE_IN_COPPER = 50 * Gold.VALUE_IN_COPPER


class Emeralds(Gems):
    VALUE_IN_COPPER = 100 * Gold.VALUE_IN_COPPER


class Rubies(Gems):
    VALUE_IN_COPPER = 500 * Gold.VALUE_IN_COPPER


class Diamonds(Gems):
    VALUE_IN_COPPER = 1000 * Gold.VALUE_IN_COPPER


class Jewellery(Stowable, Valuable):

    # TODO small… wearable?
    # TODO head: earring, crown
    # TODO hands: bracelet, ring
    # TODO torso: brooch, necklace

    RELATIVE_VALUE_IN_COPPER = 100 * Gold.VALUE_IN_COPPER

    # TODO value=3d6
    def __init__(self, value: int) -> None:
        self.__damaged = False
        self.__value = value

    @property
    def damaged(self) -> bool:
        return self.__damaged

    @property
    def value_in_copper(self) -> int:
        value_in_copper = int(self.__value * self.RELATIVE_VALUE_IN_COPPER)
        return value_in_copper // 2 if self.damaged else value_in_copper

    def damage(self) -> None:
        self.__damaged = True
