# -*- coding: utf-8 -*-

from . import Creature, Unit


class DireWolf(Creature):
    '''Large, savage, semi-intelligent wolves. Dwell in caves, mountains, and forests.'''

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

    # TODO Training: At the referee’s discretion, captured cubs may be trained like dogs. Dire wolves are ferocious and extremely difficult to train.
    # TODO Mounts: Sometimes trained as mounts by goblins.


class SpittingCobra(Creature):
    '''3’ long snakes with grey/white scales. Prefer to attack from a distance with spit.'''

    class Bite(Creature.Attack):
        DAMAGE = 2
        # TODO Poison: Causes death in 1d10 turns (save versus poison).

    class Spit(Creature.Attack):
        DAMAGE = 0
        # TODO Blinding spit: Range: 6’. A hit causes permanent blindness (save vs poison).

    AC = 7
    HD = 1
    AT = [(Bite,), (Spit,)]
    TH = 19
    MV = 9
    SV = 14
    ML = 7
    XP = 13


class Wolf(Creature):
    '''Carnivorous relatives of dogs that hunt in packs. Dwell primarily in wild lands, but occasionally lair in caves.'''

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
    ML_PACK = 8
    XP = 25

    @property
    def morale_rating(self) -> int:
        '''Strength in numbers: Packs of 4 or more wolves have morale 8.'''
        if isinstance(self.location, Unit):
            if len({member for member in self.location.members if isinstance(member, Wolf)}) >= 4:
                return self.ML_PACK
        # TODO If the pack is reduced to less than 50% of its original size, this morale bonus is lost.
        return super().morale_rating

    # TODO Training: At the referee’s discretion, captured cubs may be trained like dogs. Wolves are difficult to train.
