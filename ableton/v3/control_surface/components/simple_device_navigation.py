<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
import Live
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/simple_device_navigation.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 1439 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ...base import add_scroll_encoder, skin_scroll_buttons
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from . import Scrollable, ScrollComponent
NavDirection = Live.Application.Application.View.NavDirection

class SimpleDeviceNavigationComponent(ScrollComponent, Scrollable):

    def __init__(self, name='Device_Navigation', *a, **k):
<<<<<<< HEAD
        (super().__init__)(a, name=name, scroll_skin_name='Device.Navigation', **k)
=======
        (super().__init__)(a, name=name, **k)
        add_scroll_encoder(self)
        skin_scroll_buttons(self, 'Device.Navigation', 'Device.NavigationPressed')
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def set_prev_button(self, button):
        self.scroll_up_button.set_control_element(button)

    def set_next_button(self, button):
        self.scroll_down_button.set_control_element(button)

    def can_scroll_up(self):
        return True

    def can_scroll_down(self):
        return True

    def scroll_up(self):
        self._scroll_device_chain(NavDirection.left)

    def scroll_down(self):
        self._scroll_device_chain(NavDirection.right)

    def _scroll_device_chain(self, direction):
        view = self.application.view
        if not (view.is_view_visible('Detail') and view.is_view_visible('Detail/DeviceChain')):
            view.show_view('Detail')
            view.show_view('Detail/DeviceChain')
        else:
            view.scroll_view(direction, 'Detail/DeviceChain', False)