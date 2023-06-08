from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import old_hasattr

def is_set_to_split_stereo(mixer):
    modes = Live.MixerDevice.MixerDevice.panning_modes
    return modes.stereo_split == getattr(mixer, 'panning_mode', modes.stereo)


def has_pan_mode(mixer):
    return old_hasattr(mixer, 'panning_mode')