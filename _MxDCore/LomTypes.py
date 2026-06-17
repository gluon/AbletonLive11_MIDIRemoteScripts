# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MxDCore\LomTypes.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 41307 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, range
from past.builtins import basestring
import ast, json, types
from collections import namedtuple
import Live
import _Framework.ControlElement as ControlElement
import _Framework.ControlSurface as ControlSurface
import _Framework.ControlSurfaceComponent as ControlSurfaceComponent
from _Framework.Util import is_iterable
from ableton.v2.base import PY2, old_hasattr
from _MxDCore.ControlSurfaceWrapper import ControlProxy, ControlSurfaceWrapper, is_real_control_surface

class MFLPropertyFormats(object):
    Default, JSON = (0, 1)


_MFLProperty = namedtuple('MFLProperty', 'name format to_json from_json min_epii_version')
SORT_KEYS = False

def MFLProperty(name, format=MFLPropertyFormats.Default, to_json=None, from_json=None, min_epii_version=(-1, -1)):
    return _MFLProperty(name, format, to_json, from_json, min_epii_version)


def data_dict_to_json(property_name, data_dict):
    return json.dumps({property_name: data_dict}, ensure_ascii=True, sort_keys=SORT_KEYS)


def json_to_data_dict(property_name, json_dict):
    data_dict = ast.literal_eval(json_dict)
    return data_dict.get(property_name, data_dict)


def warp_markers_to_json(obj):
    property_value = getattr(obj, 'warp_markers')
    return data_dict_to_json('warp_markers', tuple([warp_marker_to_dict(t) for t in property_value]))


def warp_marker_to_dict(warp_marker):
    return {'sample_time':warp_marker.sample_time, 
     'beat_time':warp_marker.beat_time}


def verify_routings_available_for_object(obj, prop_name):
    if isinstance(obj, Live.Track.Track):
        error_format = "'%s' not available on %s"
        song = obj.canonical_parent
        if obj == song.master_track:
            raise RuntimeError(error_format % (prop_name, 'master track'))
        else:
            if 'input' in prop_name:
                if obj.is_foldable:
                    raise RuntimeError(error_format % (prop_name, 'group tracks'))
                else:
                    if obj in song.return_tracks:
                        raise RuntimeError(error_format % (prop_name, 'return tracks'))


def routing_object_to_dict(routing_type):
    return {'display_name':routing_type.display_name, 
     'identifier':hash(routing_type)}


def available_routing_objects_to_json(obj, property_name):
    verify_routings_available_for_object(obj, property_name)
    property_value = getattr(obj, property_name)
    return data_dict_to_json(property_name, tuple([routing_object_to_dict(t) for t in property_value]))


def available_routing_input_types_to_json(obj):
    return available_routing_objects_to_json(obj, 'available_input_routing_types')


def available_routing_output_types_to_json(obj):
    return available_routing_objects_to_json(obj, 'available_output_routing_types')


def available_routing_input_channels_to_json(obj):
    return available_routing_objects_to_json(obj, 'available_input_routing_channels')


def available_routing_output_channels_to_json(obj):
    return available_routing_objects_to_json(obj, 'available_output_routing_channels')


def available_routing_types_to_json(device):
    return available_routing_objects_to_json(device, 'available_routing_types')


def available_routing_channels_to_json(device):
    return available_routing_objects_to_json(device, 'available_routing_channels')


def routing_object_to_json(obj, property_name):
    verify_routings_available_for_object(obj, property_name)
    property_value = getattr(obj, property_name)
    return data_dict_to_json(property_name, routing_object_to_dict(property_value))


def routing_input_type_to_json(obj):
    return routing_object_to_json(obj, 'input_routing_type')


def routing_output_type_to_json(obj):
    return routing_object_to_json(obj, 'output_routing_type')


def routing_input_channel_to_json(obj):
    return routing_object_to_json(obj, 'input_routing_channel')


def routing_output_channel_to_json(obj):
    return routing_object_to_json(obj, 'output_routing_channel')


def routing_type_to_json(device):
    return routing_object_to_json(device, 'routing_type')


def routing_channel_to_json(device):
    return routing_object_to_json(device, 'routing_channel')


def json_to_routing_object(obj, property_name, json_dict):
    verify_routings_available_for_object(obj, property_name)
    objects = getattr(obj, 'available_%ss' % property_name, [])
    identifier = json_to_data_dict(property_name, json_dict)['identifier']
    for routing_object in objects:
        if hash(routing_object) == identifier:
            return routing_object


def json_to_input_routing_type(obj, json_dict):
    return json_to_routing_object(obj, 'input_routing_type', json_dict)


def json_to_output_routing_type(obj, json_dict):
    return json_to_routing_object(obj, 'output_routing_type', json_dict)


def json_to_input_routing_channel(obj, json_dict):
    return json_to_routing_object(obj, 'input_routing_channel', json_dict)


def json_to_output_routing_channel(obj, json_dict):
    return json_to_routing_object(obj, 'output_routing_channel', json_dict)


def json_to_routing_type(device, json_dict):
    return json_to_routing_object(device, 'routing_type', json_dict)


def json_to_routing_channel(device, json_dict):
    return json_to_routing_object(device, 'routing_channel', json_dict)


