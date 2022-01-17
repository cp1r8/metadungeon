# -*- coding: utf-8 -*-

from . import Creature


class Cobra(Creature):
    pass


class CrabSpider(Creature):
    pass


class DireWolf(Creature):
    pass


class FireBeetle(Creature):

    class Bite(Creature.Attack):
        DAMAGE = 5

    AC = 4
    HD = 1
    HD_MOD = +2
    AT = [(Bite,)]
    TH = 18
    MV = 12
    SV = 14
    ML = 7
    XP = 15
    # TODO drop glowing nodules


class Gecko(Creature):
    pass


class GiantShrew(Creature):
    pass


class KillerBee(Creature):
    pass


class Wolf(Creature):
    pass
