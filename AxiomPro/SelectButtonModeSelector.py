# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/AxiomPro/SelectButtonModeSelector.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 4402 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import _Framework.ButtonElement as ButtonElement
import _Framework.MixerComponent as MixerComponent
import _Framework.ModeSelectorComponent as ModeSelectorComponent
import _Framework.PhysicalDisplayElement as PhysicalDisplayElement

class SelectButtonModeSelector(ModeSelectorComponent):

    def __init__(self, mixer, buttons):
        ModeSelectorComponent.__init__(self)
        self._mixer = mixer
        self._buttons = buttons
        self._mode_display = None
        self._mode_index = 0
        self.update()

    def disconnect(self):
        self._mixer = None
        self._buttons = None
        self._mode_display = None

    def set_mode_display(self, display):
        self._mode_display = display

    def number_of_modes(self):
        return 4

    def update(self):
        super(SelectButtonModeSelector, self).update()
        if self.is_enabled():
            for index in range(len(self._buttons)):
                if self._mode_index == 0:
                    self._mixer.channel_strip(index).set_select_button(self._buttons[index])
                    self._mixer.channel_strip(index).set_arm_button(None)
                    self._mixer.channel_strip(index).set_mute_button(None)
                    self._mixer.channel_strip(index).set_solo_button(None)
                else:
                    if self._mode_index == 1:
                        self._mixer.channel_strip(index).set_select_button(None)
                        self._mixer.channel_strip(index).set_arm_button(self._buttons[index])
                        self._mixer.channel_strip(index).set_mute_button(None)
                        self._mixer.channel_strip(index).set_solo_button(None)
                    else:
                        if self._mode_index == 2:
                            self._mixer.channel_strip(index).set_select_button(None)
                            self._mixer.channel_strip(index).set_arm_button(None)
                            self._mixer.channel_strip(index).set_mute_button(self._buttons[index])
                            self._mixer.channel_strip(index).set_solo_button(None)
                        else:
                            if self._mode_index == 3:
                                self._mixer.channel_strip(index).set_select_button(None)
                                self._mixer.channel_strip(index).set_arm_button(None)
                                self._mixer.channel_strip(index).set_mute_button(None)
                                self._mixer.channel_strip(index).set_solo_button(self._buttons[index])
                            else:
                                print('Invalid mode index')

    def _toggle_value(self, value):
        ModeSelectorComponent._toggle_value(self, value)
        if value != 0 and self._mode_display is not None:
            mode_name = ''
            if self._mode_index == 0:
                mode_name = 'Select'
            elif self._mode_index == 1:
                mode_name = 'Arm'
            elif self._mode_index == 2:
                mode_name = 'Mute'
            elif self._mode_index == 3:
                mode_name = 'Solo'
            self._mode_display.display_message(mode_name)
        else:
            self._mode_display.update()