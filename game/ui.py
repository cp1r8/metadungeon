# -*- coding: utf-8 -*-

from game.creatures.humans import Human
from .adventure import Location
from .adventure.underground import Dungeon
from .creatures import Creature, Humanoid
from .creatures.adventurers import Adventurer
from .objects import Heavy, Stowable, TwoHanded
from .objects.armour import Armour, Shield
from .objects.containers import Belt, ResourceContainer, StorageContainer
from .objects.supplies import Supply
from .objects.tools import ImprovisedWeapon
from .objects.weapons import Missile, Weapon
from math import ceil, floor


def handle(char: Creature) -> str:
    if hasattr(char, 'name'):
        return getattr(char, 'name')
    if isinstance(char, Adventurer):
        return char.handle
    return type(char).__name__


def health_bar(char: Creature, width: int) -> str:
    if char.hit_dice == 0:
        return ('·' * width) if char.hits_taken else ('█' * width)
    if char.hits_taken < char.hit_dice:
        hits = char.hits_taken + (0.5 if char.partial_hit else 0)
        health = '█' * floor(width * (char.hit_dice - hits) / char.hit_dice)
        return health + ('▒' * ceil(width * hits / char.hit_dice))
    wounds = char.hits_taken - char.hit_dice
    if wounds >= char.hit_dice:
        return '·' * width
    survive = '▒' * floor(width * (char.hit_dice - wounds) / char.hit_dice)
    return survive + ('·' * ceil(width * wounds / char.hit_dice))


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
        inventory['~'] = char.waist
    if full and char.shoulders:
        inventory[']'] = char.shoulders

    for prefix, item in inventory.items():
        if isinstance(item, Belt):
            container = item
            for item in container.items:
                print_inventory_item(item)
        else:
            print_inventory_item(item, prefix)
            if full and isinstance(item, StorageContainer):
                container = item
                for item in container.items:
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
        if isinstance(item, Missile):
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
    elif isinstance(item, StorageContainer):
        if item.is_empty:
            name = f"{name} (empty)"
        elif prefix == ' ':
            name = f"{name} ({len(item.items):d} items)"
        else:
            name = f"{name}:"
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


def print_dungeon_area(location: Dungeon):

    if location.flee:
        bearing = f"{location.z}-? FLEE!"
    elif location.lost:
        bearing = f"{location.z}-? LOST!"
    else:
        bearing = f"{location.z}-{location.y}"

    if isinstance(location.area, Dungeon.Door):
        if location.area.locked:
            area = 'Door: locked'
        elif location.area.stuck:
            area = 'Door: stuck'
        else:
            area = 'Door: open'
    elif isinstance(location.area, Dungeon.Passage):
        if location.area.ahead and location.area.branch:
            area = 'Passage branches'
        elif location.area.ahead:
            area = 'Passage ahead'
        elif location.area.branch:
            area = 'Passage turns'
        else:
            area = 'Dead end'
    elif isinstance(location.area, Dungeon.Stairway):
        if location.area.up and location.area.down:
            area = 'Stairs up/down'
        elif location.area.up:
            area = 'Stairs up'
        elif location.area.down:
            area = 'Stairs down'
        else:
            area = 'Stairs blocked'
    else:
        area = type(location.area).__name__

    print(f"{bearing} {area}")


def statblock(char: Creature):
    stats = [
        f"HD:{char.hit_dice:d}{char.hit_die_modifier:+d}",
        f"TH:{char.attack_target_value:d}",
        f"SV:{char.save_target_value:d}",
    ]

    if char.armour_class == char.base_armour_class:
        stats.append(f"AC:{char.armour_class:d}")
    else:
        stats.append(f"AC{char.base_armour_class:d}:{char.armour_class:d}")

    if char.movement_rate == char.base_movement_rate:
        stats.append(f"MV:{char.movement_rate:d}")
    else:
        stats.append(f"MV{char.base_movement_rate:d}:{char.movement_rate:d}")

    if char.morale_rating == char.base_morale_rating:
        stats.append(f"ML:{char.morale_rating:d}")
    else:
        stats.append(f"ML{char.base_morale_rating:d}:{char.morale_rating:d}")

    return ' '.join(stats)
