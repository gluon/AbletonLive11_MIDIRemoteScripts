#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad/MainSelectorComponent.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from builtins import range
from _Framework.SessionZoomingComponent import DeprecatedSessionZoomingComponent
from .SpecialSessionComponent import SpecialSessionComponent
from .SubSelectorComponent import *
SESSION_MODE = 0
USER_1_MODE = 1
USER_2_MODE = 2
MIXER_MODE = 3

class MainSelectorComponent(ModeSelectorComponent):
    u""" Class that reassigns the button on the launchpad to different functions """

    def __init__(self, matrix, top_buttons, side_buttons, config_button):
        assert isinstance(matrix, ButtonMatrixElement)
        assert matrix.width() == 8 and matrix.height() == 8
        assert isinstance(top_buttons, tuple)
        assert len(top_buttons) == 8
        assert isinstance(side_buttons, tuple)
        assert len(side_buttons) == 8
        assert isinstance(config_button, ButtonElement)
        ModeSelectorComponent.__init__(self)
        self._session = SpecialSessionComponent(matrix.width(), matrix.height())
        self._zooming = DeprecatedSessionZoomingComponent(self._session)
        self._session.name = u'Session_Control'
        self._zooming.name = u'Session_Overview'
        self._matrix = matrix
        self._side_buttons = side_buttons
        self._nav_buttons = top_buttons[:4]
        self._config_button = config_button
        self._zooming.set_empty_value(LED_OFF)
        self._all_buttons = []
        for button in self._side_buttons + self._nav_buttons:
            self._all_buttons.append(button)

        self._sub_modes = SubSelectorComponent(matrix, side_buttons, self._session)
        self._sub_modes.name = u'Mixer_Modes'
        self._sub_modes.set_update_callback(self._update_control_channels)
        self._init_session()
        self._all_buttons = tuple(self._all_buttons)
        self.set_modes_buttons(top_buttons[4:])

    def disconnect(self):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._session = None
        self._zooming = None
        for button in self._all_buttons:
            button.set_on_off_values(127, LED_OFF)

        self._config_button.turn_off()
        self._matrix = None
        self._side_buttons = None
        self._nav_buttons = None
        self._config_button = None
        ModeSelectorComponent.disconnect(self)

    def session_component(self):
        return self._session

    def set_modes_buttons(self, buttons):
        assert buttons == None or isinstance(buttons, tuple) or len(buttons) == self.number_of_modes()
        identify_sender = True
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        if buttons != None:
            for button in buttons:
                assert isinstance(button, ButtonElement)
                self._modes_buttons.append(button)
                button.add_value_listener(self._mode_value, identify_sender)

        self.set_mode(SESSION_MODE)

    def number_of_modes(self):
        return 4

    def on_enabled_changed(self):
        self.update()

    def set_mode(self, mode):
        assert mode in range(self.number_of_modes())
        if self._mode_index != mode or mode == MIXER_MODE:
            self._mode_index = mode
            self.update()

    def channel_for_current_mode(self):
        new_channel = self._mode_index + self._sub_modes.mode()
        if new_channel > 0:
            new_channel += 3
        return new_channel

    def update(self):
        super(MainSelectorComponent, self).update()
        assert self._modes_buttons != None
        if self.is_enabled():
            for index in range(len(self._modes_buttons)):
                self._modes_buttons[index].set_force_next_value()
                if index == self._mode_index:
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()

            for scene_index in range(8):
                self._side_buttons[scene_index].set_enabled(True)
                for track_index in range(8):
                    self._matrix.get_button(track_index, scene_index).set_enabled(True)

            for button in self._nav_buttons:
                button.set_enabled(True)

            as_active = True
            as_enabled = True
            self._session.set_allow_update(False)
            self._zooming.set_allow_update(False)
            self._config_button.send_value(40)
            self._config_button.send_value(1)
            release_buttons = self._mode_index == USER_1_MODE
            if self._mode_index == SESSION_MODE:
                self._setup_mixer(not as_active)
                self._setup_session(as_active, as_enabled)
            elif self._mode_index == USER_1_MODE:
                self._setup_session(not as_active, not as_enabled)
                self._setup_mixer(not as_active)
                self._setup_user(release_buttons)
            elif self._mode_index == USER_2_MODE:
                self._setup_session(not as_active, not as_enabled)
                self._setup_mixer(not as_active)
                self._setup_user(release_buttons)
            elif self._mode_index == MIXER_MODE:
                self._setup_session(not as_active, as_enabled)
                self._setup_mixer(as_active)
            else:
                assert False
            self._session.set_allow_update(True)
            self._zooming.set_allow_update(True)
            self._update_control_channels()

    def _update_control_channels(self):
        new_channel = self.channel_for_current_mode()
        for button in self._all_buttons:
            button.set_channel(new_channel)
            button.set_force_next_value()

    def _setup_session(self, as_active, as_enabled):
        assert isinstance(as_active, type(False))
        for button in self._nav_buttons:
            if as_enabled:
                button.set_on_off_values(GREEN_FULL, GREEN_THIRD)
            else:
                button.set_on_off_values(127, LED_OFF)

        for scene_index in range(8):
            scene = self._session.scene(scene_index)
            if as_active:
                scene_button = self._side_buttons[scene_index]
                scene_button.set_on_off_values(127, LED_OFF)
                scene.set_launch_button(scene_button)
            else:
                scene.set_launch_button(None)
            for track_index in range(8):
                if as_active:
                    button = self._matrix.get_button(track_index, scene_index)
                    button.set_on_off_values(127, LED_OFF)
                    scene.clip_slot(track_index).set_launch_button(button)
                else:
                    scene.clip_slot(track_index).set_launch_button(None)

        if as_active:
            self._zooming.set_zoom_button(self._modes_buttons[0])
            self._zooming.set_button_matrix(self._matrix)
            self._zooming.set_scene_bank_buttons(self._side_buttons)
            self._zooming.set_nav_buttons(self._nav_buttons[0], self._nav_buttons[1], self._nav_buttons[2], self._nav_buttons[3])
            self._zooming.update()
        else:
            self._zooming.set_zoom_button(None)
            self._zooming.set_button_matrix(None)
            self._zooming.set_scene_bank_buttons(None)
            self._zooming.set_nav_buttons(None, None, None, None)
        if as_enabled:
            self._session.set_track_bank_buttons(self._nav_buttons[3], self._nav_buttons[2])
            self._session.set_scene_bank_buttons(self._nav_buttons[1], self._nav_buttons[0])
        else:
            self._session.set_track_bank_buttons(None, None)
            self._session.set_scene_bank_buttons(None, None)

    def _setup_mixer(self, as_active):
        assert isinstance(as_active, type(False))
        if as_active and self._sub_modes.is_enabled():
            self._sub_modes.set_mode(-1)
        self._sub_modes.set_enabled(as_active)

    def _setup_user(self, release_buttons):
        for scene_index in range(8):
            scene_button = self._side_buttons[scene_index]
            scene_button.set_on_off_values(127, LED_OFF)
            scene_button.turn_off()
            scene_button.set_enabled(not release_buttons)
            for track_index in range(8):
                button = self._matrix.get_button(track_index, scene_index)
                button.set_on_off_values(127, LED_OFF)
                button.turn_off()
                button.set_enabled(not release_buttons)

        for button in self._nav_buttons:
            button.set_on_off_values(127, LED_OFF)
            button.turn_off()
            button.set_enabled(not release_buttons)

        if self._mode_index == USER_1_MODE:
            self._config_button.send_value(2)
        self._config_button.send_value(32, force=True)

    def _init_session(self):
        self._session.set_stop_clip_value(AMBER_THIRD)
        self._session.set_stop_clip_triggered_value(AMBER_BLINK)
        for scene_index in range(self._matrix.height()):
            scene = self._session.scene(scene_index)
            scene.set_triggered_value(GREEN_BLINK)
            scene.name = u'Scene_' + str(scene_index)
            for track_index in range(self._matrix.width()):
                clip_slot = scene.clip_slot(track_index)
                clip_slot.set_triggered_to_play_value(GREEN_BLINK)
                clip_slot.set_triggered_to_record_value(RED_BLINK)
                clip_slot.set_stopped_value(AMBER_FULL)
                clip_slot.set_started_value(GREEN_FULL)
                clip_slot.set_recording_value(RED_FULL)
                clip_slot.name = str(track_index) + u'_Clip_Slot_' + str(scene_index)
                self._all_buttons.append(self._matrix.get_button(track_index, scene_index))

        self._zooming.set_stopped_value(RED_FULL)
        self._zooming.set_selected_value(AMBER_FULL)
        self._zooming.set_playing_value(GREEN_FULL)
