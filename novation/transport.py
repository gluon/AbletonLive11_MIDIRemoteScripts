from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl, ToggleButtonControl

class TransportComponent(TransportComponentBase):
    play_button = ToggleButtonControl(toggled_color='Transport.PlayOn',
      untoggled_color='Transport.PlayOff')
    capture_midi_button = ButtonControl()

    def __init__(self, *a, **k):
        (super(TransportComponent, self).__init__)(*a, **k)
        self._metronome_toggle.view_transform = lambda v: 'Transport.MetronomeOn' if v else 'Transport.MetronomeOff'
        self._TransportComponent__on_can_capture_midi_changed.subject = self.song
        self._TransportComponent__on_can_capture_midi_changed()

    @play_button.toggled
    def _on_play_button_toggled(self, is_toggled, _):
        self.song.is_playing = is_toggled
        if is_toggled:
            self.song.current_song_time = 0.0

    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        try:
            if self.song.can_capture_midi:
                self.song.capture_midi()
        except RuntimeError:
            pass

    @listens('can_capture_midi')
    def __on_can_capture_midi_changed(self):
        self.capture_midi_button.color = 'Transport.Capture{}'.format('On' if self.song.can_capture_midi else 'Off')

    def _update_button_states(self):
        super(TransportComponent, self)._update_button_states()
        self.continue_playing_button.color = 'Transport.Continue{}'.format('Off' if self.song.is_playing else 'On')