<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from KeyLab_Essential.session import SceneComponent as SceneComponentBase
from KeyLab_Essential.session import SessionComponent as SessionComponentBase
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/KeyLab_mkII/session.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 514 bytes
from __future__ import absolute_import, print_function, unicode_literals
import KeyLab_Essential.session as SceneComponentBase
import KeyLab_Essential.session as SessionComponentBase
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from .clip_slot import ClipSlotComponent

class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent


class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent