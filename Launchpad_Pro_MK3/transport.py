# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Pro_MK3/transport.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 783 bytes
from __future__ import absolute_import, print_function, unicode_literals
from novation.blinking_button import BlinkingButtonControl
import novation.transport as TransportComponentBase

class TransportComponent(TransportComponentBase):
    capture_midi_button = BlinkingButtonControl(color='Transport.CaptureOff',
      blink_on_color='Transport.CaptureOn',
      blink_off_color='Transport.CaptureOff')

    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        try:
            if self.song.can_capture_midi:
                self.song.capture_midi()
                self.capture_midi_button.start_blinking()
        except RuntimeError:
            pass