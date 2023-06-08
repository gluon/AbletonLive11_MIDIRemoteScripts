from __future__ import absolute_import, print_function, unicode_literals
from _Komplete_Kontrol.komplete_kontrol_base import KompleteKontrolBase, Layer, create_button, create_encoder
from .view_control_component import ViewControlComponent

class Komplete_Kontrol_A(KompleteKontrolBase):

    def _create_controls(self):
        super(Komplete_Kontrol_A, self)._create_controls()
        self._mute_button = create_button(67, 'Mute_Button')
        self._solo_button = create_button(68, 'Solo_Button')
        self._vertical_encoder = create_encoder(48, 'Vertical_Encoder')
        self._horizontal_encoder = create_encoder(50, 'Horizontal_Encoder')

    def _create_components(self):
        super(Komplete_Kontrol_A, self)._create_components()
        self._create_view_control()

    def _create_view_control(self):
        self._view_control = ViewControlComponent(name='View_Control',
          is_enabled=False,
          layer=Layer(vertical_encoder=(self._vertical_encoder),
          horizontal_encoder=(self._horizontal_encoder)))

    def _create_mixer_component_layer(self):
        return super(Komplete_Kontrol_A, self)._create_mixer_component_layer() + Layer(mute_button=(self._mute_button),
          solo_button=(self._solo_button))