# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\settings.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 4485 bytes
from __future__ import absolute_import, print_function, unicode_literals
from Live.Song import RecordingQuantization
from ableton.v3.base import CompoundDisconnectable
from ableton.v3.control_surface import Component, EnumWrappingParameter, NotifyingList
from ableton.v3.control_surface.controls import ButtonControl, MappedSensitivitySettingControl
from ableton.v3.live import get_bar_length, liveobj_valid
LENGTH_OPTIONS = {
  '1 Bar': 1,
  '2 Bars': 2,
  '4 Bars': 4,
  '8 Bars': 8,
  '16 Bars': 16,
  '32 Bars': 32}
QUANTIZATION_OPTIONS = {'1/4':RecordingQuantization.rec_q_quarter, 
 '1/8':RecordingQuantization.rec_q_eight, 
 '1/8T':RecordingQuantization.rec_q_eight_triplet, 
 '1/8 + T':RecordingQuantization.rec_q_eight_eight_triplet, 
 '1/16':RecordingQuantization.rec_q_sixtenth, 
 '1/16T':RecordingQuantization.rec_q_sixtenth_triplet, 
 '1/16 + T':RecordingQuantization.rec_q_sixtenth_sixtenth_triplet, 
 '1/32':RecordingQuantization.rec_q_thirtysecond}

def make_wrapping_parameter(parent, name, options, default_value):
    options = NotifyingList(available_values=(list(options.keys())),
      default_value=default_value)
    return parent.register_disconnectable(EnumWrappingParameter(name=name,
      parent=parent,
      values_host=options,
      index_property_host=options,
      values_property='available_values',
      index_property='index'))


class FixedLength(CompoundDisconnectable):

    def __init__(self, control, *a, **k):
        (super().__init__)(*a, **k)
        self._enabled = False
        self._length_setting = make_wrapping_parameter(self, 'Fixed Length', LENGTH_OPTIONS, 0)
        control.mapped_parameter = self._length_setting

    @property
    def enabled(self):
        return self._enabled

    @property
    def record_length(self):
        return LENGTH_OPTIONS[str(self._length_setting)] * get_bar_length()

    def toggle_enabled(self):
        self._enabled = not self._enabled


class Quantization(CompoundDisconnectable):

    def __init__(self, control, *a, **k):
        (super().__init__)(*a, **k)
        self._quantization_setting = make_wrapping_parameter(self, 'Quantization', QUANTIZATION_OPTIONS, 4)
        control.mapped_parameter = self._quantization_setting

    @property
    def quantization_setting(self):
        return QUANTIZATION_OPTIONS[str(self._quantization_setting)]

    def quantize_clip(self, clip):
        if liveobj_valid(clip):
            clip.quantize(self.quantization_setting, 1.0)


class SettingsComponent(Component):
    fixed_length_button = ButtonControl(color='Settings.FixedLengthOff',
      on_color='Settings.FixedLengthOn',
      pressed_color='Settings.FixedLengthOn')
    fixed_length_encoder = MappedSensitivitySettingControl(default_sensitivity=8.0)
    quantization_encoder = MappedSensitivitySettingControl(default_sensitivity=8.0)

    def __init__(self, *a, **k):
        (super().__init__)(a, name='Settings', **k)
        self._fixed_length = self.register_disconnectable(FixedLength(self.fixed_length_encoder))
        self._quantization = self.register_disconnectable(Quantization(self.quantization_encoder))

    @property
    def fixed_length(self):
        return self._fixed_length

    @property
    def quantization(self):
        return self._quantization

    @fixed_length_button.released_immediately
    def fixed_length_button(self, _):
        self._fixed_length.toggle_enabled()
        self.update()

    def update(self):
        super().update()
        self.fixed_length_button.is_on = self._fixed_length.enabled