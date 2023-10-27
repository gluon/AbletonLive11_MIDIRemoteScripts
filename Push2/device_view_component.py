# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\device_view_component.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 6136 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject, const, listenable_property, listens, liveobj_valid
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.mode import ModesComponent
from pushbase.internal_parameter import ProxyParameter

class NamedParameter(EventObject):

    def __init__(self, name):
        self._name = name

    @listenable_property
    def name(self):
        return self._name


def get_view_parameter(parameter, name):
    if liveobj_valid(parameter):
        if name != parameter.name:
            parameter = ProxyParameter(proxied_object=parameter,
              proxied_interface=(NamedParameter(name)))
    return parameter


class DeviceViewConnector(Component):

    def __init__(self, device_component=None, parameter_provider=None, device_type_provider=const('default'), view=None, *a, **k):
        (super(DeviceViewConnector, self).__init__)(*a, **k)
        self._device_component = device_component
        self._parameter_provider = parameter_provider
        self._view = view
        self._parameter_infos = None
        self._device_type_provider = device_type_provider

    def update(self):
        super(DeviceViewConnector, self).update()
        if self.is_enabled():
            self._view.deviceType = self._device_type_provider()
        self._view.device = self._device_component.device()
        parameter_infos = self._value_for_state(self._parameter_provider.parameters, [])
        if parameter_infos != self._parameter_infos:
            self._parameter_infos = parameter_infos
            self._view.parameters = [get_view_parameter(info.parameter, info.name) if info else None for info in parameter_infos]

    def on_enabled_changed(self):
        self._view.visible = self.is_enabled()
        self._on_parameters_changed.subject = self._value_for_state(self._parameter_provider, None)
        super(DeviceViewConnector, self).on_enabled_changed()

    @listens('parameters')
    def _on_parameters_changed(self):
        self.update()

    def _value_for_state(self, enabled_value, disabled_value):
        if self.is_enabled():
            return enabled_value
        return disabled_value


class SimplerDeviceViewConnector(DeviceViewConnector):

    def update(self):
        super(SimplerDeviceViewConnector, self).update()
        device = self._value_for_state(self._device_component.device(), None)
        self._view.properties = device
        self._view.bank_view_description = self._parameter_provider.device_component.bank_view_description


class CompressorDeviceViewConnector(DeviceViewConnector):

    def update(self):
        super(CompressorDeviceViewConnector, self).update()
        device = self._value_for_state(self._device_component.device(), None)
        self._view.bank_view_description = self._parameter_provider.device_component.bank_view_description
        if liveobj_valid(device):
            self._view.routing_type_list = device.routing_type_list
            self._view.routing_channel_list = device.routing_channel_list
            self._view.routing_channel_position_list = device.routing_channel_position_list


class DeviceViewComponent(ModesComponent):

    def __init__(self, device_component=None, view_model=None, *a, **k):
        (super(DeviceViewComponent, self).__init__)(*a, **k)
        self._get_device = device_component.device
        for view, connector, name in (
         (
          view_model.deviceParameterView, DeviceViewConnector, 'default'),
         (
          view_model.simplerDeviceView, SimplerDeviceViewConnector, 'OriginalSimpler'),
         (
          view_model.compressorDeviceView,
          CompressorDeviceViewConnector,
          'Compressor2')):
            view.visible = False
            self.add_mode(name, connector(device_component=device_component,
              parameter_provider=device_component,
              device_type_provider=(self._device_type),
              view=view,
              is_enabled=False))

        self._on_parameters_changed.subject = device_component
        self._on_parameters_changed()

    def on_enabled_changed(self):
        self._last_selected_mode = None
        super(DeviceViewComponent, self).on_enabled_changed()

    def update(self):
        super(DeviceViewComponent, self).update()
        if self.is_enabled():
            self.selected_mode = self._mode_to_select()

    def _device_type(self):
        device = self._get_device()
        if liveobj_valid(device):
            return device.class_name
        return ''

    def _mode_to_select(self):
        device = self._get_device()
        device_type = device and device.class_name
        if self.get_mode(device_type) != None:
            return device_type
        return 'default'

    @listens('parameters')
    def _on_parameters_changed(self):
        self.selected_mode = self._mode_to_select()