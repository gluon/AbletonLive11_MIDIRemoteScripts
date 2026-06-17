# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\banking_util.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 7044 bytes
from __future__ import absolute_import, print_function, unicode_literals
from math import ceil
from ableton.v2.control_surface import BankingInfo as BankingInfoBase
from ableton.v2.control_surface import DescribedDeviceParameterBank as DescribedDeviceParameterBankBase
from ableton.v2.control_surface.device_parameter_bank import DeviceParameterBank
from ableton.v2.control_surface.device_parameter_bank import MaxDeviceParameterBank as MaxDeviceParameterBankBase
from ..live import liveobj_valid
from . import BANK_FORMAT, BANK_PARAMETERS_KEY, all_parameters
BANK_NAME_JOIN_STR = ' and '
DEFAULT_BANK_SIZE = 8

def create_parameter_bank(device, banking_info):
    bank = None
    if liveobj_valid(device):
        bank_class = DeviceParameterBank
        size = banking_info.bank_size
        if size >= DEFAULT_BANK_SIZE:
            if banking_info.has_bank_count(device):
                bank_class = MaxDeviceParameterBank
            else:
                if banking_info.device_bank_definition(device) is not None:
                    bank_class = DescribedDeviceParameterBank
        bank = bank_class(device=device, size=size, banking_info=banking_info)
    return bank


class DescribedDeviceParameterBank(DescribedDeviceParameterBankBase):

    def _current_parameter_slots(self):
        next_index = self.index + 1
        bank_count = self._banking_info.device_bank_count(self._device)
        if self._size > DEFAULT_BANK_SIZE:
            if next_index < bank_count:
                result = (self._definition.value_by_index(self.index).get(BANK_PARAMETERS_KEY) or tuple()) + (self._definition.value_by_index(next_index).get(BANK_PARAMETERS_KEY) or tuple())
                return result
        return super()._current_parameter_slots()

    def _calc_name(self):
        if self._size > DEFAULT_BANK_SIZE:
            return self._banking_info.device_bank_names(self._device)[self.index]
        return super()._calc_name()


class MaxDeviceParameterBank(MaxDeviceParameterBankBase):

    def _collect_parameters(self):
        bank_count = self._banking_info.device_bank_count(self._device)
        if bank_count == 0:
            return [(None, None)] * self._size
        bank = self._get_parameters_for_bank_index(self.index)
        next_index = self.index + 1
        if self._size > DEFAULT_BANK_SIZE:
            if next_index < bank_count:
                bank.extend(self._get_parameters_for_bank_index(next_index))
        return bank

    def _get_parameters_for_bank_index(self, bank_index):
        parameters = self._device.parameters
        mx_index = bank_index - int(self._banking_info.has_main_bank(self._device))
        indices = self.device.get_bank_parameters(mx_index)
        parameters = [parameters[index] if index >= 0 else None for index in indices]
        return [(param, None) for param in parameters]

    def _calc_name(self):
        bank_count = self._banking_info.device_bank_count(self._device)
        if self._size > DEFAULT_BANK_SIZE:
            if self.index < bank_count:
                return self._banking_info.device_bank_names(self._device)[self.index]
        return super()._calc_name()


class BankingInfo(BankingInfoBase):

    def __init__(self, bank_definitions, bank_size=DEFAULT_BANK_SIZE, *a, **k):
        (super().__init__)(bank_definitions, *a, **k)
        self._bank_size = bank_size
        self._num_simultaneous_banks = 2 if bank_size > DEFAULT_BANK_SIZE else 1

    @property
    def bank_size(self):
        return self._bank_size

    @property
    def num_simultaneous_banks(self):
        return self._num_simultaneous_banks

    def device_bank_count(self, device, **k):
        if self._bank_size < DEFAULT_BANK_SIZE:
            return ceil(float(len(all_parameters(device))) / self._bank_size)
        return (super().device_bank_count)(device, **k)

    def device_bank_names(self, device, **k):
        if self._bank_size < DEFAULT_BANK_SIZE:
            return [BANK_FORMAT % (index + 1) for index in range(self.device_bank_count(device))]
        names = (super().device_bank_names)(device, **k)
        if self._num_simultaneous_banks == 2:
            if len(names) > 1:
                result = [BANK_NAME_JOIN_STR.join(n) for n in [(names[i], names[i + 1]) for i in range(len(names) - 1)]]
                result.append(names[-1])
                return result
        return names