# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\routing.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 42163 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import filter, map, range
from functools import partial
import Live
from ableton.v2.base import EventObject, MultiSlot, const, depends, find_if, listenable_property, listens, listens_group, liveobj_valid, nop, old_hasattr, task
from ableton.v2.base.util import index_if
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ListIndexEncoderControl, ListValueEncoderControl, control_list
from ableton.v2.control_surface.mode import ModesComponent, SetAttributeMode
from pushbase.song_utils import is_return_track
from .mixable_utilities import is_chain
from .real_time_channel import RealTimeDataComponent
MASTER_OUTPUT_TARGET_ID = 'Master'
NO_INPUT_TARGET_ID = 'No Input'
AUDIO_CHANNEL_POSITION_POSTFIXES = [
 'Pre FX', 'Post FX', 'Post Mixer']
MIDI_CHANNEL_POSITION_POSTFIXES = AUDIO_CHANNEL_POSITION_POSTFIXES[:2]

class RoutingMeterRealTimeChannelAssigner(Component):
    list_index_to_pool_index_mapping = listenable_property.managed({})

    def __init__(self, real_time_mapper=None, register_real_time_data=nop, sliding_window_size=None, *a, **k):
        (super(RoutingMeterRealTimeChannelAssigner, self).__init__)(*a, **k)
        if sliding_window_size is None:
            sliding_window_size = real_time_mapper.METER_POOLSIZE
        self._half_window_size = sliding_window_size // 2
        self._routing_channels = []
        self._selected_index = -1
        self.real_time_channels = [RealTimeDataComponent(parent=self, channel_type='meter', real_time_mapper=real_time_mapper, register_real_time_data=register_real_time_data) for _ in range(sliding_window_size)]

    def disconnect(self):
        super(RoutingMeterRealTimeChannelAssigner, self).disconnect()
        self._routing_channels = []

    @property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, index):
        self._selected_index = index
        self._update_attachments()

    @property
    def routing_channels(self):
        return self._routing_channels

    @routing_channels.setter
    def routing_channels(self, channels):
        self._routing_channels = channels
        for rt in self.real_time_channels:
            rt.set_data(None)

        self.list_index_to_pool_index_mapping = {}
        self._update_attachments()

    def _update_attachments(self):
        visible_routing_channels = set(self._visible_routing_channels())
        attached_routing_channels = set(self._attached_routing_channels())
        to_be_detached = attached_routing_channels - visible_routing_channels
        to_be_attached = visible_routing_channels - attached_routing_channels
        for routing_channel in to_be_detached:
            rt_assignment = find_if(lambda rt: rt.attached_object == routing_channel
, self.real_time_channels)
            rt_assignment.set_data(None)

        for routing_channel in to_be_attached:
            free_channel = find_if(lambda rt: rt.attached_object is None
, self.real_time_channels)
            free_channel.set_data(routing_channel)

        self._update_list_index_to_pool_index_mapping()

    def _visible_routing_channels(self):
        window_start = max(0, self._selected_index - self._half_window_size)
        window_end = self._selected_index + self._half_window_size + 1
        return self._routing_channels[window_start:window_end]

    def _attached_routing_channels(self):
        return list(filter(liveobj_valid, map(lambda real_time_assignment: real_time_assignment.attached_object
, self.real_time_channels)))

    def _update_list_index_to_pool_index_mapping(self):
        new_mapping = {}
        for index, rt_assignment in enumerate(self.real_time_channels):
            if liveobj_valid(rt_assignment.attached_object):
                list_index = self._routing_channels.index(rt_assignment.attached_object)
                new_mapping[list_index] = index

        self.list_index_to_pool_index_mapping = new_mapping


