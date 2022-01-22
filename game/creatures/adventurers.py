# -*- coding: utf-8 -*-

from . import Unit
from .. import Place
from ..dice import d3, d4, d6
from ..objects import armour, containers, supplies, tools, valuables, weapons
from .humans import Human
from random import choice


class Adventurer(Human):

    # TODO Disadvantage using armour/shields and/or using weapons other than club, dagger, or staff

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

    # TT = [U, V]

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
    def gold_for_next_level(self) -> float:
        return self.copper_for_next_level / valuables.Gold.VALUE_IN_COPPER

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
            f".{self.id:04X}",
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
    def prefix(self) -> str:
        return 'NH'

    @property
    def save_target_value(self) -> int:
        return self.SV_BY_WIS[self.__wis - 3]

    # TODO level up
    # TODO Adventurer must select a character class after gaining XP on an adventure.

    @classmethod
    def generate(cls, level: int, auto_equip: bool = True) -> 'Adventurer':

        if cls is Adventurer and level > 0:
            cls = choice([Fighter, Fighter, Muser, Thief])

        adventurer = cls(
            *(sum(3*d6) for _ in range(6)),
            level=0 if cls is Adventurer else max(1, level),
        )

        if auto_equip:
            adventurer.__auto_equip()
        else:
            adventurer.__belt_and_money()

        return adventurer

    def random_adventuring_gear(self, roll: int) -> list:
        if roll <= 3:
            return [supplies.Rope(supplies.Rope.ITEMS_PER_SLOT)]
        if roll <= 4:
            return [tools.Crowbar()]
        if roll <= 5:
            return [tools.Pole()]
        return [tools.Mallet(), supplies.Spikes(supplies.Spikes.ITEMS_PER_SLOT)]

    def random_armour(self, roll: int) -> list:
        return []

    def random_essentials(self, roll: int) -> list:
        return [
            supplies.Rations(supplies.Rations.ITEMS_PER_SLOT),
            supplies.Sundries(supplies.Sundries.ITEMS_PER_SLOT),
            tools.Tinderbox(),
        ]

    def random_extra_gear(self, roll: int) -> list:
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

    def random_fill_belt(self, belt: containers.Belt) -> None:
        skin = containers.Waterskin()
        skin.store(supplies.Water(containers.Waterskin.CAPACITY))
        belt.store(skin)

    def random_fill_pack(self, pack: containers.Backpack) -> None:
        for item in self.random_essentials(d6()):
            pack.store(item)
        for item in self.random_light_source(d6()):
            pack.store(item)
        for item in self.random_adventuring_gear(d6()):
            pack.store(item)
        for item in self.random_extra_gear(d6()):
            pack.store(item)

    def random_light_source(self, roll: int):
        if roll <= 3:
            return [supplies.Torches(supplies.Torches.ITEMS_PER_SLOT)]
        if roll <= 4:
            lantern = tools.Lantern()
            lantern.store(supplies.Oil(lantern.capacity))
            return [lantern]
        lantern = tools.Lantern()
        lantern.store(supplies.Oil(lantern.capacity))
        return [lantern, containers.Flask.of(supplies.Oil())]

    def random_primary_weapons(self, roll: int):
        if roll <= 2:
            return [weapons.Club()]
        if roll <= 4:
            return [weapons.Staff()]
        return [weapons.Dagger()]

    def random_starting_funds(self, roll: int) -> list:
        return [valuables.Gold(roll * 10)]

    def __auto_equip(self) -> None:
        belt = containers.Belt()
        self.random_fill_belt(belt)
        self.don(belt)
        pack = containers.Backpack()
        self.random_fill_pack(pack)
        self.don(pack)
        for item in self.random_armour(d6()):
            self.don(item)
        for item in self.random_primary_weapons(d6()):
            self.hold(item)

    def __belt_and_money(self) -> None:
        belt = containers.Belt()
        for item in self.random_starting_funds(sum(3*d6)):
            belt.store(item)
        self.don(belt)


