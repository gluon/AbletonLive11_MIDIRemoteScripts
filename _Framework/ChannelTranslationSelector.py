# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/ChannelTranslationSelector.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 2426 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .InputControlElement import InputControlElement
from .ModeSelectorComponent import ModeSelectorComponent

class ChannelTranslationSelector(ModeSelectorComponent):

    def __init__(self, num_modes=0, *a, **k):
        (super(ChannelTranslationSelector, self).__init__)(*a, **k)
        self._controls_to_translate = None
        self._initial_num_modes = num_modes

    def disconnect(self):
        ModeSelectorComponent.disconnect(self)
        self._controls_to_translate = None

    def set_controls_to_translate(self, controls):
        for control in controls:
            pass

        self._controls_to_translate = controls

    def number_of_modes(self):
        result = self._initial_num_modes
        if result == 0:
            if self._modes_buttons != None:
                result = len(self._modes_buttons)
        return result

    def update(self):
        super(ChannelTranslationSelector, self).update()
        if self._controls_to_translate != None:
            for control in self._controls_to_translate:
                control.use_default_message()
                if self.is_enabled():
                    control.set_channel((control.message_channel() + self._mode_index) % 16)