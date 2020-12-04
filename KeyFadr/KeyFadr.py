#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/KeyFadr/KeyFadr.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from KeyPad import KeyPad

class KeyFadr(KeyPad):
    u"""
    Reloop KeyFadr controller script.
    """
    _encoder_range = list(range(80, 72, -1))
    _product_model_id = 102

    def __init__(self, *a, **k):
        super(KeyFadr, self).__init__(*a, **k)
