# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\hybrid_reverb.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 22346 bytes
from __future__ import absolute_import, print_function, unicode_literals
import math, re, Live
from ableton.v2.base import EventObject, clamp, listens
from ableton.v2.control_surface import BoolWrappingParameter, EnumWrappingParameter, LiveObjectDecorator, NotifyingList, WrappingParameter, get_parameter_by_name
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .device_options import DeviceOnOffOption, DeviceSwitchOption
from .visualisation_settings import VisualisationGuides
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
    format_str = '%.0f'
    percentage_str = format_str % percentage
    return percentage_str + ' %'


def to_ms_display(value):
    format = '%.2f'
    if value < 0.9995:
        value = value * 1000
        if value < 10:
            format = '%.2f'
        else:
            if value < 100:
                format = '%.1f'
            else:
                if value < 1000:
                    format = '%.0f'
        out_str = str(format % value) + ' ms'
    else:
        if value < 10:
            format = '%.2f'
        else:
            if value < 100:
                format = '%.1f'
            else:
                format = '%.0f'
        out_str = str(format % value) + ' s'
    return out_str


class HybridReverbDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        (super(HybridReverbDeviceDecorator, self).__init__)(*a, **k)
        self.main_section_labels = [
         'Convolution', 'Algo', 'Mix', 'EQ']
        self.routing_full_labels = ['Serial', 'Parallel', 'Algorithm', 'Convolution']
        self.routing_option_labels = ['Ser.', 'Par.', 'Alg.', 'Cv.']
        self.vintage_labels = ['Off','Subtle','Old','Older','Extreme']
        self.band_names_labels = ['1&4', '2&3']
        self.pre_delay_sync_labels = ['Ms', 'Sync']
        self.filter_types_labels = ['Cut', 'Shelf']
        self.routing_live_parameter = get_parameter_by_name(self, 'Routing')
        self.vintage_live_parameter = get_parameter_by_name(self, 'Vintage')
        self.pre_delay_sync_live_parameter = get_parameter_by_name(self, 'P.Dly Sync')
        self.eq_low_type_live_parameter = get_parameter_by_name(self, 'EQ Low Type')
        self.eq_high_type_live_parameter = get_parameter_by_name(self, 'EQ High Type')
        self.eq_on_live_parameter = get_parameter_by_name(self, 'EQ On')
        self.freeze_live_parameter = get_parameter_by_name(self, 'Freeze')
        self.freeze_in_live_parameter = get_parameter_by_name(self, 'Freeze In')
        self.eq_prealgo_live_parameter = get_parameter_by_name(self, 'EQ Pre Algo')
        self.bass_mono_live_parameter = get_parameter_by_name(self, 'Bass Mono')
        self._band_names_provider = NotifyingList(available_values=(self.band_names_labels),
          default_value=0)
        self.band = EnumWrappingParameter(name='Band',
          parent=self,
          values_host=(self._band_names_provider),
          index_property_host=(self._band_names_provider),
          values_property='available_values',
          index_property='index')
        self._main_section_provider = NotifyingList(available_values=(self.main_section_labels),
          default_value=0)
        self.main_section = EnumWrappingParameter(name='Section',
          parent=self,
          values_host=(self._main_section_provider),
          index_property_host=(self._main_section_provider),
          values_property='available_values',
          index_property='index')
        self.feedback_ms_sync_switch = DeviceSwitchOption(name='Ms Sync Switch',
          parameter=(self.pre_delay_sync_live_parameter),
          labels=(self.pre_delay_sync_labels))
        self.eq_low_type_switch = DeviceSwitchOption(name='Low Type Switch',
          parameter=(self.eq_low_type_live_parameter),
          labels=(self.filter_types_labels))
        self.eq_high_type_switch = DeviceSwitchOption(name='High Type Switch',
          parameter=(self.eq_high_type_live_parameter),
          labels=(self.filter_types_labels))
        self.ir_post_processing_bool = BoolWrappingParameter(name='Ir Post Processing Bool',
          parent=self,
          property_host=self,
          source_property='ir_time_shaping_on')
        self.ir_post_processing_option = DeviceOnOffOption(name='Shape',
          property_host=(self.ir_post_processing_bool))
        self.eq_on_option = DeviceOnOffOption(name='EQ',
          property_host=(self.eq_on_live_parameter))
        self.freeze_option = DeviceOnOffOption(name='Freeze',
          property_host=(self.freeze_live_parameter))
        self.freeze_in_option = DeviceOnOffOption(name='Freeze In',
          property_host=(self.freeze_in_live_parameter))
        self.prealgo_option = DeviceOnOffOption(name='Pre Algo',
          property_host=(self.eq_prealgo_live_parameter))
        self.bass_mono_option = DeviceOnOffOption(name='Bass Mono',
          property_host=(self.bass_mono_live_parameter))
        self.ir_attack_time_parameter = WrappingParameter(name='Ir Attack Time',
          parent=self,
          property_host=self,
          source_property='ir_attack_time',
          display_value_conversion=to_ms_display,
          from_property_value=(user_to_linear_exp(0.0, 3.0, 3.33)),
          to_property_value=(linear_to_user_exp(0.0, 3.0, 3.33)))
        self.ir_decay_time_parameter = WrappingParameter(name='Ir Decay Time',
          parent=self,
          property_host=self,
          source_property='ir_decay_time',
          display_value_conversion=to_ms_display,
          from_property_value=(user_to_linear_exp(0.02, 20.0, 3.33)),
          to_property_value=(linear_to_user_exp(0.02, 20.0, 3.33)))
        self.ir_size_factor_parameter = WrappingParameter(name='Ir Size Factor',
          parent=self,
          property_host=self,
          source_property='ir_size_factor',
          display_value_conversion=to_percentage_display,
          from_property_value=(user_to_linear_log(0.2, 5.0)),
          to_property_value=(linear_to_user_log(0.2, 5.0)))
        self.ir_category_list_parameter = EnumWrappingParameter(name='IR Category',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='ir_category_list',
          index_property='ir_category_index')
        self.ir_file_list_parameter = EnumWrappingParameter(name='IR',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='ir_file_list',
          index_property='ir_file_index')
        self.vintage_enum_copy = NotifyingList(available_values=(self.vintage_labels),
          default_value=0)
        self.vintage_parameter_copy = EnumWrappingParameter(name='Vintage Copy',
          parent=self,
          values_host=(self.vintage_enum_copy),
          index_property_host=(self.vintage_enum_copy),
          values_property='available_values',
          index_property='index')
        self.routing_parameter_enum = NotifyingList(available_values=(self.routing_full_labels),
          default_value=0)
        self.routing_parameter_eq_off = EnumWrappingParameter(name='Routing Eq Off',
          parent=self,
          values_host=(self.routing_parameter_enum),
          index_property_host=(self.routing_parameter_enum),
          values_property='available_values',
          index_property='index')
        self.routing_parameter_eq_on_prealgo_off = EnumWrappingParameter(name='Routing Eq On PreAlgo Off',
          parent=self,
          values_host=(self.routing_parameter_enum),
          index_property_host=(self.routing_parameter_enum),
          values_property='available_values',
          index_property='index')
        self.routing_parameter_eq_on_prealgo_on = EnumWrappingParameter(name='Routing Eq On PreAlgo On',
          parent=self,
          values_host=(self.routing_parameter_enum),
          index_property_host=(self.routing_parameter_enum),
          values_property='available_values',
          index_property='index')
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
        self._additional_parameters = (
         self.band,
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
        self._additional_options = (
         self.feedback_ms_sync_switch,
         self.eq_low_type_switch,
         self.eq_high_type_switch,
         self.eq_on_option,
         self.ir_post_processing_option,
         self.freeze_option,
         self.freeze_in_option,
         self.prealgo_option,
         self.bass_mono_option)
        self.register_disconnectables(self._additional_parameters + self._additional_options)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    @property
    def options(self):
        return self._additional_options

    @listens('value')
    def on_vintage_parameter_change(self):
        self.vintage_parameter_copy.value = self.vintage_live_parameter.value

    @listens('value')
    def on_vintage_copy_parameter_change(self):
        if self.vintage_parameter_copy.value != self.vintage_live_parameter.value:
            self.vintage_live_parameter.value = self.vintage_parameter_copy.value

    @listens('value')
    def on_shape_option_change(self):
        self.update_convolution_parameters()

    @listens('value')
    def on_routing_parameter_change(self):
        self.routing_parameter_eq_off.value = self.routing_live_parameter.value
        self.routing_parameter_eq_on_prealgo_on.value = self.routing_live_parameter.value
        self.routing_parameter_eq_on_prealgo_off.value = self.routing_live_parameter.value
        self.update_convolution_parameters()

    @listens('value')
    def on_routing_parameter_eq_off_change(self):
        self.set_routing_parameter(self.routing_parameter_eq_off.value)

    @listens('value')
    def on_routing_parameter_eq_on_prealgo_on_change(self):
        self.set_routing_parameter(self.routing_parameter_eq_on_prealgo_on.value)

    @listens('value')
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
        shape_state = ParameterState.enabled if (self.ir_post_processing_bool.value) and (self.routing_live_parameter.value != 2) else (ParameterState.disabled)
        self.ir_attack_time_parameter.state = shape_state
        self.ir_decay_time_parameter.state = shape_state
        self.ir_size_factor_parameter.state = shape_state


class HybridReverbDeviceComponent(DeviceComponentWithTrackColorViewData):
    FILTER_VISUALISATION_CONFIGURATION_IN_EQ = {4: ButtonRange(0, 7)}
    FILTER_VISUALISATION_CONFIGURATION_IN_MAIN = {0: ButtonRange(1, 5)}
    IR_VISUALISATION_CONFIGURATION_IN_IR = {1: ButtonRange(0, 4)}
    IR_VISUALISATION_CONFIGURATION_IN_MAIN = {0: ButtonRange(1, 5)}
    LOW_BAND_PARAMETERS_NAME = re.compile('Low')
    PEAK_2_PARAMETERS_NAME = re.compile('2')
    PEAK_3_PARAMETERS_NAME = re.compile('3')
    HIGH_BAND_PARAMETERS_NAME = re.compile('High')

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
        else:
            if self._bank.index == 4:
                eq_is_active = True
            else:
                if self._bank.index == 0 and self._decorated_device.main_section.value == 0:
                    ir_is_active = True
                else:
                    if self._bank.index == 0:
                        if self._decorated_device.main_section.value == 3:
                            eq_is_active = True
        if self._bank.index == 4:
            if self._decorated_device.band.value == 1:
                low_and_high_band_is_selected = False
        touched_parameters = [self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed]
        for parameter in touched_parameters:
            if self.LOW_BAND_PARAMETERS_NAME.search(parameter.name) is not None:
                active_filter_index = 1
            else:
                if self.PEAK_2_PARAMETERS_NAME.search(parameter.name) is not None:
                    active_filter_index = 2
                else:
                    if self.PEAK_3_PARAMETERS_NAME.search(parameter.name) is not None:
                        active_filter_index = 3
            if self.HIGH_BAND_PARAMETERS_NAME.search(parameter.name) is not None:
                active_filter_index = 4

        return { 'ActiveBandIndex': active_filter_index,
          'LowAndHighBandIsSelected': low_and_high_band_is_selected,
          'IrIsActive': ir_is_active,
          'EqIsActive': eq_is_active}

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
        return self._bank.index in self.FILTER_VISUALISATION_CONFIGURATION_IN_EQ or (self._bank.index in self.FILTER_VISUALISATION_CONFIGURATION_IN_MAIN) and (self._decorated_device.main_section.value == 3) or (self._bank.index in self.IR_VISUALISATION_CONFIGURATION_IN_IR) or ((self._bank.index in self.IR_VISUALISATION_CONFIGURATION_IN_MAIN) and (self._decorated_device.main_section.value == 0))

    @property
    def _shrink_parameters(self):
        if self._visualisation_visible:
            filter_config = self.FILTER_VISUALISATION_CONFIGURATION_IN_EQ.get(self._bank.index, ButtonRange(-1, -1))
            filter_config_main = self.FILTER_VISUALISATION_CONFIGURATION_IN_MAIN.get(self._bank.index, ButtonRange(-1, -1))
            ir_config_main = self.IR_VISUALISATION_CONFIGURATION_IN_MAIN.get(self._bank.index, ButtonRange(-1, -1))
            ir_config = self.IR_VISUALISATION_CONFIGURATION_IN_IR.get(self._bank.index, ButtonRange(-1, -1))
            return [filter_config.left_index <= index <= filter_config.right_index or filter_config_main.left_index <= index <= filter_config_main.right_index or ir_config_main.left_index <= index <= ir_config_main.right_index or ir_config.left_index <= index <= ir_config.right_index for index in range(8)]
        return [
         False] * 8

    @property
    def _configuration_view_data(self):
        if self._bank.index == 0 and self._decorated_device.main_section.value == 3:
            range_left, range_right = self._calculate_view_size(self.FILTER_VISUALISATION_CONFIGURATION_IN_MAIN)
        else:
            if self._bank.index == 0 and self._decorated_device.main_section.value == 0:
                range_left, range_right = self._calculate_view_size(self.IR_VISUALISATION_CONFIGURATION_IN_MAIN)
            else:
                if self._bank.index == 1:
                    range_left, range_right = self._calculate_view_size(self.IR_VISUALISATION_CONFIGURATION_IN_IR)
                else:
                    range_left, range_right = self._calculate_view_size(self.FILTER_VISUALISATION_CONFIGURATION_IN_EQ)
        return {'RangeLeft':range_left,  'RangeRight':range_right}

    def _initial_visualisation_view_data(self):
        view_data = super(HybridReverbDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._configuration_view_data)
        view_data.update(self._adjustment_view_data)
        return view_data

    def _calculate_view_size(self, configuration):
        if self._bank.index not in configuration:
            return (0, 0)
        config = configuration[self._bank.index]
        return (
         VisualisationGuides.light_left_x(config.left_index),
         VisualisationGuides.light_right_x(config.right_index))

    @listens('index')
    def on_main_bank_section_change(self):
        self._update_visualisation_view_data(self._configuration_view_data)
        self._update_visualisation_view_data(self._adjustment_view_data)
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    @listens('value')
    def on_eq_band_parameter_change(self):
        if self._bank.index == 4 and self._decorated_device.band.value == 1:
            self._update_visualisation_view_data({'LowAndHighBandIsSelected': False})
        else:
            self._update_visualisation_view_data({'LowAndHighBandIsSelecteda_': True})