#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_MxDCore/LomTypes.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from past.builtins import basestring
from builtins import object
import ast
from collections import namedtuple
import json
import types
import Live
from ableton.v2.base import old_hasattr, PY2
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ControlElement import ControlElement
from _Framework.Util import is_iterable

class MFLPropertyFormats(object):
    Default, JSON = (0, 1)


_MFLProperty = namedtuple(u'MFLProperty', u'name format to_json from_json min_epii_version')
SORT_KEYS = False

def MFLProperty(name, format = MFLPropertyFormats.Default, to_json = None, from_json = None, min_epii_version = (-1, -1)):
    return _MFLProperty(name, format, to_json, from_json, min_epii_version)


def data_dict_to_json(property_name, data_dict):
    return json.dumps({property_name: data_dict}, ensure_ascii=PY2, sort_keys=SORT_KEYS)


def json_to_data_dict(property_name, json_dict):
    data_dict = ast.literal_eval(json_dict)
    return data_dict.get(property_name, data_dict)


def warp_markers_to_json(obj):
    property_value = getattr(obj, u'warp_markers')
    return data_dict_to_json(u'warp_markers', tuple([ warp_marker_to_dict(t) for t in property_value ]))


def warp_marker_to_dict(warp_marker):
    return {u'sample_time': warp_marker.sample_time,
     u'beat_time': warp_marker.beat_time}


def verify_routings_available_for_object(obj, prop_name):
    if isinstance(obj, Live.Track.Track):
        error_format = u"'%s' not available on %s"
        song = obj.canonical_parent
        if obj == song.master_track:
            raise RuntimeError(error_format % (prop_name, u'master track'))
        elif u'input' in prop_name:
            if obj.is_foldable:
                raise RuntimeError(error_format % (prop_name, u'group tracks'))
            elif obj in song.return_tracks:
                raise RuntimeError(error_format % (prop_name, u'return tracks'))


def routing_object_to_dict(routing_type):
    return {u'display_name': routing_type.display_name,
     u'identifier': hash(routing_type)}


def available_routing_objects_to_json(obj, property_name):
    verify_routings_available_for_object(obj, property_name)
    property_value = getattr(obj, property_name)
    return data_dict_to_json(property_name, tuple([ routing_object_to_dict(t) for t in property_value ]))


def available_routing_input_types_to_json(obj):
    return available_routing_objects_to_json(obj, u'available_input_routing_types')


def available_routing_output_types_to_json(obj):
    return available_routing_objects_to_json(obj, u'available_output_routing_types')


def available_routing_input_channels_to_json(obj):
    return available_routing_objects_to_json(obj, u'available_input_routing_channels')


def available_routing_output_channels_to_json(obj):
    return available_routing_objects_to_json(obj, u'available_output_routing_channels')


def available_routing_types_to_json(device):
    return available_routing_objects_to_json(device, u'available_routing_types')


def available_routing_channels_to_json(device):
    return available_routing_objects_to_json(device, u'available_routing_channels')


def routing_object_to_json(obj, property_name):
    verify_routings_available_for_object(obj, property_name)
    property_value = getattr(obj, property_name)
    return data_dict_to_json(property_name, routing_object_to_dict(property_value))


def routing_input_type_to_json(obj):
    return routing_object_to_json(obj, u'input_routing_type')


def routing_output_type_to_json(obj):
    return routing_object_to_json(obj, u'output_routing_type')


def routing_input_channel_to_json(obj):
    return routing_object_to_json(obj, u'input_routing_channel')


def routing_output_channel_to_json(obj):
    return routing_object_to_json(obj, u'output_routing_channel')


def routing_type_to_json(device):
    return routing_object_to_json(device, u'routing_type')


def routing_channel_to_json(device):
    return routing_object_to_json(device, u'routing_channel')


def json_to_routing_object(obj, property_name, json_dict):
    verify_routings_available_for_object(obj, property_name)
    objects = getattr(obj, u'available_%ss' % property_name, [])
    identifier = json_to_data_dict(property_name, json_dict)[u'identifier']
    for routing_object in objects:
        if hash(routing_object) == identifier:
            return routing_object


def json_to_input_routing_type(obj, json_dict):
    return json_to_routing_object(obj, u'input_routing_type', json_dict)


def json_to_output_routing_type(obj, json_dict):
    return json_to_routing_object(obj, u'output_routing_type', json_dict)


def json_to_input_routing_channel(obj, json_dict):
    return json_to_routing_object(obj, u'input_routing_channel', json_dict)


def json_to_output_routing_channel(obj, json_dict):
    return json_to_routing_object(obj, u'output_routing_channel', json_dict)


def json_to_routing_type(device, json_dict):
    return json_to_routing_object(device, u'routing_type', json_dict)


def json_to_routing_channel(device, json_dict):
    return json_to_routing_object(device, u'routing_channel', json_dict)


