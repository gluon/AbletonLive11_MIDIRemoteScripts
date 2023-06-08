from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import SUGGESTED_PORT_NAMES_KEY
from .komplete_kontrol_a import Komplete_Kontrol_A

def get_capabilities():
    return {SUGGESTED_PORT_NAMES_KEY: ['Komplete Kontrol A DAW', 'Komplete Kontrol M DAW']}


def create_instance(c_instance):
    return Komplete_Kontrol_A(c_instance=c_instance)