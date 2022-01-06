# -*- coding: utf-8 -*-

from .. import d4, d6, d10
from ..objects import armour, containers, supplies, tools, valuables, weapons
from .humanoids import Human


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

    # XP_VALUE_IN_COPPER = valuables.Silver.VALUE_IN_COPPER
    XP_VALUE_IN_COPPER = valuables.Gold.VALUE_IN_COPPER

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
    def morale_rating(self) -> int:
        return self.ML_BY_CHA[self.__cha - 3]

    @property
    def movement_rate(self) -> int:
        if isinstance(self.torso, armour.Armour):
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
        belt = containers.Belt()
        self.don(belt)
        skin = containers.Waterskin()
        belt.store(skin)
        skin.store(supplies.Water(containers.Waterskin.CAPACITY))
        pack = containers.Backpack()
        self.don(pack)
        pack.store(supplies.Rations(supplies.Rations.ITEMS_PER_SLOT))
        pack.store(supplies.Sundries(supplies.Sundries.ITEMS_PER_SLOT))
        pack.store(tools.Tinderbox())
        for item in self.__random_light_source(d6()):
            pack.store(item)
        for item in self.__random_adventuring_gear(d6()):
            pack.store(item)
        for item in self.__random_extra_gear(d6()):
            pack.store(item)

    def __random_adventuring_gear(self, roll: int) -> list:
        if roll <= 3:
            return [supplies.Rope(supplies.Rope.ITEMS_PER_SLOT)]
        if roll <= 4:
            return [tools.Crowbar()]
        if roll <= 5:
            return [tools.Pole()]
        return [tools.Mallet(), supplies.Spikes(supplies.Spikes.ITEMS_PER_SLOT)]

    def __random_extra_gear(self, roll: int) -> list:
        if roll <= 1:
            return [containers.SmallSack()]
        if roll <= 2:
            return [containers.Flask.of(supplies.Oil())]
        if roll <= 3:
            return [tools.Mirror()]
        if roll <= 4:
            return [supplies.Rations(7)]
        if roll <= 5:
            return [supplies.Rope(supplies.Rope.ITEMS_PER_SLOT)]
        return [containers.LargeSack()]

    def __random_light_source(self, roll: int):
        if roll <= 3:
            return [supplies.Torches(supplies.Torches.ITEMS_PER_SLOT)]
        if roll <= 4:
            lantern = tools.Lantern()
            lantern.store(supplies.Oil(lantern.capacity))
            return [lantern]
        lantern = tools.Lantern()
        lantern.store(supplies.Oil(lantern.capacity))
        return [lantern, containers.Flask.of(supplies.Oil())]

    @classmethod
    def random(cls, level: int) -> 'Adventurer':
        if cls is Adventurer and level > 0:
            cls = cls.__random_class(d4())
        return cls(*(sum(3*d6) for _ in range(6)), level=level)

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
        if isinstance(self.waist, containers.Belt):
            for item in self.__random_secondary_weapons(d6()):
                self.waist.store(item)

    def __random_armour(self, roll: int) -> list:
        if roll <= 1:
            return []
        if roll <= 3:
            return [armour.Leather()]
        if roll <= 5:
            return [armour.Chain()]
        return [armour.Plate()]

    def __random_primary_weapons(self, roll: int) -> list:
        if roll <= 1:
            return [weapons.Axe(), armour.Shield()]
        if roll <= 2:
            return [weapons.Maul(), armour.Shield()]
        if roll <= 3:
            return [weapons.Shortsword(), armour.Shield()]
        if roll <= 4:
            return [weapons.Spear(), armour.Shield()]
        if roll <= 5:
            return [weapons.Sword(), armour.Shield()]
        if roll <= 6:
            bow = weapons.Crossbow()
            bow.store(supplies.Quarrels(bow.capacity))
            return [bow]
        if roll <= 7:
            bow = weapons.Longbow()
            bow.store(supplies.Arrows(bow.capacity))
            return [bow]
        if roll <= 8:
            return [weapons.Battleaxe()]
        if roll <= 9:
            return [weapons.Greatsword()]
        return [weapons.Polearm()]

    def __random_secondary_weapons(self, roll: int) -> list:
        if roll <= 1:
            return []
        if roll <= 2:
            return [weapons.Club()]
        if roll <= 3:
            return [weapons.Dagger()]
        if roll <= 5:
            sling = weapons.Sling()
            sling.store(supplies.Stones(sling.capacity))
            return [sling]
        bow = weapons.Shortbow()
        bow.store(supplies.Arrows(bow.capacity))
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
        if isinstance(self.waist, containers.Belt):
            for item in self.__random_compound(d6()):
                self.waist.store(item)
        # TODO codex and L1 algorithm

    def __random_compound(self, roll: int) -> list:
        if roll <= 1:
            return [containers.Flask.of(supplies.Liquor())]
        if roll <= 2:
            return [containers.Flask.of(supplies.Oil())]
        if roll <= 3:
            return [containers.Vial.of(supplies.Acid())]
        if roll <= 4:
            return [containers.Vial.of(supplies.Gunpowder())]
        if roll <= 5:
            return [containers.Vial.of(supplies.Poison())]
        return [containers.Vial.of(supplies.Smoke())]

    def __random_weapon(self, roll: int) -> list:
        if roll <= 1:
            return [weapons.Staff()]
        if roll <= 5:
            return [weapons.Dagger()]
        return [weapons.SilverDagger()]


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
        if isinstance(self.shoulders, containers.Backpack):
            for item in self.__random_specialist_gear(d6()):
                self.shoulders.store(item)
        if isinstance(self.waist, containers.Belt):
            self.waist.store(weapons.Dagger())

    def __random_armour(self, roll: int) -> list:
        if roll <= 3:
            return []
        return [armour.Leather()]

    def __random_specialist_gear(self, roll: int) -> list:
        if roll <= 1:
            return [containers.DrySack()]
        if roll <= 3:
            return [tools.Grapnel()]
        return [tools.Lockpicks()]

    def __random_weapon(self, roll: int) -> list:
        if roll <= 1:
            return [weapons.Club()]
        if roll <= 4:
            return [weapons.Dagger()]
        if roll <= 5:
            return [weapons.Shortsword()]
        bow = weapons.Shortbow()
        bow.store(supplies.Arrows(bow.capacity))
        return [bow]
