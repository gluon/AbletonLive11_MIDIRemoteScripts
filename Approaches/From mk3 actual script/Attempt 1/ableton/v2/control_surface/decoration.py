#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/decoration.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import round
from builtins import map
from builtins import filter
from future.utils import iteritems
import Live
AutomationState = Live.DeviceParameter.AutomationState
from ..base import CompoundDisconnectable, EventObject, Proxy, clamp, find_if, listenable_property, listens, liveobj_valid, old_hasattr
from .internal_parameter import InternalParameter

def get_parameter_by_name(decorator, name):
    return find_if(lambda p: p.name == name, decorator._live_object.parameters)


def get_parameter_automation_state(parameter):
    return getattr(parameter, u'automation_state', AutomationState.none)


class LiveObjectDict(dict):

    def __init__(self, *a, **k):
        self.update(*a, **k)

    def __getitem__(self, key):
        return super(LiveObjectDict, self).__getitem__(self._transform_key(key))

    def __setitem__(self, key, value):
        return super(LiveObjectDict, self).__setitem__(self._transform_key(key), value)

    def __delitem__(self, key):
        return super(LiveObjectDict, self).__delitem__(self._transform_key(key))

    def __contains__(self, key):
        return super(LiveObjectDict, self).__contains__(self._transform_key(key))

    def get(self, key, *default):
        return super(LiveObjectDict, self).get(self._transform_key(key), *default)

    def _transform_key(self, key):
        assert old_hasattr(key, u'_live_ptr')
        return key._live_ptr

    def update(self, *a, **k):
        trans = self._transform_key
        super(LiveObjectDict, self).update(*[ (trans(key), v) for key, v in a ], **dict(((trans(key), k[key]) for key in k)))

    def prune(self, keys):
        transformed_keys = list(map(self._transform_key, keys))
        deleted_objects = []
        for key in filter(lambda x: x not in transformed_keys, list(self.keys())):
            deleted_objects.append(super(LiveObjectDict, self).__getitem__(key))
            super(LiveObjectDict, self).__delitem__(key)

        return deleted_objects


class LiveObjectDecorator(CompoundDisconnectable, Proxy):

    def __init__(self, live_object = None, additional_properties = {}):
        assert live_object is not None
        super(LiveObjectDecorator, self).__init__(proxied_object=live_object)
        self._live_object = live_object
        for name, value in iteritems(additional_properties):
            setattr(self, name, value)

    def __eq__(self, other):
        return id(self) == id(other) or self._live_object == other

    def __ne__(self, other):
        return not self == other

    def __nonzero__(self):
        return self._live_object != None

    def __bool__(self):
        return self.__nonzero__()

    def __hash__(self):
        return hash(self._live_object)


class DecoratorFactory(CompoundDisconnectable):
    _decorator = LiveObjectDecorator

    def __init__(self, *a, **k):
        super(DecoratorFactory, self).__init__(*a, **k)
        self.decorated_objects = LiveObjectDict()

    def decorate(self, live_object, additional_properties = {}, **k):
        if self._should_be_decorated(live_object):
            if not self.decorated_objects.get(live_object, None):
                self.decorated_objects[live_object] = self.register_disconnectable(self._get_decorated_object(live_object, additional_properties, **k))
            live_object = self.decorated_objects[live_object]
        return live_object

    def _get_decorated_object(self, live_object, additional_properties, **k):
        return self._decorator(live_object=live_object, additional_properties=additional_properties, **k)

    def sync_decorated_objects(self, keys):
        deleted_objects = self.decorated_objects.prune(keys)
        for decorated in deleted_objects:
            self.unregister_disconnectable(decorated)
            decorated.disconnect()

    @classmethod
    def _should_be_decorated(cls, device):
        return True


class NotifyingList(EventObject):
    __events__ = (u'index',)

    def __init__(self, available_values, default_value = None, *a, **k):
        super(NotifyingList, self).__init__(*a, **k)
        self._index = default_value if default_value is not None else 0
        self._available_values = available_values

    @property
    def available_values(self):
        return self._available_values

    def _get_index(self):
        return self._index

    def _set_index(self, value):
        if value < 0 or value >= len(self.available_values):
            raise IndexError
        self._index = value
        self.notify_index()

    index = property(_get_index, _set_index)


