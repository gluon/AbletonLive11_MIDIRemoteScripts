#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/transport.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl, ToggleButtonControl

class TransportComponent(TransportComponentBase):
    play_button = ToggleButtonControl(toggled_color=u'Transport.PlayOn', untoggled_color=u'Transport.PlayOff')
    capture_midi_button = ButtonControl()

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._metronome_toggle.view_transform = lambda v: (u'Transport.MetronomeOn' if v else u'Transport.MetronomeOff')
        self.__on_can_capture_midi_changed.subject = self.song
        self.__on_can_capture_midi_changed()

    @play_button.toggled
    def _on_play_button_toggled(self, is_toggled, _):
        if is_toggled:
            self.song.stop_playing()
        self.song.is_playing = is_toggled

    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        try:
            if self.song.can_capture_midi:
                self.song.capture_midi()
        except RuntimeError:
            pass

    @listens(u'can_capture_midi')
    def __on_can_capture_midi_changed(self):
        self.capture_midi_button.color = u'Transport.Capture{}'.format(u'On' if self.song.can_capture_midi else u'Off')

    def _update_button_states(self):
        super(TransportComponent, self)._update_button_states()
        self.continue_playing_button.color = u'Transport.Continue{}'.format(u'Off' if self.song.is_playing else u'On')
