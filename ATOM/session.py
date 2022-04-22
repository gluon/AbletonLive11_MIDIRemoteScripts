# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/session.py
# Compiled at: 2021-11-23 12:54:43
# Size of source mod 2**32: 1043 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
import ableton.v2.control_surface.components as ClipSlotComponentBase
import ableton.v2.control_surface.components as SceneComponentBase
import ableton.v2.control_surface.components as SessionComponentBase
from .colors import LIVE_COLOR_INDEX_TO_RGB

class ClipSlotComponent(ClipSlotComponentBase):

    def _color_value(self, slot_or_clip):
        return LIVE_COLOR_INDEX_TO_RGB.get(slot_or_clip.color_index, 0)


class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent

    def _color_value(self, color):
        if liveobj_valid(self._scene):
            return LIVE_COLOR_INDEX_TO_RGB.get(self._scene.color_index, 0)
        return 0


class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent