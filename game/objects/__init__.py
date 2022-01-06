# -*- coding: utf-8 -*-


class QuantityError(ValueError):
    pass


class Heavy:
    pass


class Portable:
    '''Able to be carried in some way.'''


class Holdable(Portable):
    '''Able to be held in one‘s hand(s).'''


class TwoHanded(Holdable):
    '''Requires both hands to use.'''


class DualHanded(TwoHanded):
    '''Requires both hands to hold and use.'''


class Quantifiable:
    '''Represents a limited amount of some item or resource.'''

    def __init__(self, quantity: int = 1) -> None:
        self.__quantity = quantity

    @property
    def quantity(self) -> int:
        return self.__quantity

    def deplete(self, quantity: int) -> None:
        if self.__quantity < quantity:
            raise QuantityError()
        self.__quantity -= quantity

    def merge(self, other) -> None:
        if type(other) is not type(self):
            raise QuantityError()
        self.__quantity += other.quantity
        other.deplete(other.quantity)

    # TODO split


class Substance(Quantifiable):
    '''A kind of matter with uniform properties.'''


class Fluid(Substance):
    '''A substance that flows.'''


class Stowable(Portable):
    '''Able to be stored in a storage container.'''

    SLOTS_REQUIRED = 1

    @property
    def slots_required(self) -> int:
        return self.SLOTS_REQUIRED


class Wearable(Portable):
    '''Able to be worn on one’s person.'''

    ON = '-'

    @property
    def on(self) -> str:
        return self.ON
