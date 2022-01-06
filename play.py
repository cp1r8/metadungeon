#!/usr/bin/env python3

from game import d4, d6, ui
from game.adventure import Party
from game.adventure.underground import Dungeon
from game.objects.containers import Backpack
from game.objects.valuables import Gold
from pathlib import Path

import pickle
import sys


if __name__ == '__main__':

    game_file = Path.home() / '.local' / 'metadungeon.pickle'

    if game_file.exists() and '--reset' not in sys.argv:
        with game_file.open('rb') as input:
            party = pickle.load(input)
    else:

        dungeon = Dungeon()

        if '--expert' in sys.argv:
            party = Party.expert(dungeon, d4() + 4)
        elif '--funnel' in sys.argv:
            party = Party.funnel(dungeon, sum(4*d4) + 4)
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

    ui.print_location(party.location)

    for adventurer in party.members:
        ui.print_adventurer(adventurer)
        if '--stats' in sys.argv:
            ui.print_statblock(adventurer)
        if '--inventory' in sys.argv:
            ui.print_inventory(adventurer, True)
            print('-' * 39)
        elif '--arms' in sys.argv:
            ui.print_inventory(adventurer)
            print('-' * 39)
        print()

    with game_file.open('wb') as output:
        pickle.dump(party, output)

    if '--actions' in sys.argv:
        actions = party.location.actions(party)
        print(' / '.join(actions))
