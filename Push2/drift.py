# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\drift.py
# Compiled at: 2023-06-30 09:18:52
# Size of source mod 2**32: 13550 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from enum import IntEnum
import Live
from ableton.v2.base import EventObject, listens, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData, extend_with_envelope_features_for_parameter, make_vector
from .visualisation_settings import VisualisationGuides
ParameterState = Live.DeviceParameter.ParameterState

class DriftDeviceDecorator(LiveObjectDecorator, EventObject):

    class oscSelect(IntEnum):
        osc1 = 0
        osc2 = 1

    class modSlotSelect(IntEnum):
        src1 = 0
        src2 = 1
        src3 = 2

    class modDestSelect(IntEnum):
        shape = 0
        pitch = 1
        filter = 2
        lfo = 3

    def __init__(self, *a, **k):
        (super(DriftDeviceDecorator, self).__init__)(*a, **k)
        self._add_enum_parameter(name='Osc Select',
          values=[
         'Osc 1', 'Osc 2'],
          default_value=(self.oscSelect.osc1))
        self._add_enum_parameter(name='Mod Slot',
          values=['1', '2', '3'],
          default_value=(self.modSlotSelect.src1))
        self._add_enum_parameter(name='Mod Dest',
          values=[
         'Shape', 'Pitch', 'Filter', 'LFO'],
          default_value=(self.modDestSelect.shape))
        self.voice_mode = self._add_non_automatable_enum_parameter(name='Voice Mode',
          list='voice_mode_list',
          index='voice_mode_index')
        self.voice_count = self._add_non_automatable_enum_parameter(name='Voice Count',
          list='voice_count_list',
          index='voice_count_index')
        self._add_non_automatable_enum_parameter(name='Shape Mod Src',
          list='mod_matrix_shape_source_list',
          index='mod_matrix_shape_source_index')
        self._add_non_automatable_enum_parameter(name='LFO Mod Src',
          list='mod_matrix_lfo_source_list',
          index='mod_matrix_lfo_source_index')
        self._add_non_automatable_enum_parameter(name='LP Mod Src 1',
          list='mod_matrix_filter_source_1_list',
          index='mod_matrix_filter_source_1_index')
        self._add_non_automatable_enum_parameter(name='LP Mod Src 2',
          list='mod_matrix_filter_source_2_list',
          index='mod_matrix_filter_source_2_index')
        self._add_non_automatable_enum_parameter(name='Pitch Mod Src 1',
          list='mod_matrix_pitch_source_1_list',
          index='mod_matrix_pitch_source_1_index')
        self._add_non_automatable_enum_parameter(name='Pitch Mod Src 2',
          list='mod_matrix_pitch_source_2_list',
          index='mod_matrix_pitch_source_2_index')
        self._add_non_automatable_enum_parameter(name='Mod Source 1',
          list='mod_matrix_source_1_list',
          index='mod_matrix_source_1_index')
        self._add_non_automatable_enum_parameter(name='Mod Source 2',
          list='mod_matrix_source_2_list',
          index='mod_matrix_source_2_index')
        self._add_non_automatable_enum_parameter(name='Mod Source 3',
          list='mod_matrix_source_3_list',
          index='mod_matrix_source_3_index')
        self._add_non_automatable_enum_parameter(name='Mod Dest 1',
          list='mod_matrix_target_1_list',
          index='mod_matrix_target_1_index')
        self._add_non_automatable_enum_parameter(name='Mod Dest 2',
          list='mod_matrix_target_2_list',
          index='mod_matrix_target_2_index')
        self._add_non_automatable_enum_parameter(name='Mod Dest 3',
          list='mod_matrix_target_3_list',
          index='mod_matrix_target_3_index')
        self._add_non_automatable_int_parameter(name='PB Range',
          property_name='pitch_bend_range',
          min=0,
          max=12,
          units='st')
        self._add_switch_option(name='Osc 2 Wave',
          pname='Osc 2 Wave',
          labels=[
         'Sin','Tri','Sat','Saw','Rec'])
        self._add_switch_option(name='Env 2 Cyc On',
          pname='Env 2 Cyc On',
          labels=['Env', 'Cyc'])
        self._add_on_off_option(name='Osc 1', pname='Osc 1 On')
        self._add_on_off_option(name='Osc 2', pname='Osc 2 On')
        self._add_on_off_option(name='Osc Retrig', pname='Osc Retrig On')
        self._add_on_off_option(name='Osc 1 Flt', pname='Osc 1 Flt On')
        self._add_on_off_option(name='Osc 2 Flt', pname='Osc 2 Flt On')
        self._add_on_off_option(name='LFO Retrig', pname='LFO Retrig On')
        self._add_on_off_option(name='Legato', pname='Legato On')
        self._add_on_off_option(name='Noise', pname='Noise On')
        self._add_on_off_option(name='Noise Flt', pname='Noise Flt On')
        self._add_on_off_option(name='Note PB', pname='Note Pitch Bend On')
        self.on_voice_mode_change.subject = self.voice_mode
        self.on_voice_mode_change()
        self.register_disconnectables(self.options)

    @listens('value')
    def on_voice_mode_change(self):
        self.update_voice_count_parameter()

    def update_voice_count_parameter(self):
        voice_count_state = ParameterState.enabled if self.voice_mode.value != 1 else ParameterState.disabled
        self.voice_count.state = voice_count_state


