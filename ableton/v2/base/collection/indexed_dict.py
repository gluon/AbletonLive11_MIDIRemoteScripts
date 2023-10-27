# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\collection\indexed_dict.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1614 bytes
from __future__ import absolute_import, print_function, unicode_literals
from collections import OrderedDict

class IndexedDict(OrderedDict):

    def __init__(self, *args, **kwds):
        self._IndexedDict__keys = []
        (super(IndexedDict, self).__init__)(*args, **kwds)

    def __setitem__(self, key, value, *args, **kwds):
        (super(IndexedDict, self).__setitem__)(key, value, *args, **kwds)
        if key not in self._IndexedDict__keys:
            self._IndexedDict__keys.append(key)

    def __delitem__(self, key, *args, **kwds):
        (super(IndexedDict, self).__delitem__)(key, *args, **kwds)
        self._IndexedDict__keys.remove(key)

    def clear(self):
        super(IndexedDict, self).clear()
        self._IndexedDict__keys = []

    def popitem(self, last=True):
        item = super(IndexedDict, self).popitem(last)
        self._IndexedDict__keys.pop(-1 if last else 0)
        return item

    def keys(self):
        return self._IndexedDict__keys

    def item_by_index(self, ix):
        key = self._IndexedDict__keys[ix]
        return (
         key, self[key])

    def key_by_index(self, ix):
        return self._IndexedDict__keys[ix]

    def value_by_index(self, ix):
        return self[self._IndexedDict__keys[ix]]

    def index_by_key(self, key):
        return self._IndexedDict__keys.index(key)