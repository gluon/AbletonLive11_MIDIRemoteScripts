#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/mixer_control_component.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import filter
from builtins import range
from past.utils import old_div
from contextlib import contextmanager
from functools import partial
from future.moves.itertools import zip_longest
from math import ceil
import Live
from ableton.v2.base import clamp, depends, listens, listens_group, liveobj_valid, NamedTuple
from ableton.v2.control_surface.components import SimpleItemSlot
from ableton.v2.control_surface.control import control_list, ButtonControl, MappedSensitivitySettingControl
from ableton.v2.control_surface.mode import ModesComponent
from pushbase.internal_parameter import ConstantParameter
from pushbase.mixer_utils import has_pan_mode, is_set_to_split_stereo
from pushbase.song_utils import find_parent_track
from .item_lister import IconItemSlot
from .real_time_channel import RealTimeDataComponent
MIXER_SECTIONS = (u'Volumes', u'Pans')
SEND_SECTIONS = [u'A Sends',
 u'B Sends',
 u'C Sends',
 u'D Sends',
 u'E Sends',
 u'F Sends',
 u'G Sends',
 u'H Sends',
 u'I Sends',
 u'J Sends',
 u'K Sends',
 u'L Sends']
SEND_LIST_LENGTH = 5
SEND_MODE_NAMES = [u'send_slot_one',
 u'send_slot_two',
 u'send_slot_three',
 u'send_slot_four',
 u'send_slot_five']

class MixerSectionDescription(NamedTuple):
    view = None
    parameter_name = None


def assign_parameters(controls, parameters):
    for control, parameter in zip_longest(controls, parameters):
        if control:
            if not liveobj_valid(parameter) or isinstance(parameter.canonical_parent, Live.MixerDevice.MixerDevice):
                control.mapped_parameter = parameter
            else:
                track = find_parent_track(parameter)
                control.mapped_parameter = parameter if liveobj_valid(track) and not track.is_frozen else None


