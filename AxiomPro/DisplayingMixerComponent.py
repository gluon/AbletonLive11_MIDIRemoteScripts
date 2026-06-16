# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AxiomPro\DisplayingMixerComponent.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 7001 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range, str
import _Framework.ButtonElement as ButtonElement
import _Framework.MixerComponent as MixerComponent
import _Framework.PhysicalDisplayElement as PhysicalDisplayElement

class DisplayingMixerComponent(MixerComponent):

    def __init__(self, num_tracks):
        MixerComponent.__init__(self, num_tracks)
        self._selected_tracks = []
        self._display = None
        self._mute_button = None
        self._solo_button = None
        self._register_timer_callback(self._on_timer)

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        self._selected_tracks = None
        MixerComponent.disconnect(self)
        self._display = None

    def set_display(self, display):
        self._display = display

    def set_solo_button(self, button):
        self.selected_strip().set_solo_button(button)
        if self._solo_button != button:
            if self._solo_button != None:
                self._solo_button.remove_value_listener(self._solo_value)
            self._solo_button = button
            if self._solo_button != None:
                self._solo_button.add_value_listener(self._solo_value)
            self.update()

    def set_mute_button(self, button):
        self.selected_strip().set_mute_button(button)
        if self._mute_button != button:
            if self._mute_button != None:
                self._mute_button.remove_value_listener(self._mute_value)
            self._mute_button = button
            if self._mute_button != None:
                self._mute_button.add_value_listener(self._mute_value)
            self.update()

    def _on_timer(self):
        sel_track = None
        while len(self._selected_tracks) > 0:
            track = self._selected_tracks[-1]
            if track != None:
                if track.has_midi_input:
                    if track.can_be_armed:
                        if not track.arm:
                            sel_track = track
                            break
                        del self._selected_tracks[-1]

        if sel_track != None:
            found_recording_clip = False
            song = self.song()
            tracks = song.tracks
            check_arrangement = song.is_playing and song.record_mode
            for track in tracks:
                if track.can_be_armed:
                    if track.arm:
                        if check_arrangement:
                            found_recording_clip = True
                            break
                        else:
                            playing_slot_index = track.playing_slot_index
                        if playing_slot_index in range(len(track.clip_slots)):
                            slot = track.clip_slots[playing_slot_index]
                            if slot.has_clip:
                                if slot.clip.is_recording:
                                    found_recording_clip = True
                                    break

            if not found_recording_clip:
                if song.exclusive_arm:
                    for track in tracks:
                        if track.can_be_armed:
                            if track.arm:
                                if track != sel_track:
                                    track.arm = False

                sel_track.arm = True
                sel_track.view.select_instrument()
        self._selected_tracks = []

    def _solo_value(self, value):
        if self._display != None:
            if self.song().view.selected_track not in (
             self.song().master_track,
             None):
                if value != 0:
                    track = self.song().view.selected_track
                    display_string = str(track.name) + ': Solo '
                    if track.solo:
                        display_string += 'On'
                    else:
                        display_string += 'Off'
                    self._display.display_message(display_string)
                else:
                    self._display.update()

    def _mute_value(self, value):
        if self._display != None:
            if self.song().view.selected_track not in (
             self.song().master_track,
             None):
                if value != 0:
                    track = self.song().view.selected_track
                    display_string = str(track.name) + ': Mute '
                    if track.mute:
                        display_string += 'On'
                    else:
                        display_string += 'Off'
                    self._display.display_message(display_string)
                else:
                    self._display.update()

    def _next_track_value(self, value):
        MixerComponent._next_track_value(self, value)
        self._selected_tracks.append(self.song().view.selected_track)

    def _prev_track_value(self, value):
        MixerComponent._prev_track_value(self, value)
        self._selected_tracks.append(self.song().view.selected_track)