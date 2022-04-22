# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/SysexValueControl.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 1115 bytes
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