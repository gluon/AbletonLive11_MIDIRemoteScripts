# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\blackstar_live_logic.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 1936 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface import Layer, SimpleControlSurface
from ableton.v2.control_surface.midi import is_sysex
from .elements import Elements
from .looper import LooperComponent

class Blackstar_Live_Logic(SimpleControlSurface):

    def __init__(self, *a, **k):
        (super(Blackstar_Live_Logic, self).__init__)(*a, **k)
        with self.component_guard():
            self._elements = Elements()
            self._looper = LooperComponent(name='Looper',
              is_enabled=False,
              layer=Layer(foot_switches=(self._elements.foot_switches),
              time_display=(self._elements.time_display)))

    def disconnect(self):
        super(Blackstar_Live_Logic, self).disconnect()
        self._elements.live_integration_mode_switch.send_value(0)

    def port_settings_changed(self):
        self._elements.live_integration_mode_switch.send_value(1)
        self.schedule_message(1, self._looper.set_enabled, True)
        self.schedule_message(2, self.refresh_state)

    def process_midi_bytes(self, midi_bytes, midi_processor):
        if is_sysex(midi_bytes):
            return
        return super(Blackstar_Live_Logic, self).process_midi_bytes(midi_bytes, midi_processor)