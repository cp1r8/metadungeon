# -*- coding: utf-8 -*-

from ..dice import d6, d20
from ..objects import armour, DualHanded, Holdable, Wearable
from ..objects.weapons import Weapon


class HoldError(ValueError):
    pass


class WearError(ValueError):
    pass


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
        return max(0, self.hit_dice - self.hits_taken)

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
        self.__partial_hit = False
        self.__hits_taken += damage
        return True


class Humanoid(Creature):

    class Attack(Creature.Attack):

        def __init__(self, source: 'Humanoid', target) -> None:
            super().__init__(source, target)

        @property
        def damage(self) -> int:
            if isinstance(self.source.main_hand, Weapon):
                return self.source.main_hand.damage
            return super().damage

        @property
        def modifier(self) -> int:
            # TODO improvised weapon -2 to hit
            # TODO two-handed weapon needs both hands
            # TODO short/long range +1/-1 to hit
            return super().modifier

        @property
        def source(self) -> 'Humanoid':
            source = super().source
            if isinstance(source, Humanoid):
                return source
            raise TypeError()

    AT = [(Attack,)]

    def __init__(self) -> None:
        super().__init__()
        self.__main_hand = None
        self.__off_hand = None
        self.__shoulders = None
        self.__torso = None
        self.__waist = None

    @property
    def armour_class(self) -> int:
        if isinstance(self.torso, armour.Armour):
            armour_class = self.torso.armour_class
        else:
            armour_class = self.base_armour_class
        if isinstance(self.off_hand, armour.Shield):
            armour_class += self.off_hand.armour_class_modifier
        elif isinstance(self.main_hand, armour.Shield):
            armour_class += self.main_hand.armour_class_modifier
        return armour_class

    @property
    def base_armour_class(self) -> int:
        return super().armour_class

    @property
    def base_movement_rate(self) -> int:
        return super().movement_rate

    @property
    def main_hand(self):
        return self.__main_hand

    @property
    def movement_rate(self) -> int:
        if isinstance(self.torso, armour.Armour):
            return self.torso.movement_rate
        return self.base_movement_rate

    @property
    def off_hand(self):
        return self.__off_hand

    @property
    def shoulders(self):
        return self.__shoulders

    @property
    def torso(self):
        return self.__torso

    @property
    def waist(self):
        return self.__waist

    def doff(self, item: Wearable) -> None:
        # TODO takes time…
        if self.__shoulders is item:
            self.__shoulders = None
        elif self.__torso is item:
            self.__torso = None
        elif self.__waist is item:
            self.__waist = None
        raise WearError()

    def don(self, item: Wearable) -> None:
        # TODO takes time…
        if item.on == 'shoulders':
            if self.__shoulders:
                raise WearError()
            self.__shoulders = item
        elif item.on == 'torso':
            if self.__torso:
                raise WearError()
            self.__torso = item
        elif item.on == 'waist':
            if self.__waist:
                raise WearError()
            self.__waist = item

    def drop(self, item: Holdable) -> None:
        if self.__main_hand is item:
            self.__main_hand = None
            if self.__off_hand is item:
                self.__off_hand = None
        elif self.__off_hand is item:
            self.__off_hand = None
        else:
            raise HoldError()

    def hold(self, item: Holdable, hand: str = 'any') -> None:
        if hand not in ('main', 'off'):
            hand = 'off' if self.main_hand else 'main'
        if hand == 'main':
            if self.main_hand:
                raise HoldError()
            if isinstance(item, DualHanded):
                if self.off_hand:
                    raise HoldError()
                self.__off_hand = item
            self.__main_hand = item
        if hand == 'off':
            if self.off_hand:
                raise HoldError()
            if isinstance(item, DualHanded):
                if self.main_hand:
                    raise HoldError()
                self.__main_hand = item
            self.__off_hand = item


class Person:
    pass