_DEVICE_BASE_PROPS = [
 MFLProperty('can_have_chains'),
 MFLProperty('can_have_drum_pads'),
 MFLProperty('canonical_parent'),
 MFLProperty('class_display_name'),
 MFLProperty('class_name'),
 MFLProperty('is_active'),
 MFLProperty('latency_in_ms'),
 MFLProperty('latency_in_samples'),
 MFLProperty('name'),
 MFLProperty('parameters'),
 MFLProperty('store_chosen_bank'),
 MFLProperty('type'),
 MFLProperty('view')]
_DEVICE_VIEW_BASE_PROPS = [
 MFLProperty('canonical_parent'), MFLProperty('is_collapsed')]
_CHAIN_BASE_PROPS = [
 MFLProperty('canonical_parent'),
 MFLProperty('color'),
 MFLProperty('color_index'),
 MFLProperty('delete_device'),
 MFLProperty('devices'),
 MFLProperty('has_audio_input'),
 MFLProperty('has_audio_output'),
 MFLProperty('has_midi_input'),
 MFLProperty('has_midi_output'),
 MFLProperty('is_auto_colored'),
 MFLProperty('mixer_device'),
 MFLProperty('mute'),
 MFLProperty('muted_via_solo'),
 MFLProperty('name'),
 MFLProperty('solo')]
