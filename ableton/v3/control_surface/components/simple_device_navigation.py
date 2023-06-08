from __future__ import absolute_import, print_function, unicode_literals
import Live
from . import Scrollable, ScrollComponent
NavDirection = Live.Application.Application.View.NavDirection

class SimpleDeviceNavigationComponent(ScrollComponent, Scrollable):

    def __init__(self, name='Device_Navigation', *a, **k):
        (super().__init__)(a, name=name, scroll_skin_name='Device.Navigation', **k)

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