# -*- coding: utf-8 -*-

from . import d6


class Creature:

    HD = 1
    HD_MOD = +0
    TH = 20
    SV = 16
    AC = 9
    MV = 12
    ML = 6

    # TODO attacks

    def __init__(self) -> None:
        self.__hits_taken = 0
        self.__partial_hit = False

    @property
    def armour_class(self) -> int:
        return int(self.AC)

    @property
    def attack_target_value(self) -> int:
        return int(self.TH)

    @property
    def hit_dice(self) -> int:
        return int(self.HD)

    @property
    def hit_die_modifier(self) -> int:
        return int(self.HD_MOD)

    @property
    def hits_remaining(self) -> int:
        return self.hit_dice - self.hits_taken - (1 if self.partial_hit else 0)

    @property
    def hits_taken(self) -> int:
        return int(self.__hits_taken)

    @property
    def morale(self) -> int:
        return int(self.ML)

    @property
    def partial_hit(self) -> bool:
        return self.__partial_hit

    @property
    def movement_rate(self) -> int:
        return int(self.MV)

    @property
    def save_target_value(self) -> int:
        return int(self.SV)

    def hit(self, damage: int) -> bool:
        while damage > 0 and self.hits_taken < self.hit_dice:
            damage -= d6()
            if self.hits_taken == 0:
                damage -= self.hit_die_modifier
            if damage < 0:
                if self.partial_hit:
                    self.__hits_taken += 1
                    self.__partial_hit = False
                else:
                    self.__partial_hit = True
                return False
            self.__hits_taken += 1
        self.__hits_taken += damage
        return True
