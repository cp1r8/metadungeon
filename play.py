#!/usr/bin/env python3

from game import ui
from game.adventure import World
from game.adventure.underground import Dungeon
from game.creatures import Humanoid
from game.creatures.adventurers import Adventurer
from game.dice import d3, d4, d6
from pathlib import Path

import pickle
import sys


if __name__ == '__main__':

    game_file = Path.home() / '.local' / 'metadungeon.pickle'

    if game_file.exists() and '--reset' not in sys.argv:
        with game_file.open('rb') as input:
            world = pickle.load(input)
            party = world.parties[0]
    else:

        world = World()
        dungeon = Dungeon()
        world.establish(dungeon)

        if '--no-equip' in sys.argv:
            # TODO start in town
            auto_equip = False
        else:
            auto_equip = True

        if '--basic' in sys.argv:
            party = world.assemble(dungeon, [
                Adventurer.random(d3(), auto_equip) for _ in range(0, d4() + 4)
            ])
        elif '--expert' in sys.argv:
            party = world.assemble(dungeon, [
                Adventurer.random(d6() + 3, auto_equip) for _ in range(0, d4() + 4)
            ])
        elif '--funnel' in sys.argv:
            party = world.assemble(dungeon, [
                Adventurer.random(0, auto_equip) for _ in range(0, sum(4*d4) + 4)
            ])
        else:
            party = world.assemble(dungeon, [
                Adventurer.random(1, auto_equip) for _ in range(0, sum(2*d4) + 4)
            ])

    # for testing
    if '--hit' in sys.argv:
        damage = sys.argv.count('--hit')
        for char in party.members:
            char.hit(damage)

    actions = party.location.actions(party)

    for arg in sys.argv:
        if arg in actions:
            getattr(party.location, arg)(party)
            break

    print(world.time)
    ui.print_location(party.location)
    print('=' * 39)
    print()

    for char in party.members:
        print(f"{ui.handle(char):<18} {ui.health_bar(char, 20)}")
        if '--stats' in sys.argv:
            print(ui.statblock(char))
        if isinstance(char, Adventurer):
            if '--stats' in sys.argv:
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
        pickle.dump(world, output)

    if '--actions' in sys.argv:
        actions = party.location.actions(party)
        print(' / '.join(actions))
