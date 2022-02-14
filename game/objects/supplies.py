# -*- coding: utf-8 -*-

from .. import Entity
from . import Fluid, Quantifiable, Stowable, Substance


class Drinkable:
    pass


class Eatable:
    pass


class Flammable:
    pass


class Supply(Quantifiable, Stowable):

    ITEMS_PER_SLOT = 1

    @property
    def items_per_slot(self) -> int:
        return self.ITEMS_PER_SLOT

    @property
    def slots_required(self) -> int:
        return ((self.quantity - 1) // self.items_per_slot) + 1


class Rations(Supply, Eatable):
    ITEMS_PER_SLOT = 7


class Rope(Supply):
    '''Can hold the weight of approxi- mately three human-sized beings.'''
    ITEMS_PER_SLOT = 5  # 10' lengths


class Spikes(Supply):
    '''May be used for wedging doors open or shut, as an anchor to attach a rope to, and many other purposes.'''
    ITEMS_PER_SLOT = 6  #  use in pairs?
    # ITEMS_PER_SLOT = 12


class Sundries(Supply):
    '''Bandages, chalk, grease, and other miscellaneous materials.'''
    ITEMS_PER_SLOT = 5


class Torches(Supply):

    ITEMS_PER_SLOT = 6

    def draw(self) -> Entity:
        from .tools import Torch
        self.deplete(1)
        return Torch()


class Ammunition(Supply):
    pass


class Arrows(Ammunition):
    ITEMS_PER_SLOT = 6  # volleys of 3-4
    # ITEMS_PER_SLOT = 20


class Quarrels(Ammunition):
    ITEMS_PER_SLOT = 9  # volleys of 3-4
    # ITEMS_PER_SLOT = 30


class Stones(Ammunition):
    ITEMS_PER_SLOT = 3  # volleys of 3-4
    # ITEMS_PER_SLOT = 10


class Acid(Substance):
    pass


class Gunpowder(Substance):
    pass


class Poison(Substance):
    pass


class Smoke(Substance):
    pass


class Liquor(Fluid, Drinkable, Flammable):
    pass


class Oil(Fluid, Flammable):
    # TODO Pools: Oil that is poured on the ground and lit covers a diameter of 3 feet and burns for 1 turn, inflicting damage on any creature moving through the pool.
    pass


class Water(Fluid, Drinkable):
    pass


class Wine(Fluid, Drinkable):
    pass


# TODO Provisions
