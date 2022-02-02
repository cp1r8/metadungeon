# -*- coding: utf-8 -*-

from . import Script


# 1st Level


class Darkness1(Script):

    LV = 1

    @classmethod
    @property
    def inverse(cls) -> type:
        return Light1


class Decompile(Script):
    LV = 1


class DetectScript(Script):
    LV = 1


class FloatingDisc(Script):
    LV = 1


class HoldPortal(Script):
    LV = 1


class HypnotisePerson(Script):
    LV = 1


class Light1(Script):

    LV = 1

    @classmethod
    @property
    def inverse(cls) -> type:
        return Darkness1


class Shield1(Script):
    LV = 1


class Sleep(Script):
    LV = 1


class TranslateWriting(Script):
    LV = 1


class Ventriloquism(Script):
    LV = 1


class Ward1(Script):
    LV = 1


class Zap(Script):
    LV = 1


# 2nd Level


class Darkness2(Darkness1):

    LV = 2

    @classmethod
    @property
    def inverse(cls) -> type:
        return Light2


class DetectInvisible(Script):
    LV = 2


class Illusion(Script):
    LV = 2


class Invisibility(Script):
    LV = 2


class Levitate(Script):
    LV = 2


class Light2(Light1):

    LV = 2

    @classmethod
    @property
    def inverse(cls) -> type:
        return Darkness2


class LocateObject(Script):
    LV = 2


class LockPortal(Script):
    LV = 2


class MirrorImage(Script):
    LV = 2


class OpenPortal(Script):
    LV = 2


class Telepathy(Script):
    LV = 2


class Web(Script):
    LV = 2


# 3rd Level


class Clairvoyance(Script):
    LV = 3


class Fireball(Script):
    LV = 3


class Fly(Script):
    LV = 3


class Haste(Script):
    LV = 3


class HoldPerson(Script):
    LV = 3


class Infravision(Script):
    LV = 3


class Invisibility2(Invisibility):
    LV = 3


class KillScript(Script):
    LV = 3


class Lightning(Script):
    LV = 3


class Shield2(Shield1):
    LV = 3


class Ward2(Ward1):
    LV = 3


class WaterBreathing(Script):
    LV = 3


# 4th Level


class Confusion(Script):
    LV = 4


class Curse(Script):

    LV = 4

    @classmethod
    @property
    def inverse(cls) -> type:
        return RemoveCurse


class DimensionDoor(Script):
    LV = 4


class FlameWall(Script):
    LV = 4


class HypnotiseCreature(Script):
    LV = 4


class IceWall(Script):
    LV = 4


class IllusoryTerrain(Script):
    LV = 4


class MassIllusion(Script):
    LV = 4


class PlantGrowth(Script):
    LV = 4


class Polymorph(Script):
    LV = 4


class PolymorphSelf(Script):
    LV = 4


class RemoveCurse(Script):

    LV = 4

    @classmethod
    @property
    def inverse(cls) -> type:
        return Curse


class Telesthesia(Script):
    LV = 4


# 5th Level


class ContactEntity(Script):
    LV = 5


class CreateDrone(Script):
    LV = 5


class ElementalContruct(Script):
    LV = 5


class HoldCreature(Script):
    LV = 5


class Neuroinhibitor(Script):
    LV = 5


class Neurotoxin(Script):
    LV = 5


class Portal(Script):
    LV = 5


class StoneWall(Script):
    LV = 5


class Telekinesis(Script):
    LV = 5


class Teleport(Script):
    LV = 5


class Transmute(Script):
    LV = 5


# 6th Level


class Compel(Script):

    LV = 6

    @classmethod
    @property
    def inverse(cls) -> type:
        return RemoveCompulsion


class ControlWeather(Script):
    LV = 6


class Death(Script):
    LV = 6


class Depetrify(Script):

    LV = 6

    @classmethod
    @property
    def inverse(cls) -> type:
        return Petrify


class Disintegrate(Script):
    LV = 6


class Hydrokinesis(Script):
    LV = 6


class Petrify(Script):

    LV = 6

    @classmethod
    @property
    def inverse(cls) -> type:
        return Depetrify


class RemoveCompulsion(Script):

    LV = 6

    @classmethod
    @property
    def inverse(cls) -> type:
        return Compel


class ScriptBarrier(Script):
    LV = 6


class Stalker(Script):
    LV = 6


class Telepresence(Script):
    LV = 6


class Terrakinesis(Script):
    LV = 6
