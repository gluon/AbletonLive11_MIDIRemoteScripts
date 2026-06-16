# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\track_util.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 6989 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
import Live
from ableton.v2.base import compose, const, depends, find_if, liveobj_valid
from .clip_util import clip_of_slot, has_clip

def playing_slot_index(track):
    if liveobj_valid(track):
        return track.playing_slot_index


def playing_or_recording_clip_slot(track):
    index = playing_slot_index(track)
    if index is not None:
        if index >= 0:
            slot = track.clip_slots[index]
            if liveobj_valid(slot):
                return slot


def fired_clip_slot(track):
    if liveobj_valid(track):
        if track.fired_slot_index >= 0:
            slot = track.clip_slots[track.fired_slot_index]
            if liveobj_valid(slot):
                return slot


def is_fired(track):
    if liveobj_valid(track):
        return track.fired_slot_index != -1


def playing_clip_slot(track):
    slot = playing_or_recording_clip_slot(track)
    if liveobj_valid(slot):
        if not slot.is_recording:
            return slot


def recording_clip_slot(track):
    slot = playing_or_recording_clip_slot(track)
    if liveobj_valid(slot):
        if slot.is_recording:
            return slot


playing_or_recording_clip = compose(clip_of_slot, playing_or_recording_clip_slot)
playing_clip = compose(clip_of_slot, playing_clip_slot)
recording_clip = compose(clip_of_slot, recording_clip_slot)

@depends(song=(const(None)))
def get_or_create_first_empty_clip_slot(track, song=None):
    if liveobj_valid(track):
        first_empty_slot = find_if(lambda s: not s.has_clip
, track.clip_slots)
        if first_empty_slot:
            if liveobj_valid(first_empty_slot):
                return first_empty_slot
        try:
            song.create_scene(-1)
            slot = track.clip_slots[-1]
            if liveobj_valid(slot):
                return slot
        except Live.Base.LimitationError:
            pass


def last_slot_with_clip(track):
    return find_if(has_clip, reversed(clip_slots(track)))


def clip_slots(track):
    if liveobj_valid(track):
        return track.clip_slots
    return []


def is_playing(track):
    if liveobj_valid(track):
        return track.playing_slot_index >= 0


def is_group_track(track):
    if liveobj_valid(track):
        return track.is_foldable


def is_grouped(track):
    if liveobj_valid(track):
        return track.is_grouped


def group_track(track):
    if is_grouped(track):
        return track.group_track


def flatten_tracks(tracks):
    return chain(*(grouped_tracks(t) if is_group_track(t) else [t] for t in tracks))


@depends(song=(const(None)))
def grouped_tracks(track, song=None):
    if not is_group_track(track):
        return []
    return flatten_tracks(filter(lambda t: group_track(t) == track
, song.tracks))


def toggle_fold(track):
    if is_group_track(track):
        track.fold_state = not track.fold_state
        return True
    return False


def is_folded(track):
    if is_group_track(track):
        return track.fold_state


def has_clips(track):
    if is_group_track(track):
        return any(map(has_clips, grouped_tracks(track)))
    return any(map(has_clip, clip_slots(track)))


def can_be_armed(track):
    if liveobj_valid(track):
        return track.can_be_armed


def arm(track):
    if can_be_armed(track):
        track.arm = True
        return True
    return False


def unarm(track):
    if can_be_armed(track):
        track.arm = False
        return True
    return False


def stop_all_clips(track, quantized=True):
    if liveobj_valid(track):
        track.stop_all_clips(quantized)
        return True
    return False


def unarm_tracks(tracks):
    for track in tracks:
        unarm(track)


def tracks(song):
    return filter(liveobj_valid, song.tracks)


def visible_tracks(song):
    return filter(liveobj_valid, song.visible_tracks)