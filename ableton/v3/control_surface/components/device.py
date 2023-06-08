# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/device.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 8009 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import zip_longest
from _Generic.Devices import best_of_parameter_bank, parameter_bank_names, parameter_banks
from ...base import clamp, depends, listens, liveobj_valid
from .. import Component
from ..controls import ButtonControl, FixedRadioButtonGroup, MappedButtonControl, MappedControl, ToggleButtonControl, control_list

class DeviceComponent(Component):
    bank_skin = {'color':'Device.Bank.Navigation', 
     'pressed_color':'Device.Bank.NavigationPressed'}
    prev_bank_button = ButtonControl(**bank_skin)
    next_bank_button = ButtonControl(**bank_skin)
    bank_select_buttons = FixedRadioButtonGroup(control_count=8,
      unchecked_color='Device.Bank.NotSelected',
      checked_color='Device.Bank.Selected')
    device_on_off_button = MappedButtonControl(color='Device.Off', on_color='Device.On')
    device_lock_button = ToggleButtonControl(untoggled_color='Device.LockOff',
      toggled_color='Device.LockOn')
    parameter_controls = control_list(MappedControl, control_count=8)

    @depends(device_provider=None,
      device_bank_registry=None,
      toggle_lock=None,
      show_message=None)
    def __init__(self, name='Device', device_provider=None, device_bank_registry=None, toggle_lock=None, show_message=None, force_use_parameter_banks=False, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._device_bank_registry = device_bank_registry
        self._show_message = show_message
        self._toggle_lock = toggle_lock
        self._use_parameter_banks = force_use_parameter_banks
        self._has_parameter_controls = False
        self._device = None
        self._banks = []
        self._bank_index = 0
        self._device_provider = device_provider
        self._DeviceComponent__on_provided_device_changed.subject = device_provider
        self._DeviceComponent__on_provided_device_changed()
        self.register_slot(self._device_provider, self._update_device_lock_button, 'is_locked_to_device')
        self._update_device_lock_button()

    def disconnect(self):
        self._device = None
        self._banks = None
        super().disconnect()

    def set_parameter_controls(self, controls):
        self._has_parameter_controls = controls is not None
        self.parameter_controls.set_control_element(controls)
        self._show_device_and_bank_name()

    def set_bank_select_buttons(self, buttons):
        self._on_bank_buttons_set()
        self.bank_select_buttons.set_control_element(buttons)

    def set_prev_bank_button(self, button):
        self._on_bank_buttons_set()
        self.prev_bank_button.set_control_element(button)

    def set_next_bank_button(self, button):
        self._on_bank_buttons_set()
        self.next_bank_button.set_control_element(button)

    def _on_bank_buttons_set(self):
        if not self._use_parameter_banks:
            self._use_parameter_banks = True
            self.update()

    @device_lock_button.toggled
    def device_lock_button(self, *_):
        self._toggle_lock()

    @bank_select_buttons.checked
    def bank_select_buttons(self, button):
        self.bank_index = button.index

    @prev_bank_button.pressed
    def prev_bank_button(self, _):
        self.bank_index = self._bank_index - 1

    @next_bank_button.pressed
    def next_bank_button(self, _):
        self.bank_index = self._bank_index + 1

    @property
    def bank_index(self):
        if self._use_parameter_banks:
            return self._bank_index
        return 0

    @bank_index.setter
    def bank_index(self, value):
        self._bank_index = self._clamp_to_bank_size(value)
        self._device_bank_registry.set_device_bank(self._device, self._bank_index)
        self.update()

    def _clamp_to_bank_size(self, value):
        return clamp(value, 0, self.num_banks - 1)

    @property
    def selected_bank(self):
        if self.num_banks:
            return self._banks[(self._bank_index or 0)]
        return []

    @property
    def num_banks(self):
        return len(self._banks)

    @listens('device')
    def __on_provided_device_changed(self):
        self._device = self._device_provider.device
        self._DeviceComponent__on_bank_changed.subject = self._device_bank_registry
        self._bank_index = self._device_bank_registry.get_device_bank(self._device)
        self.update()

    @listens('device_bank')
    def __on_bank_changed(self, device, bank):
        if device == self._device:
            self.bank_index = bank

    def update(self):
        super().update()
        if self.is_enabled():
            self._update_parameter_banks()
            self._update_bank_select_buttons()
            self._update_bank_navigation_buttons()
            if liveobj_valid(self._device):
                self._connect_parameters()
                self._show_device_and_bank_name()
            else:
                self._disconnect_parameters()
        else:
            self._disconnect_parameters()

    def _show_device_and_bank_name(self):
        if self._has_parameter_controls:
            if liveobj_valid(self._device):
                self._show_message('Controlling {}: {}'.format(self._device.name, self._get_bank_name()))

    def _get_bank_name(self):
        bank_name = ''
        if liveobj_valid(self._device):
            if self._use_parameter_banks:
                names = parameter_bank_names(self._device)
                if self._bank_index < len(names):
                    bank_name = names[self._bank_index]
            else:
                bank_name = 'Best of Parameters'
        return bank_name

    def _disconnect_parameters(self):
        for control in self.parameter_controls:
            control.mapped_parameter = None

        self.device_on_off_button.mapped_parameter = None

    def _connect_parameters(self):
        for control, parameter in zip_longest(self.parameter_controls, self.selected_bank):
            control.mapped_parameter = parameter if liveobj_valid(parameter) else None

        self.device_on_off_button.mapped_parameter = self._on_off_parameter()

    def _on_off_parameter(self):
        if liveobj_valid(self._device):
            for p in self._device.parameters:
                if p.name.startswith('Device On'):
                    if liveobj_valid(p):
                        if p.is_enabled:
                            return p

    def _update_parameter_banks(self):
        if liveobj_valid(self._device):
            if self._use_parameter_banks:
                self._banks = parameter_banks(self._device)
            else:
                self._banks = [
                 best_of_parameter_bank(self._device)]
        else:
            self._banks = []
        self._bank_index = self._clamp_to_bank_size(self._bank_index)

    def _update_device_lock_button(self):
        self.device_lock_button.is_toggled = self._device_provider.is_locked_to_device

    def _update_bank_select_buttons(self):
        self.bank_select_buttons.active_control_count = self.num_banks
        if self.bank_index < self.num_banks:
            self.bank_select_buttons[self.bank_index].is_checked = True

    def _update_bank_navigation_buttons(self):
        self.prev_bank_button.enabled = self.bank_index > 0
        self.next_bank_button.enabled = self.bank_index < self.num_banks - 1