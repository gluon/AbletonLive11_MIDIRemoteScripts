# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\touch_strip.py
# Compiled at: 2023-06-30 09:18:52
# Size of source mod 2**32: 5808 bytes
from __future__ import absolute_import, print_function, unicode_literals
from enum import Enum
from ableton.v3.base import clamp, listens, nop
from ableton.v3.control_surface.elements import EncoderElement, TouchElement
from ableton.v3.control_surface.midi import CC_STATUS
from ableton.v3.live import find_parent_track, is_parameter_bipolar, is_parameter_quantized, liveobj_valid, parameter_value_to_midi_value
from .colors import make_color_for_liveobj
FINE_TUNE_FACTOR = 65536

class TouchStripTouchElement(TouchElement):

    def receive_value(self, value):
        super().receive_value(value)
        self._encoder.on_touch_strip_touched_or_released(value != 0)


class LedStyle(Enum):
    off = 0
    default = 1
    bipolar = 3


class TouchStripElement(EncoderElement):

    def __init__(self, *a, **k):
        (super().__init__)(a, feedback_delay=-1, send_should_depend_on_forwarding=False, **k)
        self._track = None
        self._led_style_cc = self.message_channel() + 104
        self._led_color_cc = self.message_channel() + 112
        self._is_touched = False

    def reset(self):
        self._send_led_style_value(LedStyle.off.value)

    def script_wants_forwarding(self):
        return super().script_wants_forwarding() or (self._parameter_can_be_fine_tuned()) and ((self._sensitivity_modifier.is_pressed) or (self._is_touched))

    def install_connections(self, *a, **k):
        if self._parameter_can_be_fine_tuned() and self._sensitivity_modifier.is_pressed:
            super().install_connections(nop, nop, a[-1])
        else:
            (super().install_connections)(*a, **k)
        self._last_received_value = None

    def on_touch_strip_touched_or_released(self, is_touched):
        self._is_touched = is_touched
        self._last_received_value = None

    def receive_value(self, value):
        parameter = self.mapped_object
        if self._last_received_value is not None:
            if liveobj_valid(parameter):
                diff = value - self._last_received_value
                step_size = (parameter.max - parameter.min) / FINE_TUNE_FACTOR
                parameter.value = clamp(parameter.value + diff * step_size, parameter.min, parameter.max)
        self._last_received_value = value
        self.notify_value(value)

    def _update_parameter_listeners(self):
        self._track = None
        if self.is_mapped_to_parameter():
            self._track = find_parent_track(self.mapped_object)
        self._TouchStripElement__on_automation_state_changed.subject = self.mapped_object
        self._TouchStripElement__on_track_color_index_changed.subject = self._track
        self._TouchStripElement__on_automation_state_changed()
        self._TouchStripElement__on_track_color_index_changed()
        super()._update_parameter_listeners()

    def _parameter_value_changed(self):
        self.send_value(parameter_value_to_midi_value((self.mapped_object), max_value=(self._max_value)))

    def _parameter_can_be_fine_tuned(self):
        parameter = self.mapped_object
        return liveobj_valid(parameter) and not is_parameter_quantized(parameter, parameter.canonical_parent)

    def _send_led_style_value(self, style_value):
        self.send_midi((CC_STATUS, self._led_style_cc, style_value))

    def _get_led_style_value(self):
        style_value = LedStyle.off.value
        if self.is_mapped_to_parameter():
            style_value = LedStyle.bipolar.value if is_parameter_bipolar(self.mapped_object) else LedStyle.default.value
            if self.mapped_object.automation_state == 1:
                style_value += 1
        return style_value

    @listens('color_index')
    def __on_track_color_index_changed(self):
        self.send_midi((
         CC_STATUS,
         self._led_color_cc,
         make_color_for_liveobj(self._track).midi_value))

    @listens('automation_state')
    def __on_automation_state_changed(self):
        self._send_led_style_value(self._get_led_style_value())