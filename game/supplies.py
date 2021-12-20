# -*- coding: utf-8 -*-

from .objects import Fluid, Quantifiable, Stowable, Substance


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


class Rations(Eatable, Supply):
    ITEMS_PER_SLOT = 7


class Rope(Supply):
    ITEMS_PER_SLOT = 5  # 10' lengths


class Spikes(Supply):
    ITEMS_PER_SLOT = 6  #  use in pairs?
    # ITEMS_PER_SLOT = 12


class Sundries(Supply):
    '''Bandages, chalk, grease, and other miscellaneous materials.'''
    ITEMS_PER_SLOT = 5


class Torches(Supply):
    ITEMS_PER_SLOT = 6


class Arrows(Supply):
    ITEMS_PER_SLOT = 6  # volleys of 3-4
    # ITEMS_PER_SLOT = 20


class Quarrels(Supply):
    ITEMS_PER_SLOT = 9  # volleys of 3-4
    # ITEMS_PER_SLOT = 30


class Stones(Supply):
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


class Liquor(Drinkable, Flammable, Fluid):
    pass


class Oil(Flammable, Fluid):
    pass


class Water(Drinkable, Fluid):
    pass


class Wine(Drinkable, Fluid):
    pass


# TODO Provisions
