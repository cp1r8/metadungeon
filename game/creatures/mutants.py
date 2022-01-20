# -*- coding: utf-8 -*-

from . import Creature, FlyingCreature


class GiantGecko(Creature):
    '''5’ long, carnivorous, nocturnal lizards. Light blue scales with orange spots.'''

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
    # TODO Cling: Climb walls, trees, etc. and drop on victims.


class GiantCrabSpider(Creature):
    '''5’ long hunting spiders that can change their colour to match their surroundings.'''

    class Bite(Creature.Attack):
        DAMAGE = 4
        # TODO Poison: Causes death in 1d4 turns (save versus poison with a +2 bonus).

    AC = 7
    HD = 2
    AT = [(Bite,)]
    TH = 18
    MV = 12
    SV = 14
    ML = 7
    XP = 25
    # TT = [U]
    # TODO Ambush: Attack by dropping on vic- tims from above.
    # TODO Surprise: On a 1–4, due to camouflage.
    # TODO Cling: Can walk on walls and ceilings.


class GiantFireBeetle(Creature):
    '''Two and a half feet long. Commonly found underground.'''

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
    # TODO Glowing nodules: Three glowing glands (two above the eyes, one on the abdomen) cast light in a 10’ radius. If removed, keep glowing for 1d6 days.


class GiantKillerBee(FlyingCreature):
    '''Giant (foot-long) bees of aggressive temperament. Build hives underground.'''

    class Sting(Creature.Attack):
        DAMAGE = 2
        # TODO Poison: Causes death (save vs poison).
        # TODO Lodged stinger: Inflicts 1 damage per round, as the stinger works its way in. A round can be spent to remove it.

    AC = 7
    HD = 1/2
    AT = [(Sting,)]
    TH = 19
    MV = 3  #  ?
    MV_FLY = 15
    SV = 14
    ML = 9
    XP = 6
    # TODO TT = [Honey]
    # TODO Aggressive: Usually attack on sight. Always attack intruders within 30’ of their hive.
    # TODO Die after attacking: On a successful sting attack, a killer bee dies.
    # TODO Honey: around 2 pints may be found in the hive. It heals 1d4 hit points if eaten (in its entirety)
    # TODO Guards: At least 10 bees (4 or more of which have 1HD) remain in or near the hive to protect the queen.


class GiantKillerBeeDrone(GiantKillerBee):
    HD = 1


class GiantKillerBeeQueen(GiantKillerBee):
    # TODO The queen does not die when she stings.
    HD = 2


class GiantShrew(Creature):
    '''Brown-furred, mole-like, insectivores with long snouts. Dwell underground; skilled burrowers.'''

    class Bite(Creature.Attack):
        DAMAGE = 3
        # TODO Ferocity: Attack targets’ heads. Targets with 3 HD or less must save versus death or flee.

    AC = 4
    HD = 1
    AT = [(Bite, Bite)]
    TH = 19
    MV = 18
    SV = 14
    ML = 10
    XP = 10
    # TODO Initiative: Always win initiative in the round of their first attack. +1 to initiative in the round of their second attack.
    # TODO Climbing: Skilled climbers; can jump up to 5’.
    # TODO Territorial: Ferociously defend their hunting area from all intruders.
    # TODO Echolocation: Perceive their surroundings up to 60’. Unaffected by lack of light. If unable to hear (e.g. silence, 15’ radius): AC = 8, –4 penalty to attacks.
