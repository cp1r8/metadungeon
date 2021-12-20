# -*- coding: utf-8 -*-

from random import randint


class Dice:

    def __init__(self, dice: list):
        self.__dice = dice
        self.__multiplier = 1

    def __add__(self, other):
        if isinstance(other, Dice):
            self.__dice.extend(other)
        else:
            self.__dice.append(other)
        return self

    def __iter__(self):
        for die in self.__dice:
            yield (die() if callable(die) else die) * self.__multiplier

    def __mul__(self, number: int):
        self.__multiplier *= number
        return self


class Die:

    def __init__(self, sides: int):
        self.__sides = sides

    def __call__(self) -> int:
        return randint(1, self.__sides)

    def __rmul__(self, number) -> Dice:
        return Dice([self] * number)

    def __str__(self) -> str:
        return f"d{self.sides}"

    @property
    def sides(self) -> int:
        return self.__sides


d1 = Die(1)
d2 = Die(2)
d3 = Die(3)
d4 = Die(4)
d6 = Die(6)
d8 = Die(8)
d10 = Die(10)
d12 = Die(12)
d20 = Die(20)
d100 = Die(100)
