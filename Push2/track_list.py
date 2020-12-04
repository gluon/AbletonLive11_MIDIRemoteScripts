#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/track_list.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import zip
from builtins import filter
from builtins import range
from functools import partial
import Live
from ableton.v2.base import nop, listenable_property, listens, listens_group, liveobj_changed, liveobj_valid, old_hasattr
from ableton.v2.control_surface import Component, find_instrument_devices
from ableton.v2.control_surface.control import ButtonControl, control_list
from ableton.v2.control_surface.mode import ModeButtonBehaviour, ModesComponent
from pushbase.actions import is_clip_stop_pending
from pushbase.consts import MessageBoxText
from pushbase.message_box_component import Messenger
from pushbase.selected_track_parameter_provider import toggle_arm
from pushbase.song_utils import delete_track_or_return_track, find_parent_track
from .colors import DISPLAY_BUTTON_SHADE_LEVEL, IndexedColor, make_blinking_track_color, make_pulsing_track_color
from .mixable_utilities import can_play_clips, is_chain
from .real_time_channel import RealTimeDataComponent
from .skin_default import RECORDING_COLOR, UNLIT_COLOR
from .track_selection import get_all_mixer_tracks, SelectedMixerTrackProvider
DeviceType = Live.Device.DeviceType

def track_color_with_pending_stop(track):
    return make_blinking_track_color(track, UNLIT_COLOR)


def mixable_button_color(mixer_track, song, selected_track = None):
    color = u'Mixer.NoTrack'
    if mixer_track:
        mixer_track_parent_track = find_parent_track(mixer_track.proxied_object)
        is_frozen_chain = mixer_track_parent_track.is_frozen and not isinstance(mixer_track.proxied_object, Live.Track.Track)
        if can_play_clips(mixer_track) and is_clip_stop_pending(mixer_track):
            color = track_color_with_pending_stop(mixer_track)
        elif mixer_track.solo:
            color = u'Mixer.SoloOn'
        elif mixer_track == selected_track and not mixer_track.mute:
            color = u'Mixer.TrackSelected'
        elif mixer_track.mute or mixer_track.muted_via_solo:
            color = u'Mixer.MutedTrack'
        elif is_frozen_chain:
            color = u'Mixer.FrozenChain'
        else:
            color = IndexedColor.from_live_index(mixer_track.color_index, DISPLAY_BUTTON_SHADE_LEVEL)
    return color


def stop_clip_button_color(track, song, _):
    if liveobj_valid(track) and not is_chain(track) and bool(track.clip_slots):
        if is_clip_stop_pending(track):
            return track_color_with_pending_stop(track)
        elif track.playing_slot_index >= 0:
            if track.solo:
                return u'StopClips.SoloedTrack'
            if track.mute:
                return u'StopClips.MutedTrack'
            if track.clip_slots[track.playing_slot_index].is_recording:
                pulse_to = RECORDING_COLOR
            else:
                pulse_to = UNLIT_COLOR
            return make_pulsing_track_color(track, pulse_to)
        else:
            return u'Session.StoppedClip'
    else:
        return u'Mixer.NoTrack'


def toggle_mixable_mute(mixable, song):
    if mixable != song.master_track:
        mixable.mute = not mixable.mute


def toggle_mixable_solo(mixable, song):
    if mixable != song.master_track:
        tracks = get_all_mixer_tracks(song)
        other_solos = any([ track.solo for track in tracks ])
        if other_solos and song.exclusive_solo and not mixable.solo:
            for track in tracks:
                track.solo = False

        mixable.solo = not mixable.solo


def playing_clip(track):
    if old_hasattr(track, u'playing_slot_index'):
        try:
            if track.playing_slot_index >= 0:
                playing_clip_slot = track.clip_slots[track.playing_slot_index]
                if liveobj_valid(playing_clip_slot):
                    return playing_clip_slot.clip
                return None
        except RuntimeError:
            pass


class TrackListBehaviour(ModeButtonBehaviour):

    def press_immediate(self, component, mode):
        component.push_mode(mode)

    def release_delayed(self, component, mode):
        self.release_immediate(component, mode)

    def release_immediate(self, component, mode):
        component.pop_mode(mode)


