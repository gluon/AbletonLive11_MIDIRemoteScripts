from __future__ import absolute_import, print_function, unicode_literals
from .launchpad_mini_mk3_send_matrix import Launchpad_Mini_MK3
from ableton.v2.control_surface.capabilities import (
    CONTROLLER_ID_KEY,
    NOTES_CC,
    PORTS_KEY,
    REMOTE,
    SCRIPT,
    SYNC,
    controller_id,
    inport,
    outport,
)


def get_capabilities():
    return {
        CONTROLLER_ID_KEY: controller_id(
            vendor_id=4661, product_ids=[275], model_name=["Launchpad Mini MK3"]
        ),
        PORTS_KEY: [
            inport(props=[NOTES_CC, SCRIPT]),
            inport(props=[NOTES_CC, REMOTE]),
            outport(props=[NOTES_CC, SYNC, SCRIPT]),
            outport(props=[REMOTE]),
        ],
    }


def create_instance(c_instance):
    return Launchpad_Mini_MK3(c_instance=c_instance)
