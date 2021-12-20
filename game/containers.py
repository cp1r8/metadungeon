# -*- coding: utf-8 -*-

from .objects import DualHanded, Fluid, Holdable, Quantifiable, Stowable, Substance, Wearable
from typing import Generic, TypeVar


T = TypeVar('T', bound=Quantifiable)


class ContainerError(ValueError):
    pass


class ResourceContainer(Generic[T]):

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

    def remove(self, quantity: int) -> T:
        if isinstance(self.__contents, Quantifiable):
            self.__contents.deplete(quantity)
            return self.contents(quantity)
        raise ContainerError()

    def store(self, item: T) -> None:
        if isinstance(self.__contents, Quantifiable):
            if self.capacity_free < item.quantity:
                raise ContainerError()
            self.__contents.merge(item)
        else:
            if self.__contents:
                raise ContainerError()
            self.__contents = item


class StorageContainer:

    CAPACITY = 1

    def __init__(self) -> None:
        self.__items = []

    @property
    def capacity(self) -> int:
        return int(self.CAPACITY)

    @property
    def capacity_free(self) -> int:
        return self.capacity - self.capacity_used

    @property
    def capacity_used(self) -> int:
        return sum(item.slots_required for item in self.__items)

    @property
    def is_empty(self) -> bool:
        return not self.__items

    @property
    def items(self) -> list[Stowable]:
        return self.__items.copy()

    def remove(self, item: Stowable) -> None:
        if item not in self.__items:
            raise ContainerError()
        self.__items.remove(item)

    def store(self, item: Stowable) -> None:
        if not self.capacity_free:
            raise ContainerError()
        self.__items.append(item)


class StowableContainer(StorageContainer, Stowable):

    @property
    def slots_required(self) -> int:
        return super().slots_required if self.is_empty else (self.capacity_used + 1)


class Backpack(StorageContainer, Wearable):
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


class Flask(ResourceContainer[Fluid], Stowable):

    CAPACITY = 1

    @ classmethod
    def of(cls, contents: Fluid):
        self = cls()
        self.store(contents)
        return self


class Vial(ResourceContainer[Substance], Stowable):

    CAPACITY = 1

    @ classmethod
    def of(cls, contents: Substance):
        self = cls()
        self.store(contents)
        return self


class Waterskin(ResourceContainer[Fluid], Stowable):
    CAPACITY = 2
