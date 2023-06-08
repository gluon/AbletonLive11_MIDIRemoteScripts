<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from ...base import clamp, delete_notes_with_pitch, depends, first, listens, listens_group, liveobj_changed, liveobj_valid
from ..controls import ButtonControl
from ..skin import LiveObjSkinEntry
from .drum_group_scroll import DrumGroupScrollComponent
from .playable import PlayableComponent
DEFAULT_DRUM_TRANSLATION_CHANNEL = 15
BASE_DRUM_GROUP_NOTE = 36

class DrumGroupComponent(PlayableComponent):
    mute_button = ButtonControl(color=None)
    solo_button = ButtonControl(color=None)
    delete_button = ButtonControl(color=None)
    quantize_button = ButtonControl(color=None)

    @depends(set_pad_translations=None, target_track=None)
    def __init__(self, name='Drum_Group', translation_channel=DEFAULT_DRUM_TRANSLATION_CHANNEL, set_pad_translations=None, target_track=None, scroll_component_type=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._target_track = target_track
        self._translation_channel = translation_channel
        self._set_pad_translations = set_pad_translations
        scroll_component_type = scroll_component_type or DrumGroupScrollComponent
        self._drum_group_scroller = scroll_component_type(parent=self)
        self._drum_group_device = None
        self._selected_drum_pad = None
        self._all_drum_pads = []
        self._assigned_drum_pads = []

    @property
    def has_assigned_drum_pads(self):
        return self._assigned_drum_pads and liveobj_valid(first(self._assigned_drum_pads))

    @property
    def assigned_drum_pads(self):
        return self._assigned_drum_pads

    def set_matrix(self, matrix):
        super().set_matrix(matrix)
        self._update_assigned_drum_pads()
        self._create_and_set_pad_translations()
        if self._any_modifier_pressed():
            self._set_control_pads_from_script(True)

    def __getattr__(self, name):
        if name.startswith('set_'):
            if 'scroll' in name:
                return getattr(self._drum_group_scroller, name)
        raise AttributeError

    def set_drum_group_device(self, drum_group_device):
        if liveobj_changed(drum_group_device, self._drum_group_device):
            self._drum_group_device = drum_group_device
            self._drum_group_scroller.set_drum_group_device(drum_group_device)
            drum_group_view = drum_group_device.view if drum_group_device else None
            self._DrumGroupComponent__on_visible_drum_pads_changed.subject = drum_group_device
            self._DrumGroupComponent__on_selected_drum_pad_changed.subject = drum_group_view
            self._DrumGroupComponent__on_drum_pads_scroll_position_changed.subject = drum_group_view
            self._DrumGroupComponent__on_chains_changed.subject = drum_group_device
            self._update_drum_pad_listeners()
            self._update_selected_drum_pad()
            self._update_note_translations()
            super().update()
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/drum_group.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 2811 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as DrumGroupComponentBase
from ...base import add_scroll_encoder, depends, liveobj_valid, skin_scroll_buttons
from . import PlayableComponent
DEFAULT_TRANSLATION_CHANNEL = 15

class DrumGroupComponent(DrumGroupComponentBase):

    @depends(full_velocity=None)
    def __init__(self, name='Drum_Group', translation_channel=DEFAULT_TRANSLATION_CHANNEL, full_velocity=None, *a, **k):
        (super().__init__)(a, name=name, translation_channel=translation_channel, **k)
        self.mute_button.color = 'DrumGroup.Mute'
        self.mute_button.pressed_color = 'DrumGroup.MutePressed'
        self.solo_button.color = 'DrumGroup.Solo'
        self.solo_button.pressed_color = 'DrumGroup.SoloPressed'
        add_scroll_encoder(self._position_scroll)
        for scroll in (self._position_scroll, self._page_scroll):
            skin_scroll_buttons(scroll, 'DrumGroup.Scroll', 'DrumGroup.ScrollPressed')

        self.set_full_velocity(full_velocity)

    def set_scroll_encoder(self, encoder):
        self._position_scroll.scroll_encoder.set_control_element(encoder)

    def set_drum_group_device(self, drum_group_device):
        super().set_drum_group_device(drum_group_device)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        if not liveobj_valid(self._drum_group_device):
            self._update_assigned_drum_pads()
            self._update_led_feedback()

<<<<<<< HEAD
    def quantize_pitch(self, note):
        pass

    def delete_pitch(self, drum_pad):
        pass

    def select_drum_pad(self, drum_pad):
        pass

    def _on_matrix_pressed(self, button):
        if not liveobj_valid(self._drum_group_device):
            return
        selected_drum_pad = self._pad_for_button(button)
        if self.mute_button.is_pressed:
            selected_drum_pad.mute = not selected_drum_pad.mute
        if self.solo_button.is_pressed:
            selected_drum_pad.solo = not selected_drum_pad.solo
        if self.quantize_button.is_pressed:
            button.color = 'DrumGroup.PadAction'
            self.quantize_pitch(selected_drum_pad.note)
        if self.delete_button.is_pressed:
            button.color = 'DrumGroup.PadAction'
            delete_notes_with_pitch(self._target_track.target_clip, selected_drum_pad.note)
            self.delete_pitch(selected_drum_pad)
        if self.select_button.is_pressed:
            self._drum_group_device.view.selected_drum_pad = selected_drum_pad
            self.select_drum_pad(selected_drum_pad)
            super()._on_matrix_pressed(button)
        if self.mute_button.is_pressed or self.solo_button.is_pressed:
            self._update_led_feedback()

    @mute_button.value
    def mute_button(self, _, button):
        self._set_control_pads_from_script(button.is_pressed)

    @solo_button.value
    def solo_button(self, _, button):
        self._set_control_pads_from_script(button.is_pressed)

    @delete_button.value
    def delete_button(self, _, button):
        self._set_control_pads_from_script(button.is_pressed)

    @quantize_button.value
    def quantize_button(self, _, button):
        self._set_control_pads_from_script(button.is_pressed)

    def _any_modifier_pressed(self):
        return any([
         self.select_button.is_pressed,
         self.mute_button.is_pressed,
         self.solo_button.is_pressed,
         self.delete_button.is_pressed,
         self.quantize_button.is_pressed])

    def _update_led_feedback(self):
        for button in self.matrix:
            self._update_button_color(button)
=======
    def _update_led_feedback(self):
        PlayableComponent._update_led_feedback(self)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def _update_button_color(self, button):
        pad = self._pad_for_button(button)
        button.color = self._color_for_pad(pad) if pad else 'DrumGroup.PadEmpty'

    def _color_for_pad(self, pad):
        button_color = 'DrumGroup.PadEmpty'
<<<<<<< HEAD
        is_selected = pad == self._selected_drum_pad
        if is_selected:
            button_color = 'DrumGroup.PadSelected'
        if pad.chains:
            format_str = 'Selected' if is_selected else ''
            if pad.mute:
                button_color = 'DrumGroup.PadMuted{}'.format(format_str)
            else:
                if pad.solo:
                    button_color = 'DrumGroup.PadSoloed{}'.format(format_str)
                else:
                    if not is_selected:
                        button_color = self._filled_color(pad)
            return button_color

    @staticmethod
    def _filled_color(pad):
        return LiveObjSkinEntry('DrumGroup.PadFilled', pad.chains[0])

    def _update_assigned_drum_pads(self):
        assigned_drum_pads = []
        visible_drum_pads = self._drum_group_device.visible_drum_pads if liveobj_valid(self._drum_group_device) else None
        if visible_drum_pads:
            if self._all_drum_pads:
                first_pad = first(visible_drum_pads)
                if first_pad:
                    size = self.width * self.height
                    first_note = first_pad.note
                    if first_note > 128 - size:
                        size = 128 - first_note
                    offset = clamp(first_note, 0, 128 - len(visible_drum_pads))
                    assigned_drum_pads = self._all_drum_pads[offset:offset + size]
        self._assigned_drum_pads = assigned_drum_pads

    def _update_drum_pad_listeners(self):
        if liveobj_valid(self._drum_group_device):
            self._all_drum_pads = self._drum_group_device.drum_pads
            visible_drum_pads = self._drum_group_device.visible_drum_pads
            self._DrumGroupComponent__on_solo_changed.replace_subjects(visible_drum_pads)
            self._DrumGroupComponent__on_mute_changed.replace_subjects(visible_drum_pads)
            self._DrumGroupComponent__on_color_changed.replace_subjects([pad.chains[0] for pad in visible_drum_pads if pad.chains])
            self._update_assigned_drum_pads()
            self._update_note_translations()

    def _update_selected_drum_pad(self):
        selected_drum_pad = self._drum_group_device.view.selected_drum_pad if liveobj_valid(self._drum_group_device) else None
        if liveobj_changed(self._selected_drum_pad, selected_drum_pad):
            self._selected_drum_pad = selected_drum_pad
            self._update_led_feedback()

    def _update_note_translations(self):
        if self._assigned_drum_pads:
            if not self._can_set_pad_translations():
                super()._update_note_translations()

    def _pad_for_button(self, button):
        if self.has_assigned_drum_pads:
            index = self._button_coordinates_to_pad_index(first(self._assigned_drum_pads).note, button.coordinate)
            if index < 128:
                return self._all_drum_pads[index]
            return

    def _note_translation_for_button(self, button):
        identifier = None
        channel = None
        if self.has_assigned_drum_pads:
            identifier = self._button_coordinates_to_pad_index(first(self._assigned_drum_pads).note, button.coordinate)
            channel = self._translation_channel
        return (
         identifier, channel)
=======
        if pad == self._selected_drum_pad:
            button_color = 'DrumGroup.PadSelected'
            if pad.mute:
                button_color = 'DrumGroup.PadMutedSelected'
            elif pad.solo:
                button_color = 'DrumGroup.PadSoloedSelected'
        elif pad.chains:
            button_color = 'DrumGroup.PadFilled'
            if pad.mute:
                button_color = 'DrumGroup.PadMuted'
            elif pad.solo:
                button_color = 'DrumGroup.PadSoloed'
        return button_color
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def _button_coordinates_to_pad_index(self, first_note, coordinates):
        y, x = coordinates
        inverted_y = self.height - y - 1
        index = first_note + 4 * inverted_y + x
        if x >= 4:
            index += y * 4 + inverted_y * 4
<<<<<<< HEAD
        return index

    def _can_set_pad_translations(self):
        return self.width <= 4 and self.height <= 4

    def _create_and_set_pad_translations(self):

        def create_translation_entry(button):
            row, col = button.coordinate
            return (
             col, row, button.identifier, button.channel)

        if self._can_set_pad_translations():
            translations = []
            for button in self.matrix:
                button.channel = self._translation_channel
                button.identifier = self._button_coordinates_to_pad_index(BASE_DRUM_GROUP_NOTE, button.coordinate)
                button.enabled = True
                translations.append(create_translation_entry(button))

            self._set_pad_translations(tuple(translations))
        else:
            self._update_note_translations()
            self._set_pad_translations(None)

    @listens_group('solo')
    def __on_solo_changed(self, _):
        self._update_led_feedback()

    @listens_group('mute')
    def __on_mute_changed(self, _):
        self._update_led_feedback()

    @listens_group('color')
    def __on_color_changed(self, _):
        self._update_led_feedback()

    @listens('visible_drum_pads')
    def __on_visible_drum_pads_changed(self):
        self._update_drum_pad_listeners()
        self._update_led_feedback()

    @listens('drum_pads_scroll_position')
    def __on_drum_pads_scroll_position_changed(self):
        self._update_note_translations()
        self._update_led_feedback()

    @listens('selected_drum_pad')
    def __on_selected_drum_pad_changed(self):
        self._update_selected_drum_pad()

    @listens('chains')
    def __on_chains_changed(self):
        self._update_led_feedback()
=======
        return index
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
