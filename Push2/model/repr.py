#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/model/repr.py
from __future__ import absolute_import, print_function, unicode_literals
from future.builtins import round
from future.builtins import map
from past.builtins import unicode
import re
from functools import partial
from ableton.v2.base import EventObject, Slot, EventError, find_if, listenable_property, listens, liveobj_valid, old_hasattr
from ..device_parameter_icons import get_image_filenames, get_image_filenames_from_ids
DEVICE_TYPES_WITH_PRESET_NAME = [u'InstrumentGroupDevice',
 u'DrumGroupDevice',
 u'AudioEffectGroupDevice',
 u'MidiEffectGroupDevice',
 u'ProxyInstrumentDevice',
 u'ProxyAudioEffectDevice',
 u'MxDeviceInstrument',
 u'MxDeviceAudioEffect',
 u'MxDeviceMidiEffect']

def _get_parameter_by_name(device, name):
    parameters = device.parameters if liveobj_valid(device) else []
    return find_if(lambda x: x.name == name, parameters)


def _try_to_round_number(parameter_string):
    value_as_number = None
    try:
        value_as_number = int(parameter_string)
    except ValueError:
        pass

    if value_as_number is None:
        try:
            value_as_number = round(float(parameter_string), 2)
        except ValueError:
            pass

    return value_as_number


note_pattern = re.compile(u'^([CDEFGAB].?)((?:-[1-2])|[0-8])$')
hybrid_rate_pattern = re.compile(u'1/[0-9]+ (T|D)')
large_pattern = re.compile(u'\\d|\\xb0|/|\\%|\\.|\\:|\\-|\\+|inf')

def get_parameter_display_large(parameter):
    u"""
    If a numerical value is found, round and return it. Otherwise return the full string.
    
    Used together with get_parameter_display_small to draw the number part of a
    parameter value larger than the unit part.
    
    There are some exceptions, sometimes the unit looks better in the large part.
    See the tests for intended usage and special cases.
    """
    parameter_string = unicode(parameter)
    if note_pattern.search(parameter_string) is not None:
        return parameter_string
    if hybrid_rate_pattern.search(parameter_string) is not None:
        return parameter_string[0:-2]
    large_string = u''.join(large_pattern.findall(parameter_string))
    if large_string in (u'inf', u'-inf'):
        return large_string
    large_number = _try_to_round_number(large_string)
    if large_number is None:
        return parameter_string
    if large_string.startswith(u'+'):
        return u'+' + unicode(large_number)
    return unicode(large_number)


small_pattern = re.compile(u'inf\\s*[A-z]+$|\\d\\s*[A-z]+$')
string_pattern = re.compile(u'[A-z]+$')

def get_parameter_display_small(parameter):
    parameter_string = unicode(parameter)
    small_tokens = small_pattern.findall(parameter_string)
    if len(small_tokens) is 0:
        return u''
    return u''.join(string_pattern.findall(small_tokens[0]))


def strip_formatted_string(str):
    u"""
    Remove multiple whitespaces (including new lines) and whitespaces at the beginning
    and end of the given string.
    """
    return re.sub(u'\\s\\s+', u' ', str).strip()


def convert_color_index(color_index):
    from ..colors import UNCOLORED_INDEX
    if color_index is None:
        return UNCOLORED_INDEX
    return color_index


def determine_color_label_index(item):
    u"""
    Returns a number >= 0 if the given item is a color label (aka Collection),
    -1 otherwise. The number represents the index of the color label in the list of
    *all* color labels (i.e. including currently invisible/disabled labels)
    """
    match = re.search(u'^color:colors=(\\d+)$', item.uri)
    is_color_label = match is not None
    if is_color_label:
        return int(match.group(1)) - 1
    return -1


