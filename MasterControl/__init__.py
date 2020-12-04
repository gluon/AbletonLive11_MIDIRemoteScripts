#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/MasterControl/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from .MasterControl import MasterControl

def create_instance(c_instance):
    return MasterControl(c_instance)
