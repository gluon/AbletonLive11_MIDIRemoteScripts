# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24) 
# [Clang 6.0 (clang-600.0.57)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/track_info_display.py
# Compiled at: 2021-08-05 15:33:19
# Size of source mod 2**32: 2964 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import depends
from .simple_display import SimpleDisplayElement, adjust_string, as_ascii
from .sysex import NAME_LENGTH, NAME_TERMINATOR
INFO_LENGTH = 3
DEFAULT_TRACK_STATUS_BYTE = 64
RETURN_TRACK_MASK = 32
PAN_MASK = 16
VOLUME_MASK = 8
SEND_A_MASK = 4
SEND_B_MASK = 2
SPLIT_PAN_MASK = 1

class TrackInfoDisplayElement(SimpleDisplayElement):

    @depends(song=None)
    def __init__(self, *a, **k):
        self.song = k.pop('song')
        (super(TrackInfoDisplayElement, self).__init__)(*a, **k)

    def display_data(self, track_list):
        num_sends = len(self.song.return_tracks)
        data_to_send = [len(track_list)]
        for track in track_list:
            data_to_send.append(self._calculate_track_status_byte(track, num_sends))
            data_to_send.append(int(track.color_index) if track.color_index else 0)
            data_to_send.extend(as_ascii(adjust_string(track.name, NAME_LENGTH).strip()))
            data_to_send.append(NAME_TERMINATOR)

        self._message_to_send = self._message_header + tuple(data_to_send) + self._message_tail
        self._request_send_message()

    def _calculate_track_status_byte(self, track, num_sends):
        track_status_byte = DEFAULT_TRACK_STATUS_BYTE
        if track in self.song.return_tracks:
            track_status_byte |= RETURN_TRACK_MASK
        if track.has_audio_output:
            track_status_byte |= PAN_MASK | VOLUME_MASK
            if num_sends:
                track_status_byte |= SEND_A_MASK
                if num_sends > 1:
                    track_status_byte |= SEND_B_MASK
            if track.mixer_device.panning_mode:
                track_status_byte |= SPLIT_PAN_MASK
        return track_status_byte