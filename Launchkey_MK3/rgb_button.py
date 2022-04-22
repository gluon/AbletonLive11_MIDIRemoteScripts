# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchkey_MK3/rgb_button.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 1017 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import ButtonElement

class RgbButtonElement(ButtonElement):

    def __init__(self, *a, **k):
        self._led_channel = k.pop('led_channel', 0)
        (super(RgbButtonElement, self).__init__)(*a, **k)

    def _do_send_value(self, value, channel=None):
        super(RgbButtonElement, self)._do_send_value(value, channel=(self._led_channel))