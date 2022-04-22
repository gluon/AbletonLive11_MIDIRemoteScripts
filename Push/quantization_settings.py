# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/quantization_settings.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 2949 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from ableton.v2.base import listens
from ableton.v2.control_surface.control import TextDisplayControl
from pushbase.quantization_component import QUANTIZATION_NAMES
import pushbase.quantization_component as QuantizationSettingsComponentBase
from pushbase.quantization_component import quantize_amount_to_string

class QuantizationSettingsComponent(QuantizationSettingsComponentBase):
    display_line1 = TextDisplayControl(segments=('', '', '', '', '', '', '', ''))
    display_line2 = TextDisplayControl(segments=('Swing', 'Quantize', 'Quantize', '',
                                                 '', '', '', 'Record'))
    display_line3 = TextDisplayControl(segments=('Amount', 'To', 'Amount', '', '',
                                                 '', '', 'Quantize'))
    display_line4 = TextDisplayControl(segments=('', '', '', '', '', '', '', ''))

    def __init__(self, *a, **k):
        (super(QuantizationSettingsComponent, self).__init__)(*a, **k)
        self._update_swing_amount_display()
        self._update_quantize_to_display()
        self._update_quantize_amount_display()
        self._update_record_quantization_display()
        self._QuantizationSettingsComponent__on_swing_amount_changed.subject = self.song
        self._QuantizationSettingsComponent__on_record_quantization_index_changed.subject = self
        self._QuantizationSettingsComponent__on_record_quantization_enabled_changed.subject = self
        self._QuantizationSettingsComponent__on_quantize_to_index_changed.subject = self
        self._QuantizationSettingsComponent__on_quantize_amount_changed.subject = self

    def _update_swing_amount_display(self):
        self.display_line1[0] = str(int(self.song.swing_amount * 200.0)) + '%'

    def _update_record_quantization_display(self):
        record_quantization_on = self.record_quantization_toggle_button.is_toggled
        self.display_line1[-1] = QUANTIZATION_NAMES[self.record_quantization_index]
        self.display_line4[-1] = '[  On  ]' if record_quantization_on else '[  Off ]'

    def _update_quantize_to_display(self):
        self.display_line1[1] = QUANTIZATION_NAMES[self.quantize_to_index]

    def _update_quantize_amount_display(self):
        self.display_line1[2] = quantize_amount_to_string(self.quantize_amount)

    @listens('quantize_to_index')
    def __on_quantize_to_index_changed(self, _):
        self._update_quantize_to_display()

    @listens('quantize_amount')
    def __on_quantize_amount_changed(self, _):
        self._update_quantize_amount_display()

    @listens('swing_amount')
    def __on_swing_amount_changed(self):
        self._update_swing_amount_display()

    @listens('record_quantization_index')
    def __on_record_quantization_index_changed(self, _):
        self._update_record_quantization_display()

    @listens('record_quantization_enabled')
    def __on_record_quantization_enabled_changed(self, _):
        self._update_record_quantization_display()