_DEVICE_BASE_PROPS = [MFLProperty(u'canonical_parent'),
 MFLProperty(u'parameters'),
 MFLProperty(u'view'),
 MFLProperty(u'can_have_chains'),
 MFLProperty(u'can_have_drum_pads'),
 MFLProperty(u'class_display_name'),
 MFLProperty(u'class_name'),
 MFLProperty(u'is_active'),
 MFLProperty(u'name'),
 MFLProperty(u'type'),
 MFLProperty(u'store_chosen_bank')]
_DEVICE_VIEW_BASE_PROPS = [MFLProperty(u'canonical_parent'), MFLProperty(u'is_collapsed')]
_CHAIN_BASE_PROPS = [MFLProperty(u'canonical_parent'),
 MFLProperty(u'devices'),
 MFLProperty(u'mixer_device'),
 MFLProperty(u'color'),
 MFLProperty(u'color_index'),
 MFLProperty(u'is_auto_colored'),
 MFLProperty(u'has_audio_input'),
 MFLProperty(u'has_audio_output'),
 MFLProperty(u'has_midi_input'),
 MFLProperty(u'has_midi_output'),
 MFLProperty(u'mute'),
 MFLProperty(u'muted_via_solo'),
 MFLProperty(u'name'),
 MFLProperty(u'solo'),
 MFLProperty(u'delete_device')]
