# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\device_chain_utils.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 769 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from itertools import chain
import Live
from ableton.v2.base import find_if, liveobj_valid

def is_empty_drum_pad(drum_pad):
    return isinstance(drum_pad, Live.DrumPad.DrumPad) and (not drum_pad.chains or not drum_pad.chains[0].devices)


def is_first_device_on_pad(device, drum_pad):
    return find_if(lambda pad: pad.chains and pad.chains[0].devices and pad.chains[0].devices[0] == device
, drum_pad.canonical_parent.drum_pads)


def is_simpler(device):
    return device and device.class_name == 'OriginalSimpler'