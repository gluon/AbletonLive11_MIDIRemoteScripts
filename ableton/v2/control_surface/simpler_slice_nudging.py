# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\simpler_slice_nudging.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 4644 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import round
from past.utils import old_div
from contextlib import contextmanager
import Live
from ..base import EventObject, clamp, find_if, listens, liveobj_valid
CENTERED_NUDGE_VALUE = 0.5
MINIMUM_SLICE_DISTANCE = 2

def is_simpler(device):
    return device and device.class_name == 'OriginalSimpler'


class SimplerSliceNudging(EventObject):
    _simpler = None
    _nudge_parameter = None

    def set_device(self, device):
        self._simpler = device if is_simpler(device) else None
        self._SimplerSliceNudging__on_selected_slice_changed.subject = self._simpler
        with self._updating_nudge_parameter():
            self._nudge_parameter = find_if(lambda p: p.name == 'Nudge'
, self._simpler.parameters if liveobj_valid(self._simpler) else [])

    @contextmanager
    def _updating_nudge_parameter(self):
        if self._nudge_parameter:
            self._nudge_parameter.set_display_value_conversion(None)
        yield
        if self._nudge_parameter:
            self._nudge_parameter.set_display_value_conversion(self._display_value_conversion)
        self._SimplerSliceNudging__on_nudge_delta.subject = self._nudge_parameter

    def _can_access_slicing_properties(self):
        return liveobj_valid(self._simpler) and liveobj_valid(self._simpler.sample) and self._simpler.current_playback_mode == Live.SimplerDevice.PlaybackMode.slicing

    @listens('view.selected_slice')
    def __on_selected_slice_changed(self):
        if self._nudge_parameter:
            self._nudge_parameter.notify_value()

    @listens('delta')
    def __on_nudge_delta(self, delta):
        if self._can_access_slicing_properties():
            old_slice_time = self._simpler.view.selected_slice
            if old_slice_time >= 0:
                if self._is_first_slice_at_time(old_slice_time):
                    new_start = self._new_start_marker_time(old_slice_time, delta)
                    self._simpler.sample.start_marker = new_start
                    return
                new_slice_time = old_slice_time + self._sample_change_from_delta(delta)
                if old_slice_time != new_slice_time:
                    original_slices = self._simpler.sample.slices
                    returned_time = self._simpler.sample.move_slice(old_slice_time, new_slice_time)
                    try:
                        self._simpler.view.selected_slice = returned_time
                    except RuntimeError:
                        self._simpler.view.selected_slice = self._simpler.slices[list(original_slices).index(old_slice_time)]

    def _is_first_slice_at_time(self, slice_time):
        start_sample = self._simpler.sample.start_marker
        return abs(slice_time - start_sample) < MINIMUM_SLICE_DISTANCE

    def _new_start_marker_time(self, old_slice_time, delta):
        change_in_samples = self._sample_change_from_delta(delta)
        new_start_marker_time = old_slice_time + change_in_samples
        return clamp(new_start_marker_time, 0, self._simpler.sample.length - MINIMUM_SLICE_DISTANCE)

    def _sample_change_from_delta(self, delta):
        sample_length = self._simpler.sample.length
        change_in_samples = round(old_div(delta * sample_length, 10))
        return int(change_in_samples)

    def _display_value_conversion(self, _value):
        selected_slice = self._simpler.view.selected_slice if self._can_access_slicing_properties() else -1
        if selected_slice >= 0:
            return str(selected_slice)
        return '-'