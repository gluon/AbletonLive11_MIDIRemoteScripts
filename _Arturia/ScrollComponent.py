from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Control import EncoderControl
from _Framework.ScrollComponent import ScrollComponent as ScrollComponentBase

class ScrollComponent(ScrollComponentBase):
    scroll_encoder = EncoderControl()

    def set_scroll_encoder(self, encoder):
        self.scroll_encoder.set_control_element(encoder)
        self.update()

    @scroll_encoder.value
    def scroll_encoder(self, value, encoder):
        scroll_step = None
        if value > 0 and self.can_scroll_down():
            scroll_step = self._do_scroll_down
        else:
            if value < 0:
                if self.can_scroll_up():
                    scroll_step = self._do_scroll_up
        if scroll_step is not None:
            scroll_step()