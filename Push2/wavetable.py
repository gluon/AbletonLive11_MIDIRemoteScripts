# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\wavetable.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 33112 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import re, Live
AutomationState = Live.DeviceParameter.AutomationState
ModulationSource = Live.WavetableDevice.ModulationSource
from ableton.v2.base import const, find_if, listenable_property, listens, liveobj_valid
from ableton.v2.control_surface import EnumWrappingParameter, InternalParameter, InternalParameterBase, Layer, PitchParameter
from ableton.v2.control_surface import WavetableDeviceDecorator as WavetableDeviceDecoratorBase
from ableton.v2.control_surface import WavetableEnvelopeType, WavetableFilterType, WavetableLfoType, WavetableOscillatorType, get_parameter_by_name
from pushbase.actions import DeleteAndReturnToDefaultComponent
from pushbase.consts import MessageBoxText
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData, extend_with_envelope_features_for_parameter, make_vector
from .device_decoration import IndexProvider, ModMatrixParameter
from .device_options import DeviceOnOffOption, DeviceSwitchOption, DeviceTriggerOption
from .visualisation_settings import VisualisationGuides

class WavetableDeviceDecorator(WavetableDeviceDecoratorBase):
    __events__ = ('request_bank_view', 'request_previous_bank_from_mod_matrix')

    def __init__(self, *a, **k):
        self.current_mod_target_index = IndexProvider()
        (super(WavetableDeviceDecorator, self).__init__)(*a, **k)
        self._single_selected_parameter = None
        self._options = self._create_options()
        self.register_disconnectables(self._options)
        self._WavetableDeviceDecorator__on_oscillator_switch_value_changed.subject = self.oscillator_switch
        self._WavetableDeviceDecorator__on_internal_filter_switch_value_changed.subject = self.filter_switch_for_filter_switch_option
        self._WavetableDeviceDecorator__on_current_mod_target_index_changed.subject = self.current_mod_target_index
        self._WavetableDeviceDecorator__on_lfo_types_provider_index_changed.subject = self._lfo_types_provider
        self._WavetableDeviceDecorator__on_envelope_types_provider_index_changed.subject = self._envelope_types_provider
        self._WavetableDeviceDecorator__on_amp_envelope_view_types_provider_index_changed.subject = self._amp_envelope_view_types_provider
        self._WavetableDeviceDecorator__on_mod_envelope_view_types_provider_index_changed.subject = self._mod_envelope_view_types_provider

    @property
    def options(self):
        return self._options

    @listenable_property
    def oscillator_index(self):
        return self._osc_types_provider.index

    @listenable_property
    def filter_index(self):
        return self._filter_types_provider.index

    @listenable_property
    def lfo_index(self):
        return self._lfo_types_provider.index

    @listenable_property
    def envelope_index(self):
        return self._envelope_types_provider.index

    @listenable_property
    def envelope_view_index(self):
        if self.envelope_index == WavetableEnvelopeType.amp:
            return self._amp_envelope_view_types_provider.index
        return self._mod_envelope_view_types_provider.index

    @property
    def single_selected_parameter(self):
        return self._single_selected_parameter

    def set_single_selected_parameter(self, value):
        self._single_selected_parameter = value
        self.add_to_mod_matrix_option.notify_active()

    @listenable_property
    def current_mod_target_parameter(self):
        return self._get_current_mod_target_parameter()

    def _create_parameters(self):
        self.filter_switch_for_filter_switch_option = EnumWrappingParameter(name='Internal Filter',
          parent=self,
          values_host=(self._filter_types_provider),
          index_property_host=(self._filter_types_provider),
          values_property='available_values',
          index_property='index',
          value_type=WavetableFilterType)
        self.current_mod_target = InternalParameter(name='Current Mod Target',
          parent=self)
        return super(WavetableDeviceDecorator, self)._create_parameters() + (EnumWrappingParameter(name='Modulation Target Names', parent=self, values_host=(self._live_object), index_property_host=(self.current_mod_target_index), values_property='visible_modulation_target_names', index_property='index'), ModMatrixParameter(name='Amp Env Mod Amount', parent=self, modulation_value_host=(self._live_object), modulation_target_index_host=(self.current_mod_target_index), modulation_source=(ModulationSource.amp_envelope)), ModMatrixParameter(name='Env 2 Mod Amount', parent=self, modulation_value_host=(self._live_object), modulation_target_index_host=(self.current_mod_target_index), modulation_source=(ModulationSource.envelope_2)), ModMatrixParameter(name='Env 3 Mod Amount', parent=self, modulation_value_host=(self._live_object), modulation_target_index_host=(self.current_mod_target_index), modulation_source=(ModulationSource.envelope_3)), ModMatrixParameter(name='Lfo 1 Mod Amount', parent=self, modulation_value_host=(self._live_object), modulation_target_index_host=(self.current_mod_target_index), modulation_source=(ModulationSource.lfo_1)), ModMatrixParameter(name='Lfo 2 Mod Amount', parent=self, modulation_value_host=(self._live_object), modulation_target_index_host=(self.current_mod_target_index), modulation_source=(ModulationSource.lfo_2)), ModMatrixParameter(name='MIDI Velocity Mod Amount', parent=self, modulation_value_host=(self._live_object), modulation_target_index_host=(self.current_mod_target_index), modulation_source=(ModulationSource.midi_velocity)), ModMatrixParameter(name='MIDI Note Mod Amount', parent=self, modulation_value_host=(self._live_object), modulation_target_index_host=(self.current_mod_target_index), modulation_source=(ModulationSource.midi_note)), ModMatrixParameter(name='MIDI Pitch Bend Mod Amount', parent=self, modulation_value_host=(self._live_object), modulation_target_index_host=(self.current_mod_target_index), modulation_source=(ModulationSource.midi_pitch_bend)), ModMatrixParameter(name='MIDI Aftertouch Mod Amount', parent=self, modulation_value_host=(self._live_object), modulation_target_index_host=(self.current_mod_target_index), modulation_source=(ModulationSource.midi_channel_pressure)), ModMatrixParameter(name='MIDI Mod Wheel Mod Amount', parent=self, modulation_value_host=(self._live_object), modulation_target_index_host=(self.current_mod_target_index), modulation_source=(ModulationSource.midi_mod_wheel)), ModMatrixParameter(name='MIDI Random On Note On', parent=self, modulation_value_host=(self._live_object), modulation_target_index_host=(self.current_mod_target_index), modulation_source=(ModulationSource.midi_random))) + (self.filter_switch_for_filter_switch_option, self.current_mod_target)

    def _create_options(self):

        def is_selected_parameter_modulatable():
            if self.single_selected_parameter is None:
                return False
            if isinstance(self.single_selected_parameter, PitchParameter):
                return True
            if isinstance(self.single_selected_parameter, InternalParameterBase):
                return False
            return self._live_object.is_parameter_modulatable(self.single_selected_parameter)

        def add_selected_parameter_to_mod_matrix():
            if is_selected_parameter_modulatable():
                param = self.single_selected_parameter.decimal_value_host if isinstance(self.single_selected_parameter, PitchParameter) else self.single_selected_parameter
                self.current_mod_target_index.index = self._live_object.add_parameter_to_modulation_matrix(param)
                self.notify_request_bank_view('Matrix')

        def jump_to_bank(bank_name):
            self.notify_request_bank_view(bank_name)

        def choose_envelope(value):
            self.envelope_switch.value = value

        def choose_lfo(value):
            self.lfo_switch.value = value

        self.osc_on_option = DeviceOnOffOption(name='Osc',
          property_host=(self._get_osc_on_property_host()))
        self.filter_on_option = DeviceOnOffOption(name='Filter',
          property_host=(self._get_filter_on_property_host()))
        self.lfo_retrigger_option = DeviceOnOffOption(name='Retrigger',
          property_host=(self._get_lfo_retrigger_property_host()))
        self.add_to_mod_matrix_option = DeviceTriggerOption(name='Add to Matrix',
          callback=add_selected_parameter_to_mod_matrix,
          is_active=is_selected_parameter_modulatable)
        return (
         DeviceOnOffOption(name='Sub',
           property_host=(get_parameter_by_name(self, 'Sub On'))),
         DeviceSwitchOption(name='Filter 1 Slope',
           parameter=(get_parameter_by_name(self, 'Filter 1 Slope')),
           labels=[
          '12dB', '24dB']),
         DeviceSwitchOption(name='Filter 2 Slope',
           parameter=(get_parameter_by_name(self, 'Filter 2 Slope')),
           labels=[
          '12dB', '24dB']),
         DeviceSwitchOption(name='Filter Switch',
           parameter=(self.filter_switch_for_filter_switch_option),
           labels=[
          'Filter 1', 'Filter 2']),
         DeviceSwitchOption(name='LFO 1 Sync',
           parameter=(get_parameter_by_name(self, 'LFO 1 Sync')),
           labels=[
          'Hz', 'Sync']),
         DeviceSwitchOption(name='LFO 2 Sync',
           parameter=(get_parameter_by_name(self, 'LFO 2 Sync')),
           labels=[
          'Hz', 'Sync']),
         DeviceTriggerOption(name='Go to Amp Env',
           callback=(lambda: (
          choose_envelope(WavetableEnvelopeType.amp),
          jump_to_bank('Envelopes'))
)),
         DeviceTriggerOption(name='Go to Env 2',
           callback=(lambda: (
          choose_envelope(WavetableEnvelopeType.env2),
          jump_to_bank('Envelopes'))
)),
         DeviceTriggerOption(name='Go to Env 3',
           callback=(lambda: (
          choose_envelope(WavetableEnvelopeType.env3),
          jump_to_bank('Envelopes'))
)),
         DeviceTriggerOption(name='Go to LFO 1',
           callback=(lambda: (
          choose_lfo(WavetableLfoType.one), jump_to_bank('LFOs'))
)),
         DeviceTriggerOption(name='Go to LFO 2',
           callback=(lambda: (
          choose_lfo(WavetableLfoType.two), jump_to_bank('LFOs'))
)),
         DeviceTriggerOption(name='Back',
           callback=(self.notify_request_previous_bank_from_mod_matrix))) + (
         self.osc_on_option,
         self.filter_on_option,
         self.lfo_retrigger_option,
         self.add_to_mod_matrix_option)

    def _get_parameter_by_name(self, name):
        return find_if(lambda p: p.name == name
, self.parameters)

    def _get_osc_on_property_host(self):
        return get_parameter_by_name(self, 'Osc {} On'.format(2 if self.oscillator_switch.value else 1))

    def _get_filter_on_property_host(self):
        return get_parameter_by_name(self, 'Filter {} On'.format(self.filter_switch_for_filter_switch_option.value + 1))

    def _get_lfo_retrigger_property_host(self):
        return get_parameter_by_name(self, 'LFO {} Retrigger'.format(self._lfo_types_provider.index + 1))

    def _resolve_ambiguous_modulation_target_name(self, target_parameter_name):
        if re.match('^Osc (1|2) Transp$', target_parameter_name):
            return target_parameter_name.replace('Transp', 'Pitch')
        lfo_rate_re = re.match('^LFO (1|2) S\\. Rate$', target_parameter_name)
        if lfo_rate_re:
            lfo_number = lfo_rate_re.group(1)
            lfo_sync_param = get_parameter_by_name(self, 'LFO {} Sync'.format(lfo_number))
            if lfo_sync_param.value == 0:
                return 'LFO {} Rate'.format(lfo_number)
        return target_parameter_name

    def _get_current_mod_target_parameter(self):
        target_parameter_name = self._resolve_ambiguous_modulation_target_name(self.get_modulation_target_parameter_name(self.current_mod_target_index.index))
        return self._get_parameter_by_name(target_parameter_name)

    @listens('value')
    def __on_oscillator_switch_value_changed(self):
        self.osc_on_option.set_property_host(self._get_osc_on_property_host())
        self.notify_oscillator_index()

    @listens('value')
    def __on_internal_filter_switch_value_changed(self):
        self.filter_on_option.set_property_host(self._get_filter_on_property_host())
        self.notify_filter_index()

    @listens('index')
    def __on_current_mod_target_index_changed(self):
        self.notify_current_mod_target_parameter()

    @listens('index')
    def __on_lfo_types_provider_index_changed(self):
        self.lfo_retrigger_option.set_property_host(self._get_lfo_retrigger_property_host())
        self.notify_lfo_index()

    @listens('index')
    def __on_envelope_types_provider_index_changed(self):
        self.notify_envelope_index()

    @listens('index')
    def __on_amp_envelope_view_types_provider_index_changed(self):
        self.notify_envelope_view_index()

    @listens('index')
    def __on_mod_envelope_view_types_provider_index_changed(self):
        self.notify_envelope_view_index()


