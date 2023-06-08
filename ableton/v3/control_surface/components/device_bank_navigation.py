from __future__ import absolute_import, print_function, unicode_literals
from math import ceil
from ...base import depends, listens
from ..controls import FixedRadioButtonGroup
from .scroll import Scrollable, ScrollComponent
NUM_BANK_SELECT_BUTTONS = 8

class DeviceBankNavigationComponent(ScrollComponent, Scrollable):
    bank_select_buttons = FixedRadioButtonGroup(control_count=NUM_BANK_SELECT_BUTTONS,
      unchecked_color='Device.Bank.NotSelected',
      checked_color='Device.Bank.Selected')

    @depends(device_bank_registry=None)
    def __init__(self, name='Device_Bank_Navigation', banking_info=None, device_bank_registry=None, *a, **k):
        (super().__init__)(a, name=name, scroll_skin_name='Device.Bank.Navigation', **k)
        self._bank_provider = None
        self._banking_info = banking_info
        self._device_bank_registry = device_bank_registry

    @property
    def bank_provider(self):
        return self._bank_provider

    @bank_provider.setter
    def bank_provider(self, provider):
        self._bank_provider = provider
        self._sync_registry()
        self._DeviceBankNavigationComponent__on_provider_bank_changed.subject = provider
        self._DeviceBankNavigationComponent__on_parameters_changed_in_device.subject = provider.device if provider else None
        self.update()

    def set_bank_scroll_encoder(self, encoder):
        self.set_scroll_encoder(encoder)

    def set_prev_bank_button(self, button):
        self.set_scroll_down_button(button)

    def set_next_bank_button(self, button):
        self.set_scroll_up_button(button)

    def set_bank_select_buttons(self, buttons):
        self.bank_select_buttons.set_control_element(buttons)
        self._sync_registry()

    def can_scroll_up(self):
        return self._bank_provider is not None and (self.scroll_down_button.control_element is None or self._bank_provider.index < self._bank_provider.bank_count() - self._banking_info.num_simultaneous_banks)

    def can_scroll_down(self):
        return self._bank_provider is not None and self._bank_provider.index > 0

    def scroll_up(self):
        roundtrip_banking = self.scroll_down_button.control_element is None and self.scroll_up_button.is_pressed
        new_index = self._bank_provider.index + self._banking_info.num_simultaneous_banks
        if roundtrip_banking:
            if new_index >= self._bank_provider.bank_count():
                new_index = 0
        self._bank_provider.index = new_index

    def scroll_down(self):
        self._bank_provider.index = self._bank_provider.index - self._banking_info.num_simultaneous_banks

    @bank_select_buttons.checked
    def bank_select_buttons(self, button):
        self._bank_provider.index = button.index * self._banking_info.num_simultaneous_banks + int(self._should_skip_first_bank())

    def _adjusted_bank_count(self):
        if self._bank_provider:
            return ceil(self._bank_provider.bank_count() / self._banking_info.num_simultaneous_banks)
        return 0

    def _should_skip_first_bank(self):
        return self.bank_select_buttons[0].control_element is not None and self._bank_provider is not None and self._banking_info.has_main_bank(self._bank_provider.device) and self._adjusted_bank_count() > NUM_BANK_SELECT_BUTTONS

    def _sync_registry(self):
        registry = self._device_bank_registry
        device = self._bank_provider.device if self._bank_provider is not None else None
        if self._should_skip_first_bank():
            if registry.get_device_bank(device) == 0:
                registry.set_device_bank(device, 1)

    @listens('parameters')
    def __on_provider_bank_changed(self):
        self.update()

    @listens('parameters')
    def __on_parameters_changed_in_device(self):
        self.update()

    def update(self):
        super().update()
        self._update_bank_select_buttons()

    def _update_bank_select_buttons(self):
        bank_index = ceil((self._bank_provider.index if self._bank_provider else 0) / self._banking_info.num_simultaneous_banks)
        bank_count = self._adjusted_bank_count()
        if self._should_skip_first_bank():
            bank_count -= 1
            bank_index -= 1
        has_banks = bank_count > 1
        self.bank_select_buttons.active_control_count = bank_count if has_banks else 0
        if has_banks:
            self.bank_select_buttons.checked_index = bank_index if bank_index < NUM_BANK_SELECT_BUTTONS else -1