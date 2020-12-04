#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/eq8.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import re
from ableton.v2.base import EventObject, liveobj_valid, listens
from ableton.v2.control_surface import BoolWrappingParameter, EnumWrappingParameter, LiveObjectDecorator, get_parameter_by_name
from .device_component import DeviceComponentWithTrackColorViewData
from .device_decoration import DeviceSwitchOption

class Eq8DeviceDecorator(EventObject, LiveObjectDecorator):
    available_band_indices = list(range(1, 9))
    available_global_modes = [u'Stereo', u'Left/Right', u'Mid/Side']

    def __init__(self, *a, **k):
        super(Eq8DeviceDecorator, self).__init__(*a, **k)
        self.band = EnumWrappingParameter(name=u'Band', parent=self, values_host=self, index_property_host=self.view, values_property=u'available_band_indices', index_property=u'selected_band')
        self.mode = EnumWrappingParameter(name=u'Eq Mode', parent=self, values_host=self, index_property_host=self, values_property=u'available_global_modes', index_property=u'global_mode')
        self.edit_switch = BoolWrappingParameter(name=u'Edit Mode', parent=self, property_host=self, source_property=u'edit_mode')
        self.oversampling = BoolWrappingParameter(name=u'Oversampling', parent=self, property_host=self, source_property=u'oversample')
        self.left_right_curve_switch_option = DeviceSwitchOption(name=u'Left/Right', labels=[u'Left', u'Right'], parameter=self.edit_switch)
        self.mid_side_curve_switch_option = DeviceSwitchOption(name=u'Mid/Side', labels=[u'Mid', u'Side'], parameter=self.edit_switch)
        self._additional_parameters = (self.band,
         self.mode,
         self.edit_switch,
         self.oversampling)
        self._additional_options = (self.left_right_curve_switch_option, self.mid_side_curve_switch_option)
        self.register_disconnectables(self._additional_parameters + self._additional_options)
        self.__on_parameters_changed.subject = self

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    @property
    def options(self):
        return self._additional_options

    @listens(u'parameters')
    def __on_parameters_changed(self):
        edit_mode_parameter = get_parameter_by_name(self, u'Edit Mode')
        self.left_right_curve_switch_option.set_parameter(edit_mode_parameter)
        self.mid_side_curve_switch_option.set_parameter(edit_mode_parameter)


class Eq8DeviceComponent(DeviceComponentWithTrackColorViewData):
    FILTER_BAND_PARAMETER_NAMES = re.compile(u'([1-8] [A-z ]+ [A])|(Scale)')

    def _parameter_touched(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            if self.FILTER_BAND_PARAMETER_NAMES.match(parameter.name):
                self._update_visualisation_view_data({u'AdjustingSelectedBand': True})
            elif parameter.name == u'Band':
                self._update_visualisation_view_data({u'ChangingSelectedBand': True})

    def _parameter_released(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            if not self._any_filter_band_parameter_touched():
                self._update_visualisation_view_data({u'AdjustingSelectedBand': False})
            if parameter.name == u'Band':
                self._update_visualisation_view_data({u'ChangingSelectedBand': False})

    def _any_filter_band_parameter_touched(self):
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        return any([ self.FILTER_BAND_PARAMETER_NAMES.match(parameter.name) for parameter in touched_parameters ])

    def _initial_visualisation_view_data(self):
        view_data = super(Eq8DeviceComponent, self)._initial_visualisation_view_data()
        view_data[u'AdjustingSelectedBand'] = False
        view_data[u'ChangingSelectedBand'] = False
        return view_data

    @property
    def _visualisation_visible(self):
        return True

    @property
    def _shrink_parameters(self):
        return [True] * 8
