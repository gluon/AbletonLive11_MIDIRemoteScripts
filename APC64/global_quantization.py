# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\global_quantization.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 1533 bytes
from __future__ import absolute_import, print_function, unicode_literals
from Live.Song import Quantization
from ableton.v3.base import listens
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import FixedRadioButtonGroup
AVAILABLE_RATES = (
 Quantization.q_8_bars,
 Quantization.q_4_bars,
 Quantization.q_2_bars,
 Quantization.q_bar,
 Quantization.q_quarter,
 Quantization.q_eight,
 Quantization.q_sixtenth,
 Quantization.q_thirtytwoth)

class GlobalQuantizationComponent(Component):
    rate_buttons = FixedRadioButtonGroup(control_count=8,
      unchecked_color='GlobalQuantization.NotSelected',
      checked_color='GlobalQuantization.Selected')

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self._GlobalQuantizationComponent__on_global_quantization_changed.subject = self.song
        self._GlobalQuantizationComponent__on_global_quantization_changed()

    @rate_buttons.checked
    def rate_buttons(self, button):
        self.song.clip_trigger_quantization = AVAILABLE_RATES[button.index]

    @listens('clip_trigger_quantization')
    def __on_global_quantization_changed(self):
        rate = self.song.clip_trigger_quantization
        self.rate_buttons.checked_index = AVAILABLE_RATES.index(rate) if rate in AVAILABLE_RATES else -1