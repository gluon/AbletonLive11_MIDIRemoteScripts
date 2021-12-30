#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/DeviceBankRegistry.py
u"""
Classes to keep a global registry of the currently selected bank for
given device instances.

[jbo] After some though about this, I personally believe that moving
banking to the C++ code is the best mid-term solution.
"""
from __future__ import absolute_import, print_function, unicode_literals
from .SubjectSlot import Subject

class DeviceBankRegistry(Subject):
    __subject_events__ = (u'device_bank',)

    def __init__(self, *a, **k):
        super(DeviceBankRegistry, self).__init__(*a, **k)
        self._device_bank_registry = {}
        self._device_bank_listeners = []

    def compact_registry(self):
        newreg = dict([ k__ for k__ in list(self._device_bank_registry.items()) if k__[0] != None ])
        self._device_bank_registry = newreg

    def set_device_bank(self, device, bank):
        key = self._find_device_bank_key(device) or device
        old = self._device_bank_registry[key] if key in self._device_bank_registry else 0
        if old != bank:
            self._device_bank_registry[key] = bank
            self.notify_device_bank(device, bank)

    def get_device_bank(self, device):
        return self._device_bank_registry.get(self._find_device_bank_key(device), 0)

    def _find_device_bank_key(self, device):
        for k in self._device_bank_registry.keys():
            if k == device:
                return k
