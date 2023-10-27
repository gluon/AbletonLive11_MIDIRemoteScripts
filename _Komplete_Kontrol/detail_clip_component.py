# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\detail_clip_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1944 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface.component import Component
from ableton.v2.control_surface.control import ButtonControl
RecordingQuantization = Live.Song.RecordingQuantization

class DetailClipComponent(Component):
    quantize_notes_button = ButtonControl()
    delete_notes_button = ButtonControl()

    def __init__(self, *a, **k):
        (super(DetailClipComponent, self).__init__)(*a, **k)
        self._record_quantization = RecordingQuantization.rec_q_sixtenth
        self._DetailClipComponent__on_record_quantization_changed.subject = self.song
        self._DetailClipComponent__on_record_quantization_changed()
        self._DetailClipComponent__on_detail_clip_changed.subject = self.song.view
        self._DetailClipComponent__on_detail_clip_changed()

    @listens('detail_clip')
    def __on_detail_clip_changed(self):
        clip = self.song.view.detail_clip
        if liveobj_valid(clip) and clip.is_midi_clip:
            self.quantize_notes_button.enabled = True
            self.delete_notes_button.enabled = True
        else:
            self.quantize_notes_button.enabled = False
            self.delete_notes_button.enabled = False

    @listens('midi_recording_quantization')
    def __on_record_quantization_changed(self):
        if self.song.midi_recording_quantization:
            self._record_quantization = self.song.midi_recording_quantization

    @quantize_notes_button.pressed
    def quantize_notes_button(self, _):
        self.song.view.detail_clip.quantize(self._record_quantization, 1.0)

    @delete_notes_button.pressed
    def delete_notes_button(self, _):
        clip = self.song.view.detail_clip
        clip.remove_notes_extended(from_time=0,
          from_pitch=0,
          time_span=(clip.loop_end),
          pitch_span=128)