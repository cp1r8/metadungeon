# -*- coding: utf-8 -*-

from .. import d6, d20


class Creature:

    class Attack:

        # TODO melee vs. missile/ranged
        DAMAGE = 1

        def __init__(self, source: 'Creature', target) -> None:
            self.__source = source
            self.__target = target

        @property
        def damage(self) -> int:
            return int(self.DAMAGE)

        @property
        def modifier(self) -> int:
            return int(getattr(self.target, 'armour_class', 0))

        @property
        def source(self) -> 'Creature':
            return self.__source

        @property
        def target(self):
            return self.__target

        def __call__(self, roll: int) -> bool:
            if roll == 1:
                return False
            if roll == 20:
                return True
            return roll + self.modifier >= self.source.attack_target_value

        def hits(self) -> bool:
            return self(d20())

    HD = 1
    HD_MOD = +0
    TH = 20
    SV = 16
    AC = 9
    MV = 12
    ML = 6
    AT = []
    TT = []

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
    def attacks(self) -> list:
        return self.AT

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
    def morale_rating(self) -> int:
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

    @property
    def treasure_types(self) -> list:
        return self.TT

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