class ModelAdapter(EventObject):

    def __init__(self, adaptee = None, *a, **k):
        assert liveobj_valid(adaptee)
        super(ModelAdapter, self).__init__(*a, **k)
        self._adaptee = adaptee

    def is_valid(self):
        return liveobj_valid(self._adaptee)

    def __getattr__(self, name):
        if name in self.__dict__ or name in self.__class__.__dict__:
            return object.__getattribute__(self, name)
        return getattr(self._adaptee, name)

    @property
    def _live_ptr(self):
        if old_hasattr(self._adaptee, u'_live_ptr'):
            return self._adaptee._live_ptr
        return id(self._adaptee)

    def _alias_observable_property(self, prop_name, alias_name, getter = None):
        default_getter = lambda self_: getattr(self_._adaptee, prop_name)
        aliased_prop = property(getter or default_getter)
        setattr(self.__class__, alias_name, aliased_prop)
        notifier = getattr(self, u'notify_' + alias_name)
        self.register_slot(Slot(self._adaptee, notifier, prop_name))


class ClipAdapter(ModelAdapter):

    def __init__(self, *a, **k):
        super(ClipAdapter, self).__init__(*a, **k)
        self.register_slot(self._adaptee, self.notify_name, u'name')

    @listenable_property
    def name(self):
        name = self._adaptee.name
        if len(name.strip()) == 0:
            name = u'MIDI clip' if self._adaptee.is_midi_clip else u'Audio clip'
        return name

    @property
    def positions(self):
        return getattr(self._adaptee, u'positions', None)

    @property
    def warping(self):
        return self._adaptee.is_audio_clip and self._adaptee.warping


class DeviceParameterAdapter(ModelAdapter):
    __events__ = (u'hasAutomation',)

    def __init__(self, *a, **k):
        super(DeviceParameterAdapter, self).__init__(*a, **k)
        self._alias_observable_property(u'automation_state', u'hasAutomation', getter=lambda self_: self_._has_automation())
        self.register_slot(self._adaptee, self.notify_displayValue, u'value')
        self.register_slot(self._adaptee, self.notify_unit, u'value')
        self.register_slot(self._adaptee, self.notify_automationActive, u'automation_state')
        self.register_slot(self._adaptee, self.notify_isActive, u'state')
        try:
            self.register_slot(self._adaptee, self.notify_valueItems, u'value_items')
        except EventError:
            pass

    @listenable_property
    def valueItems(self):
        if self._adaptee.is_quantized:
            return self._adaptee.value_items
        return []

    def _get_image_filenames(self, small_images = False):
        device = self.canonical_parent
        if not old_hasattr(device, u'class_name'):
            return []
        custom_images = None
        if liveobj_valid(device):
            try:
                custom_images = device.get_value_item_icons(getattr(self._adaptee, u'original_parameter', self._adaptee))
            except (AttributeError, RuntimeError):
                pass

        if custom_images is not None:
            return get_image_filenames_from_ids(custom_images, small_images)
        else:
            return get_image_filenames(self.original_name, device.class_name, small_images)

    @listenable_property
    def valueItemImages(self):
        return self._get_image_filenames(small_images=False)

    @listenable_property
    def valueItemSmallImages(self):
        result = self._get_image_filenames(small_images=True)
        return result

    @listenable_property
    def displayValue(self):
        return get_parameter_display_large(self._adaptee)

    @listenable_property
    def unit(self):
        return get_parameter_display_small(self._adaptee)

    def _has_automation(self):
        no_automation = 0
        return self._adaptee.automation_state != no_automation

    @listenable_property
    def automationActive(self):
        active_automation = 1
        return self._adaptee.automation_state == active_automation

    @listenable_property
    def isActive(self):
        enabled_state = 0
        return self._adaptee.state == enabled_state