EXPOSED_TYPE_PROPERTIES = {Live.Application.Application: (
                                MFLProperty('control_surfaces'),
                                MFLProperty('current_dialog_button_count'),
                                MFLProperty('current_dialog_message'),
                                MFLProperty('get_bugfix_version'),
                                MFLProperty('get_document'),
                                MFLProperty('get_version_string'),
                                MFLProperty('get_major_version'),
                                MFLProperty('get_minor_version'),
                                MFLProperty('open_dialog_count'),
                                MFLProperty('press_current_dialog_button'),
                                MFLProperty('average_process_usage'),
                                MFLProperty('peak_process_usage'),
                                MFLProperty('view')), 
 
 Live.Application.Application.View: (
                                     MFLProperty('available_main_views'),
                                     MFLProperty('browse_mode'),
                                     MFLProperty('canonical_parent'),
                                     MFLProperty('focus_view'),
                                     MFLProperty('focused_document_view'),
                                     MFLProperty('hide_view'),
                                     MFLProperty('is_view_visible'),
                                     MFLProperty('scroll_view'),
                                     MFLProperty('show_view'),
                                     MFLProperty('toggle_browse'),
                                     MFLProperty('zoom_view')), 
 
 Live.Chain.Chain: tuple(_CHAIN_BASE_PROPS), 
 Live.ChainMixerDevice.ChainMixerDevice: (
                                          MFLProperty('canonical_parent'),
                                          MFLProperty('chain_activator'),
                                          MFLProperty('panning'),
                                          MFLProperty('sends'),
                                          MFLProperty('volume')), 
 
 Live.Clip.Clip: (
                  MFLProperty('add_new_notes', min_epii_version=(4, 3)),
                  MFLProperty('add_warp_marker', min_epii_version=(4, 3)),
                  MFLProperty('apply_note_modifications', min_epii_version=(4, 3)),
                  MFLProperty('available_warp_modes'),
                  MFLProperty('canonical_parent'),
                  MFLProperty('clear_all_envelopes'),
                  MFLProperty('clear_envelope'),
                  MFLProperty('color'),
                  MFLProperty('color_index'),
                  MFLProperty('crop'),
                  MFLProperty('deselect_all_notes'),
                  MFLProperty('duplicate_loop'),
                  MFLProperty('duplicate_notes_by_id'),
                  MFLProperty('duplicate_region'),
                  MFLProperty('end_marker'),
                  MFLProperty('end_time'),
                  MFLProperty('file_path'),
                  MFLProperty('fire'),
                  MFLProperty('gain'),
                  MFLProperty('gain_display_string'),
                  MFLProperty('get_all_notes_extended'),
                  MFLProperty('get_notes'),
                  MFLProperty('get_notes_by_id', min_epii_version=(4, 3)),
                  MFLProperty('get_notes_extended', min_epii_version=(4, 3)),
                  MFLProperty('get_selected_notes'),
                  MFLProperty('get_selected_notes_extended', min_epii_version=(4, 3)),
                  MFLProperty('groove'),
                  MFLProperty('has_envelopes'),
                  MFLProperty('has_groove'),
                  MFLProperty('is_arrangement_clip'),
                  MFLProperty('is_audio_clip'),
                  MFLProperty('is_midi_clip'),
                  MFLProperty('is_overdubbing'),
                  MFLProperty('is_playing'),
                  MFLProperty('is_recording'),
                  MFLProperty('is_triggered'),
                  MFLProperty('launch_mode'),
                  MFLProperty('launch_quantization'),
                  MFLProperty('legato'),
                  MFLProperty('length'),
                  MFLProperty('loop_end'),
                  MFLProperty('loop_start'),
                  MFLProperty('looping'),
                  MFLProperty('move_playing_pos'),
                  MFLProperty('move_warp_marker'),
                  MFLProperty('muted'),
                  MFLProperty('name'),
                  MFLProperty('pitch_coarse'),
                  MFLProperty('pitch_fine'),
                  MFLProperty('playing_position'),
                  MFLProperty('position'),
                  MFLProperty('quantize'),
                  MFLProperty('quantize_pitch'),
                  MFLProperty('ram_mode'),
                  MFLProperty('remove_notes'),
                  MFLProperty('remove_notes_by_id', min_epii_version=(4, 3)),
                  MFLProperty('remove_notes_extended', min_epii_version=(4, 3)),
                  MFLProperty('remove_warp_marker'),
                  MFLProperty('replace_selected_notes'),
                  MFLProperty('sample_length'),
                  MFLProperty('sample_rate'),
                  MFLProperty('scrub'),
                  MFLProperty('select_all_notes'),
                  MFLProperty('select_notes_by_id'),
                  MFLProperty('set_fire_button_state'),
                  MFLProperty('set_notes'),
                  MFLProperty('signature_denominator'),
                  MFLProperty('signature_numerator'),
                  MFLProperty('start_marker'),
                  MFLProperty('start_time'),
                  MFLProperty('stop'),
                  MFLProperty('stop_scrub'),
                  MFLProperty('velocity_amount'),
                  MFLProperty('view'),
                  MFLProperty('warp_markers',
                    format=(MFLPropertyFormats.JSON),
                    to_json=warp_markers_to_json,
                    min_epii_version=(4, 3)),
                  MFLProperty('warp_mode'),
                  MFLProperty('warping'),
                  MFLProperty('will_record_on_start')), 
 
 Live.Clip.Clip.View: (
                       MFLProperty('canonical_parent'),
                       MFLProperty('grid_is_triplet'),
                       MFLProperty('grid_quantization'),
                       MFLProperty('hide_envelope'),
                       MFLProperty('select_envelope_parameter'),
                       MFLProperty('show_envelope'),
                       MFLProperty('show_loop')), 
 
 Live.Groove.Groove: (
                      MFLProperty('base'),
                      MFLProperty('canonical_parent'),
                      MFLProperty('name'),
                      MFLProperty('quantization_amount'),
                      MFLProperty('random_amount'),
                      MFLProperty('timing_amount'),
                      MFLProperty('velocity_amount')), 
 
 Live.ClipSlot.ClipSlot: (
                          MFLProperty('canonical_parent'),
                          MFLProperty('clip'),
                          MFLProperty('color'),
                          MFLProperty('color_index'),
                          MFLProperty('controls_other_clips'),
                          MFLProperty('create_clip'),
                          MFLProperty('delete_clip'),
                          MFLProperty('duplicate_clip_to'),
                          MFLProperty('fire'),
                          MFLProperty('has_clip'),
                          MFLProperty('has_stop_button'),
                          MFLProperty('is_group_slot'),
                          MFLProperty('is_playing'),
                          MFLProperty('is_recording'),
                          MFLProperty('is_triggered'),
                          MFLProperty('playing_status'),
                          MFLProperty('set_fire_button_state'),
                          MFLProperty('stop'),
                          MFLProperty('will_record_on_start')), 
 
 Live.CompressorDevice.CompressorDevice: tuple(_DEVICE_BASE_PROPS + [
                                          MFLProperty('available_input_routing_channels',
                                            format=(MFLPropertyFormats.JSON),
                                            to_json=available_routing_input_channels_to_json,
                                            min_epii_version=(4, 3)),
                                          MFLProperty('available_input_routing_types',
                                            format=(MFLPropertyFormats.JSON),
                                            to_json=available_routing_input_types_to_json,
                                            min_epii_version=(4, 3)),
                                          MFLProperty('input_routing_channel',
                                            format=(MFLPropertyFormats.JSON),
                                            to_json=routing_input_channel_to_json,
                                            from_json=json_to_input_routing_channel,
                                            min_epii_version=(4, 3)),
                                          MFLProperty('input_routing_type',
                                            format=(MFLPropertyFormats.JSON),
                                            to_json=routing_input_type_to_json,
                                            from_json=json_to_input_routing_type,
                                            min_epii_version=(4, 3))]), 
 
 Live.Device.Device: tuple(_DEVICE_BASE_PROPS), 
 Live.Device.Device.View: tuple(_DEVICE_VIEW_BASE_PROPS), 
 Live.DeviceParameter.DeviceParameter: (
                                        MFLProperty('__str__'),
                                        MFLProperty('automation_state'),
                                        MFLProperty('canonical_parent'),
                                        MFLProperty('default_value'),
                                        MFLProperty('is_enabled'),
                                        MFLProperty('is_quantized'),
                                        MFLProperty('max'),
                                        MFLProperty('min'),
                                        MFLProperty('name'),
                                        MFLProperty('original_name'),
                                        MFLProperty('re_enable_automation'),
                                        MFLProperty('state'),
                                        MFLProperty('str_for_value'),
                                        MFLProperty('value'),
                                        MFLProperty('value_items')), 
 
 Live.DeviceIO.DeviceIO: (
                          MFLProperty('available_routing_channels',
                            format=(MFLPropertyFormats.JSON),
                            to_json=available_routing_channels_to_json,
                            min_epii_version=(4, 4)),
                          MFLProperty('available_routing_types',
                            format=(MFLPropertyFormats.JSON),
                            to_json=available_routing_types_to_json,
                            min_epii_version=(4, 4)),
                          MFLProperty('canonical_parent'),
                          MFLProperty('default_external_routing_channel_is_none'),
                          MFLProperty('routing_channel',
                            format=(MFLPropertyFormats.JSON),
                            to_json=routing_channel_to_json,
                            from_json=json_to_routing_channel,
                            min_epii_version=(4, 4)),
                          MFLProperty('routing_type',
                            format=(MFLPropertyFormats.JSON),
                            to_json=routing_type_to_json,
                            from_json=json_to_routing_type,
                            min_epii_version=(4, 4))), 
 
 Live.DrumChain.DrumChain: tuple(_CHAIN_BASE_PROPS + [MFLProperty('out_note'), MFLProperty('choke_group')]), 
 
 Live.DrumPad.DrumPad: (
                        MFLProperty('canonical_parent'),
                        MFLProperty('chains'),
                        MFLProperty('delete_all_chains'),
                        MFLProperty('mute'),
                        MFLProperty('name'),
                        MFLProperty('note'),
                        MFLProperty('solo')), 
 
 Live.Eq8Device.Eq8Device: tuple(_DEVICE_BASE_PROPS + [
                            MFLProperty('edit_mode'),
                            MFLProperty('global_mode'),
                            MFLProperty('oversample')]), 
 
 Live.Eq8Device.Eq8Device.View: tuple(_DEVICE_VIEW_BASE_PROPS + [MFLProperty('selected_band')]), 
 
 Live.DriftDevice.DriftDevice: tuple(_DEVICE_BASE_PROPS), 
 Live.HybridReverbDevice.HybridReverbDevice: tuple(_DEVICE_BASE_PROPS + [
                                              MFLProperty('ir_attack_time'),
                                              MFLProperty('ir_category_index'),
                                              MFLProperty('ir_category_list'),
                                              MFLProperty('ir_decay_time'),
                                              MFLProperty('ir_file_index'),
                                              MFLProperty('ir_file_list'),
                                              MFLProperty('ir_size_factor'),
                                              MFLProperty('ir_time_shaping_on')]), 
 
 Live.MaxDevice.MaxDevice: tuple(_DEVICE_BASE_PROPS + [
                            MFLProperty('audio_inputs'),
                            MFLProperty('audio_outputs'),
                            MFLProperty('get_bank_count'),
                            MFLProperty('get_bank_name'),
                            MFLProperty('get_bank_parameters'),
                            MFLProperty('midi_inputs'),
                            MFLProperty('midi_outputs')]), 
 
 Live.MixerDevice.MixerDevice: (
                                MFLProperty('canonical_parent'),
                                MFLProperty('crossfade_assign'),
                                MFLProperty('crossfader'),
                                MFLProperty('cue_volume'),
                                MFLProperty('left_split_stereo'),
                                MFLProperty('panning'),
                                MFLProperty('panning_mode'),
                                MFLProperty('right_split_stereo'),
                                MFLProperty('sends'),
                                MFLProperty('song_tempo'),
                                MFLProperty('track_activator'),
                                MFLProperty('volume')), 
 
 Live.PluginDevice.PluginDevice: tuple(_DEVICE_BASE_PROPS + [
                                  MFLProperty('presets'), MFLProperty('selected_preset_index')]), 
 
 Live.RackDevice.RackDevice: tuple(_DEVICE_BASE_PROPS + [
                              MFLProperty('add_macro'),
                              MFLProperty('can_show_chains'),
                              MFLProperty('chain_selector'),
                              MFLProperty('chains'),
                              MFLProperty('copy_pad'),
                              MFLProperty('delete_selected_variation'),
                              MFLProperty('drum_pads'),
                              MFLProperty('has_drum_pads'),
                              MFLProperty('has_macro_mappings'),
                              MFLProperty('is_showing_chains'),
                              MFLProperty('randomize_macros'),
                              MFLProperty('recall_last_used_variation'),
                              MFLProperty('recall_selected_variation'),
                              MFLProperty('remove_macro'),
                              MFLProperty('return_chains'),
                              MFLProperty('selected_variation_index'),
                              MFLProperty('store_variation'),
                              MFLProperty('variation_count'),
                              MFLProperty('visible_drum_pads'),
                              MFLProperty('visible_macro_count')]), 
 
 Live.RackDevice.RackDevice.View: tuple(_DEVICE_VIEW_BASE_PROPS + [
                                   MFLProperty('drum_pads_scroll_position'),
                                   MFLProperty('is_showing_chain_devices'),
                                   MFLProperty('selected_chain'),
                                   MFLProperty('selected_drum_pad')]), 
 
 Live.Sample.Sample: (
                      MFLProperty('beats_granulation_resolution'),
                      MFLProperty('beats_transient_envelope'),
                      MFLProperty('beats_transient_loop_mode'),
                      MFLProperty('canonical_parent'),
                      MFLProperty('clear_slices'),
                      MFLProperty('complex_pro_envelope'),
                      MFLProperty('complex_pro_formants'),
                      MFLProperty('end_marker'),
                      MFLProperty('file_path'),
                      MFLProperty('gain'),
                      MFLProperty('gain_display_string'),
                      MFLProperty('insert_slice'),
                      MFLProperty('length'),
                      MFLProperty('move_slice'),
                      MFLProperty('remove_slice'),
                      MFLProperty('reset_slices'),
                      MFLProperty('sample_rate'),
                      MFLProperty('slices'),
                      MFLProperty('slicing_beat_division'),
                      MFLProperty('slicing_region_count'),
                      MFLProperty('slicing_sensitivity'),
                      MFLProperty('slicing_style'),
                      MFLProperty('start_marker'),
                      MFLProperty('texture_flux'),
                      MFLProperty('texture_grain_size'),
                      MFLProperty('tones_grain_size'),
                      MFLProperty('warp_mode'),
                      MFLProperty('warp_markers',
                        format=(MFLPropertyFormats.JSON),
                        to_json=warp_markers_to_json,
                        min_epii_version=(4, 3)),
                      MFLProperty('warping')), 
 
 Live.Scene.Scene: (
                    MFLProperty('canonical_parent'),
                    MFLProperty('clip_slots'),
                    MFLProperty('color'),
                    MFLProperty('color_index'),
                    MFLProperty('fire'),
                    MFLProperty('fire_as_selected'),
                    MFLProperty('is_empty'),
                    MFLProperty('is_triggered'),
                    MFLProperty('name'),
                    MFLProperty('set_fire_button_state'),
                    MFLProperty('tempo'),
                    MFLProperty('tempo_enabled'),
                    MFLProperty('time_signature_numerator'),
                    MFLProperty('time_signature_denominator'),
                    MFLProperty('time_signature_enabled')), 
 
 Live.ShifterDevice.ShifterDevice: tuple(_DEVICE_BASE_PROPS + [
                                    MFLProperty('pitch_bend_range'), MFLProperty('pitch_mode_index')]), 
 
 Live.SimplerDevice.SimplerDevice: tuple(_DEVICE_BASE_PROPS + [
                                    MFLProperty('can_warp_as'),
                                    MFLProperty('can_warp_double'),
                                    MFLProperty('can_warp_half'),
                                    MFLProperty('crop'),
                                    MFLProperty('guess_playback_length'),
                                    MFLProperty('multi_sample_mode'),
                                    MFLProperty('pad_slicing'),
                                    MFLProperty('playback_mode'),
                                    MFLProperty('playing_position'),
                                    MFLProperty('playing_position_enabled'),
                                    MFLProperty('retrigger'),
                                    MFLProperty('reverse'),
                                    MFLProperty('sample'),
                                    MFLProperty('slicing_playback_mode'),
                                    MFLProperty('voices'),
                                    MFLProperty('warp_as'),
                                    MFLProperty('warp_double'),
                                    MFLProperty('warp_half')]), 
 
 Live.SimplerDevice.SimplerDevice.View: tuple(_DEVICE_VIEW_BASE_PROPS + [MFLProperty('selected_slice')]), 
 
 Live.Song.Song: (
                  MFLProperty('appointed_device'),
                  MFLProperty('arrangement_overdub'),
                  MFLProperty('back_to_arranger'),
                  MFLProperty('can_capture_midi'),
                  MFLProperty('can_jump_to_next_cue'),
                  MFLProperty('can_jump_to_prev_cue'),
                  MFLProperty('can_redo'),
                  MFLProperty('can_undo'),
                  MFLProperty('capture_and_insert_scene'),
                  MFLProperty('capture_midi'),
                  MFLProperty('clip_trigger_quantization'),
                  MFLProperty('continue_playing'),
                  MFLProperty('count_in_duration'),
                  MFLProperty('create_audio_track'),
                  MFLProperty('create_midi_track'),
                  MFLProperty('create_return_track'),
                  MFLProperty('create_scene'),
                  MFLProperty('cue_points'),
                  MFLProperty('current_song_time'),
                  MFLProperty('delete_return_track'),
                  MFLProperty('delete_scene'),
                  MFLProperty('delete_track'),
                  MFLProperty('duplicate_scene'),
                  MFLProperty('duplicate_track'),
                  MFLProperty('exclusive_arm'),
                  MFLProperty('exclusive_solo'),
                  MFLProperty('find_device_position'),
                  MFLProperty('force_link_beat_time'),
                  MFLProperty('get_beats_loop_length'),
                  MFLProperty('get_beats_loop_start'),
                  MFLProperty('get_current_beats_song_time'),
                  MFLProperty('get_current_smpte_song_time'),
                  MFLProperty('groove_amount'),
                  MFLProperty('groove_pool'),
                  MFLProperty('is_ableton_link_enabled'),
                  MFLProperty('is_ableton_link_start_stop_sync_enabled'),
                  MFLProperty('is_counting_in'),
                  MFLProperty('is_cue_point_selected'),
                  MFLProperty('is_playing'),
                  MFLProperty('jump_by'),
                  MFLProperty('jump_to_next_cue'),
                  MFLProperty('jump_to_prev_cue'),
                  MFLProperty('last_event_time'),
                  MFLProperty('loop'),
                  MFLProperty('loop_length'),
                  MFLProperty('loop_start'),
                  MFLProperty('master_track'),
                  MFLProperty('metronome'),
                  MFLProperty('midi_recording_quantization'),
                  MFLProperty('move_device'),
                  MFLProperty('nudge_down'),
                  MFLProperty('nudge_up'),
                  MFLProperty('tempo_follower_enabled'),
                  MFLProperty('overdub'),
                  MFLProperty('play_selection'),
                  MFLProperty('punch_in'),
                  MFLProperty('punch_out'),
                  MFLProperty('re_enable_automation'),
                  MFLProperty('re_enable_automation_enabled'),
                  MFLProperty('record_mode'),
                  MFLProperty('redo'),
                  MFLProperty('return_tracks'),
                  MFLProperty('root_note'),
                  MFLProperty('scale_intervals'),
                  MFLProperty('scale_name'),
                  MFLProperty('scenes'),
                  MFLProperty('scrub_by'),
                  MFLProperty('select_on_launch'),
                  MFLProperty('session_automation_record'),
                  MFLProperty('session_record'),
                  MFLProperty('session_record_status'),
                  MFLProperty('set_or_delete_cue'),
                  MFLProperty('signature_denominator'),
                  MFLProperty('signature_numerator'),
                  MFLProperty('song_length'),
                  MFLProperty('start_playing'),
                  MFLProperty('start_time'),
                  MFLProperty('stop_all_clips'),
                  MFLProperty('stop_playing'),
                  MFLProperty('swing_amount'),
                  MFLProperty('tap_tempo'),
                  MFLProperty('tempo'),
                  MFLProperty('tracks'),
                  MFLProperty('trigger_session_record'),
                  MFLProperty('undo'),
                  MFLProperty('view'),
                  MFLProperty('visible_tracks')), 
 
 Live.Song.Song.View: (
                       MFLProperty('canonical_parent'),
                       MFLProperty('detail_clip'),
                       MFLProperty('draw_mode'),
                       MFLProperty('follow_song'),
                       MFLProperty('highlighted_clip_slot'),
                       MFLProperty('select_device'),
                       MFLProperty('selected_chain'),
                       MFLProperty('selected_parameter'),
                       MFLProperty('selected_scene'),
                       MFLProperty('selected_track')), 
 
 Live.GroovePool.GroovePool: (MFLProperty('canonical_parent'), MFLProperty('grooves')), 
 Live.Song.CuePoint: (
                      MFLProperty('canonical_parent'),
                      MFLProperty('jump'),
                      MFLProperty('name'),
                      MFLProperty('time')), 
 
 Live.Track.Track: (
                    MFLProperty('arm'),
                    MFLProperty('arrangement_clips'),
                    MFLProperty('available_input_routing_channels',
                      format=(MFLPropertyFormats.JSON),
                      to_json=available_routing_input_channels_to_json,
                      min_epii_version=(4, 3)),
                    MFLProperty('available_input_routing_types',
                      format=(MFLPropertyFormats.JSON),
                      to_json=available_routing_input_types_to_json,
                      min_epii_version=(4, 3)),
                    MFLProperty('available_output_routing_channels',
                      format=(MFLPropertyFormats.JSON),
                      to_json=available_routing_output_channels_to_json,
                      min_epii_version=(4, 3)),
                    MFLProperty('available_output_routing_types',
                      format=(MFLPropertyFormats.JSON),
                      to_json=available_routing_output_types_to_json,
                      min_epii_version=(4, 3)),
                    MFLProperty('can_be_armed'),
                    MFLProperty('can_be_frozen'),
                    MFLProperty('can_show_chains'),
                    MFLProperty('canonical_parent'),
                    MFLProperty('clip_slots'),
                    MFLProperty('color'),
                    MFLProperty('color_index'),
                    MFLProperty('current_input_routing'),
                    MFLProperty('current_input_sub_routing'),
                    MFLProperty('current_monitoring_state'),
                    MFLProperty('current_output_routing'),
                    MFLProperty('current_output_sub_routing'),
                    MFLProperty('delete_clip'),
                    MFLProperty('delete_device'),
                    MFLProperty('devices'),
                    MFLProperty('duplicate_clip_slot'),
                    MFLProperty('duplicate_clip_to_arrangement'),
                    MFLProperty('fired_slot_index'),
                    MFLProperty('fold_state'),
                    MFLProperty('group_track'),
                    MFLProperty('has_audio_input'),
                    MFLProperty('has_audio_output'),
                    MFLProperty('has_midi_input'),
                    MFLProperty('has_midi_output'),
                    MFLProperty('implicit_arm'),
                    MFLProperty('input_meter_left'),
                    MFLProperty('input_meter_level'),
                    MFLProperty('input_meter_right'),
                    MFLProperty('input_routing_channel',
                      format=(MFLPropertyFormats.JSON),
                      to_json=routing_input_channel_to_json,
                      from_json=json_to_input_routing_channel,
                      min_epii_version=(4, 3)),
                    MFLProperty('input_routing_type',
                      format=(MFLPropertyFormats.JSON),
                      to_json=routing_input_type_to_json,
                      from_json=json_to_input_routing_type,
                      min_epii_version=(4, 3)),
                    MFLProperty('input_routings'),
                    MFLProperty('input_sub_routings'),
                    MFLProperty('is_foldable'),
                    MFLProperty('is_frozen'),
                    MFLProperty('is_grouped'),
                    MFLProperty('is_part_of_selection'),
                    MFLProperty('is_showing_chains'),
                    MFLProperty('is_visible'),
                    MFLProperty('jump_in_running_session_clip'),
                    MFLProperty('mixer_device'),
                    MFLProperty('mute'),
                    MFLProperty('muted_via_solo'),
                    MFLProperty('name'),
                    MFLProperty('output_meter_left'),
                    MFLProperty('output_meter_level'),
                    MFLProperty('output_meter_right'),
                    MFLProperty('output_routing_channel',
                      format=(MFLPropertyFormats.JSON),
                      to_json=routing_output_channel_to_json,
                      from_json=json_to_output_routing_channel,
                      min_epii_version=(4, 3)),
                    MFLProperty('output_routing_type',
                      format=(MFLPropertyFormats.JSON),
                      to_json=routing_output_type_to_json,
                      from_json=json_to_output_routing_type,
                      min_epii_version=(4, 3)),
                    MFLProperty('output_routings'),
                    MFLProperty('output_sub_routings'),
                    MFLProperty('performance_impact'),
                    MFLProperty('playing_slot_index'),
                    MFLProperty('solo'),
                    MFLProperty('stop_all_clips'),
                    MFLProperty('view')), 
 
 Live.Track.Track.View: (
                         MFLProperty('canonical_parent'),
                         MFLProperty('device_insert_mode'),
                         MFLProperty('is_collapsed'),
                         MFLProperty('select_instrument'),
                         MFLProperty('selected_device')), 
 
 Live.SpectralResonatorDevice.SpectralResonatorDevice: tuple(_DEVICE_BASE_PROPS + [
                                                        MFLProperty('frequency_dial_mode'),
                                                        MFLProperty('midi_gate'),
                                                        MFLProperty('mod_mode'),
                                                        MFLProperty('mono_poly'),
                                                        MFLProperty('pitch_mode'),
                                                        MFLProperty('pitch_bend_range'),
                                                        MFLProperty('polyphony')]), 
 
 Live.WavetableDevice.WavetableDevice: tuple(_DEVICE_BASE_PROPS + [
                                        MFLProperty('add_parameter_to_modulation_matrix'),
                                        MFLProperty('filter_routing'),
                                        MFLProperty('get_modulation_target_parameter_name'),
                                        MFLProperty('get_modulation_value'),
                                        MFLProperty('is_parameter_modulatable'),
                                        MFLProperty('mono_poly'),
                                        MFLProperty('oscillator_1_effect_mode'),
                                        MFLProperty('oscillator_1_wavetable_category'),
                                        MFLProperty('oscillator_1_wavetable_index'),
                                        MFLProperty('oscillator_1_wavetables'),
                                        MFLProperty('oscillator_2_effect_mode'),
                                        MFLProperty('oscillator_2_wavetable_category'),
                                        MFLProperty('oscillator_2_wavetable_index'),
                                        MFLProperty('oscillator_2_wavetables'),
                                        MFLProperty('oscillator_wavetable_categories'),
                                        MFLProperty('poly_voices'),
                                        MFLProperty('set_modulation_value'),
                                        MFLProperty('unison_mode'),
                                        MFLProperty('unison_voice_count'),
                                        MFLProperty('visible_modulation_target_names')])}
