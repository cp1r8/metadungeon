# -*- coding: utf-8 -*-

from . import Holdable, Stowable, TwoHanded
from .containers import ResourceContainer
from .supplies import Oil
from .weapons import Weapon


class ImprovisedWeapon(Weapon):
    DAMAGE = 2


class LightSource:

    def __init__(self) -> None:
        self.__lit = False

    @property
    def lit(self) -> bool:
        return self.__lit

    def extinguish(self) -> None:
        self.__lit = False

    def light(self) -> None:
        if not self.lit:
            # TODO takes time, requires tinderbox…
            self.__lit = True


class Crowbar(Stowable, TwoHanded, ImprovisedWeapon):
    pass


class Grapnel(Holdable, Stowable, ImprovisedWeapon):
    pass


class Lantern(ResourceContainer[Oil], Holdable, Stowable, LightSource):
    CAPACITY = 2


class Lockpicks(Holdable, Stowable):
    # TODO small
    pass


class Mallet(Holdable, Stowable, ImprovisedWeapon):
    # TODO small
    pass


class Mirror(Holdable, Stowable):
    # TODO small
    pass


class Pole(Stowable, TwoHanded):
    # TODO bulky?
    pass


class Tinderbox(Holdable, Stowable):
    pass


class Torch(Holdable, LightSource, ImprovisedWeapon):
    pass
