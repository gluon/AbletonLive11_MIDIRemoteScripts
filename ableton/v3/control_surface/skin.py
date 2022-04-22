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

class Skin:

    def __init__(self, colors=None, *a, **k):
        (super().__init__)(*a, **k)
        self._colors = {}
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
                    self._colors['{}{}'.format(pathname, k)] = v

    def __getitem__(self, key):
        if key not in self._colors:
            if key.lower().endswith(ON_SUFFIXES):
                return BasicColors.ON
            return BasicColors.OFF
        return self._colors[key]


def merge_skins(*skins):
    skin = Skin()
    skin._colors = dict(chain(*map(lambda s: s._colors.items(), skins)))
    return skin