class EditModeOptionAdapter(ModelAdapter):
    __events__ = (u'activeIndex', u'choices')

    def __init__(self, *a, **k):
        super(EditModeOptionAdapter, self).__init__(*a, **k)
        if old_hasattr(self._adaptee, u'active_index'):
            self._alias_observable_property(u'active_index', u'activeIndex', getter=lambda self_: getattr(self_._adaptee, u'active_index', 0))
        self._alias_observable_property(u'default_label', u'choices', getter=lambda self_: self_._choices)

    @property
    def activeIndex(self):
        return 0

    @property
    def _choices(self):
        return getattr(self._adaptee, u'labels', [self._adaptee.default_label])


class SimplerDeviceAdapter(ModelAdapter):

    def __init__(self, *a, **k):
        super(SimplerDeviceAdapter, self).__init__(*a, **k)
        self.register_slot(self._adaptee.view, self.notify_selected_slice, u'selected_slice')
        get_parameter = partial(_get_parameter_by_name, self._adaptee)
        self.sample_start = get_parameter(u'S Start')
        self.sample_length = get_parameter(u'S Length')
        self.loop_length = get_parameter(u'S Loop Length')
        self.loop_on = get_parameter(u'S Loop On')
        self.zoom = get_parameter(u'Zoom')
        self.__on_sample_changed.subject = self._adaptee
        self.__on_sample_changed()

    def _is_slicing(self):
        return self._adaptee.playback_mode == 2

    def _get_slice_times(self):
        slice_times = []
        if self._is_slicing() and liveobj_valid(self._adaptee.sample):
            try:
                slice_times = self._adaptee.sample.slices
            except RuntimeError:
                pass

        return slice_times

    @listens(u'sample')
    def __on_sample_changed(self):
        self.register_slot(self._adaptee.sample, self.notify_start_marker, u'start_marker')
        self.register_slot(self._adaptee.sample, self.notify_end_marker, u'end_marker')
        self.register_slot(self._adaptee.sample, self.notify_slices, u'slices')
        self.register_slot(self._adaptee.sample, self.notify_slicing_sensitivity, u'slicing_sensitivity')
        self.register_slot(self._adaptee.sample, self.notify_gain, u'gain')

    @listenable_property
    def slices(self):

        class SlicePoint(object):

            def __init__(self, __id__, time):
                self.__id__ = __id__
                self.time = time

        return [ SlicePoint(time, time) for time in self._get_slice_times() ]

    @listenable_property
    def selected_slice(self):
        return find_if(lambda s: s.time == self.view.selected_slice, self.slices)

    @listenable_property
    def start_marker(self):
        if liveobj_valid(self._adaptee) and liveobj_valid(self._adaptee.sample):
            return self._adaptee.sample.start_marker
        return 0

    @listenable_property
    def end_marker(self):
        if liveobj_valid(self._adaptee) and liveobj_valid(self._adaptee.sample):
            return self._adaptee.sample.end_marker
        return 0

    @listenable_property
    def slicing_sensitivity(self):
        if liveobj_valid(self._adaptee) and liveobj_valid(self._adaptee.sample):
            return self._adaptee.sample.slicing_sensitivity
        return 0.0

    @listenable_property
    def gain(self):
        if liveobj_valid(self._adaptee) and liveobj_valid(self._adaptee.sample):
            return self._adaptee.sample.gain
        return 0.0

    @listenable_property
    def warping(self):
        if liveobj_valid(self._adaptee) and liveobj_valid(self._adaptee.sample):
            return self._adaptee.sample.warping
        return False


class VisibleAdapter(ModelAdapter):

    def __init__(self, adaptee = None, *a, **k):
        super(VisibleAdapter, self).__init__(adaptee=adaptee, *a, **k)
        self.__on_enabled_changed.subject = adaptee

    @listenable_property
    def visible(self):
        return self._adaptee.is_enabled()

    @listens(u'enabled')
    def __on_enabled_changed(self, enabled):
        self.notify_visible()


class TrackMixAdapter(VisibleAdapter):
    __events__ = (u'scrollOffset',)

    def __init__(self, *a, **k):
        super(TrackMixAdapter, self).__init__(*a, **k)
        self._alias_observable_property(u'scroll_offset', u'scrollOffset')


