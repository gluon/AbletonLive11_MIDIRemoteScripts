# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\clip_control.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 43457 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import map, round, str
from past.utils import old_div
from contextlib import contextmanager
from itertools import chain
from MidiRemoteScript import MutableVector
from ableton.v2.base import listenable_property, listens, listens_group, liveobj_valid, old_hasattr, task
from ableton.v2.control_surface import Component, WrappingParameter
from ableton.v2.control_surface.control import ButtonControl, EncoderControl, MappedSensitivitySettingControl, ToggleButtonControl
from ableton.v2.control_surface.mode import ModesComponent
from pushbase.clip_control_component import ONE_YEAR_AT_120BPM_IN_BEATS, WARP_MODE_NAMES
from pushbase.clip_control_component import AudioClipSettingsControllerComponent as AudioClipSettingsControllerComponentBase
from pushbase.clip_control_component import LoopSettingsControllerComponent as LoopSettingsControllerComponentBase
from pushbase.clip_control_component import convert_beat_length_to_bars_beats_sixteenths, convert_beat_time_to_bars_beats_sixteenths
from pushbase.note_editor_component import DEFAULT_START_NOTE
from .clip_decoration import ClipDecoratorFactory
from .colors import COLOR_INDEX_TO_SCREEN_COLOR
from .decoration import find_decorated_object
from .drum_group_component import DrumPadColorNotifier
from .real_time_channel import RealTimeDataComponent
from .timeline_navigation import ObjectDescription
PARAMETERS_LOOPED = ('Loop position', 'Loop length', 'Start offset')
PARAMETERS_NOT_LOOPED = ('Start', 'End')
PARAMETERS_AUDIO = ('Warp', 'Transpose', 'Detune', 'Gain')

def make_color_vector(color_indices):
    color_vector = MutableVector()
    for color_index in color_indices:
        color_vector.append(COLOR_INDEX_TO_SCREEN_COLOR[color_index].as_remote_script_color())

    return color_vector


def make_vector(items):
    vector = MutableVector()
    for item in items:
        vector.append(item)

    return vector


class LoopSetting(WrappingParameter):
    min = -ONE_YEAR_AT_120BPM_IN_BEATS
    max = ONE_YEAR_AT_120BPM_IN_BEATS

    def __init__(self, use_length_conversion=False, *a, **k):
        (super(LoopSetting, self).__init__)(*a, **k)
        self._conversion = convert_beat_length_to_bars_beats_sixteenths if use_length_conversion else convert_beat_time_to_bars_beats_sixteenths
        self._recording = False
        self.set_property_host(self._parent)
        self._LoopSetting__on_clip_changed.subject = self.canonical_parent
        self._LoopSetting__on_clip_changed()

    @property
    def recording(self):
        return self._recording

    @recording.setter
    def recording(self, value):
        self._recording = value
        self.notify_value()

    @listens('clip')
    def __on_clip_changed(self):
        self._LoopSetting__on_signature_numerator_changed.subject = self.canonical_parent.clip
        self._LoopSetting__on_signature_denominator_changed.subject = self.canonical_parent.clip

    @listens('signature_numerator')
    def __on_signature_numerator_changed(self):
        self.notify_value()

    @listens('signature_denominator')
    def __on_signature_denominator_changed(self):
        self.notify_value()

    @property
    def display_value(self):
        if not liveobj_valid(self.canonical_parent.clip):
            return str('-')
        if self.recording:
            return str('...')
        return str(self._conversion((
         self.canonical_parent.clip.signature_numerator,
         self.canonical_parent.clip.signature_denominator), self._get_property_value()))


