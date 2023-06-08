from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import SUGGESTED_PORT_NAMES_KEY
from .komplete_kontrol_s_mk2 import Komplete_Kontrol_S_Mk2

def get_capabilities():
    return {SUGGESTED_PORT_NAMES_KEY: ['Komplete Kontrol DAW - 1']}


def create_instance(c_instance):
    return Komplete_Kontrol_S_Mk2(c_instance=c_instance)