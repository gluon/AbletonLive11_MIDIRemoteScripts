# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK2\DeviceComponent.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3830 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
from _Generic.Devices import BANK_NAME_DICT, DEVICE_BOB_DICT, DEVICE_DICT, parameter_bank_names, parameter_banks
from _Framework.Control import ButtonControl
from _Framework.DeviceComponent import DeviceComponent as DeviceComponentBase
BOB_BANK_NAME = 'Best of Parameters'
NavDirection = Live.Application.Application.View.NavDirection

class DeviceComponent(DeviceComponentBase):
    device_nav_left_button = ButtonControl()
    device_nav_right_button = ButtonControl()

    def __init__(self, *a, **k):
        (super(DeviceComponent, self).__init__)(*a, **k)
        new_banks = {}
        new_bank_names = {}
        self._device_banks = DEVICE_DICT
        self._device_bank_names = BANK_NAME_DICT
        self._device_best_banks = DEVICE_BOB_DICT
        for device_name, current_banks in self._device_banks.items():
            if len(current_banks) > 1:
                current_banks = self._device_best_banks[device_name] + current_banks
                new_bank_names[device_name] = (BOB_BANK_NAME,) + self._device_bank_names[device_name]
            else:
                new_banks[device_name] = current_banks

        self._device_banks = new_banks
        self._device_bank_names = new_bank_names

    @device_nav_left_button.pressed
    def device_nav_left_button(self, value):
        self._scroll_device_chain(NavDirection.left)

    @device_nav_right_button.pressed
    def device_nav_right_button(self, value):
        self._scroll_device_chain(NavDirection.right)

    def _scroll_device_chain(self, direction):
        view = self.application().view
        if not (view.is_view_visible('Detail') and view.is_view_visible('Detail/DeviceChain')):
            view.show_view('Detail')
            view.show_view('Detail/DeviceChain')
        else:
            view.scroll_view(direction, 'Detail/DeviceChain', False)

    def _is_banking_enabled(self):
        return True

    def _number_of_parameter_banks(self):
        result = 0
        if self._device != None:
            if self._device.class_name in list(self._device_banks.keys()):
                result = len(self._device_banks[self._device.class_name])
            else:
                result = super(DeviceComponent, self)._number_of_parameter_banks()
        return result

    def _parameter_banks(self):
        return parameter_banks(self._device, self._device_banks)

    def _parameter_bank_names(self):
        return parameter_bank_names(self._device, self._device_bank_names)

    def _update_device_bank_buttons(self):
        if self.is_enabled():
            bank_length = len(self._parameter_banks())
            for index, button in enumerate(self._bank_buttons or []):
                if button:
                    value_to_send = False
                    if index == self._bank_index and self._device:
                        value_to_send = 'Device.BankSelected'
                    else:
                        if index == 0:
                            value_to_send = 'Device.BestOfBank'
                        else:
                            if index in range(bank_length):
                                value_to_send = 'Device.Bank'
                    button.set_light(value_to_send)