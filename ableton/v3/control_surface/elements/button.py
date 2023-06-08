from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import ButtonElement as ButtonElementBase
from ...base import depends
from .. import MIDI_CC_TYPE
from ..midi import SYSEX_END

class ButtonElement(ButtonElementBase):

    @depends(skin=None)
    def __init__(self, identifier, channel=0, msg_type=MIDI_CC_TYPE, is_momentary=True, led_channel=None, *a, **k):
        self._led_channel = led_channel
        (super().__init__)(is_momentary, msg_type, channel, identifier, *a, **k)
        self._do_request_rebuild = self._request_rebuild
        self._request_rebuild = self._request_rebuild_and_release

    def send_value(self, value, force=False, channel=None):
        channel = channel if channel is not None else self._led_channel
        super().send_value(value, force=force, channel=channel)

    def _request_rebuild_and_release(self):
        self._do_request_rebuild()
        if self.is_pressed():
            self.receive_value(0)


class SysexSendingButtonElement(ButtonElement):

    def __init__(self, identifier, sysex_identifier, optimized=True, tail=(SYSEX_END,), *a, **k):
        (super().__init__)(identifier, *a, **k)
        self._send_message_generator = lambda *values: sysex_identifier + tuple(values) + tail
        self._optimized = optimized

    def send_value(self, *value, **_):
        message = (self._send_message_generator)(*value)
        if self._optimized:
            if not message != self._last_sent_message or self.send_midi(message):
                self._last_sent_message = message
        else:
            self.send_midi(message)