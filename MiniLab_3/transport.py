from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v3.base import move_current_song_time, sign
from ableton.v3.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v3.control_surface.controls import ButtonControl, EncoderControl, ToggleButtonControl

class TransportComponent(TransportComponentBase):
    __events__ = ('transport_event', )
    arrangement_position_encoder = EncoderControl()
    tap_tempo_button = ButtonControl(color='Transport.TapTempo',
      pressed_color='Transport.TapTempoPressed')
    loop_button = ToggleButtonControl(color='Transport.LoopOff',
      on_color='Transport.LoopOn')

    @arrangement_position_encoder.value
    def arrangement_position_encoder(self, value, _):
        move_current_song_time(self.song, sign(value))
        self.notify_transport_event('', str(self.song.get_current_smpte_song_time(Live.Song.TimeFormat.smpte_25)))

    @tap_tempo_button.pressed
    def tap_tempo_button(self, _):
        if not self._end_undo_step_task.is_running:
            self.song.begin_undo_step()
        self._end_undo_step_task.restart()
        self.song.tap_tempo()
        self.notify_transport_event('Tap Tempo', '{} BPM'.format(int(self.song.tempo)))

    @loop_button.released
    def loop_button(self, *_):
        self.notify_transport_event('Loop Mode', 'ON' if self.song.loop else 'OFF')