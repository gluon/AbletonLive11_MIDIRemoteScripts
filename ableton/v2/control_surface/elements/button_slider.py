# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\button_slider.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 4975 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from past.utils import old_div
from ...base import EventObject, liveobj_valid
from ..input_control_element import MIDI_INVALID_TYPE, InputControlElement
from .button import ButtonElement
from .slider import SliderElement

class ButtonSliderElement(SliderElement):
    _last_sent_value = -1

    def __init__(self, buttons):
        SliderElement.__init__(self, MIDI_INVALID_TYPE, 0, 0)
        self._parameter_value_slot = self.register_slot(None, self._on_parameter_changed, 'value')
        self._buttons = buttons
        self._button_slots = self.register_disconnectable(EventObject())
        for button in self._buttons:
            self._button_slots.register_slot(button,
              (self._button_value), 'value', extra_kws={'identify_sender': True})

    def disconnect(self):
        SliderElement.disconnect(self)
        self._buttons = None

    def message_channel(self):
        raise NotImplementedError('message_channel() should not be called directly on ButtonSliderElement')

    def message_identifier(self):
        raise NotImplementedError('message_identifier() should not be called directly on ButtonSliderElement')

    def message_map_mode(self):
        raise NotImplementedError('message_map_mode() should not be called directly on ButtonSliderElement')

    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        pass

    def connect_to(self, parameter):
        InputControlElement.connect_to(self, parameter)
        self._parameter_value_slot.subject = parameter
        if liveobj_valid(self._parameter_to_map_to):
            self._on_parameter_changed()

    def release_parameter(self):
        self._parameter_value_slot.subject = None
        InputControlElement.release_parameter(self)

    def identifier_bytes(self):
        raise RuntimeWarning('identifier_bytes() should not be called on ButtonSliderElement')

    def send_value(self, value):
        if value != self._last_sent_value:
            num_buttons = len(self._buttons)
            index_to_light = 0
            index_to_light = int(old_div((num_buttons - 1) * value, 127)) if value > 0 else 0
            for index in range(num_buttons):
                if index == index_to_light:
                    self._buttons[index].set_light(True)
                else:
                    self._buttons[index].set_light(False)

            self._last_sent_value = value

    def _button_value(self, value, sender):
        self.clear_send_cache()
        if not (value != 0 or sender.is_momentary()):
            index_of_sender = list(self._buttons).index(sender)
            midi_value = int(old_div(127 * index_of_sender, len(self._buttons) - 1))
            if liveobj_valid(self._parameter_to_map_to):
                if self._parameter_to_map_to.is_enabled:
                    param_range = self._parameter_to_map_to.max - self._parameter_to_map_to.min
                    param_value = old_div(param_range * index_of_sender, len(self._buttons) - 1) + self._parameter_to_map_to.min
                    if index_of_sender > 0:
                        param_value += old_div(param_range, 4 * len(self._buttons))
                        if param_value > self._parameter_to_map_to.max:
                            param_value = self._parameter_to_map_to.max
                    self._parameter_to_map_to.value = param_value
            self.notify_value(midi_value)

    def _on_parameter_changed(self):
        param_range = abs(self._parameter_to_map_to.max - self._parameter_to_map_to.min)
        midi_value = int(old_div(127 * abs(self._parameter_to_map_to.value - self._parameter_to_map_to.min), param_range))
        self.send_value(midi_value)