EXPOSED_TYPE_PROPERTIES = {Live.Application.Application: (MFLProperty(u'view'),
                                MFLProperty(u'current_dialog_button_count'),
                                MFLProperty(u'current_dialog_message'),
                                MFLProperty(u'open_dialog_count'),
                                MFLProperty(u'get_bugfix_version'),
                                MFLProperty(u'get_document'),
                                MFLProperty(u'get_major_version'),
                                MFLProperty(u'get_minor_version'),
                                MFLProperty(u'press_current_dialog_button'),
                                MFLProperty(u'control_surfaces')),
 Live.Application.Application.View: (MFLProperty(u'canonical_parent'),
                                     MFLProperty(u'browse_mode'),
                                     MFLProperty(u'focused_document_view'),
                                     MFLProperty(u'available_main_views'),
                                     MFLProperty(u'focus_view'),
                                     MFLProperty(u'hide_view'),
                                     MFLProperty(u'is_view_visible'),
                                     MFLProperty(u'scroll_view'),
                                     MFLProperty(u'show_view'),
                                     MFLProperty(u'toggle_browse'),
                                     MFLProperty(u'zoom_view')),
 Live.Chain.Chain: tuple(_CHAIN_BASE_PROPS),
 Live.ChainMixerDevice.ChainMixerDevice: (MFLProperty(u'canonical_parent'),
                                          MFLProperty(u'chain_activator'),
                                          MFLProperty(u'panning'),
                                          MFLProperty(u'sends'),
                                          MFLProperty(u'volume')),
 Live.Clip.Clip: (MFLProperty(u'canonical_parent'),
                  MFLProperty(u'view'),
                  MFLProperty(u'available_warp_modes'),
                  MFLProperty(u'color'),
                  MFLProperty(u'color_index'),
                  MFLProperty(u'crop'),
                  MFLProperty(u'end_marker'),
                  MFLProperty(u'end_time'),
                  MFLProperty(u'gain'),
                  MFLProperty(u'gain_display_string'),
                  MFLProperty(u'has_groove'),
                  MFLProperty(u'groove'),
                  MFLProperty(u'file_path'),
                  MFLProperty(u'has_envelopes'),
                  MFLProperty(u'is_arrangement_clip'),
                  MFLProperty(u'is_audio_clip'),
                  MFLProperty(u'is_midi_clip'),
                  MFLProperty(u'is_overdubbing'),
                  MFLProperty(u'is_playing'),
                  MFLProperty(u'is_recording'),
                  MFLProperty(u'is_triggered'),
                  MFLProperty(u'launch_mode'),
                  MFLProperty(u'launch_quantization'),
                  MFLProperty(u'legato'),
                  MFLProperty(u'length'),
                  MFLProperty(u'loop_end'),
                  MFLProperty(u'loop_start'),
                  MFLProperty(u'looping'),
                  MFLProperty(u'muted'),
                  MFLProperty(u'name'),
                  MFLProperty(u'pitch_coarse'),
                  MFLProperty(u'pitch_fine'),
                  MFLProperty(u'playing_position'),
                  MFLProperty(u'position'),
                  MFLProperty(u'ram_mode'),
                  MFLProperty(u'signature_denominator'),
                  MFLProperty(u'signature_numerator'),
                  MFLProperty(u'start_marker'),
                  MFLProperty(u'start_time'),
                  MFLProperty(u'warp_mode'),
                  MFLProperty(u'warp_markers', format=MFLPropertyFormats.JSON, to_json=warp_markers_to_json, min_epii_version=(4, 3)),
                  MFLProperty(u'warping'),
                  MFLProperty(u'will_record_on_start'),
                  MFLProperty(u'clear_all_envelopes'),
                  MFLProperty(u'clear_envelope'),
                  MFLProperty(u'deselect_all_notes'),
                  MFLProperty(u'duplicate_loop'),
                  MFLProperty(u'duplicate_region'),
                  MFLProperty(u'fire'),
                  MFLProperty(u'get_notes'),
                  MFLProperty(u'get_selected_notes'),
                  MFLProperty(u'get_notes_by_id', min_epii_version=(4, 3)),
                  MFLProperty(u'get_notes_extended', min_epii_version=(4, 3)),
                  MFLProperty(u'get_selected_notes_extended', min_epii_version=(4, 3)),
                  MFLProperty(u'add_new_notes', min_epii_version=(4, 3)),
                  MFLProperty(u'apply_note_modifications', min_epii_version=(4, 3)),
                  MFLProperty(u'remove_notes_extended', min_epii_version=(4, 3)),
                  MFLProperty(u'remove_notes_by_id', min_epii_version=(4, 3)),
                  MFLProperty(u'move_playing_pos'),
                  MFLProperty(u'quantize'),
                  MFLProperty(u'quantize_pitch'),
                  MFLProperty(u'remove_notes'),
                  MFLProperty(u'replace_selected_notes'),
                  MFLProperty(u'scrub'),
                  MFLProperty(u'select_all_notes'),
                  MFLProperty(u'set_fire_button_state'),
                  MFLProperty(u'set_notes'),
                  MFLProperty(u'stop'),
                  MFLProperty(u'stop_scrub'),
                  MFLProperty(u'velocity_amount')),
 Live.Clip.Clip.View: (MFLProperty(u'canonical_parent'),
                       MFLProperty(u'grid_is_triplet'),
                       MFLProperty(u'grid_quantization'),
                       MFLProperty(u'hide_envelope'),
                       MFLProperty(u'select_envelope_parameter'),
                       MFLProperty(u'show_envelope'),
                       MFLProperty(u'show_loop')),
 Live.Groove.Groove: (MFLProperty(u'name'),
                      MFLProperty(u'base'),
                      MFLProperty(u'quantization_amount'),
                      MFLProperty(u'timing_amount'),
                      MFLProperty(u'random_amount'),
                      MFLProperty(u'velocity_amount')),
 Live.ClipSlot.ClipSlot: (MFLProperty(u'canonical_parent'),
                          MFLProperty(u'clip'),
                          MFLProperty(u'color'),
                          MFLProperty(u'color_index'),
                          MFLProperty(u'controls_other_clips'),
                          MFLProperty(u'has_clip'),
                          MFLProperty(u'has_stop_button'),
                          MFLProperty(u'is_group_slot'),
                          MFLProperty(u'is_playing'),
                          MFLProperty(u'is_recording'),
                          MFLProperty(u'is_triggered'),
                          MFLProperty(u'playing_status'),
                          MFLProperty(u'will_record_on_start'),
                          MFLProperty(u'create_clip'),
                          MFLProperty(u'delete_clip'),
                          MFLProperty(u'duplicate_clip_to'),
                          MFLProperty(u'fire'),
                          MFLProperty(u'set_fire_button_state'),
                          MFLProperty(u'stop')),
 Live.CompressorDevice.CompressorDevice: tuple(_DEVICE_BASE_PROPS + [MFLProperty(u'available_input_routing_channels', format=MFLPropertyFormats.JSON, to_json=available_routing_input_channels_to_json, min_epii_version=(4, 3)),
                                          MFLProperty(u'available_input_routing_types', format=MFLPropertyFormats.JSON, to_json=available_routing_input_types_to_json, min_epii_version=(4, 3)),
                                          MFLProperty(u'input_routing_channel', format=MFLPropertyFormats.JSON, to_json=routing_input_channel_to_json, min_epii_version=(4, 3)),
                                          MFLProperty(u'input_routing_type', format=MFLPropertyFormats.JSON, to_json=routing_input_channel_to_json, min_epii_version=(4, 3))]),
 Live.Device.Device: tuple(_DEVICE_BASE_PROPS),
 Live.Device.Device.View: tuple(_DEVICE_VIEW_BASE_PROPS),
 Live.DeviceParameter.DeviceParameter: (MFLProperty(u'canonical_parent'),
                                        MFLProperty(u'automation_state'),
                                        MFLProperty(u'default_value'),
                                        MFLProperty(u'is_enabled'),
                                        MFLProperty(u'is_quantized'),
                                        MFLProperty(u'max'),
                                        MFLProperty(u'min'),
                                        MFLProperty(u'name'),
                                        MFLProperty(u'original_name'),
                                        MFLProperty(u'state'),
                                        MFLProperty(u'value'),
                                        MFLProperty(u'value_items'),
                                        MFLProperty(u're_enable_automation'),
                                        MFLProperty(u'str_for_value'),
                                        MFLProperty(u'__str__')),
 Live.DeviceIO.DeviceIO: (MFLProperty(u'available_routing_channels', format=MFLPropertyFormats.JSON, to_json=available_routing_channels_to_json, min_epii_version=(4, 4)),
                          MFLProperty(u'available_routing_types', format=MFLPropertyFormats.JSON, to_json=available_routing_types_to_json, min_epii_version=(4, 4)),
                          MFLProperty(u'routing_channel', format=MFLPropertyFormats.JSON, to_json=routing_channel_to_json, from_json=json_to_routing_channel, min_epii_version=(4, 4)),
                          MFLProperty(u'routing_type', format=MFLPropertyFormats.JSON, to_json=routing_type_to_json, from_json=json_to_routing_type, min_epii_version=(4, 4)),
                          MFLProperty(u'default_external_routing_channel_is_none')),
 Live.DrumChain.DrumChain: tuple(_CHAIN_BASE_PROPS + [MFLProperty(u'out_note'), MFLProperty(u'choke_group')]),
 Live.DrumPad.DrumPad: (MFLProperty(u'canonical_parent'),
                        MFLProperty(u'chains'),
                        MFLProperty(u'mute'),
                        MFLProperty(u'name'),
                        MFLProperty(u'note'),
                        MFLProperty(u'solo'),
                        MFLProperty(u'delete_all_chains')),
 Live.Eq8Device.Eq8Device: tuple(_DEVICE_BASE_PROPS + [MFLProperty(u'global_mode'), MFLProperty(u'edit_mode'), MFLProperty(u'oversample')]),
 Live.Eq8Device.Eq8Device.View: tuple(_DEVICE_VIEW_BASE_PROPS + [MFLProperty(u'selected_band')]),
 Live.MaxDevice.MaxDevice: tuple(_DEVICE_BASE_PROPS + [MFLProperty(u'get_bank_count'),
                            MFLProperty(u'get_bank_name'),
                            MFLProperty(u'get_bank_parameters'),
                            MFLProperty(u'audio_outputs'),
                            MFLProperty(u'audio_inputs'),
                            MFLProperty(u'midi_outputs'),
                            MFLProperty(u'midi_inputs')]),
 Live.MixerDevice.MixerDevice: (MFLProperty(u'canonical_parent'),
                                MFLProperty(u'sends'),
                                MFLProperty(u'cue_volume'),
                                MFLProperty(u'crossfader'),
                                MFLProperty(u'left_split_stereo'),
                                MFLProperty(u'panning'),
                                MFLProperty(u'panning_mode'),
                                MFLProperty(u'right_split_stereo'),
                                MFLProperty(u'song_tempo'),
                                MFLProperty(u'track_activator'),
                                MFLProperty(u'volume'),
                                MFLProperty(u'crossfade_assign')),
 Live.PluginDevice.PluginDevice: tuple(_DEVICE_BASE_PROPS + [MFLProperty(u'presets'), MFLProperty(u'selected_preset_index')]),
 Live.RackDevice.RackDevice: tuple(_DEVICE_BASE_PROPS + [MFLProperty(u'chains'),
                              MFLProperty(u'can_show_chains'),
                              MFLProperty(u'drum_pads'),
                              MFLProperty(u'is_showing_chains'),
                              MFLProperty(u'return_chains'),
                              MFLProperty(u'visible_drum_pads'),
                              MFLProperty(u'has_macro_mappings'),
                              MFLProperty(u'has_drum_pads'),
                              MFLProperty(u'copy_pad'),
                              MFLProperty(u'add_macro'),
                              MFLProperty(u'remove_macro'),
                              MFLProperty(u'randomize_macros'),
                              MFLProperty(u'variation_count'),
                              MFLProperty(u'selected_variation_index'),
                              MFLProperty(u'store_variation'),
                              MFLProperty(u'recall_selected_variation'),
                              MFLProperty(u'recall_last_used_variation'),
                              MFLProperty(u'delete_selected_variation')]),
 Live.RackDevice.RackDevice.View: tuple(_DEVICE_VIEW_BASE_PROPS + [MFLProperty(u'selected_chain'),
                                   MFLProperty(u'selected_drum_pad'),
                                   MFLProperty(u'drum_pads_scroll_position'),
                                   MFLProperty(u'is_showing_chain_devices')]),
 Live.Sample.Sample: (MFLProperty(u'canonical_parent'),
                      MFLProperty(u'beats_granulation_resolution'),
                      MFLProperty(u'beats_transient_envelope'),
                      MFLProperty(u'beats_transient_loop_mode'),
                      MFLProperty(u'complex_pro_envelope'),
                      MFLProperty(u'complex_pro_formants'),
                      MFLProperty(u'end_marker'),
                      MFLProperty(u'file_path'),
                      MFLProperty(u'gain'),
                      MFLProperty(u'length'),
                      MFLProperty(u'sample_rate'),
                      MFLProperty(u'slicing_sensitivity'),
                      MFLProperty(u'start_marker'),
                      MFLProperty(u'texture_flux'),
                      MFLProperty(u'texture_grain_size'),
                      MFLProperty(u'tones_grain_size'),
                      MFLProperty(u'warp_mode'),
                      MFLProperty(u'warping'),
                      MFLProperty(u'warp_markers', format=MFLPropertyFormats.JSON, to_json=warp_markers_to_json, min_epii_version=(4, 3)),
                      MFLProperty(u'slicing_style'),
                      MFLProperty(u'slicing_beat_division'),
                      MFLProperty(u'slicing_region_count'),
                      MFLProperty(u'gain_display_string'),
                      MFLProperty(u'insert_slice'),
                      MFLProperty(u'move_slice'),
                      MFLProperty(u'remove_slice'),
                      MFLProperty(u'clear_slices'),
                      MFLProperty(u'reset_slices'),
                      MFLProperty(u'slices')),
 Live.Scene.Scene: (MFLProperty(u'canonical_parent'),
                    MFLProperty(u'clip_slots'),
                    MFLProperty(u'color'),
                    MFLProperty(u'color_index'),
                    MFLProperty(u'is_empty'),
                    MFLProperty(u'is_triggered'),
                    MFLProperty(u'name'),
                    MFLProperty(u'tempo'),
                    MFLProperty(u'fire'),
                    MFLProperty(u'fire_as_selected'),
                    MFLProperty(u'set_fire_button_state')),
 Live.SimplerDevice.SimplerDevice: tuple(_DEVICE_BASE_PROPS + [MFLProperty(u'sample'),
                                    MFLProperty(u'can_warp_as'),
                                    MFLProperty(u'can_warp_double'),
                                    MFLProperty(u'can_warp_half'),
                                    MFLProperty(u'multi_sample_mode'),
                                    MFLProperty(u'pad_slicing'),
                                    MFLProperty(u'playback_mode'),
                                    MFLProperty(u'playing_position'),
                                    MFLProperty(u'playing_position_enabled'),
                                    MFLProperty(u'retrigger'),
                                    MFLProperty(u'slicing_playback_mode'),
                                    MFLProperty(u'voices'),
                                    MFLProperty(u'crop'),
                                    MFLProperty(u'guess_playback_length'),
                                    MFLProperty(u'reverse'),
                                    MFLProperty(u'warp_as'),
                                    MFLProperty(u'warp_double'),
                                    MFLProperty(u'warp_half')]),
 Live.SimplerDevice.SimplerDevice.View: tuple(_DEVICE_VIEW_BASE_PROPS + [MFLProperty(u'selected_slice')]),
 Live.Song.Song: (MFLProperty(u'cue_points'),
                  MFLProperty(u'return_tracks'),
                  MFLProperty(u'scenes'),
                  MFLProperty(u'tracks'),
                  MFLProperty(u'visible_tracks'),
                  MFLProperty(u'master_track'),
                  MFLProperty(u'view'),
                  MFLProperty(u'appointed_device'),
                  MFLProperty(u'arrangement_overdub'),
                  MFLProperty(u'back_to_arranger'),
                  MFLProperty(u'can_jump_to_next_cue'),
                  MFLProperty(u'can_jump_to_prev_cue'),
                  MFLProperty(u'can_redo'),
                  MFLProperty(u'can_undo'),
                  MFLProperty(u'clip_trigger_quantization'),
                  MFLProperty(u'count_in_duration'),
                  MFLProperty(u'current_song_time'),
                  MFLProperty(u'exclusive_arm'),
                  MFLProperty(u'exclusive_solo'),
                  MFLProperty(u'groove_amount'),
                  MFLProperty(u'groove_pool'),
                  MFLProperty(u'is_counting_in'),
                  MFLProperty(u'is_playing'),
                  MFLProperty(u'last_event_time'),
                  MFLProperty(u'loop'),
                  MFLProperty(u'loop_length'),
                  MFLProperty(u'loop_start'),
                  MFLProperty(u'metronome'),
                  MFLProperty(u'midi_recording_quantization'),
                  MFLProperty(u'nudge_down'),
                  MFLProperty(u'nudge_up'),
                  MFLProperty(u'overdub'),
                  MFLProperty(u'punch_in'),
                  MFLProperty(u'punch_out'),
                  MFLProperty(u're_enable_automation_enabled'),
                  MFLProperty(u'record_mode'),
                  MFLProperty(u'root_note'),
                  MFLProperty(u'scale_name'),
                  MFLProperty(u'scale_intervals'),
                  MFLProperty(u'select_on_launch'),
                  MFLProperty(u'session_automation_record'),
                  MFLProperty(u'session_record'),
                  MFLProperty(u'session_record_status'),
                  MFLProperty(u'signature_denominator'),
                  MFLProperty(u'signature_numerator'),
                  MFLProperty(u'song_length'),
                  MFLProperty(u'swing_amount'),
                  MFLProperty(u'tempo'),
                  MFLProperty(u'capture_and_insert_scene'),
                  MFLProperty(u'capture_midi'),
                  MFLProperty(u'can_capture_midi'),
                  MFLProperty(u'continue_playing'),
                  MFLProperty(u'create_audio_track'),
                  MFLProperty(u'create_midi_track'),
                  MFLProperty(u'create_return_track'),
                  MFLProperty(u'create_scene'),
                  MFLProperty(u'delete_scene'),
                  MFLProperty(u'delete_track'),
                  MFLProperty(u'delete_return_track'),
                  MFLProperty(u'duplicate_scene'),
                  MFLProperty(u'duplicate_track'),
                  MFLProperty(u'find_device_position'),
                  MFLProperty(u'force_link_beat_time'),
                  MFLProperty(u'get_beats_loop_length'),
                  MFLProperty(u'get_beats_loop_start'),
                  MFLProperty(u'get_current_beats_song_time'),
                  MFLProperty(u'get_current_smpte_song_time'),
                  MFLProperty(u'is_cue_point_selected'),
                  MFLProperty(u'jump_by'),
                  MFLProperty(u'jump_to_next_cue'),
                  MFLProperty(u'jump_to_prev_cue'),
                  MFLProperty(u'move_device'),
                  MFLProperty(u'play_selection'),
                  MFLProperty(u're_enable_automation'),
                  MFLProperty(u'redo'),
                  MFLProperty(u'scrub_by'),
                  MFLProperty(u'set_or_delete_cue'),
                  MFLProperty(u'start_playing'),
                  MFLProperty(u'stop_all_clips'),
                  MFLProperty(u'stop_playing'),
                  MFLProperty(u'tap_tempo'),
                  MFLProperty(u'trigger_session_record'),
                  MFLProperty(u'undo')),
 Live.Song.Song.View: (MFLProperty(u'canonical_parent'),
                       MFLProperty(u'detail_clip'),
                       MFLProperty(u'highlighted_clip_slot'),
                       MFLProperty(u'selected_chain'),
                       MFLProperty(u'selected_parameter'),
                       MFLProperty(u'selected_scene'),
                       MFLProperty(u'selected_track'),
                       MFLProperty(u'draw_mode'),
                       MFLProperty(u'follow_song'),
                       MFLProperty(u'select_device')),
 Live.GroovePool.GroovePool: (MFLProperty(u'grooves'),),
 Live.Song.CuePoint: (MFLProperty(u'canonical_parent'),
                      MFLProperty(u'name'),
                      MFLProperty(u'time'),
                      MFLProperty(u'jump')),
 Live.Track.Track: (MFLProperty(u'clip_slots'),
                    MFLProperty(u'arrangement_clips'),
                    MFLProperty(u'devices'),
                    MFLProperty(u'canonical_parent'),
                    MFLProperty(u'mixer_device'),
                    MFLProperty(u'view'),
                    MFLProperty(u'arm'),
                    MFLProperty(u'available_input_routing_channels', format=MFLPropertyFormats.JSON, to_json=available_routing_input_channels_to_json, min_epii_version=(4, 3)),
                    MFLProperty(u'available_input_routing_types', format=MFLPropertyFormats.JSON, to_json=available_routing_input_types_to_json, min_epii_version=(4, 3)),
                    MFLProperty(u'available_output_routing_channels', format=MFLPropertyFormats.JSON, to_json=available_routing_output_channels_to_json, min_epii_version=(4, 3)),
                    MFLProperty(u'available_output_routing_types', format=MFLPropertyFormats.JSON, to_json=available_routing_output_types_to_json, min_epii_version=(4, 3)),
                    MFLProperty(u'can_be_armed'),
                    MFLProperty(u'can_be_frozen'),
                    MFLProperty(u'can_show_chains'),
                    MFLProperty(u'color'),
                    MFLProperty(u'color_index'),
                    MFLProperty(u'current_input_routing'),
                    MFLProperty(u'current_input_sub_routing'),
                    MFLProperty(u'current_monitoring_state'),
                    MFLProperty(u'current_output_routing'),
                    MFLProperty(u'current_output_sub_routing'),
                    MFLProperty(u'fired_slot_index'),
                    MFLProperty(u'fold_state'),
                    MFLProperty(u'group_track'),
                    MFLProperty(u'has_audio_input'),
                    MFLProperty(u'has_audio_output'),
                    MFLProperty(u'has_midi_input'),
                    MFLProperty(u'has_midi_output'),
                    MFLProperty(u'implicit_arm'),
                    MFLProperty(u'input_meter_left'),
                    MFLProperty(u'input_meter_level'),
                    MFLProperty(u'input_meter_right'),
                    MFLProperty(u'input_routing_channel', format=MFLPropertyFormats.JSON, to_json=routing_input_channel_to_json, from_json=json_to_input_routing_channel, min_epii_version=(4, 3)),
                    MFLProperty(u'input_routing_type', format=MFLPropertyFormats.JSON, to_json=routing_input_type_to_json, from_json=json_to_input_routing_type, min_epii_version=(4, 3)),
                    MFLProperty(u'input_routings'),
                    MFLProperty(u'input_sub_routings'),
                    MFLProperty(u'is_foldable'),
                    MFLProperty(u'is_frozen'),
                    MFLProperty(u'is_grouped'),
                    MFLProperty(u'is_part_of_selection'),
                    MFLProperty(u'is_showing_chains'),
                    MFLProperty(u'is_visible'),
                    MFLProperty(u'mute'),
                    MFLProperty(u'muted_via_solo'),
                    MFLProperty(u'name'),
                    MFLProperty(u'output_meter_left'),
                    MFLProperty(u'output_meter_level'),
                    MFLProperty(u'output_meter_right'),
                    MFLProperty(u'output_routing_channel', format=MFLPropertyFormats.JSON, to_json=routing_output_channel_to_json, from_json=json_to_output_routing_channel, min_epii_version=(4, 3)),
                    MFLProperty(u'output_routing_type', format=MFLPropertyFormats.JSON, to_json=routing_output_type_to_json, from_json=json_to_output_routing_type, min_epii_version=(4, 3)),
                    MFLProperty(u'output_routings'),
                    MFLProperty(u'output_sub_routings'),
                    MFLProperty(u'playing_slot_index'),
                    MFLProperty(u'solo'),
                    MFLProperty(u'delete_clip'),
                    MFLProperty(u'delete_device'),
                    MFLProperty(u'duplicate_clip_slot'),
                    MFLProperty(u'duplicate_clip_to_arrangement'),
                    MFLProperty(u'jump_in_running_session_clip'),
                    MFLProperty(u'stop_all_clips')),
 Live.Track.Track.View: (MFLProperty(u'canonical_parent'),
                         MFLProperty(u'selected_device'),
                         MFLProperty(u'device_insert_mode'),
                         MFLProperty(u'is_collapsed'),
                         MFLProperty(u'select_instrument')),
 Live.WavetableDevice.WavetableDevice: tuple(_DEVICE_BASE_PROPS + [MFLProperty(u'add_parameter_to_modulation_matrix'),
                                        MFLProperty(u'filter_routing'),
                                        MFLProperty(u'get_modulation_target_parameter_name'),
                                        MFLProperty(u'get_modulation_value'),
                                        MFLProperty(u'is_parameter_modulatable'),
                                        MFLProperty(u'mono_poly'),
                                        MFLProperty(u'oscillator_1_effect_mode'),
                                        MFLProperty(u'oscillator_2_effect_mode'),
                                        MFLProperty(u'oscillator_1_wavetable_category'),
                                        MFLProperty(u'oscillator_2_wavetable_category'),
                                        MFLProperty(u'oscillator_1_wavetable_index'),
                                        MFLProperty(u'oscillator_2_wavetable_index'),
                                        MFLProperty(u'oscillator_1_wavetables'),
                                        MFLProperty(u'oscillator_2_wavetables'),
                                        MFLProperty(u'oscillator_wavetable_categories'),
                                        MFLProperty(u'poly_voices'),
                                        MFLProperty(u'set_modulation_value'),
                                        MFLProperty(u'unison_mode'),
                                        MFLProperty(u'unison_voice_count'),
                                        MFLProperty(u'visible_modulation_target_names')])}
