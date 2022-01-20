# -*- coding: utf-8 -*-

from . import Humanoid, Person, Unit, adventurers
from .. import Location
from ..dice import d3
from ..objects import armour, weapons
import random


class Human(Humanoid, Person):
    '''Non-adventuring humans without a character class. Artists, beggars, children, craftspeople, farmers, fishermen, house- wives, scholars, slaves.'''
    AC = 9
    HD = 1/2
    TH = 20
    MV = 12
    SV = 16
    ML = 6
    XP = 5
    # TT = [U]


class Acolyte(Human):
    '''1st level clerics on a quest for their deity.'''
    # AC = 2
    HD = 1
    TH = 19
    # MV = 6
    SV = 14
    ML = 7
    XP = 10
    # TT = [U]
    HANDS = [weapons.Mace, armour.Shield]
    TORSO = [armour.Plate]

    @classmethod
    def encounter(cls, number_appearing: int, place: Location) -> Unit:
        '''Leader: Groups of 4+ are led by a higher level cleric (1d10: 1-4: 2nd level, 5-7: 3rd level, 8-9: 4th level, 10: 5th level).'''
        unit = super().encounter(number_appearing, place)
        if number_appearing >= 4:
            level = random.choice([2, 2, 2, 2, 3, 3, 3, 4, 4, 5])
            unit.assign(adventurers.Cleric.generate(level, True))
        return unit


class Bandit(Human):
    '''NPC thieves who live by robbery.'''
    # AC = 6
    HD = 1
    TH = 19
    # MV = 12 # override?
    SV = 13
    ML = 8
    XP = 10
    # TT = [U]
    # TT_LAIR = [A]
    HANDS = [weapons.Shortsword, armour.Shield]
    TORSO = [armour.Leather]
    # TODO Hoard: Only have treasure type A when encountered in their wilderness lair.
    # TODO Trickery: Use disguise or trickery to surprise victims.

    @classmethod
    def encounter(cls, number_appearing: int, place: Location) -> Unit:
        '''Leader: May have a leader of 2nd level or higher (any human class).'''
        unit = super().encounter(number_appearing, place)
        if number_appearing >= 4:
            level = random.choice([2, 2, 2, 2, 3, 3, 3, 4, 4, 5])
            unit.assign(adventurers.Adventurer.generate(level, True))
        return unit


class Trader(Human):
    '''1st level fighters who live by trading in borderland areas. Usually carry: hand-axe, sword, shield, furs (equivalent to leather armour).'''
    # AC = 6
    HD = 1
    TH = 19
    # MV = 12 # override?
    SV = 14
    ML = 7
    XP = 10
    # TT = [U, V]
    HANDS = [weapons.Sword, armour.Shield]
    TORSO = [armour.Leather]
    WAIST = [weapons.Axe]
    # TODO Mules: In the wilderness, have 1d4 mules loaded with trade goods (e.g. carved wooden items, furs, spices).
