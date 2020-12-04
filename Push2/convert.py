#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/convert.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from builtins import map
from builtins import object
from functools import partial
import Live
from ableton.v2.base import EventObject, find_if, listenable_property, listens, liveobj_valid, old_hasattr, task
from ableton.v2.control_surface import Component, find_instrument_devices
from ableton.v2.control_surface.control import ButtonControl, control_list
from .colors import UNCOLORED_INDEX
from .decoration import find_decorated_object
from .device_decoration import SimplerDecoratedPropertiesCopier
from .drum_group_component import find_all_simplers_on_pad, find_simplers
from .mixable_utilities import find_drum_rack_instrument, find_simpler, is_audio_track, is_midi_track
from .track_selection import SelectedMixerTrackProvider

def possible_conversions(track, decorator_factory = None):
    category = NullConvertCategory()
    if liveobj_valid(track):
        if is_midi_track(track) and len(track.devices) > 0:
            drum_rack = find_drum_rack_instrument(track)
            if liveobj_valid(drum_rack):
                drum_pad = drum_rack.view.selected_drum_pad
                if liveobj_valid(drum_pad) and len(drum_pad.chains) == 1 and find_instrument_devices(drum_pad.chains[0]):
                    category = MidiTrackWithDrumRack(actions=[DrumPadToMidiTrack()], drum_pad=drum_pad, track=track)
            else:
                simpler = find_simpler(track)
                if simpler != None and simpler.playback_mode == Live.SimplerDevice.PlaybackMode.slicing:
                    category = MidiTrackWithSimpler(actions=[SlicesToDrumRack()], device=simpler, track=track)
                else:
                    category = MidiTrackWithoutSimpler(actions=[MoveDeviceChain()], device=simpler, track=track, decorator_factory=decorator_factory)
        elif is_audio_track(track):
            detail_clip = track.canonical_parent.view.detail_clip
            song = track.canonical_parent
            if liveobj_valid(detail_clip) and detail_clip.is_arrangement_clip:
                if not detail_clip.is_recording:
                    actions = [CreateTrackWithSimpler(), CreateTrackWithClipInDrumRackPad()]
                    if Live.Conversions.is_convertible_to_midi(song, detail_clip):
                        actions.extend([ConvertAudioClipToHarmonyMidi(), ConvertAudioClipToMelodyMidi(), ConvertAudioClipToDrumsMidi()])
                    category = AudioTrackWithArrangementClip(actions=actions, song_view=track.canonical_parent.view, track=track)
            else:
                highlighted_clip_slot = track.canonical_parent.view.highlighted_clip_slot
                clip_slot = find_if(lambda slot: slot.has_clip and highlighted_clip_slot == slot, track.clip_slots)
                if liveobj_valid(clip_slot) and not clip_slot.is_recording:
                    actions = [CreateTrackWithSimpler(), CreateTrackWithClipInDrumRackPad()]
                    if Live.Conversions.is_convertible_to_midi(song, clip_slot.clip):
                        actions.extend([ConvertAudioClipToHarmonyMidi(), ConvertAudioClipToMelodyMidi(), ConvertAudioClipToDrumsMidi()])
                    category = AudioTrackWithSessionClip(actions=actions, clip_slot=highlighted_clip_slot, track=track)
    return category


class ConvertAction(object):
    needs_deferred_invocation = False

    @staticmethod
    def conversion(song, *a):
        raise NotImplementedError


class ConvertCategory(EventObject):
    __events__ = (u'action_invalidated',)
    color_source = None
    name_source = None

    def __init__(self, actions = [], color_source = None, name_source = None, *a, **k):
        super(ConvertCategory, self).__init__(*a, **k)
        self.actions = actions
        self.color_source = color_source
        self.name_source = name_source

    def convert(self, song, action_index):
        raise NotImplementedError


class NullConvertCategory(ConvertCategory):

    def convert(self, song, action_index):
        assert False, u'Cannot call convert on NullConvertCategory'


class TrackBasedConvertCategory(ConvertCategory):

    def __init__(self, track = None, *a, **k):
        assert liveobj_valid(track)
        super(TrackBasedConvertCategory, self).__init__(color_source=track, name_source=track, *a, **k)
        self._track = track


class MoveDeviceChain(ConvertAction):
    label = u'Drum Pad'

    @staticmethod
    def conversion(song, track_index):
        return Live.Conversions.move_devices_on_track_to_new_drum_rack_pad(song, track_index)


