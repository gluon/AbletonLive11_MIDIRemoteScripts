# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AxiomPro\SelectButtonModeSelector.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 4521 bytes
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
            else:
                if self._mode_index == 1:
                    mode_name = 'Arm'
                else:
                    if self._mode_index == 2:
                        mode_name = 'Mute'
                    else:
                        if self._mode_index == 3:
                            mode_name = 'Solo'
            self._mode_display.display_message(mode_name)
        else:
            self._mode_display.update()