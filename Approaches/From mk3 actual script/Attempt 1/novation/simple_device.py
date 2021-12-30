#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/simple_device.py
from __future__ import absolute_import, print_function, unicode_literals
from future.moves.itertools import zip_longest
from _Generic.Devices import best_of_parameter_bank, parameter_banks
from ableton.v2.base import clamp, depends, EventObject, listens, liveobj_valid, nop
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ToggleButtonControl
from .fixed_radio_button_group import FixedRadioButtonGroup

def release_control(control):
    if liveobj_valid(control):
        control.release_parameter()


class SimpleDeviceParameterComponent(Component):
    bank_select_buttons = FixedRadioButtonGroup(control_count=8, unchecked_color=u'Mode.Device.Bank.Available', checked_color=u'Mode.Device.Bank.Selected')
    device_lock_button = ToggleButtonControl()

    @depends(device_provider=None)
    def __init__(self, device_provider = None, device_bank_registry = None, toggle_lock = None, use_parameter_banks = False, *a, **k):
        super(SimpleDeviceParameterComponent, self).__init__(*a, **k)
        self._toggle_lock = toggle_lock
        self._use_parameter_banks = use_parameter_banks
        self._device = None
        self._banks = []
        self._bank_index = 0
        self._parameter_controls = None
        self._empty_control_slots = self.register_disconnectable(EventObject())
        self._device_bank_registry = device_bank_registry
        self._device_provider = device_provider
        self.__on_provided_device_changed.subject = device_provider
        self.__on_provided_device_changed()
        if toggle_lock:
            self.__on_is_locked_to_device_changed.subject = self._device_provider
            self.__on_is_locked_to_device_changed()

    @bank_select_buttons.checked
    def bank_select_buttons(self, button):
        self._on_bank_select_button_checked(button)

    def _on_bank_select_button_checked(self, button):
        self.bank_index = button.index

    @bank_select_buttons.value
    def bank_select_buttons(self, value, _):
        if not value:
            self._on_bank_select_button_released()

    def _on_bank_select_button_released(self):
        pass

    @device_lock_button.toggled
    def device_lock_button(self, *_):
        self._on_device_lock_button_toggled()

    def _on_device_lock_button_toggled(self):
        self._toggle_lock()
        self._update_device_lock_button()

    @property
    def bank_index(self):
        if self._use_parameter_banks:
            return self._bank_index
        return 0

    @bank_index.setter
    def bank_index(self, value):
        self._bank_index = self._clamp_to_bank_size(value)
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

    @listens(u'device_bank')
    def __on_bank_changed(self, device, bank):
        if device == self._device:
            self.bank_index = bank

    @listens(u'is_locked_to_device')
    def __on_is_locked_to_device_changed(self):
        self._update_device_lock_button()

    def update(self):
        super(SimpleDeviceParameterComponent, self).update()
        if self.is_enabled():
            self._update_parameter_banks()
            self._update_bank_select_buttons()
            self._empty_control_slots.disconnect()
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

    def _update_parameter_banks(self):
        if liveobj_valid(self._device):
            if self._use_parameter_banks:
                self._banks = parameter_banks(self._device)
            else:
                self._banks = [best_of_parameter_bank(self._device)]
        else:
            self._banks = []
        self._bank_index = self._clamp_to_bank_size(self._bank_index)

    def _update_bank_select_buttons(self):
        self.bank_select_buttons.active_control_count = self.num_banks
        if self.bank_index < self.num_banks:
            self.bank_select_buttons[self.bank_index].is_checked = True

    def _update_device_lock_button(self):
        self.device_lock_button.is_toggled = self._device_provider.is_locked_to_device
