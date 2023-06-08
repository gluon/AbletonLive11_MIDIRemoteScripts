from __future__ import absolute_import, print_function, unicode_literals
import Live
from .FaderfoxDeviceController import FaderfoxDeviceController

class LV2DeviceController(FaderfoxDeviceController):
    __module__ = __name__

    def __init__(self, parent):
        LV2DeviceController.realinit(self, parent)

    def realinit(self, parent):
        FaderfoxDeviceController.realinit(self, parent)