class TrackOrRoutingControlChooserComponent(ModesComponent):

    def __init__(self, tracks_provider=None, track_mixer_component=None, routing_control_component=None, *a, **k):
        (super(TrackOrRoutingControlChooserComponent, self).__init__)(*a, **k)
        self._tracks_provider = tracks_provider
        self._track_mixer = track_mixer_component
        self._routing_control = routing_control_component
        self.add_mode('mix', track_mixer_component)
        self.add_mode('routing', routing_control_component)
        self.selected_mode = 'mix'
        for mode in ('mix', 'routing'):
            button = self.get_mode_button(mode)
            button.mode_selected_color = 'MixOrRoutingChooser.ModeActive'
            button.mode_unselected_color = 'MixOrRoutingChooser.ModeInactive'

        self._routing_previously_available = False
        self._update_buttons(False)
        self._TrackOrRoutingControlChooserComponent__on_selected_item_changed.subject = self._tracks_provider
        self._TrackOrRoutingControlChooserComponent__on_selected_item_changed()

    @property
    def track_mix(self):
        return self._track_mixer

    @property
    def routing(self):
        return self._routing_control

    @listenable_property
    def routing_mode_available(self):
        return self._can_enable_routing_mode()

    def update(self):
        super(TrackOrRoutingControlChooserComponent, self).update()
        if self.is_enabled():
            self._update_routing_mode_availability()

    @listens('selected_item')
    def __on_selected_item_changed(self):
        if self.is_enabled():
            self._update_routing_mode_availability()

    def _update_routing_mode_availability(self):
        is_available = self._can_enable_routing_mode()
        if is_available != self._routing_previously_available:
            self._update_buttons(enable_buttons=is_available)
            if is_available and 'routing' in self.active_modes:
                self.pop_mode('mix')
            else:
                self.push_mode('mix')
            self.notify_routing_mode_available()
            self._routing_previously_available = is_available

    def _can_enable_routing_mode(self):
        return not is_chain(self._tracks_provider.selected_item)

    def _update_buttons(self, enable_buttons):
        for mode in ('mix', 'routing'):
            self.get_mode_button(mode).enabled = enable_buttons


def reorder_routing_targets(targets, desired_first_target_display_name):
    targets = list(targets)
    index_of_desired_first_target = None
    index_of_desired_first_target = index_if(lambda target: target.display_name == desired_first_target_display_name
, targets)
    if index_of_desired_first_target >= 0:
        if index_of_desired_first_target < len(targets):
            return [
             targets[index_of_desired_first_target]] + targets[:index_of_desired_first_target] + targets[index_of_desired_first_target + 1:]
    return targets


class Router(EventObject):
    current_target_index = listenable_property.managed(-1)

    def __init__(self, routing_level=None, routing_direction=None, song=None, *a, **k):
        (super(Router, self).__init__)(*a, **k)
        self._song = song
        self._current_target_property = '%s_routing_%s' % (
         routing_direction,
         routing_level)
        self._register_listeners()
        self.current_target_index = self._current_target_index()

    def _register_listeners(self):
        self.register_slot(MultiSlot(subject=(self._song.view),
          event_name_list=(
         'selected_track', self._current_target_property),
          listener=(self._Router__on_current_routing_changed)))
        self.register_slot(MultiSlot(subject=(self._song.view),
          event_name_list=(
         'selected_track',
         'available_%ss' % self._current_target_property),
          listener=(self._Router__on_routings_changed)))

    @listenable_property
    def routing_targets(self):
        return self._get_targets()

    def _current_target_index(self):
        try:
            return self._get_targets().index(self._get_current_target())
        except ValueError:
            return -1

    @property
    def current_target(self):
        return self._get_current_target()

    @current_target.setter
    def current_target(self, new_target):
        self._set_current_target(new_target)

    def __on_current_routing_changed(self):
        self.current_target_index = self._current_target_index()

    def __on_routings_changed(self):
        self.notify_routing_targets()

    def _get_routing_host(self):
        return self._song.view.selected_track

    def _get_targets(self):
        raise NotImplementedError

    def _get_current_target(self):
        return getattr(self._get_routing_host(), self._current_target_property)

    def _set_current_target(self, new_target_id):
        setattr(self._get_routing_host(), self._current_target_property, new_target_id)

    @listenable_property
    def has_input_channel_position(self):
        return False


