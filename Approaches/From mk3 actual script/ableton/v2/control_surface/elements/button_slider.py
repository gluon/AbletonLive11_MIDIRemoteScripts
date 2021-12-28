#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/elements/button_slider.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from past.utils import old_div
from ...base import EventObject
from ..input_control_element import InputControlElement, MIDI_INVALID_TYPE
from .button import ButtonElement
from .slider import SliderElement

class ButtonSliderElement(SliderElement):
    u""" Class representing a set of buttons used as a slider """
    _last_sent_value = -1

    def __init__(self, buttons):
        assert buttons != None
        assert isinstance(buttons, tuple)
        assert len(buttons) > 1
        SliderElement.__init__(self, MIDI_INVALID_TYPE, 0, 0)
        self._parameter_value_slot = self.register_slot(None, self._on_parameter_changed, u'value')
        self._buttons = buttons
        self._button_slots = self.register_disconnectable(EventObject())
        for button in self._buttons:
            assert button != None
            assert isinstance(button, ButtonElement)
            self._button_slots.register_slot(button, self._button_value, u'value', extra_kws={u'identify_sender': True})

    def disconnect(self):
        SliderElement.disconnect(self)
        self._buttons = None

    def message_channel(self):
        raise NotImplementedError(u'message_channel() should not be called directly on ButtonSliderElement')

    def message_identifier(self):
        raise NotImplementedError(u'message_identifier() should not be called directly on ButtonSliderElement')

    def message_map_mode(self):
        raise NotImplementedError(u'message_map_mode() should not be called directly on ButtonSliderElement')

    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        pass

    def connect_to(self, parameter):
        InputControlElement.connect_to(self, parameter)
        self._parameter_value_slot.subject = parameter
        if self._parameter_to_map_to != None:
            self._on_parameter_changed()

    def release_parameter(self):
        self._parameter_value_slot.subject = None
        InputControlElement.release_parameter(self)

    def identifier_bytes(self):
        raise RuntimeWarning(u'identifier_bytes() should not be called on ButtonSliderElement')

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
        if value != 0 or not sender.is_momentary():
            index_of_sender = list(self._buttons).index(sender)
            midi_value = int(old_div(127 * index_of_sender, len(self._buttons) - 1))
            if self._parameter_to_map_to != None and self._parameter_to_map_to.is_enabled:
                param_range = self._parameter_to_map_to.max - self._parameter_to_map_to.min
                param_value = old_div(param_range * index_of_sender, len(self._buttons) - 1) + self._parameter_to_map_to.min
                if index_of_sender > 0:
                    param_value += old_div(param_range, 4 * len(self._buttons))
                    if param_value > self._parameter_to_map_to.max:
                        param_value = self._parameter_to_map_to.max
                self._parameter_to_map_to.value = param_value
            self.notify_value(midi_value)

    def _on_parameter_changed(self):
        assert self._parameter_to_map_to != None
        param_range = abs(self._parameter_to_map_to.max - self._parameter_to_map_to.min)
        midi_value = int(old_div(127 * abs(self._parameter_to_map_to.value - self._parameter_to_map_to.min), param_range))
        self.send_value(midi_value)
