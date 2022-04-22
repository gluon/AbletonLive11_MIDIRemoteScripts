# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/drum_group_component.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 508 bytes
from __future__ import absolute_import, print_function, unicode_literals
import pushbase.drum_group_component as DrumGroupComponentBase

class DrumGroupComponent(DrumGroupComponentBase):

    def __init__(self, selector=None, *a, **k):
        (super(DrumGroupComponent, self).__init__)(*a, **k)
        self._selector = selector

    def select_drum_pad(self, drum_pad):
        self._selector.on_select_drum_pad(drum_pad)