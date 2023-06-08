<<<<<<< HEAD
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


=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/skin.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 1375 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from . import BasicColors
ON_SUFFIXES = ('enabled', 'on', 'pressed', 'selected')

>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
class Skin:

    def __init__(self, colors=None, *a, **k):
        (super().__init__)(*a, **k)
<<<<<<< HEAD
        self.colors = {}
=======
        self._colors = {}
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
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
<<<<<<< HEAD
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
=======
                    self._colors['{}{}'.format(pathname, k)] = v

    def __getitem__(self, key):
        if key not in self._colors:
            if key.lower().endswith(ON_SUFFIXES):
                return BasicColors.ON
            return BasicColors.OFF
        return self._colors[key]
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34


def merge_skins(*skins):
    skin = Skin()
<<<<<<< HEAD
    skin.colors = dict(chain(*map(lambda s: s.colors.items()
, skins)))
=======
    skin._colors = dict(chain(*map(lambda s: s._colors.items(), skins)))
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    return skin