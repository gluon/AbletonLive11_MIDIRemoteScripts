#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/base/live_api_utils.py
from __future__ import absolute_import, print_function, unicode_literals

def liveobj_changed(obj, other):
    u"""
    Check whether obj and other are not equal, properly handling lost weakrefs.
    
    Use this whenever you cache a Live API object in some variable, and want to check
    whether you need to update the cached object.
    """
    return obj != other or type(obj) != type(other)


def liveobj_valid(obj):
    u"""
    Check whether obj represents a valid Live API obj.
    
    This will return False both if obj represents a lost weakref or is None.
    It's important that Live API objects are not checked using "is None", since this
    would treat lost weakrefs as valid.
    """
    return obj != None


def is_parameter_bipolar(param):
    return param.min == -1 * param.max


def duplicate_clip_loop(clip):
    if liveobj_valid(clip) and clip.is_midi_clip:
        try:
            clip.duplicate_loop()
        except RuntimeError:
            pass
