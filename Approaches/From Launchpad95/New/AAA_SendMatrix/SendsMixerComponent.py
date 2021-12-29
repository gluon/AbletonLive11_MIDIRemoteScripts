from _Framework.MixerComponent import MixerComponent
from .SendsChannelStripComponent import SendsChannelStripComponent


class SendsMixerComponent(MixerComponent):

    """Stripped down version of SpecialMixerComponent"""

    def __init__(self, num_tracks, num_returns=0):
        MixerComponent.__init__(self, num_tracks, num_returns)

    def disconnect(self):
        MixerComponent.disconnect(self)

    def _reassign_tracks(self):
        MixerComponent._reassign_tracks(self)

    def _create_strip(self):
        return SendsChannelStripComponent()

    def update(self):
        MixerComponent.update(self)

    def set_enabled(self, enabled):
        MixerComponent.set_enabled(self, enabled)
