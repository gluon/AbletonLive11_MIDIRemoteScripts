#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/hybrid_reverb.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject, listens
from ableton.v2.control_surface import NotifyingList, EnumWrappingParameter, BoolWrappingParameter, WrappingParameter
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_options import DeviceSwitchOption, DeviceOnOffOption
from ableton.v2.base import clamp
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .visualisation_settings import VisualisationGuides
import re
import Live
import math
ParameterState = Live.DeviceParameter.ParameterState

def user_to_linear_log(minv, maxv):
    min = math.log(minv)
    range = math.log(maxv) - min
    return lambda v, s: (math.log(v) - min) / range


def linear_to_user_log(minv, maxv):
    min = math.log(minv)
    range = math.log(maxv) - min
    return lambda v, s: math.exp(min + v * range)


def user_to_linear_exp(minv, maxv, scalv):
    range = maxv - minv
    scal = 1.0 / scalv

    def exp_calc(v, self):
        min = clamp(v - minv, 0.0, range)
        return math.pow(min / range, scal)

    return exp_calc


def linear_to_user_exp(minv, maxv, scalv):
    range = maxv - minv
    return lambda v, s: math.pow(v, scalv) * range + minv


def to_percentage_display(value):
    percentage = 100.0 * value
    format_str = u'%.0f'
    percentage_str = format_str % percentage
    return unicode(percentage_str + u' %')


def to_ms_display(value):
    format = u'%.2f'
    if value < 0.9995:
        value = value * 1000
        if value < 10:
            format = u'%.2f'
        elif value < 100:
            format = u'%.1f'
        elif value < 1000:
            format = u'%.0f'
        out_str = str(format % value) + u' ms'
    else:
        if value < 10:
            format = u'%.2f'
        elif value < 100:
            format = u'%.1f'
        else:
            format = u'%.0f'
        out_str = str(format % value) + u' s'
    return out_str


class HybridReverbDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        super(HybridReverbDeviceDecorator, self).__init__(*a, **k)
        self.main_section_labels = [u'Convolution',
         u'Algo',
         u'Mix',
         u'EQ']
        self.routing_full_labels = [u'Serial',
         u'Parallel',
         u'Algorithm',
         u'Convolution']
        self.routing_option_labels = [u'Ser.',
         u'Par.',
         u'Alg.',
         u'Cv.']
        self.vintage_labels = [u'Off',
         u'Subtle',
         u'Old',
         u'Older',
         u'Extreme']
        self.band_names_labels = [u'1&4', u'2&3']
        self.pre_delay_sync_labels = [u'Ms', u'Sync']
        self.filter_types_labels = [u'Cut', u'Shelf']
        self.routing_live_parameter = get_parameter_by_name(self, u'Routing')
        self.vintage_live_parameter = get_parameter_by_name(self, u'Vintage')
        self.pre_delay_sync_live_parameter = get_parameter_by_name(self, u'P.Dly Sync')
        self.eq_low_type_live_parameter = get_parameter_by_name(self, u'EQ Low Type')
        self.eq_high_type_live_parameter = get_parameter_by_name(self, u'EQ High Type')
        self.eq_on_live_parameter = get_parameter_by_name(self, u'EQ On')
        self.freeze_live_parameter = get_parameter_by_name(self, u'Freeze')
        self.freeze_in_live_parameter = get_parameter_by_name(self, u'Freeze In')
        self.eq_prealgo_live_parameter = get_parameter_by_name(self, u'EQ Pre Algo')
        self.bass_mono_live_parameter = get_parameter_by_name(self, u'Bass Mono')
        self._band_names_provider = NotifyingList(available_values=self.band_names_labels, default_value=0)
        self.band = EnumWrappingParameter(name=u'Band', parent=self, values_host=self._band_names_provider, index_property_host=self._band_names_provider, values_property=u'available_values', index_property=u'index')
        self._main_section_provider = NotifyingList(available_values=self.main_section_labels, default_value=0)
        self.main_section = EnumWrappingParameter(name=u'Section', parent=self, values_host=self._main_section_provider, index_property_host=self._main_section_provider, values_property=u'available_values', index_property=u'index')
        self.routing_switch = DeviceSwitchOption(name=u'Routing Switch', parameter=self.routing_live_parameter, labels=self.routing_option_labels)
        self.feedback_ms_sync_switch = DeviceSwitchOption(name=u'Ms Sync Switch', parameter=self.pre_delay_sync_live_parameter, labels=self.pre_delay_sync_labels)
        self.eq_low_type_switch = DeviceSwitchOption(name=u'Low Type Switch', parameter=self.eq_low_type_live_parameter, labels=self.filter_types_labels)
        self.eq_high_type_switch = DeviceSwitchOption(name=u'High Type Switch', parameter=self.eq_high_type_live_parameter, labels=self.filter_types_labels)
        self.ir_post_processing_bool = BoolWrappingParameter(name=u'Ir Post Processing Bool', parent=self, property_host=self, source_property=u'ir_time_shaping_on')
        self.ir_post_processing_option = DeviceOnOffOption(name=u'Shape', property_host=self.ir_post_processing_bool)
        self.eq_on_option = DeviceOnOffOption(name=u'EQ', property_host=self.eq_on_live_parameter)
        self.freeze_option = DeviceOnOffOption(name=u'Freeze', property_host=self.freeze_live_parameter)
        self.freeze_in_option = DeviceOnOffOption(name=u'Freeze In', property_host=self.freeze_in_live_parameter)
        self.prealgo_option = DeviceOnOffOption(name=u'Pre Algo', property_host=self.eq_prealgo_live_parameter)
        self.bass_mono_option = DeviceOnOffOption(name=u'Bass Mono', property_host=self.bass_mono_live_parameter)
        self.ir_attack_time_parameter = WrappingParameter(name=u'Ir Attack Time', parent=self, property_host=self, source_property=u'ir_attack_time', display_value_conversion=to_ms_display, from_property_value=user_to_linear_exp(0.0, 3.0, 3.33), to_property_value=linear_to_user_exp(0.0, 3.0, 3.33))
        self.ir_decay_time_parameter = WrappingParameter(name=u'Ir Decay Time', parent=self, property_host=self, source_property=u'ir_decay_time', display_value_conversion=to_ms_display, from_property_value=user_to_linear_exp(0.02, 20.0, 3.33), to_property_value=linear_to_user_exp(0.02, 20.0, 3.33))
        self.ir_size_factor_parameter = WrappingParameter(name=u'Ir Size Factor', parent=self, property_host=self, source_property=u'ir_size_factor', display_value_conversion=to_percentage_display, from_property_value=user_to_linear_log(0.2, 5.0), to_property_value=linear_to_user_log(0.2, 5.0))
        self.ir_category_list_parameter = EnumWrappingParameter(name=u'IR Category', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'ir_category_list', index_property=u'ir_category_index')
        self.ir_file_list_parameter = EnumWrappingParameter(name=u'IR', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'ir_file_list', index_property=u'ir_file_index')
        self.vintage_enum_copy = NotifyingList(available_values=self.vintage_labels, default_value=0)
        self.vintage_parameter_copy = EnumWrappingParameter(name=u'Vintage Copy', parent=self, values_host=self.vintage_enum_copy, index_property_host=self.vintage_enum_copy, values_property=u'available_values', index_property=u'index')
        self.routing_parameter_enum = NotifyingList(available_values=self.routing_full_labels, default_value=0)
        self.routing_parameter_eq_off = EnumWrappingParameter(name=u'Routing Eq Off', parent=self, values_host=self.routing_parameter_enum, index_property_host=self.routing_parameter_enum, values_property=u'available_values', index_property=u'index')
        self.routing_parameter_eq_on_prealgo_off = EnumWrappingParameter(name=u'Routing Eq On PreAlgo Off', parent=self, values_host=self.routing_parameter_enum, index_property_host=self.routing_parameter_enum, values_property=u'available_values', index_property=u'index')
        self.routing_parameter_eq_on_prealgo_on = EnumWrappingParameter(name=u'Routing Eq On PreAlgo On', parent=self, values_host=self.routing_parameter_enum, index_property_host=self.routing_parameter_enum, values_property=u'available_values', index_property=u'index')
        self.on_routing_parameter_change.subject = self.routing_live_parameter
        self.on_routing_parameter_change()
        self.on_routing_parameter_eq_off_change.subject = self.routing_parameter_eq_off
        self.on_routing_parameter_eq_off_change()
        self.on_routing_parameter_eq_on_prealgo_on_change.subject = self.routing_parameter_eq_on_prealgo_on
        self.on_routing_parameter_eq_on_prealgo_on_change()
        self.on_routing_parameter_eq_on_prealgo_off_change.subject = self.routing_parameter_eq_on_prealgo_off
        self.on_routing_parameter_eq_on_prealgo_off_change()
        self.on_vintage_parameter_change.subject = self.vintage_live_parameter
        self.on_vintage_parameter_change()
        self.on_vintage_copy_parameter_change.subject = self.vintage_parameter_copy
        self.on_vintage_copy_parameter_change()
        self.on_shape_option_change.subject = self.ir_post_processing_bool
        self.on_shape_option_change()
        self._additional_parameters = (self.band,
         self.main_section,
         self.ir_post_processing_bool,
         self.ir_attack_time_parameter,
         self.ir_decay_time_parameter,
         self.ir_size_factor_parameter,
         self.ir_category_list_parameter,
         self.ir_file_list_parameter,
         self.vintage_parameter_copy,
         self.routing_parameter_eq_off,
         self.routing_parameter_eq_on_prealgo_on,
         self.routing_parameter_eq_on_prealgo_off)
        self.register_disconnectable(self._additional_parameters)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    @property
    def options(self):
        return (self.feedback_ms_sync_switch,
         self.eq_low_type_switch,
         self.eq_high_type_switch,
         self.routing_switch,
         self.eq_on_option,
         self.ir_post_processing_option,
         self.freeze_option,
         self.freeze_in_option,
         self.prealgo_option,
         self.bass_mono_option)

    @listens(u'value')
    def on_vintage_parameter_change(self):
        self.vintage_parameter_copy.value = self.vintage_live_parameter.value

    @listens(u'value')
    def on_vintage_copy_parameter_change(self):
        if self.vintage_parameter_copy.value != self.vintage_live_parameter.value:
            self.vintage_live_parameter.value = self.vintage_parameter_copy.value

    @listens(u'value')
    def on_shape_option_change(self):
        self.update_convolution_parameters()

    @listens(u'value')
    def on_routing_parameter_change(self):
        self.routing_parameter_eq_off.value = self.routing_live_parameter.value
        self.routing_parameter_eq_on_prealgo_on.value = self.routing_live_parameter.value
        self.routing_parameter_eq_on_prealgo_off.value = self.routing_live_parameter.value
        self.update_convolution_parameters()

    @listens(u'value')
    def on_routing_parameter_eq_off_change(self):
        self.set_routing_parameter(self.routing_parameter_eq_off.value)

    @listens(u'value')
    def on_routing_parameter_eq_on_prealgo_on_change(self):
        self.set_routing_parameter(self.routing_parameter_eq_on_prealgo_on.value)

    @listens(u'value')
    def on_routing_parameter_eq_on_prealgo_off_change(self):
        self.set_routing_parameter(self.routing_parameter_eq_on_prealgo_off.value)

    def set_routing_parameter(self, value):
        if self.routing_live_parameter.value != value:
            self.routing_live_parameter.value = value

    def update_convolution_parameters(self):
        convolution_state = ParameterState.enabled if self.routing_live_parameter.value != 2 else ParameterState.disabled
        self.ir_post_processing_bool.state = convolution_state
        self.ir_category_list_parameter.state = convolution_state
        self.ir_file_list_parameter.state = convolution_state
        shape_state = ParameterState.enabled if self.ir_post_processing_bool.value and self.routing_live_parameter.value != 2 else ParameterState.disabled
        self.ir_attack_time_parameter.state = shape_state
        self.ir_decay_time_parameter.state = shape_state
        self.ir_size_factor_parameter.state = shape_state


