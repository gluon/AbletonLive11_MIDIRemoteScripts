# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\filterdelay.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 1426 bytes
from __future__ import absolute_import, print_function, unicode_literals
from enum import IntEnum
from ableton.v2.base import EventObject, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator

class FilterDelayDeviceDecorator(LiveObjectDecorator, EventObject):

    class ChanSelect(IntEnum):
        l = 0
        lr = 1
        r = 2
        dry = 3

    def __init__(self, *a, **k):
        (super(FilterDelayDeviceDecorator, self).__init__)(*a, **k)
        self._add_enum_parameter(name='Chan Select',
          values=[
         'L', 'L+R', 'R', 'Dry'],
          default_value=(self.ChanSelect.l))
        self._add_on_off_option(name='L Sync', pname='1 Delay Mode')
        self._add_on_off_option(name='L+R Sync', pname='2 Delay Mode')
        self._add_on_off_option(name='R Sync', pname='3 Delay Mode')
        self._add_on_off_option(name='L Channel', pname='1 Input On')
        self._add_on_off_option(name='L+R Channel', pname='2 Input On')
        self._add_on_off_option(name='R Channel', pname='3 Input On')
        self._add_on_off_option(name='L Filter', pname='1 Filter On')
        self._add_on_off_option(name='L+R Filter', pname='2 Filter On')
        self._add_on_off_option(name='R Filter', pname='3 Filter On')
        self.register_disconnectables(self.options)