class TrackControlAdapter(VisibleAdapter):
    __events__ = (u'track_control_mode',)

    def __init__(self, *a, **k):
        super(TrackControlAdapter, self).__init__(*a, **k)
        self._alias_observable_property(u'selected_mode', u'track_control_mode')


class OptionsListAdapter(VisibleAdapter):
    __events__ = (u'selectedItem',)

    def __init__(self, *a, **k):
        super(OptionsListAdapter, self).__init__(*a, **k)
        self._alias_observable_property(u'selected_item', u'selectedItem')


class ItemListAdapter(VisibleAdapter):
    __events__ = (u'selectedItem',)

    def __init__(self, *a, **k):
        super(ItemListAdapter, self).__init__(*a, **k)
        self.__on_selected_item_changed.subject = self._adaptee.item_provider

    @listens(u'selected_item')
    def __on_selected_item_changed(self):
        self.notify_selectedItem()

    @property
    def selectedItem(self):
        return self._adaptee.item_provider.selected_item


class ItemSlotAdapter(ModelAdapter):

    @property
    def icon(self):
        return getattr(self._adaptee, u'icon', u'')


class DeviceAdapter(ModelAdapter):
    __events__ = (u'is_active',)

    def __init__(self, *a, **k):
        from ..device_util import is_drum_pad, find_chain_or_track, find_rack
        from ..device_navigation import is_bank_rack_2
        super(DeviceAdapter, self).__init__(*a, **k)
        item = self._unwrapped_item()
        if old_hasattr(item, u'is_active'):
            if is_bank_rack_2(item):
                self.__on_is_active_changed.subject = item.rack_device
            else:
                self.__on_is_active_changed.subject = item
        elif is_drum_pad(item):
            self.__on_is_active_changed.subject = item.canonical_parent
            self.__on_mute_changed.subject = item
        if old_hasattr(item, u'name'):
            self.__on_name_changed.subject = item
        self._chain = find_chain_or_track(item)
        self._rack_chain = find_chain_or_track(find_rack(item))
        self.__on_chain_color_index_changed.subject = self._chain
        self.__on_rack_color_index_changed.subject = self._rack_chain

    def _unwrapped_item(self):
        return getattr(self._adaptee, u'item', self._adaptee)

    @listenable_property
    def navigation_name(self):
        from ..device_navigation import is_rack_with_bank_2, is_bank_rack_2
        item = self._unwrapped_item()
        name = getattr(item, u'name', u'')
        class_name = getattr(item, u'class_name', None)
        if class_name not in DEVICE_TYPES_WITH_PRESET_NAME:
            name = getattr(item, u'class_display_name', name)
        if is_bank_rack_2(item):
            name = u'\u2022\u2022' + name
        elif is_rack_with_bank_2(item):
            name = u'\u2022' + name
        return name

    @property
    def class_name(self):
        import Live
        item = self._unwrapped_item()
        if isinstance(item, Live.DrumPad.DrumPad):
            return u'DrumPad'
        else:
            return getattr(item, u'class_name', u'')

    @property
    def nestingLevel(self):
        try:
            return self._adaptee.nesting_level
        except AttributeError:
            return 0

    @property
    def is_active(self):
        from ..device_navigation import is_active_element
        try:
            return is_active_element(self._unwrapped_item())
        except AttributeError:
            return True

    @listens(u'is_active')
    def __on_is_active_changed(self):
        self.notify_is_active()

    @listens(u'mute')
    def __on_mute_changed(self):
        self.notify_is_active()

    @listens(u'name')
    def __on_name_changed(self):
        self.notify_navigation_name()

    @property
    def icon(self):
        return getattr(self._adaptee, u'icon', u'')

    @listenable_property
    def chain_color_index(self):
        if liveobj_valid(self._chain):
            return convert_color_index(self._chain.color_index)
        return -1

    @listens(u'color_index')
    def __on_chain_color_index_changed(self):
        self.notify_chain_color_index()

    @listenable_property
    def rack_color_index(self):
        if liveobj_valid(self._rack_chain):
            return convert_color_index(self._rack_chain.color_index)
        return -1

    @listens(u'color_index')
    def __on_rack_color_index_changed(self):
        self.notify_rack_color_index()


