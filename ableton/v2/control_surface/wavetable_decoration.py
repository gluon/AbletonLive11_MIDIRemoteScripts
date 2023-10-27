# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\wavetable_decoration.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 11883 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ..base import EventObject, listens, liveobj_valid
from .decoration import LiveObjectDecorator, NotifyingList, PitchParameter, get_parameter_by_name
from .internal_parameter import EnumWrappingParameter, IntegerParameter
ParameterState = Live.DeviceParameter.ParameterState

class WavetableEnvelopeType(int):
    pass


WavetableEnvelopeType.amp = WavetableEnvelopeType(0)
WavetableEnvelopeType.env2 = WavetableEnvelopeType(1)
WavetableEnvelopeType.env3 = WavetableEnvelopeType(2)

class WavetableLfoType(int):
    pass


WavetableLfoType.one = WavetableLfoType(0)
WavetableLfoType.two = WavetableLfoType(1)

class WavetableEnvelopeViewType(int):
    pass


WavetableEnvelopeViewType.time = WavetableEnvelopeViewType(0)
WavetableEnvelopeViewType.slope = WavetableEnvelopeViewType(1)
WavetableEnvelopeViewType.value = WavetableEnvelopeViewType(2)

class WavetableOscillatorType(int):
    pass


WavetableOscillatorType.one = WavetableOscillatorType(0)
WavetableOscillatorType.two = WavetableOscillatorType(1)
WavetableOscillatorType.s = WavetableOscillatorType(2)
WavetableOscillatorType.mix = WavetableOscillatorType(3)

class WavetableFilterType(int):
    pass


WavetableFilterType.one = WavetableFilterType(0)
WavetableFilterType.two = WavetableFilterType(1)

