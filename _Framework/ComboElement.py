# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\ComboElement.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 15225 bytes
from __future__ import absolute_import, print_function, unicode_literals
from contextlib import contextmanager
from ableton.v2.base import PY3
from . import Defaults, Task
from .ButtonElement import ButtonElementMixin
from .CompoundElement import CompoundElement
from .Dependency import depends
from .InputControlElement import ParameterSlot
from .NotifyingControlElement import NotifyingControlElement
from .Proxy import ProxyBase
from .Resource import DEFAULT_PRIORITY
from .SubjectSlot import SlotManager, Subject, subject_slot
from .Util import const, find_if, lazy_attribute, nop

class WrapperElement(CompoundElement, ProxyBase):

    class ProxiedInterface(CompoundElement.ProxiedInterface):

        def __getattr__(self, name):
            if PY3:
                if '_wrapped_control' not in self.outer.__dict__:
                    raise AttributeError()
            wrapped = self.outer.__dict__['_wrapped_control']
            return getattr(wrapped.proxied_interface, name)

    def __init__(self, wrapped_control=None, *a, **k):
        (super(WrapperElement, self).__init__)(*a, **k)
        self._wrapped_control = wrapped_control
        self._parameter_slot = ParameterSlot()

    @property
    def proxied_object(self):
        if self._is_initialized():
            if self.owns_control_element(self._wrapped_control):
                return self._wrapped_control

    def _is_initialized(self):
        return '_wrapped_control' in self.__dict__

    def register_wrapped(self):
        self.register_control_element(self._wrapped_control)

    def unregister_wrapped(self):
        self.unregister_control_element(self._wrapped_control)

    @property
    def wrapped_control(self):
        return self._wrapped_control

    def __bool__(self):
        return self.owns_control_element(self._wrapped_control)

    def on_nested_control_element_received(self, control):
        if control == self._wrapped_control:
            self._parameter_slot.control = control

    def on_nested_control_element_lost(self, control):
        if control == self._wrapped_control:
            self._parameter_slot.control = None

    def on_nested_control_element_value(self, value, control):
        if control == self._wrapped_control:
            self.notify_value(value)

    def connect_to(self, parameter):
        if self._parameter_slot.parameter == None:
            self.request_listen_nested_control_elements()
        self._parameter_slot.parameter = parameter

    def release_parameter(self):
        if self._parameter_slot.parameter != None:
            self.unrequest_listen_nested_control_elements()
        self._parameter_slot.parameter = None


class ComboElement(WrapperElement):
    priority_increment = 0.5

    def __init__(self, control=None, modifiers=[], negative_modifiers=[], *a, **k):
        (super(ComboElement, self).__init__)(a, wrapped_control=control, **k)
        self._combo_modifiers = dict([(x, True) for x in modifiers] + [(x, False) for x in negative_modifiers])
        (self.register_control_elements)(*list(self._combo_modifiers.keys()))
        self.request_listen_nested_control_elements()

    def reset(self):
        if self.owns_control_element(self._wrapped_control):
            self._wrapped_control.reset()

    def get_control_element_priority(self, element, priority):
        if element == self._wrapped_control:
            priority = DEFAULT_PRIORITY if priority is None else priority
            return priority + self.priority_increment
        return priority

    def on_nested_control_element_received(self, control):
        if control != self._wrapped_control:
            self._enforce_control_invariant()
        else:
            super(ComboElement, self).on_nested_control_element_received(control)

    def on_nested_control_element_lost(self, control):
        if control != self._wrapped_control:
            self._enforce_control_invariant()
        else:
            super(ComboElement, self).on_nested_control_element_lost(control)

    def on_nested_control_element_value(self, value, control):
        if control != self._wrapped_control:
            self._enforce_control_invariant()
        else:
            super(ComboElement, self).on_nested_control_element_value(value, control)

    def _enforce_control_invariant(self):
        if self._combo_is_on():
            if not self.has_control_element(self._wrapped_control):
                self.register_control_element(self._wrapped_control)
        else:
            if self.has_control_element(self._wrapped_control):
                self.unregister_control_element(self._wrapped_control)

    def _combo_is_on(self):
        return all(map(self._modifier_is_valid, self._combo_modifiers))

    def _modifier_is_valid(self, mod):
        return self.owns_control_element(mod) and mod.is_pressed() == self._combo_modifiers[mod]


