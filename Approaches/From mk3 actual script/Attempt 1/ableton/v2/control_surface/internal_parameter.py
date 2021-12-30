#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/internal_parameter.py
from __future__ import absolute_import, print_function, unicode_literals
from past.builtins import unicode
from Live import DeviceParameter
from ..base import clamp, listenable_property, liveobj_valid, nop, old_hasattr, EventError, EventObject, Slot

def identity(value, _parent):
    return value


def to_percentage_display(value):
    percentage = 100.0 * value
    percentage_str = u'100'
    if percentage < 100.0:
        precision = 2 if percentage < 10.0 else 1
        format_str = u'%.' + str(precision) + u'f'
        percentage_str = format_str % percentage
    return unicode(percentage_str + u' %')


class InternalParameterBase(EventObject):
    is_enabled = True
    is_quantized = False

    def __init__(self, name = None, *a, **k):
        assert name is not None
        super(InternalParameterBase, self).__init__(*a, **k)
        self._name = name
        self._state = DeviceParameter.ParameterState.enabled

    def _has_valid_parent(self):
        return liveobj_valid(self._parent)

    @property
    def canonical_parent(self):
        raise NotImplementedError

    @property
    def display_value(self):
        raise NotImplementedError

    @property
    def min(self):
        raise NotImplementedError

    @property
    def max(self):
        raise NotImplementedError

    @property
    def value(self):
        raise NotImplementedError

    @listenable_property
    def name(self):
        return self._name

    @property
    def original_name(self):
        return self._name

    @property
    def default_value(self):
        return self.min

    @listenable_property
    def automation_state(self):
        return DeviceParameter.AutomationState.none

    @listenable_property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        assert new_state in (DeviceParameter.ParameterState.enabled, DeviceParameter.ParameterState.irrelevant, DeviceParameter.ParameterState.disabled)
        self._state = new_state
        self.notify_state()

    @property
    def _live_ptr(self):
        return id(self)

    def __str__(self):
        return self.display_value


class InternalParameter(InternalParameterBase):
    u"""
    Class implementing the DeviceParameter interface. Using instances of this class,
    we can mix script-internal values with DeviceParameter instances.
    """
    __events__ = (u'value',)

    def __init__(self, parent = None, display_value_conversion = None, *a, **k):
        super(InternalParameter, self).__init__(*a, **k)
        self._value = 0.0
        self._parent = parent
        self.set_display_value_conversion(display_value_conversion)
        self.set_scaling_functions(None, None)

    def set_display_value_conversion(self, display_value_conversion):
        self._display_value_conversion = display_value_conversion or to_percentage_display
        self.notify_value()

    def set_scaling_functions(self, to_internal, from_internal):
        self._to_internal = to_internal or identity
        self._from_internal = from_internal or identity

    @property
    def canonical_parent(self):
        return self._parent

    def _get_value(self):
        if self._has_valid_parent():
            return self._from_internal(self.linear_value, self._parent)
        return self.min

    def _set_value(self, new_value):
        assert self.min <= new_value <= self.max, u'Invalid value %f' % new_value
        self.linear_value = self._to_internal(new_value, self._parent)

    value = property(_get_value, _set_value)

    def _get_linear_value(self):
        return self._value

    def _set_linear_value(self, new_value):
        if new_value != self._value:
            self._value = new_value
            self.notify_value()

    linear_value = property(_get_linear_value, _set_linear_value)

    @property
    def min(self):
        return 0.0

    @property
    def max(self):
        return 1.0

    @property
    def display_value(self):
        return self._display_value_conversion(self.value)


class PropertyHostMixin(object):
    u"""
    This is only used to document the set_property_host API
    """

    def set_property_host(self, new_host):
        raise NotImplementedError


class WrappingParameter(InternalParameter, PropertyHostMixin):

    def __init__(self, property_host = None, source_property = None, from_property_value = None, to_property_value = None, display_value_conversion = nop, value_items = [], *a, **k):
        assert source_property is not None
        super(WrappingParameter, self).__init__(display_value_conversion=display_value_conversion, *a, **k)
        self._property_host = property_host
        assert self._property_host == None or old_hasattr(self._property_host, source_property) or source_property in dir(self._property_host)
        self._source_property = source_property
        self._value_items = value_items
        self.set_scaling_functions(to_property_value, from_property_value)
        self._property_slot = self.register_slot(Slot(listener=self.notify_value, event_name=source_property, subject=self._property_host))

    def set_property_host(self, new_host):
        self._property_host = new_host
        self._property_slot.subject = self._property_host

    def _get_property_value(self):
        if liveobj_valid(self._property_host):
            return getattr(self._property_host, self._source_property)
        return self.min

    def _get_value(self):
        try:
            if liveobj_valid(self._property_host):
                return self._from_internal(self._get_property_value(), self._property_host)
            return self.min
        except RuntimeError:
            return self.min

    def _set_value(self, new_value):
        assert self.min <= new_value <= self.max, u'Invalid value %f' % new_value
        if liveobj_valid(self._property_host):
            try:
                setattr(self._property_host, self._source_property, self._to_internal(new_value, self._property_host))
            except RuntimeError:
                pass

    linear_value = property(_get_value, _set_value)
    value = property(_get_value, _set_value)

    @property
    def display_value(self):
        try:
            value = self._get_property_value()
            return unicode(self._display_value_conversion(value) if liveobj_valid(self._property_host) else u'')
        except RuntimeError:
            return unicode()

    @property
    def is_quantized(self):
        return len(self._value_items) > 0

    @property
    def value_items(self):
        return self._value_items


