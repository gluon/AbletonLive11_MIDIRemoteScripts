import math
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SessionComponent import SessionComponent
from .SendsMixerComponent import SendsMixerComponent

try:
    exec("from .Settings import Settings")
except ImportError:
    exec("from .Settings import *")

# Stripped down version of SubSelector
class SendsSelectorComponent(ModeSelectorComponent):
    def __init__(self, matrix, side_buttons, session, control_surface):
        assert isinstance(matrix, ButtonMatrixElement)
        assert (matrix.width() == 8) and (matrix.height() == 8)
        assert isinstance(side_buttons, tuple)
        assert len(side_buttons) == 8
        assert isinstance(session, SessionComponent)

        ModeSelectorComponent.__init__(self)

        self._control_surface = control_surface
        self._session = session
        self._mixer = SendsMixerComponent(matrix.width())
        self._matrix = matrix
        self._mixer.name = "Mixer"
        self._mixer.selected_strip().name = "Selected_Channel_strip"
        for column in range(matrix.width()):
            self._mixer.channel_strip(column).name = "Channel_Strip_" + str(column)

        self._side_buttons = side_buttons[4:]
        self._update_callback = None
        self._session.set_mixer(self._mixer)
        self.set_modes_buttons(side_buttons[:4])

    def disconnect(self):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._session = None
        self._mixer = None
        self._matrix = None
        self._side_buttons = None
        self._update_callback = None
        ModeSelectorComponent.disconnect(self)

    def set_update_callback(self, callback):
        self._update_callback = callback

    def set_modes_buttons(self, buttons):
        assert (buttons == None) or (isinstance(buttons, tuple))
        assert len(buttons) == self.number_of_modes()
        identify_sender = True
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        if buttons != None:
            for button in buttons:
                assert isinstance(button, ButtonElement)
                self._modes_buttons.append(button)
                button.add_value_listener(self._mode_value, identify_sender)

    def set_mode(self, mode):
        assert isinstance(mode, int)
        assert mode in range(-1, self.number_of_modes())
        if (self._mode_index != mode) or (mode == -1):
            self._mode_index = mode
            self.update()

    def mode(self):
        result = 0
        if self.is_enabled():
            result = self._mode_index + 1
        return result

    def number_of_modes(self):
        return 4

    def on_enabled_changed(self):
        enabled = self.is_enabled()

        self._mixer.set_enabled(enabled)
        self.set_mode(-1)

    def release_controls(self):
        for track in range(self._matrix.width()):
            for row in range(self._matrix.height()):
                self._matrix.get_button(track, row).set_on_off_values(
                    127, "DefaultButton.Disabled"
                )

            strip = self._mixer.channel_strip(track)
            strip.set_default_buttons(None, None)
            strip.set_send_controls((None, None))

    def update(self):
        super(SendsSelectorComponent, self).update()
        assert self._modes_buttons != None
        if self.is_enabled():
            if self._modes_buttons != None:
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

            for button in self._side_buttons:
                button.set_on_off_values(127, "DefaultButton.Disabled")
                button.turn_off()

            self._mixer.set_allow_update(False)
            self._session.set_allow_update(False)
            if self._mode_index == -1:
                self._setup_mixer_overview()
            elif self._mode_index == 2:
                self._setup_send1_mode()
            elif self._mode_index == 3:
                self._setup_send2_mode()
            else:
                assert False
            if self._update_callback != None:
                self._update_callback()
            self._mixer.set_allow_update(True)
            self._session.set_allow_update(True)
        else:
            self.release_controls()

    def _setup_mixer_overview(self):
        stop_buttons = []
        for track in range(self._matrix.width()):
            strip = self._mixer.channel_strip(track)
            strip.set_send_controls((None, None))
            for row in range(self._matrix.height()):
                if row == 2:
                    self._matrix.get_button(track, row).set_on_off_values("Mixer.Sends")
                elif row == 3:
                    self._matrix.get_button(track, row).set_on_off_values("Mixer.Sends")

            strip.set_default_buttons(
                self._matrix.get_button(track, 0),
                self._matrix.get_button(track, 1),
            )

            for button in self._side_buttons:
                # TODO Set send buttons here?
                # if list(self._side_buttons).index(button) == 0:
                #     button.set_on_off_values("Mixer.Stop")
                pass

            button.force_next_send()
            button.turn_off()

    def _setup_send1_mode(self):
        for track in range(self._matrix.width()):
            strip = self._mixer.channel_strip(track)
            strip.set_default_buttons(None, None)
            for row in range(self._matrix.height()):
                self._matrix.get_button(track, row).set_on_off_values(
                    "Mixer.SendsSlider_1"
                )

        # TODO set button as slider

        # self._session.set_stop_track_clip_buttons(None)
        # self._session.set_stop_all_clips_button(None)
        # self._mixer.set_global_buttons(None, None, None)

    def _setup_send2_mode(self):
        # TODO generalise sends function
        pass
