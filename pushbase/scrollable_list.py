# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\scrollable_list.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 19884 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import object, str
from past.utils import old_div
from functools import partial
from ableton.v2.base import BooleanContext, EventObject, clamp, forward_property, in_range, index_if, listens, task
from ableton.v2.control_surface import Component, defaults
from ableton.v2.control_surface.components import Scrollable, ScrollComponent
from ableton.v2.control_surface.control import ButtonControl, EncoderControl, control_list
from . import consts

class ScrollableListItem(object):

    def __init__(self, index=None, content=None, scrollable_list=None, *a, **k):
        (super(ScrollableListItem, self).__init__)(*a, **k)
        self._content = content
        self._index = index
        self._scrollable_list = scrollable_list

    def __str__(self):
        return str(self._content)

    @property
    def content(self):
        return self._content

    @property
    def index(self):
        return self._index

    @property
    def container(self):
        return self._scrollable_list

    @property
    def is_selected(self):
        return self._scrollable_list and self._scrollable_list.is_selected(self)

    def select(self):
        return self._scrollable_list and self._scrollable_list.select_item(self)


class ScrollableList(EventObject, Scrollable):
    __events__ = ('selected_item', 'item_activated', 'scroll')
    item_type = ScrollableListItem
    fixed_offset = None

    def __init__(self, num_visible_items=1, item_type=None, *a, **k):
        (super(ScrollableList, self).__init__)(*a, **k)
        if item_type != None:
            self.item_type = item_type
        self._items = []
        self._num_visible_items = num_visible_items
        self._selected_item_index = -1
        self._last_activated_item_index = None
        self._offset = 0
        self._pager = Scrollable()
        self._pager.scroll_up = self.prev_page
        self._pager.scroll_down = self.next_page
        self._pager.can_scroll_up = self.can_scroll_up
        self._pager.can_scroll_down = self.can_scroll_down

    @property
    def pager(self):
        return self._pager

    def scroll_up(self):
        if self.can_scroll_up():
            self.select_item_index_with_border(self.selected_item_index - 1, 1)
            self.notify_scroll()

    def can_scroll_up(self):
        return self._selected_item_index > 0

    def scroll_down(self):
        if self.can_scroll_down():
            self.select_item_index_with_border(self.selected_item_index + 1, 1)
            self.notify_scroll()

    def can_scroll_down(self):
        return self._selected_item_index < len(self._items) - 1

    def _get_num_visible_items(self):
        return self._num_visible_items

    def _set_num_visible_items(self, num_items):
        self._num_visible_items = num_items
        self._normalize_offset(self._selected_item_index)

    num_visible_items = property(_get_num_visible_items, _set_num_visible_items)

    @property
    def visible_items(self):
        return self.items[self._offset:self._offset + self._num_visible_items]

    def select_item_index_with_offset(self, index, offset):
        if index != self.selected_item_index:
            if index >= 0:
                if index < len(self._items):
                    self._offset = clamp(index - offset, 0, len(self._items))
                    self._normalize_offset(index)
                    self._do_set_selected_item_index(index)

    def select_item_index_with_border(self, index, border_size):
        if self.fixed_offset is not None:
            self.select_item_index_with_offset(index, self.fixed_offset)
        else:
            if index >= 0:
                if index < len(self._items):
                    if not in_range(index, self._offset + border_size, self._offset + self._num_visible_items - border_size):
                        offset = index - (self._num_visible_items - 2 * border_size) if self.selected_item_index < index else index - border_size
                        self._offset = clamp(offset, 0, len(self._items))
                    self._normalize_offset(index)
                    self._do_set_selected_item_index(index)

    def next_page(self):
        if self.can_scroll_down():
            current_page = old_div(self.selected_item_index, self.num_visible_items)
            last_page_index = len(self.items) - self.num_visible_items
            if self.selected_item_index < last_page_index:
                index = clamp((current_page + 1) * self.num_visible_items, 0, len(self.items) - self.num_visible_items)
            else:
                index = len(self.items) - 1
            self.select_item_index_with_offset(index, 0)

    def prev_page(self):
        if self.can_scroll_up():
            current_page = old_div(self.selected_item_index, self.num_visible_items)
            last_page_index = len(self.items) - self.num_visible_items
            if self.selected_item_index <= last_page_index:
                index = clamp((current_page - 1) * self.num_visible_items, 0, len(self.items) - self.num_visible_items)
            else:
                index = max(len(self.items) - self.num_visible_items, 0)
            self.select_item_index_with_offset(index, 0)

    def _set_selected_item_index(self, index):
        if index >= 0:
            if index < len(self._items):
                self._normalize_offset(index)
                self._do_set_selected_item_index(index)

    def _get_selected_item_index(self):
        return self._selected_item_index

    selected_item_index = property(_get_selected_item_index, _set_selected_item_index)

    def _normalize_offset(self, index):
        if index >= 0:
            if index >= self._offset + self._num_visible_items:
                self._offset = index - (self._num_visible_items - 1)
            else:
                if index < self._offset:
                    self._offset = index
            self._offset = clamp(self._offset, 0, len(self._items) - self._num_visible_items)

    @property
    def selected_item(self):
        if in_range(self._selected_item_index, 0, len(self._items)):
            return self._items[self.selected_item_index]

    @property
    def items(self):
        return self._items

    def assign_items(self, items):
        old_selection = str(self.selected_item)
        for item in self._items:
            item._scrollable_list = None

        self._items = tuple([self.item_type(index=index, content=item, scrollable_list=self) for index, item in enumerate(items)])
        if self._items:
            new_selection = index_if(lambda item: str(item) == old_selection
, self._items)
            self._selected_item_index = new_selection if in_range(new_selection, 0, len(self._items)) else 0
            self._normalize_offset(self._selected_item_index)
        else:
            self._offset = 0
            self._selected_item_index = -1
        self._last_activated_item_index = None
        self.notify_selected_item()
        self.request_notify_item_activated()

    def select_item(self, item):
        self.selected_item_index = item.index

    def is_selected(self, item):
        return item and item.index == self.selected_item_index

    def request_notify_item_activated(self):
        if self._selected_item_index != self._last_activated_item_index:
            self._last_activated_item_index = self._selected_item_index
            self.notify_item_activated()

    def _do_set_selected_item_index(self, index):
        if index != self._selected_item_index:
            self._selected_item_index = index
            self.notify_selected_item()


