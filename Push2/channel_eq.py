# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\channel_eq.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 2468 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .visualisation_settings import VisualisationGuides

class ChannelEqDeviceComponent(DeviceComponentWithTrackColorViewData):
    VISUALISATION_POSITION = ButtonRange(1, 6)
    FILTER_PARAMETERS = ['Highpass On','Low','Mid','Mid Freq','High']

    def _parameter_touched(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    def _parameter_released(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    @property
    def _adjustment_view_data(self):
        adjusting_filter = False
        touched_parameters = [self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed]
        for parameter in touched_parameters:
            if parameter.name in self.FILTER_PARAMETERS:
                adjusting_filter = True
                break

        return {'AdjustingFilter': adjusting_filter}

    @property
    def _visualisation_visible(self):
        return True

    @property
    def _shrink_parameters(self):

        def is_shrunk(parameter_index):
            return self.VISUALISATION_POSITION.left_index <= parameter_index <= self.VISUALISATION_POSITION.right_index

        return [is_shrunk(parameter_index) for parameter_index in range(8)]

    @property
    def _get_current_view_data(self):
        position = self.VISUALISATION_POSITION
        start_position_in_px = VisualisationGuides.light_left_x(position.left_index)
        end_position_in_px = VisualisationGuides.light_right_x(position.right_index)
        return {'VisualisationStart':start_position_in_px, 
         'VisualisationWidth':end_position_in_px - start_position_in_px, 
         'AdjustingFilter':False}

    def _initial_visualisation_view_data(self):
        view_data = super(ChannelEqDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._get_current_view_data)
        view_data.update(self._adjustment_view_data)
        return view_data