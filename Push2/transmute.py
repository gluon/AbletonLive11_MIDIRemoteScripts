#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/transmute.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from ableton.v2.base import EventObject
from ableton.v2.control_surface import EnumWrappingParameter, IntegerParameter, LiveObjectDecorator, NotifyingList, get_parameter_by_name, WrappingParameter
from .device_decoration import DeviceOnOffOption, DeviceSwitchOption
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .visualisation_settings import VisualisationGuides

class TransmuteDeviceDecorator(LiveObjectDecorator, EventObject):
    MIN_PITCH_BEND_RANGE = 0
    MAX_PITCH_BEND_RANGE = 24
    polyphony_values = (u'2', u'4', u'8', u'16')

    def __init__(self, *a, **k):
        super(TransmuteDeviceDecorator, self).__init__(*a, **k)
        self.frequency_dial_mode = EnumWrappingParameter(name=u'Frequency Dial Mode', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'frequency_dial_mode_list', index_property=u'frequency_dial_mode_index')
        self.midi_gate = EnumWrappingParameter(name=u'Midi Gate', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'midi_gate_list', index_property=u'midi_gate_index')
        self.mod_mode = EnumWrappingParameter(name=u'Mod Mode', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'mod_mode_list', index_property=u'mod_mode_index')
        self.mono_poly = EnumWrappingParameter(name=u'Mono Poly', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'mono_poly_list', index_property=u'mono_poly_index')
        self.pitch_mode = EnumWrappingParameter(name=u'Pitch Mode', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'pitch_mode_list', index_property=u'pitch_mode_index')
        self.pitch_bend_range_parameter = IntegerParameter(name=u'Pitch Bend Range', parent=self, integer_value_host=self._live_object, integer_value_property_name=u'pitch_bend_range', min_value=self.MIN_PITCH_BEND_RANGE, max_value=self.MAX_PITCH_BEND_RANGE, show_as_quantized=False)
        self.polyphony_parameter = EnumWrappingParameter(name=u'Polyphony', parent=self, values_host=self, index_property_host=self, values_property=u'polyphony_values', index_property=u'polyphony')
        self._additional_parameters = (self.frequency_dial_mode,
         self.midi_gate,
         self.mod_mode,
         self.mono_poly,
         self.pitch_mode,
         self.pitch_bend_range_parameter,
         self.polyphony_parameter)
        self.freq_dial_mode_option = DeviceSwitchOption(name=u'frequency_dial_mode_opt', parameter=self.frequency_dial_mode, labels=[u'Hz', u'Note'])
        self.register_disconnectables(self._additional_parameters)
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.freq_dial_mode_option,)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters
