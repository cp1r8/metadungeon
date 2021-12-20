#!/usr/bin/env python3

from game import d4, d6
from game.adventure import Door, Dungeon, Location, Party, Passage, Stairway
from game.armour import Armour, Shield
from game.characters import Adventurer
from game.containers import Backpack, Belt, ResourceContainer, StorageContainer
from game.creatures import Creature
from game.objects import Heavy, Stowable, TwoHanded
from game.supplies import Supply
from game.tools import ImprovisedWeapon
from game.valuables import Gold
from game.weapons import Missile, Weapon
from pathlib import Path

import pickle
import sys


# paragon = flawless diamond, no inclusions, at least 100 carats (20g) mass
# 1600 "coins" = 160 lbs = ~72.6 kg
# 1200 "coins" = 120 lbs = ~54.4 kg
# 600 "coins" = 60 lbs = ~27.2 kg
# 400 "coins" = 40 lbs = ~18.1 kg
# 100 "coins" = 10 lbs = ~4.54 kg
# 10 "coins" = 1 lbs = ~454 g
# 1 "coin" = ~45 g
# 1 troy ounce = ~31 g
# 1 carat = ~0.20 g
# 1 stone = ~6.35 kg = 141 "coins"
# 6 stone = ~38.1 kg
# 9 stone = ~57.2 kg
# 12 stone = ~76.2 kg
# 15 stone = ~95.3 kg
# 1p = 3.56g
# 2p = 7.12g
# 5p = 3.25g
# 10p = 6.5g
# 20p = 5.0g
# 50p = 8.0g
# £1 = 8.75g
# £2 = 12.0g
# 1 denarius (10 assēs) = 3.41-3.90g silver
# 1 penny (24 grains, 1/20 ozt) = 1.56g
# cp sp ep gp pp pg sg eg rg dg
# ¢  $  €  ¥  £  ☻  ♠  ♣  ♥  ♦


def hit_boxes(char: Creature):
    boxes = (['□'] * char.hits_remaining)
    if char.partial_hit:
        boxes += ['◩']
    boxes += (['■'] * char.hits_taken)
    if char.hit_die_modifier:
        boxes[-1] += f"{char.hit_die_modifier:+d}"
    return ' '.join(boxes)


def print_inventory(char: Adventurer, full: bool = False):

    inventory = {}

    if char.main_hand:
        if isinstance(char.main_hand, TwoHanded):
            if char.main_hand is char.off_hand:
                inventory['%'] = char.main_hand
            else:
                inventory['/'] = char.main_hand
        else:
            inventory['>'] = char.main_hand
    if char.off_hand and char.off_hand is not char.main_hand:
        inventory['<'] = char.off_hand
    if full and char.torso:
        inventory['['] = char.torso
    if full and char.waist:
        inventory['~'] = char.waist
    if full and char.shoulders:
        inventory[']'] = char.shoulders

    for prefix, item in inventory.items():
        if isinstance(item, Belt):
            belt = item
            for item in belt.items:
                print_inventory_item(item, prefix)
        else:
            print_inventory_item(item, prefix)
            if full and isinstance(item, StorageContainer):
                container = item
                for item in container.items:
                    print_inventory_item(item)


def print_inventory_item(item, prefix: str = ' '):

    mass = '+' if isinstance(item, Heavy) else ' '
    name = type(item).__name__
    uses = ''

    if isinstance(item, Armour):
        name = f"AC{item.armour_class} MV{item.movement_rate} {name}"
    elif isinstance(item, Shield):
        name = f"AC{-item.armour_class_modifier:+d} {name}"
    elif isinstance(item, Weapon) and not isinstance(item, ImprovisedWeapon):
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

    if uses:
        print(f"{prefix}{mass}{name:<24} {uses:>9}")
    else:
        print(f"{prefix}{mass}{name}")

    if isinstance(item, Stowable):
        for _ in range(0, item.slots_required - 1):
            print(f" {mass} · · ·")


def print_location(location: Location):
    if (isinstance(location, Dungeon)):
        if location.flee:
            bearing = f"{location.y}-? FLEE!"
        elif location.lost:
            bearing = f"{location.y}-? LOST!"
        else:
            bearing = f"{location.y}-{location.x}"
        if isinstance(location.area, Door):
            if location.area.locked:
                area = 'Door: locked'
            elif location.area.stuck:
                area = 'Door: stuck'
            else:
                area = 'Door: open'
        elif isinstance(location.area, Passage):
            if location.area.ahead and location.area.branch:
                area = 'Passage branches'
            elif location.area.ahead:
                area = 'Passage ahead'
            elif location.area.branch:
                area = 'Passage turns'
            else:
                area = 'Dead end'
        elif isinstance(location.area, Stairway):
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
        print(f"{type(location).__name__} {bearing} {area}")
    else:
        print(type(location).__name__)
    print('-' * 36)
    print()


def print_statblock(char: Creature):

    statblock = ' '.join([
        # f"HD{char.hit_dice:d}{char.hit_die_modifier:+d}",
        f"TH{char.attack_target_value:d}",
        f"SV{char.save_target_value:d}",
        f"AC{char.armour_class:d}",
        f"MV{char.movement_rate:d}",
        f"ML{char.morale:d}",
        # AL, XP, NA, TT
    ])

    if isinstance(char, Adventurer) and char.copper_for_next_level > 0:
        next_level = char.copper_for_next_level / Gold.VALUE_IN_COPPER
        print(f"{statblock:<25} {next_level:8,.0f} ↑")
    else:
        print(statblock)


if __name__ == '__main__':

    game_file = Path.home() / 'game.pickle'

    if game_file.exists():
        with game_file.open('rb') as input:
            party = pickle.load(input)
    else:

        dungeon = Dungeon()

        if '--expert' in sys.argv:
            party = Party.expert(dungeon, d4() + 4)
        else:
            party = Party.basic(dungeon, d4() + 4)

        if '--hit' in sys.argv:
            for adventurer in party.members:
                adventurer.hit(1)

        if '--loot' in sys.argv:
            # TODO TT U+V
            for adventurer in party.members:
                if isinstance(adventurer.shoulders, Backpack):
                    adventurer.shoulders.store(Gold(3*d6() * 10))

    actions = party.location.actions(party)

    for arg in sys.argv:
        if arg in actions:
            getattr(party.location, arg)(party)
            break

    print_location(party.location)

    for adventurer in party.members:
        print(f"{adventurer.handle:<9} {hit_boxes(adventurer):>26}")
        if '--stats' in sys.argv:
            print_statblock(adventurer)
        if '--inventory' in sys.argv:
            print_inventory(adventurer, True)
            print('-' * 36)
        elif '--arms' in sys.argv:
            print_inventory(adventurer)
            print('-' * 36)
        print()

    with game_file.open('wb') as output:
        pickle.dump(party, output)

    if '--actions' in sys.argv:
        actions = party.location.actions(party)
        print(' / '.join(actions))
