#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/fixed_length.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from past.utils import old_div
from functools import partial
import Live
from ableton.v2.base import EventObject, listens, listenable_property, task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import RadioButtonControl, TextDisplayControl, ToggleButtonControl, ButtonControl, control_list
from . import consts
from .message_box_component import Messenger
Quantization = Live.Song.Quantization
LENGTH_OPTIONS = (Quantization.q_quarter,
 Quantization.q_half,
 Quantization.q_bar,
 Quantization.q_2_bars,
 Quantization.q_4_bars,
 Quantization.q_8_bars,
 Quantization.q_8_bars,
 Quantization.q_8_bars)
LENGTH_OPTION_NAMES = (u'1 Beat', u'2 Beats', u'1 Bar', u'2 Bars', u'4 Bars', u'8 Bars', u'16 Bars', u'32 Bars')
LENGTH_LABELS = (u'Recording length:', u'', u'', u'')
DEFAULT_LENGTH_OPTION_INDEX = list(LENGTH_OPTIONS).index(Quantization.q_2_bars)

class FixedLengthSetting(EventObject):
    option_names = LENGTH_OPTION_NAMES
    selected_index = listenable_property.managed(0)
    enabled = listenable_property.managed(False)
    legato_launch = listenable_property.managed(False)

    def get_selected_length(self, song):
        index = self.selected_index
        length = 2.0 ** index
        quant = LENGTH_OPTIONS[index]
        if index > 1:
            length = old_div(length * song.signature_numerator, song.signature_denominator)
        return (length, quant)


class FixedLengthSettingComponent(Component):
    length_option_buttons = control_list(RadioButtonControl, checked_color=u'Option.Selected', unchecked_color=u'Option.Unselected', control_count=len(LENGTH_OPTIONS))
    fixed_length_toggle_button = ToggleButtonControl(toggled_color=u'Option.On', untoggled_color=u'Option.Off')
    legato_launch_toggle_button = ToggleButtonControl(toggled_color=u'FixedLength.PhraseAlignedOn', untoggled_color=u'FixedLength.PhraseAlignedOff')
    label_display_line = TextDisplayControl(LENGTH_LABELS)
    option_display_line = TextDisplayControl(LENGTH_OPTION_NAMES)

    def __init__(self, fixed_length_setting = None, *a, **k):
        assert fixed_length_setting is not None
        super(FixedLengthSettingComponent, self).__init__(*a, **k)
        self._fixed_length_setting = fixed_length_setting
        self.length_option_buttons.connect_property(fixed_length_setting, u'selected_index')
        self.fixed_length_toggle_button.connect_property(fixed_length_setting, u'enabled')
        self.legato_launch_toggle_button.connect_property(fixed_length_setting, u'legato_launch')
        self.__on_setting_selected_index_changes.subject = fixed_length_setting
        self.__on_setting_selected_index_changes(fixed_length_setting.selected_index)

    @listens(u'selected_index')
    def __on_setting_selected_index_changes(self, index):
        self._update_option_display()

    def _update_option_display(self):
        for index, option_name in enumerate(LENGTH_OPTION_NAMES):
            prefix = consts.CHAR_SELECT if index == self._fixed_length_setting.selected_index else u' '
            self.option_display_line[index] = prefix + option_name


class FixedLengthComponent(Component, Messenger):
    fixed_length_toggle_button = ButtonControl()

    def __init__(self, fixed_length_setting = None, *a, **k):
        assert fixed_length_setting is not None
        super(FixedLengthComponent, self).__init__(*a, **k)
        self._fixed_length_setting = fixed_length_setting
        self.settings_component = FixedLengthSettingComponent(fixed_length_setting=self._fixed_length_setting, parent=self, is_enabled=False)
        self._length_press_state = None
        self.__on_setting_enabled_changes.subject = fixed_length_setting
        self.__on_setting_enabled_changes(fixed_length_setting.enabled)

    @fixed_length_toggle_button.released_immediately
    def fixed_length_toggle_button(self, button):
        loop_set = self._set_loop()
        if not loop_set:
            enabled = not self._fixed_length_setting.enabled
            self._fixed_length_setting.enabled = enabled
            self.show_notification(consts.MessageBoxText.FIXED_LENGTH % (u'On' if enabled else u'Off'))

    @fixed_length_toggle_button.pressed_delayed
    def fixed_length_toggle_button(self, button):
        self.settings_component.set_enabled(True)

    @fixed_length_toggle_button.released_delayed
    def fixed_length_toggle_button(self, button):
        self.settings_component.set_enabled(False)
        self._set_loop()

    @fixed_length_toggle_button.pressed
    def fixed_length_toggle_button(self, button):
        song = self.song
        slot = song.view.highlighted_clip_slot
        if slot is None:
            return
        clip = slot.clip
        if slot.is_recording and not clip.is_overdubbing:
            self._length_press_state = (slot, clip.playing_position)

    def _set_loop(self):
        song = self.song
        slot = song.view.highlighted_clip_slot
        if slot is None:
            return
        clip = slot.clip
        loop_set = False
        if self._length_press_state is not None:
            press_slot, press_position = self._length_press_state
            if press_slot == slot and slot.is_recording and not clip.is_overdubbing:
                length, _ = self._fixed_length_setting.get_selected_length(song)
                one_bar = old_div(4.0 * song.signature_numerator, song.signature_denominator)
                loop_start = int(old_div(press_position, length)) * length
                loop_end = loop_start + length
                clip.loop_end = loop_end
                clip.end_marker = loop_end
                clip.loop_start = loop_start
                clip.start_marker = loop_start
                progress = old_div(press_position - loop_start, loop_end - loop_start)
                if progress < 0.5 and loop_start - length >= 0:
                    launch_quantization = Quantization.q_no_q
                    self.song.overdub = False
                else:
                    duration_needed_to_finish_recording_bar = old_div(loop_end - press_position, one_bar)
                    launch_quantization = Quantization.q_no_q
                    if duration_needed_to_finish_recording_bar < 0.5:
                        launch_quantization = Quantization.q_half
                    elif duration_needed_to_finish_recording_bar < 1:
                        launch_quantization = Quantization.q_bar
                    elif duration_needed_to_finish_recording_bar < 2:
                        launch_quantization = Quantization.q_2_bars
                    elif duration_needed_to_finish_recording_bar < 4:
                        launch_quantization = Quantization.q_4_bars
                    elif duration_needed_to_finish_recording_bar < 8:
                        launch_quantization = Quantization.q_8_bars
                self._tasks.add(task.sequence(task.delay(0), task.run(partial(slot.fire, force_legato=True, launch_quantization=launch_quantization))))
                loop_set = True
        self._length_press_state = None
        return loop_set

    @listens(u'enabled')
    def __on_setting_enabled_changes(self, enabled):
        self.fixed_length_toggle_button.color = u'FixedLength.On' if enabled else u'FixedLength.Off'
