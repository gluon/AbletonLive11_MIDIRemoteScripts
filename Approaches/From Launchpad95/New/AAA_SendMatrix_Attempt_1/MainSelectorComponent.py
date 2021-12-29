# -*- coding: utf-8 -*-

from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from .SpecialSessionComponent import SpecialSessionComponent
from .SendsMixerComponent import SendsMixerComponent
from .Settings import Settings


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
        self.set_mode_buttons(self._mode_buttons)

        # initialise session
        self._session = SpecialSessionComponent(
            matrix.width(), matrix.height(), None, self._control_surface, self
        )
        self._session.name = "Session_Control"

        # Non-Matrix buttons
        self._all_buttons = []
        for button in self._side_buttons + self._nav_buttons:
            self._all_buttons.append(button)

        self._init_session()
        self._all_buttons = tuple(self._all_buttons)

        # Initialise mixer
        self._mixer = SendsMixerComponent(matrix.width())
        self._mixer.name = "Mixer"
        self._mixer.selected_strip().name = "Selected_Channel_strip"
        for column in range(matrix.width()):
            self._mixer.channel_strip(column).name = "Channel_Strip_" + str(column)
        self._session.set_mixer(self._mixer)

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
        self._mixer = None
        ModeSelectorComponent.disconnect(self)

    def session_component(self):
        return self._session

    def _update_mode(self):
        # Get the mode (the first value of last _modes_heap tuple, where _modes_heap tuple structure is (mode, sender, observer))
        mode = self._modes_heap[-1][0]
        self.log_message(f"Mode: {mode}")

        # TODO Come back here and figure out what this is doing
        if self._main_mode_index == mode:
            # Mixer mode
            if self._main_mode_index == 3:
                self.update()
            # Session mode
            else:
                self._mode_index = 0

        else:
            self._main_mode_index = mode
            self.update()

    def set_mode(self, mode):
        self._clean_heap()
        self._modes_heap = [(mode, None, None)]

    def on_enabled_changed(self):
        self.update()

    def _update_mode_buttons(self):
        self._modes_buttons[0].set_on_off_values("Mode.Session.On", "Mode.Session.Off")

        for index in range(4):
            if index == self._main_mode_index:
                self._modes_buttons[index].turn_on()
            else:
                self._modes_buttons[index].turn_off()

    def update(self):
        assert self._modes_buttons != None
        if self.is_enabled():

            self._update_mode_buttons()

            as_active = True
            as_enabled = True
            self._mixer.set_allow_update(False)
            self._session.set_allow_update(False)

            # Set LP double buffering mode (investigate this)
            self._config_button.send_value(40)
            # Set LP X-Y layout grid mapping mode
            self._config_button.send_value(1)

            if self._main_mode_index == 0:
                # session
                self._control_surface.show_message("Sends matrix mode")
                self._setup_session(as_active, as_enabled)
                self._update_control_channels()
                self._mode_index = 0

            for index in range(len(self._modes_buttons)):
                button = self._modes_buttons[index]
                if index == 2:
                    button.set_on_off_values("Mixer.Sends")
                elif index == 3:
                    button.set_on_off_values("Mixer.Sends")
                if index == self._mode_index:
                    button.turn_off()
                else:
                    button.turn_on()

            self._mixer.set_allow_update(True)
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
            for track in range(self._matrix.width()):
                for row in range(self._matrix.height()):
                    self._matrix.get_button(track, row).set_on_off_values(
                        127, "DefaultButton.Disabled"
                    )

                strip = self._mixer.channel_strip(track)
                strip.set_default_buttons(None)
                strip.set_send_controls((None, None))

        self._activate_matrix(True)
        # iterate over tracks
        for track_index in range(self._session._num_tracks):
            if as_active:
                for send_index in range(self._matrix.height()):
                    button = self._matrix.get_button(track_index, send_index)
                    strip = self._mixer.channel_strip(track)
                    button.set_on_off_values("Mixer.Sends")
                    button.set_enabled(as_active)

                    strip.set_default_buttons(button)
                    button.force_next_send()
                    button.turn_off()

        # Always have track nav buttons (don't need scene nav because we're not working with clips)
        self._nav_buttons[3], self._nav_buttons[2]

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
        new_channel = 0
        for button in self._all_buttons:
            button.set_channel(new_channel)
            button.force_next_send()

    def _setup_send_mode(self, send_number):
        for track in range(self._matrix.width()):
            strip = self._mixer.channel_strip(track)
            strip.set_default_buttons(None)
            for row in range(self._matrix.height()):
                self._matrix.get_button(track, row).set_on_off_values(
                    f"Mixer.SendsSlider_{send_number}"
                )

        # TODO set button as slider

        # self._session.set_stop_track_clip_buttons(None)
        # self._session.set_stop_all_clips_button(None)
        # self._mixer.set_global_buttons(None, None, None)
