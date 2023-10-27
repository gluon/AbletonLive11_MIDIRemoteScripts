# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\lockable_button.py
# Compiled at: 2023-08-04 12:30:20
# Size of source mod 2**32: 2689 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ...base import EventObject, listenable_property, task
from .. import DOUBLE_CLICK_DELAY
from ..display import Renderable
from . import ButtonElement

class LockableButtonElementMixin(EventObject, Renderable):
    is_locked = listenable_property.managed(False)
    double_click_time = DOUBLE_CLICK_DELAY

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self._locked_color = 'DefaultButton.{}Locked'.format(self.name.title().replace('_', ''))
        self._double_click_count = 0
        self._double_click_task = self._tasks.add(task.wait(self.double_click_time))
        self._double_click_task.kill()

    def reset(self):
        self._set_is_locked(False, do_notify=False)
        super().reset()

    def receive_value(self, value):
        if value:
            self._on_press()
        else:
            self._on_release()
        super().receive_value(value)

    def _on_press(self):
        self._set_is_locked(False)
        if not self._double_click_task.is_running:
            self._double_click_task.restart()
            self._double_click_count = 0

    def _on_release(self):
        if self._double_click_task.is_running:
            self._double_click_count += 1
            if self._double_click_count == 2:
                self._set_is_locked(True)
                self._double_click_task.kill()

    def _set_is_locked(self, is_locked, do_notify=True):
        if self.is_locked != is_locked:
            self.is_locked = is_locked
            if do_notify:
                self.notify(self.notifications.Element.button_lock, self.name, is_locked)

    def _set_skin_light(self, value):
        if self.is_locked:
            value = self._locked_color
        super()._set_skin_light(value)


class LockableButtonElement(LockableButtonElementMixin, ButtonElement):
    pass