from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_options import DeviceOnOffOption

class PhaserNewDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        (super(PhaserNewDeviceDecorator, self).__init__)(*a, **k)
        self.mod_sync_option = DeviceOnOffOption(name='Sync',
          property_host=(get_parameter_by_name(self, 'Mod Sync')))
        self.fb_inv_option = DeviceOnOffOption(name='FB Inv',
          property_host=(get_parameter_by_name(self, 'FB Inv')))
        self.spin_option = DeviceOnOffOption(name='Spin',
          property_host=(get_parameter_by_name(self, 'Spin Enabled')))
        self.env_fol_option = DeviceOnOffOption(name='Env Follow',
          property_host=(get_parameter_by_name(self, 'Env Enabled')))
        self.mod_sync2_option = DeviceOnOffOption(name='Sync 2',
          property_host=(get_parameter_by_name(self, 'Mod Sync 2')))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (
         self.mod_sync_option,
         self.fb_inv_option,
         self.spin_option,
         self.env_fol_option,
         self.mod_sync2_option)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters)