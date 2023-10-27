# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\transmute.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3864 bytes
from __future__ import absolute_import, print_function, unicode_literals
from past.builtins import unicode
from ableton.v2.base import EventObject
from ableton.v2.control_surface import EnumWrappingParameter, IntegerParameter, LiveObjectDecorator
from .device_decoration import DeviceSwitchOption

class TransmuteDeviceDecorator(LiveObjectDecorator, EventObject):
    MIN_PITCH_BEND_RANGE = 0
    MAX_PITCH_BEND_RANGE = 24
    polyphony_values = ('2', '4', '8', '16')

    def __init__(self, *a, **k):
        (super(TransmuteDeviceDecorator, self).__init__)(*a, **k)
        self.frequency_dial_mode_parameter = EnumWrappingParameter(name='Frequency Dial Mode',
          parent=self,
          values_host=(self._live_object),
          index_property_host=(self._live_object),
          values_property='frequency_dial_mode_list',
          index_property='frequency_dial_mode')
        self.midi_gate_parameter = EnumWrappingParameter(name='Midi Gate',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='midi_gate_list',
          index_property='midi_gate')
        self.mod_mode_parameter = EnumWrappingParameter(name='Mod Mode',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='mod_mode_list',
          index_property='mod_mode')
        self.mono_poly_parameter = EnumWrappingParameter(name='Mono Poly',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='mono_poly_list',
          index_property='mono_poly')
        self.pitch_mode_parameter = EnumWrappingParameter(name='Pitch Mode',
          parent=self,
          values_host=(self._live_object),
          index_property_host=self,
          values_property='pitch_mode_list',
          index_property='pitch_mode')
        self.pitch_bend_range_parameter = IntegerParameter(name='Pitch Bend Range',
          parent=self,
          integer_value_host=(self._live_object),
          integer_value_property_name='pitch_bend_range',
          min_value=(self.MIN_PITCH_BEND_RANGE),
          max_value=(self.MAX_PITCH_BEND_RANGE),
          show_as_quantized=False,
          display_value_conversion=(lambda x: unicode(x) + ' st'
))
        self.polyphony_parameter = EnumWrappingParameter(name='Polyphony',
          parent=self,
          values_host=self,
          index_property_host=self,
          values_property='polyphony_values',
          index_property='polyphony')
        self._additional_parameters = (
         self.frequency_dial_mode_parameter,
         self.midi_gate_parameter,
         self.mod_mode_parameter,
         self.mono_poly_parameter,
         self.pitch_mode_parameter,
         self.pitch_bend_range_parameter,
         self.polyphony_parameter)
        self.freq_dial_mode_option = DeviceSwitchOption(name='frequency_dial_mode_opt',
          parameter=(self.frequency_dial_mode_parameter),
          labels=[
         'Hz', 'Note'])
        self.register_disconnectables(self._additional_parameters)
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (
         self.freq_dial_mode_option,)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters