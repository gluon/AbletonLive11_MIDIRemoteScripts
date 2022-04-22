# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Komplete_Kontrol_A/view_control_component.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 868 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import EncoderControl
NavDirection = Live.Application.Application.View.NavDirection

class ViewControlComponent(Component):
    vertical_encoder = EncoderControl()
    horizontal_encoder = EncoderControl()

    @vertical_encoder.value
    def vertical_encoder(self, value, _):
        direction = NavDirection.up if value < 0 else NavDirection.down
        self.application.view.scroll_view(direction, '', False)

    @horizontal_encoder.value
    def horizontal_encoder(self, value, _):
        direction = NavDirection.left if value < 0 else NavDirection.right
        self.application.view.scroll_view(direction, '', False)