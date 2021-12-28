#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/control/control.py
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ...base import lazy_attribute, mixin, nop, old_hasattr, task, Disconnectable, EventObject, NamedTuple
__all__ = (u'Control', u'InputControl', u'ControlManager', u'control_event', u'control_color', u'Connectable')

class ControlManager(EventObject):
    u"""
    Base class needed to define Controls. The Control Manager stores the state of the
    Controls.
    """

    def __init__(self, *a, **k):
        super(ControlManager, self).__init__(*a, **k)
        self._control_states = dict()

    def add_control(self, name, control):
        u"""
        Dynamically adds a Control to the object. The Control will be added to the object
        as an attribute with the given `name`.
        """
        if old_hasattr(self, name):
            raise AttributeError(u'Control would overwrite an existing property')
        control_state = control._get_state(self)
        setattr(self, name, control_state)
        return control_state

    @lazy_attribute
    def _tasks(self):
        u"""
        Task Group for Controls for time-based events and feedback.
        """
        return task.TaskGroup()

    def control_notifications_enabled(self):
        u"""
        Override to enable/disable triggering events for all Controls in this
        Control Manager.
        """
        return True

    def update(self):
        u"""
        Sends the current feedback to all Control Elements that are connected to Controls
        of this Control Manager.
        """
        for control_state in self._control_states.values():
            control_state.update()


def control_event(event_name):
    u"""
    Defines an event of a Control. The event can be used in two ways:
    
     * As a function-decorator on a class level
     * By assigning a callable to the event
    
    Only one listener can be connected with an event.
    
    Events need to be defined on a Control class-level.
    """

    def event_decorator(self):

        def event_listener_decorator(event_listener):
            assert event_listener not in self._event_listeners
            self._event_listeners[event_name] = event_listener
            return self

        return event_listener_decorator

    def event_setter(self, event_listener):
        self._event_listeners[event_name] = event_listener

    return property(event_decorator, event_setter)


class control_color(object):
    u"""
    Defines a color of a Control. The color is created with a default color and will
    update the Control every time a new color is set.
    
    Colors need to be defined on Control-state level.
    """

    def __init__(self, default_color, *a, **k):
        super(control_color, self).__init__(*a, **k)
        self.default_color = default_color

    def __get__(self, obj, owner):
        if obj is None or self not in obj._colors:
            return self.default_color
        return obj._colors[self]

    def __set__(self, obj, val):
        obj._colors[self] = val
        obj._send_current_color()


class Control(object):
    u"""
    Base class for all Controls. Controls are used to define a high level interface for
    low level Control Elements. They add a useful set of functionality to it:
    
     * Well defined and descriptive events that compensate for inconsistencies of
       the received MIDI.
     * Logic and state common in other UI frameworks, like an enabled state to deactivate
       the Control under certain circumstances.
     * Feedback to represent different states of the Control.
    
    Controls are a virtual representation of a relation between a hardware control and
    a piece of logic. A Control needs to be connected with a Control Element to be
    functional. The Control Element is connected and disconnected by using
    :meth:`Control.State.set_control_element`. The user of a Control does not need to
    care if a Control Element is currently connected, which makes working with Controls
    much less error-prone than working with Control Elements directly.
    
    Controls are a Descriptor on a class level, so listeners can be easily defined using
    decorators. Events are defined using :func:`control_event`. Classes using Controls
    need to inherit from :class:`ControlManager`.
    
    The Control needs an actual stateful representation, that instantiated for each
    instance of the class implementing it. This is defined in the inner State-class.
    """

    class State(EventObject):
        u"""
        State-full representation of the Control.
        """
        enabled = True

        def __init__(self, control = None, manager = None, *a, **k):
            super(Control.State, self).__init__(*a, **k)
            assert control is not None
            assert manager is not None
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
            u"""
            Returns a Task Group for this Control. The Task Group is created the first
            time the property is accessed.
            """
            self._has_tasks = True
            return self._manager._tasks.add(task.TaskGroup())

        def set_control_element(self, control_element):
            u"""
            Connect a Control with a Control Element or disconnect the Control if
            None is passed. When connecting, the Control Element is reset and the
            Control's current color is sent. When disconnecting, the Control Element
            needs to be updated by its new owner.
            """
            self._control_element = control_element
            if self._control_element:
                self._control_element.reset_state()

        def _call_listener(self, listener_name, *args):
            listener = self._event_listeners.get(listener_name, None)
            if listener is not None and self._notifications_enabled():
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

    def __init__(self, extra_args = None, extra_kws = None, *a, **k):
        super(Control, self).__init__(*a, **k)
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
        raise RuntimeError(u'Cannot change control.')

    def _make_control_state(self, manager):
        return self.State(control=self, manager=manager, *self._extra_args, **self._extra_kws)

    def _get_state(self, manager, state_factory = None):
        if self not in manager._control_states:
            if state_factory is None:
                state_factory = self._make_control_state
            manager._control_states[self] = None
            manager._control_states[self] = state_factory(manager)
        if manager._control_states[self] is None:
            raise RuntimeError(u'Cannot fetch state during construction of controls.')
        return manager._control_states[self]

    def _clear_state(self, manager):
        if self in manager._control_states:
            del manager._control_states[self]


class InputControl(Control):
    u"""
    Base Class for Controls that react to a MIDI value event.
    """
    value = control_event(u'value')

    class State(Control.State):
        u"""
        State-full representation of the Control.
        """

        def __init__(self, control = None, channel = None, identifier = None, *a, **k):
            super(InputControl.State, self).__init__(control=control, *a, **k)
            self._value_slot = None
            self._channel = channel
            self._identifier = identifier
            self._register_value_slot(self._manager, control)
            self._manager.register_disconnectable(self)

        def set_control_element(self, control_element):
            u"""
            Connects the Control to the value-event of the Control Element and sets the
            defined :attr:`channel` and :attr:`identifier`.
            """
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
                self._value_slot = self.register_slot(None, self._on_value, u'value')

        def _on_value(self, value, *a, **k):
            self._call_listener(u'value', value)

        @property
        def channel(self):
            u"""
            Translates the channel of the received MIDI when sent to Live.
            """
            return self._channel

        @channel.setter
        def channel(self, channel):
            self._channel = channel
            if self._control_element:
                self._control_element.set_channel(self._channel)

        @property
        def identifier(self):
            u"""
            Translates the identifier of the received MIDI when sent to Live.
            """
            return self._identifier

        @identifier.setter
        def identifier(self, value):
            self._identifier = value
            if self._control_element:
                self._control_element.set_identifier(self._identifier)


class ProxyControl(object):
    u"""
    Control that has its own event listeners, but forwards everything else from the
    proxied control. This way, a derived class can forward the control of its base class.
    """

    def __init__(self, control = None, *a, **k):
        super(ProxyControl, self).__init__(*a, **k)
        self._control = control
        assert not self._control._event_listeners, u'Cannot forward control that already has events.'

    def _make_control_state(self, manager):
        u"""
        Pass the proxy control to the state, as this one includes the event handlers
        """
        return self._control.State(control=self, manager=manager, *self._control._extra_args, **self._control._extra_kws)

    def _get_state(self, manager, state_factory = None):
        return self._control._get_state(manager, self._make_control_state)

    def _clear_state(self, manager):
        self._control._clear_state(manager)


def forward_control(control):
    return mixin(ProxyControl, control.__class__)(control)


class NullSlot(Disconnectable):
    pass


class Connectable(EventObject):
    u"""
    Mixin for connecting a property with a control.
    """
    requires_listenable_connected_property = False

    def __init__(self, *a, **k):
        super(Connectable, self).__init__(*a, **k)
        self._connection = self._make_empty_connection()

    def connect_property(self, subject, property_name, transform = nop):
        u"""
        Create a bidirectional connection between a property and a Control.
        The `subject` is the host of the property with the given name.
        The connected property needs to be listenable in case
        :attr:`requires_listenable_connected_property` is set to True.
        If a Control is a Connectable, it has certain expectations on the connected
        property.
        
        The transform argument can be used to transform the Control's value to the
        expected value of the property.
        
        Only one property can be connected at a time.
        """
        assert subject is not None
        self.disconnect_property()
        self._connection = NamedTuple(slot=self._register_property_slot(subject, property_name), getter=partial(getattr, subject, property_name), setter=partial(setattr, subject, property_name), transform=transform)

    def disconnect_property(self):
        u"""
        Disconnects a property that has been connected with :meth:`connect_property`.
        """
        self._connection.slot.disconnect()
        self._connection = self._make_empty_connection()

    def _make_empty_connection(self):
        return NamedTuple(slot=NullSlot(), getter=nop, setter=nop, transform=nop)

    def _register_property_slot(self, subject, property_name):
        if self.requires_listenable_connected_property:
            return self.register_slot(subject, self.on_connected_property_changed, property_name)
        else:
            return NullSlot()

    @property
    def connected_property_value(self):
        u"""
        Get/set the property connected with :meth:`connect_property`
        """
        return self._connection.getter()

    @connected_property_value.setter
    def connected_property_value(self, value):
        self._connection.setter(self._connection.transform(value))

    def on_connected_property_changed(self, value):
        u"""
        Called if the connected property changes.
        Has no effect if :attr:`requires_listenable_connected_property` is set to False.
        """
        pass


class SendValueMixin(object):

    def __init__(self, *a, **k):
        super(SendValueMixin, self).__init__(*a, **k)
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
