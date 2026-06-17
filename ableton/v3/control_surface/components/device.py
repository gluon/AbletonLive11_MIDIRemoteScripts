# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\device.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 12380 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.simpler_slice_nudging import SimplerSliceNudging
from ...base import depends, find_if, listenable_property, listens
from ...live import deduplicate_parameters, liveobj_changed, liveobj_valid
from .. import DEFAULT_BANK_SIZE, BankingInfo, Component, ParameterProvider, create_parameter_bank, legacy_bank_definitions
from ..controls import MappedButtonControl, ToggleButtonControl
from ..default_bank_definitions import BANK_DEFINITIONS
from ..device_decorators import DeviceDecoratorFactory
from ..display import Renderable
from ..parameter_info import ParameterInfo
from ..parameter_mapping_sensitivities import DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY, parameter_mapping_sensitivities
from .device_bank_navigation import DeviceBankNavigationComponent
from .device_parameters import DeviceParametersComponent

def get_on_off_parameter(device):
    if liveobj_valid(device):
        return find_if(lambda p: p.original_name.startswith('Device On') and liveobj_valid(p) and p.is_enabled
, device.parameters)


def create_device_decorator_factory--- This code section failed: ---

 L.  57         0  LOAD_FAST                'bank_definitions'

 L.  58         2  LOAD_GLOBAL              legacy_bank_definitions
                4  LOAD_METHOD              banked
                6  CALL_METHOD_0         0  '0 positional arguments'
                8  LOAD_GLOBAL              legacy_bank_definitions
               10  LOAD_METHOD              best_of_banks
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  BUILD_LIST_2          2 
               16  COMPARE_OP               not-in
               18  POP_JUMP_IF_FALSE    30  'to 30'
               20  LOAD_FAST                'device_decorator_factory'
               22  JUMP_IF_TRUE_OR_POP    32  'to 32'
               24  LOAD_GLOBAL              DeviceDecoratorFactory
               26  CALL_FUNCTION_0       0  '0 positional arguments'
               28  RETURN_VALUE     
             30_0  COME_FROM            18  '18'

 L.  59        30  LOAD_CONST               None
             32_0  COME_FROM            22  '22'
               32  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 32_0


