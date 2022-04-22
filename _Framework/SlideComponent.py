# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/SlideComponent.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 4192 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from .CompoundComponent import CompoundComponent
from .ScrollComponent import Scrollable, ScrollComponent
from .SubjectSlot import Subject, subject_slot
from .Util import clamp

class Slideable(Subject):
    __subject_events__ = ('page_offset', 'page_length', 'position', 'position_count',
                          'contents')

    def contents_range(self, pmin, pmax):
        pos_count = self.position_count
        first_pos = max(int(pmin), 0)
        last_pos = min(int(pmax), pos_count)
        return list(range(first_pos, last_pos))

    def contents(self, position):
        return False

    @property
    def position_count(self):
        raise NotImplementedError

    @property
    def position(self):
        raise NotImplementedError

    @property
    def page_offset(self):
        raise NotImplementedError

    @property
    def page_length(self):
        raise NotImplementedError


class SlideComponent(CompoundComponent, Scrollable):

    def __init__(self, slideable=None, *a, **k):
        (super(SlideComponent, self).__init__)(*a, **k)
        slideable = slideable or self
        self._slideable = slideable
        self._position_scroll, self._page_scroll = self.register_components(ScrollComponent(), ScrollComponent())
        self._position_scroll.scrollable = self
        self._page_scroll.can_scroll_up = self.can_scroll_page_up
        self._page_scroll.can_scroll_down = self.can_scroll_page_down
        self._page_scroll.scroll_down = self.scroll_page_down
        self._page_scroll.scroll_up = self.scroll_page_up
        self._on_position_changed.subject = slideable

    def set_scroll_up_button(self, button):
        self._position_scroll.set_scroll_up_button(button)

    def set_scroll_down_button(self, button):
        self._position_scroll.set_scroll_down_button(button)

    def set_scroll_page_up_button(self, button):
        self._page_scroll.set_scroll_up_button(button)

    def set_scroll_page_down_button(self, button):
        self._page_scroll.set_scroll_down_button(button)

    def scroll_page_up(self):
        self._scroll_page(1)

    def scroll_page_down(self):
        self._scroll_page(-1)

    def scroll_up(self):
        self._scroll_position(1)

    def scroll_down(self):
        self._scroll_position(-1)

    def can_scroll_page_up(self):
        model = self._slideable
        return model.position < model.position_count - model.page_length

    def can_scroll_page_down(self):
        return self._slideable.position > 0

    def can_scroll_up(self):
        return self.can_scroll_page_up()

    def can_scroll_down(self):
        return self.can_scroll_page_down()

    def _scroll_position(self, delta):
        if self.is_enabled():
            model = self._slideable
            model.position = clamp(model.position + delta, 0, model.position_count - model.page_length)

    def _scroll_page(self, sign):
        if self.is_enabled():
            model = self._slideable
            remainder = (model.position - model.page_offset) % model.page_length
            if sign > 0:
                delta = model.page_length - remainder
            elif remainder == 0:
                delta = -model.page_length
            else:
                delta = -remainder
            self._scroll_position(delta)

    def update(self):
        self._position_scroll.update()
        self._page_scroll.update()

    @subject_slot('position')
    def _on_position_changed(self):
        self._position_scroll.update()
        self._page_scroll.update()