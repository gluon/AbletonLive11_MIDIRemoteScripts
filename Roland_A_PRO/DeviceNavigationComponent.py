# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Roland_A_PRO\DeviceNavigationComponent.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1163 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.Control import ButtonControl
import _Framework.ControlSurfaceComponent as ControlSurfaceComponent
NavDirection = Live.Application.Application.View.NavDirection

class DeviceNavigationComponent(ControlSurfaceComponent):
    device_nav_left_button = ButtonControl()
    device_nav_right_button = ButtonControl()

    @device_nav_left_button.pressed
    def device_nav_left_button(self, value):
        self._scroll_device_chain(NavDirection.left)

    @device_nav_right_button.pressed
    def device_nav_right_button(self, value):
        self._scroll_device_chain(NavDirection.right)

    def _scroll_device_chain(self, direction):
        view = self.application().view
        if not (view.is_view_visible('Detail') and view.is_view_visible('Detail/DeviceChain')):
            view.show_view('Detail')
            view.show_view('Detail/DeviceChain')
        else:
            view.scroll_view(direction, 'Detail/DeviceChain', False)