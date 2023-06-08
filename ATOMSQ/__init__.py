from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v3.base import listens
from ableton.v3.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from ableton.v3.control_surface.components import MixerComponent, TranslatingBackgroundComponent
from universal import UniversalControlSurface, UniversalControlSurfaceSpecification, create_skin
from . import midi
from .button_labels import ButtonLabelsComponent
from .channel_strip import ChannelStripComponent
from .colors import Rgb
from .elements import SESSION_HEIGHT, SESSION_WIDTH, Elements
from .launch_and_stop import LaunchAndStopComponent
from .mappings import create_mappings
from .simple_device import SimpleDeviceParameterComponent
from .skin import Skin

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6479,
                          product_ids=[522],
                          model_name=['ATM SQ']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC, SYNC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return ATOMSQ(c_instance=c_instance)


class Specification(UniversalControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    num_tracks = SESSION_WIDTH
    num_scenes = SESSION_HEIGHT
    link_session_ring_to_track_selection = True
    identity_response_id_bytes = midi.PRODUCT_ID_BYTES
    hello_messages = (midi.NATIVE_MODE_ON_MESSAGE,)
    goodbye_messages = (midi.NATIVE_MODE_OFF_MESSAGE,)
    create_mappings_function = create_mappings
    quantized_parameter_sensitivity = 0.3
    component_map = {'Button_Labels':ButtonLabelsComponent, 
     'Launch_And_Stop':LaunchAndStopComponent, 
     'Mixer':partial(MixerComponent,
       channel_strip_component_type=ChannelStripComponent), 
     'Simple_Device':SimpleDeviceParameterComponent, 
     'Translating_Background':partial(TranslatingBackgroundComponent,
       translation_channel=midi.USER_MODE_START_CHANNEL)}


class ATOMSQ(UniversalControlSurface):

    def __init__(self, *a, **k):
        (super().__init__)(a, specification=Specification, **k)

    def setup(self):
        super().setup()
        self._ATOMSQ__on_main_modes_changed.subject = self.component_map['Main_Modes']
        self._update_firmware()

    def on_identified(self, response_bytes):
        self.schedule_message(1, self._update_firmware)
        super().on_identified(response_bytes)

    @listens('selected_mode')
    def __on_main_modes_changed(self, mode):
        self._update_firmware()
        self.component_map['Button_Labels'].show_button_labels_for_mode(mode)
        self.elements.track_name_display.clear_send_cache()
        self.elements.device_name_display.clear_send_cache()

    def _update_firmware(self):
        mode = self.component_map['Main_Modes'].selected_mode
        self.elements.lower_firmware_toggle_switch.send_value(bool(mode != 'song'))
        self.elements.upper_firmware_toggle_switch.send_value(bool(mode == 'instrument'))