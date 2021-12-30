#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/wavetable_decoration.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
ParameterState = Live.DeviceParameter.ParameterState
from ..base import EventObject, listens, liveobj_valid
from .decoration import LiveObjectDecorator, NotifyingList, PitchParameter, get_parameter_by_name
from .internal_parameter import EnumWrappingParameter, IntegerParameter

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
    available_effect_modes = (u'None', u'Fm', u'Classic', u'Modern')
    available_unison_modes = (u'None', u'Classic', u'Shimmer', u'Noise', u'Phase Sync', u'Position Spread', u'Random Note')
    mono_off_on_values = (u'Off', u'On')
    poly_voices_values = (u'2', u'3', u'4', u'5', u'6', u'7', u'8')
    available_filter_routings = (u'Serial', u'Parallel', u'Split')

    def __init__(self, *a, **k):
        super(WavetableDeviceDecorator, self).__init__(*a, **k)
        self._osc_types_provider = NotifyingList(available_values=[u'1',
         u'2',
         u'S',
         u'Mix'], default_value=WavetableOscillatorType.one)
        self._filter_types_provider = NotifyingList(available_values=[u'1', u'2'], default_value=WavetableFilterType.one)
        self._envelope_types_provider = NotifyingList(available_values=[u'Amp', u'Env2', u'Env3'], default_value=WavetableEnvelopeType.amp)
        self._lfo_types_provider = NotifyingList(available_values=[u'LFO1', u'LFO2'], default_value=WavetableLfoType.one)
        self._amp_envelope_view_types_provider = NotifyingList(available_values=[u'Time', u'Slope'], default_value=WavetableEnvelopeViewType.time)
        self._mod_envelope_view_types_provider = NotifyingList(available_values=[u'Time', u'Slope', u'Value'], default_value=WavetableEnvelopeViewType.time)
        self._additional_parameters = self._create_parameters()
        self.register_disconnectables(self._additional_parameters)
        self._osc_1_on_parameter = get_parameter_by_name(self, u'Osc 1 On')
        self._osc_2_on_parameter = get_parameter_by_name(self, u'Osc 2 On')
        self.__on_osc_1_on_value_changed.subject = self._osc_1_on_parameter
        self.__on_osc_1_on_value_changed()
        self.__on_osc_2_on_value_changed.subject = self._osc_2_on_parameter
        self.__on_osc_2_on_value_changed()

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    def _create_parameters(self):
        self.oscillator_switch = EnumWrappingParameter(name=u'Oscillator', parent=self, values_host=self._osc_types_provider, index_property_host=self._osc_types_provider, values_property=u'available_values', index_property=u'index', value_type=WavetableOscillatorType)
        self.osc_1_pitch = PitchParameter(name=u'Osc 1 Pitch', parent=self, integer_value_host=get_parameter_by_name(self, u'Osc 1 Transp'), decimal_value_host=get_parameter_by_name(self, u'Osc 1 Detune'))
        self.osc_2_pitch = PitchParameter(name=u'Osc 2 Pitch', parent=self, integer_value_host=get_parameter_by_name(self, u'Osc 2 Transp'), decimal_value_host=get_parameter_by_name(self, u'Osc 2 Detune'))
        self.envelope_switch = EnumWrappingParameter(name=u'Envelopes', parent=self, values_host=self._envelope_types_provider, index_property_host=self._envelope_types_provider, values_property=u'available_values', index_property=u'index', value_type=WavetableEnvelopeType)
        self.lfo_switch = EnumWrappingParameter(name=u'LFO', parent=self, values_host=self._lfo_types_provider, index_property_host=self._lfo_types_provider, values_property=u'available_values', index_property=u'index', value_type=WavetableLfoType)
        self._osc_1_category_switch = EnumWrappingParameter(name=u'Osc 1 Category', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'oscillator_wavetable_categories', index_property=u'oscillator_1_wavetable_category')
        self._osc_2_category_switch = EnumWrappingParameter(name=u'Osc 2 Category', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'oscillator_wavetable_categories', index_property=u'oscillator_2_wavetable_category')
        self._osc_1_table_switch = EnumWrappingParameter(name=u'Osc 1 Table', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'oscillator_1_wavetables', index_property=u'oscillator_1_wavetable_index')
        self._osc_2_table_switch = EnumWrappingParameter(name=u'Osc 2 Table', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'oscillator_2_wavetables', index_property=u'oscillator_2_wavetable_index')
        self._osc_1_effect_type_switch = EnumWrappingParameter(name=u'Osc 1 Effect Type', parent=self, values_host=self, index_property_host=self, values_property=u'available_effect_modes', index_property=u'oscillator_1_effect_mode')
        self._osc_2_effect_type_switch = EnumWrappingParameter(name=u'Osc 2 Effect Type', parent=self, values_host=self, index_property_host=self, values_property=u'available_effect_modes', index_property=u'oscillator_2_effect_mode')
        return (EnumWrappingParameter(name=u'Filter', parent=self, values_host=self._filter_types_provider, index_property_host=self._filter_types_provider, values_property=u'available_values', index_property=u'index', value_type=WavetableFilterType),
         EnumWrappingParameter(name=u'Amp Env View', parent=self, values_host=self._amp_envelope_view_types_provider, index_property_host=self._amp_envelope_view_types_provider, values_property=u'available_values', index_property=u'index', value_type=WavetableEnvelopeViewType),
         EnumWrappingParameter(name=u'Mod Env View', parent=self, values_host=self._mod_envelope_view_types_provider, index_property_host=self._mod_envelope_view_types_provider, values_property=u'available_values', index_property=u'index', value_type=WavetableEnvelopeViewType),
         EnumWrappingParameter(name=u'Unison Mode', parent=self, values_host=self, index_property_host=self, values_property=u'available_unison_modes', index_property=u'unison_mode'),
         IntegerParameter(name=u'Unison Voices', parent=self, integer_value_host=self._live_object, integer_value_property_name=u'unison_voice_count', min_value=self.MIN_UNISON_VOICE_COUNT, max_value=self.MAX_UNISON_VOICE_COUNT, show_as_quantized=True),
         EnumWrappingParameter(name=u'Mono On', parent=self, values_host=self, index_property_host=self, values_property=u'mono_off_on_values', index_property=u'mono_poly', to_index_conversion=lambda index: int(not index), from_index_conversion=lambda index: int(not index)),
         EnumWrappingParameter(name=u'Poly Voices', parent=self, values_host=self, index_property_host=self, values_property=u'poly_voices_values', index_property=u'poly_voices'),
         EnumWrappingParameter(name=u'Filter Routing', parent=self, values_host=self, index_property_host=self, values_property=u'available_filter_routings', index_property=u'filter_routing')) + (self.oscillator_switch,
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

    @listens(u'value')
    def __on_osc_1_on_value_changed(self):
        if liveobj_valid(self._osc_1_on_parameter):
            state = self._get_parameter_enabled_state(self._osc_1_on_parameter)
            self._osc_1_category_switch.state = state
            self._osc_1_table_switch.state = state
            self._osc_1_effect_type_switch.state = state
            self.osc_1_pitch.state = state

    @listens(u'value')
    def __on_osc_2_on_value_changed(self):
        if liveobj_valid(self._osc_2_on_parameter):
            state = self._get_parameter_enabled_state(self._osc_2_on_parameter)
            self._osc_2_category_switch.state = state
            self._osc_2_table_switch.state = state
            self._osc_2_effect_type_switch.state = state
            self.osc_2_pitch.state = state
