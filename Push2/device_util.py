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