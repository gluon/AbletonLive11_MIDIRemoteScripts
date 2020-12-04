#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchkey_MK3/rgb_button.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import ButtonElement

class RgbButtonElement(ButtonElement):
    u"""
    RGBButtonElement extends ButtonElement for use with buttons on a controller that
    have RGB LEDs that receive MIDI on a different channel than the channel used to
    send MIDI.
    
    Note that the Color class provides a means of doing the same thing we're doing here.
    However, that approach is impractical when RGB LEDs are used to reflect the color
    of objects in Live since it would involve nearly 200 Color objects and corresponding
    dicts for handling look up.
    """

    def __init__(self, *a, **k):
        self._led_channel = k.pop(u'led_channel', 0)
        super(RgbButtonElement, self).__init__(*a, **k)

    def _do_send_value(self, value, channel = None):
        super(RgbButtonElement, self)._do_send_value(value, channel=self._led_channel)
