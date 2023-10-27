# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\slideable_touch_strip_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 6062 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import range
from past.utils import old_div
from math import ceil
from ableton.v2.base import clamp, listens
from ableton.v2.control_surface import Component
from .touch_strip_element import MAX_PITCHBEND, DraggingBehaviour, SelectingBehaviour, TouchStripHandle, TouchStripStates

class SlideableTouchStripComponent(Component):

    def __init__(self, touch_slideable=None, dragging_enabled=False, *a, **k):
        (super(SlideableTouchStripComponent, self).__init__)(*a, **k)
        self._behaviour = DraggingBehaviour() if dragging_enabled else SelectingBehaviour()
        self._touch_strip_array = []
        self._on_page_length_changed.subject = touch_slideable
        self._on_position_changed.subject = touch_slideable
        self._on_contents_changed.subject = touch_slideable
        self._slideable = touch_slideable

    def set_page_strip(self, strip):
        self._on_page_touch_strip_value.subject = strip
        self._update_touch_strip_state(strip)

    def set_scroll_strip(self, strip):
        self._on_touch_strip_value.subject = strip
        self._update_touch_strip_state(strip)

    def update(self):
        super(SlideableTouchStripComponent, self).update()
        self._touch_strip_array = []
        self._update_touch_strips()

    def _update_touch_strips(self):
        self._update_touch_strip_state(self._on_touch_strip_value.subject)
        self._update_touch_strip_state(self._on_page_touch_strip_value.subject)

    def _scroll_to_led_position(self, scroll_pos, num_leds):
        scroll_pos += 1
        pos_count = self._slideable.position_count
        return min(int(old_div(float(scroll_pos), pos_count) * num_leds), num_leds)

    def _touch_strip_to_scroll_position(self, value):
        bank_size = self._slideable.page_length
        num_pad_rows = self._slideable.position_count
        max_pad_row = num_pad_rows - bank_size
        return min(int(old_div(float(value), MAX_PITCHBEND) * num_pad_rows), max_pad_row)

    def _touch_strip_to_page_position(self, value):
        bank_size = self._slideable.page_length
        num_pad_rows = self._slideable.position_count
        max_pad_row = num_pad_rows - bank_size
        offset = bank_size - self._slideable.page_offset
        return clamp(int(old_div(int(old_div(value, MAX_PITCHBEND) * num_pad_rows + offset), float(bank_size))) * bank_size - offset, 0, max_pad_row)

    def _scroll_to_touch_strip_position(self, scroll_pos):
        num_pad_rows = self._slideable.position_count
        return min(int(old_div(float(scroll_pos), num_pad_rows) * MAX_PITCHBEND), int(MAX_PITCHBEND))

    def _touch_strip_led_page_length(self, num_leds):
        return int(ceil(old_div(float(self._slideable.page_length), self._slideable.position_count) * num_leds))

    def _update_touch_strip_state(self, strip):
        if strip:
            if self.is_enabled():
                strip.behaviour = self._behaviour
                if len(self._touch_strip_array) != strip.state_count:
                    self._update_touch_strip_array(strip.state_count)
                model_pos = self._slideable.position
                led_pos = self._scroll_to_led_position(model_pos, strip.state_count)
                strip_pos = self._scroll_to_touch_strip_position(model_pos)
                array = list(self._touch_strip_array)
                led_page_length = self._touch_strip_led_page_length(strip.state_count)
                array[led_pos:led_pos + led_page_length] = [
                 TouchStripStates.STATE_FULL] * led_page_length
                led_size = old_div(MAX_PITCHBEND, strip.state_count)
                self._behaviour.handle = TouchStripHandle(range=(
                 -led_size, led_size * led_page_length),
                  position=strip_pos)
                strip.send_state(array[:strip.state_count])

    def _update_touch_strip_array(self, num_leds):
        if self.is_enabled():
            model = self._slideable

            def led_contents(i):
                pmin = old_div(float(i), num_leds) * model.position_count
                pmax = pmin + old_div(float(model.position_count), num_leds)
                return any(map(model.contents, model.contents_range(pmin, pmax)))

            array = [TouchStripStates.STATE_HALF if led_contents(i) else TouchStripStates.STATE_OFF for i in range(num_leds)]
            self._touch_strip_array = array

    @listens('value')
    def _on_touch_strip_value(self, value):
        if self.is_enabled():
            position = self._touch_strip_to_scroll_position(value)
            self._slideable.position = position

    @listens('value')
    def _on_page_touch_strip_value(self, value):
        if self.is_enabled():
            position = self._touch_strip_to_page_position(value)
            self._slideable.position = position

    @listens('page_length')
    def _on_page_length_changed(self):
        self._update_touch_strips()

    @listens('position')
    def _on_position_changed(self):
        self._update_touch_strips()

    @listens('contents')
    def _on_contents_changed(self):
        self._touch_strip_array = []
        self._update_touch_strips()