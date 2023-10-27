# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\control\encoder.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 13899 bytes
from __future__ import absolute_import, print_function, unicode_literals
import logging
from ...base import clamp, const, lazy_attribute, old_hasattr, sign, task
from .control import Connectable, InputControl, SendValueMixin, control_event
logger = logging.getLogger(__name__)
__all__ = ('EncoderControl', 'StepEncoderControl', 'ListValueEncoderControl', 'ListIndexEncoderControl',
           'ValueStepper')

class EncoderControl(InputControl):
    TOUCH_TIME = 0.5
    touched = control_event('touched')
    released = control_event('released')

    class State(InputControl.State, Connectable):

        def __init__(self, control=None, manager=None, touch_event_delay=0, *a, **k):
            (super(EncoderControl.State, self).__init__)(a, control=control, manager=manager, **k)
            self._is_touched = False
            self._touch_value_slot = None
            self._timer_based = False
            self._touch_event_delay = touch_event_delay
            self._touch_value_slot = self.register_slot(None, self._on_touch_value, 'value')

        @property
        def is_touched(self):
            return self._is_touched

        def set_control_element(self, control_element):
            if self._control_element != control_element or self._lost_touch_element(self._control_element):
                self._release_encoder()
                self._kill_all_tasks()
            super(EncoderControl.State, self).set_control_element(control_element)
            self._touch_value_slot.subject = self._get_touch_element(control_element) if control_element is not None else None
            if control_element:
                if old_hasattr(control_element, 'is_pressed'):
                    if control_element.is_pressed():
                        self._touch_encoder()

        def _get_touch_element(self, control_element):
            return getattr(control_element, 'touch_element', None)

        def _lost_touch_element(self, control_element):
            return control_element is not None and self._get_touch_element(control_element) is None

        def _touch_encoder(self):
            is_touched = self._is_touched
            self._is_touched = True
            if not is_touched:
                self._call_listener('touched')

        def _release_encoder(self):
            is_touched = self._is_touched
            self._is_touched = False
            if is_touched:
                self._call_listener('released')

        def _event_listener_required(self):
            return True

        def _notify_encoder_value(self, value, *a, **k):
            normalized_value = self._control_element.normalize_value(value)
            self._call_listener('value', normalized_value)
            self.connected_property_value = normalized_value

        def _on_value(self, value, *a, **k):
            if self._notifications_enabled():
                if not self._is_touched:
                    self._touch_encoder()
                    if self._delayed_touch_task.is_running:
                        self._delayed_touch_task.kill()
                    else:
                        self._timer_based = True
                        self._timer_based_release_task.restart()
                else:
                    if self._timer_based:
                        self._timer_based_release_task.restart()
                if self._control_element:
                    (self._notify_encoder_value)(value, *a, **k)

        def _on_touch_value(self, value, *a, **k):
            if self._notifications_enabled():
                if value:
                    if self._touch_event_delay > 0:
                        self._delayed_touch_task.restart()
                    else:
                        self._touch_encoder()
                else:
                    self._release_encoder()
                    self._delayed_touch_task.kill()
                self._cancel_timer_based_events()

        @lazy_attribute
        def _timer_based_release_task(self):
            return self.tasks.add(task.sequence(task.wait(EncoderControl.TOUCH_TIME), task.run(self._release_encoder)))

        @lazy_attribute
        def _delayed_touch_task(self):
            return self.tasks.add(task.sequence(task.wait(self._touch_event_delay), task.run(self._touch_encoder)))

        def _cancel_timer_based_events(self):
            if self._timer_based:
                self._timer_based_release_task.kill()
                self._timer_based = False

        def _kill_all_tasks(self):
            self._timer_based_release_task.kill()
            self._delayed_touch_task.kill()

    def __init__(self, *a, **k):
        super(EncoderControl, self).__init__(extra_args=a, extra_kws=k)


class ValueStepper(object):

    def __init__(self, num_steps=10, *a, **k):
        (super(ValueStepper, self).__init__)(*a, **k)
        self._step = 0.0
        self._num_steps = float(num_steps)

    @property
    def num_steps(self):
        return self._num_steps

    def advance(self, value):
        result = 0
        if sign(value) != sign(self._step):
            self.reset()
        new_value = self._step + value * self._num_steps
        if int(new_value) != int(self._step):
            result = int(new_value)
            self.reset()
        else:
            self._step = new_value
        return result

    def reset(self):
        self._step = 0.0


class StepEncoderControl(EncoderControl):

    class State(EncoderControl.State):

        def __init__(self, num_steps=10, *a, **k):
            (super(StepEncoderControl.State, self).__init__)(*a, **k)
            self._stepper = ValueStepper(num_steps=num_steps)

        def _notify_encoder_value(self, value, *a, **k):
            steps = self._stepper.advance(self._control_element.normalize_value(value))
            if steps != 0:
                self._call_listener('value', steps)
                self._on_stepped(steps)

        def _on_stepped(self, steps):
            self.connected_property_value = steps

        def _on_touch_value(self, value, *a, **k):
            (super(StepEncoderControl.State, self)._on_touch_value)(value, *a, **k)
            if not value:
                self._stepper.reset()

        @property
        def num_steps(self):
            return self._stepper._num_steps


class ListValueEncoderControl(StepEncoderControl):

    class State(StepEncoderControl.State):

        def __init__(self, *a, **k):
            (super(ListValueEncoderControl.State, self).__init__)(*a, **k)
            self._list_values_getter = None

        def connect_list_property(self, subject, list_property_name=None, current_value_property_name=None):
            self.connect_property(subject, current_value_property_name)
            self._list_values_getter = lambda: getattr(subject, list_property_name)

        def connect_static_list(self, subject, current_value_property_name=None, list_values=None):
            self.connect_property(subject, current_value_property_name)
            self._list_values_getter = const(list_values)

        def disconnect_property(self):
            super(ListValueEncoderControl.State, self).disconnect_property()
            self._list_values_getter = None

        def _on_stepped(self, steps):
            if self._list_values_getter is not None:
                list_values = self._list_values_getter()
                try:
                    current_index = list_values.index(self.connected_property_value)
                except ValueError:
                    logger.warning('Encoder was turned, but current value is not in list!')
                    current_index = 0

                new_index = clamp(current_index + steps, 0, len(list_values) - 1)
                self.connected_property_value = list_values[new_index]


class ListIndexEncoderControl(StepEncoderControl):

    class State(StepEncoderControl.State):

        def __init__(self, *a, **k):
            (super(ListIndexEncoderControl.State, self).__init__)(*a, **k)
            self._max_index = None

        def connect_list_property(self, subject, current_index_property_name=None, max_index=None):
            self.connect_property(subject, current_index_property_name)
            self._max_index = max_index

        def disconnect_property(self):
            super(ListIndexEncoderControl.State, self).disconnect_property()
            self._max_index = None

        def _on_stepped(self, steps):
            if self._max_index is not None:
                new_index = clamp(self.connected_property_value + steps, 0, self._max_index)
                self.connected_property_value = new_index


class SendValueEncoderControl(EncoderControl):

    class State(SendValueMixin, EncoderControl.State):
        pass