# -*- coding: utf-8 -*-

from .. import Piece, Place
from ..dice import d6, d20
from ..objects import armour, containers, DualHanded, Holdable, Wearable
from ..objects.weapons import Weapon


class HoldError(ValueError):
    pass


class WearError(ValueError):
    pass


class Creature(Piece):

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

    AC = 9
    HD = 1
    HD_MOD = +0
    AT = []
    TH = 20
    MV = 12
    SV = 16
    ML = 6
    XP = 0
    TT = []

    def __init__(self, location: Place) -> None:
        super().__init__(location)
        self.__hits_taken = 0
        self.__partial_hit = False

    @property
    def armour_class(self) -> int:
        return self.base_armour_class

    @property
    def attack_target_value(self) -> int:
        return int(self.TH)

    @property
    def attacks(self) -> list:
        return self.AT

    @property
    def base_armour_class(self) -> int:
        return int(self.AC)

    @property
    def base_morale_rating(self) -> int:
        return int(self.ML)

    @property
    def base_movement_rate(self) -> int:
        return int(self.MV)

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
        return self.base_morale_rating

    @property
    def movement_rate(self) -> int:
        return self.base_movement_rate

    @property
    def partial_hit(self) -> bool:
        return self.__partial_hit

    @property
    def save_target_value(self) -> int:
        return int(self.SV)

    @property
    def treasure_types(self) -> list:
        return self.TT

    @classmethod
    def encounter(cls, location: Place, number_appearing: int) -> 'Unit':
        unit = Unit(location)
        for _ in range(0, number_appearing):
            unit.add(cls(unit))
        return unit

    def hit(self, damage: int) -> bool:
        while damage > 0 and self.hits_taken < self.hit_dice:
            absorb = d6()
            if self.hits_taken == 0:
                absorb = max(1, absorb + self.hit_die_modifier)
            damage -= absorb
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


class FlyingCreature(Creature):

    MV_FLY = 12

    def __init__(self, location: Place) -> None:
        super().__init__(location)
        self.__flying = False

    @property
    def fly_movement_rate(self) -> int:
        return int(self.MV_FLY)

    @property
    def flying(self) -> bool:
        return self.__flying

    @property
    def movement_rate(self) -> int:
        if self.flying:
            return self.fly_movement_rate
        return super().movement_rate

    def fly(self) -> None:
        self.__flying = True

    def land(self) -> None:
        self.__flying = False


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

        def __call__(self, roll: int) -> bool:
            if super().__call__(roll):
                if isinstance(self.source.main_hand, containers.ResourceContainer):
                    self.source.main_hand.remove(1)
                return True
            return False

    AT = [(Attack,)]
    HANDS = []
    TORSO = []
    WAIST = []

    def __init__(self, location: Place) -> None:
        super().__init__(location)
        self.__main_hand = None
        self.__off_hand = None
        self.__shoulders = None
        self.__torso = None
        self.__waist = None
        self.__equip()

    @property
    def armour_class(self) -> int:
        if isinstance(self.torso, armour.Armour):
            armour_class = self.torso.armour_class
        else:
            armour_class = super().armour_class
        if isinstance(self.off_hand, armour.Shield):
            armour_class += self.off_hand.armour_class_modifier
        elif isinstance(self.main_hand, armour.Shield):
            armour_class += self.main_hand.armour_class_modifier
        return armour_class

    @property
    def main_hand(self):
        return self.__main_hand

    @property
    def movement_rate(self) -> int:
        if isinstance(self.torso, armour.Armour):
            return self.torso.movement_rate
        return super().movement_rate

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
        # TODO takes time???
        if self.__shoulders is item:
            self.__shoulders = None
        elif self.__torso is item:
            self.__torso = None
        elif self.__waist is item:
            self.__waist = None
        raise WearError()

    def don(self, item: Wearable) -> None:
        # TODO takes time???
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

    def __equip(self) -> None:
        for item_type in self.HANDS:
            self.hold(item_type())
        for item_type in self.TORSO:
            self.don(item_type())
        if self.WAIST:
            belt = containers.Belt()
            for item_type in self.WAIST:
                belt.add(item_type())
            self.don(belt)


class Person:
    pass


class Unit(Place):

    @property
    def members(self) -> set[Creature]:
        return {entity for entity in self.entities if isinstance(entity, Creature)}

    @property
    def hit_dice(self) -> int:
        return sum(getattr(entity, 'hit_dice', 0) for entity in self.entities)

    @property
    def movement_rate(self) -> int:
        return min(getattr(entity, 'movement_rate', 0) for entity in self.entities)
