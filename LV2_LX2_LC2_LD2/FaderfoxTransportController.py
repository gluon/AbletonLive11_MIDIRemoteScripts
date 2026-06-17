# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\LV2_LX2_LC2_LD2\FaderfoxTransportController.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 6962 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
from .consts import *
from .FaderfoxComponent import FaderfoxComponent

class FaderfoxTransportController(FaderfoxComponent):
    __module__ = __name__
    __doc__ = 'Class representing the transport section of faderfox controllers'
    __filter_funcs__ = ['update_display', 'log']

    def __init__(self, parent):
        FaderfoxTransportController.realinit(self, parent)

    def realinit(self, parent):
        FaderfoxComponent.realinit(self, parent)

    def receive_midi_cc(self, channel, cc_no, cc_value):
        if channel == CHANNEL_SETUP2:
            if cc_no == SCENE_SCROLL_CC:
                val = 0
                if cc_value >= 64:
                    val = cc_value - 128
                else:
                    val = cc_value
                idx = self.helper.selected_scene_idx() - val
                new_scene_idx = min(len(self.parent.song().scenes) - 1, max(0, idx))
                self.parent.song().view.selected_scene = self.parent.song().scenes[new_scene_idx]

    def receive_midi_note(self, channel, status, note_no, note_vel):

        def index_of(list, elt):
            for i in range(0, len(list)):
                if list[i] == elt:
                    return i

        if status == NOTEON_STATUS:
            if channel == CHANNEL_SETUP2:
                if note_no == SCENE_LAUNCH_NOTE:
                    self.parent.song().view.selected_scene.fire_as_selected()
                else:
                    if note_no == SCENE_STOP_NOTE:
                        self.parent.song().stop_all_clips()
                    else:
                        if note_no == SCENE_UP_NOTE:
                            idx = self.helper.selected_scene_idx() - 1
                            new_scene_idx = min(len(self.parent.song().scenes) - 1, max(0, idx))
                            self.parent.song().view.selected_scene = self.parent.song().scenes[new_scene_idx]
                        else:
                            if note_no == SCENE_DOWN_NOTE:
                                idx = self.helper.selected_scene_idx() + 1
                                new_scene_idx = min(len(self.parent.song().scenes) - 1, max(0, idx))
                                self.parent.song().view.selected_scene = self.parent.song().scenes[new_scene_idx]
                            else:
                                if note_no == GLOBAL_PLAY_NOTE:
                                    self.parent.song().start_playing()
                                else:
                                    if note_no == GLOBAL_STOP_NOTE:
                                        self.parent.song().stop_playing()
                                    else:
                                        if note_no == SESSION_ARRANGE_SWITCH_NOTE:
                                            view = self.parent.application().view
                                            if view.is_view_visible('Session'):
                                                view.show_view('Arranger')
                                            else:
                                                view.show_view('Session')
                                        else:
                                            if note_no == CLIP_TRACK_SWITCH_NOTE:
                                                view = self.parent.application().view
                                                if view.is_view_visible('Detail/Clip'):
                                                    view.show_view('Detail/DeviceChain')
                                                else:
                                                    view.show_view('Detail/Clip')
                                            else:
                                                if note_no == CLIP_SELECT_NOTE:
                                                    view = self.parent.application().view
                                                    if view.is_view_visible('Detail'):
                                                        view.hide_view('Detail')
                                                    else:
                                                        view.show_view('Detail')
                                                else:
                                                    if note_no in SCENE_LAUNCH_NOTES:
                                                        scene_idx = index_of(SCENE_LAUNCH_NOTES, note_no)
                                                        if scene_idx < len(self.parent.song().scenes):
                                                            self.parent.song().scenes[scene_idx].fire()
                                                    else:
                                                        track_idx = 0
                                                        for notes in SLOT_LAUNCH_NOTES2:
                                                            if note_no in notes[2:]:
                                                                clip_idx = index_of(notes, note_no) + 6
                                                                self.trigger_track_clip(track_idx, clip_idx)
                                                            else:
                                                                track_idx += 1

            else:
                if channel == TRACK_CHANNEL_SETUP2:
                    if note_no in LAUNCH_NOTES:
                        idx = index_of(LAUNCH_NOTES, note_no)
                        scene = self.parent.song().view.selected_scene
                        max_track_idx = len(scene.clip_slots)
                        if max_track_idx > idx:
                            scene.clip_slots[idx].fire()
                    if note_no in STOP_NOTES:
                        idx = index_of(STOP_NOTES, note_no)
                        if len(self.parent.song().tracks) > idx:
                            self.stop_track(idx)
                else:
                    if channel == AUX_CHANNEL_SETUP2:
                        track_idx = 0
                        for notes in SLOT_LAUNCH_NOTES1:
                            if note_no in notes:
                                self.trigger_track_clip(track_idx, index_of(notes, note_no))
                            else:
                                track_idx += 1

                        track_idx = 0
                        for notes in SLOT_LAUNCH_NOTES2:
                            if note_no in notes[0:2]:
                                self.trigger_track_clip(track_idx, index_of(notes, note_no) + 6)
                            else:
                                track_idx += 1

    def trigger_track_clip(self, track_idx, clip_idx):
        self.helper.trigger_track_clip(track_idx, clip_idx)

    def stop_track(self, track_idx):
        self.helper.stop_track(track_idx)

    def build_midi_map(self, script_handle, midi_map_handle):

        def forward_note(chan, note):
            Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, chan, note)

        def forward_cc(chan, cc):
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, chan, cc)

        forward_cc(CHANNEL_SETUP2, SCENE_SCROLL_CC)
        forward_note(CHANNEL_SETUP2, SCENE_UP_NOTE)
        forward_note(CHANNEL_SETUP2, SCENE_DOWN_NOTE)
        for note in LAUNCH_NOTES:
            forward_note(TRACK_CHANNEL_SETUP2, note)

        for note in STOP_NOTES:
            forward_note(TRACK_CHANNEL_SETUP2, note)

        forward_note(CHANNEL_SETUP2, SCENE_LAUNCH_NOTE)
        forward_note(CHANNEL_SETUP2, SCENE_STOP_NOTE)
        for note in [
         CLIP_SELECT_NOTE,
         GLOBAL_STOP_NOTE,
         GLOBAL_PLAY_NOTE,
         SESSION_ARRANGE_SWITCH_NOTE,
         CLIP_TRACK_SWITCH_NOTE]:
            forward_note(CHANNEL_SETUP2, note)

        for note in SCENE_LAUNCH_NOTES:
            forward_note(CHANNEL_SETUP2, note)

        for notes in SLOT_LAUNCH_NOTES1:
            for note in notes:
                forward_note(AUX_CHANNEL_SETUP2, note)

        for notes in SLOT_LAUNCH_NOTES2:
            for note in notes[0:2]:
                forward_note(AUX_CHANNEL_SETUP2, note)

            for note in notes[2:]:
                forward_note(CHANNEL_SETUP2, note)

    def disconnect(self):
        pass