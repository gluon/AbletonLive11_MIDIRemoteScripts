# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\active_parameter.py
# Compiled at: 2023-08-04 12:30:20
# Size of source mod 2**32: 4168 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ...base import find_if, listenable_property, listens_group, task
from ...live import liveobj_valid
from .. import ACTIVE_PARAMETER_TIMEOUT, Component
from ..controls import TouchControl, control_matrix
from ..display import Renderable

class ActiveParameterComponent(Component, Renderable):
    touch_controls = control_matrix(TouchControl)

    def __init__(self, timeout=ACTIVE_PARAMETER_TIMEOUT, *a, **k):
        (super().__init__)(a, name='Active_Parameter', **k)
        self._pressed_touch_elements = {}
        self._release_tasks = {}
        self._timeout = timeout

    @listenable_property
    def parameter(self):
        return find_if(liveobj_valid, (elem.controlled_parameter for elem in reversed(list(self._pressed_touch_elements.values()))))

    @touch_controls.pressed
    def touch_controls(self, button):
        self._pressed_touch_elements[button.index] = button.control_element
        self._cancel_release_task(button.index)
        self._on_pressed_touch_elements_changed()

    @touch_controls.released
    def touch_controls(self, button):
        if any((t.is_pressed for t in self.touch_controls)):
            self._on_touch_control_release(button.index)
        else:
            self._release_tasks[button.index] = self._tasks.add(task.sequence(task.wait(self._timeout), task.run(partial(self._on_touch_control_release, button.index))))

    def _on_touch_control_release(self, index):
        self._clear_release_task(index)
        del self._pressed_touch_elements[index]
        self._on_pressed_touch_elements_changed()

    def _cancel_release_task(self, index):
        if index in self._release_tasks:
            self._release_tasks[index].kill()
            self._clear_release_task(index)

    def _on_pressed_touch_elements_changed(self):
        self._ActiveParameterComponent__on_touch_control_parameter_changed.replace_subjects(self._pressed_touch_elements.values())
        self._ActiveParameterComponent__on_touch_control_parameter_assignment_changed.replace_subjects(self._pressed_touch_elements.values())
        self.notify_parameter()

    def _clear_release_task(self, index):
        if index in self._release_tasks:
            self._tasks.remove(self._release_tasks[index])
            del self._release_tasks[index]

    @listens_group('controlled_parameter')
    def __on_touch_control_parameter_changed(self, _):
        self.notify_parameter()

    @listens_group('assignment')
    def __on_touch_control_parameter_assignment_changed(self, element):
        if not element.is_pressed:
            for index, pressed_element in self._pressed_touch_elements.items():
                if element == pressed_element:
                    if index in self._release_tasks:
                        self._cancel_release_task(index)
                        self._on_touch_control_release(index)
                    break