class HybridReverbDeviceComponent(DeviceComponentWithTrackColorViewData):
    FILTER_VISUALISATION_CONFIGURATION_IN_EQ = {4: ButtonRange(0, 7)}
    FILTER_VISUALISATION_CONFIGURATION_IN_MAIN = {0: ButtonRange(2, 6)}
    IR_VISUALISATION_CONFIGURATION_IN_IR = {1: ButtonRange(0, 4)}
    IR_VISUALISATION_CONFIGURATION_IN_MAIN = {0: ButtonRange(2, 6)}
    LOW_BAND_PARAMETERS_NAME = re.compile(u'Low')
    PEAK_2_PARAMETERS_NAME = re.compile(u'2')
    PEAK_3_PARAMETERS_NAME = re.compile(u'3')
    HIGH_BAND_PARAMETERS_NAME = re.compile(u'High')

    def _parameter_touched(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    def _parameter_released(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    @property
    def _adjustment_view_data(self):
        active_filter_index = -1
        low_and_high_band_is_selected = True
        ir_is_active = False
        eq_is_active = False
        if self._bank.index == 1:
            ir_is_active = True
        elif self._bank.index == 4:
            eq_is_active = True
        elif self._bank.index == 0 and self._decorated_device.main_section.value == 0:
            ir_is_active = True
        elif self._bank.index == 0 and self._decorated_device.main_section.value == 3:
            eq_is_active = True
        if self._bank.index == 4 and self._decorated_device.band.value == 1:
            low_and_high_band_is_selected = False
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        for parameter in touched_parameters:
            if self.LOW_BAND_PARAMETERS_NAME.search(parameter.name) is not None:
                active_filter_index = 1
            elif self.PEAK_2_PARAMETERS_NAME.search(parameter.name) is not None:
                active_filter_index = 2
            elif self.PEAK_3_PARAMETERS_NAME.search(parameter.name) is not None:
                active_filter_index = 3
            elif self.HIGH_BAND_PARAMETERS_NAME.search(parameter.name) is not None:
                active_filter_index = 4

        return {u'ActiveBandIndex': active_filter_index,
         u'LowAndHighBandIsSelected': low_and_high_band_is_selected,
         u'IrIsActive': ir_is_active,
         u'EqIsActive': eq_is_active}

    def _set_bank_index(self, bank):
        super(HybridReverbDeviceComponent, self)._set_bank_index(bank)
        self._update_visualisation_view_data(self._configuration_view_data)
        self._update_visualisation_view_data(self._adjustment_view_data)
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    def _set_decorated_device(self, decorated_device):
        super(HybridReverbDeviceComponent, self)._set_decorated_device(decorated_device)
        self.on_main_bank_section_change.subject = self._decorated_device._main_section_provider
        self.on_eq_band_parameter_change.subject = self._decorated_device.band

    @property
    def _visualisation_visible(self):
        return self._bank.index in self.FILTER_VISUALISATION_CONFIGURATION_IN_EQ or self._bank.index in self.FILTER_VISUALISATION_CONFIGURATION_IN_MAIN and self._decorated_device.main_section.value == 3 or self._bank.index in self.IR_VISUALISATION_CONFIGURATION_IN_IR or self._bank.index in self.IR_VISUALISATION_CONFIGURATION_IN_MAIN and self._decorated_device.main_section.value == 0

    @property
    def _shrink_parameters(self):
        if self._visualisation_visible:
            filter_config = self.FILTER_VISUALISATION_CONFIGURATION_IN_EQ.get(self._bank.index, ButtonRange(-1, -1))
            filter_config_main = self.FILTER_VISUALISATION_CONFIGURATION_IN_MAIN.get(self._bank.index, ButtonRange(-1, -1))
            ir_config_main = self.IR_VISUALISATION_CONFIGURATION_IN_MAIN.get(self._bank.index, ButtonRange(-1, -1))
            ir_config = self.IR_VISUALISATION_CONFIGURATION_IN_IR.get(self._bank.index, ButtonRange(-1, -1))
            return [ filter_config.left_index <= index <= filter_config.right_index or filter_config_main.left_index <= index <= filter_config_main.right_index or ir_config_main.left_index <= index <= ir_config_main.right_index or ir_config.left_index <= index <= ir_config.right_index for index in range(8) ]
        else:
            return [False] * 8

    @property
    def _configuration_view_data(self):
        if self._bank.index == 0 and self._decorated_device.main_section.value == 3:
            range_left, range_right = self._calculate_view_size(self.FILTER_VISUALISATION_CONFIGURATION_IN_MAIN)
        elif self._bank.index == 0 and self._decorated_device.main_section.value == 0:
            range_left, range_right = self._calculate_view_size(self.IR_VISUALISATION_CONFIGURATION_IN_MAIN)
        elif self._bank.index == 1:
            range_left, range_right = self._calculate_view_size(self.IR_VISUALISATION_CONFIGURATION_IN_IR)
        else:
            range_left, range_right = self._calculate_view_size(self.FILTER_VISUALISATION_CONFIGURATION_IN_EQ)
        return {u'RangeLeft': range_left,
         u'RangeRight': range_right}

    def _initial_visualisation_view_data(self):
        view_data = super(HybridReverbDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._configuration_view_data)
        view_data.update(self._adjustment_view_data)
        return view_data

    def _calculate_view_size(self, configuration):
        if self._bank.index not in configuration:
            return (0, 0)
        config = configuration[self._bank.index]
        return (VisualisationGuides.light_left_x(config.left_index), VisualisationGuides.light_right_x(config.right_index))

    @listens(u'index')
    def on_main_bank_section_change(self):
        self._update_visualisation_view_data(self._configuration_view_data)
        self._update_visualisation_view_data(self._adjustment_view_data)
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    @listens(u'value')
    def on_eq_band_parameter_change(self):
        if self._bank.index == 4 and self._decorated_device.band.value == 1:
            self._update_visualisation_view_data({u'LowAndHighBandIsSelected': False})
        else:
            self._update_visualisation_view_data({u'LowAndHighBandIsSelecteda_': True})
