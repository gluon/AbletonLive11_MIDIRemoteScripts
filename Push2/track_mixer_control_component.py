# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\track_mixer_control_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 6956 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from ableton.v2.base import clamp, depends, listens, liveobj_valid
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import SimpleItemSlot
from ableton.v2.control_surface.control import ButtonControl, MappedSensitivitySettingControl, control_list
from pushbase.mixer_utils import has_pan_mode, is_set_to_split_stereo
from .item_lister import IconItemSlot
from .mixer_control_component import assign_parameters
from .real_time_channel import RealTimeDataComponent

class TrackMixerControlComponent(Component):
    __events__ = ('parameters', 'scroll_offset', 'items')
    BUTTON_SKIN = dict(color='TrackControlView.ButtonOff',
      pressed_color='TrackControlView.ButtonOn',
      disabled_color='TrackControlView.ButtonDisabled')
    controls = control_list(MappedSensitivitySettingControl)
    scroll_right_button = ButtonControl(**BUTTON_SKIN)
    scroll_left_button = ButtonControl(**BUTTON_SKIN)

    @depends(tracks_provider=None, real_time_mapper=None, register_real_time_data=None)
    def __init__(self, real_time_mapper=None, register_real_time_data=None, tracks_provider=None, *a, **k):
        (super(TrackMixerControlComponent, self).__init__)(*a, **k)
        self._tracks_provider = tracks_provider
        self._on_return_tracks_changed.subject = self.song
        self.real_time_meter_channel = RealTimeDataComponent(parent=self,
          real_time_mapper=real_time_mapper,
          register_real_time_data=register_real_time_data,
          channel_type='meter')
        self._scroll_offset = 0
        self._items = []
        self._number_return_tracks = self._number_sends()
        self._update_scroll_buttons()
        self._TrackMixerControlComponent__on_selected_item_changed.subject = self._tracks_provider
        self._TrackMixerControlComponent__on_selected_item_changed()

    def set_controls(self, controls):
        self.controls.set_control_element(controls)
        self._update_controls()

    @listens('panning_mode')
    def __on_pan_mode_changed(self):
        self._update_controls()
        self._update_scroll_offset()

    @listens('selected_item')
    def __on_selected_item_changed(self):
        self._update_scroll_offset()
        self._update_real_time_channel_id()
        mixer = self._tracks_provider.selected_item.mixer_device
        self._TrackMixerControlComponent__on_pan_mode_changed.subject = mixer if has_pan_mode(mixer) else None
        self._TrackMixerControlComponent__on_pan_mode_changed()

    def update(self):
        super(TrackMixerControlComponent, self).update()
        if self.is_enabled():
            self._update_controls()
            self._update_scroll_buttons()
            self._update_real_time_channel_id()

    def _update_real_time_channel_id(self):
        self.real_time_meter_channel.set_data(self._tracks_provider.selected_item.mixer_device)

    def _update_controls(self):
        if self.is_enabled():
            assign_parameters(self.controls, self.parameters[self.scroll_offset:])
            self.notify_parameters()

    @property
    def parameters(self):
        return self._get_track_mixer_parameters()

    @property
    def scroll_offset(self):
        return self._scroll_offset

    @listens('return_tracks')
    def _on_return_tracks_changed(self):
        self._update_controls()
        self._update_scroll_offset()

    def _number_sends(self):
        mixable = self._tracks_provider.selected_item
        if mixable != self.song.master_track:
            return len(mixable.mixer_device.sends)
        return 0

    def _max_return_tracks(self):
        mixer = self._tracks_provider.selected_item.mixer_device
        if is_set_to_split_stereo(mixer):
            return 5
        return 6

    def _update_scroll_offset(self):
        new_number_return_tracks = self._number_sends()
        max_return_tracks = self._max_return_tracks()
        if max_return_tracks<= new_number_return_tracks < self._number_return_tracks and max_return_tracks + self._scroll_offset > new_number_return_tracks:
            delta = min(new_number_return_tracks - self._number_return_tracks, 0)
            self._scroll_controls(delta)
        else:
            if new_number_return_tracks < max_return_tracks or self._tracks_provider.selected_item == self.song.master_track:
                self._scroll_offset = 0
        self._update_controls()
        self._update_scroll_buttons()
        self._number_return_tracks = new_number_return_tracks

    def _get_track_mixer_parameters(self):
        mixer_params = []
        if self._tracks_provider.selected_item:
            mixer = self._tracks_provider.selected_item.mixer_device
            mixer_params = [mixer.volume]
            if is_set_to_split_stereo(mixer):
                mixer_params += [mixer.left_split_stereo, mixer.right_split_stereo]
            else:
                mixer_params += [mixer.panning]
            mixer_params += list(mixer.sends)
        return mixer_params

    @scroll_right_button.pressed
    def scroll_right_button(self, button):
        self._scroll_controls(1)

    @scroll_left_button.pressed
    def scroll_left_button(self, button):
        self._scroll_controls(-1)

    def _update_scroll_buttons(self):
        if self.is_enabled():
            num_return_tracks = self._number_sends()
            self.scroll_right_button.enabled = num_return_tracks > self._max_return_tracks() + self._scroll_offset
            self.scroll_left_button.enabled = self._scroll_offset > 0
            self._update_view_slots()

    @property
    def items(self):
        return self._items

    def _update_view_slots(self):
        self._items = [IconItemSlot() for _ in range(6)]
        self._items.append(IconItemSlot(icon=('page_left.svg' if self.scroll_left_button.enabled else '')))
        self._items.append(IconItemSlot(icon=('page_right.svg' if self.scroll_right_button.enabled else '')))
        self.notify_items()

    def _scroll_controls(self, delta):
        num_return_tracks = self._number_sends()
        self._scroll_offset = clamp(self._scroll_offset + delta, 0, num_return_tracks if num_return_tracks > self._max_return_tracks() else 0)
        self.notify_scroll_offset()
        self._update_controls()
        self._update_scroll_buttons()