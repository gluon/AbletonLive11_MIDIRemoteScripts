#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/testing/control_surface_test_base.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import midi
from ableton.v2.testing import advance_tasks_by_time, ControlSurfaceTestBase, count_calls, interaction_guard
from .. import sysex
from ..launchpad_elements import SESSION_HEIGHT, SESSION_WIDTH
IDENTITY_RESPONSE = (sysex.SYSEX_START_BYTE,
 midi.SYSEX_NON_REALTIME,
 0,
 midi.SYSEX_GENERAL_INFO,
 midi.SYSEX_IDENTITY_RESPONSE_ID) + sysex.NOVATION_MANUFACTURER_ID + (0, 0) + sysex.DEVICE_FAMILY_MEMBER_CODE + (0,
 0,
 0,
 0,
 sysex.SYSEX_END_BYTE)

class NovationControlSurfaceTestBase(ControlSurfaceTestBase):
    control_surface_class = None
    num_player_tracks = 9

    def create_control_surface(self, c_instance):
        self.capture_sent_midi(c_instance)
        c_instance.set_session_highlight = count_calls()
        surface = self.control_surface_class(c_instance=c_instance)
        surface.refresh_state = count_calls()
        surface.on_identified(IDENTITY_RESPONSE)
        advance_tasks_by_time(surface, 1)
        return surface

    def send_layout_change(self, layout_bytes):
        with interaction_guard():
            self.surface.get_control_by_name(u'Layout_Switch').receive_value(layout_bytes)

    def assertDawModeMessageSent(self, model_id):
        self.assertIn(sysex.STD_MSG_HEADER + (model_id,
         sysex.FIRMWARE_MODE_COMMAND_BYTE,
         sysex.DAW_MODE_BYTE,
         sysex.SYSEX_END_BYTE), self.sent_midi)

    def assertLayoutChangeMessageSent(self, model_id, layout_bytes):
        self.assertIn(sysex.STD_MSG_HEADER + (model_id, sysex.LAYOUT_COMMAND_BYTE) + layout_bytes + (sysex.SYSEX_END_BYTE,), self.sent_midi)

    def assertLayoutRequestMessageSent(self, model_id):
        self.assertIn(sysex.STD_MSG_HEADER + (model_id, sysex.LAYOUT_COMMAND_BYTE, sysex.SYSEX_END_BYTE), self.sent_midi)
