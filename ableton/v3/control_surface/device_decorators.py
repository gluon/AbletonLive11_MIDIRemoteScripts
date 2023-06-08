from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import DelayDeviceDecorator
from ableton.v2.control_surface import DeviceDecoratorFactory as DeviceDecoratorFactoryBase
from ableton.v2.control_surface import EnumWrappingParameter, LiveObjectDecorator

class DeviceDecorator(LiveObjectDecorator):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self._additional_parameters = self.get_additional_parameters()
        self.register_disconnectables(self._additional_parameters)

    def get_additional_parameters(self):
        raise NotImplementedError('Must return a tuple of additional parameters for the device')

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters


class TransmuteDeviceDecorator(DeviceDecorator):

    def get_additional_parameters(self):
        return (
         EnumWrappingParameter(name='Hz/Note Mode',
           parent=self,
           values_host=(self._live_object),
           index_property_host=(self._live_object),
           values_property='frequency_dial_mode_list',
           index_property='frequency_dial_mode'),
         EnumWrappingParameter(name='Pitch Mode',
           parent=self,
           values_host=(self._live_object),
           index_property_host=self,
           values_property='pitch_mode_list',
           index_property='pitch_mode'))


class DeviceDecoratorFactory(DeviceDecoratorFactoryBase):
    DECORATOR_CLASSES = {'Delay':DelayDeviceDecorator, 
     'Transmute':TransmuteDeviceDecorator}