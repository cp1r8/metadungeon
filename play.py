#!/usr/bin/env python3

from game import World
from game.adventure.underground import Dungeon
from game.creatures import Creature, Humanoid
from game.creatures.adventurers import Adventurer, Party
from game.dice import d4
from pathlib import Path

import pickle
import sys
import ui


if __name__ == '__main__':

    game_file = Path.home() / '.local' / 'metadungeon.pickle'

    if game_file.exists() and '--reset' not in sys.argv:
        with game_file.open('rb') as input:
            world, party = pickle.load(input)
    else:

        world = World()

        if '--no-equip' in sys.argv:
            auto_equip = False
            # TODO start in town
            place = Dungeon()
        else:
            auto_equip = True
            place = Dungeon()

        world.establish(place)

        if '--basic' in sys.argv:
            party = Party.basic(place, auto_equip)
        elif '--expert' in sys.argv:
            party = Party.expert(place, auto_equip)
        elif '--funnel' in sys.argv:
            party = Party.assemble(0, sum(4*d4) + 4, place, auto_equip)
        else:
            party = Party.assemble(1, sum(2*d4) + 4, place, auto_equip)

    # for testing
    if '--hit' in sys.argv:
        damage = sys.argv.count('--hit')
        if (isinstance(party.place, Dungeon)):
            for item in party.place.area.content:
                if isinstance(item, Creature):
                    item.hit(damage)
        for char in party.members:
            char.hit(damage)

    actions = party.place.actions()

    for arg in sys.argv:
        if arg in actions:
            getattr(party.place, arg)()
            break

    print(f"{world.time} {type(party.place).__name__}")

    if (isinstance(party.place, Dungeon)):
        ui.print_dungeon_area(party.place)
        print('=' * 39)
        print()
        for item in party.place.area.content:
            if isinstance(item, Creature):
                print(f"{ui.handle(item):<18} {ui.health_bar(item, 20)}")
                if '--stats' in sys.argv:
                    print(ui.statblock(item))
                if isinstance(item, Humanoid):
                    if '--inventory' in sys.argv:
                        ui.print_inventory(item, True)
                        print('-' * 39)
                    elif '--arms' in sys.argv:
                        ui.print_inventory(item)
                        print('-' * 39)
                print()

    for char in party.members:
        print(f"{ui.handle(char):<18} {ui.health_bar(char, 20)}")
        if '--stats' in sys.argv:
            print(ui.statblock(char))
        if isinstance(char, Adventurer):
            if '--level' in sys.argv:
                # print(f"LV:{char.gold_for_next_level:,.0f}¤")
                print(f"LV:{char.copper_for_next_level:,.0f}¢")
        if isinstance(char, Humanoid):
            if '--inventory' in sys.argv:
                ui.print_inventory(char, True)
                print('-' * 39)
            elif '--arms' in sys.argv:
                ui.print_inventory(char)
                print('-' * 39)
        print()

    with game_file.open('wb') as output:
        pickle.dump((world, party), output)

    if '--actions' in sys.argv:
        actions = party.place.actions()
        print(' / '.join(actions))
