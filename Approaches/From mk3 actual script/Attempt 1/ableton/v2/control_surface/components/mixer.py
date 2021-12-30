#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/components/mixer.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from builtins import zip
from future.moves.itertools import zip_longest
from ...base import clamp, listens, liveobj_valid
from ..component import Component
from .channel_strip import ChannelStripComponent, release_control

class TrackAssigner(object):

    def tracks(self, tracks_provider):
        raise NotImplementedError


class SimpleTrackAssigner(TrackAssigner):

    def tracks(self, tracks_provider):
        tracks = list(tracks_provider.controlled_tracks())
        if len(tracks) < tracks_provider.num_tracks:
            num_empty_track_slots = tracks_provider.num_tracks - len(tracks)
            tracks += [None] * num_empty_track_slots
        return tracks


class RightAlignTracksTrackAssigner(TrackAssigner):
    u"""
    Track assigner which aligns certain tracks to the right, leaving a gap
    between regular and right-aligned tracks (if applicable). Useful for
    e.g. right-aligning return tracks.
    """

    def __init__(self, song = None, include_master_track = False, *a, **k):
        super(RightAlignTracksTrackAssigner, self).__init__(*a, **k)
        self._song = song
        self._include_master_track = include_master_track

    def tracks(self, tracks_provider):
        offset = tracks_provider.track_offset
        tracks = tracks_provider.tracks_to_use()
        tracks_to_right_align = list(self._song.return_tracks) + ([self._song.master_track] if self._include_master_track else [])
        size = tracks_provider.num_tracks
        num_empty_tracks = max(0, size + offset - len(tracks))
        track_list = size * [None]
        for i in range(size):
            track_index = i + offset
            if len(tracks) > track_index:
                track = tracks[track_index]
                empty_offset = 0 if tracks[track_index] not in tracks_to_right_align else num_empty_tracks
                track_list[i + empty_offset] = track

        return track_list


class MixerComponent(Component):
    u""" Class encompassing several channel strips to form a mixer """

    def __init__(self, tracks_provider = None, track_assigner = None, auto_name = False, invert_mute_feedback = False, channel_strip_component_type = None, *a, **k):
        assert tracks_provider is not None
        super(MixerComponent, self).__init__(*a, **k)
        self._channel_strip_component_type = channel_strip_component_type or ChannelStripComponent
        self._track_assigner = track_assigner if track_assigner is not None else RightAlignTracksTrackAssigner(song=self.song)
        self._provider = tracks_provider
        self.__on_offset_changed.subject = tracks_provider
        self._send_index = 0
        self._prehear_volume_control = None
        self._crossfader_control = None
        self._send_controls = None
        self._channel_strips = []
        self._offset_can_start_after_tracks = False
        for _ in range(self._provider.num_tracks):
            strip = self._channel_strip_component_type(parent=self)
            self._channel_strips.append(strip)
            if invert_mute_feedback:
                strip.set_invert_mute_feedback(True)

        self._master_strip = self._channel_strip_component_type(parent=self)
        self._master_strip.set_track(self.song.master_track)
        self._selected_strip = self._channel_strip_component_type(parent=self)
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_track_changed()
        self._reassign_tracks()
        if auto_name:
            self._auto_name()
        self.__on_track_list_changed.subject = self.song
        self.__on_return_tracks_changed.subject = self.song
        self.__on_return_tracks_changed()

    def disconnect(self):
        super(MixerComponent, self).disconnect()
        release_control(self._prehear_volume_control)
        release_control(self._crossfader_control)
        self._prehear_volume_control = None
        self._crossfader_control = None

    @property
    def send_index(self):
        return self._send_index

    @send_index.setter
    def send_index(self, index):
        if index is None or 0 <= index < self.num_sends:
            if self._send_index != index:
                self._send_index = index
                self.set_send_controls(self._send_controls)
                self.on_send_index_changed()
        else:
            raise IndexError

    def on_send_index_changed(self):
        pass

    @property
    def num_sends(self):
        return len(self.song.return_tracks)

    def channel_strip(self, index):
        assert index in range(len(self._channel_strips))
        return self._channel_strips[index]

    def master_strip(self):
        return self._master_strip

    def selected_strip(self):
        return self._selected_strip

    def set_prehear_volume_control(self, control):
        release_control(self._prehear_volume_control)
        self._prehear_volume_control = control
        self.update()

    def set_crossfader_control(self, control):
        release_control(self._crossfader_control)
        self._crossfader_control = control
        self.update()

    def set_volume_controls(self, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            strip.set_volume_control(control)

    def set_pan_controls(self, controls):
        for strip, control in zip_longest(self._channel_strips, controls or []):
            strip.set_pan_control(control)

    def set_send_controls(self, controls):
        self._send_controls = controls
        for strip, control in zip_longest(self._channel_strips, controls or []):
            if self._send_index is None:
                strip.set_send_controls(None)
            else:
                strip.set_send_controls((None,) * self._send_index + (control,))

    def set_arm_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_arm_button(button)

    def set_solo_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_solo_button(button)

    def set_mute_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_mute_button(button)

    def set_track_select_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_select_button(button)

    def set_shift_button(self, button):
        for strip in self._channel_strips or []:
            strip.set_shift_button(button)

    @listens(u'offset')
    def __on_offset_changed(self, *a):
        self._reassign_tracks()

    @listens(u'visible_tracks')
    def __on_track_list_changed(self):
        self._reassign_tracks()

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        self._update_selected_strip()
        self._on_selected_track_changed()

    def _update_selected_strip(self):
        selected_track = self.song.view.selected_track
        if liveobj_valid(self._selected_strip):
            if selected_track != self.song.master_track:
                self._selected_strip.set_track(selected_track)
            else:
                self._selected_strip.set_track(None)

    def _on_selected_track_changed(self):
        pass

    @listens(u'return_tracks')
    def __on_return_tracks_changed(self):
        self._update_send_index()
        self.on_num_sends_changed()

    def _update_send_index(self):
        num_sends = self.num_sends
        if self._send_index is not None:
            self.send_index = clamp(self._send_index, 0, num_sends - 1) if num_sends > 0 else None
        else:
            self.send_index = 0 if num_sends > 0 else None

    def on_num_sends_changed(self):
        pass

    def update(self):
        super(MixerComponent, self).update()
        master_track = self.song.master_track
        if self.is_enabled():
            if self._prehear_volume_control != None:
                self._prehear_volume_control.connect_to(master_track.mixer_device.cue_volume)
            if self._crossfader_control != None:
                self._crossfader_control.connect_to(master_track.mixer_device.crossfader)
        else:
            release_control(self._prehear_volume_control)
            release_control(self._crossfader_control)

    def _reassign_tracks(self):
        tracks = self._track_assigner.tracks(self._provider)
        for track, channel_strip in zip(tracks, self._channel_strips):
            channel_strip.set_track(track)

    def _auto_name(self):
        self.name = u'Mixer'
        self.master_strip().name = u'Master_Channel_Strip'
        self.selected_strip().name = u'Selected_Channel_Strip'
        for index, strip in enumerate(self._channel_strips):
            strip.name = u'Channel_Strip_%d' % index