class MidiTrackWithoutSimpler(TrackBasedConvertCategory):
    internal_name = u'midi_track_to_drum_pad'

    def __init__(self, device = None, decorator_factory = None, *a, **k):
        super(MidiTrackWithoutSimpler, self).__init__(*a, **k)
        self._decorator_factory = decorator_factory
        if old_hasattr(device, u'playback_mode'):
            self.__on_playback_mode_changed.subject = device

    def convert(self, song, action):
        self._track.stop_all_clips()
        track_index = list(song.tracks).index(self._track)
        copiers = self._create_copiers()
        drum_pad = action.conversion(song, track_index)
        if liveobj_valid(drum_pad) and copiers:
            self._apply_simpler_properties(drum_pad, song, copiers)

    @listens(u'playback_mode')
    def __on_playback_mode_changed(self):
        self.notify_action_invalidated()

    def _apply_simpler_properties(self, drum_pad, song, copiers):
        destination_simplers = find_all_simplers_on_pad(drum_pad)
        for copier, destination in zip(copiers, destination_simplers):
            if copier:
                copier.apply_properties(destination, song)

    def _create_copiers(self):

        def create_copier_if_decorated(simpler):
            decorated = find_decorated_object(simpler, self._decorator_factory)
            if decorated:
                return SimplerDecoratedPropertiesCopier(decorated, self._decorator_factory)

        return list(map(create_copier_if_decorated, find_simplers(self._track)))


class CreateTrackWithSimpler(ConvertAction):
    label = u'Simpler'

    @staticmethod
    def conversion(song, clip):
        Live.Conversions.create_midi_track_with_simpler(song, clip)


class CreateTrackWithClipInDrumRackPad(ConvertAction):
    label = u'Drum Pad'

    @staticmethod
    def conversion(song, clip):
        Live.Conversions.create_drum_rack_from_audio_clip(song, clip)


class ConvertAudioClipToMidi(ConvertAction):
    conversion_type = None

    def conversion(self, song, clip):
        Live.Conversions.audio_to_midi_clip(song, clip, self.conversion_type)


class ConvertAudioClipToHarmonyMidi(ConvertAudioClipToMidi):
    label = u'Harmony-MIDI'
    conversion_type = Live.Conversions.AudioToMidiType.harmony_to_midi


class ConvertAudioClipToMelodyMidi(ConvertAudioClipToMidi):
    label = u'Melody-MIDI'
    conversion_type = Live.Conversions.AudioToMidiType.melody_to_midi


class ConvertAudioClipToDrumsMidi(ConvertAudioClipToMidi):
    label = u'Drums-MIDI'
    conversion_type = Live.Conversions.AudioToMidiType.drums_to_midi


class AudioTrackWithSessionClip(ConvertCategory):
    internal_name = u'audio_clip_to_simpler'

    def __init__(self, clip_slot = None, track = None, *a, **k):
        assert liveobj_valid(clip_slot)
        assert liveobj_valid(track)
        super(AudioTrackWithSessionClip, self).__init__(name_source=clip_slot.clip, color_source=clip_slot.clip, *a, **k)
        self._clip_slot = clip_slot
        self._track = track
        self.__on_has_clip_changed.subject = self._clip_slot

    def convert(self, song, action):
        self._track.stop_all_clips()
        action.conversion(song, self._clip_slot.clip)

    @listens(u'has_clip')
    def __on_has_clip_changed(self):
        self.notify_action_invalidated()


class AudioTrackWithArrangementClip(ConvertCategory):
    internal_name = u'audio_arrangement_clip_to_simpler'

    def __init__(self, song_view = None, track = None, *a, **k):
        assert liveobj_valid(song_view)
        assert liveobj_valid(track)
        super(AudioTrackWithArrangementClip, self).__init__(name_source=song_view.detail_clip, color_source=song_view.detail_clip, *a, **k)
        self._clip = song_view.detail_clip
        self._track = track
        self.__on_detail_clip_changed.subject = song_view

    def convert(self, song, action):
        self._track.stop_all_clips()
        action.conversion(song, self._clip)

    @listens(u'detail_clip')
    def __on_detail_clip_changed(self):
        self.notify_action_invalidated()


class SlicesToDrumRack(ConvertAction):
    label = u'Drum Rack'
    needs_deferred_invocation = True

    @staticmethod
    def conversion(song, device):
        Live.Conversions.sliced_simpler_to_drum_rack(song, device)


