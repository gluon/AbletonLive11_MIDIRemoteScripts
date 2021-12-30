#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/control/button.py
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ...base import lazy_attribute, task
from ..defaults import MOMENTARY_DELAY, DOUBLE_CLICK_DELAY
from ..input_control_element import ScriptForwarding
from .control import InputControl, control_event, control_color
__all__ = (u'ButtonControl',
 u'PlayableControl',
 u'ButtonControlBase',
 u'DoubleClickContext')

class DoubleClickContext(object):
    u"""
    Injectable context to use in conjunction with ButtonControls that ensures other clicks
    in the same scope will cancel a double click event if occurring between clicks of a
    double click.
    """
    control_state = None
    click_count = 0

    def set_new_context(self, control_state):
        self.control_state = control_state
        self.click_count = 0


class ButtonControlBase(InputControl):
    u"""
    Base class for Button-like Controls. The class has a set of common events when
    interacting with buttons. It is expected to connect with a
    :class:`ableton.v2.control_surface.elements.button.ButtonElement`.
    
    As a base class, no default color is defined, as different Button types define
    different states. Use :class:`ButtonControl` for the simplest implementation of
    a button.
    """
    DELAY_TIME = MOMENTARY_DELAY
    DOUBLE_CLICK_TIME = DOUBLE_CLICK_DELAY
    REPEAT_RATE = 0.1
    pressed = control_event(u'pressed')
    released = control_event(u'released')
    pressed_delayed = control_event(u'pressed_delayed')
    released_delayed = control_event(u'released_delayed')
    released_immediately = control_event(u'released_immediately')
    double_clicked = control_event(u'double_clicked')

    class State(InputControl.State):
        u"""
        State-full representation of the Control.
        """
        disabled_color = control_color(u'DefaultButton.Disabled')
        pressed_color = control_color(None)

        def __init__(self, pressed_color = None, disabled_color = None, repeat = False, enabled = True, double_click_context = None, delay_time = None, *a, **k):
            super(ButtonControlBase.State, self).__init__(*a, **k)
            if disabled_color is not None:
                self.disabled_color = disabled_color
            self.pressed_color = pressed_color
            self._repeat = repeat
            self._is_pressed = False
            self._enabled = enabled
            self._double_click_context = double_click_context or DoubleClickContext()
            self._delay_time = delay_time if delay_time is not None else ButtonControlBase.DELAY_TIME

        @property
        def enabled(self):
            u"""
            Enables/disables a button. A disabled button is indicated using the
            :attr:`disabled_color` and will not react to any input. No event is triggered
            while it's disabled. If a button is disabled while it's pressed, the button
            is released first.
            """
            return self._enabled

        @enabled.setter
        def enabled(self, enabled):
            if self._enabled != enabled:
                if not enabled:
                    self._release_button()
                self._enabled = enabled
                self._send_current_color()

        @property
        def is_momentary(self):
            u"""
            True if the Control is connected to a Button Element and it's a momentary
            button.
            """
            return self._control_element and self._control_element.is_momentary()

        @property
        def is_pressed(self):
            u"""
            True while the Control is pressed. The state might be different than the
            connected Button Element's `is_pressed` state.
            """
            return self._is_pressed

        def _event_listener_required(self):
            return True

        def set_control_element(self, control_element):
            u"""
            Connects a :class:`~ableton.v2.control_surface.elements.button.ButtonElement`
            with the Control. If a Button Element is already connected and it's
            currently pressed, the :attr:`released` event will be triggered.
            """
            if self._control_element != control_element:
                self._release_button()
                self._kill_all_tasks()
            super(ButtonControlBase.State, self).set_control_element(control_element)
            self._send_current_color()

        def _send_current_color(self):
            if self._control_element:
                if not self._enabled:
                    self._control_element.set_light(self.disabled_color)
                elif self.pressed_color is not None and self.is_pressed:
                    self._control_element.set_light(self.pressed_color)
                else:
                    self._send_button_color()

        def _send_button_color(self):
            raise NotImplementedError

        def _on_value(self, value, *a, **k):
            if self._notifications_enabled():
                if not self.is_momentary:
                    self._press_button()
                    self._release_button()
                elif value:
                    self._press_button()
                else:
                    self._release_button()
                super(ButtonControlBase.State, self)._on_value(value, *a, **k)
            self._send_current_color()

        def _press_button(self):
            is_pressed = self._is_pressed
            self._is_pressed = True
            if self._notifications_enabled() and not is_pressed:
                self._on_pressed()

        def _on_pressed(self):
            if self._repeat:
                self._repeat_task.restart()
            self._call_listener(u'pressed')
            if self._has_delayed_event():
                self._delay_task.restart()
            self._check_double_click_press()

        def _release_button(self):
            is_pressed = self._is_pressed
            self._is_pressed = False
            if self._notifications_enabled() and is_pressed:
                self._on_released()

        def _on_released(self):
            self._call_listener(u'released')
            if self._repeat:
                self._repeat_task.kill()
            if self._has_delayed_event():
                if self._delay_task.is_running:
                    self._call_listener(u'released_immediately')
                    self._delay_task.kill()
                else:
                    self._call_listener(u'released_delayed')
            self._check_double_click_release()

        def _check_double_click_press(self):
            if self._has_listener(u'double_clicked') and not self._double_click_task.is_running:
                self._double_click_task.restart()
                self._double_click_context.click_count = 0
            if self._double_click_context.control_state != self:
                self._double_click_context.set_new_context(self)

        def _check_double_click_release(self):
            if self._has_listener(u'double_clicked') and self._double_click_task.is_running and self._double_click_context.control_state == self:
                self._double_click_context.click_count += 1
                if self._double_click_context.click_count == 2:
                    self._call_listener(u'double_clicked')
                    self._double_click_task.kill()

        def set_double_click_context(self, context):
            self._double_click_context = context

        @lazy_attribute
        def _delay_task(self):
            return self.tasks.add(task.sequence(task.wait(self._delay_time), task.run(self._on_pressed_delayed)))

        @lazy_attribute
        def _repeat_task(self):
            notify_pressed = partial(self._call_listener, u'pressed')
            return self.tasks.add(task.sequence(task.wait(self._delay_time), task.loop(task.wait(ButtonControlBase.REPEAT_RATE), task.run(notify_pressed))))

        def _kill_all_tasks(self):
            if self._repeat:
                self._repeat_task.kill()
            if self._has_delayed_event():
                self._delay_task.kill()

        @lazy_attribute
        def _double_click_task(self):
            return self.tasks.add(task.wait(ButtonControlBase.DOUBLE_CLICK_TIME))

        def _has_delayed_event(self):
            return self._has_listener(u'pressed_delayed') or self._has_listener(u'released_delayed') or self._has_listener(u'released_immediately')

        def _on_pressed_delayed(self):
            if self._is_pressed:
                self._call_listener(u'pressed_delayed')

        def update(self):
            self._send_current_color()

    def __init__(self, *a, **k):
        super(ButtonControlBase, self).__init__(extra_args=a, extra_kws=k)


