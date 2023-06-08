from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from ableton.v2.base import EventObject
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .device_options import DeviceOnOffOption, DeviceSwitchOption
from .visualisation_settings import VisualisationGuides

class SubZeroDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        (super(SubZeroDeviceDecorator, self).__init__)(*a, **k)
        self.osc2_Type_option = DeviceSwitchOption(name='Oscillator2 Type',
          parameter=(get_parameter_by_name(self, 'Oscillator2 Type')),
          labels=[
         'Sin','Tri','Sat','Saw','Rec'])
        self.in_osc1on_option = DeviceOnOffOption(name='Osc 1',
          property_host=(get_parameter_by_name(self, 'Oscillator On 1')))
        self.in_osc2on_option = DeviceOnOffOption(name='Osc 2',
          property_host=(get_parameter_by_name(self, 'Oscillator On 2')))
        self.in_osc2reset_option = DeviceOnOffOption(name='Osc Retrig',
          property_host=(get_parameter_by_name(self, 'Global ResetOscillatorPhase')))
        self.in_filOsc1On_option = DeviceOnOffOption(name='Osc 1 Flt',
          property_host=(get_parameter_by_name(self, 'Filter Oscillator Through 1')))
        self.in_filOsc2On_option = DeviceOnOffOption(name='Osc 2 Flt',
          property_host=(get_parameter_by_name(self, 'Filter Oscillator Through 2')))
        self.in_filOsc3On_option = DeviceOnOffOption(name='Filter Noise',
          property_host=(get_parameter_by_name(self, 'Filter Noise Through')))
        self.in_LfoRetrigger_option = DeviceOnOffOption(name='LFO Retrig',
          property_host=(get_parameter_by_name(self, 'Lfo Retrigger')))
        self.in_legatoOn_option = DeviceOnOffOption(name='Legato',
          property_host=(get_parameter_by_name(self, 'Global Legato')))
        self.in_noiseOn_option = DeviceOnOffOption(name='Noise',
          property_host=(get_parameter_by_name(self, 'Noise On')))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (
         self.in_osc1on_option,
         self.osc2_Type_option,
         self.in_osc2on_option,
         self.in_osc2reset_option,
         self.in_filOsc1On_option,
         self.in_filOsc2On_option,
         self.in_filOsc3On_option,
         self.in_LfoRetrigger_option,
         self.in_legatoOn_option,
         self.in_noiseOn_option)