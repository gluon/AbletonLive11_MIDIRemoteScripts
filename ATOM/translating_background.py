#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/translating_background.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import BackgroundComponent

class TranslatingBackgroundComponent(BackgroundComponent):

    def __init__(self, translation_channel, *a, **k):
        super(TranslatingBackgroundComponent, self).__init__(*a, **k)
        self._translation_channel = translation_channel

    def _clear_control(self, name, control):
        prior_control = self._control_map.get(name, None)
        if prior_control:
            if prior_control.name == u'Encoders':
                for encoder in prior_control:
                    encoder.use_default_message()

            prior_control.reset()
        super(TranslatingBackgroundComponent, self)._clear_control(name, control)
        if control:
            control.set_channel(self._translation_channel)
            if control.name == u'Pads':
                for button in control:
                    if button:
                        button.set_light(u'DefaultButton.RgbOff')

    def update(self):
        super(BackgroundComponent, self).update()
