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
    '''Burns one oil flask about every four hours. Casts light in a 30’ radius.'''

    CAPACITY = 2

    def __init__(self) -> None:
        FluidContainer.__init__(self)
        LightSource.__init__(self)

    # TODO Can be closed to hide the light.


class Lockpicks(Entity, Holdable, Stowable):
    pass


class Mallet(ImprovisedWeapon, Holdable, Stowable):
    '''Can be used for construction or for driving in spikes.'''


class Mirror(Entity, Holdable, Stowable):
    '''Useful for looking around cor- ners or for reflecting light.'''


class Pole(Entity, Stowable, TwoHanded):
    '''A 2” thick wooden pole useful for poking and prodding suspicious items.'''


class Tinderbox(Entity, Holdable, Stowable):
    '''Used to light fires, including torches.'''
    # TODO Using takes one round. There is a 2-in-6 chance of success per round.


class Torch(ImprovisedWeapon, Holdable, LightSource):
    '''A torch burns for about an hour, clearly illuminating a 30’ radius.'''

    def __init__(self) -> None:
        ImprovisedWeapon.__init__(self)
        LightSource.__init__(self)
