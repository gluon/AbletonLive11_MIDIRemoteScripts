# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Axiom\Transport.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 4438 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
import Live
from .consts import *

class Transport(object):

    def __init__(self, parent):
        self._Transport__parent = parent
        self._Transport__ffwd_held = False
        self._Transport__rwd_held = False
        self._Transport__delay_counter = 0

    def build_midi_map(self, script_handle, midi_map_handle):
        for cc_no in AXIOM_TRANSPORT:
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, 15, cc_no)

    def receive_midi_cc(self, cc_no, cc_value):
        if cc_no == AXIOM_STOP:
            if cc_value > 0:
                self._Transport__parent.song().is_playing = False
        else:
            if cc_no == AXIOM_PLAY:
                if cc_value > 0:
                    self._Transport__parent.song().is_playing = True
            else:
                if cc_no == AXIOM_REC:
                    if cc_value > 0:
                        self._Transport__parent.song().record_mode = not self._Transport__parent.song().record_mode
                else:
                    if self._Transport__parent.application().view.is_view_visible('Session'):
                        if cc_value > 0:
                            self._Transport__cc_in_session(cc_no)
                    else:
                        self._Transport__cc_in_arranger(cc_no, cc_value)

    def __cc_in_session(self, cc_no):
        index = list(self._Transport__parent.song().scenes).index(self._Transport__parent.song().view.selected_scene)
        if cc_no == AXIOM_LOOP:
            self._Transport__parent.song().view.selected_scene.fire_as_selected()
        else:
            if cc_no == AXIOM_RWD:
                if index > 0:
                    index = index - 1
                    self._Transport__parent.song().view.selected_scene = self._Transport__parent.song().scenes[index]
            else:
                if cc_no == AXIOM_FFWD:
                    if index < len(self._Transport__parent.song().scenes) - 1:
                        index = index + 1
                        self._Transport__parent.song().view.selected_scene = self._Transport__parent.song().scenes[index]

    def __cc_in_arranger(self, cc_no, cc_value):
        if cc_no == AXIOM_LOOP:
            if cc_value > 0:
                self._Transport__parent.song().loop = not self._Transport__parent.song().loop
        else:
            if cc_no == AXIOM_RWD:
                if not self._Transport__ffwd_held:
                    if cc_value > 0:
                        self._Transport__rwd_held = True
                        self._Transport__delay_counter = 0
                        self._Transport__parent.song().jump_by(-1 * self._Transport__parent.song().signature_denominator)
                    else:
                        self._Transport__rwd_held = False
            else:
                if cc_no == AXIOM_FFWD and not self._Transport__rwd_held:
                    if cc_value > 0:
                        self._Transport__ffwd_held = True
                        self._Transport__delay_counter = 0
                        self._Transport__parent.song().jump_by(self._Transport__parent.song().signature_denominator)
                else:
                    self._Transport__ffwd_held = False

    def refresh_state(self):
        if self._Transport__ffwd_held:
            self._Transport__delay_counter += 1
            if self._Transport__delay_counter % 5 == 0:
                self._Transport__parent.song().jump_by(self._Transport__parent.song().signature_denominator)
        if self._Transport__rwd_held:
            self._Transport__delay_counter += 1
            if self._Transport__delay_counter % 5 == 0:
                self._Transport__parent.song().jump_by(-1 * self._Transport__parent.song().signature_denominator)