PROPERTY_NAMES_EXCLUDED_FROM_DOCUMENTATION = (u'canonical_parent',)
EXTRA_CS_FUNCTIONS = (u'get_control_names', u'get_control', u'grab_control', u'release_control', u'send_midi', u'send_receive_sysex', u'grab_midi', u'release_midi')
ENUM_TYPES = (Live.Song.Quantization,
 Live.Song.RecordingQuantization,
 Live.Song.CaptureMode,
 Live.Clip.GridQuantization,
 Live.DeviceParameter.AutomationState,
 Live.Groove.Base,
 Live.Sample.SlicingStyle,
 Live.Sample.SlicingBeatDivision)
TUPLE_TYPES = {u'tracks': Live.Track.Track,
 u'grooves': Live.Groove.Groove,
 u'visible_tracks': Live.Track.Track,
 u'return_tracks': Live.Track.Track,
 u'clip_slots': Live.ClipSlot.ClipSlot,
 u'arrangement_clips': Live.Clip.Clip,
 u'scenes': Live.Scene.Scene,
 u'parameters': Live.DeviceParameter.DeviceParameter,
 u'sends': Live.DeviceParameter.DeviceParameter,
 u'devices': Live.Device.Device,
 u'cue_points': Live.Song.CuePoint,
 u'chains': Live.Chain.Chain,
 u'return_chains': Live.Chain.Chain,
 u'drum_pads': Live.DrumPad.DrumPad,
 u'visible_drum_pads': Live.DrumPad.DrumPad,
 u'control_surfaces': ControlSurface,
 u'components': ControlSurfaceComponent,
 u'controls': ControlElement,
 u'audio_outputs': Live.DeviceIO.DeviceIO,
 u'audio_inputs': Live.DeviceIO.DeviceIO,
 u'midi_outputs': Live.DeviceIO.DeviceIO,
 u'midi_inputs': Live.DeviceIO.DeviceIO}
