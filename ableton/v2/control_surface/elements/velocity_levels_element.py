# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\velocity_levels_element.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 892 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ...base import EventObject, listenable_property
from .proxy_element import ProxyElement

class NullVelocityLevels(EventObject):
    enabled = False
    target_note = -1
    target_channel = -1
    source_channel = -1
    notes = []

    @property
    def levels(self):
        return []

    @listenable_property
    def last_played_level(self):
        return -1.0


class VelocityLevelsElement(ProxyElement):

    def __init__(self, velocity_levels=None, *a, **k):
        super(VelocityLevelsElement, self).__init__(proxied_object=velocity_levels,
          proxied_interface=(NullVelocityLevels()))

    def reset(self):
        self.notes = []
        self.source_channel = -1