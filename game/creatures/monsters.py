# -*- coding: utf-8 -*-

from . import Creature, FlyingCreature


class GreenSlime(Creature):
    '''Dripping, green slime that clings to walls and ceilings.'''

    class Touch(Creature.Attack):
        # TODO Acid: When in contact with a victim, sticks on and exudes acid. The acid de- stroys wood or metal (including armour) in 6 rounds, but cannot affect stone.
        # TODO Consume flesh: Once in contact with flesh for 6 rounds, the victim is turned into green slime in a further 1d4 rounds.
        # TODO Removing: Once stuck on a victim, can only be removed by fire. This inflicts half damage to the victim and half to the slime.
        pass

    AC = 19
    HD = 2
    AT = [(Touch,)]
    TH = 18
    # MV = 1/3
    MV = 1
    SV = 14
    ML = 12
    XP = 25
    # TODO Surprise: Drops down on surprised characters from above.
    # TODO Immunity: Unharmed by all attacks except cold or fire.


class Stirge(FlyingCreature):
    '''Feathered, bird-like creatures with long, sharp beaks.'''

    class Beak(Creature.Attack):
        DAMAGE = 2
        # TODO Dive attack: First attack is at +2 to hit.
        # TODO Blood sucking: Upon a successful attack, attaches and drains victim’s blood: 1d3 automatic damage per round.
        # TODO Detach: If stirge or victim dies.

    AC = 7
    HD = 1
    AT = [(Beak,)]
    TH = 19
    MV = 3
    MV_FLY = 18
    SV = 14
    ML = 9
    XP = 13
    # TT = [L]
