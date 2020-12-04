#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOMSQ/simple_device.py
from __future__ import absolute_import, print_function, unicode_literals
from future.moves.itertools import zip_longest
from _Generic.Devices import parameter_banks, parameter_bank_names
from ableton.v2.base import clamp, depends, EventObject, listens, liveobj_valid, nop, task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl, ToggleButtonControl
from .control import DisplayControl
BANK_NAME_DISPLAY_DURATION = 1

def release_control(control):
    if liveobj_valid(control):
        control.release_parameter()


class SimpleDeviceParameterComponent(Component):
    prev_bank_button = ButtonControl()
    next_bank_button = ButtonControl()
    device_lock_button = ToggleButtonControl()
    device_on_off_button = ToggleButtonControl()
    device_name_display = DisplayControl()

    @depends(device_provider=None)
    def __init__(self, device_provider = None, device_bank_registry = None, toggle_lock = None, *a, **k):
        super(SimpleDeviceParameterComponent, self).__init__(*a, **k)
        self._toggle_lock = toggle_lock
        self._device = None
        self._banks = []
        self._bank_index = 0
        self._parameter_controls = None
        self._empty_control_slots = self.register_disconnectable(EventObject())
        self._device_bank_registry = device_bank_registry
        self._device_provider = device_provider
        self._device_name_slot = self.register_slot(None, self._update_device_name_display, u'name')
        self.__on_provided_device_changed.subject = device_provider
        self.__on_provided_device_changed()
        self._display_bank_name_task = self._tasks.add(task.sequence(task.run(self._display_bank_name), task.wait(BANK_NAME_DISPLAY_DURATION), task.run(self._update_device_name_display)))
        self._display_bank_name_task.kill()
        if toggle_lock:
            self.__on_is_locked_to_device_changed.subject = self._device_provider
            self.__on_is_locked_to_device_changed()

    @device_lock_button.toggled
    def device_lock_button(self, *_):
        self._on_device_lock_button_toggled()

    @device_on_off_button.toggled
    def device_on_off_button(self, is_toggled, _):
        parameter = self._on_off_parameter()
        if parameter is not None:
            parameter.value = float(is_toggled)

    def _on_device_lock_button_toggled(self):
        self._toggle_lock()
        self._update_device_lock_button()

    @prev_bank_button.pressed
    def prev_bank_button(self, _):
        self.bank_index = self._bank_index - 1

    @next_bank_button.pressed
    def next_bank_button(self, _):
        self.bank_index = self._bank_index + 1

    @property
    def bank_index(self):
        return self._bank_index

    @bank_index.setter
    def bank_index(self, value):
        prev_bank_index = self._bank_index
        self._bank_index = self._clamp_to_bank_size(value)
        if prev_bank_index != self._bank_index:
            self._display_bank_name_task.restart()
        if self._device_bank_registry:
            self._device_bank_registry.set_device_bank(self._device, self._bank_index)
        self.update()

    def _clamp_to_bank_size(self, value):
        return clamp(value, 0, self.num_banks - 1)

    @property
    def selected_bank(self):
        if self.num_banks:
            return self._banks[self._bank_index or 0]
        return []

    @property
    def num_banks(self):
        return len(self._banks)

    def set_parameter_controls(self, controls):
        for control in self._parameter_controls or []:
            release_control(control)

        self._parameter_controls = controls
        self.update()

    @listens(u'device')
    def __on_provided_device_changed(self):
        for control in self._parameter_controls or []:
            release_control(control)

        self._device = self._device_provider.device
        self.__on_bank_changed.subject = self._device_bank_registry
        if self._device_bank_registry:
            self._bank_index = self._device_bank_registry.get_device_bank(self._device)
            self.update()
        else:
            self.bank_index = 0
        self._device_name_slot.subject = self._device
        self._update_device_name_display()

    @listens(u'device_bank')
    def __on_bank_changed(self, device, bank):
        if device == self._device:
            self.bank_index = bank

    @listens(u'is_locked_to_device')
    def __on_is_locked_to_device_changed(self):
        self._update_device_lock_button()

    @listens(u'value')
    def __on_device_on_off_changed(self):
        self._update_device_on_off_button()

    def update(self):
        super(SimpleDeviceParameterComponent, self).update()
        if self.is_enabled():
            self._update_parameter_banks()
            self._update_bank_navigation_buttons()
            self._empty_control_slots.disconnect()
            self.__on_device_on_off_changed.subject = self._on_off_parameter()
            self._update_device_on_off_button()
            if liveobj_valid(self._device):
                self._connect_parameters()
            else:
                self._disconnect_parameters()
        else:
            self._disconnect_parameters()

    def _disconnect_parameters(self):
        for control in self._parameter_controls or []:
            release_control(control)
            self._empty_control_slots.register_slot(control, nop, u'value')

    def _connect_parameters(self):
        for control, parameter in zip_longest(self._parameter_controls or [], self.selected_bank):
            if liveobj_valid(control):
                if liveobj_valid(parameter):
                    control.connect_to(parameter)
                else:
                    control.release_parameter()
                    self._empty_control_slots.register_slot(control, nop, u'value')

    def _on_off_parameter(self):
        if liveobj_valid(self._device):
            for p in self._device.parameters:
                if p.name.startswith(u'Device On') and liveobj_valid(p) and p.is_enabled:
                    return p

    def _update_parameter_banks(self):
        if liveobj_valid(self._device):
            self._banks = parameter_banks(self._device)
        else:
            self._banks = []
        self._bank_index = self._clamp_to_bank_size(self._bank_index)

    def _update_bank_navigation_buttons(self):
        self.prev_bank_button.enabled = self.bank_index > 0
        self.next_bank_button.enabled = self.bank_index < self.num_banks - 1

    def _update_device_lock_button(self):
        self.device_lock_button.is_toggled = self._device_provider.is_locked_to_device

    def _update_device_on_off_button(self):
        parameter = self._on_off_parameter()
        self.device_on_off_button.enabled = parameter is not None
        if parameter is not None:
            self.device_on_off_button.is_toggled = parameter.value > 0

    def _update_device_name_display(self):
        self.device_name_display.message = self._device.name if liveobj_valid(self._device) else u' - '

    def _display_bank_name(self):
        names = parameter_bank_names(self._device)
        if self.bank_index < len(names):
            self.device_name_display.message = names[self.bank_index]
