# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\notification.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 1149 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import control_list
from .control import DisplayControl
CLEAR_DELAY = 5

class NotificationComponent(Component):
    display_lines = control_list(DisplayControl, control_count=2)

    def __init__(self, *a, **k):
        (super(NotificationComponent, self).__init__)(*a, **k)
        self._clear_notification_task = self._tasks.add(task.sequence(task.wait(CLEAR_DELAY), task.run(self._clear_notification)))
        self._clear_notification_task.kill()

    def show_notification(self, upper_line, lower_line):
        self._clear_notification_task.kill()
        self._clear_notification_task.restart()
        self.display_lines[0].message = upper_line
        self.display_lines[1].message = lower_line

    def _clear_notification(self):
        self.display_lines[0].message = ' '
        self.display_lines[1].message = ' '