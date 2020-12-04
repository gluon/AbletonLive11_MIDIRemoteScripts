#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/pad_sensitivity.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import lazy_attribute, NamedTuple
from .sysex import to_bytes

class PadParameters(NamedTuple):
    u"""
    Describes the properties of pad parameters.
    """
    off_threshold = 0
    on_threshold = 0
    gain = 0
    curve1 = 0
    curve2 = 0
    name = u''

    def __str__(self):
        return self.name

    @lazy_attribute
    def sysex_bytes(self):
        return to_bytes(self.off_threshold, 4) + to_bytes(self.on_threshold, 4) + to_bytes(self.gain, 8) + to_bytes(self.curve1, 8) + to_bytes(self.curve2, 8)


def pad_parameter_sender(global_control, pad_control):
    u"""
    Sends the sensitivity parameters for a given pad, or all pads (pad
    == None) over the given ValueControl.
    """

    def do_send(parameters, pad = None):
        if pad != None:
            pad_control.send_value((pad,) + parameters.sysex_bytes)
        else:
            global_control.send_value(parameters.sysex_bytes)

    return do_send
