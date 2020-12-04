#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/device_options.py
from __future__ import absolute_import, print_function, unicode_literals
from Live import DeviceParameter
from ableton.v2.base import clamp, liveobj_valid, listenable_property, listens, const, EventObject, Slot

class DeviceTriggerOption(EventObject):
    __events__ = (u'default_label',)

    def __init__(self, name = None, default_label = None, callback = None, is_active = None, *a, **k):
        assert callback
        super(DeviceTriggerOption, self).__init__(*a, **k)
        self.trigger = callback
        self._name = name or u'Option'
        self._default_label = default_label or self._name
        self._is_active_callback = is_active or const(True)

    @property
    def name(self):
        return self._name

    @listenable_property
    def active(self):
        return self._is_active()

    def _is_active(self):
        return self._is_active_callback()

    def _get_default_label(self):
        return self._default_label

    def _set_default_label(self, label):
        self._default_label = label
        self.notify_default_label()

    default_label = property(_get_default_label, _set_default_label)


class DeviceSwitchOption(DeviceTriggerOption):

    def __init__(self, labels = None, parameter = None, *a, **k):
        super(DeviceSwitchOption, self).__init__(callback=self.cycle_index, *a, **k)
        self._custom_labels = labels
        self.set_parameter(parameter)

    def set_parameter(self, parameter):
        self._parameter = parameter
        self.__on_value_changed.subject = parameter
        self._parameter_labels = []
        self._num_items = 2
        if liveobj_valid(parameter) and parameter.is_quantized:
            self._parameter_labels = [ item.replace(u' ', u'') for item in parameter.value_items ]
            self._num_items = max(len(parameter.value_items), 1)
        self.notify_active_index()
        self.notify_active()

    def _is_active(self):
        return super(DeviceSwitchOption, self)._is_active() and liveobj_valid(self._parameter) and self._parameter.state == DeviceParameter.ParameterState.enabled

    @listenable_property
    def active_index(self):
        if liveobj_valid(self._parameter):
            return clamp(int(self._parameter.value), 0, self._num_items - 1)
        return 0

    @listens(u'value')
    def __on_value_changed(self):
        self.notify_active_index()

    @property
    def labels(self):
        if self._custom_labels is not None:
            return self._custom_labels
        return self._parameter_labels

    def cycle_index(self):
        if liveobj_valid(self._parameter):
            self._parameter.value = float((self.active_index + 1) % self._num_items)


class DeviceOnOffOption(DeviceTriggerOption):
    ON_LABEL = u'On'
    OFF_LABEL = u'Off'

    def __init__(self, name = None, property_host = None, value_property_name = u'value', state_property_name = u'state', *a, **k):
        super(DeviceOnOffOption, self).__init__(callback=self.cycle_index, name=name, *a, **k)
        self._value_property_name = value_property_name
        self._state_property_name = state_property_name
        self.set_property_host(property_host)

    def set_property_host(self, property_host):
        self._property_host = property_host

        def notify_index_and_default_label():
            self.notify_active_index()
            self.notify_default_label()

        self._property_slot = self.register_slot(Slot(subject=property_host, event_name=self._value_property_name, listener=notify_index_and_default_label))

    def _property_value(self):
        if liveobj_valid(self._property_host):
            return getattr(self._property_host, self._value_property_name, False)
        return False

    def _is_active(self):
        return super(DeviceOnOffOption, self)._is_active() and liveobj_valid(self._property_host) and getattr(self._property_host, self._state_property_name, 0) == DeviceParameter.ParameterState.enabled

    @listenable_property
    def active_index(self):
        return int(not self._property_value())

    def cycle_index(self):
        if liveobj_valid(self._property_host):
            value_type = type(self._property_value())
            new_value = not bool((self.active_index + 1) % 2)
            setattr(self._property_host, self._value_property_name, value_type(new_value))

    @property
    def default_label(self):
        return u'%s %s' % (self._default_label, self.ON_LABEL if self._property_value() else self.OFF_LABEL)