class InputTypeRouter(Router):

    def __init__(self, *a, **k):
        (super(InputTypeRouter, self).__init__)(a, routing_direction='input', routing_level='type', **k)

    def _get_targets(self):
        return reorder_routing_targets(self._get_routing_host().available_input_routing_types, NO_INPUT_TARGET_ID)


class OutputTypeRouter(Router):

    def __init__(self, *a, **k):
        (super(OutputTypeRouter, self).__init__)(a, routing_direction='output', routing_level='type', **k)

    def _get_targets(self):
        return reorder_routing_targets(self._get_routing_host().available_output_routing_types, MASTER_OUTPUT_TARGET_ID)


class InputChannelRouter(Router):

    def __init__(self, *a, **k):
        (super(InputChannelRouter, self).__init__)(a, routing_direction='input', routing_level='channel', **k)

    def _get_targets(self):
        return list(self._get_routing_host().available_input_routing_channels)


def _target_has_postfix(target_and_postfix):
    target, postfix = target_and_postfix
    return target.display_name.endswith(postfix)


def can_combine_targets(targets, postfixes):
    if len(targets) == len(postfixes):
        if all(map(_target_has_postfix, zip(targets, postfixes))):
            first_name = targets[0].display_name
            common_prefix = first_name[:first_name.rfind(postfixes[0])]
            return all(map(lambda t: t.display_name.startswith(common_prefix)
, targets))
    return False


def targets_can_be_grouped(targets, postfixes):
    if len(targets) > 0:
        num_postfixes = len(postfixes)
        while can_combine_targets(targets[:num_postfixes], postfixes):
            targets = targets[num_postfixes:]

        return len(targets) == 0
    return False


