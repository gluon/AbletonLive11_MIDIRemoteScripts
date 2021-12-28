#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/elements/sysex_element.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import old_hasattr
from ...base.dependency import depends
from ..input_control_element import InputControlElement, MIDI_SYSEX_TYPE
from .. import midi

class SysexElement(InputControlElement):
    u"""
    Control element for sending and receiving sysex message.
    
    Set sysex_identifier to the unique static part of the sysex message, to notify
    the value event about incoming sysex messages.
    
    send_message_generator should be a function object that takes the arguments of
    send_value and generates a valid sysex message. send_value will raise an error
    if the generated message is not valid.
    
    enquire_message is the sysex message for requesting a value. Use enquire_value to
    send out the message.
    
    default_value is being used when calling reset on the element. The value is passed
    as an argument to send_value. Setting the property to None will disable sending
    a value when resetting the element (default).
    """

    def __init__(self, send_message_generator = None, enquire_message = None, default_value = None, optimized = False, *a, **k):
        super(SysexElement, self).__init__(msg_type=MIDI_SYSEX_TYPE, *a, **k)
        self._send_message_generator = send_message_generator
        self._enquire_message = enquire_message
        self._default_value = default_value
        self._optimized = optimized

    def send_value(self, *arguments):
        assert self._send_message_generator is not None
        message = self._send_message_generator(*arguments)
        assert midi.is_valid_sysex(message), u'Trying to send sysex message %r, which is not valid.' % list(map(hex, message))
        self._do_send_value(message)

    def enquire_value(self):
        assert self._enquire_message is not None
        self.send_midi(self._enquire_message)

    def reset(self):
        if self._default_value is not None:
            self.send_value(self._default_value)

    def _do_send_value(self, message):
        if self._optimized:
            if message != self._last_sent_message and self.send_midi(message):
                self._last_sent_message = message
        else:
            self.send_midi(message)

    @property
    def _last_sent_value(self):
        if self._last_sent_message:
            return self._last_sent_message
        return -1


class ColorSysexElement(SysexElement):

    @depends(skin=None)
    def __init__(self, skin = None, *a, **k):
        super(ColorSysexElement, self).__init__(*a, **k)
        self._skin = skin

    def set_light(self, value):
        color = None
        if old_hasattr(value, u'draw'):
            color = value
        else:
            color = self._skin[value]
        color.draw(self)
