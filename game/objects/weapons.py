# -*- coding: utf-8 -*-

from . import Heavy, Holdable, Stowable, TwoHanded
from .containers import ResourceContainer
from .supplies import Arrows, Quarrels, Stones


class Weapon:
    '''Able to inflict physical damage or harm.'''

    DAMAGE = 1

    @property
    def damage(self) -> int:
        return self.DAMAGE


class Melee:
    '''Able to be used in hand-to-hand combat.'''


class Missile:
    '''Able to be used in ranged combat.'''

    RANGES = (0, 0, 0)

    @property
    def ranges(self) -> tuple:
        return self.RANGES


class Staff(TwoHanded, Melee, Weapon):
    DAMAGE = 2


class Club(Holdable, Melee, Weapon, Stowable):
    DAMAGE = 2


class Dagger(Holdable, Melee, Missile, Weapon, Stowable):
    DAMAGE = 2
    RANGES = (1, 2, 3)


class SilverDagger(Dagger):
    pass


class Javelin(Holdable, Missile, Weapon, Stowable):
    DAMAGE = 2
    RANGES = (3, 6, 9)


class Sling(Holdable, Missile, Weapon, Stowable, ResourceContainer[Stones]):
    CAPACITY = Stones.ITEMS_PER_SLOT
    DAMAGE = 2
    RANGES = (3, 6, 9)


class Mace(Holdable, Heavy, Melee, Weapon, Stowable):
    DAMAGE = 3


class Maul(Holdable, Heavy, Melee, Weapon, Stowable):
    DAMAGE = 3


class Shortsword(Holdable, Melee, Weapon, Stowable):
    DAMAGE = 3


class Axe(Holdable, Melee, Missile, Weapon, Stowable):
    DAMAGE = 3
    RANGES = (1, 2, 3)


class Spear(Holdable, Melee, Missile, Weapon):
    DAMAGE = 3
    RANGES = (2, 4, 6)


class Shortbow(TwoHanded, Missile, Weapon, Stowable, ResourceContainer[Arrows]):
    CAPACITY = Arrows.ITEMS_PER_SLOT
    DAMAGE = 3
    RANGES = (5, 10, 15)


class Crossbow(TwoHanded, Missile, Weapon, ResourceContainer[Quarrels]):
    # TODO heavy? reload
    CAPACITY = Quarrels.ITEMS_PER_SLOT
    DAMAGE = 3
    RANGES = (8, 16, 24)


class Sword(Holdable, Melee, Weapon, Stowable):
    DAMAGE = 4


class Longbow(TwoHanded, Missile, Weapon, ResourceContainer[Arrows]):
    CAPACITY = Arrows.ITEMS_PER_SLOT
    DAMAGE = 4
    RANGES = (7, 14, 21)


class Battleaxe(Heavy, TwoHanded, Melee, Weapon):
    DAMAGE = 4


class Greatsword(Heavy, TwoHanded, Melee, Weapon):
    DAMAGE = 5


class Polearm(Heavy, TwoHanded, Melee, Weapon):
    DAMAGE = 5


Warhammer = Maul
