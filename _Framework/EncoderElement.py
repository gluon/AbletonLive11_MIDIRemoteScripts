# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/EncoderElement.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 7712 bytes
from __future__ import absolute_import, print_function, unicode_literals
from past.utils import old_div
import Live
from .ComboElement import WrapperElement
from .CompoundElement import CompoundElement
from .InputControlElement import MIDI_CC_TYPE, InputControlElement, InputSignal
from .SubjectSlot import SubjectEvent, subject_slot
from .Util import const, nop

def _not_implemented(value):
    raise NotImplementedError


_map_modes = map_modes = Live.MidiMap.MapMode
ENCODER_VALUE_NORMALIZER = {_map_modes.relative_smooth_two_compliment: lambda v: v if v <= 64 else v - 128, 
 _map_modes.relative_smooth_signed_bit: lambda v: v if v <= 64 else 64 - v, 
 _map_modes.relative_smooth_binary_offset: lambda v: v - 64}
MAX_14_BIT_CC = 95

class EncoderElement(InputControlElement):

    class ProxiedInterface(InputControlElement.ProxiedInterface):
        normalize_value = nop

    __subject_events__ = (
     SubjectEvent(name='normalized_value', signal=InputSignal),)
    encoder_sensitivity = 1.0

    def __init__(self, msg_type, channel, identifier, map_mode, encoder_sensitivity=None, *a, **k):
        (super(EncoderElement, self).__init__)(msg_type, channel, identifier, *a, **k)
        if encoder_sensitivity is not None:
            self.encoder_sensitivity = encoder_sensitivity
        if map_mode is _map_modes.absolute_14_bit and identifier > MAX_14_BIT_CC:
            self._EncoderElement__map_mode = _map_modes.absolute
        else:
            self._EncoderElement__map_mode = map_mode
        self._EncoderElement__value_normalizer = ENCODER_VALUE_NORMALIZER.get(map_mode, _not_implemented)

    def message_map_mode(self):
        return self._EncoderElement__map_mode

    def relative_value_to_delta(self, value):
        return self._EncoderElement__value_normalizer(value)

    def normalize_value(self, value):
        return old_div(self.relative_value_to_delta(value), 64.0) * self.encoder_sensitivity

    def notify_value(self, value):
        super(EncoderElement, self).notify_value(value)
        if self.normalized_value_listener_count():
            self.notify_normalized_value(self.normalize_value(value))


class TouchEncoderElementBase(EncoderElement):

    class ProxiedInterface(EncoderElement.ProxiedInterface):
        is_pressed = const(False)
        add_touch_value_listener = nop
        remove_touch_value_listener = nop
        touch_value_has_listener = nop

    __subject_events__ = ('touch_value', )

    def is_pressed(self):
        raise NotImplementedError


class TouchEncoderElement(CompoundElement, TouchEncoderElementBase):

    def __init__(self, channel=0, identifier=0, map_mode=_map_modes.absolute, touch_element=None, *a, **k):
        (super(TouchEncoderElement, self).__init__)(
 MIDI_CC_TYPE, channel, identifier, map_mode, *a, **k)
        self._touch_element = self.register_control_element(touch_element)

    def add_touch_value_listener(self, *a, **k):
        if self.value_listener_count() == 0:
            self.request_listen_nested_control_elements()
        (super(TouchEncoderElement, self).add_touch_value_listener)(*a, **k)

    def remove_touch_value_listener(self, *a, **k):
        (super(TouchEncoderElement, self).remove_touch_value_listener)(*a, **k)
        if self.value_listener_count() == 0:
            self.unrequest_listen_nested_control_elements()

    def on_nested_control_element_value(self, value, control):
        self.notify_touch_value(value)

    def is_pressed(self):
        return self.owns_control_element(self._touch_element) and self._touch_element.is_pressed()

    def on_nested_control_element_received(self, control):
        pass

    def on_nested_control_element_lost(self, control):
        pass


class FineGrainWithModifierEncoderElement(WrapperElement):

    def __init__(self, encoder=None, modifier=None, modified_sensitivity=0.1, default_sensitivity=None, *a, **k):
        (super(FineGrainWithModifierEncoderElement, self).__init__)(a, wrapped_control=encoder, **k)
        self._modified_sensitivity = modified_sensitivity
        self._default_sensitivity = default_sensitivity or self.wrapped_control.mapping_sensitivity
        self._normalized_value_listeners = []
        self._modifier = modifier
        self.register_control_elements(modifier, encoder)
        self._on_nested_control_element_value.add_subject(self._modifier)

    def add_normalized_value_listener(self, listener):
        self._normalized_value_listeners.append(listener)
        if len(self._normalized_value_listeners) == 1:
            self._enforce_control_invariant()

    def remove_normalized_value_listener(self, listener):
        self._normalized_value_listeners.remove(listener)
        if len(self._normalized_value_listeners) == 0:
            self._enforce_control_invariant()

    def normalized_value_has_listener(self, listener):
        return listener in self._normalized_value_listeners

    @subject_slot('normalized_value')
    def __on_normalized_value(self, value):
        for listener in self._normalized_value_listeners:
            listener(value)

    def on_nested_control_element_received(self, control):
        super(FineGrainWithModifierEncoderElement, self).on_nested_control_element_received(control)
        self._enforce_control_invariant()

    def on_nested_control_element_lost(self, control):
        super(FineGrainWithModifierEncoderElement, self).on_nested_control_element_lost(control)
        self._enforce_control_invariant()

    def on_nested_control_element_value(self, value, control):
        if control == self._modifier:
            self._enforce_control_invariant()
        else:
            super(FineGrainWithModifierEncoderElement, self).on_nested_control_element_value(value, control)

    def _enforce_control_invariant(self):
        if self.owns_control_element(self._wrapped_control):
            if self._modifier.is_pressed():
                self.wrapped_control.mapping_sensitivity = self._modified_sensitivity
            else:
                self.wrapped_control.mapping_sensitivity = self._default_sensitivity
        should_listen = self.owns_control_element(self._wrapped_control) and len(self._normalized_value_listeners) > 0
        self._FineGrainWithModifierEncoderElement__on_normalized_value.subject = self._wrapped_control if should_listen else None

    def set_sensitivities(self, default, modified):
        self._default_sensitivity = default
        self._modified_sensitivity = modified
        self._enforce_control_invariant()