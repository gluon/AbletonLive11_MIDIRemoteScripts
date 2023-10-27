# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\clip_util.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 1961 bytes
from __future__ import absolute_import, print_function, unicode_literals
from past.utils import old_div
from ableton.v2.base import compose, find_if, liveobj_valid

def has_clip(slot):
    if liveobj_valid(slot):
        return slot.has_clip


def clip_of_slot(slot):
    if liveobj_valid(slot):
        if liveobj_valid(slot.clip):
            return slot.clip


def fire(clip_or_slot, **k):
    if liveobj_valid(clip_or_slot):
        (clip_or_slot.fire)(**k)
        return True
    return False


def delete_clip(slot):
    if liveobj_valid(slot):
        if has_clip(slot):
            slot.delete_clip()
            return True
    return False


def is_looping(clip):
    if liveobj_valid(clip):
        return clip.looping


def get_clip_time(clip):
    sig_num, sig_denom = clip.signature_numerator, clip.signature_denominator
    loop_position = (clip.playing_position - clip.loop_start) * old_div(sig_denom, 4.0)
    beats = int(loop_position) % sig_num + 1
    bars = int(old_div(loop_position, sig_num)) + 1
    return (
     bars, beats)