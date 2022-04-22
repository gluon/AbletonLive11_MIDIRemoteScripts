# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/ScrollComponent.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 4551 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from . import Defaults, Task
from .Control import ButtonControl
from .ControlSurfaceComponent import ControlSurfaceComponent

class Scrollable(object):

    def can_scroll_up(self):
        return False

    def can_scroll_down(self):
        return False

    def scroll_up(self):
        pass

    def scroll_down(self):
        pass


class ScrollComponent(ControlSurfaceComponent, Scrollable):
    is_private = True
    scrolling_delay = Defaults.MOMENTARY_DELAY
    scrolling_step_delay = 0.1
    default_scrollable = Scrollable()
    default_pager = Scrollable()
    _scrollable = default_scrollable
    default_scroll_skin = dict(color='Enabled',
      pressed_color='Pressed',
      disabled_color=False)
    scroll_up_button = ButtonControl(**default_scroll_skin)
    scroll_down_button = ButtonControl(**default_scroll_skin)

    def __init__(self, scrollable=None, *a, **k):
        (super(ScrollComponent, self).__init__)(*a, **k)
        self._scroll_task_up = self._make_scroll_task(self._do_scroll_up)
        self._scroll_task_down = self._make_scroll_task(self._do_scroll_down)
        if scrollable != None:
            self.scrollable = scrollable

    def _make_scroll_task(self, scroll_step):
        task = self._tasks.add(Task.sequence(Task.wait(self.scrolling_delay), Task.loop(Task.wait(self.scrolling_step_delay), Task.run(scroll_step))))
        task.kill()
        return task

    def _get_scrollable(self):
        return self._scrollable

    def _set_scrollable(self, scrollable):
        self._scrollable = scrollable
        self._update_scroll_buttons()

    scrollable = property(_get_scrollable, _set_scrollable)

    def can_scroll_up(self):
        return self._scrollable.can_scroll_up()

    def can_scroll_down(self):
        return self._scrollable.can_scroll_down()

    def scroll_up(self):
        return self._scrollable.scroll_up()

    def scroll_down(self):
        return self._scrollable.scroll_down()

    def set_scroll_up_button(self, button):
        self.scroll_up_button.set_control_element(button)
        self._update_scroll_buttons()

    def set_scroll_down_button(self, button):
        self.scroll_down_button.set_control_element(button)
        self._update_scroll_buttons()

    def _update_scroll_buttons(self):
        self.scroll_up_button.enabled = self.can_scroll_up()
        self.scroll_down_button.enabled = self.can_scroll_down()

    @scroll_up_button.pressed
    def scroll_up_button(self, button):
        self._on_scroll_pressed(button, self._do_scroll_up, self._scroll_task_up)

    @scroll_up_button.released
    def scroll_up_button(self, button):
        self._on_scroll_released(self._scroll_task_up)

    @scroll_down_button.pressed
    def scroll_down_button(self, button):
        self._on_scroll_pressed(button, self._do_scroll_down, self._scroll_task_down)

    @scroll_down_button.released
    def scroll_down_button(self, button):
        self._on_scroll_released(self._scroll_task_down)

    def _do_scroll_up(self):
        self.scroll_up()
        self._update_scroll_buttons()

    def _do_scroll_down(self):
        self.scroll_down()
        self._update_scroll_buttons()

    def update(self):
        super(ScrollComponent, self).update()
        self._update_scroll_buttons()

    def _on_scroll_pressed(self, button, scroll_step, scroll_task):
        is_scrolling = not self._scroll_task_up.is_killed or not self._scroll_task_down.is_killed
        if not is_scrolling:
            scroll_step()
        if button.enabled:
            scroll_task.restart()
        self._ensure_scroll_one_direction()

    def _on_scroll_released(self, scroll_task):
        scroll_task.kill()
        self._ensure_scroll_one_direction()

    def _ensure_scroll_one_direction(self):
        if self.scroll_up_button.is_pressed and self.scroll_down_button.is_pressed:
            self._scroll_task_up.pause()
            self._scroll_task_down.pause()
        else:
            self._scroll_task_up.resume()
            self._scroll_task_down.resume()