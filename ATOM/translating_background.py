# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/translating_background.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 1458 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import BackgroundComponent

class TranslatingBackgroundComponent(BackgroundComponent):

    def __init__(self, translation_channel, *a, **k):
        (super(TranslatingBackgroundComponent, self).__init__)(*a, **k)
        self._translation_channel = translation_channel

    def _clear_control(self, name, control):
        prior_control = self._control_map.get(name, None)
        if prior_control:
            if prior_control.name == 'Encoders':
                for encoder in prior_control:
                    encoder.use_default_message()

            prior_control.reset()
        super(TranslatingBackgroundComponent, self)._clear_control(name, control)
        if control:
            control.set_channel(self._translation_channel)
            if control.name == 'Pads':
                for button in control:
                    if button:
                        button.set_light('DefaultButton.RgbOff')

    def update(self):
        super(BackgroundComponent, self).update()