# -*- coding: utf-8 -*-

from . import Creature, FlyingCreature


class GreenSlime(Creature):

    class Touch(Creature.Attack):
        # TODO destroy wood and metal (armour/weapons)
        # TODO turn victim into slime in 6 rounds
        pass

    AC = 19
    HD = 2
    AT = [(Touch,)]
    TH = 18
    MV = 1/3
    SV = 14
    ML = 12
    XP = 25
    # TODO immune to anything except cold and fire


class Stirge(FlyingCreature):
    pass
