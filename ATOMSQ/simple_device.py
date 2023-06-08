from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import liveobj_valid, task
from ableton.v3.control_surface.components import DeviceComponent
from ableton.v3.control_surface.legacy_bank_definitions import banked
from .control import DisplayControl
BANK_NAME_DISPLAY_DURATION = 1

class SimpleDeviceParameterComponent(DeviceComponent):
    device_name_display = DisplayControl()

    def __init__(self, *a, **k):
        self._device_name_slot = None
        self._display_bank_name_task = None
        (super().__init__)(a, bank_definitions=banked(), **k)
        self._device_name_slot = self.register_slot(self.device, self._update_device_name_display, 'name')
        self._display_bank_name_task = self._tasks.add(task.sequence(task.run(self._display_bank_name), task.wait(BANK_NAME_DISPLAY_DURATION), task.run(self._update_device_name_display)))
        self._display_bank_name_task.kill()

    def set_device_name_display(self, display):
        self.device_name_display.set_control_element(display)

    def _set_bank_index(self, bank):
        super()._set_bank_index(bank)
        if self._display_bank_name_task:
            self._display_bank_name_task.restart()

    def _set_device(self, device):
        super()._set_device(device)
        if self._device_name_slot:
            self._device_name_slot.subject = device
            self._display_bank_name_task.kill()
        self._update_device_name_display()

    def _update_device_name_display(self):
        device = self.device
        self.device_name_display.message = device.name if liveobj_valid(device) else ' - '

    def _display_bank_name(self):
        self.device_name_display.message = self._current_bank_details()[0] if liveobj_valid(self.device) else ''