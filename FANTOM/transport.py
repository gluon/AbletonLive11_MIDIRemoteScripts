# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/transport.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 2069 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import clamp, listens
import ableton.v3.control_surface.components as TransportComponentBase
from ableton.v3.control_surface.controls import EncoderControl
from .control import DisplayControl
MAX_NUM_BARS_WITH_BEATS = 9999

class TransportComponent(TransportComponentBase):
    tempo_coarse_control = EncoderControl()
    tempo_fine_control = EncoderControl()
    beat_time_display = DisplayControl()
    tempo_display = DisplayControl()

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self._TransportComponent__on_song_time_changed.subject = self.song
        self._TransportComponent__on_tempo_changed.subject = self.song

    def set_tempo_fine_control(self, control):
        self.tempo_fine_control.set_control_element(control)

    @tempo_coarse_control.value
    def tempo_coarse_control(self, value, _):
        factor = 1 if value > 0 else -1
        self.song.tempo = clamp(self.song.tempo + factor, 20, 999)

    @tempo_fine_control.value
    def tempo_fine_control(self, value, _):
        factor = 0.1 if value > 0 else -0.1
        self.song.tempo = clamp(self.song.tempo + factor, 20, 999)

    def update(self):
        super().update()
        self._TransportComponent__on_song_time_changed()
        self._TransportComponent__on_tempo_changed()

    @listens('current_song_time')
    def __on_song_time_changed(self):
        beat_time = self.song.get_current_beats_song_time()
        bars = beat_time.bars
        if bars <= MAX_NUM_BARS_WITH_BEATS:
            self.beat_time_display.data = '{}.{}'.format(bars, beat_time.beats)
        else:
            self.beat_time_display.data = str(bars)

    @listens('tempo')
    def __on_tempo_changed(self):
        tempo = '{:.2f}'.format(self.song.tempo)
        self.tempo_display.data = tempo