class LoopSettingsControllerComponent(LoopSettingsControllerComponentBase):
    __events__ = ('looping', 'loop_parameters', 'zoom', 'clip')
    ZOOM_DEFAULT_SENSITIVITY = MappedSensitivitySettingControl.DEFAULT_SENSITIVITY
    ZOOM_FINE_SENSITIVITY = MappedSensitivitySettingControl.FINE_SENSITIVITY
    zoom_encoder = MappedSensitivitySettingControl()
    zoom_touch_encoder = EncoderControl()
    loop_button = ToggleButtonControl(toggled_color='Clip.Option',
      untoggled_color='Clip.OptionDisabled')
    crop_button = ButtonControl(color='Clip.Action')

    def __init__(self, *a, **k):
        (super(LoopSettingsControllerComponent, self).__init__)(*a, **k)
        self._looping_settings = [
         LoopSetting(name=(PARAMETERS_LOOPED[0]),
           parent=(self._loop_model),
           source_property='position'),
         LoopSetting(name=(PARAMETERS_LOOPED[1]),
           parent=(self._loop_model),
           use_length_conversion=True,
           source_property='loop_length'),
         LoopSetting(name=(PARAMETERS_LOOPED[2]),
           parent=(self._loop_model),
           source_property='start_marker')]
        self._non_looping_settings = [
         LoopSetting(name=(PARAMETERS_NOT_LOOPED[0]),
           parent=(self._loop_model),
           source_property='loop_start'),
         LoopSetting(name=(PARAMETERS_NOT_LOOPED[1]),
           parent=(self._loop_model),
           source_property='loop_end')]
        for setting in self._looping_settings + self._non_looping_settings:
            self.register_disconnectable(setting)

        self._LoopSettingsControllerComponent__on_looping_changed.subject = self._loop_model
        self._LoopSettingsControllerComponent__on_looping_changed()

    def update(self):
        super(LoopSettingsControllerComponent, self).update()
        if self.is_enabled():
            self.notify_timeline_navigation()
            self.notify_clip()

    @loop_button.toggled
    def loop_button(self, toggled, button):
        self._loop_model.looping = toggled

    @crop_button.pressed
    def crop_button(self, button):
        if liveobj_valid(self.clip):
            self.clip.crop()

    @property
    def looping(self):
        if self.clip:
            return self._loop_model.looping
        return False

    @property
    def loop_parameters(self):
        if not liveobj_valid(self.clip):
            return []
        parameters = self._looping_settings if self.looping else self._non_looping_settings
        if self.zoom:
            return [self.zoom] + parameters
        return parameters

    @property
    def zoom(self):
        if liveobj_valid(self.clip):
            return getattr(self.clip, 'zoom', None)

    @listenable_property
    def timeline_navigation(self):
        if liveobj_valid(self.clip):
            return getattr(self.clip, 'timeline_navigation', None)

    @listens('is_recording')
    def __on_is_recording_changed(self):
        self._update_recording_state()

    @listens('is_overdubbing')
    def __on_is_overdubbing_changed(self):
        self._update_recording_state()

    def _update_recording_state(self):
        clip = self._loop_model.clip
        if liveobj_valid(clip):
            recording = clip.is_recording and not clip.is_overdubbing
            self._looping_settings[1].recording = recording
            self._non_looping_settings[1].recording = recording

    @listens('looping')
    def __on_looping_changed(self):
        self._update_and_notify()

    def _update_loop_button(self):
        self.loop_button.enabled = liveobj_valid(self.clip)
        if liveobj_valid(self.clip):
            self.loop_button.is_toggled = self._loop_model.looping

    def _on_clip_changed(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.reset_focus_and_animation()
        self._update_and_notify()
        self._LoopSettingsControllerComponent__on_is_recording_changed.subject = self._loop_model.clip
        self._LoopSettingsControllerComponent__on_is_overdubbing_changed.subject = self._loop_model.clip
        self._update_recording_state()
        self.crop_button.enabled = liveobj_valid(self.clip) and self.clip.is_midi_clip
        self._connect_encoder()
        if self.is_enabled():
            self.notify_timeline_navigation()

    def _on_clip_start_marker_touched(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.touch_object(self.timeline_navigation.start_marker_focus)

    def _on_clip_position_touched(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.touch_object(self.timeline_navigation.loop_start_focus)

    def _on_clip_end_touched(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.touch_object(self.timeline_navigation.loop_end_focus)

    def _on_clip_start_marker_released(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.release_object(self.timeline_navigation.start_marker_focus)

    def _on_clip_position_released(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.release_object(self.timeline_navigation.loop_start_focus)

    def _on_clip_end_released(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.release_object(self.timeline_navigation.loop_end_focus)

    @zoom_touch_encoder.touched
    def zoom_touch_encoder(self, encoder):
        if self.timeline_navigation is not None:
            self.timeline_navigation.touch_object(self.timeline_navigation.zoom_focus)

    @zoom_touch_encoder.released
    def zoom_touch_encoder(self, encoder):
        if self.timeline_navigation is not None:
            self.timeline_navigation.release_object(self.timeline_navigation.zoom_focus)

    def _update_and_notify(self):
        self._update_loop_button()
        self.notify_looping()
        self.notify_loop_parameters()
        self.notify_zoom()

    def _connect_encoder(self):
        self.zoom_encoder.mapped_parameter = self.zoom
        self.zoom_encoder.update_sensitivities(self.ZOOM_DEFAULT_SENSITIVITY, self.ZOOM_FINE_SENSITIVITY)

    def set_zoom_encoder(self, encoder):
        self.zoom_encoder.set_control_element(encoder)
        self.zoom_touch_encoder.set_control_element(encoder)
        self._connect_encoder()


class GainSetting(WrappingParameter):

    def __init__(self, *a, **k):
        (super(GainSetting, self).__init__)(*a, **k)
        self.set_property_host(self._parent)

    @property
    def display_value(self):
        return str(self._property_host.clip.gain_display_string if self._property_host.clip else '')


class PitchSetting(WrappingParameter):

    def __init__(self, min_value, max_value, unit, *a, **k):
        (super(PitchSetting, self).__init__)(*a, **k)
        self._min = min_value
        self._max = max_value
        self._unit = unit
        self.set_property_host(self._parent)

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def display_value(self):
        value = int(round(float(self._get_property_value())))
        positive_indicator = '+' if value > 0 else ''
        return positive_indicator + str(value) + self._unit


class WarpSetting(WrappingParameter):

    def __init__(self, *a, **k):
        (super(WarpSetting, self).__init__)(*a, **k)
        self.set_property_host(self._parent)

    @property
    def max(self):
        return len(self._property_host.available_warp_modes) - 1

    @property
    def is_quantized(self):
        return True

    @property
    def value_items(self):
        return list(map(lambda x: str(WARP_MODE_NAMES[x])
, self._property_host.available_warp_modes))

    @property
    def short_value_items(self):
        return self.value_items

    def _get_property_value(self):
        return self._property_host.available_warp_modes.index(getattr(self._property_host, self._source_property))


class AudioClipSettingsControllerComponent(AudioClipSettingsControllerComponentBase):
    __events__ = ('audio_parameters', 'warping', 'gain')

    def __init__(self, *a, **k):
        (super(AudioClipSettingsControllerComponent, self).__init__)(*a, **k)
        self._audio_clip_parameters = [
         WarpSetting(name=(PARAMETERS_AUDIO[0]),
           parent=(self._audio_clip_model),
           source_property='warp_mode'),
         PitchSetting(name=(PARAMETERS_AUDIO[1]),
           parent=(self._audio_clip_model),
           source_property='pitch_coarse',
           min_value=(-49.0),
           max_value=49.0,
           unit='st'),
         PitchSetting(name=(PARAMETERS_AUDIO[2]),
           parent=(self._audio_clip_model),
           source_property='pitch_fine',
           min_value=(-51.0),
           max_value=51.0,
           unit='ct'),
         GainSetting(name=(PARAMETERS_AUDIO[3]),
           parent=(self._audio_clip_model),
           source_property='gain')]
        self._playhead_real_time_data = RealTimeDataComponent(channel_type='playhead',
          parent=self)
        self._waveform_real_time_data = RealTimeDataComponent(channel_type='waveform',
          parent=self)
        for parameter in self._audio_clip_parameters:
            self.register_disconnectable(parameter)

        self._AudioClipSettingsControllerComponent__on_warping_changed.subject = self._audio_clip_model
        self._AudioClipSettingsControllerComponent__on_gain_changed.subject = self._audio_clip_model
        self._AudioClipSettingsControllerComponent__on_warping_changed()
        self._AudioClipSettingsControllerComponent__on_gain_changed()

    def disconnect(self):
        super(AudioClipSettingsControllerComponent, self).disconnect()
        self._playhead_real_time_data.set_data(None)
        self._waveform_real_time_data.set_data(None)

    @property
    def audio_parameters(self):
        if liveobj_valid(self.clip):
            return self._audio_clip_parameters
        return []

    @property
    def warping(self):
        if liveobj_valid(self.clip):
            return self._audio_clip_model.warping
        return False

    @property
    def gain(self):
        if liveobj_valid(self.clip):
            return self._audio_clip_model.gain
        return 0.0

    @property
    def waveform_real_time_channel_id(self):
        return self._waveform_real_time_data.channel_id

    @property
    def playhead_real_time_channel_id(self):
        return self._playhead_real_time_data.channel_id

    def _on_clip_changed(self):
        self._playhead_real_time_data.set_data(self.clip)
        self._waveform_real_time_data.set_data(self.clip)
        self._AudioClipSettingsControllerComponent__on_file_path_changed.subject = self.clip
        self.notify_audio_parameters()
        self.notify_warping()
        self.notify_gain()

    def _on_transpose_encoder_value(self, value):
        self._audio_clip_model.set_clip_pitch_coarse(value, False)

    def _on_detune_encoder_value(self, value):
        self._audio_clip_model.set_clip_pitch_fine(value, False)

    @listens('warping')
    def __on_warping_changed(self):
        self.notify_warping()

    @listens('gain')
    def __on_gain_changed(self):
        self.notify_gain()

    @listens('file_path')
    def __on_file_path_changed(self):
        self._waveform_real_time_data.invalidate()


def register_matrix_mode(matrix_map, name, modes_component=None, parent_path=None):

    def find_leaf(tree, path):
        key_name, rest = path[0], path[1:]
        if key_name not in tree:
            tree[key_name] = dict(modes_component=None, children={})
        sub_tree = tree[key_name]['children']
        if len(rest) == 0:
            return sub_tree
        return find_leaf(sub_tree, rest)

    matrix_map_to_edit = matrix_map if parent_path is None else find_leaf(matrix_map, parent_path)
    children_to_add_to_map = matrix_map_to_edit[name].get('children', {}) if name in matrix_map_to_edit else {}
    matrix_map_to_edit[name] = dict(modes_component=modes_component,
      children=children_to_add_to_map)


class MatrixModeWatcherComponent(Component):

    def __init__(self, matrix_mode_map=None, *a, **k):
        (super(MatrixModeWatcherComponent, self).__init__)(*a, **k)
        self._matrix_mode_map = matrix_mode_map

        def connect_listeners(dct):
            for key, value in dct.items():
                if key == 'modes_component':
                    self.register_slot(value, self._MatrixModeWatcherComponent__on_matrix_mode_changed, 'selected_mode')
                else:
                    connect_listeners(value)

        connect_listeners(matrix_mode_map)
        self._matrix_mode_path = None
        self.matrix_mode_path = self.create_mode_path(matrix_mode_map)

    @staticmethod
    def create_mode_path(initial_mode_map):
        mode_path = []

        def create_mode_path_recursive(mode_map):
            mode_entry = list(mode_map.keys())[0]
            mode_path.append(mode_entry)
            parent = mode_map[mode_entry]
            children = parent['children']
            modes_comp = parent['modes_component']
            selected_mode = modes_comp.selected_mode
            if selected_mode in children:
                if len(list(children[selected_mode]['children'].keys())) > 0:
                    return create_mode_path_recursive({selected_mode: children[selected_mode]})
                mode_path.append(selected_mode)
            return mode_path

        return '.'.join(create_mode_path_recursive(initial_mode_map))

    @listenable_property
    def matrix_mode_path(self):
        return self._matrix_mode_path

    @matrix_mode_path.setter
    def matrix_mode_path(self, mode):
        if self._matrix_mode_path != mode:
            self._matrix_mode_path = mode
            self.notify_matrix_mode_path()

    def __on_matrix_mode_changed(self, mode):
        if mode is not None:
            self.matrix_mode_path = self.create_mode_path(self._matrix_mode_map)


_MATRIX_MODE_PATH_TO_DATA = {'matrix_modes.note.instrument.play':{
   'Fold': True,
   'NumDisplayKeys': 0,
   'ShowGridWindow': False,
   'ShowScrollbarCursor': False,
   'NumPitches': 128,
   'PitchOffset': 0,
   'ShowStepLengthGrid': False,
   'ShowMultipleGridWindows': False}, 
 'matrix_modes.note.instrument.sequence':{
   'Fold': False,
   'NumDisplayKeys': 23,
   'ShowGridWindow': True,
   'ShowScrollbarCursor': True,
   'NumPitches': 128,
   'PitchOffset': 0,
   'ShowStepLengthGrid': True,
   'ShowMultipleGridWindows': False}, 
 'matrix_modes.note.instrument.split_melodic_sequencer':{
   'Fold': True,
   'NumDisplayKeys': 32,
   'ShowGridWindow': True,
   'ShowScrollbarCursor': True,
   'NumPitches': 128,
   'PitchOffset': 0,
   'ShowStepLengthGrid': True,
   'ShowMultipleGridWindows': True}, 
 'matrix_modes.note.drums.64pads':{
   'Fold': True,
   'NumDisplayKeys': 0,
   'ShowGridWindow': False,
   'ShowScrollbarCursor': False,
   'NumPitches': 128,
   'PitchOffset': 0,
   'ShowStepLengthGrid': False,
   'ShowMultipleGridWindows': False}, 
 'matrix_modes.note.drums.sequencer_loop':{
   'Fold': False,
   'NumDisplayKeys': 17,
   'ShowGridWindow': True,
   'ShowScrollbarCursor': True,
   'NumPitches': 128,
   'PitchOffset': 0,
   'ShowStepLengthGrid': True,
   'ShowMultipleGridWindows': False}, 
 'matrix_modes.note.drums.sequencer_velocity_levels':{
   'Fold': False,
   'NumDisplayKeys': 17,
   'ShowGridWindow': True,
   'ShowScrollbarCursor': True,
   'NumPitches': 128,
   'PitchOffset': 0,
   'ShowStepLengthGrid': True,
   'ShowMultipleGridWindows': False}, 
 'matrix_modes.note.slicing.64pads':{
   'Fold': True,
   'NumDisplayKeys': 0,
   'ShowGridWindow': False,
   'ShowScrollbarCursor': False,
   'NumPitches': 64,
   'PitchOffset': 36,
   'ShowStepLengthGrid': False,
   'ShowMultipleGridWindows': False}, 
 'matrix_modes.note.slicing.sequencer_loop':{
   'Fold': False,
   'NumDisplayKeys': 17,
   'ShowGridWindow': True,
   'ShowScrollbarCursor': True,
   'NumPitches': 64,
   'PitchOffset': 36,
   'ShowStepLengthGrid': True,
   'ShowMultipleGridWindows': False}, 
 'matrix_modes.note.slicing.sequencer_velocity_levels':{
   'Fold': False,
   'NumDisplayKeys': 17,
   'ShowGridWindow': True,
   'ShowScrollbarCursor': True,
   'NumPitches': 64,
   'PitchOffset': 36,
   'ShowStepLengthGrid': True,
   'ShowMultipleGridWindows': False}, 
 'matrix_modes.session':{
   'Fold': True,
   'NumDisplayKeys': 0,
   'ShowGridWindow': False,
   'ShowScrollbarCursor': False,
   'NumPitches': 128,
   'PitchOffset': 0,
   'ShowStepLengthGrid': False,
   'ShowMultipleGridWindows': False}}
_DEFAULT_VIEW_DATA = {
  'Fold': True,
  'NumDisplayKeys': 0,
  'ShowGridWindow': False,
  'ShowScrollbarCursor': False,
  'MinPitch': DEFAULT_START_NOTE,
  'MaxSequenceablePitch': DEFAULT_START_NOTE,
  'MinSequenceablePitch': DEFAULT_START_NOTE,
  'PageIndex': 0,
  'PageLength': 1.0,
  'MinGridWindowPitch': DEFAULT_START_NOTE,
  'MaxGridWindowPitch': DEFAULT_START_NOTE,
  'NumPitches': 128,
  'PitchOffset': 0,
  'ShowStepLengthGrid': False,
  'IsRecording': False,
  'ShowMultipleGridWindows': False}

def get_static_view_data(matrix_mode_path):
    return _MATRIX_MODE_PATH_TO_DATA.get(matrix_mode_path, _DEFAULT_VIEW_DATA)


class MidiClipControllerComponent(Component):
    grid_window_focus = 'grid_window_start'

    def __init__(self, *a, **k):
        (super(MidiClipControllerComponent, self).__init__)(*a, **k)
        self._configure_vis_task = self._tasks.add(task.sequence(task.delay(1), task.run(self._configure_visualisation))).kill()
        self._clip = None
        self._matrix_mode_watcher = None
        self._most_recent_base_note = DEFAULT_START_NOTE
        self._most_recent_max_note = DEFAULT_START_NOTE
        self._loose_follow_base_note = DEFAULT_START_NOTE
        self._most_recent_editable_pitches = (DEFAULT_START_NOTE, DEFAULT_START_NOTE)
        self._most_recent_row_start_times = []
        self._most_recent_step_length = 1.0
        self._most_recent_page_index = 0
        self._most_recent_page_length = 1.0
        self._most_recent_editing_note_regions = []
        self._visualisation_real_time_data = RealTimeDataComponent(channel_type='visualisation',
          parent=self)
        self._MidiClipControllerComponent__on_visualisation_channel_changed.subject = self._visualisation_real_time_data
        self._MidiClipControllerComponent__on_visualisation_attached.subject = self._visualisation_real_time_data
        self._instruments = []
        self._sequencers = []
        self._mute_during_track_change_components = []
        self._note_settings_component = None
        self._note_editor_settings_component = None
        self._real_time_data_attached = False
        self._drum_rack_finder = None
        self._drum_pad_color_notifier = self.register_disconnectable(DrumPadColorNotifier())
        self._MidiClipControllerComponent__on_note_colors_changed.subject = self._drum_pad_color_notifier

    @property
    def clip(self):
        return self._clip

    @clip.setter
    def clip(self, clip):
        self._clip = clip
        self._on_clip_changed()

    @listenable_property
    def visualisation_real_time_channel_id(self):
        return self._visualisation_real_time_data.channel_id

    def set_drum_rack_finder(self, finder_component):
        self._drum_rack_finder = finder_component
        self._MidiClipControllerComponent__on_drum_rack_changed.subject = self._drum_rack_finder
        self._MidiClipControllerComponent__on_drum_rack_changed()

    def set_matrix_mode_watcher(self, watcher):
        self._matrix_mode_watcher = watcher
        self._MidiClipControllerComponent__on_matrix_mode_changed.subject = watcher

    def external_regions_of_interest_creator(self, region_of_interest_creator):

        def grid_start_time():
            return self._most_recent_page_index * self._most_recent_page_length

        return {'grid_window': region_of_interest_creator(start_identifier=(self.grid_window_focus),
                          getter=(lambda: (
                         grid_start_time(),
                         grid_start_time() + self._most_recent_page_length)
))}

    @property
    def external_focusable_object_descriptions(self):
        return {self.grid_window_focus: ObjectDescription(('start_end', 'loop', 'grid_window'), self.grid_window_focus)}

    def set_note_settings_component(self, note_settings_component):
        self._note_settings_component = note_settings_component
        self._MidiClipControllerComponent__on_note_settings_enabled_changed.subject = note_settings_component

    def set_note_editor_settings_component(self, note_editor_settings_component):
        self._note_editor_settings_component = note_editor_settings_component
        self._MidiClipControllerComponent__on_note_editor_settings_touched_changed.subject = note_editor_settings_component

    def add_instrument_component(self, instrument):
        self._MidiClipControllerComponent__on_instrument_position_changed.add_subject(instrument)
        self._instruments.append(instrument)

    def add_mute_during_track_change_component(self, component):
        self._mute_during_track_change_components.append(component)

    def add_paginator(self, paginator):
        self._MidiClipControllerComponent__on_paginator_page_index_changed.add_subject(paginator)
        self._MidiClipControllerComponent__on_paginator_page_length_changed.add_subject(paginator)

    def add_sequencer(self, sequencer):
        self._MidiClipControllerComponent__on_editable_pitches_changed.add_subject(sequencer)
        self._MidiClipControllerComponent__on_row_start_times_changed.add_subject(sequencer)
        self._MidiClipControllerComponent__on_step_length_changed.add_subject(sequencer)
        self._MidiClipControllerComponent__on_selected_notes_changed.add_subject(sequencer)
        self._sequencers.append(sequencer)

    def disconnect(self):
        super(MidiClipControllerComponent, self).disconnect()
        self._visualisation_real_time_data.set_data(None)

    def update(self):
        super(MidiClipControllerComponent, self).update()
        self._update_notification_mutes()
        if self.is_enabled():
            self._MidiClipControllerComponent__on_matrix_mode_changed()

    def _on_clip_changed(self):
        self._visualisation_real_time_data.set_data(getattr(self.clip, 'proxied_object', self.clip))
        self._MidiClipControllerComponent__on_clip_color_changed.subject = self.clip
        timeline_navigation = getattr(self.clip, 'timeline_navigation', None)
        self._MidiClipControllerComponent__on_visible_region_changed.subject = timeline_navigation
        self._MidiClipControllerComponent__on_focus_marker_changed.subject = timeline_navigation
        self._MidiClipControllerComponent__on_show_focus_changed.subject = timeline_navigation

    def _focus_grid_window(self):
        if liveobj_valid(self.clip):
            if self.get_static_view_data()['ShowGridWindow']:
                self.clip.timeline_navigation.change_object(self.grid_window_focus)

    def _configure_visualisation_delayed(self):
        self._configure_vis_task.restart()

    @listens('instrument')
    def __on_drum_rack_changed(self):
        self._drum_pad_color_notifier.set_drum_group(self._drum_rack_finder.drum_group)

    @listens('enabled')
    def __on_note_settings_enabled_changed(self, _):
        self._configure_visualisation()

    @listens('is_touched')
    def __on_note_editor_settings_touched_changed(self):
        self._configure_visualisation()

    @listens_group('editing_note_regions')
    def __on_selected_notes_changed(self, sequencer):
        self._most_recent_editing_note_regions = sequencer.editing_note_regions
        self._configure_visualisation()

    @listens('channel_id')
    def __on_visualisation_channel_changed(self):
        self.notify_visualisation_real_time_channel_id()

    @listens('attached')
    def __on_visualisation_attached(self):
        self._real_time_data_attached = True
        self._configure_visualisation()

    @listens('color_index')
    def __on_clip_color_changed(self):
        self._configure_visualisation()

    @listens('visible_region')
    def __on_visible_region_changed(self, *a):
        self._configure_visualisation()

    @listens('focus_marker')
    def __on_focus_marker_changed(self, *a):
        self._configure_visualisation()

    @listens('show_focus')
    def __on_show_focus_changed(self, *a):
        self._configure_visualisation()

    @listens('matrix_mode_path')
    def __on_matrix_mode_changed(self):
        if self.is_enabled():
            if self._matrix_mode_watcher:
                static_view_data = self.get_static_view_data()
                if self.matrix_mode_path() == 'matrix_modes.note.instrument.sequence':
                    num_visible_keys = static_view_data['NumDisplayKeys']
                    lower = self._most_recent_editable_pitches[0]
                    upper = self._most_recent_editable_pitches[-1]
                    self._loose_follow_base_note = (lower + upper) // 2 - num_visible_keys // 2
                if static_view_data['ShowGridWindow']:
                    self._focus_grid_window()
                else:
                    if liveobj_valid(self.clip):
                        nav = self.clip.timeline_navigation
                        nav.set_focus_marker_without_updating_visible_region('start_marker')
                self._configure_visualisation()
                self._update_notification_mutes()

    @listens_group('position')
    def __on_instrument_position_changed(self, instrument):
        self._most_recent_base_note = instrument.min_pitch
        self._most_recent_max_note = instrument.max_pitch
        self._configure_visualisation()

    @listens('note_colors')
    def __on_note_colors_changed(self):
        self._configure_visualisation()

    @listens_group('editable_pitches')
    def __on_editable_pitches_changed(self, sequencer):
        self._most_recent_editable_pitches = sequencer.editable_pitches
        if self.is_enabled():
            self._configure_visualisation_delayed()

    @listens_group('row_start_times')
    def __on_row_start_times_changed(self, sequencer):
        if sequencer.is_enabled():
            self._most_recent_row_start_times = sequencer.row_start_times
            self._configure_visualisation_delayed()

    @listens_group('step_length')
    def __on_step_length_changed(self, sequencer):
        if sequencer.is_enabled():
            self._most_recent_step_length = sequencer.step_length
            self._configure_visualisation()

    @listens_group('page_index')
    def __on_paginator_page_index_changed(self, paginator):
        self._most_recent_page_index = paginator.page_index
        self._focus_grid_window()
        self._configure_visualisation()

    @listens_group('page_length')
    def __on_paginator_page_length_changed(self, paginator):
        self._most_recent_page_length = paginator.page_length
        self._focus_grid_window()
        self._configure_visualisation()

    def get_static_view_data(self):
        return get_static_view_data(self._matrix_mode_watcher.matrix_mode_path)

    def _add_items_to_view_data(self, view_data):
        for key, value in self.get_static_view_data().items():
            view_data[key] = value

    def matrix_mode_path(self):
        if self._matrix_mode_watcher is not None:
            return self._matrix_mode_watcher.matrix_mode_path

    def _update_notification_mutes(self):
        for component in chain(self._sequencers, self._instruments):
            if old_hasattr(component, 'show_notifications'):
                component.show_notifications = not (self.is_enabled() and self.get_static_view_data()['ShowScrollbarCursor'])

    def mute_components_during_track_change(self, muted):
        if self.is_enabled():
            for component in self._mute_during_track_change_components:
                component.muted = muted

    @contextmanager
    def changing_track(self):
        self.mute_components_during_track_change(True)
        self._real_time_data_attached = False
        yield
        self.mute_components_during_track_change(False)

    def _update_minimum_pitch(self):
        if self.matrix_mode_path() == 'matrix_modes.note.instrument.sequence':
            num_visible_keys = self.get_static_view_data()['NumDisplayKeys']
            lower = self._most_recent_editable_pitches[0]
            upper = self._most_recent_editable_pitches[-1]
            window_size = upper - lower
            base_note = self._loose_follow_base_note
            if window_size >= old_div(num_visible_keys, 3):
                base_note = old_div(lower + upper, 2) - old_div(num_visible_keys, 2)
            else:
                if lower - window_size < base_note:
                    base_note = lower - window_size
                if upper + window_size > base_note + num_visible_keys:
                    base_note = upper + window_size - num_visible_keys
            self._loose_follow_base_note = max(0, min(127 - num_visible_keys, base_note))
            return self._loose_follow_base_note
        return self._most_recent_base_note

    def _update_maximum_sequenceable_pitch(self):
        if self.matrix_mode_path() == 'matrix_modes.note.instrument.sequence':
            return self._most_recent_editable_pitches[-1]
        return self._most_recent_max_note

    def _update_minimum_sequenceable_pitch(self):
        if self.matrix_mode_path() == 'matrix_modes.note.instrument.sequence':
            return self._most_recent_editable_pitches[0]
        return self._most_recent_base_note

    def _update_note_colors(self):
        matrix_mode = self.matrix_mode_path()
        in_correct_mode = (matrix_mode is not None) and (matrix_mode.startswith('matrix_modes.note.drums')) or (matrix_mode == 'matrix_modes.session')
        if in_correct_mode:
            note_colors = self._drum_pad_color_notifier.note_colors if self._drum_pad_color_notifier.has_drum_group else []
            return make_color_vector(note_colors)

    def _configure_visualisation(self):
        visualisation = self._visualisation_real_time_data.device_visualisation()
        if liveobj_valid(visualisation):
            if liveobj_valid(self.clip):
                if self._real_time_data_attached:
                    color = COLOR_INDEX_TO_SCREEN_COLOR[self.clip.color_index]
                    visible_region = self.clip.zoom.visible_region
                    focus_marker = self.clip.timeline_navigation.focus_marker
                    new_data = {'ClipColor':color.as_remote_script_color(), 
                     'PageIndex':self._most_recent_page_index, 
                     'PageLength':float(self._most_recent_page_length), 
                     'RowStartTimes':make_vector(self._most_recent_row_start_times), 
                     'StepLength':float(self._most_recent_step_length), 
                     'MinGridWindowPitch':self._most_recent_editable_pitches[0], 
                     'MaxGridWindowPitch':self._most_recent_editable_pitches[-1], 
                     'GridWindowPitches':make_vector(self._most_recent_editable_pitches), 
                     'MinPitch':self._update_minimum_pitch(), 
                     'MaxSequenceablePitch':self._update_maximum_sequenceable_pitch(), 
                     'MinSequenceablePitch':self._update_minimum_sequenceable_pitch(), 
                     'NoteColors':self._update_note_colors(), 
                     'IsRecording':liveobj_valid(self.clip) and self.clip.is_recording and not self.clip.is_overdubbing, 
                     'NoteSettingsMode':self._note_settings_component is not None and self._note_settings_component.is_enabled(), 
                     'NoteSettingsTouched':self._note_editor_settings_component is not None and self._note_editor_settings_component.is_enabled() and self._note_editor_settings_component.is_touched, 
                     'EditingNotePitches':make_vector([pitch for pitch, (start, end) in self._most_recent_editing_note_regions]), 
                     'EditingNoteStarts':make_vector([float(start) for pitch, (start, end) in self._most_recent_editing_note_regions]), 
                     'EditingNoteEnds':make_vector([float(end) for pitch, (start, end) in self._most_recent_editing_note_regions]), 
                     'DisplayStartTime':float(visible_region.start), 
                     'DisplayEndTime':float(visible_region.end), 
                     'FocusMarkerName':focus_marker.name, 
                     'FocusMarkerPosition':focus_marker.position, 
                     'ShowFocus':self.clip.timeline_navigation.show_focus}
                    view_data = visualisation.get_view_data()
                    if self._matrix_mode_watcher is not None:
                        self._add_items_to_view_data(view_data)
                    for key, value in new_data.items():
                        view_data[key] = value

                    visualisation.set_view_data(view_data)


class ClipControlComponent(Component):
    __events__ = ('clip', )

    def __init__(self, decorator_factory=None, *a, **k):
        (super(ClipControlComponent, self).__init__)(*a, **k)
        self._clip = None
        self.midi_loop_controller = LoopSettingsControllerComponent(parent=self)
        self.audio_loop_controller = LoopSettingsControllerComponent(parent=self)
        self.audio_clip_controller = AudioClipSettingsControllerComponent(parent=self)
        self.midi_clip_controller = MidiClipControllerComponent(parent=self)
        self.mode_selector = ModesComponent(parent=self)
        self._decorator_factory = decorator_factory or ClipDecoratorFactory()
        self._ClipControlComponent__on_selected_scene_changed.subject = self.song.view
        self._ClipControlComponent__on_selected_track_changed.subject = self.song.view
        self._ClipControlComponent__on_selected_clip_changed.subject = self.song.view
        self._ClipControlComponent__on_has_clip_changed.subject = self.song.view.highlighted_clip_slot
        self._update_controller()

    @listens('selected_scene')
    def __on_selected_scene_changed(self):
        self._update_controller()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self._update_controller()

    @listens('detail_clip')
    def __on_selected_clip_changed(self):
        self._update_controller()

    def on_enabled_changed(self):
        super(ClipControlComponent, self).on_enabled_changed()
        self._update_controller()

    def _decorate_clip(self, clip):
        return find_decorated_object(clip, self._decorator_factory) or self._decorator_factory.decorate(clip)

    @listens('has_clip')
    def __on_has_clip_changed(self):
        self._update_controller()

    def _update_controller(self):
        if self.is_enabled():
            clip = self.song.view.detail_clip
            track = None
            if liveobj_valid(clip):
                if clip.is_arrangement_clip:
                    track = clip.canonical_parent
                else:
                    clip_slot = clip.canonical_parent
                    track = clip_slot.canonical_parent if clip_slot else None
            if track != self.song.view.selected_track:
                clip = None
            self._update_selected_mode(clip)
            audio_clip = None
            midi_clip = None
            if liveobj_valid(clip) and clip.is_audio_clip:
                audio_clip = clip
            else:
                midi_clip = clip
            self.audio_clip_controller.clip = audio_clip
            self.audio_loop_controller.clip = self._decorate_clip(audio_clip)
            decorated_midi_clip = self._decorate_clip(midi_clip)
            self.midi_clip_controller.clip = decorated_midi_clip
            self.midi_loop_controller.clip = decorated_midi_clip
            self._ClipControlComponent__on_has_clip_changed.subject = self.song.view.highlighted_clip_slot
            self._clip = clip
            self.notify_clip()

    def _update_selected_mode(self, clip):
        if liveobj_valid(clip):
            self.mode_selector.selected_mode = 'audio' if clip.is_audio_clip else 'midi'
        else:
            self.mode_selector.selected_mode = 'no_clip'

    @property
    def clip(self):
        return self._clip