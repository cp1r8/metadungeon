#!/usr/bin/env python3

from game import World
from game.creatures import Humanoid, Unit
from game.creatures.adventurers import Adventurer, Party
from game.objects.containers import Container
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
        elif '--hlc' in sys.argv:
            party = Party.highLevelClient(location, auto_equip)
        elif '--hlf' in sys.argv:
            party = Party.highLevelFighter(location, auto_equip)
        elif '--hlm' in sys.argv:
            party = Party.highLevelMuser(location, auto_equip)
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
            world.age(minutes=10)
            actions = party.location.actions(party)
            break

    with game_file.open('wb') as output:
        pickle.dump((world, party), output)

    print(f"{str(world):<19} {world.now}")
    print('-' * 39)
    print(str(party.location))
    print()
    print('[ ' + ' ] [ '.join(sorted(actions.keys())) + ' ]')
    print('=' * 39)
    print()

    for entity in sorted(party.location.entities, key=lambda entity: entity.id):

        if isinstance(entity, Unit):
            continue

        print(str(entity))

        if isinstance(entity, Container):
            for item in entity.contents:
                ui.print_inventory_item(item)
            print('-' * 39)

        print()

    for entity in sorted(party.location.entities, key=lambda entity: entity.id):

        if not isinstance(entity, Unit):
            continue

        print(str(entity))

        # TODO unit "health bar"
        # TODO unit status (e.g., lost/flee)

        if '--stats' in sys.argv:
            print(ui.unitstats(entity))

        print('-' * 39)
        print()

        for member in sorted(entity.members, key=lambda member: member.id):

            print(str(member))

            if member.hits_taken > member.hit_dice:
                hit_points = f"{member.hit_dice - member.hits_taken:d}/{member.hit_dice:d}"
            else:
                hit_points = f"{member.hits_remaining - member.partial_hit:d}/{member.hit_dice:d}"

            print(
                f"[{ui.health_bar(member, 28)}]",
                f"{hit_points:>5} hp",
            )

            if '--stats' in sys.argv:
                print(ui.statblock(member))

            if isinstance(member, Adventurer):
                if '--abilities' in sys.argv:
                    print(ui.abilities(member))
                if '--level' in sys.argv:
                    # TODO calculate "bounty"
                    print(
                        f"{member.profile}",
                        f"1UP:{member.silver_for_next_level:,.0f}$"
                    )

            if isinstance(member, Humanoid):
                if '--inventory' in sys.argv:
                    ui.print_inventory(member, True)
                    print('-' * 39)
                elif '--arms' in sys.argv:
                    ui.print_inventory(member)

            print()

        print('=' * 39)
        print()
