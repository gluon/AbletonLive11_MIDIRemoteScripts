#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/operator.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from collections import namedtuple
import re
from ableton.v2.base import const, EventObject, listenable_property, listens, liveobj_valid
from ableton.v2.control_surface import EnumWrappingParameter, LiveObjectDecorator, NotifyingList, get_parameter_by_name
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData, extend_with_envelope_features_for_parameter, make_vector
from .device_decoration import DeviceSwitchOption
from .visualisation_settings import VisualisationGuides
BankConfiguration = namedtuple(u'BankConfiguration', [u'name_function', u'button_range'])

class OscillatorType(int):
    pass


OscillatorType.a = OscillatorType(0)
OscillatorType.b = OscillatorType(1)
OscillatorType.c = OscillatorType(2)
OscillatorType.d = OscillatorType(3)

class EnvelopeFeature(int):
    pass


EnvelopeFeature.time = EnvelopeFeature(0)
EnvelopeFeature.level = EnvelopeFeature(1)

class SlopedEnvelopeFeature(int):
    pass


SlopedEnvelopeFeature.time = SlopedEnvelopeFeature(0)
SlopedEnvelopeFeature.slope = SlopedEnvelopeFeature(1)
SlopedEnvelopeFeature.level = SlopedEnvelopeFeature(2)

class OperatorDeviceDecorator(EventObject, LiveObjectDecorator):

    def __init__(self, *a, **k):
        super(OperatorDeviceDecorator, self).__init__(*a, **k)
        self._osc_types_provider = NotifyingList(available_values=[u'A',
         u'B',
         u'C',
         u'D'], default_value=OscillatorType.a)
        self._env_feature_provider = NotifyingList(available_values=[u'Time', u'Level'], default_value=EnvelopeFeature.time)
        self._sloped_env_feature_provider = NotifyingList(available_values=[u'Time', u'Slope', u'Level'], default_value=SlopedEnvelopeFeature.time)
        self.__on_parameters_changed.subject = self._live_object
        self.oscillator = EnumWrappingParameter(name=u'Oscillator', parent=self, values_host=self._osc_types_provider, index_property_host=self._osc_types_provider, values_property=u'available_values', index_property=u'index', value_type=OscillatorType)
        self.env_feature = EnumWrappingParameter(name=u'Envelope Feature Time/Level', parent=self, values_host=self._env_feature_provider, index_property_host=self._env_feature_provider, values_property=u'available_values', index_property=u'index', value_type=EnvelopeFeature)
        self.sloped_env_feature = EnumWrappingParameter(name=u'Envelope Feature Time/Slope/Level', parent=self, values_host=self._sloped_env_feature_provider, index_property_host=self._sloped_env_feature_provider, values_property=u'available_values', index_property=u'index', value_type=SlopedEnvelopeFeature)
        self.__on_oscillator_switch_value_changed.subject = self.oscillator
        self.filter_slope_option = DeviceSwitchOption(name=u'Filter Slope', parameter=get_parameter_by_name(self, u'Filter Slope'))
        self.register_disconnectables(self.options)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + (self.oscillator, self.env_feature, self.sloped_env_feature)

    @property
    def options(self):
        return (self.filter_slope_option,)

    @listens(u'parameters')
    def __on_parameters_changed(self):
        self.filter_slope_option.set_parameter(get_parameter_by_name(self, u'Filter Slope'))

    @listenable_property
    def oscillator_index(self):
        return self._osc_types_provider.index

    @listens(u'value')
    def __on_oscillator_switch_value_changed(self):
        self.notify_oscillator_index()


