# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/device_bank_registry.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 1661 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ..base import EventObject

class DeviceBankRegistry(EventObject):
    __events__ = ('device_bank', )

    def __init__(self, *a, **k):
        (super(DeviceBankRegistry, self).__init__)(*a, **k)
        self._device_bank_registry = {}
        self._device_bank_listeners = []

    def compact_registry(self):
        newreg = dict(filter(lambda kv: kv[0] != None, self._device_bank_registry.items()))
        self._device_bank_registry = newreg

    def set_device_bank(self, device, bank):
        key = self._find_device_bank_key(device) or device
        old = self._device_bank_registry[key] if key in self._device_bank_registry else 0
        if old != bank:
            self._device_bank_registry[key] = bank
            self.notify_device_bank(device, bank)

    def get_device_bank(self, device):
        if hasattr(device, 'bank_index'):
            return device.bank_index
        return self._device_bank_registry.get(self._find_device_bank_key(device), 0)

    def _find_device_bank_key(self, device):
        for k in self._device_bank_registry:
            if k == device:
                return k