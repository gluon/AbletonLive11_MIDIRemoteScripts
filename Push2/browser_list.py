# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\browser_list.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3968 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from itertools import islice
import Live
from ableton.v2.base import EventObject, clamp, listenable_property, nop
from model.uniqueid import UniqueIdMixin

class BrowserList(EventObject, UniqueIdMixin):
    LAZY_ACCESS_COUNT = 1000
    LAZY_ACCESS_THRESHOLD = LAZY_ACCESS_COUNT - 100

    def __init__(self, item_iterator=None, item_wrapper=nop, limit=-1, *a, **k):
        (super(BrowserList, self).__init__)(*a, **k)
        self._selected_index = -1
        self._item_iterator = item_iterator
        self._item_wrapper = item_wrapper
        self._limit = limit
        self._access_all = False
        self._items = []
        self._update_items()

    def _get_limit(self):
        return self._limit

    def _set_limit(self, value):
        if value != self._limit:
            self._limit = value
            self._access_all = False
            self._update_items()
            self.notify_items()
            if value != -1:
                self.selected_index = -1

    limit = property(_get_limit, _set_limit)

    def _get_access_all(self):
        return self._access_all

    def _set_access_all(self, access_all):
        if self._access_all != access_all:
            self._access_all = access_all
            self._limit = -1
            self._update_items()
            self.notify_items()

    access_all = property(_get_access_all, _set_access_all)

    @listenable_property
    def items(self):
        if self.limit > 0:
            return self._items[:self.limit]
        if not self._access_all:
            return self._items[:self.LAZY_ACCESS_COUNT]
        return self._items

    def _update_items(self):
        if isinstance(self._item_iterator, Live.Browser.BrowserItemIterator):
            if self.limit > 0 and len(self._items) < self.limit:
                next_slice = islice(self._item_iterator, self.limit)
            else:
                if not self._access_all or len(self._items) < self.LAZY_ACCESS_COUNT:
                    next_slice = islice(self._item_iterator, self.LAZY_ACCESS_COUNT - len(self._items))
                else:
                    next_slice = self._item_iterator
            self._items.extend(list(map(self._item_wrapper, next_slice)))
        else:
            if len(self._items) < len(self._item_iterator):
                self._items = list(map(self._item_wrapper, self._item_iterator))

    @property
    def selected_item(self):
        if self.selected_index == -1:
            return
        return self.items[self.selected_index]

    @listenable_property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, value):
        if value != self._selected_index:
            num_children = len(self._items)
            if value < -1 or value >= num_children:
                raise IndexError('Index %i must be in [-1..%i]' % (value, num_children - 1))
            self._selected_index = value
            self.notify_selected_index()
            if self._selected_index >= self.LAZY_ACCESS_THRESHOLD:
                if not self._access_all:
                    self.access_all = True

    def select_index_with_offset(self, offset):
        self.selected_index = clamp(self._selected_index + offset, 0, len(self._items) - 1)