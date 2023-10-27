# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Roland_FA\scroll.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 1393 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import ScrollComponent as ScrollComponentBase
from ableton.v2.control_surface.control import ButtonControl

class ScrollComponent(ScrollComponentBase):
    scroll_up_button = ButtonControl(color='DefaultButton.Off',
      pressed_color='DefaultButton.On')
    scroll_down_button = ButtonControl(color='DefaultButton.Off',
      pressed_color='DefaultButton.On')

    @scroll_up_button.pressed
    def scroll_up_button(self, button):
        self.scroll_up()

    @scroll_up_button.released
    def scroll_up_button(self, _):
        self._update_scroll_buttons()

    @scroll_down_button.pressed
    def scroll_down_button(self, button):
        self.scroll_down()

    @scroll_down_button.released
    def scroll_down_button(self, _):
        self._update_scroll_buttons()

    def _update_scroll_buttons(self):
        if not self.scroll_down_button.is_pressed:
            if not self.scroll_up_button.is_pressed:
                self._do_update_scroll_buttons()

    def _do_update_scroll_buttons(self):
        self.scroll_up_button.enabled = self.can_scroll_up()
        self.scroll_down_button.enabled = self.can_scroll_down()