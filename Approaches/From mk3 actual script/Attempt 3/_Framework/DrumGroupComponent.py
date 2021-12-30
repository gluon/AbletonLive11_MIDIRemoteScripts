#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/DrumGroupComponent.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from builtins import range
from .Control import PlayableControl, ButtonControl, control_matrix
from .Dependency import depends
from .SubjectSlot import subject_slot_group, subject_slot
from .SlideComponent import SlideComponent, Slideable
from .Util import find_if, first, clamp
BASE_DRUM_RACK_NOTE = 36

class DrumGroupComponent(SlideComponent, Slideable):
    __subject_events__ = (u'pressed_pads',)
    mute_button = ButtonControl()
    solo_button = ButtonControl()
    delete_button = ButtonControl()
    quantize_button = ButtonControl()
    select_button = ButtonControl()
    drum_matrix = control_matrix(PlayableControl)

    @depends(set_pad_translations=None)
    def __init__(self, translation_channel = None, set_pad_translations = None, *a, **k):
        self._takeover_drums = False
        self._drum_group_device = None
        self._selected_drum_pad = None
        self._all_drum_pads = []
        self._selected_pads = []
        self._visible_drum_pads = []
        self._translation_channel = translation_channel
        self._coordinate_to_pad_map = {}
        super(DrumGroupComponent, self).__init__(*a, **k)
        self._set_pad_translations = set_pad_translations

    position_count = 32
    page_length = 4
    page_offset = 1

    def contents_range(self, pmin, pmax):
        pos_count = self.position_count
        first_pos = max(int(pmin - 0.05), 0)
        last_pos = min(int(pmax + 0.2), pos_count)
        return list(range(first_pos, last_pos))

    def contents(self, index):
        drum = self._drum_group_device
        if drum:
            return any(map(lambda pad: pad.chains, drum.drum_pads[index * 4:index * 4 + 4]))
        return False

    def _get_position(self):
        if self._drum_group_device:
            return self._drum_group_device.view.drum_pads_scroll_position
        return 0

    def _set_position(self, index):
        assert 0 <= index <= 28
        if self._drum_group_device:
            self._drum_group_device.view.drum_pads_scroll_position = index

    position = property(_get_position, _set_position)

    @property
    def width(self):
        if self.drum_matrix.width:
            return self.drum_matrix.width
        return 4

    @property
    def height(self):
        if self.drum_matrix.height:
            return self.drum_matrix.height
        return 4

    @property
    def pressed_pads(self):
        return self._selected_pads

    @property
    def visible_drum_pads(self):
        if self._visible_drum_pads and self._all_drum_pads:
            first_pad = first(self._visible_drum_pads)
            if first_pad:
                size = self.width * self.height
                first_note = first_pad.note
                if first_note > 128 - size:
                    size = 128 - first_note
                offset = clamp(first_note, 0, 128 - len(self._visible_drum_pads))
                return self._all_drum_pads[offset:offset + size]
        return []

    def update(self):
        super(DrumGroupComponent, self).update()
        self._set_control_pads_from_script(False)
        self._update_led_feedback()

    def set_drum_matrix(self, matrix):
        self.drum_matrix.set_control_element(matrix)
        for button in self.drum_matrix:
            button.channel = self._translation_channel

        if self._selected_pads:
            self._selected_pads = []
            self.notify_pressed_pads()
        self._create_and_set_pad_translations()
        self._update_control_from_script()
        self._update_identifier_translations()
        self._update_led_feedback()

    def set_drum_group_device(self, drum_group_device):
        if drum_group_device and not drum_group_device.can_have_drum_pads:
            drum_group_device = None
        if drum_group_device != self._drum_group_device:
            self._on_visible_drum_pads_changed.subject = drum_group_device
            drum_group_view = drum_group_device.view if drum_group_device else None
            self._on_selected_drum_pad_changed.subject = drum_group_view
            self._on_drum_pads_scroll_position_changed.subject = drum_group_view
            self._drum_group_device = drum_group_device
            self._update_drum_pad_listeners()
            self._on_selected_drum_pad_changed()
            self._update_identifier_translations()
            super(DrumGroupComponent, self).update()

    def _update_drum_pad_listeners(self):
        u"""
        add and remove listeners for visible drum pads, including
        mute and solo state
        """
        if self._drum_group_device:
            self._all_drum_pads = self._drum_group_device.drum_pads
            self._visible_drum_pads = self._drum_group_device.visible_drum_pads
            self._on_solo_changed.replace_subjects(self._visible_drum_pads)
            self._on_mute_changed.replace_subjects(self._visible_drum_pads)
            self._update_identifier_translations()

    @subject_slot_group(u'solo')
    def _on_solo_changed(self, pad):
        self._update_led_feedback()

    @subject_slot_group(u'mute')
    def _on_mute_changed(self, pad):
        self._update_led_feedback()

    def _update_led_feedback(self):
        if self._drum_group_device:
            soloed_pads = find_if(lambda pad: pad.solo, self._all_drum_pads)
            for button in self.drum_matrix:
                pad = self._coordinate_to_pad_map.get(button.coordinate, None)
                if pad:
                    self._update_pad_led(pad, button, soloed_pads)

    def _update_pad_led(self, pad, button, soloed_pads):
        button_color = u'DrumGroup.PadEmpty'
        if pad == self._selected_drum_pad:
            if soloed_pads and not pad.solo and not pad.mute:
                button_color = u'DrumGroup.PadSelectedNotSoloed'
            elif pad.mute and not pad.solo:
                button_color = u'DrumGroup.PadMutedSelected'
            elif soloed_pads and pad.solo:
                button_color = u'DrumGroup.PadSoloedSelected'
            else:
                button_color = u'DrumGroup.PadSelected'
        elif pad.chains:
            if soloed_pads and not pad.solo:
                if not pad.mute:
                    button_color = u'DrumGroup.PadFilled'
                else:
                    button_color = u'DrumGroup.PadMuted'
            elif not soloed_pads and pad.mute:
                button_color = u'DrumGroup.PadMuted'
            elif soloed_pads and pad.solo:
                button_color = u'DrumGroup.PadSoloed'
            else:
                button_color = u'DrumGroup.PadFilled'
        else:
            button_color = u'DrumGroup.PadEmpty'
        button.color = button_color

    def _button_coordinates_to_pad_index(self, first_note, coordinates):
        y, x = coordinates
        y = self.height - y - 1
        if x < 4 and y >= 4:
            first_note += 16
        elif x >= 4 and y < 4:
            first_note += 4 * self.width
        elif x >= 4 and y >= 4:
            first_note += 4 * self.width + 16
        index = x % 4 + y % 4 * 4 + first_note
        return index

    @drum_matrix.pressed
    def drum_matrix(self, pad):
        self._on_matrix_pressed(pad)

    @drum_matrix.released
    def drum_matrix(self, pad):
        self._on_matrix_released(pad)

    def _on_matrix_released(self, pad):
        selected_drum_pad = self._coordinate_to_pad_map[pad.coordinate]
        if selected_drum_pad in self._selected_pads:
            self._selected_pads.remove(selected_drum_pad)
            if not self._selected_pads:
                self._update_control_from_script()
            self.notify_pressed_pads()
        self._update_led_feedback()

    def _on_matrix_pressed(self, pad):
        selected_drum_pad = self._coordinate_to_pad_map[pad.coordinate]
        if self.mute_button.is_pressed:
            selected_drum_pad.mute = not selected_drum_pad.mute
        if self.solo_button.is_pressed:
            selected_drum_pad.solo = not selected_drum_pad.solo
        if self.quantize_button.is_pressed:
            pad.color = u'DrumGroup.PadAction'
            self.quantize_pitch(selected_drum_pad.note)
        if self.delete_button.is_pressed:
            pad.color = u'DrumGroup.PadAction'
            self.delete_pitch(selected_drum_pad)
        if self.select_button.is_pressed:
            self._drum_group_device.view.selected_drum_pad = selected_drum_pad
            self.select_drum_pad(selected_drum_pad)
            self._selected_pads.append(selected_drum_pad)
            if len(self._selected_pads) == 1:
                self._update_control_from_script()
            self.notify_pressed_pads()
        if self.mute_button.is_pressed or self.solo_button.is_pressed:
            self._update_led_feedback()

    @subject_slot(u'visible_drum_pads')
    def _on_visible_drum_pads_changed(self):
        self._update_drum_pad_listeners()
        self._update_led_feedback()

    @subject_slot(u'drum_pads_scroll_position')
    def _on_drum_pads_scroll_position_changed(self):
        self._update_identifier_translations()
        self._update_led_feedback()
        self.notify_position()

    @subject_slot(u'selected_drum_pad')
    def _on_selected_drum_pad_changed(self):
        self._selected_drum_pad = self._drum_group_device.view.selected_drum_pad if self._drum_group_device else None
        self._update_led_feedback()

    @mute_button.value
    def mute_button(self, value, button):
        self._set_control_pads_from_script(bool(value))

    @solo_button.value
    def solo_button(self, value, button):
        self._set_control_pads_from_script(bool(value))

    @delete_button.value
    def delete_button(self, value, button):
        self._set_control_pads_from_script(bool(value))

    @quantize_button.value
    def quantize_button(self, value, button):
        self._set_control_pads_from_script(bool(value))

    @select_button.value
    def select_button(self, value, button):
        self._set_control_pads_from_script(bool(value))

    def _set_control_pads_from_script(self, takeover_drums):
        u"""
        If takeover_drums, the matrix buttons will be controlled from
        the script. Otherwise they send midi notes to the track
        associated to this drum group.
        """
        if takeover_drums != self._takeover_drums:
            self._takeover_drums = takeover_drums
            self._update_control_from_script()

    def _update_control_from_script(self):
        takeover_drums = self._takeover_drums or bool(self._selected_pads)
        for button in self.drum_matrix:
            button.set_playable(not takeover_drums)

    def _update_identifier_translations(self):
        if self.visible_drum_pads:
            if not self._can_set_pad_translations():
                self._set_non_pad_translated_identifiers()
            else:
                self._set_pad_translated_identifiers()

    def _set_non_pad_translated_identifiers(self):
        visible_drum_pads = self.visible_drum_pads
        if visible_drum_pads:
            first_pad = first(visible_drum_pads)
            for button in self.drum_matrix:
                identifier = self._button_coordinates_to_pad_index(first_pad.note, button.coordinate)
                if identifier < 128:
                    button.identifier = identifier
                    button.enabled = True
                    self._coordinate_to_pad_map[button.coordinate] = self._all_drum_pads[button.identifier]
                else:
                    button.enabled = False

    def _set_pad_translated_identifiers(self):
        visible_drum_pads = self.visible_drum_pads
        if visible_drum_pads:
            for index, button in enumerate(self.drum_matrix):
                row, col = button.coordinate
                self._coordinate_to_pad_map[self.width - 1 - row, col] = visible_drum_pads[index]

    def _can_set_pad_translations(self):
        return self.width <= 4 and self.height <= 4

    def _create_and_set_pad_translations(self):

        def create_translation_entry(button):
            row, col = button.coordinate
            button.identifier = self._button_coordinates_to_pad_index(BASE_DRUM_RACK_NOTE, button.coordinate)
            return (col,
             row,
             button.identifier,
             button.channel)

        if self._can_set_pad_translations():
            translations = tuple(map(create_translation_entry, self.drum_matrix))
            self._set_pad_translated_identifiers()
        else:
            translations = None
            self._set_non_pad_translated_identifiers()
        self._set_pad_translations(translations)

    def select_drum_pad(self, drum_pad):
        u""" Override when you give it a select button """
        raise NotImplementedError

    def quantize_pitch(self, note):
        u""" Override when you give it a quantize button """
        raise NotImplementedError

    def delete_pitch(self, drum_pad):
        u""" Override when you give it a delete button """
        raise NotImplementedError
