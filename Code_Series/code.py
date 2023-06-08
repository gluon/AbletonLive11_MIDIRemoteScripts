from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from ableton.v2.base import const, inject
from ableton.v2.control_surface import Layer, SimpleControlSurface
from ableton.v2.control_surface.components import MixerComponent, SessionRingComponent, TransportComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement
from .element_utils import make_button, make_encoder, make_slider
from .mixer_navigation import MixerNavigationComponent
from .skin_default import make_default_skin

class Code(SimpleControlSurface):
    mixer_navigation_type = MixerNavigationComponent

    def __init__(self, *a, **k):
        (super(Code, self).__init__)(*a, **k)
        with self.component_guard():
            with inject(skin=(const(make_default_skin()))).everywhere():
                self._create_controls()
            self._create_transport()
            self._create_mixer()
            self._create_mixer_navigation()

    def _create_controls(self):
        self._rw_button = make_button(91, 'RW_Button')
        self._ff_button = make_button(92, 'FF_Button')
        self._stop_button = make_button(93, 'Stop_Button')
        self._play_button = make_button(94, 'Play_Button')
        self._record_button = make_button(95, 'Record_Button')
        self._faders = ButtonMatrixElement(rows=[
         [make_slider(index, 'Fader_%d' % (index + 1,)) for index in range(8)]],
          name='Faders')
        self._master_fader = make_slider(8, 'Master_Fader')
        self._encoders = ButtonMatrixElement(rows=[
         [make_encoder(index + 16, 'Encoder_%d' % (index + 1,)) for index in range(8)]],
          name='Encoders')
        self._track_select_buttons = ButtonMatrixElement(rows=[
         [make_button(index + 24, 'Track_Select_Button_%d' % (index + 1,)) for index in range(8)]],
          name='Track_Select_Buttons')
        self._mute_buttons = ButtonMatrixElement(rows=[
         [make_button(index + 8, 'Mute_Button_%d' % (index + 1,)) for index in range(8)]],
          name='Mute_Buttons')
        self._solo_buttons = ButtonMatrixElement(rows=[
         [make_button(index + 16, 'Solo_Button_%d' % (index + 1,)) for index in range(8)]],
          name='Solo_Buttons')
        self._arm_buttons = ButtonMatrixElement(rows=[
         [make_button(index, 'Record_Arm_Button_%d' % (index + 1,)) for index in range(8)]],
          name='Record_Arm_Buttons')
        self._bank_up_button = make_button(47, 'Bank_Up_Button')
        self._bank_down_button = make_button(46, 'Bank_Down_Button')

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport',
          is_enabled=False,
          layer=Layer(seek_forward_button=(self._ff_button),
          seek_backward_button=(self._rw_button),
          stop_button=(self._stop_button),
          play_button=(self._play_button),
          record_button=(self._record_button)))
        self._transport.set_enabled(True)

    def _create_mixer(self):
        self._session_ring = SessionRingComponent(name='Session_Navigation',
          num_tracks=8,
          num_scenes=0,
          is_enabled=False)
        self._mixer = MixerComponent(name='Mixer',
          is_enabled=False,
          tracks_provider=(self._session_ring),
          invert_mute_feedback=True,
          layer=Layer(volume_controls=(self._faders),
          pan_controls=(self._encoders),
          track_select_buttons=(self._track_select_buttons),
          solo_buttons=(self._solo_buttons),
          mute_buttons=(self._mute_buttons),
          arm_buttons=(self._arm_buttons)))
        self._mixer.master_strip().layer = Layer(volume_control=(self._master_fader))
        self._mixer.set_enabled(True)

    def _create_mixer_navigation(self):
        self._mixer_navigation = self.mixer_navigation_type(name='Mixer_Navigation',
          is_enabled=False,
          session_ring=(self._session_ring),
          layer=Layer(page_left_button=(self._bank_down_button),
          page_right_button=(self._bank_up_button)))
        self._mixer_navigation.set_enabled(True)