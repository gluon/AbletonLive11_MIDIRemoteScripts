from __future__ import absolute_import, print_function, unicode_literals
from novation.blinking_button import BlinkingButtonControl
from novation.transport import TransportComponent as TransportComponentBase

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