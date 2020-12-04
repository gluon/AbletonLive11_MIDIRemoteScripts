#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Komplete_Kontrol_A/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from .komplete_kontrol_a import Komplete_Kontrol_A
from ableton.v2.control_surface.capabilities import SUGGESTED_PORT_NAMES_KEY

def get_capabilities():
    return {SUGGESTED_PORT_NAMES_KEY: [u'Komplete Kontrol A DAW', u'Komplete Kontrol M DAW']}


def create_instance(c_instance):
    return Komplete_Kontrol_A(c_instance=c_instance)
