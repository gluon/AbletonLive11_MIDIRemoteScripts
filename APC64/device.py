# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\device.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 3855 bytes
from __future__ import absolute_import, print_function, unicode_literals
from typing import NamedTuple, Optional
from ableton.v3.base import listens
from ableton.v3.control_surface.components import DeviceBankNavigationComponent as DeviceBankNavigationComponentBase
from ableton.v3.control_surface.components import DeviceComponent as DeviceComponentBase
from ableton.v3.live import is_device_rack

class MacroMapping(NamedTuple):
    bank_0: list
    bank_1 = [None] * 8
    bank_1: Optional[list]


MACRO_MAPPINGS = {1:MacroMapping(bank_0=[0,None,None,None,None,None,None]), 
 2:MacroMapping(bank_0=[0,None,1,None,None,None,None,None]), 
 4:MacroMapping(bank_0=[0,1,2,3,None,None,None,None]), 
 6:MacroMapping(bank_0=[0,1,3,4,2,None,5,None]), 
 8:MacroMapping(bank_0=[0,1,4,5,2,3,6,7]), 
 10:MacroMapping(bank_0=[
  0,1,5,6,2,3,7,8],
   bank_1=[4,None,9,None,None,None,None,None]), 
 12:MacroMapping(bank_0=[
  0,1,6,7,2,3,8,9],
   bank_1=[4,5,10,11,None,None,None,None]), 
 14:MacroMapping(bank_0=[
  0,1,7,8,2,3,9,10],
   bank_1=[4,5,11,12,6,None,13,None]), 
 16:MacroMapping(bank_0=[
  0,1,8,9,2,3,10,11],
   bank_1=[4,5,12,13,6,7,14,15])}

class DeviceBankNavigationComponent(DeviceBankNavigationComponentBase):

    def can_scroll_up(self):
        if self._bank_provider is not None:
            if is_device_rack(self._bank_provider.device):
                return self._bank_provider.index == 0 and self._bank_provider.device.visible_macro_count > 8
        return super().can_scroll_up()


class DeviceComponent(DeviceComponentBase):

    def __init__(self, *a, **k):
        self._is_rack = False
        (super().__init__)(a, bank_navigation_component_type=DeviceBankNavigationComponent, **k)

    def _set_device(self, device):
        self._is_rack = is_device_rack(device)
        self._DeviceComponent__on_visible_macro_count_changed.subject = device if self._is_rack else None
        self._DeviceComponent__on_macros_mapped_changed.subject = device if self._is_rack else None
        super()._set_device(device)

    def _get_provided_parameters(self):
        if self._is_rack:
            macros = self.device.parameters[1:17]
            mappings = MACRO_MAPPINGS[self.device.visible_macro_count]
            return [self._create_parameter_info(macros[m] if (m is not None) and (self.device.macros_mapped[m]) else None, None) for m in getattr(mappings, 'bank_{}'.format(self._bank.index))]
        return super()._get_provided_parameters()

    @listens('visible_macro_count')
    def __on_visible_macro_count_changed(self):
        if self._bank.index:
            if self.device.visible_macro_count <= 8:
                self._set_bank_index(0)
        self._update_parameters()
        self._bank_navigation_component.update()

    @listens('macros_mapped')
    def __on_macros_mapped_changed(self):
        self._update_parameters()