class TrackAdapter(ModelAdapter):
    __events__ = (u'activated',)

    def __init__(self, *a, **k):
        super(TrackAdapter, self).__init__(*a, **k)
        if old_hasattr(self._adaptee, u'mute'):
            self.__on_mute_changed.subject = self._adaptee
            self.__on_solo_changed.subject = self._adaptee
            self.__on_muted_via_solo_changed.subject = self._adaptee
        self.has_playing_clip = False
        self._update_has_playing_clip()
        if old_hasattr(self._adaptee, u'playing_slot_index'):
            self.__on_playing_slot_index_changed.subject = self._adaptee
        try:
            if old_hasattr(self._adaptee.parent_track, u'is_frozen'):
                self.__on_is_frozen_changed.subject = self._adaptee.parent_track
        except AttributeError:
            pass

        try:
            self.register_slot(self._adaptee, self.notify_colorIndex, u'color_index')
        except EventError:
            pass

        try:
            self.register_slot(self._adaptee.parent_track, self.notify_parentColorIndex, u'color_index')
        except AttributeError:
            pass

        try:
            self.register_slot(self._adaptee, self.notify_isFrozen, u'is_frozen')
        except EventError:
            pass

        try:
            self.register_slot(self._adaptee, self.notify_arm, u'arm')
        except EventError:
            pass

        try:
            self.register_slot(self._adaptee, self.notify_outputRouting, u'output_routing_type')
        except EventError:
            pass

    @property
    def isFoldable(self):
        return getattr(self._adaptee, u'is_foldable', False)

    @property
    def canShowChains(self):
        return getattr(self._adaptee, u'can_show_chains', False)

    @property
    def containsDrumRack(self):
        from ableton.v2.control_surface import find_instrument_meeting_requirement
        return find_instrument_meeting_requirement(lambda i: i.can_have_drum_pads, self._adaptee) is not None

    @property
    def nestingLevel(self):
        try:
            return self._adaptee.nesting_level
        except AttributeError:
            return 0

    @property
    def activated(self):
        try:
            return not (self._adaptee.muted_via_solo or self._adaptee.mute and not self._adaptee.solo)
        except (RuntimeError, AttributeError):
            return True

    @listenable_property
    def isFrozen(self):
        try:
            return self._adaptee.is_frozen
        except AttributeError:
            return False

    @listenable_property
    def arm(self):
        try:
            if self._adaptee.can_be_armed:
                return self._adaptee.arm
            return False
        except AttributeError:
            return False

    @listenable_property
    def parent_track_frozen(self):
        try:
            return self._adaptee.parent_track.is_frozen
        except AttributeError:
            return False

    @listens(u'is_frozen')
    def __on_is_frozen_changed(self):
        self.notify_parent_track_frozen()

    @listens(u'mute')
    def __on_mute_changed(self):
        self.notify_activated()

    @listens(u'solo')
    def __on_solo_changed(self):
        self.notify_activated()

    @listens(u'muted_via_solo')
    def __on_muted_via_solo_changed(self):
        self.notify_activated()

    @listens(u'playing_slot_index')
    def __on_playing_slot_index_changed(self):
        self._update_has_playing_clip()
        self.notify_playingClip()

    def _update_has_playing_clip(self):
        has_playing_clip = self._adaptee.playing_slot_index >= 0 if old_hasattr(self._adaptee, u'playing_slot_index') else False
        if has_playing_clip != self.has_playing_clip:
            self.has_playing_clip = has_playing_clip
            self.notify_hasPlayingClip()

    def _playing_clip_slot(self):
        if old_hasattr(self._adaptee, u'playing_slot_index'):
            try:
                if self._adaptee.playing_slot_index >= 0:
                    return self._adaptee.clip_slots[self._adaptee.playing_slot_index]
            except RuntimeError:
                pass

    def _playing_clip(self):
        playing_clip_slot = self._playing_clip_slot()
        if playing_clip_slot is not None:
            return playing_clip_slot.clip

    @listenable_property
    def colorIndex(self):
        try:
            return convert_color_index(self._adaptee.color_index)
        except AttributeError:
            return self.parentColorIndex

    @listenable_property
    def parentColorIndex(self):
        try:
            return convert_color_index(self._adaptee.parent_track.color_index)
        except AttributeError:
            return -1

    @property
    def isMaster(self):
        try:
            return self._adaptee == self._adaptee.canonical_parent.master_track
        except AttributeError:
            return False

    @property
    def isAudio(self):
        try:
            return not self._adaptee.has_midi_input
        except AttributeError:
            return False

    @property
    def isReturn(self):
        try:
            return self._adaptee in list(self._adaptee.canonical_parent.return_tracks)
        except AttributeError:
            return False

    @listenable_property
    def outputRouting(self):
        routing_type = getattr(self._adaptee, u'output_routing_type', None)
        if routing_type is not None:
            return routing_type.display_name
        return u''

    @listenable_property
    def hasPlayingClip(self):
        return self.has_playing_clip

    @listenable_property
    def playingClip(self):
        return self._playing_clip()


