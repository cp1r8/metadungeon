# -*- coding: utf-8 -*-

from game import Entity
from . import Holdable, Stowable, TwoHanded
from .containers import FluidContainer
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


class Crowbar(ImprovisedWeapon, Stowable, TwoHanded):
    '''2–3’ long and made of solid iron. Can be used for forcing doors and other objects open.'''


class Grapnel(ImprovisedWeapon, Holdable, Stowable):
    '''Has 3 or 4 prongs. Can be used for anchoring a rope.'''


class Lantern(FluidContainer[Oil], Holdable, LightSource, Stowable):
    CAPACITY = 2
    # TODO Can be closed to hide the light.


class Lockpicks(Entity, Holdable, Stowable):
    # TODO small
    pass


class Mallet(ImprovisedWeapon, Holdable, Stowable):
    '''Can be used for construction or for driving in spikes.'''
    # TODO small


class Mirror(Entity, Holdable, Stowable):
    '''Useful for looking around cor- ners or for reflecting light.'''
    # TODO small


class Pole(Entity, Stowable, TwoHanded):
    '''A 2” thick wooden pole useful for poking and prodding suspicious items.'''
    # TODO bulky?


class Tinderbox(Entity, Holdable, Stowable):
    '''Used to light fires, including torches.'''
    # TODO Using takes one round. There is a 2-in-6 chance of success per round.


class Torch(ImprovisedWeapon, Holdable, LightSource):
    pass
