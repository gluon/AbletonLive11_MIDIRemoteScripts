# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\LV1_LX1\LV1_LX1.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 1214 bytes
from __future__ import absolute_import, print_function, unicode_literals
import LV2_LX2_LC2_LD2.FaderfoxComponent as FaderfoxComponent
import LV2_LX2_LC2_LD2.FaderfoxDeviceController as FaderfoxDeviceController
import LV2_LX2_LC2_LD2.FaderfoxMixerController as FaderfoxMixerController
import LV2_LX2_LC2_LD2.FaderfoxScript as FaderfoxScript
import LV2_LX2_LC2_LD2.FaderfoxTransportController as FaderfoxTransportController

class LV1_LX1(FaderfoxScript):
    __module__ = __name__
    __doc__ = 'Automap script for LV1 Faderfox controllers'
    __name__ = 'LV1_LX1 Remote Script'

    def __init__(self, c_instance):
        LV1_LX1.realinit(self, c_instance)

    def realinit(self, c_instance):
        self.suffix = '1'
        FaderfoxScript.realinit(self, c_instance)
        self.is_lv1 = True
        self.log('lv1 lx1')
        self.mixer_controller = FaderfoxMixerController(self)
        self.device_controller = FaderfoxDeviceController(self)
        self.transport_controller = FaderfoxTransportController(self)
        self.components = [
         self.mixer_controller,
         self.device_controller,
         self.transport_controller]