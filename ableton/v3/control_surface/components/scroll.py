# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\scroll.py
# Compiled at: 2023-09-13 04:24:51
# Size of source mod 2**32: 5560 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ...base import task
from .. import MOMENTARY_DELAY, Component
from ..controls import ButtonControl, StepEncoderControl

class Scrollable:
    can_scroll_up = NotImplemented
    can_scroll_down = NotImplemented
    scroll_up = NotImplemented
    scroll_down = NotImplemented


class ScrollComponent(Component, Scrollable):
    scrolling_delay = MOMENTARY_DELAY
    scrolling_step_delay = 0.1
    scroll_encoder = StepEncoderControl(num_steps=64)
    scroll_up_button = ButtonControl()
    scroll_down_button = ButtonControl()

    def __init__(self, scrollable=None, scroll_skin_name=None, *a, **k):
        (super().__init__)(*a, **k)
        if scroll_skin_name:
            pressed_colored = '{}Pressed'.format(scroll_skin_name)
            self.scroll_up_button.color = scroll_skin_name
            self.scroll_down_button.color = scroll_skin_name
            self.scroll_up_button.pressed_color = pressed_colored
            self.scroll_down_button.pressed_color = pressed_colored
        self._scroll_task_up = self._make_scroll_task(self._do_scroll_up)
        self._scroll_task_down = self._make_scroll_task(self._do_scroll_down)
        self._scrollable = scrollable or self

    def _make_scroll_task(self, scroll_step):
        t = self._tasks.add(task.sequence(task.wait(self.scrolling_delay), task.loop(task.wait(self.scrolling_step_delay), task.run(scroll_step))))
        t.kill()
        return t

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

    def set_scroll_encoder(self, encoder):
        self.scroll_encoder.set_control_element(encoder)

    def _update_scroll_buttons(self):
        self.scroll_up_button.enabled = self.can_scroll_up()
        self.scroll_down_button.enabled = self.can_scroll_down()

    @scroll_up_button.pressed
    def scroll_up_button(self, button):
        self._on_scroll_pressed(button, self._do_scroll_up, self._scroll_task_up)

    @scroll_up_button.released
    def scroll_up_button(self, _):
        self._on_scroll_released(self._scroll_task_up)

    @scroll_down_button.pressed
    def scroll_down_button(self, button):
        self._on_scroll_pressed(button, self._do_scroll_down, self._scroll_task_down)

    @scroll_down_button.released
    def scroll_down_button(self, _):
        self._on_scroll_released(self._scroll_task_down)

    @scroll_encoder.value
    def scroll_encoder(self, value, _):
        if value < 0:
            if self.can_scroll_up():
                self.scroll_up()
        else:
            if self.can_scroll_down():
                self.scroll_down()

    def _do_scroll_up(self):
        self.scroll_up()
        self._update_scroll_buttons()

    def _do_scroll_down(self):
        self.scroll_down()
        self._update_scroll_buttons()

    def update(self):
        super().update()
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