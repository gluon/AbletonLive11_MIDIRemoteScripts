# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\sysex.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 6579 bytes
from __future__ import absolute_import, print_function, unicode_literals
from contextlib import contextmanager
from inspect import signature
from ...base import index_if, lazy_attribute
from .. import MIDI_SYSEX_TYPE, InputControlElement
from ..midi import is_valid_sysex

class SysexElement(InputControlElement):

    def __init__(self, send_message_generator=None, enquire_message=None, default_value=None, optimized=False, use_first_byte_as_value=False, *a, **k):
        (super().__init__)(a, msg_type=MIDI_SYSEX_TYPE, send_should_depend_on_forwarding=False, **k)
        self._send_message_generator = send_message_generator
        self._enquire_message = enquire_message
        self._default_value = default_value
        self._optimized = optimized
        self._use_first_byte_as_value = use_first_byte_as_value
        self._is_deferring_send = False
        self._deferred_message = None

    def message_map_mode(self):
        raise AssertionError("SysexElement doesn't support mapping.")

    def receive_value(self, value):
        if self._use_first_byte_as_value:
            value = value[0]
        super().receive_value(value)

    def send_value(self, *a, **k):
        if self._send_message_generator:
            message = (self._send_message_generator)(*a, **k)
            if message is not None:
                self._do_send_value(message)

    def enquire_value(self):
        self.send_midi(self._enquire_message)

    def reset(self):
        if self._default_value is not None:
            self.send_value(self._default_value)

    @contextmanager
    def deferring_send(self):
        try:
            self._deferred_message = None
            self._is_deferring_send = True
            yield
        finally:
            self._is_deferring_send = False
            if self._deferred_message is not None:
                self._do_send_value(self._deferred_message)

    def _do_send_value(self, message):
        if not (self._is_deferring_send or self)._optimized or message != self._last_sent_message:
            if self.send_midi(message):
                self._last_sent_message = message
        else:
            if self._is_deferring_send:
                self._deferred_message = message

    @property
    def _last_sent_value(self):
        if self._last_sent_message:
            return self._last_sent_message
        return -1


class CachingSendMessageGenerator:

    def __init__(self, generator):
        self._generator = generator
        self._generator_params = signature(self._generator).parameters

    def __call__(self, *a, **k):
        message = None
        if k:
            self._update_cached_values_from_kwargs(k)
            if None not in self._cached_argument_values:
                message = (self._generator)(*self._cached_argument_values)
        else:
            for i, value in enumerate(a):
                self._cached_argument_values[i] = value

            message = (self._generator)(*a)
        return message

    @lazy_attribute
    def _cached_argument_values(self):
        return [
         None] * len(self._generator_params)

    def _update_cached_values_from_kwargs(self, kwargs):
        for key, value in kwargs.items():
            kwarg_index = index_if(lambda param_name, kwarg_name=key: param_name == kwarg_name
, self._generator_params)
            self._cached_argument_values[kwarg_index] = value