from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .device_options import DeviceOnOffOption
from .visualisation_settings import VisualisationGuides

class CorpusDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        (super(CorpusDeviceDecorator, self).__init__)(*a, **k)
        self.note_off_option = DeviceOnOffOption(name='Off Decay',
          property_host=(get_parameter_by_name(self, 'Note Off')))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (
         self.note_off_option,)


class CorpusDeviceComponent(DeviceComponentWithTrackColorViewData):
    FILTER_BANK = 4
    VISUALISATION_POSITION_IN_BANKS = {FILTER_BANK: ButtonRange(1, 2)}

    def _parameter_touched(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    def _parameter_released(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    @property
    def _adjustment_view_data(self):
        touched_parameters = (self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed)
        adjusting_filter = any((p.name in ('Frequency', 'Bandwidth') for p in touched_parameters))
        return {'AdjustingFilter': adjusting_filter}

    @property
    def _visualisation_visible(self):
        return self._bank.index in self.VISUALISATION_POSITION_IN_BANKS

    @property
    def _shrink_parameters(self):
        if self.visualisation_visible:
            visualisation_position = self._get_current_visualisation_position()

            def is_shrunk(parameter_index):
                return visualisation_position.left_index <= parameter_index <= visualisation_position.right_index

            return [is_shrunk(parameter_index) for parameter_index in range(8)]
        return [False] * 8

    def _set_bank_index(self, bank):
        super(CorpusDeviceComponent, self)._set_bank_index(bank)
        self._update_visualisation_view_data(self._get_current_view_data)
        self._update_visualisation_view_data(self._adjustment_view_data)
        self.notify_shrink_parameters()
        self.notify_visualisation_visible()

    def _get_current_visualisation_position(self):
        return self.VISUALISATION_POSITION_IN_BANKS.get(self._bank.index, ButtonRange(0, 0))

    @property
    def _get_current_view_data(self):
        position = self._get_current_visualisation_position()
        start_position_in_px = VisualisationGuides.light_left_x(position.left_index)
        end_position_in_px = VisualisationGuides.light_right_x(position.right_index)
        return {'FilterLeft':start_position_in_px, 
         'FilterRight':end_position_in_px, 
         'IsVisualisationVisible':self._visualisation_visible}

    def _initial_visualisation_view_data(self):
        view_data = super(CorpusDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._get_current_view_data)
        view_data.update(self._adjustment_view_data)
        return view_data