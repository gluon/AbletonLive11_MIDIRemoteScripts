# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\drum_group.py
# Compiled at: 2023-09-22 14:37:57
# Size of source mod 2**32: 17106 bytes
from __future__ import absolute_import, print_function, unicode_literals
from typing import cast
from ...base import clamp, depends, first, listenable_property, listens, listens_group
from ...live import action, liveobj_changed, liveobj_valid
from ..controls import ButtonControl
from ..display import Renderable
from ..skin import LiveObjSkinEntry
from .clipboard import ClipboardComponent
from .drum_group_scroll import DrumGroupScrollComponent
from .note_editor import PitchProvider
from .playable import PlayableComponent
DEFAULT_DRUM_TRANSLATION_CHANNEL = 15
BASE_DRUM_GROUP_NOTE = 36

class DrumGroupComponent(PlayableComponent, PitchProvider, Renderable):
    mute_button = ButtonControl(color=None)
    solo_button = ButtonControl(color=None)
    delete_button = ButtonControl(color=None)
    quantize_button = ButtonControl(color=None)
    copy_button = ButtonControl(color=None)

    @depends(set_pad_translations=None, target_track=None)
    def __init__(self, name='Drum_Group', translation_channel=DEFAULT_DRUM_TRANSLATION_CHANNEL, set_pad_translations=None, target_track=None, scroll_component_type=None, clipboard_component_type=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._target_track = target_track
        self._translation_channel = translation_channel
        self._set_pad_translations = set_pad_translations
        scroll_component_type = scroll_component_type or DrumGroupScrollComponent
        self._drum_group_scroller = scroll_component_type(parent=self)
        clipboard_component_type = clipboard_component_type or DrumPadClipboardComponent
        self._clipboard = clipboard_component_type(parent=self)
        self.register_slot(self._clipboard, lambda _: self._set_control_pads_from_script(self._is_copying())
, 'has_content')
        self._drum_group_device = None
        self._selected_drum_pad = None
        self._all_drum_pads = []
        self._assigned_drum_pads = []

    @listenable_property
    def clipboard(self):
        return self._clipboard

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
        if self._any_modifier_pressed() or self._is_copying():
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
            self._clipboard.set_drum_group_device(self._drum_group_device)
            drum_group_view = drum_group_device.view if drum_group_device else None
            self._DrumGroupComponent__on_visible_drum_pads_changed.subject = drum_group_device
            self._DrumGroupComponent__on_selected_drum_pad_changed.subject = drum_group_view
            self._DrumGroupComponent__on_drum_pads_scroll_position_changed.subject = drum_group_view
            self._DrumGroupComponent__on_chains_changed.subject = drum_group_device
            self._update_drum_pad_listeners()
            self._update_selected_drum_pad()
            self._update_note_translations()
            super().update()
        if not liveobj_valid(self._drum_group_device):
            self._update_assigned_drum_pads()
            self._update_led_feedback()

    def set_copy_button(self, button):
        self.copy_button.set_control_element(button)
        self._clipboard.set_copy_button(button)

    def quantize_pitch(self, note):
        pass

    def delete_pitch(self, drum_pad):
        pass

    def select_drum_pad(self, drum_pad):
        pass

    def _on_matrix_pressed(self, button):
        pad = self._pad_for_button(button)
        if not (liveobj_valid(self._drum_group_device) and liveobj_valid(pad)):
            return
        pad_name = cast(str, pad.name)
        if self.mute_button.is_pressed:
            pad.mute = not pad.mute
            self.notify(self.notifications.DrumGroup.Pad.mute, pad_name, pad.mute)
        if self.solo_button.is_pressed:
            pad.solo = not pad.solo
        if self.quantize_button.is_pressed:
            button.color = 'DrumGroup.PadAction'
            self.quantize_pitch(pad.note)
        if self._is_copying():
            button.color = 'DrumGroup.PadAction'
            self._clipboard.copy_or_paste(pad)
        if self.delete_button.is_pressed:
            button.color = 'DrumGroup.PadAction'
            self._do_delete_pad(pad, pad_name)
        if self.select_button.is_pressed:
            self._do_select_pad(pad, pad_name)
            super()._on_matrix_pressed(button)
        if self.mute_button.is_pressed or self.solo_button.is_pressed:
            self._update_led_feedback()

    def _do_delete_pad(self, pad, pad_name):
        if action.delete_notes_with_pitch(self._target_track.target_clip, pad.note):
            self.notify(self.notifications.DrumGroup.Pad.delete_notes, pad_name)
            self.delete_pitch(pad)
        else:
            pad.delete_all_chains()
            self.notify(self.notifications.DrumGroup.Pad.delete, pad_name)

    def _do_select_pad(self, pad, pad_name):
        if liveobj_changed(self._drum_group_device.view.selected_drum_pad, pad):
            self._drum_group_device.view.selected_drum_pad = pad
            self.notify(self.notifications.DrumGroup.Pad.select, pad_name)
            self.select_drum_pad(pad)

    @mute_button.value
    def mute_button(self, _, button):
        self._set_control_pads_from_script(button.is_pressed)

    @solo_button.value
    def solo_button(self, _, button):
        self._set_control_pads_from_script(button.is_pressed)

    @delete_button.value
    def delete_button(self, _, button):
        self._set_control_pads_from_script(button.is_pressed)

    @copy_button.value
    def copy_button(self, *_):
        self._set_control_pads_from_script(self._is_copying())

    @quantize_button.value
    def quantize_button(self, _, button):
        self._set_control_pads_from_script(button.is_pressed)

    def _get_selected_drum_pad(self):
        if liveobj_valid(self._drum_group_device):
            return self._drum_group_device.view.selected_drum_pad

    def _is_copying(self):
        return self.copy_button.is_pressed or self._clipboard.has_content

    def _any_modifier_pressed(self):
        return any([
         self.select_button.is_pressed,
         self.mute_button.is_pressed,
         self.solo_button.is_pressed,
         self.delete_button.is_pressed,
         self.copy_button.is_pressed,
         self.quantize_button.is_pressed])

    def update(self):
        super().update()
        self._update_provided_pitches()

    def _update_provided_pitches(self):
        if liveobj_valid(self._selected_drum_pad):
            self.pitches = [
             self._selected_drum_pad.note]

    def _update_led_feedback(self):
        for button in self.matrix:
            self._update_button_color(button)

    def _update_button_color(self, button):
        pad = self._pad_for_button(button)
        button.color = self._color_for_pad(pad) if pad else 'DrumGroup.PadEmpty'

    def _color_for_pad(self, pad):
        button_color = 'DrumGroup.PadEmpty'
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
        selected_drum_pad = self._get_selected_drum_pad()
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

    def _button_coordinates_to_pad_index(self, first_note, coordinates):
        y, x = coordinates
        inverted_y = self.height - y - 1
        index = first_note + 4 * inverted_y + x
        if x >= 4:
            index += y * 4 + inverted_y * 4
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
        self._update_provided_pitches()

    @listens('chains')
    def __on_chains_changed(self):
        self._update_led_feedback()


class DrumPadClipboardComponent(ClipboardComponent):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self._drum_group_device = None

    def set_drum_group_device(self, drum_group):
        self._drum_group_device = drum_group
        self.clear()

    def _do_copy(self, obj):
        if not (liveobj_valid(obj) and obj.chains):
            self.notify(self.notifications.DrumGroup.Pad.CopyPaste.error_copy_from_empty_pad)
            return
        self.notify(self.notifications.DrumGroup.Pad.CopyPaste.copy, cast(str, obj.name))
        return obj

    def _do_paste(self, obj):
        if liveobj_valid(obj):
            if self._source_obj.note != obj.note:
                if obj.chains:
                    obj.delete_all_chains()
                self._drum_group_device.copy_pad(self._source_obj.note, obj.note)
                self.notify(self.notifications.DrumGroup.Pad.CopyPaste.paste, cast(str, self._source_obj.name))
                return True
            self.notify(self.notifications.DrumGroup.Pad.CopyPaste.error_paste_to_source_pad)
        return False

    def _is_source_valid(self):
        return liveobj_valid(self._drum_group_device) and liveobj_valid(self._source_obj) and self._source_obj.chains