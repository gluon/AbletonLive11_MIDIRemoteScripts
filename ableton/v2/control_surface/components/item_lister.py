# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\components\item_lister.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 9651 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map, zip
from ...base import EventObject, forward_property, listenable_property, listens, liveobj_valid
from .. import Component
from ..control import ButtonControl, control_list

class SimpleItemSlot(EventObject):

    def __init__(self, item=None, name='', nesting_level=-1, *a, **k):
        (super(SimpleItemSlot, self).__init__)(*a, **k)
        self._item = item
        self._name = name
        self._nesting_level = nesting_level
        self._SimpleItemSlot__on_name_changed.subject = self._item if getattr(self._item, 'name_has_listener', None) else None
        self._SimpleItemSlot__on_color_index_changed.subject = self._item if getattr(self._item, 'color_index_has_listener', None) else None

    @listenable_property
    def name(self):
        return self._name

    @property
    def item(self):
        return self._item

    @property
    def nesting_level(self):
        return self._nesting_level

    @listenable_property
    def color_index(self):
        return getattr(self._item, 'color_index', -1)

    @listens('name')
    def __on_name_changed(self):
        self.notify_name()
        self._name = self._item.name

    @listens('color_index')
    def __on_color_index_changed(self):
        self.notify_color_index()


class ItemSlot(SimpleItemSlot):

    def __init__(self, item=None, nesting_level=0, **k):
        (super(ItemSlot, self).__init__)(item=item, 
         name=item.name, nesting_level=nesting_level, **k)

    def __eq__(self, other):
        return id(self) == id(other) or self._item == other

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._item)

    _live_ptr = forward_property('_item')('_live_ptr')


class ItemProvider(EventObject):
    __events__ = ('items', 'selected_item')

    @property
    def items(self):
        return []

    @property
    def selected_item(self):
        pass


class ItemListerComponentBase(Component):
    __events__ = ('items', )

    def __init__(self, item_provider=ItemProvider(), num_visible_items=8, *a, **k):
        (super(ItemListerComponentBase, self).__init__)(*a, **k)
        self._item_offset = 0
        self._item_provider = item_provider
        self._items = []
        self._num_visible_items = num_visible_items
        self._ItemListerComponentBase__on_items_changed.subject = item_provider
        self.update_items()

    def reset_offset(self):
        self._item_offset = 0

    @property
    def items(self):
        return self._items

    @property
    def item_provider(self):
        return self._item_provider

    @property
    def item_offset(self):
        return self._item_offset

    @item_offset.setter
    def item_offset(self, offset):
        self._item_offset = offset
        self.update_items()

    def can_scroll_left(self):
        return self.item_offset > 0

    def can_scroll_right(self):
        items = self._item_provider.items[self.item_offset:]
        return len(items) > self._num_visible_items

    def scroll_left(self):
        self.item_offset -= 1

    def scroll_right(self):
        self.item_offset += 1

    def _adjust_offset(self):
        num_raw_items = len(self._item_provider.items)
        list_length = self._num_visible_items
        if list_length >= num_raw_items or self._item_offset >= num_raw_items - list_length:
            self._item_offset = max(0, num_raw_items - list_length)

    def update_items(self):
        for item in self._items:
            self.disconnect_disconnectable(item)

        self._adjust_offset()
        self._items = list(map(self.register_disconnectable, self._create_slots()))
        self.notify_items()

    def _create_slots(self):
        items = self._item_provider.items[self.item_offset:]
        num_slots = min(self._num_visible_items, len(items))
        new_items = []
        if num_slots > 0:
            new_items = [(self._create_slot)(index, *item) for index, item in enumerate(items[:num_slots]) if liveobj_valid(item[0])]
        return new_items

    def _create_slot(self, index, item, nesting_level):
        return ItemSlot(item=item, nesting_level=nesting_level)

    @listens('items')
    def __on_items_changed(self):
        self.update_items()
        self._on_items_changed()

    def _on_items_changed(self):
        pass


