#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Akai_Force_MPC/device_parameters.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from past.utils import old_div
from future.moves.itertools import zip_longest
from itertools import chain
from ableton.v2.base import clamp, is_parameter_bipolar, listens, liveobj_valid
from ableton.v2.control_surface.components import DisplayingDeviceParameterComponent as DeviceParameterComponentBase
from ableton.v2.control_surface.control import ButtonControl, ConfigurableTextDisplayControl, SendValueControl, control_list, is_internal_parameter
from ableton.v2.control_surface.elements import DisplayDataSource
from .control import SendingMappedAbsoluteControl, SendingMappedSensitivitySettingControl
from .elements import NUM_PARAM_CONTROLS
OFF_VALUE = 0
ON_VALUE = 127
DISPLAY_STYLE_NONE = 0
DISPLAY_STYLE_UNIPOLAR = 1
DISPLAY_STYLE_BIIPOLAR = 2

def normalized_parameter_value(param):
    value = 0.0
    if liveobj_valid(param):
        param_range = param.max - param.min
        value = old_div(float(param.value - param.min), param_range)
    return value


def convert_parameter_value_to_midi_value(param):
    return clamp(int(normalized_parameter_value(param) * 127), 0, 127)


def display_style_for_parameter(parameter):
    display_style = DISPLAY_STYLE_NONE
    if liveobj_valid(parameter):
        display_style = DISPLAY_STYLE_BIIPOLAR if is_parameter_bipolar(parameter) else DISPLAY_STYLE_UNIPOLAR
    return display_style


class DeviceParameterComponent(DeviceParameterComponentBase):
    controls = control_list(SendingMappedSensitivitySettingControl, NUM_PARAM_CONTROLS)
    absolute_controls = control_list(SendingMappedAbsoluteControl, NUM_PARAM_CONTROLS)
    parameter_enable_controls = control_list(SendValueControl, NUM_PARAM_CONTROLS)
    display_style_controls = control_list(SendValueControl, NUM_PARAM_CONTROLS)
    touch_controls = control_list(ButtonControl, NUM_PARAM_CONTROLS)
    parameter_name_or_value_displays = control_list(ConfigurableTextDisplayControl, NUM_PARAM_CONTROLS)
    device_enable_button = ButtonControl()

    def __init__(self, *a, **k):
        self._physical_display_parameter_name_data_sources = list(map(DisplayDataSource, (u'',) * NUM_PARAM_CONTROLS))
        self._physical_display_parameter_value_data_sources = list(map(DisplayDataSource, (u'',) * NUM_PARAM_CONTROLS))
        super(DeviceParameterComponent, self).__init__(*a, **k)
        self._update_parameter_name_or_value_displays()

    @property
    def device_on_off_parameter(self):
        device = self.parameter_provider.device()
        if liveobj_valid(device):
            return device.parameters[0]

    def set_name_display_line(self, line):
        super(DeviceParameterComponent, self).set_name_display_line(line)
        self._set_display_line(line, self._physical_display_parameter_name_data_sources)

    def set_value_display_line(self, line):
        super(DeviceParameterComponent, self).set_value_display_line(line)
        self._set_display_line(line, self._physical_display_parameter_value_data_sources)

    def set_absolute_parameter_controls(self, controls):
        self.absolute_controls.set_control_element(controls)
        self._connect_parameters()

    @touch_controls.pressed
    def touch_controls(self, _):
        self._update_parameter_name_or_value_displays()

    @touch_controls.released
    def touch_controls(self, _):
        self._update_parameter_name_or_value_displays()

    @device_enable_button.pressed
    def device_enable_button(self, _):
        self._toggle_device_enabled_status()

    def _toggle_device_enabled_status(self):
        on_off = self.device_on_off_parameter
        if liveobj_valid(on_off) and on_off.is_enabled:
            on_off.value = not on_off.value

    def _clear_display(self):
        super(DeviceParameterComponent, self)._clear_display()
        for source in chain(self._physical_parameter_name_data_sources, self._physical_parameter_value_data_sources):
            source.set_display_string(u'')

    def _update_parameter_names(self):
        super(DeviceParameterComponent, self)._update_parameter_names()
        for info, name_data_source in zip_longest(self.parameter_provider.parameters, self._physical_display_parameter_name_data_sources):
            name_data_source.set_display_string(self.info_to_name(info))

    def _update_parameter_values(self):
        super(DeviceParameterComponent, self)._update_parameter_values()
        for parameter, data_source, control, absolute_control in zip_longest(self.parameters, self._physical_display_parameter_value_data_sources, self.controls, self.absolute_controls):
            data_source.set_display_string(self.parameter_to_string(parameter))
            if is_internal_parameter(parameter):
                value_to_send = convert_parameter_value_to_midi_value(parameter)
                control.value = value_to_send
                absolute_control.value = value_to_send

    def _connect_parameters(self):
        for control, absolute_control, display_style_control, parameter_info in zip_longest(self.controls, self.absolute_controls, self.display_style_controls, self._parameter_provider.parameters[:NUM_PARAM_CONTROLS]):
            parameter = parameter_info.parameter if parameter_info else None
            control.mapped_parameter = parameter
            absolute_control.mapped_parameter = parameter
            display_style_control.value = display_style_for_parameter(parameter)
            if parameter:
                control.update_sensitivities(parameter_info.default_encoder_sensitivity, parameter_info.fine_grain_encoder_sensitivity)

        self._update_parameter_enable_controls()

    def _on_parameter_provider_changed(self, provider):
        self.__on_device_changed.subject = provider
        self.__on_device_changed()

    @listens(u'device')
    def __on_device_changed(self):
        self.__on_device_enabled_changed.subject = self.device_on_off_parameter
        self.__on_device_enabled_changed()

    @listens(u'value')
    def __on_device_enabled_changed(self):
        self._update_device_enable_button()

    def _update_device_enable_button(self):
        on_off = self.device_on_off_parameter
        self.device_enable_button.color = u'DefaultButton.On' if liveobj_valid(on_off) and on_off.value else u'DefaultButton.Off'

    def _update_parameter_enable_controls(self):
        for control, parameter_info in zip_longest(self.parameter_enable_controls, self._parameter_provider.parameters[:self.controls.control_count]):
            control.value = ON_VALUE if parameter_info and parameter_info.parameter else OFF_VALUE

    def _update_parameter_name_or_value_displays(self):
        for display, control, name_data_source, value_data_source in zip(self.parameter_name_or_value_displays, self.touch_controls, self._physical_display_parameter_name_data_sources, self._physical_display_parameter_value_data_sources):
            display.set_data_sources([value_data_source if control.is_pressed else name_data_source])
