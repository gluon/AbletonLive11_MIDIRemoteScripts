#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/mixable_utilities.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import old_hasattr
from ableton.v2.control_surface import find_instrument_meeting_requirement

def is_chain(track_or_chain):
    return isinstance(getattr(track_or_chain, u'proxied_object', track_or_chain), Live.Chain.Chain)


def is_midi_track(track):
    return getattr(track, u'has_midi_input', False) and not is_chain(track)


def is_audio_track(track):
    return getattr(track, u'has_audio_input', False) and not is_chain(track)


def can_play_clips(mixable):
    return old_hasattr(mixable, u'fired_slot_index')


def find_drum_rack_instrument(track):
    return find_instrument_meeting_requirement(lambda i: i.can_have_drum_pads, track)


def find_simpler(track_or_chain):
    return find_instrument_meeting_requirement(lambda i: old_hasattr(i, u'playback_mode'), track_or_chain)