class MixerControlComponent(ModesComponent):
    __events__ = (u'items', u'selected_item')
    controls = control_list(MappedSensitivitySettingControl)
    cycle_sends_button = ButtonControl(color=u'DefaultButton.Off')

    @staticmethod
    def get_tracks(items):
        return list(filter(lambda item: item is not None and isinstance(item.proxied_object, Live.Track.Track), items))

    @depends(tracks_provider=None, real_time_mapper=None, register_real_time_data=None)
    def __init__(self, view_model = None, tracks_provider = None, real_time_mapper = None, register_real_time_data = None, *a, **k):
        assert liveobj_valid(real_time_mapper)
        assert view_model is not None
        assert tracks_provider is not None
        super(MixerControlComponent, self).__init__(*a, **k)
        self._send_offset = 0
        self.real_time_meter_handlers = [ RealTimeDataComponent(channel_type=u'meter', real_time_mapper=real_time_mapper, register_real_time_data=register_real_time_data, is_enabled=False) for _ in range(8) ]
        self._track_provider = tracks_provider
        self._on_return_tracks_changed.subject = self.song
        self._on_mode_changed.subject = self
        self._mixer_section_view = None
        self._mixer_sections = []
        self._selected_view = view_model.volumeControlListView
        self._parameter_getter = lambda x: None
        self._setup_modes(view_model)
        self.selected_mode = u'volume'
        self._selected_item = u''
        self._items = []
        self._on_return_tracks_changed()
        self._update_mixer_sections()
        self._on_items_changed.subject = self._track_provider
        self._on_selected_item_changed.subject = self._track_provider
        tracks = self.get_tracks(self._track_provider.items)
        self.__on_track_frozen_state_changed.replace_subjects(tracks)
        self.__on_panning_mode_changed.replace_subjects(list(filter(has_pan_mode, [ t.mixer_device for t in tracks ])))

    def _setup_modes(self, view_model):
        self._add_mode(u'volume', view_model.volumeControlListView, lambda mixer: mixer.volume, additional_mode_contents=self.real_time_meter_handlers)
        self._add_mode(u'panning', view_model.panControlListView, lambda mixer: (ConstantParameter(original_parameter=mixer.panning) if is_set_to_split_stereo(mixer) else mixer.panning))

        def add_send_mode(index):
            self._add_mode(SEND_MODE_NAMES[index], view_model.sendControlListView, lambda mixer: (mixer.sends[self._send_offset + index] if len(mixer.sends) > self._send_offset + index else None))

        for i in range(SEND_LIST_LENGTH):
            add_send_mode(i)

    def _add_mode(self, mode, view, parameter_getter, additional_mode_contents = []):
        description = MixerSectionDescription(view=view, parameter_getter=parameter_getter)
        self.add_mode(mode, additional_mode_contents + [partial(self._set_mode, description)])
        mode_button = self.get_mode_button(mode)
        mode_button.mode_selected_color = u'MixerControlView.SectionSelected'
        mode_button.mode_unselected_color = u'MixerControlView.SectionUnSelected'

    def on_enabled_changed(self):
        super(MixerControlComponent, self).on_enabled_changed()
        self._selected_view.visible = self.is_enabled()
        self._update_mixer_sections()
        if not self.is_enabled():
            self._update_realtime_ids()

    def set_mixer_section(self, mixer_section):
        self._mixer_section_view = mixer_section
        if self._mixer_section_view:
            self._mixer_section_view.model.mode = u'Global'
            self._update_mixer_sections()

    @property
    def number_sends(self):
        return len(self._track_provider.selected_item.mixer_device.sends)

    def _set_mode(self, description):
        self._selected_view.visible = False
        self._selected_view = description.view
        self._parameter_getter = description.parameter_getter
        self._update_controls(self._parameter_getter, self._selected_view)
        self._selected_view.visible = True

    @listens(u'selected_mode')
    def _on_mode_changed(self, selected_mode):
        if selected_mode in SEND_MODE_NAMES:
            index = SEND_MODE_NAMES.index(selected_mode)
            self._selected_item = SEND_SECTIONS[clamp(index + self._send_offset, 0, self.number_sends - 1)]
        else:
            self._selected_item = MIXER_SECTIONS[1] if selected_mode == u'panning' else MIXER_SECTIONS[0]
        self.notify_selected_item()

    @listens(u'return_tracks')
    def _on_return_tracks_changed(self):
        with self._updating_send_offset_mode_selection():
            self._update_mode_selection()
            new_send_offset = max(0, int(ceil(old_div(float(self.number_sends), float(SEND_LIST_LENGTH)) - 1) * SEND_LIST_LENGTH))
            if new_send_offset < self._send_offset:
                self._send_offset = new_send_offset

    @listens(u'items')
    def _on_items_changed(self):
        tracks = self.get_tracks(self._track_provider.items)
        self.__on_panning_mode_changed.replace_subjects(list(filter(has_pan_mode, [ t.mixer_device for t in tracks ])))
        self._update_controls(self._parameter_getter, self._selected_view)

    @listens_group(u'is_frozen')
    def __on_track_frozen_state_changed(self, identifier):
        self._update_controls(self._parameter_getter, self._selected_view)

    @listens_group(u'panning_mode')
    def __on_panning_mode_changed(self, identifier):
        self._update_controls(self._parameter_getter, self._selected_view)

    @listens(u'selected_item')
    def _on_selected_item_changed(self):
        if self.number_sends <= SEND_LIST_LENGTH:
            self._send_offset = 0
        self._update_mode_selection()
        self._update_mixer_sections()
        self._update_buttons(self.selected_mode)

    def _update_mode_selection(self):
        number_sends = self.number_sends
        if self.selected_mode in SEND_MODE_NAMES:
            index = SEND_MODE_NAMES.index(self.selected_mode)
            if index + self._send_offset >= number_sends and number_sends > 0:
                self.selected_mode = SEND_MODE_NAMES[number_sends % SEND_LIST_LENGTH - 1]
            elif index == 0 and number_sends == 0:
                self.selected_mode = u'panning'

    def _update_mixer_sections(self):
        if self.is_enabled():
            position = max(self._send_offset, 0)
            pos_range = min(self.number_sends - position, SEND_LIST_LENGTH)
            mixer_section_names = list(MIXER_SECTIONS) + SEND_SECTIONS[position:position + pos_range]
            self._mixer_sections = [ IconItemSlot(name=name) for name in mixer_section_names ]
            if self.number_sends > SEND_LIST_LENGTH:
                self._mixer_sections.extend([IconItemSlot()] * (8 - len(self._mixer_sections)))
                self._mixer_sections[7] = IconItemSlot(icon=u'page_right.svg')
            self.notify_items()
            if self.selected_mode in SEND_MODE_NAMES:
                index = SEND_MODE_NAMES.index(self.selected_mode)
                self._selected_item = SEND_SECTIONS[index + self._send_offset]
                self.notify_selected_item()

    @property
    def items(self):
        return self._mixer_sections

    @property
    def selected_item(self):
        return self._selected_item

    def _update_controls(self, parameter_getter, control_view):
        if self.is_enabled():
            parameters = self._get_parameter_for_tracks(parameter_getter)
            control_view.parameters = parameters
            self._update_realtime_ids()
            assign_parameters(self.controls, parameters)

    def _update_realtime_ids(self):
        mixables = self._track_provider.items
        for handler, mixable in zip(self.real_time_meter_handlers, mixables):
            handler.set_data(mixable.mixer_device if liveobj_valid(mixable) else None)

    def _get_parameter_for_tracks(self, parameter_getter):
        tracks = self._track_provider.items
        self.controls.control_count = len(tracks)
        return [ (parameter_getter(t.mixer_device) if t else None) for t in tracks ]

    def mode_can_be_used(self, mode):
        return mode not in SEND_MODE_NAMES or SEND_MODE_NAMES.index(mode) + self._send_offset < self.number_sends

    def _update_buttons(self, selected_mode):
        for name in self._mode_map.keys():
            self.get_mode_button(name).enabled = self.mode_can_be_used(name)

        self.cycle_sends_button.enabled = self.number_sends > SEND_LIST_LENGTH

    @cycle_sends_button.pressed
    def cycle_sends_button(self, button):
        button.color = u'MixerControlView.SectionSelected'

    @cycle_sends_button.released
    def cycle_sends_button(self, button):
        button.color = u'MixerControlView.SectionUnSelected'
        self._cycle_send_offset()

    def _cycle_send_offset(self):
        with self._updating_send_offset_mode_selection():
            new_offset = self._send_offset + SEND_LIST_LENGTH
            self._send_offset = new_offset if new_offset < self.number_sends else 0
            if self.selected_mode in SEND_MODE_NAMES:
                self.selected_mode = SEND_MODE_NAMES[0]

    @contextmanager
    def _updating_send_offset_mode_selection(self):
        yield
        self._update_mixer_sections()
        self._update_buttons(self.selected_mode)
        self._update_controls(self._parameter_getter, self._selected_view)
