#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/LV2_LX2_LC2_LD2/LV2_LX2_LC2_LD2.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from .FaderfoxScript import FaderfoxScript
from .LV2MixerController import LV2MixerController
from .LV2DeviceController import LV2DeviceController
from .FaderfoxDeviceController import FaderfoxDeviceController
from .LV2TransportController import LV2TransportController
from .consts import *

class LV2_LX2_LC2_LD2(FaderfoxScript):
    __module__ = __name__
    __doc__ = u'Automap script for LV2 Faderfox controllers'
    __name__ = u'LV2_LX2_LC2_LD2 Remote Script'

    def __init__(self, c_instance):
        LV2_LX2_LC2_LD2.realinit(self, c_instance)

    def realinit(self, c_instance):
        self.suffix = u'2'
        FaderfoxScript.realinit(self, c_instance)
        self.mixer_controller = LV2MixerController(self)
        self.device_controller = LV2DeviceController(self)
        self.transport_controller = LV2TransportController(self)
        self.components = [self.mixer_controller, self.device_controller, self.transport_controller]

    def suggest_map_mode(self, cc_no, channel):
        return -1