class InputChannelAndPositionRouter(EventObject):
    has_input_channel_position = listenable_property.managed(False)

    def __init__(self, input_channel_router=None, input_type_router=None, *a, **k):
        (super(InputChannelAndPositionRouter, self).__init__)(*a, **k)
        self._input_type_router = input_type_router
        self._input_channel_router = input_channel_router
        self._input_channel_postfixes = []
        self._update_channel_grouping()
        if self.has_input_channel_position:
            self._last_input_channel_position_index = self.input_channel_position_index
        else:
            self._last_input_channel_position_index = None
        self._InputChannelAndPositionRouter__on_routing_targets_changed.subject = input_channel_router
        self._InputChannelAndPositionRouter__on_current_target_index_changed.subject = input_channel_router
        self._InputChannelAndPositionRouter__on_input_type_changed.subject = input_type_router

    @listens('current_target_index')
    def __on_input_type_changed(self, _):
        self._update_channel_grouping()
        self.notify_routing_targets()
        self.notify_input_channel_position_index()

    @listens('routing_targets')
    def __on_routing_targets_changed(self):
        self._update_channel_grouping()
        self.notify_routing_targets()

    @listens('current_target_index')
    def __on_current_target_index_changed(self, _):
        if self.has_input_channel_position:
            if self._last_input_channel_position_index != self.input_channel_position_index:
                self.notify_input_channel_position_index()
                self._last_input_channel_position_index = self.input_channel_position_index
        self.notify_current_target_index()

    @listenable_property
    def routing_targets(self):
        complete_list = self._input_channel_router.routing_targets
        if self.has_input_channel_position:
            slice_size = len(self.live_position_postfixes)
            index_in_complete_list = self._input_channel_router.current_target_index
            return complete_list[index_in_complete_list % slice_size::slice_size]
        return complete_list

    @listenable_property
    def current_target_index(self):
        index_in_complete_list = self._input_channel_router.current_target_index
        if self.has_input_channel_position:
            slice_size = len(self.live_position_postfixes)
            return index_in_complete_list // slice_size
        return index_in_complete_list

    @listenable_property
    def current_target(self):
        return self._input_channel_router.current_target

    @current_target.setter
    def current_target(self, new_target):
        self._input_channel_router.current_target = new_target

    @listenable_property
    def input_channel_positions(self):
        return self.live_position_postfixes

    @property
    def live_position_postfixes(self):
        return self._input_channel_postfixes

    @listenable_property
    def input_channel_position_index(self):
        slice_size = len(self.live_position_postfixes)
        return self._input_channel_router.current_target_index % slice_size

    @input_channel_position_index.setter
    def input_channel_position_index(self, new_index):
        complete_list = self._input_channel_router.routing_targets
        index_in_complete_list = self._input_channel_router.current_target_index
        slice_size = len(self.live_position_postfixes)
        self._input_channel_router.current_target = complete_list[index_in_complete_list // slice_size * slice_size + new_index]

    @property
    def input_type_name(self):
        current_target = self._input_type_router.current_target
        if current_target:
            return getattr(current_target.attached_object, 'name', '')
        return ''

    def _update_channel_grouping(self):
        attached_object = getattr(self._input_type_router.current_target, 'attached_object', None)
        original_channels = self._input_channel_router.routing_targets
        if can_combine_targets(original_channels[:len(AUDIO_CHANNEL_POSITION_POSTFIXES)], AUDIO_CHANNEL_POSITION_POSTFIXES):
            postfixes = AUDIO_CHANNEL_POSITION_POSTFIXES
        else:
            postfixes = MIDI_CHANNEL_POSITION_POSTFIXES
        has_positions = liveobj_valid(attached_object) and targets_can_be_grouped(original_channels, postfixes)
        self._input_channel_postfixes = postfixes if has_positions else []
        self.has_input_channel_position = has_positions
        self.notify_input_channel_positions()


class OutputChannelRouter(Router):

    def __init__(self, *a, **k):
        (super(OutputChannelRouter, self).__init__)(a, routing_direction='output', routing_level='channel', **k)

    def _get_targets(self):
        return list(self._get_routing_host().available_output_routing_channels)


class RoutingTarget(EventObject):

    def __init__(self, live_target, name=None, *a, **k):
        (super(RoutingTarget, self).__init__)(*a, **k)
        self._live_target = live_target
        self._name = name if name is not None else live_target.display_name

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        return other is not None and self._live_target == getattr(other, '_live_target', None)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._live_target)

    @property
    def __id__(self):
        return hash(self)

    def __repr__(self):
        return '<%s name=%s>' % (self.__class__.__name__, self._name)


class RoutingChannel(RoutingTarget):
    realtime_channel = listenable_property.managed(None)

    def __init__(self, realtime_channel=None, *a, **k):
        (super(RoutingChannel, self).__init__)(*a, **k)
        self.realtime_channel = realtime_channel
        self._layout_names = {Live.Track.RoutingChannelLayout.mono: 'mono', 
         Live.Track.RoutingChannelLayout.midi: 'midi', 
         Live.Track.RoutingChannelLayout.stereo: 'stereo'}

    @property
    def layout(self):
        return self._layout_names[self._live_target.layout]