PROPERTY_NAMES_EXCLUDED_FROM_DOCUMENTATION = ('canonical_parent', )
EXTRA_CS_FUNCTIONS = ('get_control', 'get_control_names', 'grab_control', 'grab_midi',
                      'release_control', 'release_midi', 'send_midi', 'send_receive_sysex')
ENUM_TYPES = (
 Live.Song.Quantization,
 Live.Song.RecordingQuantization,
 Live.Song.CaptureMode,
 Live.Clip.GridQuantization,
 Live.DeviceParameter.AutomationState,
 Live.Groove.Base,
 Live.Sample.SlicingStyle,
 Live.Sample.SlicingBeatDivision)
TUPLE_TYPES = {'arrangement_clips':Live.Clip.Clip, 
 'audio_inputs':Live.DeviceIO.DeviceIO, 
 'audio_outputs':Live.DeviceIO.DeviceIO, 
 'chains':Live.Chain.Chain, 
 'clip_slots':Live.ClipSlot.ClipSlot, 
 'components':ControlSurfaceComponent, 
 'control_surfaces':ControlSurface, 
 'controls':ControlElement, 
 'cue_points':Live.Song.CuePoint, 
 'devices':Live.Device.Device, 
 'drum_pads':Live.DrumPad.DrumPad, 
 'grooves':Live.Groove.Groove, 
 'midi_inputs':Live.DeviceIO.DeviceIO, 
 'midi_outputs':Live.DeviceIO.DeviceIO, 
 'parameters':Live.DeviceParameter.DeviceParameter, 
 'return_chains':Live.Chain.Chain, 
 'return_tracks':Live.Track.Track, 
 'scenes':Live.Scene.Scene, 
 'sends':Live.DeviceParameter.DeviceParameter, 
 'tracks':Live.Track.Track, 
 'visible_drum_pads':Live.DrumPad.DrumPad, 
 'visible_tracks':Live.Track.Track}
