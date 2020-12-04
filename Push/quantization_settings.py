#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/quantization_settings.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from ableton.v2.base import listens
from ableton.v2.control_surface.control import TextDisplayControl
from pushbase.quantization_component import QuantizationSettingsComponent as QuantizationSettingsComponentBase, QUANTIZATION_NAMES, quantize_amount_to_string

class QuantizationSettingsComponent(QuantizationSettingsComponentBase):
    display_line1 = TextDisplayControl(segments=(u'', u'', u'', u'', u'', u'', u'', u''))
    display_line2 = TextDisplayControl(segments=(u'Swing', u'Quantize', u'Quantize', u'', u'', u'', u'', u'Record'))
    display_line3 = TextDisplayControl(segments=(u'Amount', u'To', u'Amount', u'', u'', u'', u'', u'Quantize'))
    display_line4 = TextDisplayControl(segments=(u'', u'', u'', u'', u'', u'', u'', u''))

    def __init__(self, *a, **k):
        super(QuantizationSettingsComponent, self).__init__(*a, **k)
        self._update_swing_amount_display()
        self._update_quantize_to_display()
        self._update_quantize_amount_display()
        self._update_record_quantization_display()
        self.__on_swing_amount_changed.subject = self.song
        self.__on_record_quantization_index_changed.subject = self
        self.__on_record_quantization_enabled_changed.subject = self
        self.__on_quantize_to_index_changed.subject = self
        self.__on_quantize_amount_changed.subject = self

    def _update_swing_amount_display(self):
        self.display_line1[0] = str(int(self.song.swing_amount * 200.0)) + u'%'

    def _update_record_quantization_display(self):
        record_quantization_on = self.record_quantization_toggle_button.is_toggled
        self.display_line1[-1] = QUANTIZATION_NAMES[self.record_quantization_index]
        self.display_line4[-1] = u'[  On  ]' if record_quantization_on else u'[  Off ]'

    def _update_quantize_to_display(self):
        self.display_line1[1] = QUANTIZATION_NAMES[self.quantize_to_index]

    def _update_quantize_amount_display(self):
        self.display_line1[2] = quantize_amount_to_string(self.quantize_amount)

    @listens(u'quantize_to_index')
    def __on_quantize_to_index_changed(self, _):
        self._update_quantize_to_display()

    @listens(u'quantize_amount')
    def __on_quantize_amount_changed(self, _):
        self._update_quantize_amount_display()

    @listens(u'swing_amount')
    def __on_swing_amount_changed(self):
        self._update_swing_amount_display()

    @listens(u'record_quantization_index')
    def __on_record_quantization_index_changed(self, _):
        self._update_record_quantization_display()

    @listens(u'record_quantization_enabled')
    def __on_record_quantization_enabled_changed(self, _):
        self._update_record_quantization_display()
