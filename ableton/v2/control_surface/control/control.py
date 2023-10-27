# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\control\control.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 16626 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ...base import Disconnectable, EventObject, NamedTuple, lazy_attribute, mixin, nop, old_hasattr, task
__all__ = ('Control', 'InputControl', 'ControlManager', 'control_event', 'control_color',
           'Connectable')

class ControlManager(EventObject):

    def __init__(self, *a, **k):
        (super(ControlManager, self).__init__)(*a, **k)
        self._control_states = dict()

    def add_control(self, name, control):
        if old_hasattr(self, name):
            raise AttributeError('Control would overwrite an existing property')
        control_state = control._get_state(self)
        setattr(self, name, control_state)
        return control_state

    @lazy_attribute
    def _tasks(self):
        return task.TaskGroup()

    def control_notifications_enabled(self):
        return True

    def update(self):
        for control_state in self._control_states.values():
            control_state.update()


def control_event(event_name):

    def event_decorator(self):

        def event_listener_decorator(event_listener):
            self._event_listeners[event_name] = event_listener
            return self

        return event_listener_decorator

    def event_setter(self, event_listener):
        self._event_listeners[event_name] = event_listener

    return property(event_decorator, event_setter)


class control_color(object):

    def __init__(self, default_color, *a, **k):
        (super(control_color, self).__init__)(*a, **k)
        self.default_color = default_color

    def __get__(self, obj, owner):
        if obj is None or self not in obj._colors:
            return self.default_color
        return obj._colors[self]

    def __set__(self, obj, val):
        obj._colors[self] = val
        obj._send_current_color()


class Control(object):

    class State(EventObject):
        enabled = True

        def __init__(self, control=None, manager=None, *a, **k):
            (super(Control.State, self).__init__)(*a, **k)
            self._colors = dict()
            self._manager = manager
            self._event_listeners = control._event_listeners
            self._control_element = None
            self._has_tasks = False
            manager.register_disconnectable(self)

        def disconnect(self):
            super(Control.State, self).disconnect()
            if self._has_tasks:
                self.tasks.kill()
                self.tasks.clear()

        @lazy_attribute
        def tasks(self):
            self._has_tasks = True
            return self._manager._tasks.add(task.TaskGroup())

        @property
        def control_element(self):
            return self._control_element

        def set_control_element(self, control_element):
            self._control_element = control_element
            if self._control_element:
                self._control_element.reset_state()

        def _call_listener(self, listener_name, *args):
            listener = self._event_listeners.get(listener_name, None)
            if listener is not None:
                if self._notifications_enabled():
                    args = args + (self,)
                    listener(self._manager, *args)

        def _has_listener(self, listener_name):
            return listener_name in self._event_listeners

        def _event_listener_required(self):
            return len(self._event_listeners) > 0

        def _notifications_enabled(self):
            return self.enabled and self._manager.control_notifications_enabled()

        def update(self):
            pass

        def _send_current_color(self):
            pass

    _extra_kws = {}
    _extra_args = []

    def __init__(self, extra_args=None, extra_kws=None, *a, **k):
        (super(Control, self).__init__)(*a, **k)
        self._event_listeners = {}
        if extra_args is not None:
            self._extra_args = extra_args
        if extra_kws is not None:
            self._extra_kws = extra_kws

    def __get__(self, manager, owner):
        if manager is not None:
            return self._get_state(manager)
        return self

    def __set__(self, manager, owner):
        raise RuntimeError('Cannot change control.')

    def _make_control_state(self, manager):
        return (self.State)(self._extra_args, control=self, manager=manager, **self._extra_kws)

    def _get_state(self, manager, state_factory=None):
        if self not in manager._control_states:
            if state_factory is None:
                state_factory = self._make_control_state
            manager._control_states[self] = None
            manager._control_states[self] = state_factory(manager)
        if manager._control_states[self] is None:
            raise RuntimeError('Cannot fetch state during construction of controls.')
        return manager._control_states[self]

    def _clear_state(self, manager):
        if self in manager._control_states:
            del manager._control_states[self]


class InputControl(Control):
    value = control_event('value')

    class State(Control.State):

        def __init__(self, control=None, channel=None, identifier=None, *a, **k):
            (super(InputControl.State, self).__init__)(a, control=control, **k)
            self._value_slot = None
            self._channel = channel
            self._identifier = identifier
            self._register_value_slot(self._manager, control)
            self._manager.register_disconnectable(self)

        def set_control_element(self, control_element):
            super(InputControl.State, self).set_control_element(control_element)
            if self._value_slot:
                self._value_slot.subject = control_element
            if self._control_element:
                if self._channel is not None:
                    self._control_element.set_channel(self._channel)
                if self._identifier is not None:
                    self._control_element.set_identifier(self._identifier)

        def _register_value_slot(self, manager, control):
            if self._event_listener_required():
                self._value_slot = self.register_slot(None, self._on_value, 'value')

        def _on_value(self, value, *a, **k):
            self._call_listener('value', value)

        @property
        def channel(self):
            return self._channel

        @channel.setter
        def channel(self, channel):
            self._channel = channel
            if self._control_element:
                self._control_element.set_channel(self._channel)

        @property
        def identifier(self):
            return self._identifier

        @identifier.setter
        def identifier(self, value):
            self._identifier = value
            if self._control_element:
                self._control_element.set_identifier(self._identifier)


class ProxyControl(object):

    def __init__(self, control=None, *a, **k):
        (super(ProxyControl, self).__init__)(*a, **k)
        self._control = control

    def _make_control_state(self, manager):
        return (self._control.State)(self._control._extra_args, control=self, manager=manager, **self._control._extra_kws)

    def _get_state(self, manager, state_factory=None):
        return self._control._get_state(manager, self._make_control_state)

    def _clear_state(self, manager):
        self._control._clear_state(manager)


def forward_control(control):
    return mixin(ProxyControl, control.__class__)(control)


class NullSlot(Disconnectable):
    pass


class Connectable(EventObject):
    requires_listenable_connected_property = False

    def __init__(self, *a, **k):
        (super(Connectable, self).__init__)(*a, **k)
        self._connection = self._make_empty_connection()

    def connect_property(self, subject, property_name, transform=nop):
        self.disconnect_property()
        self._connection = NamedTuple(slot=(self._register_property_slot(subject, property_name)),
          getter=(partial(getattr, subject, property_name)),
          setter=(partial(setattr, subject, property_name)),
          transform=transform)

    def disconnect_property(self):
        self._connection.slot.disconnect()
        self._connection = self._make_empty_connection()

    def _make_empty_connection(self):
        return NamedTuple(slot=(NullSlot()), getter=nop, setter=nop, transform=nop)

    def _register_property_slot(self, subject, property_name):
        if self.requires_listenable_connected_property:
            return self.register_slot(subject, self._handle_connected_property_changed, property_name)
        return NullSlot()

    def _handle_connected_property_changed(self, value=None):
        self.on_connected_property_changed(value if value is not None else self._connection.getter())

    @property
    def connected_property_value(self):
        return self._connection.getter()

    @connected_property_value.setter
    def connected_property_value(self, value):
        self._connection.setter(self._connection.transform(value))

    def on_connected_property_changed(self, value):
        pass


class SendValueMixin(object):

    def __init__(self, *a, **k):
        (super(SendValueMixin, self).__init__)(*a, **k)
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._value != value:
            self._value = value
            self._send_current_value()

    def set_control_element(self, control_element):
        super(SendValueMixin, self).set_control_element(control_element)
        self._send_current_value()

    def update(self):
        super(SendValueMixin, self).update()
        self._send_current_value()

    def _send_current_value(self):
        if self._control_element:
            self._control_element.send_value(self._value)


class SendValueControl(Control):

    class State(SendValueMixin, Control.State):
        pass