PROPERTY_TYPES = {'chain_activator':Live.DeviceParameter.DeviceParameter, 
 'chain_selector':Live.DeviceParameter.DeviceParameter, 
 'clip':Live.Clip.Clip, 
 'crossfader':Live.DeviceParameter.DeviceParameter, 
 'cue_volume':Live.DeviceParameter.DeviceParameter, 
 'detail_clip':Live.Clip.Clip, 
 'groove':Live.Groove.Groove, 
 'groove_pool':Live.GroovePool.GroovePool, 
 'group_track':Live.Track.Track, 
 'highlighted_clip_slot':Live.ClipSlot.ClipSlot, 
 'left_split_stereo':Live.DeviceParameter.DeviceParameter, 
 'master_track':Live.Track.Track, 
 'mixer_device':(
  Live.MixerDevice.MixerDevice,
  Live.ChainMixerDevice.ChainMixerDevice), 
 'panning':Live.DeviceParameter.DeviceParameter, 
 'right_split_stereo':Live.DeviceParameter.DeviceParameter, 
 'sample':Live.Sample.Sample, 
 'selected_chain':Live.Chain.Chain, 
 'selected_device':Live.Device.Device, 
 'selected_drum_pad':Live.DrumPad.DrumPad, 
 'selected_parameter':Live.DeviceParameter.DeviceParameter, 
 'selected_scene':Live.Scene.Scene, 
 'selected_track':Live.Track.Track, 
 'song_tempo':Live.DeviceParameter.DeviceParameter, 
 'track_activator':Live.DeviceParameter.DeviceParameter, 
 'volume':Live.DeviceParameter.DeviceParameter, 
 'view':(
  Live.Application.Application.View,
  Live.Song.Song.View,
  Live.Track.Track.View,
  Live.Device.Device.View,
  Live.RackDevice.RackDevice.View,
  Live.Clip.Clip.View)}
