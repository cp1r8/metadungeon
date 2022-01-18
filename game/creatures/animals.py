# -*- coding: utf-8 -*-

from . import Creature


class DireWolf(Creature):

    class Bite(Creature.Attack):
        DAMAGE = 5

    AC = 6
    HD = 4
    HD_MOD = +1
    AT = [(Bite,)]
    TH = 15
    MV = 15
    SV = 14
    ML = 8
    XP = 125


class SpittingCobra(Creature):

    class Bite(Creature.Attack):
        DAMAGE = 2
        # TODO save vs. poison or dead in 1d10 turns

    class Spit(Creature.Attack):
        DAMAGE = 0
        # TODO range 1, save. vs. poison or permanently blind

    AC = 7
    HD = 1
    AT = [(Bite,), (Spit,)]
    TH = 19
    MV = 9
    SV = 14
    ML = 7
    XP = 13


class Wolf(Creature):

    class Bite(Creature.Attack):
        DAMAGE = 3

    AC = 7
    HD = 2
    HD_MOD = +2
    AT = [(Bite,)]
    TH = 17
    MV = 18
    SV = 14
    ML = 6
    XP = 25
    # TODO ML8 if NA≥4