def has_automation(parameter):
    return parameter.automation_state != AutomationState.none


class WavetableDeleteComponent(DeleteAndReturnToDefaultComponent):

    def delete_clip_envelope(self, parameter):
        if isinstance(parameter, PitchParameter) and has_automation(parameter):
            playing_clip = self._get_playing_clip()
            if playing_clip:
                deleted_automation_names = []
                for parameter in [
                 parameter.integer_value_host,
                 parameter.decimal_value_host]:
                    if has_automation(parameter):
                        playing_clip.clear_envelope(parameter)
                        deleted_automation_names.append(parameter.name)

                if deleted_automation_names:
                    self.show_notification(MessageBoxText.DELETE_ENVELOPE % dict(automation=(', '.join(deleted_automation_names))))
        else:
            super(WavetableDeleteComponent, self).delete_clip_envelope(parameter)


class WavetableDeviceComponent(DeviceComponentWithTrackColorViewData):
    OSCILLATOR_POSITION_PARAMETER_NAMES = re.compile('^(Osc (1|2) Pos)$|^Position$')
    FILTER_PARAMETER_NAMES = re.compile('^(Filter (1|2) (Type|Freq|Res))$|^Filter Type$|^Frequency$|^Resonance$')
    LFO_PARAMETER_NAMES = re.compile('^(LFO (1|2) (Shape|Shaping|S. Rate|Rate|Amount|Attack Time|Phase Offset))$|^LFO$|^LFO Type$|^Shape$|^Rate$|^Amount$|^Attack$|^Offset$')
    VISUALISATION_CONFIGURATION = {'wavetable':{'position_in_banks':{0:ButtonRange(0, 2), 
       1:ButtonRange(1, 3)}, 
      'visible_in_bank':lambda component, bank: component.selected_oscillator in [
       WavetableOscillatorType.one, WavetableOscillatorType.two]
}, 
     'filter':{'position_in_banks': {0:ButtonRange(3, 5),  2:ButtonRange(2, 4)}}, 
     'lfo':{'position_in_banks': {5: ButtonRange(0, 3)}}, 
     'envelope':{'position_in_banks': {4: ButtonRange(2, 5)}}}
    ENVELOPE_PREFIXES = [
     'Amp', 'Env 2', 'Env 3']

    def __init__(self, *a, **k):
        (super(WavetableDeviceComponent, self).__init__)(*a, **k)
        self._bank_before_mod_matrix = 0
        self._delete_default_component = WavetableDeleteComponent(parent=self,
          name='DeleteAndDefault')
        self._delete_default_component.layer = Layer(delete_button=(self._delete_button))

    def _parameter_touched(self, parameter):
        if liveobj_valid(self._decorated_device):
            if liveobj_valid(parameter):
                if self._is_resetting_parameter():
                    if self._is_custom_parameter(parameter):
                        self._delete_default_component.delete_clip_envelope(parameter)
                view_data = {}
                self._update_single_selected_parameter()
                if self.OSCILLATOR_POSITION_PARAMETER_NAMES.match(parameter.name):
                    view_data['AdjustingPosition'] = True
                if self.FILTER_PARAMETER_NAMES.match(parameter.name):
                    view_data['AdjustingFilter'] = True
                if self.LFO_PARAMETER_NAMES.match(parameter.name):
                    view_data['AdjustingLfo'] = True
                view_data.update(self._envelope_visualisation_data())
                if view_data:
                    self._update_visualisation_view_data(view_data)

    def _parameter_released(self, parameter):
        if liveobj_valid(self._decorated_device):
            if liveobj_valid(parameter):
                view_data = {}
                self._update_single_selected_parameter()
                if self.OSCILLATOR_POSITION_PARAMETER_NAMES.match(parameter.name):
                    view_data['AdjustingPosition'] = False
                if not self._any_filter_parameter_touched():
                    view_data['AdjustingFilter'] = False
                if not self._any_lfo_parameter_touched():
                    view_data['AdjustingLfo'] = False
                view_data.update(self._envelope_visualisation_data())
                if view_data:
                    self._update_visualisation_view_data(view_data)

    def _is_resetting_parameter(self):
        return self._delete_default_component is not None and self._delete_default_component.is_deleting

    def _is_custom_parameter(self, parameter):
        return isinstance(parameter, ModMatrixParameter) or isinstance(parameter, PitchParameter)

    def _get_provided_parameters(self):
        _, parameters = self._current_bank_details() if self.device() else (None, ())
        provided_parameters = []
        for param, name in parameters:
            if param == self._decorated_device.current_mod_target:
                param = self._decorated_device.current_mod_target_parameter
                name = param.name if param is not None else ''
            else:
                provided_parameters.append(self._create_parameter_info(param, name))

        return provided_parameters

    def _shift_button_pressed(self, button):
        self._decorated_device.osc_1_pitch.adjust_finegrain = True
        self._decorated_device.osc_2_pitch.adjust_finegrain = True

    def _shift_button_released(self, button):
        self._decorated_device.osc_1_pitch.adjust_finegrain = False
        self._decorated_device.osc_2_pitch.adjust_finegrain = False

    def _set_decorated_device(self, decorated_device):
        super(WavetableDeviceComponent, self)._set_decorated_device(decorated_device)
        self._WavetableDeviceComponent__on_selected_oscillator_changed.subject = decorated_device
        self._WavetableDeviceComponent__on_selected_filter_changed.subject = decorated_device
        self._WavetableDeviceComponent__on_selected_lfo_changed.subject = decorated_device
        self._WavetableDeviceComponent__on_selected_envelope_changed.subject = decorated_device
        self._WavetableDeviceComponent__on_selected_envelope_view_changed.subject = decorated_device
        self._WavetableDeviceComponent__on_request_bank_view.subject = decorated_device
        self._WavetableDeviceComponent__on_request_previous_bank_from_mod_matrix.subject = decorated_device
        self._WavetableDeviceComponent__on_current_mod_target_parameter_changed.subject = decorated_device

    def _set_bank_index(self, bank):
        current_bank = self._bank.index
        bank_definition = self._banking_info.device_bank_definition(self.device())
        if bank_definition.key_by_index(current_bank) not in ('Matrix', 'MIDI'):
            self._bank_before_mod_matrix = current_bank
        super(WavetableDeviceComponent, self)._set_bank_index(bank)
        self._update_single_selected_parameter()
        self._update_visualisation_view_data(self._get_current_view_data())
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    def _update_single_selected_parameter(self):
        touched_parameters = [self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed]
        self._decorated_device.set_single_selected_parameter(touched_parameters[0].parameter if len(touched_parameters) == 1 else None)

    def _any_filter_parameter_touched(self):
        touched_parameters = [self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed]
        return any([self.FILTER_PARAMETER_NAMES.match(parameter.name) for parameter in touched_parameters])

    def _any_lfo_parameter_touched(self):
        touched_parameters = [self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed]
        return any([self.LFO_PARAMETER_NAMES.match(parameter.name) for parameter in touched_parameters])

    def _visualisation_type_visible(self, visualisation_type):
        bank = self._bank.index
        configuration = self.VISUALISATION_CONFIGURATION[visualisation_type]
        return bank in configuration.get('position_in_banks', {}) and configuration.get('visible_in_bank', const(True))(self, bank)

    @property
    def _visualisation_visible(self):
        return any([self._visualisation_type_visible(visualisation) for visualisation in self.VISUALISATION_CONFIGURATION])

    @property
    def selected_oscillator(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.oscillator_index
        return 0

    @property
    def selected_filter(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.filter_index
        return 0

    @property
    def selected_lfo(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.lfo_index
        return 0

    @property
    def selected_envelope(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.envelope_index
        return 0

    def _get_visualisation_range(self, visualisation_type):
        configuration = self.VISUALISATION_CONFIGURATION[visualisation_type]
        positions = configuration.get('position_in_banks', {})
        return positions.get(self._bank.index, ButtonRange(0, 0))

    def _get_visualisation_start(self, visualisation_type):
        return VisualisationGuides.light_left_x(self._get_visualisation_range(visualisation_type).left_index)

    def _get_visualisation_width(self, visualisation_type):
        visualisation_range = self._get_visualisation_range(visualisation_type)
        return VisualisationGuides.light_right_x(visualisation_range.right_index) - VisualisationGuides.light_left_x(visualisation_range.left_index)

    @property
    def _shrink_parameters(self):
        if self.visualisation_visible:

            def parameter_over_visualisation(visualisation_type, parameter_index):
                visualisation_range = self._get_visualisation_range(visualisation_type)
                return visualisation_range.left_index <= parameter_index <= visualisation_range.right_index

            def is_shrunk(index):
                return any([self._visualisation_type_visible(visualisation) and parameter_over_visualisation(visualisation, index) for visualisation in self.VISUALISATION_CONFIGURATION])

            return [is_shrunk(parameter_index) for parameter_index in range(8)]
        return [False] * 8

    def _initial_visualisation_view_data(self):
        view_data = super(WavetableDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._get_current_view_data())
        return view_data

    def _get_current_view_data(self):
        view_data = {'SelectedOscillator':self.selected_oscillator, 
         'AdjustingPosition':False, 
         'AdjustingFilter':False, 
         'AdjustingLfo':False, 
         'WavetableVisualisationStart':self._get_visualisation_start('wavetable'), 
         'WavetableVisualisationWidth':self._get_visualisation_width('wavetable'), 
         'FilterCurveVisualisationStart':self._get_visualisation_start('filter'), 
         'FilterCurveVisualisationWidth':self._get_visualisation_width('filter'), 
         'LfoVisualisationStart':self._get_visualisation_start('lfo'), 
         'LfoVisualisationWidth':self._get_visualisation_width('lfo'), 
         'EnvelopeVisualisationStart':self._get_visualisation_start('envelope'), 
         'EnvelopeVisualisationWidth':self._get_visualisation_width('envelope'), 
         'WavetableVisualisationVisible':self._visualisation_type_visible('wavetable'), 
         'FilterVisualisationVisible':self._visualisation_type_visible('filter'), 
         'LfoVisualisationVisible':self._visualisation_type_visible('lfo'), 
         'EnvelopeVisualisationVisible':self._visualisation_type_visible('envelope'), 
         'SelectedFilter':self.selected_filter, 
         'SelectedLfo':self.selected_lfo}
        view_data.update(self._envelope_visualisation_data())
        return view_data

    def _envelope_visualisation_data(self):
        shown_features = set(['AttackLine', 'DecayLine', 'SustainLine', 'ReleaseLine'])
        focused_features = set()
        if self._visualisation_type_visible('envelope'):
            for parameter_info in self.parameters:
                extend_with_envelope_features_for_parameter(shown_features, parameter_info.parameter, self.ENVELOPE_PREFIXES)

            touched_parameters = [self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed]
            for parameter_info in touched_parameters:
                extend_with_envelope_features_for_parameter(focused_features, parameter_info.parameter, self.ENVELOPE_PREFIXES)

        return {'SelectedEnvelope':self.selected_envelope, 
         'EnvelopeShow':make_vector(list(shown_features)), 
         'EnvelopeFocus':make_vector(list(focused_features))}

    @listens('request_bank_view')
    def __on_request_bank_view(self, bank_name):
        device = self.device()
        bank_definition = self._banking_info.device_bank_definition(device)
        if bank_name in bank_definition:
            self._device_bank_registry.set_device_bank(device, bank_definition.index_by_key(bank_name))

    @listens('request_previous_bank_from_mod_matrix')
    def __on_request_previous_bank_from_mod_matrix(self):
        self._device_bank_registry.set_device_bank(self.device(), self._bank_before_mod_matrix)

    @listens('oscillator_index')
    def __on_selected_oscillator_changed(self):
        self._update_visualisation_view_data({'SelectedOscillator':self.selected_oscillator, 
         'WavetableVisualisationVisible':self._visualisation_type_visible('wavetable')})
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    @listens('filter_index')
    def __on_selected_filter_changed(self):
        self._update_visualisation_view_data({'SelectedFilter': self.selected_filter})

    @listens('lfo_index')
    def __on_selected_lfo_changed(self):
        self._update_visualisation_view_data({'SelectedLfo': self.selected_lfo})

    @listens('envelope_index')
    def __on_selected_envelope_changed(self):
        self._update_visualisation_view_data(self._envelope_visualisation_data())

    @listens('envelope_view_index')
    def __on_selected_envelope_view_changed(self):
        self._update_visualisation_view_data(self._envelope_visualisation_data())

    @listens('current_mod_target_parameter')
    def __on_current_mod_target_parameter_changed(self):
        self._update_parameters()