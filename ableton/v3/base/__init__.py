<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import BooleanContext, CompoundDisconnectable, Disconnectable, EventObject, MultiSlot, ObservablePropertyAlias, SlotGroup, chunks, clamp, compose, const, depends, duplicate_clip_loop, find_if, first, flatten, group, index_if, inject, is_iterable, lazy_attribute, listenable_property, listens, listens_group, liveobj_changed, liveobj_valid, memoize, mixin, move_current_song_time, nop, old_hasattr, recursive_map, sign, task
from ableton.v2.base.event import EventObjectMeta
from .live_api_util import all_visible_tracks, any_track_armed, arm_track, clip_display_name, clip_slot_display_name, delete_clip, delete_notes_with_pitch, find_parent_track, get_parameter_by_name, is_parameter_quantized, is_song_recording, is_track_armed, liveobj_color_to_midi_rgb_values, liveobj_color_to_value_from_palette, normalized_parameter_value, parameter_display_name, parameter_value_to_midi_value, scene_display_name, scene_index, set_song, song, toggle_or_cycle_parameter_value, track_index
from .util import as_ascii, get_default_ascii_translations, hex_to_rgb
__all__ = ('BooleanContext', 'CompoundDisconnectable', 'Disconnectable', 'EventObject',
           'EventObjectMeta', 'MultiSlot', 'ObservablePropertyAlias', 'SlotGroup',
           'all_visible_tracks', 'any_track_armed', 'arm_track', 'as_ascii', 'chunks',
           'clamp', 'clip_display_name', 'clip_slot_display_name', 'compose', 'const',
           'delete_clip', 'delete_notes_with_pitch', 'depends', 'duplicate_clip_loop',
           'find_if', 'find_parent_track', 'first', 'flatten', 'get_default_ascii_translations',
           'get_parameter_by_name', 'group', 'hex_to_rgb', 'index_if', 'inject',
           'is_iterable', 'is_parameter_quantized', 'is_song_recording', 'is_track_armed',
           'lazy_attribute', 'listenable_property', 'listens', 'listens_group', 'liveobj_changed',
           'liveobj_color_to_midi_rgb_values', 'liveobj_color_to_value_from_palette',
           'liveobj_valid', 'memoize', 'mixin', 'move_current_song_time', 'nop',
           'normalized_parameter_value', 'old_hasattr', 'parameter_display_name',
           'parameter_value_to_midi_value', 'recursive_map', 'scene_display_name',
           'scene_index', 'set_song', 'sign', 'song', 'task', 'toggle_or_cycle_parameter_value',
           'track_index')
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/base/__init__.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 1320 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject, MultiSlot, ObservablePropertyAlias, chunks, clamp, const, depends, find_if, first, flatten, group, index_if, inject, is_iterable, lazy_attribute, listenable_property, listens, listens_group, liveobj_changed, liveobj_valid, mixin, nop, old_hasattr, recursive_map, task
from .component_util import add_scroll_encoder, skin_scroll_buttons
from .live_api_util import is_song_recording, toggle_or_cycle_parameter_value, track_can_record
__all__ = ('EventObject', 'MultiSlot', 'ObservablePropertyAlias', 'add_scroll_encoder',
           'chunks', 'clamp', 'const', 'depends', 'find_if', 'first', 'flatten',
           'group', 'index_if', 'inject', 'is_iterable', 'is_song_recording', 'lazy_attribute',
           'listenable_property', 'listens', 'listens_group', 'liveobj_changed',
           'liveobj_valid', 'mixin', 'nop', 'old_hasattr', 'recursive_map', 'skin_scroll_buttons',
           'task', 'toggle_or_cycle_parameter_value', 'track_can_record')
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
