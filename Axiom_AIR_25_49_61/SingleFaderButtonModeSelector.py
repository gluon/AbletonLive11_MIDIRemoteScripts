<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Axiom_AIR_25_49_61/SingleFaderButtonModeSelector.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 2505 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
import _Framework.ModeSelectorComponent as ModeSelectorComponent
from .consts import *

class SingleFaderButtonModeSelector(ModeSelectorComponent):

    def __init__(self, mixer, fader_button):
        ModeSelectorComponent.__init__(self)
        self._mixer = mixer
        self._fader_button = fader_button
        self._mode_index = 0
        self._number_of_modes = 3
        self._flashing_button = None
        self._flashing_button_on = True
        self._flashing_reset_delay = 0
        self._register_timer_callback(self._on_timer)

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        ModeSelectorComponent.disconnect(self)
        self._mixer = None
        self._fader_button = None
        self._flashing_button = None

    def number_of_modes(self):
        return self._number_of_modes

    def update(self):
        super(SingleFaderButtonModeSelector, self).update()
        if self.is_enabled():
            strip = self._mixer.selected_strip()
            fader_button = self._fader_button
            self._flashing_button = None
            if self.song().view.selected_track != self.song().master_track:
                strip.set_solo_button(None)
                strip.set_arm_button(None)
                strip.set_mute_button(None)
                if self._mode_index == 0:
                    strip.set_mute_button(fader_button)
                    self._mode_toggle.send_value(AMB_FULL, True)
<<<<<<< HEAD
                else:
                    if self._mode_index == 1:
                        strip.set_solo_button(fader_button)
                        self._mode_toggle.send_value(AMB_FULL, True)
                        self._flashing_button = self._mode_toggle
                    else:
                        strip.set_arm_button(fader_button)
                        self._mode_toggle.send_value(RED_FULL, True)
=======
                elif self._mode_index == 1:
                    strip.set_solo_button(fader_button)
                    self._mode_toggle.send_value(AMB_FULL, True)
                    self._flashing_button = self._mode_toggle
                else:
                    strip.set_arm_button(fader_button)
                    self._mode_toggle.send_value(RED_FULL, True)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def _on_timer(self):
        if self._flashing_button != None:
            if self._flashing_reset_delay > 0:
                self._flashing_reset_delay -= 1
            else:
                self._flash()
                self._flashing_reset_delay = 5

    def _flash(self):
        self._flashing_button.turn_off() if self._flashing_button_on else self._flashing_button.turn_on()
        self._flashing_button_on = not self._flashing_button_on