PROPERTY_TYPES = {u'master_track': Live.Track.Track,
 u'selected_track': Live.Track.Track,
 u'selected_scene': Live.Scene.Scene,
 u'volume': Live.DeviceParameter.DeviceParameter,
 u'panning': Live.DeviceParameter.DeviceParameter,
 u'crossfader': Live.DeviceParameter.DeviceParameter,
 u'song_tempo': Live.DeviceParameter.DeviceParameter,
 u'cue_volume': Live.DeviceParameter.DeviceParameter,
 u'track_activator': Live.DeviceParameter.DeviceParameter,
 u'chain_activator': Live.DeviceParameter.DeviceParameter,
 u'groove': Live.Groove.Groove,
 u'clip': Live.Clip.Clip,
 u'detail_clip': Live.Clip.Clip,
 u'highlighted_clip_slot': Live.ClipSlot.ClipSlot,
 u'selected_device': Live.Device.Device,
 u'selected_parameter': Live.DeviceParameter.DeviceParameter,
 u'selected_chain': Live.Chain.Chain,
 u'selected_drum_pad': Live.DrumPad.DrumPad,
 u'sample': Live.Sample.Sample,
 u'mixer_device': (Live.MixerDevice.MixerDevice, Live.ChainMixerDevice.ChainMixerDevice),
 u'view': (Live.Application.Application.View,
           Live.Song.Song.View,
           Live.Track.Track.View,
           Live.Device.Device.View,
           Live.RackDevice.RackDevice.View,
           Live.Clip.Clip.View),
 u'left_split_stereo': Live.DeviceParameter.DeviceParameter,
 u'right_split_stereo': Live.DeviceParameter.DeviceParameter,
 u'group_track': Live.Track.Track}
