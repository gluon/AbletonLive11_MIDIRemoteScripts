# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/ControlSurfaceComponent.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 6090 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from . import Task
from .Control import ControlManager
from .Dependency import dependency, depends
from .SubjectSlot import Subject
from .Util import lazy_attribute

class ControlSurfaceComponent(ControlManager, Subject):
    name = ''
    canonical_parent = None
    is_private = False
    _show_msg_callback = dependency(show_message=None)
    _has_task_group = False
    _layer = None

    @depends(register_component=None, song=None)
    def __init__(self, name='', register_component=None, song=None, layer=None, is_enabled=True, is_root=False, *a, **k):
        (super(ControlSurfaceComponent, self).__init__)(*a, **k)
        self.name = name
        self._explicit_is_enabled = is_enabled
        self._recursive_is_enabled = True
        self._is_enabled = self._explicit_is_enabled
        self._is_root = is_root
        self._allow_updates = True
        self._update_requests = 0
        self._song = song
        if layer is not None:
            self._layer = layer
        register_component(self)

    def disconnect(self):
        if self._has_task_group:
            self._tasks.kill()
            self._tasks.clear()
        super(ControlSurfaceComponent, self).disconnect()

    @property
    def is_root(self):
        return self._is_root

    def _internal_on_enabled_changed(self):
        if self._layer:
            if self.is_enabled():
                grabbed = self._layer.grab(self)
            else:
                self._layer.release(self)
        if self._has_task_group:
            if self.is_enabled():
                self._tasks.resume()
            else:
                self._tasks.pause()

    def on_enabled_changed(self):
        self.update()

    def update_all(self):
        self.update()

    def set_enabled(self, enable):
        self._explicit_is_enabled = bool(enable)
        self._update_is_enabled()

    def _set_enabled_recursive(self, enable):
        self._recursive_is_enabled = bool(enable)
        self._update_is_enabled()

    def _update_is_enabled(self):
        is_enabled = self._recursive_is_enabled and self._explicit_is_enabled
        if is_enabled != self._is_enabled:
            self._is_enabled = is_enabled
            self._internal_on_enabled_changed()
            self.on_enabled_changed()

    def set_allow_update(self, allow_updates):
        allow = bool(allow_updates)
        if self._allow_updates != allow:
            self._allow_updates = allow
            if self._allow_updates:
                if self._update_requests > 0:
                    self._update_requests = 0
                    self.update()

    def control_notifications_enabled(self):
        return self.is_enabled()

    def application(self):
        return Live.Application.get_application()

    def song(self):
        return self._song

    @lazy_attribute
    @depends(parent_task_group=None)
    def _tasks(self, parent_task_group=None):
        tasks = parent_task_group.add(Task.TaskGroup())
        if not self._is_enabled:
            tasks.pause()
        self._has_task_group = True
        return tasks

    def _get_layer(self):
        return self._layer

    def _set_layer(self, new_layer):
        if self._layer != new_layer:
            if self._layer:
                self._layer.release(self)
            self._layer = new_layer
            if new_layer:
                if self.is_enabled():
                    grabbed = new_layer.grab(self)

    layer = property(_get_layer, _set_layer)

    def is_enabled(self, explicit=False):
        if not explicit:
            return self._is_enabled
        return self._explicit_is_enabled

    def on_track_list_changed(self):
        pass

    def on_scene_list_changed(self):
        pass

    def on_selected_track_changed(self):
        pass

    def on_selected_scene_changed(self):
        pass

    @depends(parent_task_group=None)
    def _register_timer_callback(self, callback, parent_task_group=None):

        def wrapper(delta):
            callback()
            return Task.RUNNING

        parent_task_group.add(Task.FuncTask(wrapper, callback))

    @depends(parent_task_group=None)
    def _unregister_timer_callback(self, callback, parent_task_group=None):
        task = parent_task_group.find(callback)
        parent_task_group.remove(task)