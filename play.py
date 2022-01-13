#!/usr/bin/env python3

from game import ui
from game.adventure import Party, World
from game.adventure.underground import Dungeon
from game.dice import d4, d6
from game.objects.containers import Backpack
from game.objects.valuables import Gold
from pathlib import Path

import pickle
import sys


if __name__ == '__main__':

    game_file = Path.home() / '.local' / 'metadungeon.pickle'

    if game_file.exists() and '--reset' not in sys.argv:
        with game_file.open('rb') as input:
            world = pickle.load(input)
    else:

        dungeon = Dungeon()

        if '--expert' in sys.argv:
            party = Party.expert(dungeon, d4() + 4)
        elif '--funnel' in sys.argv:
            party = Party.funnel(dungeon, sum(4*d4) + 4)
        else:
            party = Party.basic(dungeon, d4() + 4)

        world = World(party)

        if '--hit' in sys.argv:
            for char in world.party.members:
                char.hit(1)

        if '--loot' in sys.argv:
            # TODO TT U+V
            for char in world.party.members:
                if isinstance(char.shoulders, Backpack):
                    char.shoulders.store(Gold(3*d6() * 10))

    actions = world.party.location.actions(world.party)

    for arg in sys.argv:
        if arg in actions:
            getattr(world.party.location, arg)(world.party)
            break

    print(world.time)
    ui.print_location(world.party.location)

    for char in world.party.members:
        print(f"{char.handle:<18} {ui.health_bar(char, 20)}")
        # print(char.handle)
        # print(ui.health_bar(char, 39))
        if '--stats' in sys.argv:
            print(ui.statblock(char))
            # print(f"LV:{char.gold_for_next_level:,.0f}¤")
            print(f"LV:{char.copper_for_next_level:,.0f}¢")
        if '--inventory' in sys.argv:
            ui.print_inventory(char, True)
            print('-' * 39)
        elif '--arms' in sys.argv:
            ui.print_inventory(char)
            print('-' * 39)
        print()

    with game_file.open('wb') as output:
        pickle.dump(world, output)

    if '--actions' in sys.argv:
        actions = world.party.location.actions(world.party)
        print(' / '.join(actions))