class PitchParameter(InternalParameter):

    def __init__(self, integer_value_host = None, decimal_value_host = None, *a, **k):
        super(PitchParameter, self).__init__(*a, **k)
        self._integer_value_host = integer_value_host
        self._decimal_value_host = decimal_value_host
        self._on_integer_value_changed.subject = integer_value_host
        self._on_decimal_value_changed.subject = decimal_value_host
        self._on_integer_value_automation_state_changed.subject = integer_value_host
        self._on_decimal_value_automation_state_changed.subject = decimal_value_host
        self._integer_value = getattr(integer_value_host, u'value', 0)
        self._decimal_value = getattr(decimal_value_host, u'value', 0.0)
        self.adjust_finegrain = False

    @listens(u'value')
    def _on_integer_value_changed(self):
        new_integer_value = self._integer_value_host.value
        if self._integer_value != new_integer_value:
            self._integer_value = new_integer_value
            self.notify_value()

    @listens(u'value')
    def _on_decimal_value_changed(self):
        new_decimal_value = self._decimal_value_host.value
        if self._decimal_value != new_decimal_value:
            self._decimal_value = new_decimal_value
            self.notify_value()

    @listens(u'automation_state')
    def _on_integer_value_automation_state_changed(self):
        self.notify_automation_state()

    @listens(u'automation_state')
    def _on_decimal_value_automation_state_changed(self):
        self.notify_automation_state()

    @property
    def _combined_value(self):
        return getattr(self._integer_value_host, u'value', 0) + (getattr(self._decimal_value_host, u'value', 0.0) - 0.5)

    def _get_value(self):
        return self._combined_value

    def _set_value(self, new_value):
        if new_value != self._combined_value:
            coarse_linear_value = round(new_value)
            fine_linear_value = new_value - coarse_linear_value + 0.5
            self._set_coarse(coarse_linear_value)
            self._set_finegrain(fine_linear_value)
            self.notify_value()

    value = property(_get_value, _set_value)

    def _get_linear_value(self):
        if self.adjust_finegrain:
            return self._decimal_value
        return self._integer_value

    def _set_linear_value(self, new_value):
        if self.adjust_finegrain:
            if self._decimal_value != new_value:
                self._set_finegrain(new_value)
                self.notify_value()
        elif self._integer_value != new_value:
            self._set_coarse(new_value)
            self.notify_value()

    linear_value = listenable_property(_get_linear_value, _set_linear_value)

    def _set_coarse(self, new_value):
        self._integer_value = new_value
        if liveobj_valid(self._integer_value_host):
            self._integer_value_host.value = clamp(new_value, self._integer_value_host.min, self._integer_value_host.max)

    def _set_finegrain(self, new_value):
        if new_value < 0 or new_value > 1:
            offset = 1 if new_value < 0 else -1
            new_value += offset
            self._set_coarse(getattr(self._integer_value_host, u'value', 0) - offset)
        self._decimal_value = new_value
        if liveobj_valid(self._decimal_value_host):
            self._decimal_value_host.value = new_value

    @property
    def decimal_value_host(self):
        return self._decimal_value_host

    @property
    def integer_value_host(self):
        return self._integer_value_host

    @property
    def min(self):
        return getattr(self._integer_value_host, u'min', 0) - getattr(self._decimal_value_host, u'min', 0.0)

    @property
    def max(self):
        return getattr(self._integer_value_host, u'max', 1) + getattr(self._decimal_value_host, u'max', 1.0)

    @property
    def display_value(self):
        return u'{0:.2f}st'.format(self._combined_value)

    @property
    def default_value(self):
        return 0

    @property
    def automation_state(self):
        integer_host_automation_state = get_parameter_automation_state(self._integer_value_host)
        decimal_host_automation_state = get_parameter_automation_state(self._decimal_value_host)
        if integer_host_automation_state == AutomationState.playing or decimal_host_automation_state == AutomationState.playing:
            return AutomationState.playing
        return integer_host_automation_state or decimal_host_automation_state