LIVE_APP = 'live_app'
LIVE_SET = 'live_set'
CONTROL_SURFACES = 'control_surfaces'
THIS_DEVICE = 'this_device'
ROOT_KEYS = (
 THIS_DEVICE, CONTROL_SURFACES, LIVE_APP, LIVE_SET)

class LomAttributeError(AttributeError):
    pass


class LomObjectError(AttributeError):
    pass


class LomNoteOperationWarning(Exception):
    pass


class LomNoteOperationError(AttributeError):
    pass


def get_exposed_lom_types():
    return list(EXPOSED_TYPE_PROPERTIES.keys())


def get_exposed_properties_for_type(lom_type, epii_version=None):
    if epii_version is None:
        epii_version = (
         float('inf'), float('inf'))
    return [prop for prop in EXPOSED_TYPE_PROPERTIES.get(lom_type, []) if epii_version >= prop.min_epii_version]


def get_exposed_property_names_for_type(lom_type, epii_version=None):
    return [prop.name for prop in get_exposed_properties_for_type(lom_type, epii_version)]


def is_property_exposed_for_type(property_name, lom_type, epii_version):
    return property_name in get_exposed_property_names_for_type(lom_type, epii_version)


def get_exposed_property_info(lom_type, property_name, epii_version):
    properties = get_exposed_properties_for_type(lom_type, epii_version)
    prop = [p for p in properties if p.name == property_name]
    if not prop:
        return
    return prop[0]


