# -*- coding: utf-8 -*-

from . import Heavy, Holdable, Wearable


class Armour(Wearable):

    AC = 9
    MV = 12

    @property
    def armour_class(self) -> int:
        return self.AC

    @property
    def movement_rate(self) -> int:
        return self.MV


class Leather(Armour):
    AC = 7
    MV = 9
    ON = 'torso'


class Chain(Armour, Heavy):
    AC = 5
    MV = 6
    ON = 'torso'


class Plate(Armour, Heavy):
    AC = 3
    MV = 6
    ON = 'torso'


class Shield(Holdable):

    # TODO carry on shoulders?
    # TODO improvised weapon?
    AC_MOD = -1

    @property
    def armour_class_modifier(self):
        return self.AC_MOD
