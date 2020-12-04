#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/model/uniqueid.py
from __future__ import absolute_import, print_function, unicode_literals
from itertools import count

class UniqueIdMixin(object):
    _idgen = count()

    def __init__(self, *a, **k):
        super(UniqueIdMixin, self).__init__(*a, **k)
        self.__id__ = next(self._idgen)
