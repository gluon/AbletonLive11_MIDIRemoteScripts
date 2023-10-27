# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\fixed_length_recording.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1313 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
NUM_LENGTHS = 8

def track_can_record(track):
    return track.can_be_armed and (track.arm or track.implicit_arm)


class FixedLengthRecording(object):

    def __init__(self, song=None, fixed_length_setting=None, *a, **k):
        (super(FixedLengthRecording, self).__init__)(*a, **k)
        self._song = song
        self._fixed_length_setting = fixed_length_setting

    def should_start_recording_in_slot(self, clip_slot):
        return track_can_record(clip_slot.canonical_parent) and not clip_slot.is_recording and not clip_slot.has_clip and self._fixed_length_setting.enabled

    def start_recording_in_slot(self, clip_slot):
        if self.should_start_recording_in_slot(clip_slot):
            clip_slot.fire(record_length=(self._fixed_length_setting.get_selected_length(self._song)))
        else:
            clip_slot.fire()