class DeviceComponent(ParameterProvider, Component, Renderable):
    device_on_off_button = MappedButtonControl(color='Device.Off', on_color='Device.On')
    device_lock_button = ToggleButtonControl(color='Device.LockOff',
      on_color='Device.LockOn')

    @depends(device_provider=None,
      device_bank_registry=None,
      toggle_lock=None,
      show_message=None)
    def __init__(self, name='Device', continuous_parameter_sensitivity=DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, quantized_parameter_sensitivity=DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY, parameters_component_type=None, bank_size=DEFAULT_BANK_SIZE, bank_definitions=None, bank_navigation_component_type=None, device_provider=None, device_bank_registry=None, device_decorator_factory=None, toggle_lock=None, show_message=None, *a, **k):
        self._decorated_device = None
        self._provided_parameters = []
        self._device_provider = device_provider
        self._device_bank_registry = device_bank_registry
        self._decorator_factory = create_device_decorator_factory(device_decorator_factory, bank_definitions)
        self._parameter_mapping_sensitivities = parameter_mapping_sensitivities(continuous_parameter_sensitivity=continuous_parameter_sensitivity,
          quantized_parameter_sensitivity=quantized_parameter_sensitivity)
        parameters_component_type = parameters_component_type or DeviceParametersComponent
        self._parameters_component = parameters_component_type()
        self._parameters_component.parameter_provider = self
        self._bank = None
        self._banking_info = BankingInfo((bank_definitions or BANK_DEFINITIONS),
          bank_size=bank_size)
        bank_navigation_component_type = bank_navigation_component_type or DeviceBankNavigationComponent
        self._bank_navigation_component = bank_navigation_component_type(banking_info=(self._banking_info),
          device_bank_registry=device_bank_registry)
        (super().__init__)(a, name=name, **k)
        self._toggle_lock = toggle_lock
        self._show_message = show_message
        self._slice_nudging = self.register_disconnectable(SimplerSliceNudging())
        self.add_children(self._parameters_component, self._bank_navigation_component)
        self._DeviceComponent__on_provided_device_changed.subject = device_provider
        self._DeviceComponent__on_provided_device_changed()
        self.register_slot(self._device_provider, self._update_device_lock_button, 'is_locked_to_device')
        self._update_device_lock_button()

    @property
    def parameters(self):
        return self._provided_parameters

    @listenable_property
    def device(self):
        return self._decorated_device

    @device.setter
    def device(self, device):
        self._device_provider.device = device

    @listenable_property
    def bank_name(self):
        if self.device:
            return self._current_bank_details()[0]
        return ''

    def set_parameter_controls(self, controls):
        self._parameters_component.set_parameter_controls(controls)
        self._show_device_and_bank_info()

    def __getattr__(self, name):
        if name.startswith('set_'):
            if 'bank' in name:
                return getattr(self._bank_navigation_component, name)
        raise AttributeError

    @device_lock_button.toggled
    def device_lock_button(self, *_):
        self._toggle_lock()

    def _create_parameter_info(self, parameter, name):
        default, fine_grain = self._parameter_mapping_sensitivities(parameter, self.device)
        return ParameterInfo(parameter=parameter,
          name=name,
          default_encoder_sensitivity=default,
          fine_grain_encoder_sensitivity=fine_grain)

    def _set_device(self, device):
        self._set_decorated_device(self._get_decorated_device(device))
        device_bank_registry = self._device_bank_registry
        self._DeviceComponent__on_bank_changed.subject = device_bank_registry
        self._set_bank_index(device_bank_registry.get_device_bank(device))
        self._update_parameters()
        self._DeviceComponent__on_parameters_changed_in_device.subject = device
        self.device_on_off_button.mapped_parameter = get_on_off_parameter(device)
        self.notify_device()
        self.notify_bank_name()

    def _get_decorated_device(self, device):
        if self._decorator_factory is not None:
            return self._decorator_factory.decorate(device)
        return device

    def _set_decorated_device(self, decorated_device):
        self._decorated_device = decorated_device
        self._slice_nudging.set_device(decorated_device)
        self._setup_bank(decorated_device)
        self._DeviceComponent__on_bank_parameters_changed.subject = self._bank

    def _on_device_changed(self, device):
        current_device = getattr(self.device, '_live_object', self.device)
        if liveobj_changed(current_device, device):
            self._set_device(device)

    def _setup_bank(self, device, bank_factory=create_parameter_bank):
        if self._bank is not None:
            self.disconnect_disconnectable(self._bank)
            self._bank = None
        if liveobj_valid(device):
            self._bank = self.register_disconnectable(bank_factory(device, self._banking_info))
        self._bank_navigation_component.bank_provider = self._bank

    def _set_bank_index(self, bank):
        if self._bank is not None:
            self._bank.index = bank
        if liveobj_valid(self.device):
            self.notify_bank_name()
            self._show_device_and_bank_info()

    def _current_bank_details(self):
        if self._bank is not None:
            return (self._bank.name, self._bank.parameters)
        return (
         '', [None] * self._parameters_component.controls.control_count)

    def _show_device_and_bank_info(self):
        device = self.device
        if liveobj_valid(device):
            if self._parameters_component.controls[0].control_element:
                self._show_message('Controlling {}: {}'.format(device.name, self.bank_name))

    def _get_provided_parameters(self):
        _, parameters = self._current_bank_details() if self.device else (None, ())
        return deduplicate_parameters([self._create_parameter_info(param, name) for param, name in parameters])

    def _update_parameters(self):
        self._provided_parameters = self._get_provided_parameters()
        self.notify_parameters()

    def _update_device_lock_button(self):
        self.device_lock_button.is_on = self._device_provider.is_locked_to_device

    @listens('device')
    def __on_provided_device_changed(self):
        self._on_device_changed(self._device_provider.device)

    @listens('device_bank')
    def __on_bank_changed(self, device, bank):
        if device == self.device:
            self._set_bank_index(bank)

    @listens('parameters')
    def __on_parameters_changed_in_device(self):
        self._update_parameters()

    @listens('parameters')
    def __on_bank_parameters_changed(self):
        self._update_parameters()
        self._device_bank_registry.set_device_bank(self.device, self._bank.index)