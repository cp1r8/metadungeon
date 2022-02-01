# -*- coding: utf-8 -*-

from . import DualHanded, Fluid, Holdable, Quantifiable, Stowable, Substance, Throwable, Wearable
from .. import Entity
from typing import Generic, TypeVar


class ContainerError(ValueError):
    pass


R = TypeVar('R', bound=Quantifiable)


class ResourceContainer(Generic[R]):

    CAPACITY = 1

    def __init__(self) -> None:
        self.__contents = None

    @property
    def capacity(self) -> int:
        return int(self.CAPACITY)

    @property
    def capacity_free(self) -> int:
        return self.capacity - self.quantity

    @property
    def contents(self) -> type:
        return type(self.__contents)

    @property
    def is_empty(self) -> bool:
        return not self.__contents or self.__contents.quantity == 0

    @property
    def quantity(self) -> int:
        if isinstance(self.__contents, Quantifiable):
            return self.__contents.quantity
        return 1 if self.__contents else 0

    def add(self, item: R) -> None:
        if isinstance(self.__contents, Quantifiable):
            if self.capacity_free < item.quantity:
                raise ContainerError()
            self.__contents.merge(item)
        else:
            if self.__contents:
                raise ContainerError()
            self.__contents = item

    def remove(self, quantity: int) -> R:
        if isinstance(self.__contents, Quantifiable):
            self.__contents.deplete(quantity)
            return self.contents(quantity)
        raise ContainerError()


F = TypeVar('F', bound=Fluid)


class FluidContainer(Entity, ResourceContainer[F], Generic[F]):

    def __init__(self):
        Entity.__init__(self)
        ResourceContainer.__init__(self)


S = TypeVar('S', bound=Substance)


class SubstanceContainer(Entity, ResourceContainer[S], Generic[S]):

    def __init__(self):
        Entity.__init__(self)
        ResourceContainer.__init__(self)


T = TypeVar('T')


class Container(Generic[T]):

    CAPACITY = 0

    def __init__(self) -> None:
        self.__contents = []

    @property
    def capacity(self) -> int:
        return int(self.CAPACITY)

    @property
    def capacity_free(self) -> int:
        return self.capacity - self.capacity_used

    @property
    def capacity_used(self) -> int:
        return self.items

    @property
    def contents(self) -> list[T]:
        return self.__contents.copy()

    @property
    def is_empty(self) -> bool:
        return not self.__contents

    @property
    def items(self) -> int:
        return len(self.__contents)

    def add(self, item: T) -> None:
        if not self.capacity_free:
            raise ContainerError()
        self.__contents.append(item)

    def remove(self, item: T) -> None:
        if item not in self.__contents:
            raise ContainerError()
        self.__contents.remove(item)


class Pile(Entity, Container[object]):

    CAPACITY = 9999

    def __init__(self) -> None:
        Entity.__init__(self)
        Container.__init__(self)


class StorageContainer(Entity, Container[Stowable]):

    def __init__(self) -> None:
        Entity.__init__(self)
        Container.__init__(self)

    @property
    def capacity_used(self) -> int:
        return sum(item.slots_required for item in self.contents)

    def add(self, item: Stowable) -> None:
        if item.slots_required > self.capacity_free:
            raise ContainerError()
        # TODO heavy items
        super().add(item)


class StowableContainer(StorageContainer, Stowable):

    @property
    def slots_required(self) -> int:
        return super().slots_required if self.is_empty else (self.capacity_used + 1)


class Backpack(StorageContainer, Wearable):
    '''Has two straps and can be worn on the back, keeping the hands free.'''
    CAPACITY = 12
    ON = 'shoulders'


class Belt(StowableContainer, Wearable):
    CAPACITY = 3
    ON = 'waist'


class DrySack(StowableContainer, DualHanded):
    CAPACITY = 15


class LargeSack(StowableContainer, DualHanded):
    CAPACITY = 18


class SmallSack(StowableContainer, Holdable):
    CAPACITY = 6


class Flask(FluidContainer, Stowable, Throwable):

    CAPACITY = 1

    @ classmethod
    def of(cls, contents: Fluid):
        self = cls()
        self.add(contents)
        return self

    # TODO Throwing: An oil flask may be lit on fire and thrown


class Vial(SubstanceContainer, Stowable):

    CAPACITY = 1

    @ classmethod
    def of(cls, contents: Substance):
        self = cls()
        self.add(contents)
        return self


class Waterskin(FluidContainer, Stowable):
    '''This container, made of hide, will hold 2 pints (1 quart) of fluid.'''
    CAPACITY = 2