class WavetableDeviceDecorator(LiveObjectDecorator, EventObject):
    MIN_UNISON_VOICE_COUNT = 2
    MAX_UNISON_VOICE_COUNT = 8
    available_effect_modes = ('None', 'Fm', 'Classic', 'Modern')
    available_unison_modes = ('None', 'Classic', 'Shimmer', 'Noise', 'Phase Sync',
                              'Position Spread', 'Random Note')
    mono_off_on_values = ('Off', 'On')
    poly_voices_values = ('2', '3', '4', '5', '6', '7', '8')
    available_filter_routings = ('Serial', 'Parallel', 'Split')

    def __init__(self, *a, **k):
        (super(WavetableDeviceDecorator, self).__init__)(*a, **k)
        self._osc_types_provider = NotifyingList(available_values=[
         '1', '2', 'S', 'Mix'],
          default_value=(WavetableOscillatorType.one))
        self._filter_types_provider = NotifyingList(available_values=[
         '1', '2'],
          default_value=(WavetableFilterType.one))
        self._envelope_types_provider = NotifyingList(available_values=[
         'Amp', 'Env2', 'Env3'],
          default_value=(WavetableEnvelopeType.amp))
        self._lfo_types_provider = NotifyingList(available_values=[
         'LFO1', 'LFO2'],
          default_value=(WavetableLfoType.one))
        self._amp_envelope_view_types_provider = NotifyingList(available_values=[
         'Time', 'Slope'],
          default_value=(WavetableEnvelopeViewType.time))
        self._mod_envelope_view_types_provider = NotifyingList(available_values=[
         'Time', 'Slope', 'Value'],
          default_value=(WavetableEnvelopeViewType.time))
        self._additional_parameters = self._create_parameters()
        self.register_disconnectables(self._additional_parameters)
        self._osc_1_on_parameter = get_parameter_by_name(self, 'Osc 1 On')
        self._osc_2_on_parameter = get_parameter_by_name(self, 'Osc 2 On')
        self._WavetableDeviceDecorator__on_osc_1_on_value_changed.subject = self._osc_1_on_parameter
        self._WavetableDeviceDecorator__on_osc_1_on_value_changed()
        self._WavetableDeviceDecorator__on_osc_2_on_value_changed.subject = self._osc_2_on_parameter
        self._WavetableDeviceDecorator__on_osc_2_on_value_changed()

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    def _create_parameters(self):
        self.oscillator_switch = EnumWrappingParameter(name='Oscillator',
          parent=self,
          values_host=(self._osc_types_provider),
          index_property_host=(self._osc_types_provider),
          values_property='available_values',
          index_property='index',
          value_type=WavetableOscillatorType)
        self.osc_1_pitch = PitchParameter(name='Osc 1 Pitch',
          parent=self,
          integer_value_host=(get_parameter_by_name(self, 'Osc 1 Transp')),
          decimal_value_host=(get_parameter_by_name(self, 'Osc 1 Detune')))
        self.osc_2_pitch = PitchParameter(name='Osc 2 Pitch',
          parent=self,
          integer_value_host=(get_parameter_by_name(self, 'Osc 2 Transp')),
          decimal_value_host=(get_parameter_by_name(self, 'Osc 2 Detune')))
        self.envelope_switch = EnumWrappingParameter(name='Envelopes',
          parent=self,
          values_host=(self._envelope_types_provider),
          index_property_host=(self._envelope_types_provider),
          values_property='available_values',
          index_property='index',
          value_type=WavetableEnvelopeType)
        self.lfo_switch = EnumWrappingParameter(name='LFO',
          parent=self,
          values_host=(self._lfo_types_provider),
          index_property_host=(self._lfo_types_provider),
          values_property='available_values',
          index_property='index',
          value_type=WavetableLfoType)
        self._osc_1_category_switch = EnumWrappingParameter(name='Osc 1 Category',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='oscillator_wavetable_categories',
          index_property='oscillator_1_wavetable_category')
        self._osc_2_category_switch = EnumWrappingParameter(name='Osc 2 Category',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='oscillator_wavetable_categories',
          index_property='oscillator_2_wavetable_category')
        self._osc_1_table_switch = EnumWrappingParameter(name='Osc 1 Table',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='oscillator_1_wavetables',
          index_property='oscillator_1_wavetable_index')
        self._osc_2_table_switch = EnumWrappingParameter(name='Osc 2 Table',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='oscillator_2_wavetables',
          index_property='oscillator_2_wavetable_index')
        self._osc_1_effect_type_switch = EnumWrappingParameter(name='Osc 1 Effect Type',
          parent=self,
          values_host=self,
          index_property_host=self,
          values_property='available_effect_modes',
          index_property='oscillator_1_effect_mode')
        self._osc_2_effect_type_switch = EnumWrappingParameter(name='Osc 2 Effect Type',
          parent=self,
          values_host=self,
          index_property_host=self,
          values_property='available_effect_modes',
          index_property='oscillator_2_effect_mode')
        return (
         EnumWrappingParameter(name='Filter',
           parent=self,
           values_host=(self._filter_types_provider),
           index_property_host=(self._filter_types_provider),
           values_property='available_values',
           index_property='index',
           value_type=WavetableFilterType),
         EnumWrappingParameter(name='Amp Env View',
           parent=self,
           values_host=(self._amp_envelope_view_types_provider),
           index_property_host=(self._amp_envelope_view_types_provider),
           values_property='available_values',
           index_property='index',
           value_type=WavetableEnvelopeViewType),
         EnumWrappingParameter(name='Mod Env View',
           parent=self,
           values_host=(self._mod_envelope_view_types_provider),
           index_property_host=(self._mod_envelope_view_types_provider),
           values_property='available_values',
           index_property='index',
           value_type=WavetableEnvelopeViewType),
         EnumWrappingParameter(name='Unison Mode',
           parent=self,
           values_host=self,
           index_property_host=self,
           values_property='available_unison_modes',
           index_property='unison_mode'),
         IntegerParameter(name='Unison Voices',
           parent=self,
           integer_value_host=(self._live_object),
           integer_value_property_name='unison_voice_count',
           min_value=(self.MIN_UNISON_VOICE_COUNT),
           max_value=(self.MAX_UNISON_VOICE_COUNT),
           show_as_quantized=True),
         EnumWrappingParameter(name='Mono On',
           parent=self,
           values_host=self,
           index_property_host=self,
           values_property='mono_off_on_values',
           index_property='mono_poly',
           to_index_conversion=(lambda index: int(not index)
),
           from_index_conversion=(lambda index: int(not index)
)),
         EnumWrappingParameter(name='Poly Voices',
           parent=self,
           values_host=self,
           index_property_host=self,
           values_property='poly_voices_values',
           index_property='poly_voices'),
         EnumWrappingParameter(name='Filter Routing',
           parent=self,
           values_host=self,
           index_property_host=self,
           values_property='available_filter_routings',
           index_property='filter_routing')) + (
         self.oscillator_switch,
         self.osc_1_pitch,
         self.osc_2_pitch,
         self.envelope_switch,
         self.lfo_switch,
         self._osc_1_category_switch,
         self._osc_2_category_switch,
         self._osc_1_table_switch,
         self._osc_2_table_switch,
         self._osc_1_effect_type_switch,
         self._osc_2_effect_type_switch)

    def _get_parameter_enabled_state(self, parameter):
        if parameter.value:
            return ParameterState.enabled
        return ParameterState.disabled

    @listens('value')
    def __on_osc_1_on_value_changed(self):
        if liveobj_valid(self._osc_1_on_parameter):
            state = self._get_parameter_enabled_state(self._osc_1_on_parameter)
            self._osc_1_category_switch.state = state
            self._osc_1_table_switch.state = state
            self._osc_1_effect_type_switch.state = state
            self.osc_1_pitch.state = state

    @listens('value')
    def __on_osc_2_on_value_changed(self):
        if liveobj_valid(self._osc_2_on_parameter):
            state = self._get_parameter_enabled_state(self._osc_2_on_parameter)
            self._osc_2_category_switch.state = state
            self._osc_2_table_switch.state = state
            self._osc_2_effect_type_switch.state = state
            self.osc_2_pitch.state = state