# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/device_util.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 1134 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import liveobj_valid

def is_drum_pad(item):
    return liveobj_valid(item) and isinstance(item, Live.DrumPad.DrumPad)


def find_chain_or_track(item):
    if is_drum_pad(item) and item.chains:
        chain = item.chains[0]
    else:
        chain = item
        while liveobj_valid(chain):
            if not isinstance(chain, (Live.Track.Track, Live.Chain.Chain)):
                chain = getattr(chain, 'canonical_parent', None)

    return chain


def find_rack(item):
    rack = item
    while liveobj_valid(rack):
        if not isinstance(rack, Live.RackDevice.RackDevice):
            rack = getattr(rack, 'canonical_parent', None)

    return rack