class EnumWrappingParameter(InternalParameterBase, PropertyHostMixin):
    is_enabled = True
    is_quantized = True

    def __init__(self, parent = None, index_property_host = None, values_host = None, values_property = None, index_property = None, value_type = int, to_index_conversion = None, from_index_conversion = None, *a, **k):
        assert parent is not None
        assert values_property is not None
        assert index_property is not None
        super(EnumWrappingParameter, self).__init__(*a, **k)
        self._parent = parent
        self._values_host = values_host
        self._index_property_host = index_property_host
        self._values_property = values_property
        self._index_property = index_property
        self._to_index = to_index_conversion or (lambda x: x)
        self._from_index = from_index_conversion or (lambda x: x)
        self.value_type = value_type
        self._index_property_slot = self.register_slot(index_property_host, self.notify_value, index_property)
        try:
            self.register_slot(self._values_host, self.notify_value_items, values_property)
        except EventError:
            pass

    def set_property_host(self, new_host):
        self._index_property_host = new_host
        self._index_property_slot.subject = self._index_property_host

    @property
    def display_value(self):
        index = self._get_index()
        values = self._get_values()
        if index < len(values):
            return unicode(values[index])
        else:
            return unicode()

    @listenable_property
    def value_items(self):
        return self._get_values()

    @listenable_property
    def value(self):
        return self._get_index()

    @value.setter
    def value(self, new_value):
        if new_value < 0 or new_value >= len(self._get_values()):
            raise IndexError
        self._set_index(new_value)

    def _get_values(self):
        if liveobj_valid(self._values_host):
            return getattr(self._values_host, self._values_property)
        return []

    def _get_index(self):
        return self._from_index(int(getattr(self._index_property_host, self._index_property)) if liveobj_valid(self._index_property_host) else 0)

    def _set_index(self, index):
        if liveobj_valid(self._index_property_host):
            index = self._to_index(index)
            setattr(self._index_property_host, self._index_property, self.value_type(index))

    @property
    def canonical_parent(self):
        return self._parent

    @property
    def max(self):
        return len(self.value_items) - 1

    @property
    def min(self):
        return 0


class RelativeInternalParameter(InternalParameter):
    __events__ = (u'delta',)

    @property
    def default_value(self):
        return 0.5

    def _get_value(self):
        return self.default_value

    def _set_value(self, new_value):
        delta = new_value - self.value
        if delta != 0.0:
            self.notify_value()
            self.notify_delta(delta)

    value = property(_get_value, _set_value)
    linear_value = property(_get_value, _set_value)


class IntegerParameter(InternalParameter):

    def __init__(self, integer_value_host = None, integer_value_property_name = None, min_value = None, max_value = None, show_as_quantized = False, *a, **k):
        super(IntegerParameter, self).__init__(display_value_conversion=unicode, *a, **k)
        self._integer_value_host = integer_value_host
        self._integer_value_property_name = integer_value_property_name
        self._min_value = min_value if min_value is not None else 0
        self._max_value = max_value if max_value is not None else 1
        self._show_as_quantized = show_as_quantized
        self._value = self._get_value()
        try:
            self.register_slot(integer_value_host, self.notify_value, integer_value_property_name)
        except EventError:
            pass

    def _get_value(self):
        value = self._get_integer_value()
        if self._show_as_quantized:
            return self._index_from_value(value)
        return value

    def _set_value(self, new_value):
        if new_value != self._value:
            self._value = new_value
            self._set_integer_value(self._index_to_value(new_value) if self._show_as_quantized else new_value)

    value = property(_get_value, _set_value)

    def _get_linear_value(self):
        return self._value

    def _set_linear_value(self, new_value):
        if new_value != self._value:
            self._value = new_value
            if int(new_value) != self._get_integer_value():
                self._set_integer_value(new_value)
                self.notify_value()

    linear_value = property(_get_linear_value, _set_linear_value)

    def _get_integer_value(self):
        if liveobj_valid(self._integer_value_host):
            return getattr(self._integer_value_host, self._integer_value_property_name)
        return self._min_value

    def _set_integer_value(self, new_value):
        assert self._min_value <= new_value <= self._max_value, u'Invalid value {}'.format(new_value)
        setattr(self._integer_value_host, self._integer_value_property_name, int(new_value))

    def _index_to_value(self, index):
        return clamp(self._min_value, index + self._min_value, self._max_value)

    def _index_from_value(self, value):
        return clamp(self._min_index, value - self._min_value, self._max_index)

    @property
    def _min_index(self):
        return 0

    @property
    def _max_index(self):
        return self._max_value - self._min_value

    @property
    def min(self):
        if self._show_as_quantized:
            return self._min_index
        return self._min_value

    @property
    def max(self):
        if self._show_as_quantized:
            return self._max_index
        return self._max_value

    @property
    def is_quantized(self):
        return self._show_as_quantized

    @property
    def value_items(self):
        return list(range(self._min_value, self._max_value + 1))
