# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\pad_sensitivity.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 1981 bytes
from __future__ import absolute_import, print_function, unicode_literals
from collections import namedtuple
playing_profile = 0
default_profile = 1
loop_selector_profile = 2
MONO_AFTERTOUCH_ENABLED = 1
MONO_AFTERTOUCH_DISABLED = 0
PadSettings = namedtuple('PadSettings', ['sensitivity', 'aftertouch_enabled'])

def index_to_pad_coordinate(index):
    x, y = divmod(index, 8)
    return (
     8 - x, y + 1)


def pad_parameter_sender(global_control, pad_control, aftertouch_control):

    def do_send(pad_settings, pad=None):
        if pad is None:
            global_control.send_value(0, 0, pad_settings.sensitivity)
            aftertouch_control.send_value(0, 0, pad_settings.aftertouch_enabled)
        else:
            scene, track = index_to_pad_coordinate(pad)
            pad_control.send_value(scene, track, pad_settings.sensitivity)
            aftertouch_control.send_value(scene, track, pad_settings.aftertouch_enabled)

    return do_send