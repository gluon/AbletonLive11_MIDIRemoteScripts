# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\live\action.py
# Compiled at: 2023-10-06 07:41:29
# Size of source mod 2**32: 12404 bytes
from __future__ import absolute_import, print_function, unicode_literals
import logging
from functools import singledispatch, wraps
from sys import maxsize
from typing import Optional, Union
from Live.Base import LimitationError
import Live.Clip as Clip
import Live.ClipSlot as ClipSlot
import Live.DeviceParameter as DeviceParameter
import Live.Scene as Scene
from Live.Song import Quantization
import Live.Track as Track
from . import liveobj_changed, liveobj_valid, scene_index, song, track_index
from .util import is_clip_new_recording, raise_type_error_for_liveobj
logger = logging.getLogger(__name__)

def action(func):
    singledispatch_func = singledispatch(func)

    @wraps(func)
    def wrapper(target, *a, **k):
        if liveobj_valid(target):
            try:
                return singledispatch_func(target, *a, **k)
            except (
             AttributeError,
             AssertionError,
             ValueError,
             RuntimeError,
             TypeError,
             LimitationError) as e:
                try:
                    logger.debug('An exception occurred when attempting to perform an action: %s', e)
                finally:
                    e = None
                    del e

            return False

    wrapper.register = singledispatch_func.register
    return wrapper


@action
def arm(track: Track, exclusive=None) -> bool:
    if track.can_be_armed:
        exclusive = exclusive if exclusive is not None else song().exclusive_arm
        new_value = not track.arm
        for t in song().tracks:
            if t.can_be_armed:
                if not (t == track or track).is_part_of_selection or t.is_part_of_selection:
                    t.arm = new_value
                else:
                    if exclusive:
                        if t.arm:
                            t.arm = False

        return True
    return False


@action
def delete(deletable: Union[(Clip, ClipSlot, Scene, Track)]) -> bool:
    return raise_type_error_for_liveobj(deletable)


@delete.register
def _(deletable: Clip):
    if deletable.is_arrangement_clip:
        deletable.canonical_parent.delete_clip(deletable)
    else:
        deletable.canonical_parent.delete_clip()
    return True


@delete.register
def _(deletable: ClipSlot):
    deletable.delete_clip()
    return True


@delete.register
def _(deletable: Scene):
    song().delete_scene(scene_index(deletable))
    return True


@delete.register
def _(deletable: Track):
    if deletable in song().return_tracks:
        song().delete_return_track(track_index(deletable, track_list=(list(song().return_tracks))))
    else:
        song().delete_track(track_index(deletable))
    return True


@action
def delete_notes_with_pitch(clip: Clip, pitch: int) -> bool:
    args = dict(from_time=0, from_pitch=pitch, time_span=maxsize, pitch_span=1)
    if (clip.get_notes_extended)(**args):
        (clip.remove_notes_extended)(**args)
        return True
    return False


@action
def delete_notes_in_range(clip, from_time, time_span):
    args = dict(from_time=from_time, from_pitch=0, time_span=time_span, pitch_span=128)
    if (clip.get_notes_extended)(**args):
        (clip.remove_notes_extended)(**args)
        return True
    return False


@action
def duplicate_loop(clip: Clip) -> bool:
    clip.duplicate_loop()
    clip.view.show_loop()
    return True


@action
def duplicate(duplicatable: Union[(Clip, ClipSlot, Scene, Track)]) -> bool:
    return raise_type_error_for_liveobj(duplicatable)


@duplicate.register
def _(duplicatable: Clip):
    if duplicatable.is_arrangement_clip:
        track = duplicatable.canonical_parent
        track.duplicate_clip_to_arrangement(duplicatable, duplicatable.end_time)
        return True
    return duplicate(duplicatable.canonical_parent)


@duplicate.register
def _(duplicatable: ClipSlot):
    track = duplicatable.canonical_parent
    track.duplicate_clip_slot(list(track.clip_slots).index(duplicatable))
    return True


@duplicate.register
def _(duplicatable: Scene):
    song().duplicate_scene(scene_index(duplicatable))
    return True


@duplicate.register
def _(duplicatable: Track):
    song().duplicate_track(track_index(duplicatable))
    return True


@action
def duplicate_clip_special(clip: Clip) -> bool:
    if clip.is_arrangement_clip:
        track = clip.canonical_parent
        song().view.detail_clip = track.duplicate_clip_to_arrangement(clip, clip.end_time)
    else:
        slot = clip.canonical_parent
        track = slot.canonical_parent
        slot_index = list(track.clip_slots).index(slot)
        next_slot_index = track.duplicate_clip_slot(slot_index)
        song().view.selected_scene = song().scenes[next_slot_index]
        if clip.is_playing:
            track.clip_slots[next_slot_index].fire(force_legato=True,
              launch_quantization=(Quantization.q_no_q))
    return True


@action
def select(selectable: Union[(Clip, ClipSlot, Scene, Track)]) -> bool:
    return raise_type_error_for_liveobj(selectable)


@select.register
def _(selectable: Clip):
    return select(selectable.canonical_parent)


@select.register
def _(selectable: ClipSlot):
    if not liveobj_changed(song().view.highlighted_clip_slot, selectable):
        return False
    song().view.highlighted_clip_slot = selectable
    return True


@select.register
def _(selectable: Scene):
    if not liveobj_changed(song().view.selected_scene, selectable):
        return False
    song().view.selected_scene = selectable
    return True


@select.register
def _(selectable: Track):
    if not liveobj_changed(song().view.selected_track, selectable):
        return False
    song().view.selected_track = selectable
    return True


@action
def fire(fireable: Union[(Clip, ClipSlot, Scene)], button_state=None) -> bool:
    if isinstance(fireable, ClipSlot):
        if fireable.has_clip:
            fireable = fireable.clip
    if button_state is None:
        fireable.fire()
    else:
        fireable.set_fire_button_state(button_state)
        if button_state:
            if song().select_on_launch:
                select(fireable)
    return True


@action
def toggle_or_cycle_parameter_value(parameter: DeviceParameter) -> bool:
    if parameter.is_quantized:
        if parameter.value + 1 > parameter.max:
            parameter.value = parameter.min
        else:
            parameter.value = parameter.value + 1
    else:
        parameter.value = parameter.max if parameter.value == parameter.min else parameter.min
    return True


@action
def set_loop_start(clip: Clip, loop_start: float, show_loop: Optional[bool]=True) -> bool:
    if is_clip_new_recording(clip):
        return False
    clip.loop_start = loop_start
    clip.start_marker = loop_start
    if show_loop:
        clip.view.show_loop()
    return True


@action
def set_loop_end(clip: Clip, loop_end: float, show_loop: Optional[bool]=True) -> bool:
    if is_clip_new_recording(clip):
        return False
    clip.loop_end = loop_end
    clip.end_marker = loop_end
    if show_loop:
        clip.view.show_loop()
    return True


@action
def set_loop_position(clip, loop_start, loop_end):
    if is_clip_new_recording(clip):
        return False
    if loop_start < clip.loop_end:
        set_loop_start(clip, loop_start, show_loop=False)
        set_loop_end(clip, loop_end, show_loop=False)
    else:
        set_loop_end(clip, loop_end, show_loop=False)
        set_loop_start(clip, loop_start, show_loop=False)
    clip.view.show_loop()
    return True