# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC_Key_25/MixerComponent.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 847 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Util import nop
import _APC.MixerComponent as ChanStripComponentBase
import _APC.MixerComponent as MixerComponentBase

class ChanStripComponent(ChanStripComponentBase):

    def __init__(self, *a, **k):
        self.reset_button_on_exchange = nop
        (super(ChanStripComponent, self).__init__)(*a, **k)


class MixerComponent(MixerComponentBase):

    def on_num_sends_changed(self):
        if self.send_index is None:
            if self.num_sends > 0:
                self.send_index = 0

    def _create_strip(self):
        return ChanStripComponent()