class TrackListAdapter(VisibleAdapter):
    __events__ = (u'selectedTrack',)

    def __init__(self, *a, **k):
        super(TrackListAdapter, self).__init__(*a, **k)
        self._alias_observable_property(u'selected_track', u'selectedTrack')


class BrowserItemAdapter(ModelAdapter):

    @property
    def icon(self):
        return getattr(self._adaptee, u'icon', u'')

    @property
    def color_label_index(self):
        return determine_color_label_index(self._adaptee)


class BrowserListWrapper(EventObject):
    u"""
    Custom object wrapper that takes care of binding a browser list and serializing it.
    This is necessary to greatly improve performance and avoid unnecessary wrapping of
    each browser item.
    """

    def __init__(self, browser_list, notifier = None, *a, **k):
        super(BrowserListWrapper, self).__init__(*a, **k)
        self._browser_list = browser_list
        self._notifier = notifier
        slot = Slot(browser_list, self.notify, u'items')
        slot.connect()
        self.register_slot(slot)

    @staticmethod
    def _serialize_browser_item(item):
        return {u'id': item.uri,
         u'name': item.name,
         u'is_loadable': item.is_loadable,
         u'is_device': item.is_device,
         u'icon': getattr(item, u'icon', u''),
         u'color_label_index': determine_color_label_index(item)}

    def to_json(self):
        return list(map(self._serialize_browser_item, self._browser_list.items))

    def notify(self):
        self._notifier.structural_change()

    def disconnect(self):
        super(BrowserListWrapper, self).disconnect()
        self._browser_list = None


class LiveDialogAdapter(VisibleAdapter):

    @property
    def text(self):
        text = self._adaptee.text
        if text is not None:
            return strip_formatted_string(text)
        return u''


class RoutingAdapter(VisibleAdapter):
    __events__ = (u'routingTypeList', u'routingChannelList', u'routingChannelPositionList')

    def __init__(self, *a, **k):
        super(RoutingAdapter, self).__init__(*a, **k)
        self._alias_observable_property(u'routing_type_list', u'routingTypeList', lambda self_: [self_._adaptee.routing_type_list])
        self._alias_observable_property(u'routing_channel_list', u'routingChannelList', lambda self_: [self_._adaptee.routing_channel_list])
        self._alias_observable_property(u'routing_channel_position_list', u'routingChannelPositionList', lambda self_: [self_._adaptee.routing_channel_position_list])
