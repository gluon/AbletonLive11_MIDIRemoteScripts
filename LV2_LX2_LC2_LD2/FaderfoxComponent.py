# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/LV2_LX2_LC2_LD2/FaderfoxComponent.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 1548 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, range
from .consts import *

class FaderfoxComponent(object):
    __module__ = __name__
    __doc__ = 'Baseclass for a subcomponent for Faderfox controllers.'
    __filter_funcs__ = ['update_display', 'log']

    def __init__(self, parent):
        FaderfoxComponent.realinit(self, parent)

    def realinit(self, parent):
        self.parent = parent
        self.helper = parent.helper
        self.param_map = parent.param_map

    def log(self, string):
        self.parent.log(string)

    def logfmt(self, fmt, *args):
        args2 = []
        for i in range(0, len(args)):
            args2 += [args[i].__str__()]

        str = fmt % tuple(args2)
        return self.log(str)

    def application(self):
        return self.parent.application()

    def song(self):
        return self.parent.song()

    def send_midi(self, midi_event_bytes):
        self.parent.send_midi(midi_event_bytes)

    def request_rebuild_midi_map(self):
        self.parent.request_rebuild_midi_map()

    def disconnect(self):
        pass

    def build_midi_map(self, script_handle, midi_map_handle):
        pass

    def receive_midi_cc(channel, cc_no, cc_value):
        pass

    def receive_midi_note(channel, status, note, velocity):
        pass

    def refresh_state(self):
        pass

    def update_display(self):
        pass