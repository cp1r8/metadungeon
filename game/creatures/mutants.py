# -*- coding: utf-8 -*-

from . import Creature, FlyingCreature


class GiantGecko(Creature):

    class Bite(Creature.Attack):
        DAMAGE = 4

    AC = 5
    HD = 3
    HD_MOD = +1
    AT = [(Bite,)]
    TH = 16
    MV = 12
    SV = 14
    ML = 7
    XP = 50
    # TT = [U]


class GiantCrabSpider(Creature):

    class Bite(Creature.Attack):
        DAMAGE = 4
        # TODO save vs. poison +2, or dead in 1d4 turns

    AC = 7
    HD = 2
    AT = [(Bite,)]
    TH = 18
    MV = 12
    SV = 14
    ML = 7
    XP = 25
    # TT = [U]
    # TODO 1-4 surprise


class GiantFireBeetle(Creature):

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


class GiantKillerBee(FlyingCreature):

    class Sting(Creature.Attack):
        DAMAGE = 2
        # TODO save vs. poison
        # TODO 1 damage per round until removed

    AC = 7
    HD = 1/2
    AT = [(Sting,)]
    TH = 19
    MV = 3  #  ?
    MV_FLY = 15
    SV = 14
    ML = 9
    XP = 6
    # TODO: aggressive
    # TODO dies on successful attack


class GiantShrew(Creature):

    class Bite(Creature.Attack):
        DAMAGE = 3
        # TODO targets with HD≤3 must save vs. death (or flee)

    AC = 4
    HD = 1
    AT = [(Bite, Bite)]
    TH = 19
    MV = 18
    SV = 14
    ML = 10
    XP = 10
    # TODO always win initiative first round; +1 second round
    # TODO AC8 TH23 if deafened; does not need light
