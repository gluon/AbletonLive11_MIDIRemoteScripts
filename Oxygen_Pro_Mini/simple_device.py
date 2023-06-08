from __future__ import absolute_import, print_function, unicode_literals
from novation.simple_device import SimpleDeviceParameterComponent as SimpleDeviceParameterComponentBase
NUM_CONTROLS = 4

class SimpleDeviceParameterComponent(SimpleDeviceParameterComponentBase):

    def __init__(self, *a, **k):
        (super(SimpleDeviceParameterComponent, self).__init__)(*a, **k)
        self._parameter_offset = 0

    def toggle_parameter_offset(self):
        self._parameter_offset = NUM_CONTROLS - self._parameter_offset
        self.update()

    @SimpleDeviceParameterComponentBase.selected_bank.getter
    def selected_bank(self):
        bank = self._banks[0] or []
        if self._parameter_offset:
            if len(bank) > self._parameter_offset:
                offset_bank = bank[self._parameter_offset:]
                if any(offset_bank):
                    return offset_bank
        return bank