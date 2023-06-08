from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import GENERIC_SCRIPT_KEY
from .MaxForLive import MaxForLive

def get_capabilities():
    return {GENERIC_SCRIPT_KEY: True}


def create_instance(c_instance):
    return MaxForLive(c_instance=c_instance)