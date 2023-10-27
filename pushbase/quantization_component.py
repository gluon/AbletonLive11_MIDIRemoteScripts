# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\quantization_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 7309 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import clamp, listenable_property, listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl, EncoderControl, StepEncoderControl, ToggleButtonControl
from .consts import SIDE_BUTTON_COLORS, MessageBoxText
from .message_box_component import Messenger
RecordingQuantization = Live.Song.RecordingQuantization
QUANTIZATION_OPTIONS = [
 RecordingQuantization.rec_q_quarter,
 RecordingQuantization.rec_q_eight,
 RecordingQuantization.rec_q_eight_triplet,
 RecordingQuantization.rec_q_eight_eight_triplet,
 RecordingQuantization.rec_q_sixtenth,
 RecordingQuantization.rec_q_sixtenth_triplet,
 RecordingQuantization.rec_q_sixtenth_sixtenth_triplet,
 RecordingQuantization.rec_q_thirtysecond]
DEFAULT_QUANTIZATION_INDEX = QUANTIZATION_OPTIONS.index(RecordingQuantization.rec_q_sixtenth)
QUANTIZATION_NAMES = ('1/4', '1/8', '1/8T', '1/8+T', '1/16', '1/16T', '1/16+T', '1/32')
QUANTIZATION_NAMES_UNICODE = ('¼', '⅛', '⅛T', '⅛+T', '\ue001', '\ue001T', '\ue001+T',
                              '\ue002')

def quantize_amount_to_string(amount):
    return '%i%%' % int(amount * 100.0)


class QuantizationSettingsComponent(Component):
    swing_amount_encoder = EncoderControl()
    quantize_to_encoder = StepEncoderControl()
    quantize_amount_encoder = EncoderControl()
    record_quantization_encoder = StepEncoderControl()
    record_quantization_toggle_button = ToggleButtonControl(toggled_color='Recording.FixedLengthRecordingOn',
      untoggled_color='Recording.FixedLengthRecordingOff')
    quantize_amount = listenable_property.managed(1.0)
    quantize_to_index = listenable_property.managed(DEFAULT_QUANTIZATION_INDEX)
    record_quantization_index = listenable_property.managed(DEFAULT_QUANTIZATION_INDEX)

    def __init__(self, quantization_names=QUANTIZATION_NAMES, *a, **k):
        (super(QuantizationSettingsComponent, self).__init__)(*a, **k)
        self._quantization_names = quantization_names
        self._QuantizationSettingsComponent__on_swing_amount_changed.subject = self.song
        self._QuantizationSettingsComponent__on_record_quantization_changed.subject = self.song
        self._QuantizationSettingsComponent__on_record_quantization_changed()

    @property
    def quantize_to(self):
        return QUANTIZATION_OPTIONS[self.quantize_to_index]

    @listenable_property
    def swing_amount(self):
        return self.song.swing_amount

    @listenable_property
    def record_quantization_enabled(self):
        return self.record_quantization_toggle_button.is_toggled

    @property
    def quantization_option_names(self):
        return self._quantization_names

    @property
    def selected_quantization_name(self):
        return self.quantization_option_names[self.quantize_to_index]

    @swing_amount_encoder.value
    def swing_amount_encoder(self, value, encoder):
        self.song.swing_amount = clamp(self.song.swing_amount + value * 0.5, 0.0, 0.5)

    @staticmethod
    def _clamp_quantization_index(index):
        return clamp(index, 0, len(QUANTIZATION_OPTIONS) - 1)

    @quantize_to_encoder.value
    def quantize_to_encoder(self, value, encoder):
        self.quantize_to_index = self._clamp_quantization_index(self.quantize_to_index + value)

    @quantize_amount_encoder.value
    def quantize_amount_encoder(self, value, encoder):
        self.quantize_amount = clamp(self.quantize_amount + value, 0.0, 1.0)

    @record_quantization_encoder.value
    def record_quantization_encoder(self, value, encoder):
        self.record_quantization_index = self._clamp_quantization_index(self.record_quantization_index + value)
        self._update_record_quantization()

    @record_quantization_toggle_button.toggled
    def record_quantization_toggle_button(self, value, button):
        self._update_record_quantization()

    @listens('swing_amount')
    def __on_swing_amount_changed(self):
        self.notify_swing_amount()

    @listens('midi_recording_quantization')
    def __on_record_quantization_changed(self):
        quant_value = self.song.midi_recording_quantization
        quant_on = quant_value != RecordingQuantization.rec_q_no_q
        if quant_value in QUANTIZATION_OPTIONS:
            self.record_quantization_index = QUANTIZATION_OPTIONS.index(quant_value)
        self.record_quantization_toggle_button.is_toggled = quant_on
        self.notify_record_quantization_enabled(quant_on)

    def _update_record_quantization(self):
        index = QUANTIZATION_OPTIONS[self.record_quantization_index]
        self.song.midi_recording_quantization = index if self.record_quantization_toggle_button.is_toggled else RecordingQuantization.rec_q_no_q


class QuantizationComponent(Component, Messenger):
    action_button = ButtonControl(**SIDE_BUTTON_COLORS)

    def __init__(self, settings_class=None, quantization_names=QUANTIZATION_NAMES, *a, **k):
        (super(QuantizationComponent, self).__init__)(*a, **k)
        self.settings = settings_class(name='Quantization_Settings',
          quantization_names=quantization_names,
          is_enabled=False,
          parent=self)
        self._cancel_quantize = False

    def quantize_pitch(self, note, source=None):
        clip = self.song.view.detail_clip
        if clip:
            clip.quantize_pitch(note, self.settings.quantize_to, self.settings.quantize_amount)
            self.show_notification(MessageBoxText.QUANTIZE_CLIP_PITCH % dict(source=source,
              amount=(quantize_amount_to_string(self.settings.quantize_amount)),
              to=(self.settings.selected_quantization_name)))
        self._cancel_quantize = True

    @action_button.pressed_delayed
    def action_button(self, button):
        self.settings.set_enabled(True)

    @action_button.released_delayed
    def hide_settings(self, button):
        self.settings.set_enabled(False)
        self._cancel_quantize = False

    @action_button.released_immediately
    def action_button(self, button):
        clip = self.song.view.detail_clip
        if clip:
            if not self._cancel_quantize:
                clip.quantize(self.settings.quantize_to, self.settings.quantize_amount)
                self.show_notification(MessageBoxText.QUANTIZE_CLIP % dict(amount=(quantize_amount_to_string(self.settings.quantize_amount)),
                  to=(self.settings.selected_quantization_name)))
        self._cancel_quantize = False