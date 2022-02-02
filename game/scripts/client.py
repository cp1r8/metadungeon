# -*- coding: utf-8 -*-

from . import Script, muser


# 1st Level


class Calm(Script):

    LV = 1

    @classmethod
    @property
    def inverse(cls) -> type:
        return Panic


class Darkness1(muser.Darkness1):

    LV = 1

    @classmethod
    @property
    def inverse(cls) -> type:
        return Light1


class DetectScript(muser.DetectScript):
    LV = 1


class Harm(Script):

    LV = 1

    @classmethod
    @property
    def inverse(cls) -> type:
        return Heal


class Heal(Script):

    LV = 1

    @classmethod
    @property
    def inverse(cls) -> type:
        return Harm


class Light1(muser.Light1):

    LV = 1

    @classmethod
    @property
    def inverse(cls) -> type:
        return Darkness1


class Panic(Script):

    LV = 1

    @classmethod
    @property
    def inverse(cls) -> type:
        return Calm


class PurifyFoodWater(Script):
    LV = 1


class RepelDrones(Script):
    LV = 1


class ResistCold(Script):
    LV = 1


class Ward1(muser.Ward1):
    LV = 1


# 2nd Level


class Bless(Script):

    LV = 2

    @classmethod
    @property
    def inverse(cls) -> type:
        return Blight


class Blight(Script):

    LV = 2

    @classmethod
    @property
    def inverse(cls) -> type:
        return Bless


class FindTraps(Script):
    LV = 2


class HoldPerson(muser.HoldPerson):
    LV = 2


class HypnotiseSnake(Script):
    LV = 2


class ResistFire(Script):
    LV = 2


class Silence(Script):
    LV = 2


class SpeakWithAnimals(Script):
    LV = 2


# 3rd Level


class AnimalGrowth(Script):
    LV = 3


class Cure(Script):

    LV = 3

    @classmethod
    @property
    def inverse(cls) -> type:
        return Disease


class Curse(muser.Curse):

    LV = 3

    @classmethod
    @property
    def inverse(cls) -> type:
        return RemoveCurse


class Darkness2(muser.Darkness2):

    LV = 3

    @classmethod
    @property
    def inverse(cls) -> type:
        return Light2


class Disease(Script):

    LV = 3

    @classmethod
    @property
    def inverse(cls) -> type:
        return Cure


class Light2(muser.Light2):

    LV = 3

    @classmethod
    @property
    def inverse(cls) -> type:
        return Darkness2


class LocateObject(muser.LocateObject):
    LV = 3


class RemoveCurse(muser.RemoveCurse):

    LV = 3

    @classmethod
    @property
    def inverse(cls) -> type:
        return Curse


class Striking(Script):
    LV = 3


# 4th Level


class ConjureSnakes(Script):
    LV = 4


class CreateWater(Script):
    LV = 4


class Harm2(Harm):

    LV = 4

    @classmethod
    @property
    def inverse(cls) -> type:
        return Heal2


class Heal2(Heal):

    LV = 4

    @classmethod
    @property
    def inverse(cls) -> type:
        return Harm2


class NeutralisePoison(Script):

    LV = 4

    @classmethod
    @property
    def inverse(cls) -> type:
        return Poison


class Poison(Script):

    LV = 4

    @classmethod
    @property
    def inverse(cls) -> type:
        return NeutralisePoison


class SpeakWithPlants(Script):
    LV = 4


class Ward2(muser.Ward2):
    LV = 4


# 5th Level


class Banish(Script):
    LV = 5


class Commune(Script):
    LV = 5


class CreateFood(Script):
    LV = 5


class Dispel(Script):
    LV = 5


class FingerOfDeath(Script):

    LV = 5

    @classmethod
    @property
    def inverse(cls) -> type:
        return Resuscitate


class Quest(muser.Compel):

    LV = 5

    @classmethod
    @property
    def inverse(cls) -> type:
        return RemoveQuest


class RemoveQuest(muser.RemoveCompulsion):

    LV = 5

    @classmethod
    @property
    def inverse(cls) -> type:
        return Quest


class Resuscitate(Script):

    LV = 5

    @classmethod
    @property
    def inverse(cls) -> type:
        return FingerOfDeath


class Swarm(Script):
    LV = 5
