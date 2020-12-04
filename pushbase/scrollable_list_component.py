#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/scrollable_list_component.py
u"""
Scrollable list component.
"""
from __future__ import absolute_import, print_function, unicode_literals
from builtins import zip
from builtins import map
from builtins import range
from functools import partial
from ableton.v2.base import EventObject, in_range, Event
from ableton.v2.base.abl_signal import short_circuit_signal
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.elements import DisplayDataSource
from . import consts

class ScrollableListComponent(Component):
    u"""
    Component for handling a list of options with a limtied set of
    buttons and display segments.
    """
    __events__ = (Event(name=u'change_option', doc=u' Event signaled when the selected option changes '), Event(name=u'press_option', signal=short_circuit_signal, doc=u'\n       Event signaled when an option is pressed getting the option as\n       parameter.  The ScrollableListComponent is connected to it, if\n       you want to override selection behaviour, connect to the front\n       and return True from your handler.\n       '))
    num_segments = 8
    display_line = 3
    jump_size = 3
    ARROW_LEFT = u'   <<   '
    ARROW_RIGHT = u'   >>   '

    def __init__(self, *a, **k):
        super(ScrollableListComponent, self).__init__(*a, **k)
        self._data_sources = [ DisplayDataSource() for _ in range(self.num_segments) ]
        self._selected_option = None
        self._offset_index = 0
        self._option_names = []
        self._select_buttons = []
        self._select_button_slots = self.register_disconnectable(EventObject())
        self.register_slot(self, self._set_selected_option, u'press_option')

    def set_display_line(self, line):
        if line:
            sources = self._data_sources
            line.set_num_segments(len(sources))
            for segment in range(len(sources)):
                line.segment(segment).set_data_source(sources[segment])

    def set_select_buttons(self, buttons):
        self._select_button_slots.disconnect()
        self._select_buttons = buttons or []
        for b in self._select_buttons:
            self._select_button_slots.register_slot(b, self._on_select_value, u'value', extra_kws=dict(identify_sender=True))

        self.update()

    @property
    def offset_index(self):
        return self._offset_index

    def scroll_right(self):
        return self._scroll(1)

    def scroll_left(self):
        return self._scroll(-self.jump_size)

    def _get_option_names(self):
        return self._option_names

    def _set_option_names(self, names):
        self._option_names = names
        self._normalize_offset()
        self.update()

    option_names = property(_get_option_names, lambda self, x: self._set_option_names(x))

    def _get_selected_option(self):
        return self._selected_option

    def _set_selected_option(self, selected_option):
        if selected_option != self._selected_option:
            assert selected_option == None or in_range(selected_option, 0, len(self._option_names))
            self._selected_option = selected_option
            self.notify_change_option(selected_option)
            self.update()

    selected_option = property(_get_selected_option, _set_selected_option)

    def _has_select_button(self, index):
        return len(self._select_buttons) == self.num_segments and self._select_buttons[index] != None

    def _maximal_offset(self):
        if len(self._option_names) > self.num_segments:
            return len(self._option_names) - self.num_segments + 1
        else:
            return 0

    def _normalize_offset(self):
        quantized_offset = self._offset_index - self._offset_index % -self.jump_size
        self._offset_index = max(0, min(self._maximal_offset(), quantized_offset))

    def _scroll(self, delta):
        old_offset = self._offset_index
        self._offset_index += delta
        self._normalize_offset()
        if self._offset_index != old_offset:
            self.update()
            return True
        return False

    def _on_select_value(self, value, sender):
        if not self.is_enabled() or not value:
            return
        index = list(self._select_buttons).index(sender)
        if index == 0 and self._offset_index != 0:
            self.scroll_left()
        elif index == self.num_segments - 1 and self._offset_index < self._maximal_offset():
            self.scroll_right()
        elif self._offset_index == 0:
            self.notify_press_option(index if index < len(self._option_names) else None)
        else:
            self.notify_press_option(index + self._offset_index - 1)

    def _get_display_string(self, option_index):
        if option_index < len(self._option_names):
            decorator = consts.CHAR_SELECT if option_index == self.selected_option else u''
            return decorator + self._option_names[option_index]
        else:
            return u''

    def update(self):
        super(ScrollableListComponent, self).update()
        if not self.is_enabled():
            return
        first_segment, max_segment = 0, self.num_segments
        if self._offset_index > 0:
            self._data_sources[0].set_display_string(self.ARROW_LEFT)
            if self._has_select_button(0):
                self._select_buttons[0].set_light(u'List.ScrollerOn')
            first_segment = 1
        if self._offset_index < self._maximal_offset():
            self._data_sources[-1].set_display_string(self.ARROW_RIGHT)
            if self._has_select_button(-1):
                self._select_buttons[-1].set_light(u'List.ScrollerOn')
            max_segment -= 1
        for i, j in zip(range(first_segment, max_segment), range(self._offset_index, self._offset_index + self.num_segments)):
            self._data_sources[i].set_display_string(self._get_display_string(j))
            if self._has_select_button(i):
                if i < len(self.option_names):
                    if j == self.selected_option:
                        self._select_buttons[i].set_light(u'Option.Selected')
                    else:
                        self._select_buttons[i].set_light(u'Option.Unselected')
                else:
                    self._select_buttons[i].set_light(u'Option.Unused')


