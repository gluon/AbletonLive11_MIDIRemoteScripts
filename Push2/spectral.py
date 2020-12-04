#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/spectral.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_options import DeviceOnOffOption, DeviceSwitchOption

class SpectralDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        super(SpectralDeviceDecorator, self).__init__(*a, **k)
        self.freeze_option = DeviceOnOffOption(name=u'Freeze', property_host=get_parameter_by_name(self, u'Freeze On'))
        self.unit_option = DeviceSwitchOption(name=u'Unit', parameter=get_parameter_by_name(self, u'Unit'), labels=[u'ms', u'Notes'])
        self.delay_unit_option = DeviceSwitchOption(name=u'Delay Dly. Unit', parameter=get_parameter_by_name(self, u'Delay Dly. Unit'), labels=[u'ms',
         u'Notes',
         u'16th',
         u'Tr',
         u'Dt'])
        self.fade_type_option = DeviceSwitchOption(name=u'Fade Type', parameter=get_parameter_by_name(self, u'Fade Type'), labels=[u'X-Fade', u'Env'])
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.freeze_option,
         self.unit_option,
         self.delay_unit_option,
         self.fade_type_option)
        self._additional_parameters = ()
        self.register_disconnectable(self._additional_parameters)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters
