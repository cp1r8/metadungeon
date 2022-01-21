#!/usr/bin/env python3

from game import World
from game.creatures import Creature, Humanoid, Unit
from game.creatures.adventurers import Adventurer, Party
from game.places.underground import Dungeon
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
            place = Dungeon(world).entrance
        else:
            auto_equip = True
            place = Dungeon(world).entrance

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
        if (isinstance(party.location, Dungeon.Area)):
            for item in party.location.contents:
                if isinstance(item, Unit):
                    for member in item.members:
                        member.hit(damage)
        for char in party.members:
            char.hit(damage)

    actions = party.location.actions(party)

    for arg in sys.argv:
        if arg in actions:
            getattr(party.location, arg)(party)
            world.advance(minutes=10)
            break

    print(f"{world.now:%Y-%m-%d %H:%M} | {ui.party_location(party)}")
    print('=' * 39)
    print()

    if (isinstance(party.location, Dungeon.Area)):
        for item in party.location.contents:
            if isinstance(item, Unit):
                for char in item.members:
                    print(f"{str(char):<18} {ui.health_bar(char, 20)}")
                    if '--stats' in sys.argv:
                        print(ui.statblock(char))
                    if isinstance(char, Humanoid):
                        if '--inventory' in sys.argv:
                            ui.print_inventory(char, True)
                            print('-' * 39)
                        elif '--arms' in sys.argv:
                            ui.print_inventory(char)
                            print('-' * 39)
                    print()
                print('=' * 39)
                print()

    for char in party.members:
        print(f"{str(char):<18} {ui.health_bar(char, 20)}")
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
        actions = party.location.actions(party)
        print(' / '.join(actions))
