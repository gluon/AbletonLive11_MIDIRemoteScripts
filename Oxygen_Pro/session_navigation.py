from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionNavigationComponent as SessionNavigationComponentBase
from ableton.v2.control_surface.control import EncoderControl

class SessionNavigationComponent(SessionNavigationComponentBase):
    scene_encoder = EncoderControl()

    @scene_encoder.value
    def scene_encoder(self, value, _):
        if value > 0:
            if self._vertical_banking.can_scroll_up():
                self._vertical_banking.scroll_up()
        else:
            if self._vertical_banking.can_scroll_down():
                self._vertical_banking.scroll_down()