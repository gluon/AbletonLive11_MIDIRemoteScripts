<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Axiom_49_61_Classic/SliderSection.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 4574 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, range
import Live
from _Axiom.consts import *

class SliderSection(object):

    def __init__(self, parent):
        self._SliderSection__parent = parent
        self._SliderSection__mod_pressed = False

    def build_midi_map(self, script_handle, midi_map_handle):
        feedback_rule = Live.MidiMap.CCFeedbackRule()
        needs_takeover = True
        feedback_rule.channel = 0
        feedback_rule.cc_no = AXIOM_SLI9
        feedback_rule.cc_value_map = tuple()
        feedback_rule.delay_in_ms = -1.0
        for channel in range(16):
            Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, self._SliderSection__parent.song().master_track.mixer_device.volume, channel, AXIOM_SLI9, Live.MidiMap.MapMode.absolute, feedback_rule, not needs_takeover)

        for channel in range(4):
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, channel, AXIOM_BUT9)
            for slider in range(8):
                tracks = self._SliderSection__parent.song().visible_tracks
                track_index = slider + channel * 8
                if len(tracks) > track_index:
                    feedback_rule.channel = 0
                    feedback_rule.cc_no = AXIOM_SLIDERS[slider]
                    feedback_rule.cc_value_map = tuple()
                    feedback_rule.delay_in_ms = -1.0
                    Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, tracks[track_index].mixer_device.volume, channel, AXIOM_SLIDERS[slider], Live.MidiMap.MapMode.absolute, feedback_rule, not needs_takeover)
                    Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, channel, AXIOM_BUTTONS[slider])
                else:
                    break

    def receive_midi_cc(self, cc_no, cc_value, channel):
        if list(AXIOM_BUTTONS).count(cc_no) > 0:
            button_index = list(AXIOM_BUTTONS).index(cc_no)
            if cc_no == AXIOM_BUT9:
                self._SliderSection__mod_pressed = cc_value == 127
<<<<<<< HEAD
            else:
                if button_index in range(8):
                    tracks = self._SliderSection__parent.song().visible_tracks
                    track_index = button_index + 8 * channel
                    if len(tracks) > track_index:
                        track = tracks[track_index]
                        if track:
                            if track.can_be_armed:
                                if not self._SliderSection__mod_pressed:
                                    track.mute = not track.mute
                                else:
                                    track.arm = not track.arm
                                    if self._SliderSection__parent.song().exclusive_arm:
                                        for t in tracks:
                                            if t.can_be_armed:
                                                if t.arm:
                                                    if not t == track:
                                                        t.arm = False

                                    if track.arm:
                                        if track.view.select_instrument():
                                            self._SliderSection__parent.song().view.selected_track = track
=======
            elif button_index in range(8):
                tracks = self._SliderSection__parent.song().visible_tracks
                track_index = button_index + 8 * channel
                if len(tracks) > track_index:
                    track = tracks[track_index]
                    if track:
                        if track.can_be_armed:
                            if not self._SliderSection__mod_pressed:
                                track.mute = not track.mute
                            else:
                                track.arm = not track.arm
                                if self._SliderSection__parent.song().exclusive_arm:
                                    for t in tracks:
                                        if t.can_be_armed:
                                            if t.arm:
                                                if not t == track:
                                                    t.arm = False

                                if track.arm:
                                    if track.view.select_instrument():
                                        self._SliderSection__parent.song().view.selected_track = track
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
