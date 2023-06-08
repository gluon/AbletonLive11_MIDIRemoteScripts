<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/base/__init__.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 3064 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .abl_signal import Signal
from .dependency import DependencyError, depends, inject
from .disconnectable import CompoundDisconnectable, Disconnectable, disconnectable
from .event import Event, EventError, EventObject, MultiSlot, ObservablePropertyAlias, SerializableListenableProperties, Slot, SlotGroup, has_event, listenable_property, listens, listens_group
from .gcutil import histogram, instances_by_name, refget
from .isclose import isclose
from .live_api_utils import duplicate_clip_loop, is_parameter_bipolar, liveobj_changed, liveobj_valid
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
           'negate', 'next', 'nop', 'overlaymap', 'old_round', 'old_hasattr', 'print_message',
           'product', 'recursive_map', 'refget', 'remove_if', 'second', 'sign', 'slice_size',
           'slicer', 'third', 'to_slice', 'trace_value', 'union')
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
