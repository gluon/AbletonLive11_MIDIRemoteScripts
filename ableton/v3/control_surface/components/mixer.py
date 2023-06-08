<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/mixer.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 8186 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from itertools import zip_longest
from ...base import clamp, depends, listens
from .. import Component
from ..controls import ButtonControl, MappedControl
<<<<<<< HEAD
from . import ChannelStripComponent
=======
from . import ChannelStripComponent, RightAlignTracksTrackAssigner, SimpleTrackAssigner
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
ASCII_A = 97

def send_letter_to_index(send_letter):
    return ord(send_letter) - ASCII_A


class MixerComponent(Component):
<<<<<<< HEAD
    prehear_volume_control = MappedControl()
    crossfader_control = MappedControl()
    cycle_send_index_button = ButtonControl(color='Mixer.CycleSendIndex',
      pressed_color='Mixer.CycleSendIndexPressed',
      disabled_color='Mixer.CycleSendIndexDisabled')

    @depends(session_ring=None, target_track=None)
    def __init__(self, name='Mixer', session_ring=None, target_track=None, channel_strip_component_type=None, target_can_be_master=True, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._target_track = target_track
        self._provider = session_ring
        self._MixerComponent__on_offset_changed.subject = self._provider
        self.register_slot(self._provider, self._reassign_tracks, 'tracks')
=======
    cycle_send_index_button = ButtonControl(color='Mixer.CycleSendIndex',
      pressed_color='Mixer.CycleSendIndexPressed',
      disabled_color='Mixer.CycleSendIndexDisabled')
    prehear_volume_control = MappedControl()
    crossfader_control = MappedControl()

    @depends(session_ring=None)
    def __init__(self, name='Mixer', session_ring=None, track_assigner=None, right_align_returns=False, channel_strip_component_type=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        if track_assigner is None:
            track_assigner = RightAlignTracksTrackAssigner() if right_align_returns else SimpleTrackAssigner()
        self._track_assigner = track_assigner
        self._provider = session_ring
        self._MixerComponent__on_offset_changed.subject = self._provider
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        self._send_index = 0
        self._send_controls = None
        channel_strip_component_type = channel_strip_component_type or ChannelStripComponent
        self._channel_strips = []
        for _ in range(self._provider.num_tracks):
            strip = channel_strip_component_type(parent=self)
            self._channel_strips.append(strip)

<<<<<<< HEAD
        self._reassign_tracks()
        self._target_can_be_master = target_can_be_master
        self._target_strip = channel_strip_component_type(parent=self)
        self._MixerComponent__on_target_track_changed.subject = self._target_track
        self._update_target_strip()
=======
        self.register_slot(self.song, self._reassign_tracks, 'visible_tracks')
        self._reassign_tracks()
        self._selected_strip = channel_strip_component_type(parent=self)
        self._MixerComponent__on_selected_track_changed.subject = self.song.view
        self._update_selected_strip()
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        self._MixerComponent__on_return_tracks_changed.subject = self.song
        self._MixerComponent__on_return_tracks_changed()
        self._master_strip = channel_strip_component_type(parent=self)
        self._master_strip.set_track(self.song.master_track)

    def channel_strip(self, index):
        return self._channel_strips[index]

    @property
    def master_strip(self):
        return self._master_strip

    @property
<<<<<<< HEAD
    def target_strip(self):
        return self._target_strip
=======
    def selected_strip(self):
        return self._selected_strip
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    @property
    def num_sends(self):
        return len(self.song.return_tracks)

    @property
    def send_index(self):
        return self._send_index

    @send_index.setter
    def send_index(self, index):
        if index is not None:
            index = self._clamp_to_num_sends(index)
        if self._send_index != index:
            self._send_index = index
            self.set_send_controls(self._send_controls)

    def _clamp_to_num_sends(self, value):
        return clamp(value, 0, self.num_sends - 1)

    def set_prehear_volume_control(self, control):
        self.prehear_volume_control.set_control_element(control)

    def set_crossfader_control(self, control):
        self.crossfader_control.set_control_element(control)

    def set_cycle_send_index_button(self, button):
        self.cycle_send_index_button.set_control_element(button)

<<<<<<< HEAD
    def set_shift_button(self, button):
        for strip in self._channel_strips:
            strip.shift_button.set_control_element(button)

=======
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    def set_send_controls(self, controls):
        self._send_controls = controls
        for strip, control in zip_longest(self._channel_strips, controls or []):
            if self._send_index is None:
                strip.send_controls.set_control_element((control,))
            else:
                strip.send_controls.set_control_element((None, ) * self._send_index + (control,))
                strip.update()

    def __getattr__(self, name):
        if name.startswith('set_master_track'):
<<<<<<< HEAD
            return partial(self._set_master_or_target_strip_control, self._master_strip, name.replace('set_master_track_', ''))
        if name.startswith('set_target_track'):
            if 'send' in name:
                if not name.endswith('send_controls'):
                    return partial(self._set_target_strip_indexed_send_control, send_letter_to_index(name.split('_')[-2]))
                return partial(self._set_master_or_target_strip_control, self._target_strip, name.replace('set_target_track_', ''))
        if 'send' in name:
            if not name.endswith('send_controls'):
                return partial(self._set_indexed_send_controls, send_letter_to_index(name.split('_')[-2]))
=======
            return partial(self._set_master_or_selected_strip_control, self._master_strip, name.replace('set_master_track_', ''))
        if name.startswith('set_selected_track'):
            if 'send' in name:
                if not name.endswith('send_controls'):
                    return partial(self._set_selected_strip_indexed_send_control, send_letter_to_index(name.split('_')[(-2)]))
                return partial(self._set_master_or_selected_strip_control, self._selected_strip, name.replace('set_selected_track_', ''))
        if 'send' in name:
            if not name.endswith('send_controls'):
                return partial(self._set_indexed_send_controls, send_letter_to_index(name.split('_')[(-2)]))
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
            if name.startswith('set'):
                return partial(self._set_strip_controls, name[4:-1])
        raise AttributeError

    @staticmethod
<<<<<<< HEAD
    def _set_master_or_target_strip_control(strip, name, control):
        getattr(strip, name).set_control_element(control)

    def _set_target_strip_indexed_send_control(self, send_index, control):
        self._target_strip.set_indexed_send_control(control, send_index)
=======
    def _set_master_or_selected_strip_control(strip, name, control):
        getattr(strip, name).set_control_element(control)

    def _set_selected_strip_indexed_send_control(self, send_index, control):
        self._selected_strip.set_indexed_send_control(control, send_index)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def _set_indexed_send_controls(self, send_index, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            strip.set_indexed_send_control(control, send_index)

    def _set_strip_controls(self, name, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            getattr(strip, name).set_control_element(control)

    @cycle_send_index_button.pressed
    def cycle_send_index_button(self, _):
        self.cycle_send_index()

    def cycle_send_index(self):
        if self.num_sends:
            self.send_index = (self._send_index + 1) % self.num_sends

    @listens('offset')
    def __on_offset_changed(self, *_):
        self._reassign_tracks()

    def _reassign_tracks(self):
<<<<<<< HEAD
        for track, channel_strip in zip(self._provider.tracks, self._channel_strips):
            channel_strip.set_track(track)

    @listens('target_track')
    def __on_target_track_changed(self):
        self._update_target_strip()

    def _update_target_strip(self):
        target_track = self._target_track.target_track
        if self._target_can_be_master or target_track != self.song.master_track:
            self._target_strip.set_track(target_track)
        else:
            self._target_strip.set_track(None)
=======
        tracks = self._track_assigner.tracks(self._provider)
        for track, channel_strip in zip(tracks, self._channel_strips):
            channel_strip.set_track(track)

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self._update_selected_strip()

    def _update_selected_strip(self):
        selected_track = self.song.view.selected_track
        if selected_track != self.song.master_track:
            self._selected_strip.set_track(selected_track)
        else:
            self._selected_strip.set_track(None)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    @listens('return_tracks')
    def __on_return_tracks_changed(self):
        self._update_send_index()
        self._update_cycle_send_index_button()

    def _update_send_index(self):
        num_sends = self.num_sends
        if self._send_index is not None:
            self.send_index = self._clamp_to_num_sends(self._send_index) if num_sends > 0 else None
        else:
            self.send_index = 0 if num_sends > 0 else None

    def update(self):
        super().update()
        if self.is_enabled():
            master_track = self.song.master_track
            self.prehear_volume_control.mapped_parameter = master_track.mixer_device.cue_volume
            self.crossfader_control.mapped_parameter = master_track.mixer_device.crossfader
        else:
            self.prehear_volume_control.mapped_parameter = None
            self.crossfader_control.mapped_parameter = None

    def _update_cycle_send_index_button(self):
        self.cycle_send_index_button.enabled = self.num_sends