#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/echo.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from ableton.v2.base import EventObject
from ableton.v2.control_surface import EnumWrappingParameter, LiveObjectDecorator, NotifyingList, get_parameter_by_name
from .device_decoration import DeviceOnOffOption, DeviceSwitchOption
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .visualisation_settings import VisualisationGuides

class EchoDeviceDecorator(LiveObjectDecorator, EventObject):

    class EchoChannelName(int):
        pass

    EchoChannelName.left = EchoChannelName(0)
    EchoChannelName.right = EchoChannelName(1)

    def __init__(self, *a, **k):
        super(EchoDeviceDecorator, self).__init__(*a, **k)
        self._channel_names_provider = NotifyingList(available_values=[u'Left', u'Right'], default_value=EchoDeviceDecorator.EchoChannelName.left)
        self.channel_switch_parameter = EnumWrappingParameter(name=u'Channel Toggle', parent=self, values_host=self._channel_names_provider, index_property_host=self._channel_names_provider, values_property=u'available_values', index_property=u'index', value_type=EchoDeviceDecorator.EchoChannelName)
        self._additional_parameters = (self.channel_switch_parameter,)
        self.link_option = DeviceOnOffOption(name=u'Link', property_host=get_parameter_by_name(self, u'Link'))
        self.sync_l_option = DeviceOnOffOption(name=u'L Sync', property_host=get_parameter_by_name(self, u'L Sync'))
        self.sync_r_option = DeviceOnOffOption(name=u'R Sync', property_host=get_parameter_by_name(self, u'R Sync'))
        self.sync_m_option = DeviceOnOffOption(name=u'M Sync', property_host=get_parameter_by_name(self, u'L Sync'))
        self.sync_s_option = DeviceOnOffOption(name=u'S Sync', property_host=get_parameter_by_name(self, u'R Sync'))
        self.clip_dry_option = DeviceOnOffOption(name=u'Clip Dry', property_host=get_parameter_by_name(self, u'Clip Dry'))
        self.filter_on_option = DeviceOnOffOption(name=u'Filter', property_host=get_parameter_by_name(self, u'Filter On'))
        self.feedback_inv_option = DeviceOnOffOption(name=u'Invert', property_host=get_parameter_by_name(self, u'Feedback Inv'))
        self.modulation_times_four_option = DeviceOnOffOption(name=u'Mod 4x', property_host=get_parameter_by_name(self, u'Mod 4x'))
        self.reverb_loc_option = DeviceSwitchOption(name=u'Reverb Loc', parameter=get_parameter_by_name(self, u'Reverb Loc'))
        self.duck_option = DeviceOnOffOption(name=u'Duck', property_host=get_parameter_by_name(self, u'Duck On'))
        self.gate_option = DeviceOnOffOption(name=u'Gate', property_host=get_parameter_by_name(self, u'Gate On'))
        self.wobble_option = DeviceOnOffOption(name=u'Wobble', property_host=get_parameter_by_name(self, u'Wobble On'))
        self.noise_option = DeviceOnOffOption(name=u'Noise', property_host=get_parameter_by_name(self, u'Noise On'))
        self.channel_switch_lr_option = DeviceSwitchOption(name=u'L/R Switch', parameter=self.channel_switch_parameter, labels=[u'Left', u'Right'])
        self.channel_switch_ms_option = DeviceSwitchOption(name=u'M/S Switch', parameter=self.channel_switch_parameter, labels=[u'Mid', u'Side'])
        self.register_disconnectables(self._additional_parameters)
        self.register_disconnectables(self.options)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    @property
    def options(self):
        return (self.channel_switch_lr_option,
         self.channel_switch_ms_option,
         self.link_option,
         self.sync_l_option,
         self.sync_r_option,
         self.sync_m_option,
         self.sync_s_option,
         self.clip_dry_option,
         self.filter_on_option,
         self.feedback_inv_option,
         self.modulation_times_four_option,
         self.reverb_loc_option,
         self.duck_option,
         self.gate_option,
         self.wobble_option,
         self.noise_option)