def get_exposed_properties_to_document_for_type(lom_type):
    properties = set(get_exposed_property_names_for_type(lom_type))
    if issubclass(lom_type, Live.Device.Device):
        if lom_type != Live.Device.Device:
            properties -= {prop.name for prop in _DEVICE_BASE_PROPS}
    if issubclass(lom_type, Live.Chain.Chain):
        if lom_type != Live.Chain.Chain:
            properties -= {prop.name for prop in _CHAIN_BASE_PROPS}
    if issubclass(lom_type, Live.Device.Device.View):
        if lom_type != Live.Device.Device.View:
            properties -= {prop.name for prop in _DEVICE_VIEW_BASE_PROPS}
    properties -= set(PROPERTY_NAMES_EXCLUDED_FROM_DOCUMENTATION)
    return list(properties)


def is_class(class_object):
    return isinstance(class_object, type) or old_hasattr(class_object, '__bases__')


def get_control_surfaces():
    return tuple(filter(lambda c: c is not None
, Live.Application.get_application().control_surfaces))


def get_root_prop(external_device, prop_key):
    root_properties = {LIVE_APP: Live.Application.get_application, 
     LIVE_SET: lambda: Live.Application.get_application().get_document()
, 
     CONTROL_SURFACES: get_control_surfaces}
    if prop_key == THIS_DEVICE:
        return external_device
    return root_properties[prop_key]()


