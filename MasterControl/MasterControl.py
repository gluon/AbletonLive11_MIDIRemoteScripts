#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/MasterControl/MasterControl.py
from __future__ import absolute_import, print_function, unicode_literals
from MackieControl.MackieControl import MackieControl

class MasterControl(MackieControl):
    u""" Main class derived from MackieControl """

    def __init__(self, c_instance):
        MackieControl.__init__(self, c_instance)
