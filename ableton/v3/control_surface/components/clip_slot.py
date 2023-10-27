# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\clip_slot.py
# Compiled at: 2023-08-04 12:30:20
# Size of source mod 2**32: 8347 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ...base import const, depends, listens
from ...live import action, display_name, is_track_armed, liveobj_changed, liveobj_valid
from .. import Component
from ..controls import ButtonControl
from ..display import Renderable
from ..skin import LiveObjSkinEntry, OptionalSkinEntry

class ClipSlotComponent(Component, Renderable):
    launch_button = ButtonControl()
    select_button = ButtonControl(color=None)
    delete_button = ButtonControl(color=None)
    duplicate_button = ButtonControl(color=None)
    copy_button = ButtonControl(color=None)
    include_in_top_level_state = False

    @depends(clipboard=(const(None)))
    def __init__(self, clipboard=None, *a, **k):
        (super().__init__)(*a, **k)
        self._clipboard = clipboard
        self._clip_slot = None
        self._non_player_track = None

        def make_property_slot(property_name, update_method):
            return self.register_slot(None, update_method, property_name)

        self._track_property_slots = [
         make_property_slot('arm', self._update_launch_button_color),
         make_property_slot('implicit_arm', self._update_launch_button_color),
         make_property_slot('input_routing_type', self._update_launch_button_color)]
        self._clip_slot_property_slots = [
         make_property_slot('color', self._update_launch_button_color),
         make_property_slot('playing_status', self._update_launch_button_color),
         make_property_slot('has_stop_button', self._update_launch_button_color),
         make_property_slot('has_clip', self._update_clip_property_slots),
         make_property_slot('controls_other_clips', self._update_clip_property_slots)]
        self._clip_property_slots = [
         make_property_slot('color', self._update_launch_button_color),
         make_property_slot('playing_status', self._update_launch_button_color),
         make_property_slot('is_recording', self._update_launch_button_color)]

    @property
    def clip_slot(self):
        return self._clip_slot

    def set_clip_slot(self, clip_slot):
        if liveobj_changed(clip_slot, self._clip_slot):
            self._clip_slot = clip_slot
            for slot in self._clip_slot_property_slots:
                slot.subject = clip_slot

            self._ClipSlotComponent__on_slot_triggered_changed.subject = clip_slot
            self._update_clip_property_slots(update_launch_button=False)
            track = clip_slot.canonical_parent if clip_slot else None
            if track:
                if track in self.song.tracks:
                    for slot in self._track_property_slots:
                        slot.subject = track

            self.update()

    def set_non_player_track(self, track):
        self.set_clip_slot(None)
        self._non_player_track = track

    def set_launch_button(self, button):
        self.launch_button.set_control_element(button)
        self.update()

    @launch_button.pressed
    def launch_button(self, _):
        self._on_launch_button_pressed()

    def _on_launch_button_pressed(self):
        slot_name = display_name(self._clip_slot) if liveobj_valid(self._clip_slot) else ''
        if self.select_button.is_pressed:
            if action.select(self._clip_slot):
                self.notify(self.notifications.Clip.select, slot_name)
            else:
                action.select(self._non_player_track)
        else:
            if self.duplicate_button.is_pressed:
                action.duplicate(self._clip_slot)
            else:
                if self._is_copying():
                    self._clipboard.copy_or_paste(self._clip_slot)
                else:
                    if self.delete_button.is_pressed:
                        if action.delete(self._clip_slot):
                            self.notify(self.notifications.Clip.delete, slot_name)
                        else:
                            self.notify(self.notifications.Clip.error_delete_empty_slot)
                    else:
                        self._do_launch_slot()

    def _do_launch_slot(self):
        action.fire((self._clip_slot), button_state=True)

    @launch_button.released
    def launch_button(self, _):
        self._on_launch_button_released()

    def _on_launch_button_released(self):
        if self.launch_button.is_momentary:
            if not self._any_modifier_pressed():
                if not self._is_copying():
                    action.fire((self._clip_slot), button_state=False)

    def _has_clip(self):
        return liveobj_valid(self._clip_slot) and self._clip_slot.has_clip

    def _is_copying(self):
        return (self.copy_button.is_pressed) or ((self._clipboard) and (self._clipboard.has_content))

    def _any_modifier_pressed(self):
        return self.select_button.is_pressed or self.delete_button.is_pressed or self.duplicate_button.is_pressed or self.copy_button.is_pressed

    def update(self):
        super().update()
        self._update_launch_button_color()

    def _update_launch_button_color(self):
        value_to_send = 'Session.NoSlot'
        if liveobj_valid(self._clip_slot):
            track = self._clip_slot.canonical_parent
            slot_or_clip = self._clip_slot.clip if self._has_clip() else self._clip_slot
            value_to_send = self._feedback_value(track, slot_or_clip)
        self.launch_button.color = value_to_send

    def _feedback_value(self, track, slot_or_clip):
        is_clip = self._has_clip() or getattr(slot_or_clip, 'controls_other_clips', False)
        value = 'Session.Slot'
        if slot_or_clip.is_triggered:
            value = self._triggered_color(slot_or_clip, is_clip)
        else:
            if slot_or_clip.is_playing:
                value = 'Session.Clip{}'.format('Recording' if slot_or_clip.is_recording else 'Playing')
            else:
                if is_clip:
                    value = 'Session.ClipStopped'
                else:
                    if not self._clip_slot.has_stop_button:
                        value = OptionalSkinEntry('Session.SlotLacksStop', 'Session.Slot')
                    else:
                        if is_track_armed(track):
                            if self._clip_slot.has_stop_button:
                                value = 'Session.SlotRecordButton'
        return LiveObjSkinEntry(value, slot_or_clip)

    @staticmethod
    def _triggered_color(slot_or_clip, is_clip):
        rec_or_play = 'Triggered{}'.format('Record' if slot_or_clip.will_record_on_start else 'Play')
        default_value = 'Session.Clip{}'.format(rec_or_play)
        if not is_clip:
            return OptionalSkinEntry('Session.Slot{}'.format(rec_or_play), default_value)
        return default_value

    def _update_clip_property_slots(self, update_launch_button=True):
        clip = self._clip_slot.clip if self._clip_slot else None
        for slot in self._clip_property_slots:
            slot.subject = clip

        if update_launch_button:
            self._update_launch_button_color()

    @listens('is_triggered')
    def __on_slot_triggered_changed(self):
        if not self._has_clip():
            self._update_launch_button_color()