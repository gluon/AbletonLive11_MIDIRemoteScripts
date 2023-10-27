# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\skin.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 3610 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from typing import Any, NamedTuple, Optional
from . import BasicColors
ON_SUFFIXES = ('enabled', 'on', 'pressed', 'selected')

class OptionalSkinEntry(NamedTuple):
    name: str
    fallback_name = None
    fallback_name: Optional[str]


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
        if key is None:
            return
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