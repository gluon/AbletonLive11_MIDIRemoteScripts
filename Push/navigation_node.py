# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\navigation_node.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 22107 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import filter, map, range, zip
from functools import partial
import Live.DrumPad, Live.Song, Live.Track
from ableton.v2.base import EventObject, compose, depends, find_if, flatten, in_range, index_if, listenable_property, listens, listens_group, liveobj_changed, liveobj_valid, second
from ableton.v2.control_surface import select_and_appoint_device
from pushbase import consts
DeviceType = Live.Device.DeviceType

def make_navigation_node(model_object, is_entering=True, session_ring=None, device_bank_registry=None, banking_info=None, device_provider=None):
    if isinstance(model_object, ChainNode.RackBank2Device):
        model_object = model_object.rack_device
    node = None
    if model_object == None:
        node = None
    else:
        if isinstance(model_object, Live.Song.Song):
            node = SongNode(object=model_object, session_ring=session_ring)
        else:
            if isinstance(model_object, Live.Track.Track):
                node = TrackNode(object=model_object,
                  device_bank_registry=device_bank_registry,
                  device_provider=device_provider)
            else:
                if isinstance(model_object, Live.Chain.Chain):
                    node = ChainNode(object=model_object,
                      device_bank_registry=device_bank_registry,
                      device_provider=device_provider)
                else:
                    if isinstance(model_object, Live.DrumPad.DrumPad):
                        node = ChainNode(object=(model_object.chains[0]), device_bank_registry=device_bank_registry, device_provider=device_provider) if model_object.chains else None
                    else:
                        if isinstance(model_object, Live.Device.Device):
                            if model_object.can_have_chains:
                                if model_object.can_have_drum_pads:
                                    if is_entering:
                                        node = None
                                    else:
                                        node = make_navigation_node((model_object.canonical_parent),
                                          is_entering=is_entering,
                                          device_bank_registry=device_bank_registry,
                                          banking_info=banking_info,
                                          device_provider=device_provider)
                                else:
                                    node = RackNode(model_object)
                            else:
                                node = SimpleDeviceNode(device_bank_registry, banking_info, model_object)
    if node:
        if node.parent:
            if not node.children:
                node.disconnect()
                node = None
            if isinstance(node, RackNode):
                if len(node.children) == 1:
                    actual_model_object = node.children[0][1] if is_entering else node.parent
                    node.disconnect()
                    node = make_navigation_node(actual_model_object,
                      is_entering=is_entering,
                      device_bank_registry=device_bank_registry,
                      banking_info=banking_info,
                      device_provider=device_provider)
        return node


class NavigationNode(EventObject):
    __events__ = ('children', 'selected_child', 'state')

    def get_selected_child(self):
        pass

    def set_selected_child(self, value):
        pass

    selected_child = property(lambda self: self.get_selected_child()
, lambda self, x: self.set_selected_child(x)
)

    def get_state(self):
        pass

    state = property(lambda self: self.get_state()
)

    def set_state(self, index, value):
        pass

    def get_children(self):
        pass

    children = property(lambda self: self.get_children()
)

    def delete_child(self, index):
        pass

    def get_parent(self):
        pass

    parent = property(lambda self: self.get_parent()
)

    def get_object(self):
        pass

    object = property(lambda self: self.get_object()
)

    def preselect(self):
        selected_child_index = self.selected_child
        if selected_child_index == None:
            if self.children:
                self.selected_child = 0
        self.notify_selected_child(self.selected_child)