class MidiTrackWithSimpler(TrackBasedConvertCategory):
    internal_name = u'sliced_simpler_to_drum_rack'

    def __init__(self, device = None, *a, **k):
        assert isinstance(device, Live.SimplerDevice.SimplerDevice)
        super(MidiTrackWithSimpler, self).__init__(*a, **k)
        self._device = device
        self.__on_playback_mode_changed.subject = self._device
        self.__on_sample_changed.subject = self._device

    def convert(self, song, action):
        action.conversion(song, self._device)

    @listens(u'playback_mode')
    def __on_playback_mode_changed(self):
        self.notify_action_invalidated()

    @listens(u'sample')
    def __on_sample_changed(self):
        self.notify_action_invalidated()


class DrumPadToMidiTrack(ConvertAction):
    label = u'MIDI track'

    @staticmethod
    def conversion(song, drum_pad):
        Live.Conversions.create_midi_track_from_drum_pad(song, drum_pad)


class MidiTrackWithDrumRack(ConvertCategory):
    internal_name = u'drum_pad_to_midi_track'

    def __init__(self, drum_pad = None, track = None, *a, **k):
        assert liveobj_valid(drum_pad)
        super(MidiTrackWithDrumRack, self).__init__(name_source=drum_pad, color_source=track, *a, **k)
        self.__on_devices_changed.subject = drum_pad.chains[0]
        self.__on_chains_changed.subject = drum_pad
        self._drum_pad = drum_pad

    @listens(u'devices')
    def __on_devices_changed(self):
        self.notify_action_invalidated()

    @listens(u'chains')
    def __on_chains_changed(self):
        self.notify_action_invalidated()

    def convert(self, song, action):
        action.conversion(song, self._drum_pad)


class ConvertComponent(Component):
    __events__ = (u'cancel', u'success')
    action_buttons = control_list(ButtonControl, color=u'Option.Unselected', pressed_color=u'Option.Selected')
    cancel_button = ButtonControl(color=u'Option.Unselected', pressed_color=u'Option.Selected')
    source_color_index = listenable_property.managed(UNCOLORED_INDEX)
    source_name = listenable_property.managed(str(u''))

    def __init__(self, tracks_provider = None, conversions_provider = possible_conversions, decorator_factory = None, *a, **k):
        assert tracks_provider is not None
        assert callable(conversions_provider)
        super(ConvertComponent, self).__init__(*a, **k)
        self._tracks_provider = tracks_provider
        self._conversions_provider = conversions_provider
        self._decorator_factory = decorator_factory
        self._category = NullConvertCategory()
        self._update_possible_conversions()

    @listenable_property
    def available_conversions(self):
        return [ x.label for x in self._category.actions ]

    def on_enabled_changed(self):
        super(ConvertComponent, self).on_enabled_changed()
        self._update_possible_conversions()

    def _update_possible_conversions(self):
        self.disconnect_disconnectable(self._category)
        track = self._tracks_provider.selected_item
        self._category = self.register_disconnectable(self._conversions_provider(track, self._decorator_factory))
        self.__on_action_invalidated.subject = self._category
        self.__on_action_source_color_index_changed.subject = self._category.color_source
        self.__on_action_source_name_changed.subject = self._category.name_source
        self.__on_action_source_color_index_changed()
        self.__on_action_source_name_changed()
        self.action_buttons.control_count = len(self._category.actions)
        self.notify_available_conversions()

    @listens(u'color_index')
    def __on_action_source_color_index_changed(self):
        color_source = self.__on_action_source_color_index_changed.subject
        self.source_color_index = color_source.color_index if color_source and color_source.color_index is not None else UNCOLORED_INDEX

    @listens(u'name')
    def __on_action_source_name_changed(self):
        name_source = self.__on_action_source_name_changed.subject
        self.source_name = name_source.name if name_source else str()

    @action_buttons.released
    def action_buttons(self, button):
        if self._do_conversion(button.index):
            self.notify_cancel()

    def _do_conversion(self, action_index):
        self._update_possible_conversions()
        if action_index < len(self._category.actions):
            action = self._category.actions[action_index]
            if action.needs_deferred_invocation:
                self._tasks.add(task.sequence(task.delay(1), task.run(lambda : self._do_conversion_deferred(action))))
                return False
            self._invoke_conversion(action)
        return True

    def _do_conversion_deferred(self, action):
        self._invoke_conversion(action)
        self.notify_cancel()

    def _invoke_conversion(self, action):
        self._category.convert(self.song, action)
        self.notify_success(self._category.internal_name)

    @cancel_button.released
    def cancel_button(self, button):
        self.notify_cancel()

    @listens(u'action_invalidated')
    def __on_action_invalidated(self):
        self.notify_cancel()