class EventElement(NotifyingControlElement, SlotManager, ProxyBase, ButtonElementMixin):
    event_value = 1
    _subject = None

    def __init__(self, subject=None, event=None, *a, **k):
        (super(EventElement, self).__init__)(*a, **k)
        self._subject = subject
        self.register_slot(subject, self._on_event, event)

    @property
    def proxied_object(self):
        return self._subject

    @property
    def proxied_interface(self):
        return getattr(self._subject, 'proxied_interface', self._subject)

    def _on_event(self, *a, **k):
        self.notify_value(self.event_value)

    def is_momentary(self):
        return False

    def reset(self):
        getattr(self._subject, 'reset', nop)()

    def send_value(self, *a, **k):
        try:
            send_value = super(EventElement, self).__getattr__('send_value')
        except AttributeError:
            send_value = nop

        send_value(*a, **k)

    def set_light(self, *a, **k):
        try:
            set_light = super(EventElement, self).__getattr__('set_light')
        except AttributeError:
            set_light = nop

        set_light(*a, **k)


class DoublePressContext(Subject):
    __subject_events__ = ('break_double_press', )

    @contextmanager
    def breaking_double_press(self):
        self._broke_double_press = False
        yield
        if not self._broke_double_press:
            self.break_double_press()

    def break_double_press(self):
        self.notify_break_double_press()
        self._broke_double_press = True


GLOBAL_DOUBLE_PRESS_CONTEXT_PROVIDER = const(DoublePressContext())

class DoublePressElement(WrapperElement):
    __subject_events__ = ('single_press', 'double_press')
    DOUBLE_PRESS_MAX_DELAY = Defaults.MOMENTARY_DELAY

    @depends(double_press_context=GLOBAL_DOUBLE_PRESS_CONTEXT_PROVIDER)
    def __init__(self, wrapped_control=None, double_press_context=None, *a, **k):
        (super(DoublePressElement, self).__init__)(a, wrapped_control=wrapped_control, **k)
        self.register_control_element(self._wrapped_control)
        self._double_press_context = double_press_context
        self._double_press_task = self._tasks.add(Task.sequence(Task.wait(self.DOUBLE_PRESS_MAX_DELAY), Task.run(self.finish_single_press))).kill()
        self.request_listen_nested_control_elements()

    def on_nested_control_element_value(self, value, control):
        if not control.is_momentary() or value and self._double_press_task.is_killed:
            self._double_press_context.break_double_press()
            self._on_break_double_press.subject = self._double_press_context
            self._double_press_task.restart()
        else:
            self.finish_double_press()
            self._double_press_task.kill()
        super(DoublePressElement, self).on_nested_control_element_value(value, control)

    @subject_slot('break_double_press')
    def _on_break_double_press(self):
        if not self._double_press_task.is_killed:
            self._double_press_task.kill()
            self.finish_single_press()

    def finish_single_press(self):
        self._on_break_double_press.subject = None
        self.notify_single_press()

    def finish_double_press(self):
        self._on_break_double_press.subject = None
        self.notify_double_press()

    @lazy_attribute
    def single_press(self):
        return EventElement(self, 'single_press')

    @lazy_attribute
    def double_press(self):
        return EventElement(self, 'double_press')


class MultiElement(CompoundElement, ButtonElementMixin):

    class ProxiedInterface(CompoundElement.ProxiedInterface):

        def __getattr__(self, name):
            found = find_if(lambda x: x is not None
, map(lambda c: getattr(c.proxied_interface, name, None)
, self.outer.nested_control_elements()))
            if found is not None:
                return found
            raise AttributeError

    def __init__(self, *controls, **k):
        (super(MultiElement, self).__init__)(**k)
        (self.register_control_elements)(*controls)

    def send_value(self, value):
        for control in self.owned_control_elements():
            control.send_value(value)

    def set_light(self, value):
        for control in self.owned_control_elements():
            control.set_light(value)

    def on_nested_control_element_value(self, value, control):
        if not self.is_pressed() or value:
            self.notify_value(value)

    def is_pressed(self):
        return find_if(lambda c: getattr(c, 'is_pressed', const(False))()
, self.owned_control_elements()) != None

    def is_momentary(self):
        return find_if(lambda c: getattr(c, 'is_momentary', const(False))()
, self.nested_control_elements()) != None

    def on_nested_control_element_received(self, control):
        pass

    def on_nested_control_element_lost(self, control):
        pass


class ToggleElement(WrapperElement):

    def __init__(self, on_control=None, off_control=None, *a, **k):
        (super(ToggleElement, self).__init__)(*a, **k)
        self._on_control = on_control
        self._off_control = off_control
        self._toggled = False
        self._update_toggled()

    def set_toggled(self, value):
        self._toggled = value
        self._update_toggled()

    def _update_toggled(self):
        if self.has_control_element(self._wrapped_control):
            self.unregister_control_element(self._wrapped_control)
        self._wrapped_control = self._on_control if self._toggled else self._off_control
        if self._wrapped_control != None:
            self.register_control_element(self._wrapped_control)