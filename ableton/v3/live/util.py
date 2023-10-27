# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\live\util.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 12916 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import singledispatch
from typing import Any, Union
import Live
import Live.Clip as Clip
import Live.ClipSlot as ClipSlot
import Live.DeviceParameter as DeviceParameter
import Live.MixerDevice as MixerDevice
import Live.Scene as Scene
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import find_nearest_color
from ableton.v2.control_surface.internal_parameter import InternalParameterBase
from ..base import clamp, find_if, hex_to_rgb
TRANSLATED_MIXER_PARAMETER_NAMES = {'Track Volume':'Volume', 
 'Track Panning':'Pan'}
UNDECLARED_QUANTIZED_PARAMETERS = {
  'AutoFilter': ('LFO Sync Rate',),
  'AutoPan': ('Sync Rate',),
  'BeatRepeat': ('Gate', 'Grid', 'Interval', 'Offset', 'Variation'),
  'Corpus': ('LFO Sync Rate',),
  'Flanger': ('Sync Rate',),
  'FrequencyShifter': ('Sync Rate',),
  'GlueCompressor': ('Ratio', 'Attack', 'Release'),
  'MidiArpeggiator': ('Offset', 'Synced Rate', 'Repeats', 'Ret. Interval', 'Transp. Steps'),
  'MidiNoteLength': ('Synced Length',),
  'MidiScale': ('Base',),
  'MultiSampler': ('L 1 Sync Rate', 'L 2 Sync Rate', 'L 3 Sync Rate'),
  'Operator': ('LFO Sync',),
  'OriginalSimpler': ('L Sync Rate',),
  'Phaser': ('LFO Sync Rate',)}
_current_song = None

class LiveObjectTypeError(Exception):
    pass


def raise_type_error_for_liveobj(obj, return_value: Any=False) -> Any:
    return return_value


def application():
    return Live.Application.get_application()


def song():
    global _current_song
    if liveobj_valid(_current_song):
        return _current_song
    _current_song = application().get_document()
    return _current_song


def set_song(song_obj, from_test=False):
    global _current_song
    _current_song = song_obj


def get_bar_length(clip=None):
    obj = clip if liveobj_valid(clip) else song()
    return 4.0 * obj.signature_numerator / obj.signature_denominator


def is_arrangement_view_active():
    return application().view.focused_document_view == 'Arranger'


def is_song_recording():
    return song().session_record or song().record_mode


def is_track_recording(track):
    playing_slot = playing_clip_slot(track)
    return liveobj_valid(playing_slot) and playing_slot.is_recording


def is_clip_new_recording(clip):
    return clip.is_recording and not clip.is_overdubbing


def playing_clip_slot(track):
    if track.clip_slots:
        index = track.playing_slot_index
        if index >= 0:
            return track.clip_slots[index]


def prepare_new_clip_slot(track, stop=False):
    slot = None
    if track.clip_slots:
        try:
            new_scene_index = _next_empty_clip_slot_index(track)
            song().view.selected_scene = song().scenes[new_scene_index]
            slot = track.clip_slots[scene_index()]
            if stop:
                track.stop_all_clips(False)
        except Live.Base.LimitationError:
            pass

        return slot


def _next_empty_clip_slot_index(track):
    current_index = scene_index()
    scene_count = len(song().scenes)
    while track.clip_slots[current_index].has_clip:
        current_index += 1
        if current_index == scene_count:
            song().create_scene(scene_count)

    return current_index


def is_track_armed(track):
    return liveobj_valid(track) and track.can_be_armed and (track.arm or track.implicit_arm)


def any_track_armed():
    return any((t.can_be_armed and t.arm for t in song().tracks))


def find_parent_track(liveobj):
    parent = liveobj.canonical_parent
    if isinstance(parent, Live.Track.Track):
        return parent
    return find_parent_track(parent)


def all_visible_tracks():
    return list(tuple(song().visible_tracks) + tuple(song().return_tracks) + (song().master_track,))


def track_index(track=None, track_list=None):
    track = track or song().view.selected_track
    track_list = track_list or list(song().tracks)
    if track in track_list:
        return track_list.index(track)


def scene_index(scene=None):
    scene = scene or song().view.selected_scene
    return list(song().scenes).index(scene)


@singledispatch
def display_name(obj: Union[(Scene, Clip, ClipSlot, DeviceParameter)], strip_space=True):
    return raise_type_error_for_liveobj(obj, return_value='')


@display_name.register
def _(scene: Scene, strip_space=True):
    return liveobj_name(scene, strip_space) or 'Scene {}'.format(scene_index(scene) + 1)


@display_name.register
def _(clip: Clip, strip_space=True):
    return liveobj_name(clip, strip_space) or 'Clip'


@display_name.register
def _(clip_slot: ClipSlot, strip_space=True):
    if liveobj_valid(clip_slot.clip):
        return display_name(clip_slot.clip, strip_space)
    return 'Slot {}'.format(list(clip_slot.canonical_parent.clip_slots).index(clip_slot) + 1)


@display_name.register
def _(parameter: DeviceParameter, **_):
    if liveobj_valid(parameter):
        try:
            return parameter.display_name
        except AttributeError:
            return TRANSLATED_MIXER_PARAMETER_NAMES.get(parameter.name, parameter.name)

        return ''


@display_name.register
def _(parameter: InternalParameterBase, **_):
    return parameter.name


def liveobj_name(obj, strip_space=True):
    if liveobj_valid(obj):
        if strip_space:
            return obj.name.strip()
        return obj.name
    return ''


def is_device_rack(device):
    return liveobj_valid(device) and device.can_have_chains


def get_parameter_by_name(name, device):
    if liveobj_valid(device):
        return find_if(lambda p: p.original_name == name and liveobj_valid(p) and p.is_enabled
, device.parameters)


def normalized_parameter_value(parameter, value=None):
    result = 0.0
    if liveobj_valid(parameter):
        value = value if value is not None else parameter.value
        param_range = parameter.max - parameter.min
        result = (value - parameter.min) / param_range
    return clamp(result, 0.0, 1.0)


def parameter_value_to_midi_value(parameter, max_value=128):
    return int(normalized_parameter_value(parameter) * (max_value - 1))


def parameter_owner(parameter):
    if isinstance(parameter.canonical_parent, MixerDevice):
        return parameter.canonical_parent.canonical_parent
    return parameter.canonical_parent


def is_parameter_quantized(parameter, device):
    is_quantized = False
    if liveobj_valid(parameter):
        device_class = getattr(device, 'class_name', None)
        is_quantized = (parameter.is_quantized) or ((device_class in UNDECLARED_QUANTIZED_PARAMETERS) and (parameter.name in UNDECLARED_QUANTIZED_PARAMETERS[device_class]))
    return is_quantized


def liveobj_color_to_midi_rgb_values(obj, default_values=(0, 0, 0)):
    if liveobj_valid(obj):
        return tuple((i // 2 for i in hex_to_rgb(obj.color)))
    return default_values


def liveobj_color_to_value_from_palette(obj, palette=None, fallback_table=None, default_value=0):
    if liveobj_valid(obj):
        try:
            return palette[obj.color]
        except (KeyError, IndexError):
            return find_nearest_color(fallback_table, obj.color)

        return default_value


def deduplicate_parameters(parameters):
    param_names = set()
    to_remove = object()
    for i, parameter in enumerate(parameters):
        if getattr(parameter, 'original_name', None) in param_names:
            parameters[i] = to_remove
        if getattr(parameter, 'original_name', None):
            param_names.add(parameter.original_name)

    without_duplicates = [param for param in parameters if param is not to_remove]
    padding_length = len(parameters) - len(without_duplicates)
    return without_duplicates + [None] * padding_length


def major_version():
    return Live.Application.get_application().get_major_version()