class ButtonControl(ButtonControlBase):
    u"""
    A Control representing a simple button.
    
    The class is extending :class:`ButtonControlBase` by adding a default :attr:`color`
    to the button.
    """

    class State(ButtonControlBase.State):
        u"""
        State-full representation of the Control.
        """
        color = control_color(u'DefaultButton.On')

        def __init__(self, color = None, *a, **k):
            super(ButtonControl.State, self).__init__(*a, **k)
            if color is not None:
                self.color = color

        def _send_button_color(self):
            self._control_element.set_light(self.color)


class PlayableControl(ButtonControl):
    u"""
    Button that will make the element's MIDI go into Live, to make it playable. If
    :meth:`set_mode` is set to `PlayableControl.Mode.listenable`, the Control with behave
    like a :class:`ButtonControl`.
    """

    class Mode(int):
        u"""
        Represents the possible modes the playable control can be in.
        """
        pass

    Mode.playable = Mode(0)
    Mode.listenable = Mode(1)
    Mode.playable_and_listenable = Mode(2)

    class State(ButtonControl.State):
        u"""
        State-full representation of the Control.
        """

        def __init__(self, mode = None, *a, **k):
            super(PlayableControl.State, self).__init__(*a, **k)
            self._enabled = True
            self._mode = PlayableControl.Mode.playable if mode is None else mode
            self._mode_to_forwarding = {PlayableControl.Mode.playable: ScriptForwarding.none,
             PlayableControl.Mode.listenable: ScriptForwarding.exclusive,
             PlayableControl.Mode.playable_and_listenable: ScriptForwarding.non_consuming}

        def set_control_element(self, control_element):
            u"""
            Makes the Control Element send MIDI to Live, so it can be played.
            """
            super(PlayableControl.State, self).set_control_element(control_element)
            self._update_script_forwarding()

        def _update_script_forwarding(self):
            if self._control_element and self._enabled:
                self._control_element.script_forwarding = self._mode_to_forwarding[self._mode]

        @property
        def enabled(self):
            u"""
            Defines if the Control is enabled and playable.
            """
            return self._enabled

        @enabled.setter
        def enabled(self, enabled):
            super(PlayableControl.State, PlayableControl.State).enabled.fset(self, enabled)
            if not enabled and self._control_element:
                self._control_element.reset_state()
                self._send_current_color()
            else:
                self.set_control_element(self._control_element)

        def set_mode(self, value):
            u"""
            Set the Control's playability in Live. See :class:`PlayableControl.Mode`
            for possible modes.
            """
            assert isinstance(value, PlayableControl.Mode)
            self._mode = value
            self._update_script_forwarding()

        def _is_listenable(self):
            return self._mode != PlayableControl.Mode.playable

        def _notifications_enabled(self):
            return super(PlayableControl.State, self)._notifications_enabled() and self._is_listenable()
