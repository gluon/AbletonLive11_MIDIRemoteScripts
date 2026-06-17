# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_49_61_Classic\SliderSection.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 4698 bytes
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