#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/messenger.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.base import const, nop
from ableton.v2.base.dependency import dependency

class Messenger(object):
    message = dependency(message=const(nop))
