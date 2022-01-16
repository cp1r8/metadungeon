# -*- coding: utf-8 -*-

from game.objects.tools import Torch
from . import Humanoid, Person
from ..objects import armour, weapons


class Human(Humanoid, Person):
    AC = 9
    HD = 1/2
    TH = 20
    MV = 12
    SV = 16
    ML = 6
    XP = 5
    # TT = [U]


class Acolyte(Human):
    # AC = 2
    HD = 1
    TH = 19
    # MV = 6
    SV = 14
    ML = 7
    XP = 10
    # TT = [U]
    MHAND = weapons.Mace
    OHAND = armour.Shield
    TORSO = armour.Plate


class Bandit(Human):
    # AC = 6
    HD = 1
    TH = 19
    # MV = 9 # 12
    SV = 13
    ML = 8
    XP = 10
    # TT = [U]
    # TT_LAIR = [A]
    MHAND = weapons.Shortsword
    OHAND = armour.Shield
    TORSO = armour.Leather


# TODO Commoner = NormalHuman


class Trader(Human):
    # AC = 6
    HD = 1
    TH = 19
    # MV = 9
    SV = 14
    ML = 7
    XP = 10
    # TT = [U, V]
    MHAND = weapons.Sword
    OHAND = armour.Shield
    TORSO = armour.Leather
