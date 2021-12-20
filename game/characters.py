# -*- coding: utf-8 -*-

from . import d4, d6, d10
from .armour import Armour, Chain, Leather, Plate, Shield
from .containers import Backpack, Belt, DrySack, Flask, LargeSack, SmallSack, Vial, Waterskin
from .humanoids import Human
from .supplies import Acid, Arrows, Gunpowder, Liquor, Oil, Poison, Quarrels, Rations, Rope, Stones, Smoke, Spikes, Sundries, Torches, Water
from .tools import Crowbar, Grapnel, Lantern, Lockpicks, Mallet, Mirror, Pole, Tinderbox
from .valuables import Gold, Silver
from .weapons import Axe, Battleaxe, Club, Crossbow, Dagger, Greatsword, Longbow, Maul, Polearm, Shortsword, Shortbow, SilverDagger, Sling, Spear, Staff, Sword


class Adventurer(Human):

    AC_BY_DEX = (11, 11, 11, 10, 10, 10, 9, 9,
                 9, 9, 8, 8, 8, 7, 7, 7)
    ML_BY_CHA = (6, 6, 6, 6, 6, 6, 7, 7,
                 7, 7, 8, 8, 8, 8, 8, 8)
    MV_BY_CON = (9, 9, 9, 12, 12, 12, 12, 12,
                 12, 12, 12, 12, 12, 15, 15, 15)
    SV_BY_WIS = (16, 16, 16, 15, 15, 15, 14, 14,
                 14, 14, 13, 13, 13, 12, 12, 12)
    TH_BY_STR = (21, 21, 21, 20, 20, 20, 19, 19,
                 19, 19, 18, 18, 18, 17, 17, 17)
    XR_BY_INT = (120, 120, 120, 110, 110, 110, 100, 100,
                 100, 100, 95, 95, 95, 90, 90, 90)

    # XP_VALUE_IN_COPPER = Silver.VALUE_IN_COPPER
    XP_VALUE_IN_COPPER = Gold.VALUE_IN_COPPER

    def __init__(
        self,
        strength: int,
        intelligence: int,
        wisdom: int,
        dexterity: int,
        constitution: int,
        charisma: int,
        level: int
    ) -> None:
        super().__init__()
        self.__str = strength
        self.__int = intelligence
        self.__wis = wisdom
        self.__dex = dexterity
        self.__con = constitution
        self.__cha = charisma
        self.__lvl = level

    @property
    def armour_class(self) -> int:
        if isinstance(self.torso, Armour):
            armour_class = self.torso.armour_class
        else:
            armour_class = self.base_armour_class
        if isinstance(self.off_hand, Shield):
            armour_class += self.off_hand.armour_class_modifier
        elif isinstance(self.main_hand, Shield):
            armour_class += self.main_hand.armour_class_modifier
        return armour_class

    @property
    def attack_target_value(self) -> int:
        return self.TH_BY_STR[self.__str - 3]

    @property
    def base_armour_class(self) -> int:
        return self.AC_BY_DEX[self.__dex - 3]

    @property
    def base_movement_rate(self) -> int:
        return self.MV_BY_CON[self.__con - 3]

    @property
    def copper_for_next_level(self) -> int:
        return int(self.experience_for_next_level * self.experience_rate * self.XP_VALUE_IN_COPPER)

    @property
    def experience_for_next_level(self) -> int:
        return 0

    @property
    def experience_rate(self) -> int:
        return self.XR_BY_INT[self.__int - 3]  # percent

    @property
    def handle(self) -> str:
        return ''.join([
            f"{self.prefix}-",
            f"{self.__str-3:X}",
            f"{self.__int-3:X}",
            f"{self.__wis-3:X}",
            f"{self.__dex-3:X}",
            f"{self.__con-3:X}",
            f"{self.__cha-3:X}",
        ])

    @property
    def hit_dice(self) -> int:
        return 1

    @property
    def hit_die_modifier(self) -> int:
        return +0

    @property
    def level(self) -> int:
        return self.__lvl

    @property
    def morale(self) -> int:
        return self.ML_BY_CHA[self.__cha - 3]

    @property
    def movement_rate(self) -> int:
        if isinstance(self.torso, Armour):
            return self.torso.movement_rate
        return self.base_movement_rate

    @property
    def prefix(self) -> str:
        return 'NH'

    @property
    def save_target_value(self) -> int:
        return self.SV_BY_WIS[self.__wis - 3]

    # TODO level up

    def auto_equip(self) -> None:
        belt = Belt()
        self.don(belt)
        skin = Waterskin()
        belt.store(skin)
        skin.store(Water(2))
        pack = Backpack()
        self.don(pack)
        pack.store(Rations(Rations.ITEMS_PER_SLOT))
        pack.store(Sundries(Sundries.ITEMS_PER_SLOT))
        pack.store(Tinderbox())
        for item in self.__random_light_source(d6()):
            pack.store(item)
        for item in self.__random_adventuring_gear(d6()):
            pack.store(item)
        for item in self.__random_extra_gear(d6()):
            pack.store(item)

    def __random_adventuring_gear(self, roll: int) -> list:
        if roll <= 3:
            return [Rope(Rope.ITEMS_PER_SLOT)]
        if roll <= 4:
            return [Crowbar()]
        if roll <= 5:
            return [Pole()]
        return [Mallet(), Spikes(Spikes.ITEMS_PER_SLOT)]

    def __random_extra_gear(self, roll: int) -> list:
        if roll <= 1:
            return [SmallSack()]
        if roll <= 2:
            return [Flask.of(Oil())]
        if roll <= 3:
            return [Mirror()]
        if roll <= 4:
            return [Rations(7)]
        if roll <= 5:
            return [Rope(Rope.ITEMS_PER_SLOT)]
        return [LargeSack()]

    def __random_light_source(self, roll: int):
        if roll <= 3:
            return [Torches(Torches.ITEMS_PER_SLOT)]
        if roll <= 4:
            lantern = Lantern()
            lantern.store(Oil(lantern.capacity))
            return [lantern]
        lantern = Lantern()
        lantern.store(Oil(lantern.capacity))
        return [lantern, Flask.of(Oil())]

    @classmethod
    def random(cls, level: int) -> 'Adventurer':
        if cls is Adventurer and level > 0:
            cls = cls.__random_class(d4())
        return cls(*(3*d6() for _ in range(6)), level=level)

    @classmethod
    def __random_class(cls, roll: int) -> type:
        if roll <= 2:
            return Fighter
        if roll <= 3:
            return Muser
        return Thief


