# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/elements/velocity_levels_element.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 857 bytes
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