# -*- coding: utf-8 -*-

from .. import Place


class Area:

    def __init__(self, contents: list = []) -> None:
        self.__contents = contents

    @property
    def content(self) -> list:
        return self.__contents

# TODO Region


class Site(Place):
    pass
