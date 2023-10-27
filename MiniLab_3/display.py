# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_3\display.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 4725 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import MultiSlot, depends, listens, task
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.live import display_name
from .display_util import make_full_screen_message
NOTIFICATION_DURATION = 1

class DisplayComponent(Component):
    shift_button = ButtonControl()

    @depends(target_track=None, session_ring=None, send_midi=None)
    def __init__(self, identification, transport, target_track=None, session_ring=None, send_midi=None, *a, **k):
        (super().__init__)(a, name='Display', **k)
        self._send_midi = send_midi
        self._last_sent_message = None
        self._DisplayComponent__on_is_identified_changed.subject = identification
        self._DisplayComponent__on_transport_event.subject = transport
        self._target_track = target_track
        for arg in ('name', 'arm', 'implicit_arm', 'input_routing_type'):
            self.register_slot(MultiSlot(subject=target_track,
              listener=(self._show_static_display),
              event_name_list=(
             'target_track', arg)))

        self._session_ring = session_ring
        self._DisplayComponent__on_offset_changed.subject = session_ring
        self._DisplayComponent__on_scene_name_changed.subject = session_ring.scenes[0]
        self.register_slot(self.song, self._on_global_property_changed, 'is_playing')
        self.register_slot(self.song, self._on_global_property_changed, 'record_mode')
        self.register_slot(self.song, self._on_global_property_changed, 'session_record')
        self._hide_notification_task = self._tasks.add(task.sequence(task.wait(NOTIFICATION_DURATION), task.run(self._show_static_display)))
        self._hide_notification_task.kill()
        self._show_static_display_task = self._tasks.add(task.run(self._do_show_static_display))
        self._show_static_display_task.kill()

    @shift_button.released
    def shift_button(self, _):
        self._last_sent_message = None
        self._hide_notification_task.kill()
        self._do_show_static_display()

    def _show_static_display(self):
        self._hide_notification_task.kill()
        self._show_static_display_task.restart()

    def _do_show_static_display(self):
        track = self._target_track.target_track
        self._send_message(make_full_screen_message(track.name, display_name(self._session_ring.scenes[0]), track))

    def _show_notification_display(self, line_1, line_2):
        track = self._target_track.target_track
        self._send_message(make_full_screen_message((line_1 or track.name),
          line_2, track, display_pictograms=(not line_1)))
        self._hide_notification_task.restart()

    def _on_global_property_changed(self):
        if not self._hide_notification_task.is_running:
            self._show_static_display()

    @listens('offset')
    def __on_offset_changed(self, *_):
        self._DisplayComponent__on_scene_name_changed.subject = self._session_ring.scenes[0]
        self._DisplayComponent__on_scene_name_changed()

    @listens('name')
    def __on_scene_name_changed(self):
        self._show_static_display()

    @listens('is_identified')
    def __on_is_identified_changed(self, is_identified):
        if is_identified:
            self._show_notification_display('Live {}'.format(self.application.get_major_version()), 'Connected')

    @listens('transport_event')
    def __on_transport_event(self, line_1, line_2):
        self._show_notification_display(line_1, line_2)

    def _send_message(self, message):
        if message != self._last_sent_message:
            self._send_midi(message)
        self._last_sent_message = message