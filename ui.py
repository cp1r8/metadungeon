# -*- coding: utf-8 -*-

from game.creatures import Creature, Humanoid, Unit
from game.creatures.adventurers import Adventurer, Party
from game.objects import Heavy, Ranged, Stowable, TwoHanded
from game.objects.armour import Armour, Shield
from game.objects.containers import Belt, Container, ResourceContainer, StorageContainer
from game.objects.supplies import Supply
from game.objects.tools import ImprovisedWeapon, LightSource
from game.objects.weapons import Weapon
from math import ceil, floor


def abilities(char: Adventurer) -> str:
    return ' '.join([
        f"LV:{char.level:d}",
        f"ST:{char.abilities['ST']:d}",
        f"IN:{char.abilities['IN']:d}",
        f"WI:{char.abilities['WI']:d}",
        f"DE:{char.abilities['DE']:d}",
        f"CO:{char.abilities['CO']:d}",
        f"CH:{char.abilities['CH']:d}",
    ])


def health_bar(char: Creature, width: int, full: str = '#', hit: str = '-', wound: str = ' ') -> str:

    if char.hit_dice == 0:
        return (wound * width) if char.hits_taken else (full * width)

    if char.hits_taken < char.hit_dice:
        hits = char.hits_taken + (0.5 if char.partial_hit else 0)
        health = full * floor(width * (char.hit_dice - hits) / char.hit_dice)
        return health + (hit * ceil(width * hits / char.hit_dice))

    wounds = char.hits_taken - char.hit_dice

    if wounds >= char.hit_dice:
        return wound * width

    survive = hit * floor(width * (char.hit_dice - wounds) / char.hit_dice)

    return survive + (wound * ceil(width * wounds / char.hit_dice))


def print_inventory(char: Humanoid, full: bool = False):

    inventory = {}

    if full and char.torso:
        inventory['['] = char.torso
    if char.main_hand:
        if char.main_hand is char.off_hand:
            inventory['%'] = char.main_hand
        elif isinstance(char.main_hand, TwoHanded):
            inventory['/'] = char.main_hand
        else:
            inventory['>'] = char.main_hand
    if char.off_hand and char.off_hand is not char.main_hand:
        if isinstance(char.off_hand, TwoHanded):
            inventory['\\'] = char.off_hand
        else:
            inventory['<'] = char.off_hand
    if full and char.waist:
        inventory['-'] = char.waist
    if full and char.shoulders:
        inventory[']'] = char.shoulders

    for prefix, item in inventory.items():
        if isinstance(item, Belt):
            container = item
            for item in container.contents:
                print_inventory_item(item, prefix)
                if full and isinstance(item, Container):
                    container = item
                    for item in container.contents:
                        print_inventory_item(item)
        else:
            print_inventory_item(item, prefix)
            if full and isinstance(item, Container):
                container = item
                for item in container.contents:
                    print_inventory_item(item)


def print_inventory_item(item, prefix: str = ' '):

    mass = '=' if isinstance(item, Heavy) else ' '
    name = type(item).__name__
    uses = ''

    if isinstance(item, Armour):
        name = f"AC{item.armour_class} MV{item.movement_rate} {name}"
    elif isinstance(item, Shield):
        name = f"AC{-item.armour_class_modifier:+d} {name}"
    elif isinstance(item, Weapon) and \
            (not isinstance(item, ImprovisedWeapon) or prefix in ('%', '>', '/')):
        if isinstance(item, Ranged):
            name = f"@{item.ranges[0]} {name}"
        name = f"D{item.damage} {name}"

    if isinstance(item, ResourceContainer):
        if item.contents is type(None):
            name = f"{name}: empty"
        else:
            name = f"{name}: {item.contents.__name__.lower()}"
            if item.capacity > 9:
                uses = f"{item.quantity:d}"
            elif item.capacity:
                uses = ('○' * item.quantity) + ('●' * item.capacity_free)
    elif isinstance(item, Container):
        if item.is_empty:
            name = f"{name} (empty)"
        elif prefix == ' ':
            name = f"{name} ({item.items:d} items)"
        else:
            name = f"{name}:"
    elif isinstance(item, LightSource):
        if item.lit:
            uses = '***'
    elif isinstance(item, Supply):
        if item.items_per_slot > 10:
            uses = f"{item.quantity:d}"
        elif item.items_per_slot > 1:
            spent = item.items_per_slot - item.quantity
            uses = ('○' * (item.quantity - 1)) + ('●' * spent)

    print(f"{prefix}{mass}{name:<27}{uses:>10}")

    if isinstance(item, Stowable):
        for _ in range(0, item.slots_required - 1):
            print(f" {mass} · · ·")


def statblock(char: Creature) -> str:

    stats = []

    if char.armour_class == char.base_armour_class:
        stats.append(f"AC:{char.armour_class:d}")
    else:
        stats.append(f"AC{char.base_armour_class:d}:{char.armour_class:d}")

    # TODO partial HD
    stats.append(f"HD:{char.hit_dice:d}{char.hit_die_modifier:+d}")
    stats.append(f"TH:{char.attack_target_value:d}")

    if char.movement_rate == char.base_movement_rate:
        stats.append(f"MV:{char.movement_rate:d}")
    else:
        stats.append(f"MV{char.base_movement_rate:d}:{char.movement_rate:d}")

    stats.append(f"SV:{char.save_target_value:d}")

    if char.morale_rating == char.base_morale_rating:
        stats.append(f"ML:{char.morale_rating:d}")
    else:
        stats.append(f"ML{char.base_morale_rating:d}:{char.morale_rating:d}")

    return ' '.join(stats)


def unitstats(unit: Unit):

    stats = []

    if isinstance(unit, Party):
        stats.append(f"LV:{unit.level}")

    stats.append(f"HD:{unit.hit_dice:d}")
    stats.append(f"MV:{unit.movement_rate:d}")

    return ' '.join(stats)
