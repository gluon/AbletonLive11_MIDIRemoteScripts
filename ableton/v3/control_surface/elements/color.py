<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from abc import ABC, abstractmethod
from typing import NamedTuple, Optional
from ...base import memoize, old_hasattr

@memoize
def create_rgb_color(values):
    if values is not None:
        return RgbColor(*values)

=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/elements/color.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 2881 bytes
from __future__ import absolute_import, print_function, unicode_literals
from abc import ABC, abstractmethod
from collections import namedtuple
from ...base import old_hasattr
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

class Color(ABC):

    @abstractmethod
    def draw(self, interface):
        pass

<<<<<<< HEAD
    @property
    def midi_value(self):
        raise NotImplementedError

=======
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

class SimpleColor(Color):

    def __init__(self, value, channel=None, *a, **k):
        (super().__init__)(*a, **k)
        self._value = value
        self._channel = channel

    @property
    def midi_value(self):
        return self._value

    def draw(self, interface):
        interface.send_value((self._value), channel=(self._channel))


<<<<<<< HEAD
class RgbColor(Color):

    def __init__(self, *values, **k):
        (super().__init__)(**k)
        self._values = values

    def draw(self, interface):
        (interface.send_value)(*self._values)


class ColorPart(NamedTuple):
    value: int
    channel = None
    channel: Optional[int]

=======
ColorPart = namedtuple('ColorPart', 'value channel', defaults=(0, None))
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

class ComplexColor(Color):

    def __init__(self, color_parts, *a, **k):
        (super().__init__)(*a, **k)
        self._color_parts = color_parts

<<<<<<< HEAD
=======
    @property
    def midi_value(self):
        return self._color_parts[0].value

>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    def draw(self, interface):
        for part in self._color_parts:
            interface.send_value((part.value), channel=(part.channel))


class FallbackColor(Color):

    def __init__(self, rgb_color, fallback_color):
        self._rgb_color = rgb_color
        self._fallback_color = fallback_color

    @property
    def midi_value(self):
        return self._rgb_color.midi_value

    def draw(self, interface):
        if old_hasattr(interface, 'is_rgb') and interface.is_rgb:
            self._rgb_color.draw(interface)
        else:
            self._fallback_color.draw(interface)