# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/base/component_util.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 1239 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import ScrollComponent
from ableton.v2.control_surface.control import EncoderControl

def skin_scroll_buttons(component, color, pressed_color):
    component.scroll_up_button.color = color
    component.scroll_down_button.color = color
    component.scroll_up_button.pressed_color = pressed_color
    component.scroll_down_button.pressed_color = pressed_color


def add_scroll_encoder(component):
    scroll_encoder = EncoderControl()

    @scroll_encoder.value
    def scroll_encoder(component, value, _):
        if value < 0:
            if component.can_scroll_up():
                component.scroll_up()
        elif component.can_scroll_down():
            component.scroll_down()

    component.add_control('scroll_encoder', scroll_encoder)