class ActionListItem(ScrollableListItem):
    supports_action = False

    def action(self):
        pass


class ActionList(ScrollableList):
    item_type = ActionListItem


class DefaultItemFormatter(object):
    action_message = 'Loading...'

    def __call__(self, index, item, action_in_progress):
        display_string = ''
        if item:
            display_string += consts.CHAR_SELECT if item.is_selected else ' '
            display_string += self.action_message if action_in_progress else str(item)
        return display_string


class ListComponent(Component):
    __events__ = ('item_action', 'selected_item')
    SELECTION_DELAY = 0.5
    ENCODER_FACTOR = 10.0
    empty_list_message = ''
    _current_action_item = None
    _last_action_item = None
    action_button = ButtonControl(color='Browser.Load')
    encoders = control_list(EncoderControl)

    def __init__(self, scrollable_list=None, data_sources=tuple(), *a, **k):
        (super(ListComponent, self).__init__)(*a, **k)
        self._data_sources = data_sources
        self._activation_task = task.Task()
        self._action_on_scroll_task = task.Task()
        self._scrollable_list = None
        self._scroller = ScrollComponent(parent=self)
        self._pager = ScrollComponent(parent=self)
        self.last_action_item = lambda: self._last_action_item
        self.item_formatter = DefaultItemFormatter()
        for c in (self._scroller, self._pager):
            for button in (c.scroll_up_button, c.scroll_down_button):
                button.color = 'List.ScrollerOn'
                button.pressed_color = None
                button.disabled_color = 'List.ScrollerOff'

        if scrollable_list == None:
            self.scrollable_list = ActionList(num_visible_items=(len(data_sources)))
        else:
            self.scrollable_list = scrollable_list
        self._scrollable_list.num_visible_items = len(data_sources)
        self._delay_activation = BooleanContext()
        self._selected_index_float = 0.0
        self._in_encoder_selection = BooleanContext(False)
        self._execute_action_task = self._tasks.add(task.sequence(task.delay(1), task.run(self._execute_action)))
        self._execute_action_task.kill()

    @property
    def _trigger_action_on_scrolling(self):
        return self.action_button.is_pressed

    def _get_scrollable_list(self):
        return self._scrollable_list

    def _set_scrollable_list(self, new_list):
        if new_list != self._scrollable_list:
            self._scrollable_list = new_list
            if new_list != None:
                new_list.num_visible_items = len(self._data_sources)
                self._scroller.scrollable = new_list
                self._pager.scrollable = new_list.pager
                self._on_scroll.subject = new_list
                self._selected_index_float = new_list.selected_item_index
            else:
                self._scroller.scrollable = ScrollComponent.default_scrollable
                self._scroller.scrollable = ScrollComponent.default_pager
            self._on_selected_item_changed.subject = new_list
            self.update()

    scrollable_list = property(_get_scrollable_list, _set_scrollable_list)

    def set_data_sources(self, sources):
        self._data_sources = sources
        if self._scrollable_list:
            self._scrollable_list.num_visible_items = len(sources)
        self._update_display()

    select_next_button = forward_property('_scroller')('scroll_down_button')
    select_prev_button = forward_property('_scroller')('scroll_up_button')
    next_page_button = forward_property('_pager')('scroll_down_button')
    prev_page_button = forward_property('_pager')('scroll_up_button')

    def on_enabled_changed(self):
        super(ListComponent, self).on_enabled_changed()
        if not self.is_enabled():
            self._execute_action_task.kill()

    @listens('scroll')
    def _on_scroll(self):
        if self._trigger_action_on_scrolling:
            trigger_selected = partial(self._trigger_action, self.selected_item)
            self._action_on_scroll_task.kill()
            self._action_on_scroll_task = self._tasks.add(task.sequence(task.wait(defaults.MOMENTARY_DELAY), task.delay(1), task.run(trigger_selected)))

    @listens('selected_item')
    def _on_selected_item_changed(self):
        self._scroller.update()
        self._pager.update()
        self._update_display()
        self._update_action_feedback()
        self._activation_task.kill()
        self._action_on_scroll_task.kill()
        if self.SELECTION_DELAY and self._delay_activation:
            self._activation_task = self._tasks.add(task.sequence(task.wait(self.SELECTION_DELAY), task.run(self._scrollable_list.request_notify_item_activated)))
        else:
            self._scrollable_list.request_notify_item_activated()
        if not self._in_encoder_selection:
            self._selected_index_float = float(self._scrollable_list.selected_item_index)
        self.notify_selected_item(self._scrollable_list.selected_item)

    @encoders.value
    def encoders(self, value, encoder):
        self._add_offset_to_selected_index(value)

    def _add_offset_to_selected_index(self, offset):
        if self.is_enabled():
            if self._scrollable_list:
                with self._delay_activation():
                    with self._in_encoder_selection():
                        self._selected_index_float = clamp(self._selected_index_float + offset * self.ENCODER_FACTOR, 0, len(self._scrollable_list.items))
                        self._scrollable_list.select_item_index_with_border(int(self._selected_index_float), 1)

    @action_button.pressed
    def action_button(self, button):
        if self._current_action_item == None:
            self._trigger_action(self.next_item if self._action_target_is_next_item() else self.selected_item)

    def do_trigger_action(self, item):
        item.action()
        self.notify_item_action(item)

    def _trigger_action(self, item):
        if self.is_enabled():
            if self._can_be_used_for_action(item):
                if self._scrollable_list != None:
                    self._scrollable_list.select_item(item)
                self._current_action_item = item
                self.update()
                self._execute_action_task.restart()

    def _execute_action(self):
        if self._current_action_item != None:
            self.do_trigger_action(self._current_action_item)
            self._last_action_item = self._current_action_item
            self._current_action_item = None
            self.update()

    @property
    def selected_item(self):
        if self._scrollable_list != None:
            return self._scrollable_list.selected_item

    @property
    def next_item(self):
        item = None
        if self._scrollable_list != None:
            all_items = self._scrollable_list.items
            next_index = self._scrollable_list.selected_item_index + 1
            item = all_items[next_index] if in_range(next_index, 0, len(all_items)) else None
        return item

    def _can_be_used_for_action(self, item):
        return item != None and item.supports_action and item != self.last_action_item()

    def _action_target_is_next_item(self):
        return self.selected_item == self.last_action_item() and self._can_be_used_for_action(self.next_item)

    def _update_action_feedback(self):
        color = 'Browser.Loading'
        if self._current_action_item == None:
            if self._action_target_is_next_item():
                color = 'Browser.LoadNext'
            else:
                if self._can_be_used_for_action(self.selected_item):
                    color = 'Browser.Load'
                else:
                    color = 'Browser.LoadNotPossible'
        self.action_button.color = color

    def _update_display(self):
        visible_items = self._scrollable_list.visible_items if self._scrollable_list else []
        for index, data_source in enumerate(self._data_sources):
            item = visible_items[index] if index < len(visible_items) else None
            action_in_progress = item and item == self._current_action_item
            display_string = self.item_formatter(index, item, action_in_progress)
            data_source.set_display_string(display_string)

        if not visible_items:
            if self._data_sources:
                if self.empty_list_message:
                    self._data_sources[0].set_display_string(self.empty_list_message)

    def update(self):
        super(ListComponent, self).update()
        if self.is_enabled():
            self._update_action_feedback()
            self._update_display()