class ScrollComponent(Component):
    __events__ = ('scroll', )
    button = ButtonControl(color='ItemNavigation.ItemNotSelected', repeat=True)

    @button.pressed
    def button(self, button):
        self.notify_scroll()


class ScrollOverlayComponent(Component):

    def __init__(self, *a, **k):
        (super(ScrollOverlayComponent, self).__init__)(*a, **k)
        self._scroll_left_component, self._scroll_right_component = self.add_children(ScrollComponent(is_enabled=False), ScrollComponent(is_enabled=False))
        self._ScrollOverlayComponent__on_scroll_left.subject = self._scroll_left_component
        self._ScrollOverlayComponent__on_scroll_right.subject = self._scroll_right_component

    scroll_left_layer = forward_property('_scroll_left_component')('layer')
    scroll_right_layer = forward_property('_scroll_right_component')('layer')

    def can_scroll_left(self):
        raise NotImplementedError

    def can_scroll_right(self):
        raise NotImplementedError

    def scroll_left(self):
        raise NotImplementedError

    def scroll_right(self):
        raise NotImplementedError

    def update_scroll_buttons(self):
        if self.is_enabled():
            self._scroll_left_component.set_enabled(self.can_scroll_left())
            self._scroll_right_component.set_enabled(self.can_scroll_right())

    @listens('scroll')
    def __on_scroll_left(self):
        self.scroll_left()

    @listens('scroll')
    def __on_scroll_right(self):
        self.scroll_right()

    def update(self):
        super(ScrollOverlayComponent, self).update()
        if self.is_enabled():
            self.update_scroll_buttons()


class ItemListerComponent(ItemListerComponentBase):
    color_class_name = 'ItemNavigation'
    select_buttons = control_list(ButtonControl,
      unavailable_color=(color_class_name + '.NoItem'))

    def __init__(self, *a, **k):
        (super(ItemListerComponent, self).__init__)(*a, **k)
        self._scroll_overlay = self.add_children(ScrollOverlayComponent(is_enabled=True))
        self._scroll_overlay.can_scroll_left = self.can_scroll_left
        self._scroll_overlay.can_scroll_right = self.can_scroll_right
        self._scroll_overlay.scroll_left = self.scroll_left
        self._scroll_overlay.scroll_right = self.scroll_right
        self._ItemListerComponent__on_items_changed.subject = self
        self._ItemListerComponent__on_selection_changed.subject = self._item_provider

    scroll_left_layer = forward_property('_scroll_overlay')('scroll_left_layer')
    scroll_right_layer = forward_property('_scroll_overlay')('scroll_right_layer')

    @listens('items')
    def __on_items_changed(self):
        self.select_buttons.control_count = len(self.items)
        self._update_button_colors()
        self._scroll_overlay.update_scroll_buttons()

    @listens('selected_item')
    def __on_selection_changed(self):
        self._on_selection_changed()

    def _on_selection_changed(self):
        self._update_button_colors()

    def _items_equal(self, item, selected_item):
        return item == selected_item

    def _update_button_colors(self):
        selected_item = self._item_provider.selected_item
        for button, item in zip(self.select_buttons, self.items):
            button.color = self._color_for_button(button.index, self._items_equal(item, selected_item))

    def _color_for_button(self, button_index, is_selected):
        if is_selected:
            return self.color_class_name + '.ItemSelected'
        return self.color_class_name + '.ItemNotSelected'

    @select_buttons.pressed
    def select_buttons(self, button):
        self._on_select_button_pressed(button)

    @select_buttons.pressed_delayed
    def select_buttons(self, button):
        self._on_select_button_pressed_delayed(button)

    @select_buttons.released
    def select_buttons(self, button):
        self._on_select_button_released(button)

    @select_buttons.released_immediately
    def select_buttons(self, button):
        self._on_select_button_released_immediately(button)

    def _on_select_button_pressed(self, button):
        pass

    def _on_select_button_pressed_delayed(self, button):
        pass

    def _on_select_button_released(self, button):
        pass

    def _on_select_button_released_immediately(self, button):
        pass