class Fighter(Adventurer):
    '''Adventurers dedicated to mastering the arts of combat and war.'''

    # TODO Fighters can use all types of weapons and armour.

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
        return self.XP_NEXT_LV[min(self.level, 9) - 1] if self.level < 14 else 0

    @property
    def hit_dice(self) -> int:
        if self.level <= 9:
            return self.level
        return 9 + ((self.level - 9) // 2)

    @property
    def hit_die_modifier(self) -> int:
        if self.level == 1:
            return +1
        if self.level <= 9:
            return +0
        return +2 * ((self.level + 1) % 2)

    @property
    def morale_rating(self) -> int:
        if self.level < 4:
            return super().morale_rating
        if self.level < 7:
            return super().morale_rating + 1
        if self.level < 10:
            return super().morale_rating + 2
        if self.level < 13:
            return super().morale_rating + 3
        return super().morale_rating + 4

    @property
    def prefix(self) -> str:
        return f"F{self.level:d}"

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

    def random_armour(self, roll: int) -> list:
        if roll <= 1:
            return []
        if roll <= 3:
            return [armour.Leather()]
        if roll <= 5:
            return [armour.Chain()]
        return [armour.Plate()]

    def random_fill_belt(self, belt: containers.Belt) -> None:
        super().random_fill_belt(belt)
        for item in self.random_secondary_weapons(d6()):
            belt.store(item)

    def random_primary_weapons(self, roll: int) -> list:
        if roll <= 3:
            roll = d6()
            if roll <= 1:
                return [weapons.Javelin()]
            if roll <= 2:
                bow = weapons.Longbow()
                bow.store(supplies.Arrows(bow.capacity))
                return [bow]
            if roll <= 3:
                bow = weapons.Crossbow()
                bow.store(supplies.Quarrels(bow.capacity))
                return [bow]
            if roll <= 4:
                return [weapons.Battleaxe()]
            if roll <= 5:
                return [weapons.Greatsword()]
            return [weapons.Polearm()]
        else:
            roll = d6()
            if roll <= 1:
                return [weapons.Dagger(), armour.Shield()]
            if roll <= 2:
                return [weapons.Axe(), armour.Shield()]
            if roll <= 3:
                return [weapons.Maul(), armour.Shield()]
            if roll <= 4:
                return [weapons.Shortsword(), armour.Shield()]
            if roll <= 5:
                return [weapons.Spear(), armour.Shield()]
            return [weapons.Sword(), armour.Shield()]

    def random_secondary_weapons(self, roll: int) -> list:
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
    '''Adventurers whose study of arcane secrets has taught them how to invoke algorithms.'''

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
        return self.XP_NEXT_LV[min(self.level, 9) - 1] if self.level < 14 else 0

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
    def morale_rating(self) -> int:
        if self.level < 6:
            return super().morale_rating
        if self.level < 11:
            return super().morale_rating + 1
        return super().morale_rating + 2

    @property
    def prefix(self) -> str:
        return f"M{self.level:d}"

    @property
    def save_target_value(self) -> int:
        if self.level < 6:
            return super().save_target_value
        if self.level < 11:
            return super().save_target_value - 2
        return super().save_target_value - 5

    def random_compound(self, roll: int) -> list:
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

    def random_fill_belt(self, belt: containers.Belt) -> None:
        super().random_fill_belt(belt)
        for item in self.random_compound(d6()):
            belt.store(item)
        # TODO codex and V1 algorithm

    def random_primary_weapons(self, roll: int) -> list:
        if roll <= 1:
            return [weapons.Staff()]
        if roll <= 5:
            return [weapons.Dagger()]
        return [weapons.SilverDagger()]


class Thief(Adventurer):
    '''Adventurers who live by their skills of deception and stealth.'''

    # TODO Back-stab: When attacking an unaware opponent from behind, +4 bonus to hit and double damage.
    # TODO Disadvantage if using shield or heavy armour; can use any weapon
    # TODO Luck?

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
        return self.XP_NEXT_LV[min(self.level, 9) - 1] if self.level < 14 else 0

    @property
    def hit_dice(self) -> int:
        return (self.level + 1) // 2

    @property
    def hit_die_modifier(self) -> int:
        if self.level < 9:
            return (self.level + 1) % 2
        return +2 * ((self.level + 1) % 2)

    @property
    def morale_rating(self) -> int:
        if self.level < 5:
            return super().morale_rating
        if self.level < 9:
            return super().morale_rating + 1
        if self.level < 13:
            return super().morale_rating + 2
        return super().morale_rating + 3

    @property
    def prefix(self) -> str:
        return f"T{self.level:d}"

    @property
    def save_target_value(self) -> int:
        if self.level < 5:
            return super().save_target_value
        if self.level < 9:
            return super().save_target_value - 2
        if self.level < 13:
            return super().save_target_value - 4
        return super().save_target_value - 6

    def random_armour(self, roll: int) -> list:
        if roll <= 3:
            return []
        return [armour.Leather()]

    def random_fill_belt(self, belt: containers.Belt) -> None:
        super().random_fill_belt(belt)
        belt.store(weapons.Dagger())

    def random_fill_pack(self, pack: containers.Backpack) -> None:
        super().random_fill_pack(pack)
        for item in self.random_specialist_gear(d6()):
            pack.store(item)

    def random_primary_weapons(self, roll: int) -> list:
        if roll <= 1:
            return [weapons.Club()]
        if roll <= 4:
            return [weapons.Dagger()]
        if roll <= 5:
            return [weapons.Shortsword()]
        bow = weapons.Shortbow()
        bow.store(supplies.Arrows(bow.capacity))
        return [bow]

    def random_specialist_gear(self, roll: int) -> list:
        if roll <= 1:
            return [containers.DrySack()]
        if roll <= 3:
            return [tools.Grapnel()]
        return [tools.Lockpicks()]


class Party(Unit[Adventurer]):

    CLASS_EXPERT_LEVELS = {
        # Barbarian: 1*d6+6, # Dwarf
        # Bard: 1*d6+2, # Elf
        # Cleric: 1*d6+3,
        Fighter: 1*d6+3,
        Fighter: 1*d6+5,
        # Ranger: 1*d6+2, # Halfling
        Muser: 1*d6+3,
        Thief: 1*d6+4,
    }

    def __init__(self, members: list[Adventurer], location: Place) -> None:
        super().__init__(members, location)
        self.flee = False
        self.lost = False

    @classmethod
    def assemble(cls, level: int, members: int, location: Place, auto_equip: bool = True) -> 'Party':
        return cls([
            Adventurer.generate(level, auto_equip) for _ in range(0, members)
        ], location)

    @classmethod
    def basic(cls, location: Place, auto_equip: bool = True) -> 'Party':
        return cls([
            Adventurer.generate(d3(), auto_equip) for _ in range(0, d4() + 4)
        ], location)

    @classmethod
    def expert(cls, location: Place, auto_equip: bool = True) -> 'Party':
        # TODO level by class
        # TODO Mounts: 75% chance of being mounted, in the wilderness.
        # TODO Special items: Per individual, there is a chance of the adventurer having a special item from each suitable special item sub-table.
        # The chance per sub-table is 5% per level of the NPC. Rolled items that cannot be used by the adventurer should be ignored (no re-roll).
        return cls([
            Adventurer.generate(d6() + 3, auto_equip) for _ in range(0, d6() + 3)
        ], location)

    # TODO Hihg


# FUTURE: Cleric class?
Cleric = Muser
