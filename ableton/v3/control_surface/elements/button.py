# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\button.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 5089 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import ButtonElement as ButtonElementBase
from ...base import depends, listenable_property
from base.util import CallableBool
from .. import MIDI_CC_TYPE
from ..display import Renderable
from ..midi import SYSEX_END

class ButtonElement(ButtonElementBase, Renderable):

    class ProxiedInterface(ButtonElementBase.ProxiedInterface):
        is_momentary = CallableBool(True)
        is_pressed = CallableBool(False)

    @depends(skin=None)
    def __init__(self, identifier, channel=0, msg_type=MIDI_CC_TYPE, is_momentary=True, led_channel=None, *a, **k):
        self._led_channel = led_channel
        (super().__init__)(is_momentary, msg_type, channel, identifier, *a, **k)
        self._do_request_rebuild = self._request_rebuild
        self._request_rebuild = self._request_rebuild_and_release

    @listenable_property
    def is_pressed(self):
        return CallableBool(self._is_momentary and int(self._last_received_value) > 0)

    @property
    def is_momentary(self):
        return CallableBool(self._is_momentary)

    def receive_value(self, value):
        was_pressed = self.is_pressed
        super().receive_value(value)
        if was_pressed != self.is_pressed:
            self.notify_is_pressed()

    def send_value(self, value, force=False, channel=None):
        channel = channel if channel is not None else self._led_channel
        super().send_value(value, force=force, channel=channel)

    def _request_rebuild_and_release(self):
        self._do_request_rebuild()
        if self.is_pressed:
            self.receive_value(0)

    def _do_draw(self, color):
        if color is not None:
            super()._do_draw(color)


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