from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Util import nop
from _APC.MixerComponent import ChanStripComponent as ChanStripComponentBase
from _APC.MixerComponent import MixerComponent as MixerComponentBase

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