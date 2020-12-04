#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC_Key_25/APC_Key_25.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from builtins import range
from functools import partial
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import OptimizedControlSurface
from _Framework.ComboElement import ComboElement
from _Framework.Layer import Layer
from _Framework.ModesComponent import AddLayerMode, ModesComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.Resource import SharedResource
from _Framework.Util import nop
from _Framework.TransportComponent import TransportComponent
from _APC.APC import APC, MANUFACTURER_ID
from _APC.ControlElementUtils import make_button, make_knob
from _APC.DeviceComponent import DeviceComponent
from _APC.SkinDefault import make_default_skin, make_biled_skin, make_stop_button_skin
from .SendToggleComponent import SendToggleComponent
from .MixerComponent import MixerComponent

class APC_Key_25(APC, OptimizedControlSurface):
    u""" Script for Akai's APC_Key_25 Controller """
    SESSION_WIDTH = 8
    SESSION_HEIGHT = 5
    HAS_TRANSPORT = True

    def make_shifted_button(self, button):
        return ComboElement(button, modifiers=[self._shift_button])

    @classmethod
    def wrap_matrix(cls, control_list, wrapper = nop):
        return ButtonMatrixElement(rows=[list(map(wrapper, control_list))])

    def __init__(self, *a, **k):
        super(APC_Key_25, self).__init__(*a, **k)
        self._suppress_session_highlight = False
        self._suppress_send_midi = False
        self._color_skin = make_biled_skin()
        self._default_skin = make_default_skin()
        self._stop_button_skin = make_stop_button_skin()
        with self.component_guard():
            self._create_controls()
            self._session = self._create_session()
            self._mixer = self._create_mixer()
            self._device = self._create_device_component()
            if self.HAS_TRANSPORT:
                self._transport = self._create_transport()
            self.set_device_component(self._device)
            self._session.set_mixer(self._mixer)
            self._encoder_modes = self._create_encoder_modes()
            self._track_modes = self._create_track_button_modes()

    def get_matrix_button(self, column, row):
        return self._matrix_buttons[row][column]

    def _create_controls(self):
        make_on_off_button = partial(make_button, skin=self._default_skin)
        make_color_button = partial(make_button, skin=self._color_skin)
        make_stop_button = partial(make_button, skin=self._stop_button_skin)
        self._shift_button = make_button(0, 98, resource_type=SharedResource, name=u'Shift_Button')
        self._parameter_knobs = [ make_knob(0, index + 48, name=u'Parameter_Knob_%d' % (index + 1)) for index in range(self.SESSION_WIDTH) ]
        self._select_buttons = [ make_stop_button(0, 64 + index, name=u'Track_Select_%d' % (index + 1)) for index in range(self.SESSION_WIDTH) ]
        self._up_button = self.make_shifted_button(self._select_buttons[0])
        self._down_button = self.make_shifted_button(self._select_buttons[1])
        self._left_button = self.make_shifted_button(self._select_buttons[2])
        self._right_button = self.make_shifted_button(self._select_buttons[3])
        self._volume_button = self.make_shifted_button(self._select_buttons[4])
        self._pan_button = self.make_shifted_button(self._select_buttons[5])
        self._send_button = self.make_shifted_button(self._select_buttons[6])
        self._device_button = self.make_shifted_button(self._select_buttons[7])
        if self.HAS_TRANSPORT:
            self._play_button = make_on_off_button(0, 91, name=u'Play_Button')
            self._record_button = make_on_off_button(0, 93, name=u'Record_Button')

        def matrix_note(x, y):
            return x + self.SESSION_WIDTH * (self.SESSION_HEIGHT - y - 1)

        self._matrix_buttons = [ [ make_color_button(0, matrix_note(track, scene), name=u'%d_Clip_%d_Button' % (track, scene)) for track in range(self.SESSION_WIDTH) ] for scene in range(self.SESSION_HEIGHT) ]
        self._session_matrix = ButtonMatrixElement(name=u'Button_Matrix', rows=self._matrix_buttons)
        self._scene_launch_buttons = [ make_color_button(0, index + 82, name=u'Scene_Launch_%d' % (index + 1)) for index in range(self.SESSION_HEIGHT) ]
        self._stop_button = self.make_shifted_button(self._scene_launch_buttons[0])
        self._solo_button = self.make_shifted_button(self._scene_launch_buttons[1])
        self._arm_button = self.make_shifted_button(self._scene_launch_buttons[2])
        self._mute_button = self.make_shifted_button(self._scene_launch_buttons[3])
        self._select_button = self.make_shifted_button(self._scene_launch_buttons[4])
        self._stop_all_button = self._make_stop_all_button()

    def _make_stop_all_button(self):
        return make_button(0, 81, name=u'Stop_All_Clips_Button')

    def _create_session(self):
        session = SessionComponent(self.SESSION_WIDTH, self.SESSION_HEIGHT, auto_name=True, enable_skinning=True, is_enabled=False, layer=Layer(scene_launch_buttons=self.wrap_matrix(self._scene_launch_buttons), clip_launch_buttons=self._session_matrix, stop_all_clips_button=self._stop_all_button, track_bank_left_button=self._left_button, track_bank_right_button=self._right_button, scene_bank_up_button=self._up_button, scene_bank_down_button=self._down_button))
        for scene_index in range(self.SESSION_HEIGHT):
            for track_index in range(self.SESSION_WIDTH):
                slot = session.scene(scene_index).clip_slot(track_index)
                slot.layer = Layer(select_button=self._shift_button)

        return session

    def _create_mixer(self):
        return MixerComponent(self.SESSION_WIDTH, auto_name=True, is_enabled=False, invert_mute_feedback=True)

    def _create_device_component(self):
        return DeviceComponent(name=u'Device_Component', is_enabled=False, device_selection_follows_track_selection=True)

    def _create_transport(self):

        def play_toggle_model_transform(value):
            if self._shift_button.is_pressed():
                return False
            return value

        return TransportComponent(name=u'Transport', is_enabled=False, play_toggle_model_transform=play_toggle_model_transform, layer=Layer(play_button=self._play_button, record_button=self._record_button))

    def _create_encoder_modes(self):
        knob_modes = ModesComponent(name=u'Knob Modes', is_enabled=False)
        parameter_knobs_matrix = self.wrap_matrix(self._parameter_knobs)
        send_toggle_component = SendToggleComponent(self._mixer, name=u'Toggle Send', is_enabled=False, layer=Layer(toggle_button=self._send_button, priority=1))
        knob_modes.add_mode(u'volume', AddLayerMode(self._mixer, Layer(volume_controls=parameter_knobs_matrix)))
        knob_modes.add_mode(u'pan', AddLayerMode(self._mixer, Layer(pan_controls=parameter_knobs_matrix)))
        knob_modes.add_mode(u'send', [AddLayerMode(self._mixer, Layer(send_controls=parameter_knobs_matrix)), send_toggle_component])
        knob_modes.add_mode(u'device', AddLayerMode(self._device, Layer(parameter_controls=parameter_knobs_matrix)))
        knob_modes.selected_mode = u'volume'
        knob_modes.layer = Layer(volume_button=self._volume_button, pan_button=self._pan_button, send_button=self._send_button, device_button=self._device_button)
        return knob_modes

    def _create_track_button_modes(self):
        track_button_modes = ModesComponent(name=u'Track Button Modes', is_enabled=False)
        select_button_matrix = self.wrap_matrix(self._select_buttons)
        track_button_modes.add_mode(u'clip_stop', AddLayerMode(self._session, Layer(stop_track_clip_buttons=select_button_matrix)))
        track_button_modes.add_mode(u'solo', AddLayerMode(self._mixer, layer=Layer(solo_buttons=select_button_matrix)))
        track_button_modes.add_mode(u'arm', AddLayerMode(self._mixer, layer=Layer(arm_buttons=select_button_matrix)))
        track_button_modes.add_mode(u'mute', AddLayerMode(self._mixer, layer=Layer(mute_buttons=select_button_matrix)))
        track_button_modes.add_mode(u'select', AddLayerMode(self._mixer, layer=Layer(track_select_buttons=select_button_matrix)))
        track_button_modes.selected_mode = u'clip_stop'
        track_button_modes.layer = Layer(clip_stop_button=self._stop_button, solo_button=self._solo_button, arm_button=self._arm_button, mute_button=self._mute_button, select_button=self._select_button)
        return track_button_modes

    def _set_components_enabled(self, enable):
        with self.component_guard():
            self._session.set_enabled(enable)
            self._mixer.set_enabled(enable)
            self._device.set_enabled(enable)
            if self.HAS_TRANSPORT:
                self._transport.set_enabled(enable)
            self._encoder_modes.set_enabled(enable)
            self._track_modes.set_enabled(enable)

    def _should_combine(self):
        return False

    def _update_hardware(self):
        self.set_highlighting_session_component(None)
        self._set_components_enabled(False)
        self._send_midi((240, 126, 127, 6, 1, 247))

    def _product_model_id_byte(self):
        return 39

    def _on_identity_response(self, midi_bytes):
        super(APC_Key_25, self)._on_identity_response(midi_bytes)
        if midi_bytes[5] == MANUFACTURER_ID and midi_bytes[6] == self._product_model_id_byte():
            self._set_components_enabled(True)
            self.set_highlighting_session_component(self._session)

    def _send_dongle_challenge(self):
        pass

    def _on_handshake_successful(self):
        pass
