# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\blinking_button.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 2164 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import lazy_attribute, task
from ableton.v2.control_surface.control import ButtonControl as ButtonControlBase
from ableton.v2.control_surface.control import control_color
DEFAULT_BLINK_PERIOD = 0.1

class BlinkingButtonControl(ButtonControlBase):

    class State(ButtonControlBase.State):
        blink_on_color = control_color('DefaultButton.On')
        blink_off_color = control_color('DefaultButton.Off')

        def __init__(self, blink_on_color='DefaultButton.On', blink_off_color='DefaultButton.Off', blink_period=DEFAULT_BLINK_PERIOD, *a, **k):
            (super(BlinkingButtonControl.State, self).__init__)(*a, **k)
            self.blink_on_color = blink_on_color
            self.blink_off_color = blink_off_color
            self._blink_period = blink_period

        def start_blinking(self):
            self._blink_task.restart()

        def stop_blinking(self):
            self._blink_task.kill()

        @lazy_attribute
        def _blink_task(self):
            blink_on = partial(self._set_blinking_color, self.blink_on_color)
            blink_off = partial(self._set_blinking_color, self.blink_off_color)
            return self.tasks.add(task.sequence(task.run(blink_on), task.wait(self._blink_period), task.run(blink_off), task.wait(self._blink_period), task.run(blink_on), task.wait(self._blink_period), task.run(blink_off)))

        def _set_blinking_color(self, color):
            if self._control_element:
                self._control_element.set_light(color)

        def _kill_all_tasks(self):
            super(BlinkingButtonControl.State, self)._kill_all_tasks()
            self._blink_task.kill()