class ConvertEnabler(Component):
    convert_toggle_button = ButtonControl(color=u'DefaultButton.On')

    def __init__(self, enter_dialog_mode = None, exit_dialog_mode = None, *a, **k):
        assert enter_dialog_mode is not None
        assert exit_dialog_mode is not None
        super(ConvertEnabler, self).__init__(*a, **k)
        self._enter_dialog_mode = partial(enter_dialog_mode, u'convert')
        self._exit_dialog_mode = partial(exit_dialog_mode, u'convert')
        self._selected_item = self.register_disconnectable(SelectedMixerTrackProvider(song=self.song))
        self.__on_selected_item_changed.subject = self._selected_item
        self.__on_selected_item_changed(None)
        song = self.song
        self.__on_devices_changed.subject = song.view
        self.__on_selected_scene_changed.subject = song.view
        self.__on_detail_clip_updated.subject = song.view
        self._update_clip_slot_listener()
        self._update_drum_pad_listeners()

    @listens(u'selected_mixer_track')
    def __on_selected_item_changed(self, _):
        self._update_clip_slot_listener()
        self._disable_and_check_enabled_state()

    @convert_toggle_button.pressed
    def convert_toggle_button(self, button):
        self._enter_dialog_mode()

    def _can_enable_mode(self):
        category = possible_conversions(self._selected_item.selected_mixer_track)
        category.disconnect()
        return len(category.actions) > 0

    def _disable_and_check_enabled_state(self):
        self._exit_dialog_mode()
        self.convert_toggle_button.enabled = self._can_enable_mode()

    @listens(u'detail_clip')
    def __on_detail_clip_updated(self):
        self._disable_and_check_enabled_state()

    @listens(u'selected_track.devices')
    def __on_devices_changed(self):
        self._disable_and_check_enabled_state()
        self._update_drum_pad_listeners()

    def _update_drum_pad_listeners(self):
        drum_rack = find_drum_rack_instrument(self._selected_item.selected_mixer_track)
        drum_rack_view_or_none = drum_rack.view if liveobj_valid(drum_rack) else None
        self.__on_selected_drum_pad_changed.subject = drum_rack_view_or_none
        self.__on_drum_pad_chains_changed.subject = drum_rack_view_or_none

    @listens(u'selected_drum_pad')
    def __on_selected_drum_pad_changed(self):
        self._disable_and_check_enabled_state()
        drum_rack_view = self.__on_selected_drum_pad_changed.subject
        if liveobj_valid(drum_rack_view):
            selected_drum_pad = drum_rack_view.selected_drum_pad
            first_chain_or_none = None
            if liveobj_valid(selected_drum_pad):
                first_chain_or_none = selected_drum_pad.chains[0] if len(selected_drum_pad.chains) > 0 else None
            self.__on_drum_pad_chain_devices_changed.subject = first_chain_or_none

    @listens(u'selected_drum_pad.chains')
    def __on_drum_pad_chains_changed(self):
        self._disable_and_check_enabled_state()

    @listens(u'devices')
    def __on_drum_pad_chain_devices_changed(self):
        self._disable_and_check_enabled_state()

    @listens(u'selected_scene')
    def __on_selected_scene_changed(self):
        self._update_clip_slot_listener()
        self._disable_and_check_enabled_state()

    def _update_clip_slot_listener(self):
        clip_slot = self.song.view.highlighted_clip_slot
        self.__on_clip_slot_has_clip_changed.subject = clip_slot

    @listens(u'has_clip')
    def __on_clip_slot_has_clip_changed(self):
        self._disable_and_check_enabled_state()
        clip_slot = self.__on_clip_slot_has_clip_changed.subject
        self._update_clip_listeners(clip_slot)

    def _update_clip_listeners(self, clip_slot):
        self.__on_clip_playing_status_changed.subject = clip_slot.clip
        self.__on_clip_recording_status_changed.subject = clip_slot.clip

    @listens(u'is_recording')
    def __on_clip_recording_status_changed(self):
        self._disable_and_check_enabled_state()

    @listens(u'playing_status')
    def __on_clip_playing_status_changed(self):
        self._disable_and_check_enabled_state()
