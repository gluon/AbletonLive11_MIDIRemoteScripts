# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\SysexValueControl.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1148 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .InputControlElement import MIDI_SYSEX_TYPE, InputControlElement

class SysexValueControl(InputControlElement):

    def __init__(self, message_prefix=None, value_enquiry=None, default_value=None, *a, **k):
        (super(SysexValueControl, self).__init__)(a, msg_type=MIDI_SYSEX_TYPE, sysex_identifier=message_prefix, **k)
        self._value_enquiry = value_enquiry
        self._default_value = default_value

    def send_value(self, value_bytes):
        self.send_midi(self.message_sysex_identifier() + value_bytes + (247, ))

    def enquire_value(self):
        self.send_midi(self._value_enquiry)

    def reset(self):
        if self._default_value != None:
            self.send_value(self._default_value)