LIVE_APP = u'live_app'
LIVE_SET = u'live_set'
CONTROL_SURFACES = u'control_surfaces'
THIS_DEVICE = u'this_device'
ROOT_KEYS = (THIS_DEVICE,
 CONTROL_SURFACES,
 LIVE_APP,
 LIVE_SET)

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


def get_exposed_properties_for_type(lom_type, epii_version = None):
    if epii_version is None:
        epii_version = (float(u'inf'), float(u'inf'))
    return [ prop for prop in EXPOSED_TYPE_PROPERTIES.get(lom_type, []) if epii_version >= prop.min_epii_version ]


def get_exposed_property_names_for_type(lom_type, epii_version = None):
    return [ prop.name for prop in get_exposed_properties_for_type(lom_type, epii_version) ]


def is_property_exposed_for_type(property_name, lom_type, epii_version):
    return property_name in get_exposed_property_names_for_type(lom_type, epii_version)


def get_exposed_property_info(lom_type, property_name, epii_version):
    properties = get_exposed_properties_for_type(lom_type, epii_version)
    prop = [ p for p in properties if p.name == property_name ]
    if not prop:
        return None
    return prop[0]


def get_exposed_properties_to_document_for_type(lom_type):
    properties = set(get_exposed_property_names_for_type(lom_type))
    if issubclass(lom_type, Live.Device.Device):
        properties -= {prop.name for prop in _DEVICE_BASE_PROPS}
    if issubclass(lom_type, Live.Chain.Chain):
        properties -= {prop.name for prop in _CHAIN_BASE_PROPS}
    if issubclass(lom_type, Live.Device.Device.View):
        properties -= {prop.name for prop in _DEVICE_VIEW_BASE_PROPS}
    properties -= set(PROPERTY_NAMES_EXCLUDED_FROM_DOCUMENTATION)
    return list(properties)


