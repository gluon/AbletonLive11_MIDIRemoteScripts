import logging

from ableton.v2.control_surface import Layer
from ableton.v2.control_surface.mode import AddLayerMode, ModesComponent
from Launchpad_Mini_MK3 import Launchpad_Mini_MK3
from Launchpad_Mini_MK3.skin import skin as default_mk3_skin
from ableton.v2.control_surface.skin import Skin
from ableton.v2.control_surface import merge_skins
from novation.colors import Rgb
from novation.skin import Colors

logger = logging.getLogger(__name__)


class AugmentedColors(Colors):
    class Mixer(Colors.Mixer):
        SendControls = Rgb.PURPLE


augmented_skin = merge_skins(*(default_mk3_skin, Skin(AugmentedColors)))


class Launchpad_Mini_MK3_Augmented(Launchpad_Mini_MK3):
    skin = augmented_skin

    def _create_stop_solo_mute_modes(self):
        self._stop_solo_mute_modes = ModesComponent(
            name=u"Stop_Solo_Mute_Modes",
            is_enabled=False,
            support_momentary_mode_cycling=False,
            layer=Layer(cycle_mode_button=self._elements.scene_launch_buttons_raw[7]),
        )
        # all_rows = self._elements.clip_launch_matrix.submatrix[:, 0:8]
        bottom_row = self._elements.clip_launch_matrix.submatrix[:, 7:8]
        self._stop_solo_mute_modes.add_mode(
            u"launch", None, cycle_mode_button_color=u"Mode.Launch.On"
        )
        self._stop_solo_mute_modes.add_mode(
            u"stop",
            AddLayerMode(self._session, Layer(stop_track_clip_buttons=bottom_row)),
            cycle_mode_button_color=u"Session.StopClip",
        )
        self._stop_solo_mute_modes.add_mode(
            u"solo",
            AddLayerMode(self._mixer, Layer(solo_buttons=bottom_row)),
            cycle_mode_button_color=u"Mixer.SoloOn",
        )
        self._stop_solo_mute_modes.add_mode(
            u"mute",
            AddLayerMode(self._mixer, Layer(mute_buttons=bottom_row)),
            cycle_mode_button_color=u"Mixer.MuteOff",
        )
        self._stop_solo_mute_modes.add_mode(
            u"send_controls",
            AddLayerMode(self._mixer, Layer(send_controls=bottom_row)),
            cycle_mode_button_color=u"Mixer.SendControls",
        )
        self._stop_solo_mute_modes.selected_mode = u"send_controls"
        self._stop_solo_mute_modes.set_enabled(True)
