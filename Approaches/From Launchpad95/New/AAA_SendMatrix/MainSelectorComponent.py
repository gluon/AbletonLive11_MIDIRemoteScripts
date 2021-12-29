# -*- coding: utf-8 -*-

from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from .SpecialSessionComponent import SpecialSessionComponent
from .SendsSelectorComponent import SendsSelectorComponent

try:
    exec("from .Settings import Settings")
except ImportError:
    exec("from .Settings import *")


class MainSelectorComponent(ModeSelectorComponent):

    """Class that reassigns the button on the launchpad to different functions"""

    # def log(self, message):
    # 	self._control_surface.log_message((' ' + message + ' ').center(50, '='))

    def __init__(
        self,
        matrix,
        top_buttons,
        side_buttons,
        config_button,
        control_surface,
    ):
        # verify matrix dimentions
        assert isinstance(matrix, ButtonMatrixElement)
        assert (matrix.width() == 8) and (matrix.height() == 8)
        assert isinstance(top_buttons, tuple)
        assert len(top_buttons) == 8
        assert isinstance(side_buttons, tuple)
        assert len(side_buttons) == 8
        assert isinstance(config_button, ButtonElement)
        ModeSelectorComponent.__init__(self)  # super constructor

        # inject ControlSurface
        self._matrix = matrix
        self._nav_buttons = top_buttons[:4]  # arrow buttons
        self._mode_buttons = top_buttons[4:]  # session,drums,keys,user buttons
        self._side_buttons = side_buttons  # scene launch buttons
        self._config_button = config_button  # used to reset launchpad
        self._control_surface = control_surface

        # initialize index variables
        self._mode_index = 0  # Inherited from parent
        self._main_mode_index = 0  # LP original modes
        self._sub_mode_list = [0, 0, 0, 0]
        for index in range(4):
            self._sub_mode_list[index] = 0
        self.set_mode_buttons(self._mode_buttons)

        # Create session
        self._session = SpecialSessionComponent(
            matrix.width(), matrix.height(), None, self._control_surface, self
        )
        self._session.name = "Session_Control"

        # Non-Matrix buttons
        self._all_buttons = []
        for button in self._side_buttons + self._nav_buttons:
            self._all_buttons.append(button)

        self._sub_modes = SendsSelectorComponent(
            matrix, side_buttons, self._session, self._control_surface
        )
        self._sub_modes.name = "Mixer_Modes"
        self._sub_modes.set_update_callback(self._update_control_channels)

        self._init_session()
        self._all_buttons = tuple(self._all_buttons)

    def disconnect(self):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._session = None
        for button in self._all_buttons:
            button.set_on_off_values("DefaultButton.Disabled", "DefaultButton.Disabled")

        self._config_button.turn_off()
        self._matrix = None
        self._side_buttons = None
        self._nav_buttons = None
        self._config_button = None
        ModeSelectorComponent.disconnect(self)

    def session_component(self):
        return self._session

    def _update_mode(self):
        mode = self._modes_heap[-1][
            0
        ]  # get first value of last _modes_heap tuple. _modes_heap tuple structure is (mode, sender, observer)

        self.log_message(f"Mode: {mode}")
        assert mode in range(self.number_of_modes())  # 8 for this script

        # TODO Come back here and figure out what this is doing
        if self._main_mode_index == mode:
            if (
                self._main_mode_index == 1
            ):  # user mode 1 and device controller and instrument mode
                self._sub_mode_list[self._main_mode_index] = (
                    self._sub_mode_list[self._main_mode_index] + 1
                ) % len(Settings.USER_MODES_1)
                self.update()
            elif self._main_mode_index == 2:  # user mode 2  and step sequencer
                self._sub_mode_list[self._main_mode_index] = (
                    self._sub_mode_list[self._main_mode_index] + 1
                ) % len(Settings.USER_MODES_2)
                self.update()
            elif self._main_mode_index == 3:  # Mixer mode
                self.update()
            else:  # Session mode
                self._sub_mode_list[self._main_mode_index] = 0
                self._mode_index = 0

        else:
            self._main_mode_index = mode
            self.update()

    def set_mode(self, mode):
        self._clean_heap()
        self._modes_heap = [(mode, None, None)]

    def number_of_modes(self):
        return 1 + 3 + 3 + 1

    def on_enabled_changed(self):
        self.update()

    def _update_mode_buttons(self):
        self._modes_buttons[0].set_on_off_values("Mode.Session.On", "Mode.Session.Off")
        self._modes_buttons[3].set_on_off_values("Mode.Mixer.On", "Mode.Mixer.Off")
        mode1 = self.getSkinName(Settings.USER_MODES_1[self._sub_mode_list[1]])
        mode2 = self.getSkinName(Settings.USER_MODES_2[self._sub_mode_list[2]])
        self._modes_buttons[1].set_on_off_values(
            "Mode." + mode1 + ".On", "Mode." + mode1 + ".Off"
        )
        self._modes_buttons[2].set_on_off_values(
            "Mode." + mode2 + ".On", "Mode." + mode2 + ".Off"
        )

        for index in range(4):
            if index == self._main_mode_index:
                self._modes_buttons[index].turn_on()
            else:
                self._modes_buttons[index].turn_off()

    def getSkinName(self, user2Mode):
        if user2Mode == "instrument":
            user2Mode = "Note"
        if user2Mode == "device":
            user2Mode = "Device"
        if user2Mode == "user 1":
            user2Mode = "User"
        if user2Mode == "user 2":
            user2Mode = "User2"
        if user2Mode == "drum stepseq":
            user2Mode = "StepSequencer"
        if user2Mode == "melodic stepseq":
            user2Mode = "StepSequencer2"
        return user2Mode

    def channel_for_current_mode(self):
        # in this code, midi channels start at 0.
        # so channels range from 0 - 15.
        # mapping to 1-16 in the real world

        if self._main_mode_index == 0:
            new_channel = 0  # session

        elif self._main_mode_index == 1:
            if self._sub_mode_list[self._main_mode_index] == 0:
                new_channel = 11  # instrument controller
                # instrument controller uses base channel plus the 4 next ones. 11,12,13,14,15
                if self._instrument_controller != None:
                    self._instrument_controller.base_channel = new_channel
            elif self._sub_mode_list[self._main_mode_index] == 1:
                new_channel = 3  # device controller
            elif self._sub_mode_list[self._main_mode_index] == 2:
                new_channel = 4  # plain user mode 1

        elif self._main_mode_index == 2:
            if self._sub_mode_list[self._main_mode_index] == 0:
                new_channel = 1  # step seq
            elif self._sub_mode_list[self._main_mode_index] == 1:
                new_channel = 2  # melodic step seq
            elif self._sub_mode_list[self._main_mode_index] == 2:
                new_channel = 5  # plain user mode 2

        elif self._main_mode_index == 3:  # mixer modes
            # mixer uses base channel 7 and the 4 next ones.
            new_channel = 6 + self._sub_modes.mode()  # 6,7,8,9,10

        return new_channel

    def update(self):
        assert self._modes_buttons != None
        if self.is_enabled():

            self._update_mode_buttons()

            as_active = True
            as_enabled = True
            self._session.set_allow_update(False)
            self._config_button.send_value(
                40
            )  # Set LP double buffering mode (investigate this)
            self._config_button.send_value(1)  # Set LP X-Y layout grid mapping mode

            if self._main_mode_index == 0:
                # session
                self._control_surface.show_message("SESSION MODE")
                self._setup_session(as_active, as_enabled)
                self._update_control_channels()
                self._mode_index = 0

            self._session.set_allow_update(True)

    def _setup_session(self, as_active, as_navigation_enabled):
        assert isinstance(as_active, type(False))  # assert is boolean
        for button in self._nav_buttons:
            if as_navigation_enabled:
                button.set_on_off_values("Mode.Session.On", "Mode.Session.Off")
            else:
                button.set_on_off_values(
                    "DefaultButton.Disabled", "DefaultButton.Disabled"
                )

        if as_active:
            self._activate_navigation_buttons(True)
            self._activate_matrix(True)
            if self._sub_modes.is_enabled():  # go back to default mode
                self._sub_modes.set_mode(-1)
            else:
                self._sub_modes.release_controls()

        self._sub_modes.set_enabled(as_active)

        # TODO This is iterating through all scenes and tracks—We want to make a send button on each track / send combo
        # matrix
        self._activate_matrix(True)
        for scene_index in range(self._session._num_scenes):  # iterate over scenes
            scene = self._session.scene(scene_index)
            # if as_active:  # set scene launch buttons
            #     scene_button = self._side_buttons[scene_index]
            #     scene_button.set_enabled(as_active)
            #     scene_button.set_on_off_values(
            #         "DefaultButton.Disabled", "DefaultButton.Disabled"
            #     )
            #     scene.set_launch_button(scene_button)
            # else:
            #     scene.set_launch_button(None)

            for track_index in range(
                self._session._num_tracks
            ):  # iterate over tracks of a scene -> clip slots
                if as_active:  # set clip slot launch button
                    button = self._matrix.get_button(track_index, scene_index)
                    # button.set_on_off_values(
                    #     "DefaultButton.Disabled", "DefaultButton.Disabled"
                    # )
                    # button.set_enabled(as_active)
                    # scene.clip_slot(track_index).set_launch_button(button)
                else:
                    scene.clip_slot(track_index).set_launch_button(None)

                # FOR each SCENE??

        if as_navigation_enabled:  # track nav buttons (don't need scene nav)
            self._session.set_track_bank_buttons(
                self._nav_buttons[3], self._nav_buttons[2]
            )
        else:
            self._session.set_track_bank_buttons(None, None)

    def _init_session(self):
        session_height = self._matrix.height()

        for scene_index in range(session_height):
            for track_index in range(self._matrix.width()):
                self._all_buttons.append(
                    self._matrix.get_button(track_index, scene_index)
                )

    def _activate_navigation_buttons(self, active):
        for button in self._nav_buttons:
            button.set_enabled(active)

    def _activate_scene_buttons(self, active):
        for button in self._side_buttons:
            button.set_enabled(active)

    def _activate_matrix(self, active):
        for scene_index in range(8):
            for track_index in range(8):
                self._matrix.get_button(track_index, scene_index).set_enabled(active)

    def log_message(self, msg):
        self._control_surface.log_message(msg)

    # Update the channels of the buttons in the user modes..
    def _update_control_channels(self):
        new_channel = self.channel_for_current_mode()
        for button in self._all_buttons:
            button.set_channel(new_channel)
            button.force_next_send()
