from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from .ConfigurableButtonElement import ConfigurableButtonElement
from .MainSelectorComponent import MainSelectorComponent

try:
    exec("from .Settings import Settings")
except ImportError:
    exec("from .Settings import *")

DO_COMBINE = Live.Application.combine_apcs()  # requires 8.2 & higher

LP_MINI_MK3_FAMILY_CODE = (19, 1)
LP_MINI_MK3_ID = 13
LP_X_FAMILY_CODE = (3, 1)
LP_X_ID = 12

SYSEX_START = 240
SYSEX_END = 247
SYSEX_GENERAL_INFO = 6
SYSEX_NON_REALTIME = 126
SYSEX_IDENTITY_REQUEST_ID = 1
# SYSEX_IDENTITY_RESPONSE_ID = 2
SYSEX_IDENTITY_REQUEST_MESSAGE = (
    SYSEX_START,
    SYSEX_NON_REALTIME,
    127,
    SYSEX_GENERAL_INFO,
    SYSEX_IDENTITY_REQUEST_ID,
    SYSEX_END,
)
NOVATION_MANUFACTURER_ID = (0, 32, 41)
FIRMWARE_MODE_COMMAND = 16
STANDALONE_MODE = 0

STD_MSG_HEADER = (SYSEX_START,) + NOVATION_MANUFACTURER_ID + (2,)