class ModelNode(NavigationNode):

    def __init__(self, object=None, *a, **k):
        (super(ModelNode, self).__init__)(*a, **k)
        self._object = object
        self._children = []
        self._state = []
        self._selected_child = None
        self._in_update_children = False

    def _get_children_from_model(self):
        pass

    def _get_selected_child_from_model(self):
        pass

    def _set_selected_child_in_model(self, child):
        pass

    def _get_state_from_model(self, child):
        pass

    def _set_state_in_model(self, child, value):
        pass

    def get_state(self):
        return self._state

    def get_children(self):
        return self._children

    def get_selected_child(self):
        return self._selected_child

    def set_selected_child(self, child):
        if child is not None and child >= 0 and child < len(self._children):
            _, obj = self._children[child]
            self._set_selected_child_in_model(obj)
            self._selected_child = child
        else:
            self._selected_child = None
            self._set_selected_child_in_model(None)

    def set_state(self, child, value):
        if child >= 0:
            if child < len(self._children):
                _, obj = self._children[child]
                self._state[child] = self._set_state_in_model(obj, value)

    def get_object(self):
        return self._object

    def get_parent(self):
        if liveobj_valid(self._object):
            return self._object.canonical_parent

    def _get_song(self):
        return self._get_parent_with_class(Live.Song.Song)

    def _get_track(self):
        return self._get_parent_with_class(Live.Track.Track)

    def _get_parent_with_class(self, cls):
        node = self._object
        while liveobj_valid(node):
            if not isinstance(node, cls):
                node = node.canonical_parent

        return node

    def _update_selected_child(self):
        selected = self._get_selected_child_from_model()
        children = [c[1] for c in self._children]
        self._selected_child = children.index(selected) if selected in children else None
        self.notify_selected_child(self._selected_child)

    def _update_state(self, child):
        children = list(map(second, self.children))
        if child in children:
            index = children.index(child)
            value = self._get_state_from_model(child)
            self._state[index] = value
            self.notify_state(index, value)

    def _update_children(self):
        self._in_update_children = True
        self._children = self._get_children_from_model()
        self._state = list(map(compose(self._get_state_from_model, second), self._children))
        self.notify_children()
        for idx, value in enumerate(self._state):
            self.notify_state(idx, value)

        self._in_update_children = False


class ChainNode(ModelNode):

    class RackBank2Device(EventObject):

        def __init__(self, rack_device, *a, **k):
            (super(EventObject, self).__init__)(*a, **k)
            self._rack_device = rack_device

        @property
        def rack_device(self):
            return self._rack_device

        @listenable_property
        def name(self):
            if liveobj_valid(self._rack_device):
                return self._rack_device.name
            return ''

        @listenable_property
        def class_name(self):
            return 'RackBank2Device'

        @listenable_property
        def parameters(self):
            if liveobj_valid(self._rack_device):
                return self._rack_device.parameters
            return []

        @listenable_property
        def bank_index(self):
            return 1

    def __init__(self, device_provider=None, device_bank_registry=None, *a, **k):
        (super(ChainNode, self).__init__)(*a, **k)
        self._device_bank_registry = device_bank_registry
        self._device_provider = device_provider
        self._on_devices_changed_in_live.subject = self._object
        self._on_selected_device_changed_in_live.subject = self._get_track().view
        macro_devices = filter(lambda device: hasattr(device, 'macros_mapped')
, self._object.devices)
        self._on_macros_mapped_changed.replace_subjects(macro_devices)
        self._child_name_slots = self.register_disconnectable(EventObject())
        self._child_state_slots = self.register_disconnectable(EventObject())
        self._selected_drum_pad_slots = self.register_disconnectable(EventObject())
        self._update_children()
        self._update_selected_child()

    def preselect(self):
        old_selected_child_index = self.selected_child
        if old_selected_child_index == None:
            devices = list(map(second, self.children))
            instrument = index_if(lambda d: isinstance(d, Live.Device.Device) and d.type == DeviceType.instrument
, devices)
            if in_range(instrument, 0, len(devices)):
                if devices[instrument].can_have_drum_pads and devices[instrument].drum_pads and instrument + 1 < len(devices):
                    self.selected_child = instrument + 1
                else:
                    self.selected_child = instrument
        super(ChainNode, self).preselect()
        new_selected_child_index = self.selected_child
        track = self._get_track()
        if new_selected_child_index == old_selected_child_index:
            if new_selected_child_index != None:
                _, selected_object = self.children[new_selected_child_index]
                if isinstance(selected_object, Live.Device.Device):
                    if track:
                        if track.view.selected_device != selected_object:
                            select_and_appoint_device(self._get_song(), selected_object)
        self._device_bank_registry.set_device_bank(track.view.selected_device, 0)

    def delete_child(self, index):
        if index is not None:
            if not index >= 0 or index < len(self._children):
                if not isinstance(self._children[index][1], Live.DrumPad.DrumPad):
                    drumpads_before = len(list(filter(lambda _ChainNode__x: isinstance(_ChainNode__x[1], Live.DrumPad.DrumPad)
, self._children[:index])))
                    delete_index = index - drumpads_before
                    if len(self.object.devices) > delete_index:
                        self.object.delete_device(delete_index)

    def _get_children_from_model(self):

        def expand_device(d):
            is_rack_with_bank_2 = getattr(d, 'can_have_chains', False) and any(d.macros_mapped[8:])
            name_prefix = '°' if is_rack_with_bank_2 else ''
            result = [
             (
              name_prefix + d.name, d)]
            if is_rack_with_bank_2:
                result.append(('°°' + d.name, ChainNode.RackBank2Device(rack_device=d)))
            drum_pad = d.view.selected_drum_pad if d.can_have_drum_pads else None
            if drum_pad:
                drum_pad_name = drum_pad.name if len(drum_pad.chains) > 0 else 'EmptyPad'
                result.append((drum_pad_name, drum_pad))
            return result

        return list(flatten(map(expand_device, self._object.devices)))

    def _set_selected_child_in_model(self, selected):
        song = self._get_song()
        device_to_provide = None
        if selected and isinstance(selected, Live.DrumPad.DrumPad):
            if not selected.chains or selected.chains[0].devices:
                device_to_provide = selected.chains[0].devices[0]
                select_and_appoint_device(song, device_to_provide)
        else:
            if selected and isinstance(selected, Live.Device.Device):
                device_to_provide = selected
                select_and_appoint_device(song, selected)
                self._device_bank_registry.set_device_bank(selected, 0)
            else:
                device_to_provide = selected
        if device_to_provide is not None:
            self._device_provider.device = device_to_provide

    def _get_selected_child_from_model(self):
        devices = list(map(second, self.children))
        selected = self._get_track().view.selected_device
        if selected == None:
            return find_if(lambda d: isinstance(d, Live.DrumPad.DrumPad)
, devices)
        is_deeper = False
        while selected:
            if selected in devices:
                if isinstance(selected, Live.DrumPad.DrumPad):
                    self._on_selected_drum_pad()
                    self._update_child_slots()
                    return selected
                else:
                    if is_deeper:
                        if selected.can_have_drum_pads:
                            self._on_selected_drum_pad()
                            self._update_child_slots()
                            return selected.view.selected_drum_pad
                    return selected
            else:
                selected = selected.canonical_parent
                is_deeper = True

    def _get_state_from_model(self, child):
        if isinstance(child, Live.DrumPad.DrumPad):
            return not bool(child.mute)
        if isinstance(child, Live.Device.Device):
            if child.parameters:
                return bool(child.parameters[0].value)
        return False

    def _set_state_in_model(self, child, value):
        if child == None:
            return False
        if isinstance(child, Live.DrumPad.DrumPad):
            if child.mute == value:
                child.mute = not value
                return value
            return not child.mute
        if child.parameters:
            on_off = child.parameters[0]
            if value != on_off.value:
                if on_off.is_enabled:
                    child.parameters[0].value = int(value)
                    return value
            return bool(on_off.value)

    @listens('devices')
    def _on_devices_changed_in_live(self):
        macro_devices = filter(lambda device: hasattr(device, 'macros_mapped')
, self._object.devices)
        self._on_macros_mapped_changed.replace_subjects(macro_devices)
        self._update_children()
        self._update_selected_child()
        self._update_child_slots()

    @listens('selected_device')
    def _on_selected_device_changed_in_live(self):
        self._update_selected_child()

    @listens_group('macros_mapped')
    def _on_macros_mapped_changed(self, _):
        self._update_children()
        self._update_selected_child()
        self._update_child_slots()

    def _on_selected_drum_pad(self):
        self._update_children()

    def _update_children(self):
        super(ChainNode, self)._update_children()
        self._update_child_slots()

    def _update_child_slots(self):
        self._child_name_slots.disconnect()
        self._child_state_slots.disconnect()
        self._selected_drum_pad_slots.disconnect()
        for device in map(second, self.children):
            self._child_name_slots.register_slot(device, self._update_children, 'name')
            if isinstance(device, Live.DrumPad.DrumPad):
                self._child_state_slots.register_slot(device, partial(self._update_state, device), 'mute')
            if isinstance(device, Live.Device.Device):
                if device.can_have_drum_pads:
                    self._selected_drum_pad_slots.register_slot(device.view, self._on_selected_drum_pad, 'selected_drum_pad')
                if device.parameters:
                    self._child_state_slots.register_slot(device.parameters[0], partial(self._update_state, device), 'value')


class TrackNode(ChainNode):
    if not consts.PROTO_SONG_IS_ROOT:

        def get_parent(self):
            pass


class SongNode(ModelNode):

    def __init__(self, session_ring=None, *a, **k):
        (super(SongNode, self).__init__)(*a, **k)
        self._session_ring = session_ring
        self.register_slot(self._object, self._update_children, 'visible_tracks')
        self.register_slot(self._object, self._update_children, 'return_tracks')
        self.register_slot(self._object.view, self._update_selected_child, 'selected_track')
        self._update_children()
        self._update_selected_child()

    def _get_selected_child_from_model(self):
        return self._object.view.selected_track

    def _set_selected_child_in_model(self, value):
        if liveobj_valid(value):
            self._object.view.selected_track = value

    def _get_children_from_model(self):
        tracks_to_use = self._session_ring.tracks_to_use()
        return [(t.name, t) for t in tracks_to_use]


class SimpleDeviceNode(ModelNode):

    def __init__(self, device_bank_registry=None, banking_info=None, *a, **k):
        (super(SimpleDeviceNode, self).__init__)(*a, **k)
        self._mute_next_update = False
        self._device_bank_registry = device_bank_registry
        self._banking_info = banking_info
        self._on_device_bank_changed.subject = self._device_bank_registry
        self._on_device_parameters_changed.subject = self._object
        self._update_children()
        self._update_selected_child()

    @listens('device_bank')
    def _on_device_bank_changed(self, device, bank):
        self._update_selected_child()

    @listens('parameters')
    def _on_device_parameters_changed(self):
        if self._children != self._get_children_from_model():
            self._update_children()
            selected_child = len(self._children) - 1 if self._children else None
            self.set_selected_child(selected_child)

    def _get_selected_child_from_model(self):
        if self.children:
            return self._device_bank_registry.get_device_bank(self.object)

    def _set_selected_child_in_model(self, value):
        if value != None:
            self._device_bank_registry.set_device_bank(self.object, value)

    def _get_children_from_model(self):
        names = self._banking_info.device_bank_names(device=(self.object))
        offset = 0
        if names:
            if len(names) > 1:
                if self._banking_info.has_main_bank(self.object):
                    names = names[1:]
                    offset = 1
        return list(zip(names, list(range(offset, len(names) + offset))))


class RackNode(ModelNode):

    def __init__(self, *a, **k):
        (super(RackNode, self).__init__)(*a, **k)
        self.register_slot(self._object, self._update_children, 'chains')
        self.register_slot(self._object.view, self._update_selected_child, 'selected_chain')
        self._update_children()
        self._update_selected_child()

    def _get_selected_child_from_model(self):
        return self._object.view.selected_chain

    def _set_selected_child_in_model(self, value):
        if liveobj_valid(value):
            if liveobj_changed(self._object.view.selected_chain, value):
                self._object.view.selected_chain = value

    def _get_children_from_model(self):
        return [(c.name, c) for c in self._object.chains]