#!/usr/bin/env python3

from game import World
from game.creatures import Humanoid, Unit
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

        dungeon = Dungeon(world)
        world.add(dungeon)

        if '--shop' in sys.argv:
            auto_equip = False
            # TODO start in town (purchase equipment manually)
        else:
            auto_equip = True

        location = dungeon.entrance

        if '--basic' in sys.argv:
            party = Party.basic(location, auto_equip)
        elif '--expert' in sys.argv:
            party = Party.expert(location, auto_equip)
        elif '--funnel' in sys.argv:
            party = Party.assemble(0, sum(4*d4) + 4, location, auto_equip)
        else:
            party = Party.assemble(1, sum(2*d4) + 4, location, auto_equip)

        location.add(party)

    # for testing
    if '--zap' in sys.argv:
        damage = sys.argv.count('--zap')
        for entity in party.location.entities:
            if isinstance(entity, Unit):
                for member in entity.members:
                    member.hit(damage)

    actions = party.location.actions(party)

    for arg in sys.argv:
        if arg in actions:
            actions[arg]()
            world.age(minutes=36 / party.movement_rate)
            actions = party.location.actions(party)
            break

    with game_file.open('wb') as output:
        pickle.dump((world, party), output)

    print(f"{str(world):<18}", world.now)
    print('=' * 39)
    print()

    for entity in sorted(party.location.entities, key=lambda entity: entity.id):

        print(str(entity))
        print()

        if isinstance(entity, Unit):
            for member in sorted(entity.members, key=lambda member: member.id):

                print(f"{str(member):<18}", ui.health_bar(member, 20))

                if '--stats' in sys.argv:
                    print(ui.statblock(member))

                if isinstance(member, Adventurer):
                    if '--abilities' in sys.argv:
                        print(ui.abilities(member))
                    if '--level' in sys.argv:
                        print(f"XP:{member.gold_for_next_level:,.0f}")

                if isinstance(member, Humanoid):
                    if '--inventory' in sys.argv:
                        ui.print_inventory(member, True)
                        print('-' * 39)
                    elif '--arms' in sys.argv:
                        ui.print_inventory(member)

                print()

        print('=' * 39)
        print()

    print(str(party.location))
    print()
    print('[ ' + ' ] [ '.join(sorted(actions.keys())) + ' ]')
    print()
