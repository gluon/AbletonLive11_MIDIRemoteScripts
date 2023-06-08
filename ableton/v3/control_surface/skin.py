from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from typing import Any, NamedTuple
from . import BasicColors
ON_SUFFIXES = ('enabled', 'on', 'pressed', 'selected')

class OptionalSkinEntry(NamedTuple):
    name: str
    fallback_name: str


class LiveObjSkinEntry(NamedTuple):
    name: str
    liveobj: Any


class Skin:

    def __init__(self, colors=None, *a, **k):
        (super().__init__)(*a, **k)
        self.colors = {}
        if colors is not None:
            self._fill_colors(colors)

    def _fill_colors(self, colors, pathname=''):
        if getattr(colors, '__bases__', None):
            for base in colors.__bases__:
                self._fill_colors(base, pathname=pathname)

        for k, v in vars(colors).items():
            if k[:1] != '_':
                if callable(v):
                    self._fill_colors(v, '{}{}.'.format(pathname, k))
                else:
                    self.colors['{}{}'.format(pathname, k)] = v

    def __getitem__(self, key):
        key = self._from_wrapper(key)
        if isinstance(key, LiveObjSkinEntry):
            key_name = self._from_wrapper(key.name)
            color = self.colors[key_name]
            if callable(color):
                return color(key.liveobj)
            key = key_name
        if key not in self.colors:
            if key.lower().endswith(ON_SUFFIXES):
                return BasicColors.ON
            return BasicColors.OFF
        return self.colors[key]

    def _from_wrapper(self, key):
        if isinstance(key, OptionalSkinEntry):
            if key.name in self.colors:
                return key.name
            return key.fallback_name
        return key


def merge_skins(*skins):
    skin = Skin()
    skin.colors = dict(chain(*map(lambda s: s.colors.items()
, skins)))
    return skin