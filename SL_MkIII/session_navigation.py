from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionNavigationComponent as SessionNavigationComponentBase

class SessionNavigationComponent(SessionNavigationComponentBase):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self._vertical_banking.scroll_up_button.color = 'Session.Navigation'
        self._vertical_banking.scroll_down_button.color = 'Session.Navigation'