class Fighter(Adventurer):

    XP_NEXT_LV = (20, 20, 40, 80, 160, 320, 640, 1200, 1200)

    @property
    def attack_target_value(self) -> int:
        if self.level < 4:
            return super().attack_target_value
        if self.level < 7:
            return super().attack_target_value - 2
        if self.level < 10:
            return super().attack_target_value - 5
        if self.level < 13:
            return super().attack_target_value - 7
        return super().attack_target_value - 9

    @property
    def experience_for_next_level(self) -> int:
        return self.XP_NEXT_LV[min(self.level, 9) - 1] if self.level < 15 else 0

    @property
    def hit_dice(self) -> int:
        if self.level < 10:
            return self.level
        return 9 + ((self.level - 10) // 2)

    @property
    def hit_die_modifier(self) -> int:
        if self.level < 2:
            return +1
        if self.level < 10:
            return +0
        return +2 * ((self.level + 1) % 2)

    @property
    def prefix(self) -> str:
        return f"F{self.level:X}"

    @property
    def save_target_value(self) -> int:
        if self.level < 4:
            return super().save_target_value
        if self.level < 7:
            return super().save_target_value - 2
        if self.level < 10:
            return super().save_target_value - 4
        if self.level < 13:
            return super().save_target_value - 6
        return super().save_target_value - 7

    def auto_equip(self) -> None:
        super().auto_equip()
        for item in self.__random_armour(d6()):
            self.don(item)
        for item in self.__random_primary_weapons(d10()):
            self.hold(item)
        if isinstance(self.waist, Belt):
            for item in self.__random_secondary_weapons(d6()):
                self.waist.store(item)

    def __random_armour(self, roll: int) -> list:
        if roll <= 1:
            return []
        if roll <= 3:
            return [Leather()]
        if roll <= 5:
            return [Chain()]
        return [Plate()]

    def __random_primary_weapons(self, roll: int) -> list:
        if roll <= 1:
            return [Axe(), Shield()]
        if roll <= 2:
            return [Maul(), Shield()]
        if roll <= 3:
            return [Shortsword(), Shield()]
        if roll <= 4:
            return [Spear(), Shield()]
        if roll <= 5:
            return [Sword(), Shield()]
        if roll <= 6:
            bow = Crossbow()
            bow.store(Quarrels(bow.capacity))
            return [bow]
        if roll <= 7:
            bow = Longbow()
            bow.store(Arrows(bow.capacity))
            return [bow]
        if roll <= 8:
            return [Battleaxe()]
        if roll <= 9:
            return [Greatsword()]
        return [Polearm()]

    def __random_secondary_weapons(self, roll: int) -> list:
        if roll <= 1:
            return []
        if roll <= 2:
            return [Club()]
        if roll <= 3:
            return [Dagger()]
        if roll <= 5:
            sling = Sling()
            sling.store(Stones(sling.capacity))
            return [sling]
        bow = Shortbow()
        bow.store(Arrows(bow.capacity))
        return [bow]


class Muser(Adventurer):

    XP_NEXT_LV = (25, 25, 50, 100, 200, 400, 700, 1500, 1500)

    @property
    def attack_target_value(self) -> int:
        if self.level < 6:
            return super().attack_target_value
        if self.level < 11:
            return super().attack_target_value - 2
        return super().attack_target_value - 5

    @property
    def experience_for_next_level(self) -> int:
        return self.XP_NEXT_LV[min(self.level, 9) - 1] if self.level < 15 else 0

    @property
    def hit_dice(self) -> int:
        if self.level < 9:
            return (self.level + 1) // 2
        return 5 + ((self.level - 9) // 3)

    @property
    def hit_die_modifier(self) -> int:
        if self.level < 10:
            return (self.level + 1) % 2
        return +1 * (self.level % 3)

    @property
    def prefix(self) -> str:
        return f"M{self.level:X}"

    @property
    def save_target_value(self) -> int:
        if self.level < 6:
            return super().save_target_value
        if self.level < 11:
            return super().save_target_value - 2
        return super().save_target_value - 5

    def auto_equip(self) -> None:
        super().auto_equip()
        for item in self.__random_weapon(d6()):
            self.hold(item)
        if isinstance(self.waist, Belt):
            for item in self.__random_compound(d6()):
                self.waist.store(item)
        # TODO codex and L1 algorithm

    def __random_compound(self, roll: int) -> list:
        if roll <= 1:
            return [Flask.of(Liquor())]
        if roll <= 2:
            return [Flask.of(Oil())]
        if roll <= 3:
            return [Vial.of(Acid())]
        if roll <= 4:
            return [Vial.of(Gunpowder())]
        if roll <= 5:
            return [Vial.of(Poison())]
        return [Vial.of(Smoke())]

    def __random_weapon(self, roll: int) -> list:
        if roll <= 1:
            return [Staff()]
        if roll <= 5:
            return [Dagger()]
        return [SilverDagger()]


class Thief(Adventurer):

    XP_NEXT_LV = (12, 12, 24, 48, 100, 200, 400, 800, 1200)

    @property
    def attack_target_value(self) -> int:
        if self.level < 5:
            return super().attack_target_value
        if self.level < 9:
            return super().attack_target_value - 2
        if self.level < 13:
            return super().attack_target_value - 5
        return super().attack_target_value - 7

    @property
    def experience_for_next_level(self) -> int:
        return self.XP_NEXT_LV[min(self.level, 9) - 1] if self.level < 15 else 0

    @property
    def hit_dice(self) -> int:
        return (self.level + 1) // 2

    @property
    def hit_die_modifier(self) -> int:
        if self.level < 9:
            return (self.level + 1) % 2
        return +2 * ((self.level + 1) % 2)

    @property
    def prefix(self) -> str:
        return f"T{self.level:X}"

    @property
    def save_target_value(self) -> int:
        if self.level < 5:
            return super().save_target_value
        if self.level < 9:
            return super().save_target_value - 2
        if self.level < 13:
            return super().save_target_value - 4
        return super().save_target_value - 6

    def auto_equip(self) -> None:
        super().auto_equip()
        for item in self.__random_armour(d6()):
            self.don(item)
        for item in self.__random_weapon(d6()):
            self.hold(item)
        if isinstance(self.shoulders, Backpack):
            for item in self.__random_specialist_gear(d6()):
                self.shoulders.store(item)
        if isinstance(self.waist, Belt):
            self.waist.store(Dagger())

    def __random_armour(self, roll: int) -> list:
        if roll <= 3:
            return []
        return [Leather()]

    def __random_specialist_gear(self, roll: int) -> list:
        if roll <= 1:
            return [DrySack()]
        if roll <= 3:
            return [Grapnel()]
        return [Lockpicks()]

    def __random_weapon(self, roll: int) -> list:
        if roll <= 1:
            return [Club()]
        if roll <= 4:
            return [Dagger()]
        if roll <= 5:
            return [Shortsword()]
        bow = Shortbow()
        bow.store(Arrows(bow.capacity))
        return [bow]
