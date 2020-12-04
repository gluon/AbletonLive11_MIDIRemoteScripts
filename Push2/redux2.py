#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/redux2.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_options import DeviceOnOffOption

class Redux2DeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        super(Redux2DeviceDecorator, self).__init__(*a, **k)
        self.postFilter_on_option = DeviceOnOffOption(name=u'Post-Filter', property_host=get_parameter_by_name(self, u'Post-Filter On'))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.postFilter_on_option,)
        self._additional_parameters = ()
        self.register_disconnectable(self._additional_parameters)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters
