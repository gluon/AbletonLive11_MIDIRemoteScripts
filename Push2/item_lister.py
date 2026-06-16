# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\item_lister.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1297 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import ItemListerComponent as ItemListerComponentBase
from ableton.v2.control_surface.components import ItemSlot, SimpleItemSlot

class IconItemSlot(SimpleItemSlot):

    def __init__(self, icon='', *a, **k):
        (super(IconItemSlot, self).__init__)(*a, **k)
        self._icon = icon

    @property
    def icon(self):
        return self._icon


class ItemListerComponent(ItemListerComponentBase):

    def _create_slot(self, index, item, nesting_level):
        items = self._item_provider.items[self.item_offset:]
        num_slots = min(self._num_visible_items, len(items))
        slot = None
        if index == 0 and self.can_scroll_left():
            slot = IconItemSlot(icon='page_left.svg')
            slot.is_scrolling_indicator = True
        else:
            if index == num_slots - 1 and self.can_scroll_right():
                slot = IconItemSlot(icon='page_right.svg')
                slot.is_scrolling_indicator = True
            else:
                slot = ItemSlot(item=item, nesting_level=nesting_level)
                slot.is_scrolling_indicator = False
        return slot