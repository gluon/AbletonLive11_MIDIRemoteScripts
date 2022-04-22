# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/MPD232/MPD232.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 1798 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import _Framework.ButtonMatrixElement as ButtonMatrixElement
from _MPDMkIIBase.ControlElementUtils import make_button, make_encoder, make_slider
import _MPDMkIIBase.MPDMkIIBase as MPDMkIIBase
PAD_CHANNEL = 1
PAD_IDS = [
 [
  81, 83, 84, 86], [74, 76, 77, 79], [67, 69, 71, 72], [60, 62, 64, 65]]

class MPD232(MPDMkIIBase):

    def __init__(self, *a, **k):
        (super(MPD232, self).__init__)(PAD_IDS, PAD_CHANNEL, *a, **k)
        with self.component_guard():
            self._create_device()
            self._create_transport()
            self._create_mixer()

    def _create_controls(self):
        self._create_pads()
        self._encoders = ButtonMatrixElement(rows=[
         [make_encoder(identifier, 0, 'Encoder_%d' % index) for index, identifier in enumerate(range(22, 30))]])
        self._sliders = ButtonMatrixElement(rows=[
         [make_slider(identifier, 0, 'Slider_%d' % index) for index, identifier in enumerate(range(12, 20))]])
        self._control_buttons = ButtonMatrixElement(rows=[
         [make_button(identifier, 0, 'Control_Button_%d' % index) for index, identifier in enumerate(range(32, 40))]])
        self._play_button = make_button(118, 0, 'Play_Button')
        self._stop_button = make_button(117, 0, 'Stop_Button')
        self._record_button = make_button(119, 0, 'Record_Button')