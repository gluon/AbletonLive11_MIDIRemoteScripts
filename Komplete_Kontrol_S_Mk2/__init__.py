#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Komplete_Kontrol_S_Mk2/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from .komplete_kontrol_s_mk2 import Komplete_Kontrol_S_Mk2
from ableton.v2.control_surface.capabilities import SUGGESTED_PORT_NAMES_KEY

def get_capabilities():
    return {SUGGESTED_PORT_NAMES_KEY: [u'Komplete Kontrol DAW - 1']}


def create_instance(c_instance):
    return Komplete_Kontrol_S_Mk2(c_instance=c_instance)