class ScrollableListWithTogglesComponent(ScrollableListComponent):
    u"""
    Scrollable list that has a toggle button associated with every
    available option.
    """
    __events__ = (u'toggle_option',)

    def __init__(self, *a, **k):
        super(ScrollableListWithTogglesComponent, self).__init__(*a, **k)

        def create_state_slot(idx):
            return self.register_slot(None, partial(self._on_state_button_value, idx), u'value')

        self._state_button_slots = list(map(create_state_slot, range(self.num_segments)))
        self._option_states = []

    def set_state_buttons(self, state_buttons):
        state_buttons = state_buttons or [ None for _ in range(self.num_segments) ]
        for slot, button in zip(self._state_button_slots, state_buttons):
            slot.subject = button

        self._update_state_buttons()

    def option_state(self, index):
        return self._option_states[index]

    def set_option_state(self, index, value):
        if index < len(self._option_states) and value != self._option_states[index]:
            self._option_states[index] = value
            self.notify_toggle_option(index, value)
            self._update_state_buttons()

    def _on_state_button_value(self, index, value):
        min_button_index = int(bool(self._offset_index))
        max_button_index = len(self._state_button_slots) - int(self._maximal_offset() > self._offset_index)
        if self.is_enabled() and value:
            if in_range(index, min_button_index, max_button_index):
                index += max(0, self._offset_index - 1)
                if index < len(self._option_states):
                    new_state = not self.option_state(index)
                    self.set_option_state(index, new_state)
                else:
                    self.notify_press_option(None)
            else:
                self.notify_press_option(None)

    def _set_option_names(self, names):
        u""" overrides """
        if self.option_names != names:
            self._option_states = [ False for _ in range(len(names)) ]
            super(ScrollableListWithTogglesComponent, self)._set_option_names(names)

    def update(self):
        super(ScrollableListWithTogglesComponent, self).update()
        self._update_state_buttons()

    def _update_state_buttons(self):
        if not self.is_enabled():
            return
        buttons = [ slot.subject for slot in self._state_button_slots ]
        if buttons[0]:
            first_button, max_button = 0, len(buttons)
            if self._offset_index > 0:
                buttons[0].set_light(u'Option.Off')
                first_button = 1
            if self._offset_index < self._maximal_offset():
                buttons[-1].set_light(u'Option.Off')
                max_button -= 1
            for state, button in zip(self._option_states[self._offset_index:], buttons[first_button:max_button]):
                if button != None:
                    if state:
                        button.set_light(u'Option.On')
                    else:
                        button.set_light(u'Option.Off')

            for button in buttons[len(self._option_states):]:
                if button != None:
                    button.set_light(u'Option.Off')
