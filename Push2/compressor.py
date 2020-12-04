#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/compressor.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.base import depends, EventObject, listenable_property, listens, liveobj_valid, mixin
from ableton.v2.control_surface import EnumWrappingParameter, LiveObjectDecorator, get_parameter_by_name
from .device_decoration import DeviceOnOffOption
from .device_component import DeviceComponentWithTrackColorViewData
from .routing import InputChannelRouter, InputChannelAndPositionRouter, InputTypeRouter, RoutingChannelList, RoutingChannelPositionList, RoutingMeterRealTimeChannelAssigner, RoutingTypeList
from .visualisation_settings import VisualisationGuides

class CompressorDeviceDecorator(LiveObjectDecorator, EventObject):
    _input_router = None
    _type_list = None
    _channel_list = None
    _position_list = None

    def __init__(self, *a, **k):
        super(CompressorDeviceDecorator, self).__init__(*a, **k)
        for event, func in ((u'input_routing_type', self.notify_input_routing_type_index), (u'input_routing_channel', self.notify_input_routing_channel_index)):
            self.register_slot(event_name=event, subject=self._live_object, listener=func)

        make_option = lambda option_name, parameter_name: DeviceOnOffOption(name=option_name, property_host=get_parameter_by_name(self, parameter_name))
        self._options = tuple([ self.register_disconnectable(make_option(option_name, param_name)) for option_name, param_name in ((u'Auto Release', u'Auto Release On/Off'),
         (u'Makeup', u'Makeup'),
         (u'Listen', u'S/C Listen'),
         (u'Sidechain', u'S/C On')) ])
        make_parameter = lambda name, values, index: EnumWrappingParameter(name=name, parent=self, values_host=self, index_property_host=self, values_property=values, index_property=index)
        self._position_parameter = make_parameter(u'Position', u'input_channel_positions', u'input_channel_position_index')
        self._additional_parameters = self.register_disconnectables((make_parameter(u'Input Type', u'available_input_routing_types', u'input_routing_type_index'), make_parameter(u'Input Channel', u'available_input_routing_channels', u'input_routing_channel_index'), self._position_parameter))

    def set_routing_infrastructure(self, input_router, type_list, channel_list, position_list):
        self._input_router = input_router
        self._type_list = type_list
        self._channel_list = channel_list
        self._position_list = position_list
        self.__on_has_positions_changed.subject = self._input_router
        self.notify_input_routing_type_index()
        self.notify_input_routing_channel_index()
        self.notify_input_channel_position_index()

    def __setattr__(self, attribute, value):
        selector = dict(input_routing_type_index=self._set_input_routing_type_index, input_routing_channel_index=self._set_input_routing_channel_index, input_channel_position_index=self._set_input_channel_position_index).get(attribute, lambda v: super(CompressorDeviceDecorator, self).__setattr__(attribute, v))
        selector(value)

    @property
    def available_input_routing_types(self):
        return tuple([ t.name for t in self._type_list.targets ])

    @listenable_property
    def input_routing_type_index(self):
        return self._type_list.selected_index

    def _set_input_routing_type_index(self, index):
        self._type_list.selected_target = self._type_list.targets[index]

    @listenable_property
    def input_routing_channel_index(self):
        return self._channel_list.selected_index

    def _set_input_routing_channel_index(self, index):
        self._channel_list.selected_target = self._channel_list.targets[index]

    @property
    def available_input_routing_channels(self):
        return tuple([ t.name for t in self._channel_list.targets ] or [u''])

    @listens(u'has_input_channel_position')
    def __on_has_positions_changed(self, has_positions):
        self._position_parameter.is_enabled = has_positions
        self.notify_input_channel_position_index()
        self.notify_input_channel_positions()

    @listenable_property
    def input_channel_position_index(self):
        if self._input_router.has_input_channel_position:
            return self._input_router.input_channel_position_index
        return 0

    def _set_input_channel_position_index(self, index):
        if self._input_router.has_input_channel_position:
            self._input_router.input_channel_position_index = index

    @listenable_property
    def input_channel_positions(self):
        return tuple(self._input_router.input_channel_positions if self._input_router.has_input_channel_position else [u''])

    @property
    def options(self):
        return self._options

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    @property
    def routing_type_list(self):
        return self._type_list

    @property
    def routing_channel_list(self):
        return self._channel_list

    @property
    def routing_channel_position_list(self):
        return self._position_list