class DriftDeviceComponent(DeviceComponentWithTrackColorViewData):
    WAVEFORM_VISUALISATION_CONFIGURATION_IN_BANKS = {0:ButtonRange(1, 3), 
     1:ButtonRange(1, 3)}
    FILTER_VISUALISATION_CONFIGURATION_IN_FILTER_BANK = {2: ButtonRange(1, 3)}
    ENV1_VISUALISATION_CONFIGURATION_IN_ENV_BANK = {3: ButtonRange(0, 3)}
    ENV2_VISUALISATION_CONFIGURATION_IN_ENV_BANK = {3: ButtonRange(4, 7)}
    ENVELOPE1_PREFIX = [
     'Env 1']
    ENVELOPE2_PREFIX = ['Env 2']
    ENVELOPE_PREFIXES = ['Env 1', 'Env 2']

    def _parameter_touched(self, parameter):
        self._update_visualisation_view_data(self._visualisation_data())

    def _parameter_released(self, parameter):
        self._update_visualisation_view_data(self._visualisation_data())

    def parameter_changed(self, parameter):
        self._update_visualisation_view_data(self._visualisation_data())

    def _visualisation_data(self):
        data = self._adjustment_view_data
        data.update(self._envelope_visualisation_data())
        return data

    @property
    def _adjustment_view_data(self):
        if not liveobj_valid(self._decorated_device):
            return {}
        adjusting_filter_hp = adjusting_filter_lp = adjusting_cycling_envelope = adjusting_waveform = False
        touched_parameters = [self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed]
        for parameter in touched_parameters:
            if parameter.name == 'HP Freq':
                adjusting_filter_hp = True
            else:
                if parameter.name in ('LP Freq', 'LP Reso'):
                    adjusting_filter_lp = True
                else:
                    if parameter.name in ('Cyc Tilt', 'Cyc Hold', 'Cyc Mode', 'Cyc Rate',
                                          'Cyc Ratio', 'Cyc Time', 'Cyc Synced'):
                        adjusting_cycling_envelope = True
            if parameter.name in ('Osc 1 Wave', 'Osc 2 Wave', 'Osc 1 Shape', 'Osc 1 Oct',
                                  'Osc 2 Oct', 'Osc 2 Detune', 'Osc 1 Gain', 'Osc 2 Gain',
                                  'Noise Gain'):
                adjusting_waveform = True

        return {
          'AdjustingWaveform': adjusting_waveform,
          'AdjustingFilterHighPass': adjusting_filter_hp,
          'AdjustingFilterLowPass': adjusting_filter_lp,
          'AdjustingCyclingEnvelope': adjusting_cycling_envelope}

    def _set_bank_index(self, bank):
        super(DriftDeviceComponent, self)._set_bank_index(bank)
        self._update_visualisation_view_data(self._configuration_view_data)
        self._update_visualisation_view_data(self._visualisation_data())
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    @property
    def _visualisation_visible(self):
        return self._bank.index in self.WAVEFORM_VISUALISATION_CONFIGURATION_IN_BANKS or self._bank.index in self.FILTER_VISUALISATION_CONFIGURATION_IN_FILTER_BANK or self._bank.index in self.ENV1_VISUALISATION_CONFIGURATION_IN_ENV_BANK or self._bank.index in self.ENV2_VISUALISATION_CONFIGURATION_IN_ENV_BANK

    @property
    def _shrink_parameters(self):
        if self._visualisation_visible:
            waveform_config = self.WAVEFORM_VISUALISATION_CONFIGURATION_IN_BANKS.get(self._bank.index, ButtonRange(-1, -1))
            filter_config = self.FILTER_VISUALISATION_CONFIGURATION_IN_FILTER_BANK.get(self._bank.index, ButtonRange(-1, -1))
            env1_config = self.ENV1_VISUALISATION_CONFIGURATION_IN_ENV_BANK.get(self._bank.index, ButtonRange(-1, -1))
            env2_config = self.ENV2_VISUALISATION_CONFIGURATION_IN_ENV_BANK.get(self._bank.index, ButtonRange(-1, -1))
            return [waveform_config.left_index <= index <= waveform_config.right_index or filter_config.left_index <= index <= filter_config.right_index or env1_config.left_index <= index <= env1_config.right_index or env2_config.left_index <= index <= env2_config.right_index for index in range(8)]
        return [
         False] * 8

    @property
    def _configuration_view_data(self):
        if not liveobj_valid(self._decorated_device):
            return {}
        waveform_left, waveform_right = self._calculate_view_size(self.WAVEFORM_VISUALISATION_CONFIGURATION_IN_BANKS)
        filter_left, filter_right = self._calculate_view_size(self.FILTER_VISUALISATION_CONFIGURATION_IN_FILTER_BANK)
        env1_left, env1_right = self._calculate_view_size(self.ENV1_VISUALISATION_CONFIGURATION_IN_ENV_BANK)
        env2_left, env2_right = self._calculate_view_size(self.ENV2_VISUALISATION_CONFIGURATION_IN_ENV_BANK)
        return {
          'WaveformLeft': waveform_left,
          'WaveformRight': waveform_right,
          'FilterLeft': filter_left,
          'FilterRight': filter_right,
          'Env1Left': env1_left,
          'Env1Right': env1_right,
          'Env2Left': env2_left,
          'Env2Right': env2_right}

    def _envelope_visualisation_data(self):
        shown_features = set(['AttackLine', 'DecayLine', 'SustainLine', 'ReleaseLine'])
        focused_features = set()
        for parameter in self.parameters:
            extend_with_envelope_features_for_parameter(shown_features, parameter, self.ENVELOPE_PREFIXES)

        touched_parameters = [self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed]
        focused_features1 = set()
        focused_features2 = set()
        for parameter in touched_parameters:
            extend_with_envelope_features_for_parameter(focused_features1, parameter, self.ENVELOPE1_PREFIX)

        for parameter in touched_parameters:
            extend_with_envelope_features_for_parameter(focused_features2, parameter, self.ENVELOPE2_PREFIX)

        return {'EnvelopeShow':make_vector(shown_features), 
         'Envelope1Focus':make_vector(focused_features1), 
         'Envelope2Focus':make_vector(focused_features2)}

    def _initial_visualisation_view_data(self):
        view_data = super()._initial_visualisation_view_data()
        view_data.update(self._configuration_view_data)
        view_data.update(self._visualisation_data())
        return view_data

    def _calculate_view_size(self, configuration):
        if self._bank.index not in configuration:
            return (0, 0)
        config = configuration[self._bank.index]
        return (
         VisualisationGuides.light_left_x(config.left_index),
         VisualisationGuides.light_right_x(config.right_index))