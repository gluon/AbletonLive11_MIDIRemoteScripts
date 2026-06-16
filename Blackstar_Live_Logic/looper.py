# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\looper.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 13907 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from itertools import chain, islice, repeat
from math import ceil
from ableton.v2.base import compose, find_if, listens, listens_group, liveobj_valid, task
from ableton.v2.control_surface import Component
from .clip_util import *
from .elements import NUM_LOOPER_SWITCHES
from .footswitch_row_control import footswitch_row_control
from .time_display import TimeDisplayControl
from .track_util import *

class LooperComponent(Component):
    foot_switches = footswitch_row_control(control_count=NUM_LOOPER_SWITCHES)
    time_display = TimeDisplayControl()

    def __init__(self, session_ring=None, *a, **k):
        (super(LooperComponent, self).__init__)(*a, **k)
        self._tracks = []
        self._last_playing_slot_index_for_track = {}
        self._last_stopped_slot_for_track = {}
        self._clips_triggered_to_play_by_looper = set()
        self._longest_playing_clip = None
        self._delete_target_for_track = {}
        self._is_clip_recording_slots = [self.register_slot(None, partial(self._clip_state_changed, i), 'is_recording') for i in range(NUM_LOOPER_SWITCHES)]
        self._LooperComponent__on_song_time_changed.subject = self.song
        self._LooperComponent__on_track_list_changed.subject = self.song
        self._LooperComponent__on_song_is_playing_changed.subject = self.song

    def update(self):
        super(LooperComponent, self).update()
        self._LooperComponent__on_song_time_changed()
        self._LooperComponent__on_track_list_changed()
        self._LooperComponent__on_song_is_playing_changed()

    @foot_switches.released_immediately
    def foot_switches(self, switch):
        if switch._double_click_context.click_count > 0:
            return
        track = self._tracks[switch.index]
        if not is_group_track(track):
            self._delete_target_for_track[track] = self._get_controlled_clip_slot(track) if (not fired_clip_slot(track)) else None
            self._begin_or_finish_loop(track)

    @foot_switches.pressed_delayed
    def foot_switches(self, switch):
        self._start_or_stop_playback(self._tracks[switch.index])

    @foot_switches.double_clicked
    def foot_switches(self, switch):
        track = self._tracks[switch.index]
        if is_group_track(track):
            toggle_fold(track)
        else:
            self._delete_clip(track)

    @listens('current_song_time')
    def __on_song_time_changed(self):
        if not self.song.is_playing:
            return
        time = self.song.get_current_beats_song_time()
        self.foot_switches.update_time(time)
        if liveobj_valid(self._longest_playing_clip):
            bars, beats = get_clip_time(self._longest_playing_clip)
        else:
            bars, beats = 0, time.beats
        self.time_display.update_time(bars, beats)

    @listens('is_playing')
    def __on_song_is_playing_changed(self):
        if self.song.is_playing:
            self._update_longest_playing_clip()
        else:
            self.time_display.update_time(0, 0)

    @listens('visible_tracks')
    def __on_track_list_changed(self):
        self._update_tracks()

    @listens_group('fired_slot_index')
    def __on_fired_slot_index_changed(self, track):
        self._update_track(track)

    @listens_group('playing_slot_index')
    def __on_playing_slot_index_changed(self, track):
        self._update_track(track, update_parent_group=True)
        self._update_last_stopped_slot_for_track(track)
        if self._delete_target_for_track.get(track, False) is None:
            self._delete_target_for_track[track] = playing_or_recording_clip_slot(track)
        if track in self._tracks:
            self._is_clip_recording_slots[self._tracks.index(track)].subject = playing_or_recording_clip(track)
        self._update_longest_playing_clip(first_record=(not any(map(playing_or_recording_clip_slot, filter(lambda t: t != track
, self._tracks)))))

    @listens_group('input_routing_type')
    def __on_input_routing_type_changed(self, track):
        self._update_tracks()

    def _begin_or_finish_loop(self, track):
        self._clips_triggered_to_play_by_looper = set(filter(liveobj_valid, self._clips_triggered_to_play_by_looper))
        slot = recording_clip_slot(track)
        if slot:
            self._clips_triggered_to_play_by_looper.add(clip_of_slot(slot))
        else:
            slot = get_or_create_first_empty_clip_slot(track)
            if slot:
                arm(track)
        fire(slot)

    def _start_or_stop_playback(self, track):
        if not has_clips(track):
            self.song.is_playing = True
            if not is_group_track(track):
                return self._exclusive_arm(track)
            return self._exclusive_arm_next_track(self._tracks.index(track))
        if is_group_track(track):
            return self._start_or_stop_group_track(track)
        if playing_or_recording_clip_slot(track):
            if not self.song.is_playing:
                self.song.is_playing = True
                return
            stop_all_clips(track)
            if self.song.exclusive_arm:
                any(map(recording_clip_slot, filter(lambda t: t != track
, self._tracks))) or self._exclusive_arm(track)
        else:
            fire(self._get_controlled_clip_slot(track))

    def _start_or_stop_group_track(self, track):
        playing_children = list(filter(is_playing, grouped_tracks(track)))
        if playing_children:
            if not self.song.is_playing:
                self.song.is_playing = True
                return
            for t in playing_children:
                stop_all_clips(t)

        else:
            for t in grouped_tracks(track):
                fire(self._get_controlled_clip_slot(t))

    def _delete_clip(self, track):
        delete_target = self._delete_target_for_track.get(track, None)
        if track in self._delete_target_for_track:
            del self._delete_target_for_track[track]
        if liveobj_valid(delete_target):
            delete_clip(delete_target)
            delete_clip(playing_or_recording_clip_slot(track))
            stop_all_clips(track, quantized=False)
        else:
            self._cancel_recording(track)
        self._exclusive_arm(track)

    def _cancel_recording(self, track):
        slot = playing_clip_slot(track)
        if not fire(slot, force_legato=True):
            stop_all_clips(track, quantized=False)

    def _clip_state_changed(self, index):
        self._update_track((self._tracks[index]), update_parent_group=True)

    def _update_tracks(self):
        self._tracks = list(islice(chain(filter(lambda t: can_be_armed(t) or is_group_track(t)
, visible_tracks(self.song)), repeat(None)), NUM_LOOPER_SWITCHES))
        self._LooperComponent__on_fired_slot_index_changed.replace_subjects(self._tracks)
        self._LooperComponent__on_playing_slot_index_changed.replace_subjects(flatten_tracks(self._tracks))
        self._LooperComponent__on_input_routing_type_changed.replace_subjects(self._tracks)
        for i, track in enumerate(self._tracks):
            self._update_leds(i, track)
            self._is_clip_recording_slots[i].subject = playing_or_recording_clip(track)

    def _update_track(self, track, update_parent_group=False):
        if update_parent_group:
            if is_grouped(track):
                parent_group = group_track(track)
                if parent_group in self._tracks:
                    self._update_track(parent_group, update_parent_group=True)
        if track in filter(liveobj_valid, self._tracks):
            index = self._tracks.index(track)
            if recording_clip_slot(track):
                self._exclusive_arm(track)
            if playing_clip_slot(track):
                clip = playing_clip(track)
                if clip in self._clips_triggered_to_play_by_looper:
                    self._exclusive_arm_next_track(index)
                    self._clips_triggered_to_play_by_looper.remove(clip)
            self._update_leds(self._tracks.index(track), track)

    def _update_leds(self, index, track):
        color = 'DefaultButton.Off'
        if is_fired(track):
            color = 'Subdivision_Pulse'
        else:
            pass
        if recording_clip_slot(track) or any(map(recording_clip_slot, grouped_tracks(track))):
            color = 'Beat_Pulse'
        else:
            if playing_clip_slot(track) or any(map(playing_clip_slot, grouped_tracks(track))):
                color = 'DefaultButton.On'
        self.foot_switches[index].color = color

    def _exclusive_arm_next_track(self, index):
        if not self.song.exclusive_arm:
            return
        next_index = (index + 1) % len(self._tracks)
        self._exclusive_arm(find_if(lambda t: liveobj_valid(t) and not is_group_track(t) and not playing_or_recording_clip_slot(t)
, chain(self._tracks[next_index:], self._tracks[:next_index])) or self._tracks[next_index])

    def _exclusive_arm(self, track):
        if not self.song.exclusive_arm or is_group_track(track):
            return
        self._tasks.add(task.run(lambda: arm(track) and unarm_tracks(filter(lambda t: t != track
, self.song.tracks))
))

    def _update_last_stopped_slot_for_track(self, track):
        if not is_playing(track):
            if track in self._last_playing_slot_index_for_track:
                last_playing_index = self._last_playing_slot_index_for_track[track]
                slots = clip_slots(track)
                if 0<= last_playing_index < len(slots):
                    self._last_stopped_slot_for_track[track] = slots[last_playing_index]
        self._last_playing_slot_index_for_track[track] = playing_slot_index(track)

    def _update_longest_playing_clip(self, first_record=False):
        longest_length = -1
        longest_loop_start_bar = 1
        self._longest_playing_clip = None
        for clip in filter(is_looping, map(playing_or_recording_clip if first_record else playing_clip, flatten_tracks(self._tracks))):
            loop_length = clip.loop_end - clip.loop_start
            if loop_length > longest_length:
                longest_length = loop_length
                self._longest_playing_clip = clip

    def _get_controlled_clip_slot(self, track):
        return playing_or_recording_clip_slot(track) or self._get_last_stopped_slot_with_clip(track) or last_slot_with_clip(track)

    def _get_last_stopped_slot_with_clip(self, track):
        last_stopped = self._last_stopped_slot_for_track.get(track, None)
        if has_clip(last_stopped):
            return last_stopped