class CompressorInputRouterMixin(object):

    class NullRoutingHost(EventObject):

        @listenable_property
        def available_input_routing_types(self):
            return []

        @listenable_property
        def input_routing_type(self):
            return None

        @listenable_property
        def available_input_routing_channels(self):
            return []

        @listenable_property
        def input_routing_channel(self):
            return None

    _compressor = None
    _null_routing_host = NullRoutingHost()
    _registered_listeners = []

    def _get_routing_host(self):
        if liveobj_valid(self._compressor):
            return self._compressor
        return self._null_routing_host

    def set_compressor(self, compressor):
        self._unregister_listeners()
        self._compressor = compressor
        self._register_listeners()
        self.__on_target_changed()
        self.notify_routing_targets()

    def _register_listeners(self):
        self._registered_listeners = [self.register_slot(subject=self._get_routing_host(), event_name=u'available_%ss' % self._current_target_property, listener=self.notify_routing_targets), self.register_slot(subject=self._get_routing_host(), event_name=self._current_target_property, listener=self.__on_target_changed)]

    def _unregister_listeners(self):
        for listener in self._registered_listeners:
            self.unregister_disconnectable(listener)
            listener.disconnect()

        self._registered_listeners = []

    def __on_target_changed(self):
        self.current_target_index = self._current_target_index()
        self.notify_current_target_index(self.current_target_index)


class CompressorDeviceComponent(DeviceComponentWithTrackColorViewData):

    @depends(real_time_mapper=None, register_real_time_data=None)
    def __init__(self, real_time_mapper = None, register_real_time_data = None, *a, **k):
        super(CompressorDeviceComponent, self).__init__(*a, **k)
        self._input_channel_router, self._input_type_router = self.register_disconnectables([mixin(CompressorInputRouterMixin, InputChannelRouter)(song=self.song), mixin(CompressorInputRouterMixin, InputTypeRouter)(song=self.song)])
        self._input_router = self.register_disconnectable(InputChannelAndPositionRouter(input_channel_router=self._input_channel_router, input_type_router=self._input_type_router))
        self._type_list = self.register_disconnectable(RoutingTypeList(parent_task_group=self._tasks, router=self._input_type_router))
        self._channel_list = self.register_disconnectable(RoutingChannelList(parent_task_group=self._tasks, rt_channel_assigner=RoutingMeterRealTimeChannelAssigner(real_time_mapper=real_time_mapper, register_real_time_data=register_real_time_data, parent=self), router=self._input_router))
        self._positions_list = self.register_disconnectable(RoutingChannelPositionList(input_channel_router=self._input_router))

    def _parameter_touched(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter) and parameter.name == u'Threshold':
            self._update_visualisation_view_data({u'AdjustingThreshold': True})

    def _parameter_released(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter) and parameter.name == u'Threshold':
            self._update_visualisation_view_data({u'AdjustingThreshold': False})

    def _set_device_for_subcomponents(self, device):
        super(CompressorDeviceComponent, self)._set_device_for_subcomponents(device)
        self._input_type_router.set_compressor(device)
        self._input_channel_router.set_compressor(device)

    def _set_decorated_device_for_subcomponents(self, decorated_device):
        super(CompressorDeviceComponent, self)._set_decorated_device_for_subcomponents(decorated_device)
        decorated_device.set_routing_infrastructure(self._input_router, self._type_list, self._channel_list, self._positions_list)

    def _set_bank_index(self, bank):
        super(CompressorDeviceComponent, self)._set_bank_index(bank)
        self.notify_visualisation_visible()

    def _initial_visualisation_view_data(self):
        view_data = super(CompressorDeviceComponent, self)._initial_visualisation_view_data()
        view_data[u'AdjustingThreshold'] = False
        view_data[u'VisualisationLeft'] = VisualisationGuides.light_left_x(0)
        view_data[u'VisualisationWidth'] = VisualisationGuides.button_right_x(3) - VisualisationGuides.light_left_x(0)
        return view_data

    @property
    def _visualisation_visible(self):
        return self._bank.index == 0
