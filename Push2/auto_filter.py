#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/auto_filter.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from ableton.v2.base import EventObject, listens, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_decoration import DeviceSwitchOption
from .device_component import DeviceComponentWithTrackColorViewData
from .visualisation_settings import VisualisationGuides

class AutoFilterDeviceDecorator(EventObject, LiveObjectDecorator):

    def __init__(self, *a, **k):
        super(AutoFilterDeviceDecorator, self).__init__(*a, **k)
        self.__on_parameters_changed.subject = self._live_object
        self.slope_option = DeviceSwitchOption(name=u'Slope', parameter=get_parameter_by_name(self, u'Slope'))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.slope_option,)

    @listens(u'parameters')
    def __on_parameters_changed(self):
        self.slope_option.set_parameter(get_parameter_by_name(self, u'Slope'))


class AutoFilterDeviceComponent(DeviceComponentWithTrackColorViewData):

    def _parameter_touched(self, parameter):
        self._update_visualisation_view_data(self._filter_visualisation_data())

    def _parameter_released(self, parameter):
        self._update_visualisation_view_data(self._filter_visualisation_data())

    def parameters_changed(self):
        self._update_visualisation_view_data(self._filter_visualisation_data())

    def _set_bank_index(self, bank):
        super(AutoFilterDeviceComponent, self)._set_bank_index(bank)
        self._update_visualisation_view_data(self._filter_visualisation_data())
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    def _initial_visualisation_view_data(self):
        view_data = super(AutoFilterDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._filter_visualisation_data())
        return view_data

    def _filter_visualisation_data(self):
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        parameter_names = [u'Filter Type',
         u'Filter Type (Legacy)',
         u'Frequency',
         u'Resonance',
         u'Resonance (Legacy)']
        filter_focus = any([ parameter.parameter.name in parameter_names for parameter in touched_parameters if liveobj_valid(parameter.parameter) ])
        return {u'FilterLeft': VisualisationGuides.light_left_x(0),
         u'FilterRight': VisualisationGuides.light_right_x(2),
         u'FilterFocus': filter_focus}

    @listens(u'oscillator_index')
    def __on_selected_oscillator_changed(self):
        self._update_visualisation_view_data(self._filter_visualisation_data())

    @property
    def _visualisation_visible(self):
        return self._bank != None and self._bank.index in (0, 1)

    @property
    def _shrink_parameters(self):
        return [ self._visualisation_visible and index < 3 for index in range(8) ]
