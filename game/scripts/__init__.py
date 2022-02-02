# -*- coding: utf-8 -*-


class Script:

    LV = 0

    @classmethod
    @property
    def inverse(cls) -> type:
        return cls

    @property
    def level(self) -> int:
        return int(self.LV)
