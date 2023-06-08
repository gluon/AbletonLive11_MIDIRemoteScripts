from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.capabilities import CONTROLLER_ID_KEY, HIDDEN, NOTES_CC, PORTS_KEY, SCRIPT, SYNC, controller_id, inport, outport
from universal import UniversalControlSurfaceSpecification, create_skin, create_ucs_instance
from .colors import Rgb, Skin
from .elements import Elements
from .mappings import create_mappings

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536,
                          product_ids=[78],
                          model_name=['APC Key 25 mk2']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC]),
                 inport(props=[NOTES_CC, SCRIPT, HIDDEN]),
                 outport(props=[NOTES_CC]),
                 outport(props=[NOTES_CC, SCRIPT, SYNC, HIDDEN])]}


def create_instance(c_instance):
    return create_ucs_instance(name='APC_Key_25_mk2',
      specification=Specification,
      c_instance=c_instance)


class Specification(UniversalControlSurfaceSpecification):
    elements_type = Elements
    control_surface_skin = create_skin(skin=Skin, colors=Rgb)
    num_tracks = 8
    num_scenes = 5
    include_returns = True
    identity_response_id_bytes = (71, 78, 0, 25)
    create_mappings_function = create_mappings