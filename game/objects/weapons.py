# -*- coding: utf-8 -*-

from . import Heavy, Holdable, Ranged, Stowable, Throwable, TwoHanded
from .. import Entity
from .containers import ResourceContainer
from .supplies import Ammunition, Arrows, Quarrels, Stones
from typing import Generic, TypeVar


class Weapon(Entity):
    '''Able to inflict physical damage or harm.'''

    DAMAGE = 1

    @property
    def damage(self) -> int:
        return self.DAMAGE


class MeleeWeapon(Weapon):
    '''Able to be used in hand-to-hand combat.'''


A = TypeVar('A', bound=Ammunition)


class ProjectileWeapon(Weapon, Ranged, ResourceContainer[A], Generic[A]):

    def __init__(self):
        Weapon.__init__(self)
        ResourceContainer.__init__(self)


class Staff(MeleeWeapon, TwoHanded):
    DAMAGE = 2


class Club(MeleeWeapon, Holdable, Stowable):
    DAMAGE = 2


class Dagger(MeleeWeapon, Holdable, Stowable, Throwable):
    DAMAGE = 2
    RANGES = (1, 2, 3)


class SilverDagger(Dagger):
    pass


class Javelin(MeleeWeapon, Holdable, Stowable, Throwable):
    DAMAGE = 2
    RANGES = (3, 6, 9)


class Sling(ProjectileWeapon[Stones], Holdable, Stowable):
    CAPACITY = Stones.ITEMS_PER_SLOT
    DAMAGE = 2
    RANGES = (3, 6, 9)


class Mace(MeleeWeapon, Holdable, Heavy, Stowable):
    DAMAGE = 3


class Maul(MeleeWeapon, Holdable, Heavy, Stowable):
    DAMAGE = 3


class Shortsword(MeleeWeapon, Holdable, Stowable):
    DAMAGE = 3


class Axe(MeleeWeapon, Holdable, Stowable):
    DAMAGE = 3
    RANGES = (1, 2, 3)


class Spear(MeleeWeapon, Holdable, Throwable):
    DAMAGE = 3
    RANGES = (2, 4, 6)


class Shortbow(ProjectileWeapon[Arrows], Stowable, TwoHanded):
    CAPACITY = Arrows.ITEMS_PER_SLOT
    DAMAGE = 3
    RANGES = (5, 10, 15)


class Crossbow(ProjectileWeapon[Quarrels], TwoHanded):
    # TODO heavy? reload
    CAPACITY = Quarrels.ITEMS_PER_SLOT
    DAMAGE = 3
    RANGES = (8, 16, 24)


class Sword(MeleeWeapon, Holdable, Stowable):
    DAMAGE = 4


class Longbow(ProjectileWeapon[Arrows], TwoHanded):
    CAPACITY = Arrows.ITEMS_PER_SLOT
    DAMAGE = 4
    RANGES = (7, 14, 21)


class Battleaxe(MeleeWeapon, Heavy, TwoHanded):
    DAMAGE = 4


class Greatsword(MeleeWeapon, Heavy, TwoHanded):
    DAMAGE = 5


class Polearm(MeleeWeapon, Heavy, TwoHanded):
    DAMAGE = 5