def cs_base_classes():
    import _Framework.ControlElement as ControlElement
    import _Framework.ControlSurfaceComponent as ControlSurfaceComponent
    from ableton.v2.control_surface import Component as ControlSurfaceComponent2
    from ableton.v2.control_surface import ControlElement as ControlElement2
    from ableton.v3.control_surface import Component as ControlSurfaceComponent3
    return (
     ControlProxy,
     ControlSurfaceWrapper,
     ControlSurfaceComponent,
     ControlElement,
     ControlSurfaceComponent2,
     ControlElement2,
     ControlSurfaceComponent3)


def is_control_surface(lom_object):
    return isinstance(lom_object, ControlSurfaceWrapper)


def is_lom_object(lom_object, lom_classes):
    return isinstance(lom_object, tuple(lom_classes) + (type(None),)) or isinstance(lom_object, cs_base_classes()) or isinstance(lom_object, Live.Base.Vector)


def is_cplusplus_lom_object(lom_object):
    return isinstance(lom_object, Live.LomObject.LomObject)


def is_object_iterable(obj):
    return not isinstance(obj, basestring) and is_iterable(obj) and not isinstance(obj, cs_base_classes())


def verify_object_property(lom_object, property_name, epii_version):
    raise_error = False
    if isinstance(lom_object, cs_base_classes()):
        if not old_hasattr(lom_object, property_name):
            raise_error = True
    else:
        if not is_property_exposed_for_type(property_name, type(lom_object), epii_version):
            raise_error = True
    if raise_error:
        raise LomAttributeError("'%s' object has no attribute '%s'" % (
         lom_object.__class__.__name__, property_name))