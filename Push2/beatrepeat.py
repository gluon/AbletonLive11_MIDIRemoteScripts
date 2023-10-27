# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\beatrepeat.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 840 bytes
from __future__ import absolute_import, print_function, unicode_literals
from enum import IntEnum
from ableton.v2.base import EventObject, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator

class BeatRepeatDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        (super(BeatRepeatDeviceDecorator, self).__init__)(*a, **k)
        self._add_switch_option(name='Mix Type',
          pname='Mix Type',
          labels=['Mix', 'Ins', 'Gate'])
        self._add_on_off_option(name='Repeat', pname='Repeat')
        self._add_on_off_option(name='Filter', pname='Filter On')
        self._add_on_off_option(name='Triplets', pname='Block Triplets')
        self.register_disconnectables(self.options)