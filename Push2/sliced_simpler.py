# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\sliced_simpler.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 758 bytes
from __future__ import absolute_import, print_function, unicode_literals
from pushbase.colors import Pulse
from pushbase.sliced_simpler_component import SlicedSimplerComponent
from .colors import IndexedColor
NEXT_SLICE_PULSE_SPEED = 48

def next_slice_color(track_color_index):
    return Pulse(color1=IndexedColor.from_live_index(track_color_index, shade_level=2),
      color2=IndexedColor.from_live_index(track_color_index, shade_level=1),
      speed=NEXT_SLICE_PULSE_SPEED)


class Push2SlicedSimplerComponent(SlicedSimplerComponent):

    def _next_slice_color(self):
        return next_slice_color(self.song.view.selected_track.color_index)