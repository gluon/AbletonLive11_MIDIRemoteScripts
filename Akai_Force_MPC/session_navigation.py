from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionNavigationComponent as SessionNavigationComponentBase

class SessionNavigationComponent(SessionNavigationComponentBase):

    def __init__(self, *a, **k):
        (super(SessionNavigationComponent, self).__init__)(*a, **k)
        for scroll_component in (
         self._vertical_banking,
         self._horizontal_banking,
         self._vertical_paginator,
         self._horizontal_paginator):
            for button in (
             scroll_component.scroll_up_button,
             scroll_component.scroll_down_button):
                button.color = 'Navigation.Enabled'