class RoutingTargetList(EventObject):
    APPLY_SELECTION_DELAY = 0.2

    def __init__(self, router=None, parent_task_group=None, *a, **k):
        (super(RoutingTargetList, self).__init__)(*a, **k)
        self._router = router
        self._targets = []
        self._selected_target = None
        self._apply_selection_task = parent_task_group.add(task.sequence(task.wait(self.APPLY_SELECTION_DELAY), task.run(self._apply_selected_target)))
        self._RoutingTargetList__on_current_target_index_changed.subject = router
        self._RoutingTargetList__on_routing_targets_changed.subject = router
        self._update_targets()
        self._update_selected_target()

    def disconnect(self):
        super(RoutingTargetList, self).disconnect()
        self._targets = []
        self._selected_target = None

    @listenable_property
    def targets(self):
        return self._targets

    @listenable_property
    def selected_target(self):
        return self._selected_target

    @selected_target.setter
    def selected_target(self, value):
        if self._selected_target != value:
            self._set_selected_target(value)
            self._apply_selection_task.restart()

    @listenable_property
    def selected_index(self):
        if self._selected_target is not None:
            return self._targets.index(self._selected_target)
        return -1

    @listens('routing_targets')
    def __on_routing_targets_changed(self):
        self._update_targets()

    @listens('current_target_index')
    def __on_current_target_index_changed(self, *a):
        self._update_selected_target()

    def _set_selected_target(self, target):
        if self._selected_target != target:
            self._selected_target = target
            self.notify_selected_target()
            self.notify_selected_index()

    def _update_selected_target(self):
        self._apply_selection_task.kill()
        index = self._router.current_target_index
        if 0<= index < len(self._targets):
            new_target = self._targets[index]
        else:
            new_target = None
        self._set_selected_target(new_target)

    def _update_targets(self):
        targets = self._make_targets()
        if targets != self._targets:
            self._targets = self.register_disconnectables(targets)
            self.notify_targets()
            self._update_selected_target()

    def _apply_selected_target(self):
        if self._selected_target is not None:
            index = self._targets.index(self._selected_target)
            self._router.current_target = self._router.routing_targets[index]
        else:
            pass

    def _make_targets(self):
        raise NotImplementedError


class RoutingTypeList(RoutingTargetList):

    def __init__(self, *a, **k):
        (super(RoutingTypeList, self).__init__)(*a, **k)
        self._RoutingTypeList__on_routing_targets_changed.subject = self._router
        self._RoutingTypeList__on_current_target_index_changed.subject = self._router

    @listenable_property
    def selected_track(self):
        if self.selected_index < 0:
            return
        attached_object = self._router.routing_targets[self.selected_index].attached_object
        if isinstance(attached_object, Live.Track.Track):
            return attached_object

    @listens('routing_targets')
    def __on_routing_targets_changed(self):
        self.notify_selected_track()

    @listens('current_target_index')
    def __on_current_target_index_changed(self, *a):
        self.notify_selected_track()

    def _make_targets(self):
        return list(map(RoutingTarget, self._router.routing_targets))


class RoutingChannelList(RoutingTargetList):

    def __init__(self, rt_channel_assigner=None, router=None, *a, **k):
        self._rt_channel_assigner = rt_channel_assigner
        self._rt_channel_assigner.routing_channels = router.routing_targets
        self._rt_channel_assigner.selected_index = router.current_target_index
        (super(RoutingChannelList, self).__init__)(a, router=router, **k)
        self._RoutingChannelList__on_selected_index_changed.subject = self
        self._RoutingChannelList__on_list_index_to_pool_index_mapping_changed.subject = self._rt_channel_assigner
        self._RoutingChannelList__on_routing_targets_changed.subject = router

    def _make_targets(self):
        targets = self._router.routing_targets
        name_transform = nop
        if self._router.has_input_channel_position:
            live_position_names = self._router.live_position_postfixes
            position_name = live_position_names[self._router.input_channel_position_index]
            strip_length = len(position_name) + 3

            def stripped_name(target_name):
                if len(target_name) > strip_length:
                    return target_name[:-strip_length]
                return self._router.input_type_name

            name_transform = stripped_name
        return [RoutingChannel(live_target=target, name=(name_transform(target.display_name)), realtime_channel=(self._get_realtime_channel(list_index))) for list_index, target in enumerate(targets)]

    def _get_realtime_channel(self, list_index):
        mapping = self._rt_channel_assigner.list_index_to_pool_index_mapping
        if list_index in mapping:
            pool_index = mapping[list_index]
            return self._rt_channel_assigner.real_time_channels[pool_index]

    @listens('routing_targets')
    def __on_routing_targets_changed(self):
        self._rt_channel_assigner.routing_channels = self._router.routing_targets

    @listens('selected_index')
    def __on_selected_index_changed(self, *a):
        self._rt_channel_assigner.selected_index = self.selected_index

    @listens('list_index_to_pool_index_mapping')
    def __on_list_index_to_pool_index_mapping_changed(self, *a):
        self._reassign_realtime_channels()

    def _reassign_realtime_channels(self):
        for list_index, routing_channel in enumerate(self._targets):
            routing_channel.realtime_channel = self._get_realtime_channel(list_index)