def is_class(class_object):
    return isinstance(class_object, type) or old_hasattr(class_object, u'__bases__')


def get_control_surfaces():
    result = []
    cs_list_key = u'control_surfaces'
    if isinstance(__builtins__, dict):
        if cs_list_key in list(__builtins__.keys()):
            result = __builtins__[cs_list_key]
    elif old_hasattr(__builtins__, cs_list_key):
        result = getattr(__builtins__, cs_list_key)
    return tuple(result)


def get_root_prop(external_device, prop_key):
    root_properties = {LIVE_APP: Live.Application.get_application,
     LIVE_SET: lambda : Live.Application.get_application().get_document(),
     CONTROL_SURFACES: get_control_surfaces}
    assert prop_key in ROOT_KEYS
    if prop_key == THIS_DEVICE:
        return external_device
    return root_properties[prop_key]()


def cs_base_classes():
    from _Framework.ControlSurface import ControlSurface
    from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
    from _Framework.ControlElement import ControlElement
    from ableton.v2.control_surface import ControlElement as ControlElement2
    from ableton.v2.control_surface import ControlSurface as ControlSurface2
    from ableton.v2.control_surface import Component as ControlSurfaceComponent2
    return (ControlSurface,
     ControlSurfaceComponent,
     ControlElement,
     ControlSurface2,
     ControlSurfaceComponent2,
     ControlElement2)


def is_control_surface(lom_object):
    from _Framework.ControlSurface import ControlSurface
    from ableton.v2.control_surface import ControlSurface as ControlSurface2
    return isinstance(lom_object, (ControlSurface, ControlSurface2))


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
    elif not is_property_exposed_for_type(property_name, type(lom_object), epii_version):
        raise_error = True
    if raise_error:
        raise LomAttributeError(u"'%s' object has no attribute '%s'" % (lom_object.__class__.__name__, property_name))