class OperatorDeviceComponent(DeviceComponentWithTrackColorViewData):
    FILTER_PARAMETER_NAMES = [u'Filter Type', u'Filter Freq', u'Filter Res']
    FILTER_BANK = 2
    LARGE_PARAMETERS_LIST = [False] * 8
    ENVELOPE_PREFIXES = [u'Ae',
     u'Be',
     u'Ce',
     u'De',
     u'Fe',
     u'Le',
     u'Pe']

    def __init__(self, *a, **k):
        super(OperatorDeviceComponent, self).__init__(*a, **k)
        self._bank_configuration = {1: BankConfiguration(lambda : u'Operator%i' % self.selected_oscillator, ButtonRange(3, 6)),
         self.FILTER_BANK: BankConfiguration(const(u'Filter'), ButtonRange(1, 3)),
         3: BankConfiguration(const(u'Filter Env.'), ButtonRange(2, 5)),
         6: BankConfiguration(const(u'LFO'), ButtonRange(2, 5)),
         8: BankConfiguration(const(u'Pitch'), ButtonRange(2, 5))}

    def _parameter_touched(self, parameter):
        self._update_visualisation_view_data(self._envelope_visualisation_data())

    def _parameter_released(self, parameter):
        self._update_visualisation_view_data(self._envelope_visualisation_data())

    def parameters_changed(self):
        self._update_visualisation_view_data(self._envelope_visualisation_data())
        self.notify_shrink_parameters()

    def _set_bank_index(self, bank):
        super(OperatorDeviceComponent, self)._set_bank_index(bank)
        self._update_visualisation_view_data(self._envelope_visualisation_data())
        self.notify_visualisation_visible()

    def _set_decorated_device(self, decorated_device):
        super(OperatorDeviceComponent, self)._set_decorated_device(decorated_device)
        self.__on_selected_oscillator_changed.subject = decorated_device

    @property
    def selected_oscillator(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.oscillator_index
        return 0

    def _initial_visualisation_view_data(self):
        view_data = super(OperatorDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._envelope_visualisation_data())
        return view_data

    def _envelope_visualisation_data(self):
        config = self._bank_configuration.get(self._bank.index, BankConfiguration(const(u''), ButtonRange(0, 0)))
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        shown_features = set([u'AttackLine',
         u'DecayLine',
         u'SustainLine',
         u'ReleaseLine'])
        for parameter_info in self.parameters:
            extend_with_envelope_features_for_parameter(shown_features, parameter_info.parameter, self.ENVELOPE_PREFIXES)

        focused_features = set()
        for parameter_info in touched_parameters:
            extend_with_envelope_features_for_parameter(focused_features, parameter_info.parameter, self.ENVELOPE_PREFIXES)

        return {u'EnvelopeName': config.name_function(),
         u'EnvelopeLeft': VisualisationGuides.light_left_x(config.button_range.left_index),
         u'EnvelopeRight': VisualisationGuides.light_right_x(config.button_range.right_index),
         u'EnvelopeShow': make_vector(list(shown_features)),
         u'EnvelopeFocus': make_vector(list(focused_features)),
         u'FilterVisible': self._should_show_filter_visualisation(),
         u'FilterLeft': VisualisationGuides.light_left_x(1),
         u'FilterRight': VisualisationGuides.light_right_x(3),
         u'FilterFocus': self._is_filter_parameter_touched()}

    def _is_filter_parameter_touched(self):
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        return any([ parameter.parameter.name in self.FILTER_PARAMETER_NAMES for parameter in touched_parameters if liveobj_valid(parameter.parameter) ])

    def _has_legacy_filter(self):
        parameter_names = [ parameter.name for parameter in self._decorated_device.parameters ]
        return u'Filter Type (Legacy)' in parameter_names

    def _should_show_filter_visualisation(self):
        return not self._has_legacy_filter() and self._bank.index == self.FILTER_BANK

    @listens(u'oscillator_index')
    def __on_selected_oscillator_changed(self):
        self._update_visualisation_view_data(self._envelope_visualisation_data())

    @property
    def _visualisation_visible(self):
        return self._bank != None and self._bank.index in self._bank_configuration and not (self._bank.index == self.FILTER_BANK and self._has_legacy_filter())

    @property
    def _shrink_parameters(self):
        if self._visualisation_visible:
            config = self._bank_configuration[self._bank.index]
            return [ config.button_range.left_index <= index <= config.button_range.right_index for index in range(8) ]
        return self.LARGE_PARAMETERS_LIST
