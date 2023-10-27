# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_Mini32\MixerOrDeviceModeSelector.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 3671 bytes
from __future__ import absolute_import, print_function, unicode_literals
import _Framework.ModeSelectorComponent as ModeSelectorComponent

class MixerOrDeviceModeSelector(ModeSelectorComponent):

    def __init__(self, encoders, select_button, up_button, down_button, left_button, right_button, mixer, session, device, mixer_modes, device_nav):
        ModeSelectorComponent.__init__(self)
        self._encoders = encoders
        self._select_button = select_button
        self._up_button = up_button
        self._down_button = down_button
        self._left_button = left_button
        self._right_button = right_button
        self._mixer = mixer
        self._session = session
        self._device = device
        self._mixer_modes = mixer_modes
        self._device_nav = device_nav

    def disconnect(self):
        self._encoders = None
        self._select_button = None
        self._up_button = None
        self._down_button = None
        self._left_button = None
        self._right_button = None
        self._mixer = None
        self._session = None
        self._device = None
        self._mixer_modes = None
        self._device_nav = None
        ModeSelectorComponent.disconnect(self)

    def number_of_modes(self):
        return 3

    def update(self):
        super(MixerOrDeviceModeSelector, self).update()
        if self.is_enabled():
            if self._mode_index == 0:
                self._device.set_parameter_controls(None)
                self._mixer_modes.set_controls(self._encoders)
                self._device.set_bank_nav_buttons(None, None)
                self._device_nav.set_device_nav_buttons(None, None)
                self._mixer.set_select_buttons(self._down_button, self._up_button)
                self._session.set_page_left_button(self._left_button)
                self._session.set_page_right_button(self._right_button)
                self._device.set_on_off_button(None)
                self._mixer.selected_strip().set_arm_button(self._select_button)
            else:
                if self._mode_index == 1:
                    self._mixer_modes.set_controls(None)
                    self._device.set_parameter_controls(self._encoders)
                    self._mixer.set_select_buttons(None, None)
                    self._session.set_page_left_button(None)
                    self._session.set_page_right_button(None)
                    self._device.set_bank_nav_buttons(self._left_button, self._right_button)
                    self._device_nav.set_device_nav_buttons(self._up_button, self._down_button)
                    self._mixer.selected_strip().set_arm_button(None)
                    self._device.set_on_off_button(self._select_button)
                else:
                    if self._mode_index == 2:
                        self._mixer_modes.set_controls(None)
                        self._device.set_parameter_controls(None)
                        self._device.set_bank_nav_buttons(None, None)
                        self._device_nav.set_device_nav_buttons(None, None)
                        self._mixer.set_select_buttons(None, None)
                        self._session.set_page_left_button(None)
                        self._session.set_page_right_button(None)
                        self._device.set_on_off_button(None)
                        self._mixer.selected_strip().set_arm_button(None)