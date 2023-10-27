# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\__init__.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3291 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .abl_signal import Signal
from .dependency import DependencyError, depends, inject
from .disconnectable import CompoundDisconnectable, Disconnectable, disconnectable
from .event import Event, EventError, EventObject, MultiSlot, ObservablePropertyAlias, SerializableListenableProperties, Slot, SlotGroup, has_event, listenable_property, listens, listens_group
from .gcutil import histogram, instances_by_name, refget
from .isclose import isclose
from .live_api_utils import duplicate_clip_loop, is_parameter_bipolar, liveobj_changed, liveobj_valid, move_current_song_time
from .proxy import Proxy, ProxyBase
from .util import PY2, PY3, Bindable, BooleanContext, NamedTuple, OutermostOnlyContext, Slicer, aggregate_contexts, chunks, clamp, compose, const, dict_diff, find_if, first, flatten, forward_property, get_slice, group, in_range, index_if, infinite_context_manager, instance_decorator, is_contextmanager, is_iterable, is_matrix, lazy_attribute, linear, maybe, memoize, mixin, monkeypatch, monkeypatch_extend, negate, next, nop, old_hasattr, old_round, overlaymap, print_message, product, recursive_map, remove_if, second, sign, slice_size, slicer, third, to_slice, trace_value, union
__all__ = ('Bindable', 'BooleanContext', 'CompoundDisconnectable', 'DependencyError',
           'Disconnectable', 'Event', 'EventError', 'EventObject', 'MultiSlot', 'NamedTuple',
           'ObservablePropertyAlias', 'OutermostOnlyContext', 'Proxy', 'ProxyBase',
           'PY2', 'PY3', 'SerializableListenableProperties', 'Signal', 'Slicer',
           'Slot', 'SlotGroup', 'aggregate_contexts', 'chunks', 'clamp', 'compose',
           'const', 'depends', 'dict_diff', 'disconnectable', 'duplicate_clip_loop',
           'find_if', 'first', 'flatten', 'forward_property', 'get_slice', 'group',
           'has_event', 'histogram', 'in_range', 'index_if', 'infinite_context_manager',
           'inject', 'instance_decorator', 'instances_by_name', 'is_contextmanager',
           'is_iterable', 'is_matrix', 'is_parameter_bipolar', 'isclose', 'lazy_attribute',
           'linear', 'listenable_property', 'listens', 'listens_group', 'liveobj_changed',
           'liveobj_valid', 'maybe', 'memoize', 'mixin', 'monkeypatch', 'monkeypatch_extend',
           'move_current_song_time', 'negate', 'next', 'nop', 'overlaymap', 'old_round',
           'old_hasattr', 'print_message', 'product', 'recursive_map', 'refget',
           'remove_if', 'second', 'sign', 'slice_size', 'slicer', 'third', 'to_slice',
           'trace_value', 'union')