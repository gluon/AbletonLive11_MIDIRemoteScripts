from _Framework.MixerComponent import MixerComponent
from .SendsChannelStripComponent import SendsChannelStripComponent


class SendsMixerComponent(MixerComponent):

    """Stripped down version of SpecialMixerComponent"""

    def _create_strip(self):
        return SendsChannelStripComponent()
