#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/simple_device_navigation.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl
NavDirection = Live.Application.Application.View.NavDirection

class SimpleDeviceNavigationComponent(Component):
    u"""
    Device navigation component for the case where
    we only need to go to the next or previous device
    on a track.
    """
    next_button = ButtonControl(color=u'Device.Navigation', pressed_color=u'Device.NavigationPressed')
    prev_button = ButtonControl(color=u'Device.Navigation', pressed_color=u'Device.NavigationPressed')

    @next_button.pressed
    def next_button(self, value):
        self._scroll_device_chain(NavDirection.right)

    @prev_button.pressed
    def prev_button(self, value):
        self._scroll_device_chain(NavDirection.left)

    def _scroll_device_chain(self, direction):
        view = self.application.view
        if not view.is_view_visible(u'Detail') or not view.is_view_visible(u'Detail/DeviceChain'):
            view.show_view(u'Detail')
            view.show_view(u'Detail/DeviceChain')
        else:
            view.scroll_view(direction, u'Detail/DeviceChain', False)
