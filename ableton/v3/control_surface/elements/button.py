# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/elements/button.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 1512 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.elements as ButtonElementBase
from .. import MIDI_CC_TYPE

class ButtonElement(ButtonElementBase):

    def __init__(self, identifier, channel=0, msg_type=MIDI_CC_TYPE, is_momentary=True, led_channel=None, *a, **k):
        self._led_channel = led_channel
        (super().__init__)(is_momentary, msg_type, channel, identifier, *a, **k)

    def send_value(self, value, force=False, channel=None):
        channel = channel if channel is not None else self._led_channel
        super().send_value(value, force=force, channel=channel)