class TrackListComponent(ModesComponent, Messenger):
    u"""
    Notifies whenever a track action is executed, e.g. deleting or duplicating. But
    selection does *not* count as an action.
    """
    __events__ = (u'mute_solo_stop_cancel_action_performed',)
    track_action_buttons = control_list(ButtonControl, control_count=8)

    def __init__(self, tracks_provider = None, trigger_recording_on_release_callback = nop, color_chooser = None, clip_phase_enabler = None, *a, **k):
        assert tracks_provider is not None
        super(TrackListComponent, self).__init__(*a, **k)
        self.locked_mode = None
        self._button_handler = self._select_mixable
        self._button_feedback_provider = mixable_button_color
        self._color_chooser = color_chooser
        self._track_selected_when_pressed = [False] * self.track_action_buttons.control_count
        self._playheads_real_time_data = [ RealTimeDataComponent(parent=self, channel_type=u'playhead', is_enabled=False) for _ in range(8) ]
        self.clip_phase_enabler = Component(parent=self)
        self.__on_clip_phase_enabler_changed.subject = self.clip_phase_enabler
        self._setup_action_mode(u'select', handler=self._select_mixable)
        self._setup_action_mode(u'lock_override', handler=self._select_mixable)
        self._setup_action_mode(u'delete', handler=self._delete_mixable)
        self._setup_action_mode(u'duplicate', handler=self._duplicate_mixable)
        self._setup_action_mode(u'arm', handler=self._arm_track)
        self._setup_action_mode(u'mute', handler=partial(toggle_mixable_mute, song=self.song))
        self._setup_action_mode(u'solo', handler=partial(toggle_mixable_solo, song=self.song))
        self._setup_action_mode(u'stop', handler=self._stop_track_clip, feedback_provider=stop_clip_button_color)
        self._setup_action_mode(u'select_color', handler=self._select_mixable_color, exit_handler=partial(self._select_mixable_color, None))
        self.selected_mode = u'select'
        self._can_trigger_recording_callback = trigger_recording_on_release_callback
        self._track_provider = tracks_provider
        self._selected_track = self.register_disconnectable(SelectedMixerTrackProvider())
        self.__on_items_changed.subject = self._track_provider
        self.__on_selected_item_changed.subject = self._track_provider
        self.__on_tracks_changed.subject = self.song
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_is_playing_changed.subject = self.song
        self._update_track_and_chain_listeners()
        self._update_playheads_real_time_data()
        self._update_realtime_channels_ability()

    @listenable_property
    def playhead_real_time_channels(self):
        return self._playheads_real_time_data

    @listenable_property
    def tracks(self):
        return self._track_provider.items

    @listenable_property
    def selected_track(self):
        return self._track_provider.selected_item

    @listenable_property
    def absolute_selected_track_index(self):
        song = self.song
        tracks = song.tracks + song.return_tracks + (song.master_track,)
        selected_track = song.view.selected_track
        return list(tracks).index(selected_track)

    def _setup_action_mode(self, name, handler, exit_handler = nop, feedback_provider = mixable_button_color):
        self.add_mode(name, [(partial(self._enter_action_mode, handler=handler, feedback_provider=feedback_provider), exit_handler)], behaviour=TrackListBehaviour())
        self.get_mode_button(name).mode_selected_color = u'DefaultButton.Transparent'
        self.get_mode_button(name).mode_unselected_color = u'DefaultButton.Transparent'

    def _enter_action_mode(self, handler, feedback_provider):
        self._button_handler = handler
        if feedback_provider != self._button_feedback_provider:
            self._button_feedback_provider = feedback_provider
            self._update_all_button_colors()

    @listens(u'tracks')
    def __on_tracks_changed(self):
        self._update_track_and_chain_listeners()
        self._update_playheads_real_time_data()

    @listens_group(u'mute')
    def __on_track_mute_state_changed(self, mixable):
        self._update_mixable_color(self.tracks.index(mixable), mixable)

    @listens_group(u'solo')
    def __on_track_solo_state_changed(self, mixable):
        self._update_mixable_color(self.tracks.index(mixable), mixable)

    @listens_group(u'fired_slot_index')
    def __on_track_fired_slot_changed(self, track):
        self._update_all_button_colors()

    @listens_group(u'playing_slot_index')
    def __on_track_playing_slot_changed(self, _):
        self._update_all_button_colors()
        self._update_playheads_real_time_data()

    @listens(u'items')
    def __on_items_changed(self):
        self._update_track_and_chain_listeners()
        self._update_playheads_real_time_data()

    @listens(u'is_playing')
    def __on_is_playing_changed(self):
        self._update_playheads_real_time_data()

    @listens_group(u'is_frozen')
    def __on_track_is_frozen_state_changed(self, track):
        self._update_all_button_colors()

    def _update_playheads_real_time_data(self):
        if self.song.is_playing:
            for track, real_time_data in zip(self.tracks, self._playheads_real_time_data):
                real_time_data.set_data(playing_clip(track))

        else:
            for track, real_time_data in zip(self.tracks, self._playheads_real_time_data):
                real_time_data.set_data(None)

        self.notify_playhead_real_time_channels()

    def _update_track_and_chain_listeners(self):
        self.notify_tracks()
        tracks = self.tracks
        self.__on_track_color_index_changed.replace_subjects(tracks)
        self.__on_track_mute_state_changed.replace_subjects(tracks)
        self.__on_track_muted_via_solo_changed.replace_subjects(tracks)
        self.__on_track_solo_state_changed.replace_subjects(tracks)
        tracks_without_chains = list(filter(can_play_clips, tracks))
        self.__on_track_fired_slot_changed.replace_subjects(tracks_without_chains)
        self.__on_track_playing_slot_changed.replace_subjects(tracks_without_chains)
        self.__on_track_is_frozen_state_changed.replace_subjects(tracks_without_chains)
        self._update_button_enabled_state()
        self._update_all_button_colors()

    def _update_button_enabled_state(self):
        tracks = self.tracks
        for track, control in zip(tracks, self.track_action_buttons):
            control.enabled = liveobj_valid(track)

    @listens_group(u'color_index')
    def __on_track_color_index_changed(self, mixable):
        self._update_mixable_color(self.tracks.index(mixable), mixable)

    @listens(u'selected_item')
    def __on_selected_item_changed(self):
        self.notify_selected_track()
        self._update_all_button_colors()

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        self.notify_absolute_selected_track_index()

    @listens_group(u'muted_via_solo')
    def __on_track_muted_via_solo_changed(self, mixable):
        self._update_mixable_color(self.tracks.index(mixable), mixable)

    def _update_mixable_color(self, button_index, mixable):
        self.track_action_buttons[button_index].color = self._button_feedback_provider(mixable, self.song, self.selected_track)

    def _update_all_button_colors(self):
        for index, mixable in enumerate(self.tracks):
            self._update_mixable_color(index, mixable)

    @track_action_buttons.pressed
    def track_action_buttons(self, button):
        self._track_selected_when_pressed[button.index] = self._track_provider.selected_item == self.tracks[button.index]
        self._button_handler(self.tracks[button.index])
        if self.selected_mode != u'select':
            self.notify_mute_solo_stop_cancel_action_performed()

    @track_action_buttons.pressed_delayed
    def track_action_buttons(self, button):
        if self.selected_mode == u'select':
            (self._arm_track(self.tracks[button.index]),)

    @track_action_buttons.released_immediately
    def track_action_buttons(self, button):
        if self.selected_mode == u'select' and self._track_selected_when_pressed[button.index]:
            self._toggle_track_fold(self.tracks[button.index])

    def _toggle_track_fold(self, track):
        if old_hasattr(track, u'is_foldable') and track.is_foldable:
            track.fold_state = not track.fold_state
        elif old_hasattr(track, u'is_showing_chains') and track.can_show_chains:
            track.is_showing_chains = not track.is_showing_chains
        else:
            instruments = list(find_instrument_devices(track))
            if instruments:
                instrument = instruments[0]
                if old_hasattr(instrument, u'is_showing_chains') and instrument.can_show_chains:
                    instrument.is_showing_chains = not instrument.is_showing_chains

    def _select_mixable(self, track):
        if liveobj_valid(track) and liveobj_changed(self._track_provider.selected_item, track):
            self._track_provider.selected_item = track

    @staticmethod
    def can_duplicate(track_or_chain, return_tracks):
        unwrapped = track_or_chain.proxied_object
        return isinstance(unwrapped, Live.Track.Track) and unwrapped not in list(return_tracks)

    def _delete_mixable(self, track_or_chain):
        if liveobj_valid(track_or_chain) and not is_chain(track_or_chain):
            try:
                name = track_or_chain.name
                delete_track_or_return_track(self.song, track_or_chain)
                self.show_notification(MessageBoxText.DELETE_TRACK % name)
            except RuntimeError:
                self.show_notification(MessageBoxText.TRACK_DELETE_FAILED)

    def _duplicate_mixable(self, track_or_chain):
        if self.can_duplicate(track_or_chain, self.song.return_tracks):
            try:
                track_index = list(self.song.tracks).index(track_or_chain)
                self.song.duplicate_track(track_index)
                self.show_notification(MessageBoxText.DUPLICATE_TRACK % track_or_chain.name)
                self._update_all_button_colors()
            except Live.Base.LimitationError:
                self.show_notification(MessageBoxText.TRACK_LIMIT_REACHED)
            except RuntimeError:
                self.show_notification(MessageBoxText.TRACK_DUPLICATION_FAILED)

    def _arm_track(self, track_or_chain):
        if not is_chain(track_or_chain) and track_or_chain.can_be_armed:
            song = self.song
            toggle_arm(track_or_chain, song, exclusive=song.exclusive_arm)
        self._can_trigger_recording_callback(False)

    def _stop_track_clip(self, mixable):
        if not is_chain(mixable):
            mixable.stop_all_clips()

    def _select_mixable_color(self, mixable):
        if self._color_chooser is not None:
            self._color_chooser.object = mixable

    @listens(u'enabled')
    def __on_clip_phase_enabler_changed(self, _):
        self._update_realtime_channels_ability()

    def _update_realtime_channels_ability(self):
        for playhead in self._playheads_real_time_data:
            playhead.set_enabled(self.is_enabled() and self.clip_phase_enabler.is_enabled())

    def on_enabled_changed(self):
        super(TrackListComponent, self).on_enabled_changed()
        self._update_realtime_channels_ability()
        if not self.is_enabled():
            self.selected_mode = u'select'
            self.pop_unselected_modes()
        elif self.locked_mode is not None:
            self.push_mode(self.locked_mode)