class RoutingChannelPositionList(EventObject):

    def __init__(self, input_channel_router=None, *a, **k):
        (super(RoutingChannelPositionList, self).__init__)(*a, **k)
        self._input_channel_router = input_channel_router
        self._targets = []
        self._RoutingChannelPositionList__on_input_channel_position_index_changed.subject = input_channel_router
        self._RoutingChannelPositionList__on_input_channel_positions_changed.subject = input_channel_router
        self._RoutingChannelPositionList__on_has_input_channel_position_changed.subject = input_channel_router
        self._update_targets()

    @listenable_property
    def targets(self):
        return self._targets

    @listenable_property
    def selected_index(self):
        if not self._input_channel_router.has_input_channel_position:
            return -1
        return self._input_channel_router.input_channel_position_index

    @listens('has_input_channel_position')
    def __on_has_input_channel_position_changed(self, _):
        self._update_targets()
        self.notify_selected_index()

    @listens('input_channel_positions')
    def __on_input_channel_positions_changed(self):
        self._update_targets()

    @listens('input_channel_position_index')
    def __on_input_channel_position_index_changed(self):
        self.notify_selected_index()

    def _update_targets(self):
        original_targets = self._targets
        if not self._input_channel_router.has_input_channel_position:
            self._targets = []
        else:
            self._targets = self._input_channel_router.input_channel_positions
        if self._targets != original_targets:
            self.notify_targets()


def can_set_input_routing(track, song):
    return not is_return_track(song, track) and not track.is_frozen and not track.is_foldable


