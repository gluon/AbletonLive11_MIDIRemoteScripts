#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/note_repeat_component.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from builtins import range
from builtins import object
from past.utils import old_div
from ableton.v2.base import listens, task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl
from .action_with_options_component import OptionsComponent

def _make_triplet(base):
    return base * 1.5


def _frequency_to_repeat_rate(frequency):
    return old_div(1.0, frequency) * 4.0


NOTE_REPEAT_RATES = list(map(_frequency_to_repeat_rate, [_make_triplet(32),
 32,
 _make_triplet(16),
 16,
 _make_triplet(8),
 8,
 _make_triplet(4),
 4]))
DEFAULT_INDEX = 5
DEFAULT_RATE = NOTE_REPEAT_RATES[DEFAULT_INDEX]

class DummyNoteRepeat(object):
    repeat_rate = 1.0
    enabled = False


class NoteRepeatComponent(Component):
    u"""
    Component for setting up the note repeat
    """

    def __init__(self, note_repeat = None, *a, **k):
        super(NoteRepeatComponent, self).__init__(*a, **k)
        self._aftertouch = None
        self._last_record_quantization = None
        self._note_repeat = None
        self._options = OptionsComponent(parent=self)
        self._options.selected_color = u'NoteRepeat.RateSelected'
        self._options.unselected_color = u'NoteRepeat.RateUnselected'
        self._options.option_names = list(map(str, list(range(8))))
        self._options.selected_option = DEFAULT_INDEX
        self._on_selected_option_changed.subject = self._options
        self.__on_selected_track_changed.subject = self.song.view
        self.set_note_repeat(note_repeat)

    def update(self):
        super(NoteRepeatComponent, self).update()
        if self.is_enabled():
            self._enable_note_repeat()
            self._update_aftertouch()
        else:
            self._disable_note_repeat()

    def _update_aftertouch(self):
        if self._aftertouch and self.is_enabled():
            self._aftertouch.send_value(u'polyphonic')

    def set_aftertouch_control(self, control):
        self._aftertouch = control
        self._update_aftertouch()

    def set_select_buttons(self, buttons):
        self._options.select_buttons.set_control_element(buttons)

    def set_note_repeat(self, note_repeat):
        note_repeat = note_repeat or DummyNoteRepeat()
        if self._note_repeat != None:
            self._note_repeat.enabled = False
        self._note_repeat = note_repeat
        self._update_note_repeat(enabled=self.is_enabled())

    def set_pad_parameters(self, element):
        if element:
            element.reset()

    def _get_repeat_rate(self):
        return self.song.view.selected_track.get_data(u'push-note-repeat-rate', DEFAULT_RATE)

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        self._options.selected_option = self._get_repeat_rate_index()
        self._on_selected_option_changed(self._options.selected_option)

    def _get_repeat_rate_index(self):
        repeat_rate = self._get_repeat_rate()
        if repeat_rate in NOTE_REPEAT_RATES:
            return NOTE_REPEAT_RATES.index(repeat_rate)
        return DEFAULT_INDEX

    def _enable_note_repeat(self):
        self._last_record_quantization = self.song.midi_recording_quantization
        self._set_recording_quantization(False)
        self._update_note_repeat(enabled=True)

    def _disable_note_repeat(self):
        if not self.song.midi_recording_quantization and self._last_record_quantization:
            self._set_recording_quantization(self._last_record_quantization)
        self._update_note_repeat(enabled=False)

    def _set_recording_quantization(self, value):

        def doit():
            self.song.midi_recording_quantization = value

        self._tasks.parent_task.add(task.run(doit))

    @listens(u'selected_option')
    def _on_selected_option_changed(self, option):
        self._note_repeat.repeat_rate = NOTE_REPEAT_RATES[option]
        self._options.selected_option = option
        self.song.view.selected_track.set_data(u'push-note-repeat-rate', NOTE_REPEAT_RATES[option])

    def _update_note_repeat(self, enabled = False):
        self._on_selected_option_changed(self._get_repeat_rate_index())
        self._note_repeat.enabled = self.is_enabled()


class NoteRepeatEnabler(Component):
    repeat_button = ButtonControl()

    def __init__(self, note_repeat = None, *a, **k):
        super(NoteRepeatEnabler, self).__init__(*a, **k)
        self.note_repeat_component = NoteRepeatComponent(note_repeat=note_repeat, name=u'Note_Repeat', parent=self, is_enabled=False)
        self.__on_selected_track_changed.subject = self.song.view
        self._restore_note_repeat_enabled_state()

    def set_note_repeat(self, note_repeat):
        self.note_repeat_component.set_note_repeat(note_repeat)

    @repeat_button.pressed
    def repeat_button(self, button):
        self._toggle_note_repeat()

    @repeat_button.released_delayed
    def repeat_button(self, button):
        self._toggle_note_repeat()

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        self._restore_note_repeat_enabled_state()
        self.repeat_button.enabled = not self.song.view.selected_track.has_audio_input

    def _toggle_note_repeat(self):
        is_enabled = not self.note_repeat_component.is_enabled()
        self._set_note_repeat_enabled(is_enabled)

    def _set_note_repeat_enabled(self, is_enabled):
        self.note_repeat_component.set_enabled(is_enabled)
        self.song.view.selected_track.set_data(u'push-note-repeat-enabled', is_enabled)
        self.repeat_button.color = u'DefaultButton.Alert' if is_enabled else u'DefaultButton.On'

    def _restore_note_repeat_enabled_state(self):
        self._set_note_repeat_enabled(self._get_note_repeat_enabled())

    def _get_note_repeat_enabled(self):
        return self.song.view.selected_track.get_data(u'push-note-repeat-enabled', False)
