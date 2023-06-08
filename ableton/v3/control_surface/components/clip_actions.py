from __future__ import absolute_import, print_function, unicode_literals
from Live.Song import RecordingQuantization
from ...base import delete_clip, depends, duplicate_clip_loop, listens, liveobj_valid
from .. import Component
from ..controls import ButtonControl

class ClipActionsComponent(Component):
    delete_button = ButtonControl(color='ClipActions.Delete',
      pressed_color='ClipActions.DeletePressed')
    double_button = ButtonControl(color='ClipActions.Double',
      pressed_color='ClipActions.DoublePressed')
    quantize_button = ButtonControl(color='ClipActions.Quantize',
      pressed_color='ClipActions.QuantizePressed')

    @depends(target_track=None)
    def __init__(self, target_track=None, *a, **k):
        (super().__init__)(a, name='Clip_Actions', **k)
        self._target_track = target_track
        self._ClipActionsComponent__on_target_clip_changed.subject = target_track
        self._ClipActionsComponent__on_target_clip_recording_changed.subject = target_track
        self._ClipActionsComponent__on_target_clip_playing_status_changed.subject = target_track
        self._update_action_buttons()
        self._quantization_value = RecordingQuantization.rec_q_sixtenth
        self._ClipActionsComponent__on_record_quantization_changed.subject = self.song
        self._ClipActionsComponent__on_record_quantization_changed()

    @delete_button.pressed
    def delete_button(self, _):
        delete_clip(self._target_track.target_clip)

    @double_button.pressed
    def double_button(self, _):
        duplicate_clip_loop(self._target_track.target_clip)

    @quantize_button.pressed
    def quantize_button(self, _):
        self._target_track.target_clip.quantize(self._quantization_value, 1.0)

    def _update_action_buttons(self):
        self._update_delete_button()
        self._update_double_button()
        self._update_quantize_button()

    def _update_delete_button(self):
        self.delete_button.enabled = self._get_target_clip() is not None

    def _update_double_button(self):
        clip = self._get_target_clip()
        self.double_button.enabled = clip is not None and clip.is_midi_clip

    def _update_quantize_button(self):
        self.quantize_button.enabled = self._get_target_clip() is not None

    def _get_target_clip(self):
        clip = self._target_track.target_clip
        if liveobj_valid(clip):
            if not clip.is_recording:
                if not clip.will_record_on_start:
                    return clip

    @listens('target_clip')
    def __on_target_clip_changed(self):
        self._update_action_buttons()

    @listens('target_clip.is_recording')
    def __on_target_clip_recording_changed(self):
        self._update_action_buttons()

    @listens('target_clip.playing_status')
    def __on_target_clip_playing_status_changed(self):
        self._update_action_buttons()

    @listens('midi_recording_quantization')
    def __on_record_quantization_changed(self):
        quantization_value = self.song.midi_recording_quantization
        if quantization_value != RecordingQuantization.rec_q_no_q:
            self._quantization_value = quantization_value