class EchoDeviceComponent(DeviceComponentWithTrackColorViewData):
    TUNNEL_VISUALISATION_CONFIGURATION_IN_BANKS = {0: ButtonRange(0, 3),
     1: ButtonRange(2, 5)}
    FILTER_VISUALISATION_CONFIGURATION_IN_BANKS = {0: ButtonRange(4, 5),
     3: ButtonRange(1, 4)}
    LFO_VISUALISATION_CONFIGURATION_IN_BANKS = {4: ButtonRange(0, 3)}

    def _parameter_touched(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    def _parameter_released(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    @property
    def _adjustment_view_data(self):
        is_linked = bool(get_parameter_by_name(self.device(), u'Link').value)
        adjusting_tunnel_left = adjusting_tunnel_right = False
        adjusting_filter_hp = adjusting_filter_lp = False
        adjusting_lfo = adjusting_lfo_phase = False
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        for parameter in touched_parameters:
            if parameter.name == u'Feedback':
                adjusting_tunnel_left = adjusting_tunnel_right = True
            elif parameter.name.startswith(u'L '):
                adjusting_tunnel_left = True
                if parameter.name != u'L Offset' and is_linked:
                    adjusting_tunnel_right = True
            elif parameter.name == u'R Offset' or parameter.name.startswith(u'R ') and not is_linked:
                adjusting_tunnel_right = True
            elif parameter.name in (u'HP Freq', u'HP Res'):
                adjusting_filter_hp = True
            elif parameter.name in (u'LP Freq', u'LP Res'):
                adjusting_filter_lp = True
            elif parameter.name == u'Mod Phase':
                adjusting_lfo_phase = True
            elif parameter.name.startswith(u'Mod '):
                adjusting_lfo = True

        return {u'AdjustingTunnelLeft': adjusting_tunnel_left,
         u'AdjustingTunnelRight': adjusting_tunnel_right,
         u'AdjustingFilterHighPass': adjusting_filter_hp,
         u'AdjustingFilterLowPass': adjusting_filter_lp,
         u'AdjustingLfo': adjusting_lfo,
         u'AdjustingLfoPhase': adjusting_lfo_phase}

    def _set_bank_index(self, bank):
        super(EchoDeviceComponent, self)._set_bank_index(bank)
        self._update_visualisation_view_data(self._configuration_view_data)
        self._update_visualisation_view_data(self._adjustment_view_data)
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    @property
    def _visualisation_visible(self):
        return self._bank.index in self.TUNNEL_VISUALISATION_CONFIGURATION_IN_BANKS or self._bank.index in self.FILTER_VISUALISATION_CONFIGURATION_IN_BANKS or self._bank.index in self.LFO_VISUALISATION_CONFIGURATION_IN_BANKS

    @property
    def _shrink_parameters(self):
        if self._visualisation_visible:
            tunnel_config = self.TUNNEL_VISUALISATION_CONFIGURATION_IN_BANKS.get(self._bank.index, ButtonRange(-1, -1))
            filter_config = self.FILTER_VISUALISATION_CONFIGURATION_IN_BANKS.get(self._bank.index, ButtonRange(-1, -1))
            lfo_config = self.LFO_VISUALISATION_CONFIGURATION_IN_BANKS.get(self._bank.index, ButtonRange(-1, -1))
            return [ tunnel_config.left_index <= index <= tunnel_config.right_index or filter_config.left_index <= index <= filter_config.right_index or lfo_config.left_index <= index <= lfo_config.right_index for index in range(8) ]
        else:
            return [False] * 8

    @property
    def _configuration_view_data(self):
        tunnel_left, tunnel_right = self._calculate_view_size(self.TUNNEL_VISUALISATION_CONFIGURATION_IN_BANKS)
        filter_left, filter_right = self._calculate_view_size(self.FILTER_VISUALISATION_CONFIGURATION_IN_BANKS)
        lfo_left, lfo_right = self._calculate_view_size(self.LFO_VISUALISATION_CONFIGURATION_IN_BANKS)
        return {u'TunnelLeft': tunnel_left,
         u'TunnelRight': tunnel_right,
         u'FilterLeft': filter_left,
         u'FilterRight': filter_right,
         u'LfoLeft': lfo_left,
         u'LfoRight': lfo_right}

    def _initial_visualisation_view_data(self):
        view_data = super(EchoDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._configuration_view_data)
        view_data.update(self._adjustment_view_data)
        return view_data

    def _calculate_view_size(self, configuration):
        if self._bank.index not in configuration:
            return (0, 0)
        config = configuration[self._bank.index]
        return (VisualisationGuides.light_left_x(config.left_index), VisualisationGuides.light_right_x(config.right_index))