class RoutingControlComponent(ModesComponent):
    monitor_state_encoder = ListValueEncoderControl(num_steps=10)
    input_output_choice_encoder = ListValueEncoderControl(num_steps=10)
    routing_type_encoder = ListValueEncoderControl(num_steps=10)
    routing_channel_encoders = control_list(ListValueEncoderControl,
      control_count=4, num_steps=10)
    routing_channel_position_encoder = ListIndexEncoderControl(num_steps=10)
    can_route = listenable_property.managed(False)

    @depends(real_time_mapper=None, register_real_time_data=(const(nop)))
    def __init__(self, real_time_mapper=None, register_real_time_data=None, *a, **k):
        (super(RoutingControlComponent, self).__init__)(*a, **k)
        self._RoutingControlComponent__on_current_monitoring_state_changed.subject = self.song.view
        self._real_time_channel_assigner = RoutingMeterRealTimeChannelAssigner(real_time_mapper=real_time_mapper,
          register_real_time_data=register_real_time_data,
          is_enabled=False)
        self._update_monitoring_state_task = self._tasks.add(task.run(self._update_monitoring_state))
        input_type_router = self.register_disconnectable(InputTypeRouter(song=(self.song)))
        output_type_router = self.register_disconnectable(OutputTypeRouter(song=(self.song)))
        input_channel_router = self.register_disconnectable(InputChannelRouter(song=(self.song)))
        output_channel_router = self.register_disconnectable(OutputChannelRouter(song=(self.song)))
        input_channel_and_position_router = self.register_disconnectable(InputChannelAndPositionRouter(input_channel_router, input_type_router))
        self._active_type_router = input_type_router
        self._active_channel_router = input_channel_and_position_router
        self._can_route = can_set_input_routing
        self._update_can_route()
        self._routing_type_list, self._routing_channel_list = self.register_disconnectables([
         RoutingTypeList(parent_task_group=(self._tasks),
           router=(self._active_type_router)),
         RoutingChannelList(parent_task_group=(self._tasks),
           rt_channel_assigner=(self._real_time_channel_assigner),
           router=(self._active_channel_router))])
        self._RoutingControlComponent__on_input_channel_position_index_changed.subject = input_channel_and_position_router
        self._routing_channel_position_list = None
        self._update_routing_channel_position_list()
        self.add_mode('input', [
         SetAttributeMode(self, '_can_route', can_set_input_routing),
         partial(self._set_active_routers, input_type_router, input_channel_and_position_router),
         self._real_time_channel_assigner])
        self.add_mode('output', [
         SetAttributeMode(self, '_can_route', lambda *a: True
),
         partial(self._set_active_routers, output_type_router, output_channel_router),
         self._real_time_channel_assigner])
        self.selected_mode = 'input'
        self._RoutingControlComponent__on_selected_track_changed.subject = self.song.view
        self._RoutingControlComponent__on_selected_track_changed()
        self._connect_monitoring_state_encoder()
        self.input_output_choice_encoder.connect_static_list(self,
          'selected_mode', list_values=['input', 'output'])
        self._RoutingControlComponent__on_selected_mode_changed.subject = self
        self._RoutingControlComponent__on_tracks_changed.subject = self.song
        self._RoutingControlComponent__on_return_tracks_changed.subject = self.song
        self._update_track_listeners()

    @listenable_property
    def can_monitor(self):
        track = self.song.view.selected_track
        return old_hasattr(track, 'current_monitoring_state') and not track.is_frozen and track.can_be_armed

    @listenable_property
    def monitoring_state_index(self):
        if self.can_monitor:
            return self.song.view.selected_track.current_monitoring_state

    @listenable_property
    def is_choosing_output(self):
        return self.selected_mode == 'output'

    @listenable_property
    def routing_type_list(self):
        return self._routing_type_list

    @listenable_property
    def routing_channel_list(self):
        return self._routing_channel_list

    @listenable_property
    def routing_channel_position_list(self):
        return self._routing_channel_position_list

    @listens('tracks')
    def __on_tracks_changed(self):
        self._update_track_listeners()

    @listens('return_tracks')
    def __on_return_tracks_changed(self):
        self._update_track_listeners()

    @listens('selected_mode')
    def __on_selected_mode_changed(self, _):
        self.notify_is_choosing_output()

    @listens('selected_track.current_monitoring_state')
    def __on_current_monitoring_state_changed(self):
        self.notify_monitoring_state_index()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self._update_monitoring_state()
        self._update_can_route()
        self._update_routing_type_list()
        self._update_routing_channel_list()
        self._update_routing_channel_position_list()
        self._reconnect_selected_track_slots()

    @listens_group('output_routing_type')
    def __on_any_output_routing_type_changed(self, *_a):
        self._update_monitoring_state_task.restart()

    @listens('is_frozen')
    def __on_is_frozen_changed(self):
        self._update_can_monitor()
        self._update_can_route()

    @listens('input_channel_position_index')
    def __on_input_channel_position_index_changed(self):
        self._update_routing_channel_list()

    @listens('has_input_channel_position')
    def __on_has_input_channel_position_changed(self, *a):
        self._update_routing_channel_position_list()
        self._connect_input_channel_position_encoder()

    @listens('input_routing_type')
    def __on_input_routing_type_changed(self):
        self._update_can_monitor()

    def _update_can_route(self):
        track = self.song.view.selected_track
        self.can_route = self._can_route(track, self.song) and track != self.song.master_track
        self._enable_encoders(self.can_route)

    def _enable_encoders(self, enabled):
        self.routing_type_encoder.enabled = enabled
        self.routing_channel_position_encoder.enabled = enabled
        for encoder in self.routing_channel_encoders:
            encoder.enabled = enabled

    def _set_active_routers(self, type_router, channel_router):
        self._active_type_router = type_router
        self._active_channel_router = channel_router
        self._update_can_route()
        self._update_routing_type_list()
        self._update_routing_channel_list()
        self._update_routing_channel_position_list()
        self._connect_input_channel_position_encoder()
        self._RoutingControlComponent__on_has_input_channel_position_changed.subject = channel_router

    def _connect_input_channel_position_encoder(self):
        if self._active_channel_router.has_input_channel_position:
            self.routing_channel_position_encoder.connect_list_property((self._active_channel_router),
              current_index_property_name='input_channel_position_index',
              max_index=(len(self._active_channel_router.input_channel_positions) - 1))
            self.routing_channel_position_encoder.enabled = self.can_route
        else:
            self.routing_channel_position_encoder.enabled = False
            self.routing_channel_position_encoder.disconnect_property()

    def _update_routing_type_list(self):
        self.unregister_disconnectable(self._routing_type_list)
        self._routing_type_list.disconnect()
        self._routing_type_list = self.register_disconnectable(RoutingTypeList(parent_task_group=(self._tasks),
          router=(self._active_type_router)))
        self.notify_routing_type_list()
        self.routing_type_encoder.connect_list_property((self._routing_type_list),
          current_value_property_name='selected_target',
          list_property_name='targets')

    def _update_routing_channel_list(self):
        self.unregister_disconnectable(self._routing_channel_list)
        self._routing_channel_list.disconnect()
        self._routing_channel_list = self.register_disconnectable(RoutingChannelList(parent_task_group=(self._tasks),
          rt_channel_assigner=(self._real_time_channel_assigner),
          router=(self._active_channel_router)))
        self.notify_routing_channel_list()
        for encoder in self.routing_channel_encoders:
            encoder.connect_list_property((self._routing_channel_list),
              current_value_property_name='selected_target',
              list_property_name='targets')

    def _update_routing_channel_position_list(self):
        if self._routing_channel_position_list is not None:
            self.unregister_disconnectable(self._routing_channel_position_list)
            self._routing_channel_position_list.disconnect()
        if self._active_channel_router.has_input_channel_position:
            self._routing_channel_position_list = self.register_disconnectable(RoutingChannelPositionList(self._active_channel_router))
        else:
            self._routing_channel_position_list = None
        self.notify_routing_channel_position_list()

    def _connect_monitoring_state_encoder(self):
        self.monitor_state_encoder.connect_static_list((self.song.view.selected_track),
          'current_monitoring_state',
          list_values=[
         Live.Track.Track.monitoring_states.IN,
         Live.Track.Track.monitoring_states.AUTO,
         Live.Track.Track.monitoring_states.OFF])

    def _update_monitoring_state(self):
        self._update_monitoring_state_task.kill()
        self._connect_monitoring_state_encoder()
        self._update_can_monitor()

    def _update_can_monitor(self):
        if self.monitor_state_encoder.enabled != self.can_monitor:
            self.monitor_state_encoder.enabled = self.can_monitor
            self.notify_can_monitor()

    def _update_track_listeners(self):
        self._RoutingControlComponent__on_any_output_routing_type_changed.replace_subjects(list(self.song.tracks) + list(self.song.return_tracks))
        self._RoutingControlComponent__on_any_output_routing_type_changed()

    def _reconnect_selected_track_slots(self):
        selected_track = self.song.view.selected_track
        self._RoutingControlComponent__on_is_frozen_changed.subject = selected_track
        self._RoutingControlComponent__on_input_routing_type_changed.subject = selected_track