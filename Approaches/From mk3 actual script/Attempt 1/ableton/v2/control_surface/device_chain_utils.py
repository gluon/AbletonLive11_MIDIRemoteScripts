#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/device_chain_utils.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from builtins import map
from itertools import chain
from functools import partial
from ..base import find_if, liveobj_valid

def find_instrument_devices(track_or_chain):
    u"""
    Returns a list with all instruments from a track or chain.
    """
    if liveobj_valid(track_or_chain):
        instrument = find_if(lambda d: d.type == Live.Device.DeviceType.instrument, track_or_chain.devices)
        if liveobj_valid(instrument):
            if not instrument.can_have_drum_pads and instrument.can_have_chains:
                return chain([instrument], *map(find_instrument_devices, instrument.chains))
            return [instrument]
    return []


def find_instrument_meeting_requirement(requirement, track_or_chain):
    if liveobj_valid(track_or_chain):
        instrument = find_if(lambda d: d.type == Live.Device.DeviceType.instrument, track_or_chain.devices)
        if liveobj_valid(instrument):
            if requirement(instrument):
                return instrument
            if instrument.can_have_chains:
                recursive_call = partial(find_instrument_meeting_requirement, requirement)
                return find_if(bool, map(recursive_call, instrument.chains))
