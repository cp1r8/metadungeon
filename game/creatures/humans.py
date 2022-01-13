# -*- coding: utf-8 -*-

from . import Humanoid, Person


class Human(Humanoid, Person):
    '''Normal human'''
    HD = 1/2
    TH = 20
    SV = 16
    AC = 9
    MV = 12
    ML = 6