class Launchpad(ControlSurface):

    _active_instances = []

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        live = Live.Application.get_application()
        self._live_major_version = live.get_major_version()
        self._live_minor_version = live.get_minor_version()
        self._live_bugfix_version = live.get_bugfix_version()
        self._selector = None  # needed because update hardware is called.
        self._mk3_rgb = False
        with self.component_guard():
            self._suppress_send_midi = True
            self._suppress_session_highlight = True
            self._suggested_input_port = (
                "Launchpad",
                "Launchpad Mini",
                "Launchpad S",
                "Launchpad MK2",
                "Launchpad X",
                "Launchpad Mini MK3",
            )
            self._suggested_output_port = (
                "Launchpad",
                "Launchpad Mini",
                "Launchpad S",
                "Launchpad MK2",
                "Launchpad X",
                "Launchpad Mini MK3",
            )
            self._control_is_with_automap = False
            self._user_byte_write_button = None
            self._config_button = None
            self._wrote_user_byte = False
            self._challenge = Live.Application.get_random_int(0, 400000000) & 2139062143
            self._init_done = False
        # caller will send challenge and we will continue as challenge is received.

    def init(self):
        # skip init if already done.
        if self._init_done:
            return
        self._init_done = True

        # second part of the __init__ after model has been identified using its challenge response
        if self._mk3_rgb:
            from .SkinMK3 import make_skin

            self._skin = make_skin()
            self._side_notes = (89, 79, 69, 59, 49, 39, 29, 19)
            self._drum_notes = (
                20,
                30,
                90,
                91,
                92,
                93,
                94,
                95,
                96,
                97,
                98,
                99,
                100,
                101,
                102,
                103,
                112,
                113,
                114,
                115,
                116,
                117,
                118,
                119,
                120,
                121,
                122,
                123,
                124,
                125,
                126,
            )
        else:
            raise Exception("Not an Mk3")

        with self.component_guard():
            is_momentary = True
            self._config_button = ButtonElement(
                is_momentary, MIDI_CC_TYPE, 0, 0, optimized_send_midi=False
            )
            self._config_button.add_value_listener(self._config_value)
            self._user_byte_write_button = ButtonElement(
                is_momentary, MIDI_CC_TYPE, 0, 16
            )
            self._user_byte_write_button.name = "User_Byte_Button"
            self._user_byte_write_button.send_value(1)
            self._user_byte_write_button.add_value_listener(self._user_byte_value)
            matrix = ButtonMatrixElement()
            matrix.name = "Button_Matrix"
            for row in range(8):
                button_row = []
                for column in range(8):
                    if self._mk3_rgb:
                        # for mk2 buttons are assigned "top to bottom"
                        midi_note = (81 - (10 * row)) + column
                    else:
                        midi_note = row * 16 + column
                    button = ConfigurableButtonElement(
                        is_momentary,
                        MIDI_NOTE_TYPE,
                        0,
                        midi_note,
                        skin=self._skin,
                        control_surface=self,
                    )
                    button.name = str(column) + "_Clip_" + str(row) + "_Button"
                    button_row.append(button)
                matrix.add_row(tuple(button_row))

            top_buttons = [
                ConfigurableButtonElement(
                    is_momentary, MIDI_CC_TYPE, 0, 91 + index, skin=self._skin
                )
                for index in range(8)
            ]
            side_buttons = [
                ConfigurableButtonElement(
                    is_momentary,
                    MIDI_CC_TYPE,
                    0,
                    self._side_notes[index],
                    skin=self._skin,
                )
                for index in range(8)
            ]

            top_buttons[0].name = "Bank_Select_Up_Button"
            top_buttons[1].name = "Bank_Select_Down_Button"
            top_buttons[2].name = "Bank_Select_Left_Button"
            top_buttons[3].name = "Bank_Select_Right_Button"
            top_buttons[4].name = "Session_Button"
            top_buttons[5].name = "Drums_Button"
            top_buttons[6].name = "Keys_Button"
            top_buttons[7].name = "User_Button"
            side_buttons[0].name = "Scene1_Button"
            side_buttons[1].name = "Scene2_Button"
            side_buttons[2].name = "Scene3_Button"
            side_buttons[3].name = "Scene4_Button"
            side_buttons[4].name = "Scene5_Button"
            side_buttons[5].name = "Scene6_Button"
            side_buttons[6].name = "Scene7_Button"
            side_buttons[7].name = "Stop_Solo_Mute_Button"
            self._selector = MainSelectorComponent(
                matrix,
                tuple(top_buttons),
                tuple(side_buttons),
                self._config_button,
                self,
            )
            self._selector.name = "Main_Modes"
            self._do_combine()
            for control in self.controls:
                if isinstance(control, ConfigurableButtonElement):
                    control.add_value_listener(self._button_value)

            self._suppress_session_highlight = False
            self.set_highlighting_session_component(self._selector.session_component())
            # due to our 2 stage init, we need to rebuild midi map
            self.request_rebuild_midi_map()
            # and request update
            self._selector.update()
            self.log_message("Custom Launchpad Mini Mk3 loaded!")

    def disconnect(self):
        self._suppress_send_midi = True
        for control in self.controls:
            if isinstance(control, ConfigurableButtonElement):
                control.remove_value_listener(self._button_value)
        self._do_uncombine()
        if self._selector != None:
            self._user_byte_write_button.remove_value_listener(self._user_byte_value)
            self._config_button.remove_value_listener(self._config_value)
        ControlSurface.disconnect(self)
        self._suppress_send_midi = False
        # launchpad mk3 needs disconnect string sent
        self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, 14, 0, SYSEX_END))
        self._send_midi(
            STD_MSG_HEADER
            + (LP_MINI_MK3_ID, FIRMWARE_MODE_COMMAND, STANDALONE_MODE, SYSEX_END)
        )
        if self._config_button != None:
            self._config_button.send_value(
                32
            )  # Send enable flashing led config message to LP
            self._config_button.send_value(0)
            self._config_button = None
        if self._user_byte_write_button != None:
            self._user_byte_write_button.send_value(0)
            self._user_byte_write_button = None

    def _combine_active_instances():
        support_devices = False
        for instance in Launchpad._active_instances:
            support_devices |= instance._device_component != None
        offset = 0
        for instance in Launchpad._active_instances:
            offset += instance._selector._session.width()

    _combine_active_instances = staticmethod(_combine_active_instances)

    def _do_combine(self):
        if DO_COMBINE and (self not in Launchpad._active_instances):
            Launchpad._active_instances.append(self)
            Launchpad._combine_active_instances()

    def _do_uncombine(self):
        if self in Launchpad._active_instances:
            Launchpad._active_instances.remove(self)
            Launchpad._combine_active_instances()

    def refresh_state(self):
        ControlSurface.refresh_state(self)
        self.schedule_message(5, self._update_hardware)

    def handle_sysex(self, midi_bytes):
        if len(midi_bytes) >= 10 and midi_bytes[:8] == (
            240,
            126,
            0,
            6,
            2,
            0,
            32,
            41,
        ):  # 0,32,41=novation
            if len(midi_bytes) >= 12 and midi_bytes[8:10] == (19, 1):
                self._mk3_rgb = True
                # programmer mode
                self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, 14, 1, SYSEX_END))
                # led feedback: internal off, external on
                self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, 10, 0, 1, SYSEX_END))
                # disable sleep mode
                self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, 9, 1, SYSEX_END))
                self._suppress_send_midi = False
                self.set_enabled(True)
                self.init()
            else:
                ControlSurface.handle_sysex(self, midi_bytes)
                self.log_message("OTHER NOVATION")
        else:
            ControlSurface.handle_sysex(self, midi_bytes)

    def build_midi_map(self, midi_map_handle):
        ControlSurface.build_midi_map(self, midi_map_handle)
        if self._selector != None:
            if self._selector._main_mode_index == 1:
                mode = Settings.USER_MODES_1[
                    self._selector._sub_mode_list[self._selector._main_mode_index]
                ]
                if mode != "instrument":
                    new_channel = self._selector.channel_for_current_mode()
                    for note in self._drum_notes:
                        self._translate_message(
                            MIDI_NOTE_TYPE, note, 0, note, new_channel
                        )
            elif self._selector._main_mode_index == 2:
                mode = Settings.USER_MODES_2[
                    self._selector._sub_mode_list[self._selector._main_mode_index]
                ]

    def _send_midi(self, midi_bytes, optimized=None):
        sent_successfully = False
        if not self._suppress_send_midi:
            sent_successfully = ControlSurface._send_midi(
                self, midi_bytes, optimized=optimized
            )
        return sent_successfully

    def _update_hardware(self):
        self._suppress_send_midi = False
        if self._user_byte_write_button != None:
            self._user_byte_write_button.send_value(1)
            self._wrote_user_byte = True
        self._suppress_send_midi = True
        self.set_enabled(False)
        self._suppress_send_midi = False
        self._send_challenge()

    def _send_challenge(self):
        # send challenge for mk3 to detect that it is actually plugged in
        self._send_midi(SYSEX_IDENTITY_REQUEST_MESSAGE)

    def _user_byte_value(self, value):
        assert value in range(128)
        if not self._wrote_user_byte:
            enabled = value == 1
            self._control_is_with_automap = not enabled
            self._suppress_send_midi = self._control_is_with_automap
            if not self._control_is_with_automap:
                for control in self.controls:
                    if isinstance(control, ConfigurableButtonElement):
                        control.force_next_send()

            self._selector.set_mode(0)
            self.set_enabled(enabled)
            self._suppress_send_midi = False
        else:
            self._wrote_user_byte = False

    def _button_value(self, value):
        assert value in range(128)

    def _config_value(self, value):
        assert value in range(128)

    def _set_session_highlight(
        self, track_offset, scene_offset, width, height, include_return_tracks
    ):
        if not self._suppress_session_highlight:
            ControlSurface._set_session_highlight(
                self, track_offset, scene_offset, width, height, include_return_tracks
            )
