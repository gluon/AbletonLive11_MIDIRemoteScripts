from __future__ import absolute_import, print_function, unicode_literals
from KeyLab_Essential.session import SceneComponent as SceneComponentBase
from KeyLab_Essential.session import SessionComponent as SessionComponentBase
from .clip_slot import ClipSlotComponent

class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent


class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent