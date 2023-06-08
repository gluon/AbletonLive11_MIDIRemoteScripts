from __future__ import absolute_import, print_function, unicode_literals
from sys import maxsize
import Live
from ableton.v2.control_surface.components import find_nearest_color
from . import clamp, find_if, liveobj_valid
from .util import hex_to_rgb
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

def song():
    global _current_song
    if liveobj_valid(_current_song):
        return _current_song
    _current_song = Live.Application.get_application().get_document()
    return _current_song


def set_song(song_obj, from_test=False):
    global _current_song
    _current_song = song_obj


def is_song_recording():
    return song().session_record or song().record_mode


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


def scene_display_name(scene, strip_space=True):
    name = scene.name.strip() if strip_space else scene.name
    return name or 'Scene {}'.format(scene_index(scene) + 1)


def clip_display_name(clip):
    return clip.name or '[unnamed]'


def clip_slot_display_name(clip_slot):
    if liveobj_valid(clip_slot.clip):
        return clip_display_name(clip_slot.clip)
    return '[empty slot]'


def arm_track(track, exclusive=None):
    if liveobj_valid(track):
        if track.can_be_armed:
            exclusive = exclusive if exclusive is not None else song().exclusive_arm
            new_value = not track.arm
            for t in song().tracks:
                if t.can_be_armed:
                    if not (t == track or track).is_part_of_selection or t.is_part_of_selection:
                        t.arm = new_value
                    else:
                        if exclusive:
                            if t.arm:
                                t.arm = False


def delete_clip(clip):
    if liveobj_valid(clip):
        if clip.is_arrangement_clip:
            clip.canonical_parent.delete_clip(clip)
        else:
            clip.canonical_parent.delete_clip()


def delete_notes_with_pitch(clip, pitch):
    if liveobj_valid(clip):
        if clip.is_midi_clip:
            clip.remove_notes_extended(from_time=0,
              from_pitch=pitch,
              time_span=maxsize,
              pitch_span=1)


def get_parameter_by_name(name, device):
    if liveobj_valid(device):
        return find_if(lambda p: p.original_name == name and liveobj_valid(p) and p.is_enabled
, device.parameters)


def parameter_display_name(parameter):
    if liveobj_valid(parameter):
        try:
            return parameter.display_name
        except AttributeError:
            return TRANSLATED_MIXER_PARAMETER_NAMES.get(parameter.name, parameter.name)

        return ''


def normalized_parameter_value(parameter):
    value = 0.0
    if liveobj_valid(parameter):
        param_range = parameter.max - parameter.min
        value = (parameter.value - parameter.min) / param_range
    return clamp(value, 0.0, 1.0)


def parameter_value_to_midi_value(parameter, max_value=128):
    return int(normalized_parameter_value(parameter) * (max_value - 1))


def is_parameter_quantized(parameter, device):
    is_quantized = False
    if liveobj_valid(parameter):
        device_class = getattr(device, 'class_name', None)
        is_quantized = (parameter.is_quantized) or ((device_class in UNDECLARED_QUANTIZED_PARAMETERS) and (parameter.name in UNDECLARED_QUANTIZED_PARAMETERS[device_class]))
    return is_quantized


def toggle_or_cycle_parameter_value(parameter):
    if liveobj_valid(parameter):
        if parameter.is_quantized:
            if parameter.value + 1 > parameter.max:
                parameter.value = parameter.min
            else:
                parameter.value = parameter.value + 1
        else:
            parameter.value = parameter.max if parameter.value == parameter.min else parameter.min


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