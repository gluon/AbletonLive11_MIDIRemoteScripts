# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_25_49_61\MainModeSelector.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 3207 bytes
from __future__ import absolute_import, print_function, unicode_literals
import _Framework.ModeSelectorComponent as ModeSelectorComponent
from .consts import *

class MainModeSelector(ModeSelectorComponent):

    def __init__(self, device_0, device_1, session, mixer, device_nav, up_button, down_button, left_button, right_button, select_button):
        ModeSelectorComponent.__init__(self)
        self._device_0 = device_0
        self._device_1 = device_1
        self._session = session
        self._mixer = mixer
        self._device_nav = device_nav
        self._select_button = select_button
        self._left_button = left_button
        self._right_button = right_button
        self._up_button = up_button
        self._down_button = down_button
        self._mode_index = 0

    def disconnect(self):
        ModeSelectorComponent.disconnect(self)
        self._device_0 = None
        self._device_1 = None
        self._session = None
        self._mixer = None
        self._device_nav = None
        self._select_button = None
        self._left_button = None
        self._right_button = None
        self._up_button = None
        self._down_button = None

    def number_of_modes(self):
        return 2

    def update(self):
        super(MainModeSelector, self).update()
        if self.is_enabled():
            if self._mode_index == 0:
                self._modes_buttons[0].send_value(GRN_FULL, True)
                self._modes_buttons[1].send_value(LED_OFF, True)
                self._device_0.set_on_off_button(None)
                self._device_0.set_bank_nav_buttons(None, None)
                self._device_1.set_bank_nav_buttons(None, None)
                self._device_nav.set_device_nav_buttons(None, None)
                self._session.set_page_left_button(self._left_button)
                self._session.set_page_right_button(self._right_button)
                self._session.set_track_select_buttons(self._down_button, self._up_button)
                self._mixer.selected_strip().set_arm_button(self._select_button)
            else:
                if self._mode_index == 1:
                    self._modes_buttons[0].send_value(LED_OFF, True)
                    self._modes_buttons[1].send_value(GRN_FULL, True)
                    self._session.set_page_left_button(None)
                    self._session.set_page_right_button(None)
                    self._session.set_track_select_buttons(None, None)
                    self._mixer.selected_strip().set_arm_button(None)
                    self._device_0.set_on_off_button(self._select_button)
                    self._device_0.set_bank_nav_buttons(self._left_button, self._right_button)
                    self._device_1.set_bank_nav_buttons(self._left_button, self._right_button)
                    self._device_nav.set_device_nav_buttons(self._up_button, self._down_button)