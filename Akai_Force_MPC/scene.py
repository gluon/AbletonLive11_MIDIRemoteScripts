# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\scene.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 3311 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface.components import SceneComponent as SceneComponentBase
from ableton.v2.control_surface.control import ButtonControl, SendValueControl, TextDisplayControl
from .clip_slot import ClipSlotComponent
from .skin import LIVE_COLOR_TABLE_INDEX_OFFSET

class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent
    scene_name_display = TextDisplayControl(segments=('', ))
    scene_color_control = ButtonControl()
    scene_selection_control = SendValueControl()
    force_launch_button = ButtonControl(color='Session.SceneOff',
      pressed_color='Session.SceneOn')
    _default_scene_color = 'DefaultButton.Off'

    def __init__(self, *a, **k):
        (super(SceneComponent, self).__init__)(*a, **k)

    @force_launch_button.pressed
    def force_launch_button(self, value):
        self._on_launch_button_pressed()

    @force_launch_button.released
    def force_launch_button(self, value):
        self._on_launch_button_released()

    def set_scene(self, scene):
        super(SceneComponent, self).set_scene(scene)
        self._SceneComponent__on_scene_name_changed.subject = self._scene
        self._SceneComponent__on_scene_name_changed()
        self._SceneComponent__on_scene_color_changed.subject = self._scene
        self._SceneComponent__on_scene_color_changed()
        self._SceneComponent__on_selected_scene_changed.subject = self.song.view
        self._SceneComponent__on_selected_scene_changed()

    @listens('name')
    def __on_scene_name_changed(self):
        self._update_scene_name_display()

    @listens('color_index')
    def __on_scene_color_changed(self):
        self._update_scene_color_control()

    @listens('selected_scene')
    def __on_selected_scene_changed(self):
        self.scene_selection_control.value = int(self.song.view.selected_scene == self._scene)

    def _update_scene_color_control(self):
        color = 'DefaultButton.Off'
        scene = self._scene
        if liveobj_valid(scene):
            color = scene.color_index + LIVE_COLOR_TABLE_INDEX_OFFSET if scene.color_index != None else self._default_scene_color
        self.scene_color_control.color = color

    def _update_scene_name_display(self):
        scene = self._scene
        self.scene_name_display[0] = scene.name if liveobj_valid(scene) else ''

    def _update_launch_button(self):
        value_to_send = self._no_scene_color
        if liveobj_valid(self._scene):
            value_to_send = self._scene_color
            if self._scene.is_triggered:
                value_to_send = self._triggered_color
        self.launch_button.color = value_to_send


class MPCSceneComponent(SceneComponent):
    _default_scene_color = 'Session.SceneDefault'

    def __init__(self, *a, **k):
        (super(MPCSceneComponent, self).__init__)(*a, **k)
        self._triggered_color = 'Session.ClipTriggeredPlay'
        self._scene_color = 'Session.ClipStopped'
        self._no_scene_color = 'Session.ClipEmpty'