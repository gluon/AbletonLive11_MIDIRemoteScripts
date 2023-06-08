from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const
from ableton.v2.control_surface.elements import ButtonElement

class PadButtonElement(ButtonElement):

    class ProxiedInterface(ButtonElement.ProxiedInterface):
        sensitivity_profile = const(None)

    def __init__(self, pad_id=None, pad_sensitivity_update=None, *a, **k):
        (super(PadButtonElement, self).__init__)(*a, **k)
        self._sensitivity_profile = 'default'
        self._pad_id = pad_id
        self._pad_sensitivity_update = pad_sensitivity_update

    def _get_sensitivity_profile(self):
        return self._sensitivity_profile

    def _set_sensitivity_profile(self, profile):
        if profile != self._sensitivity_profile:
            if self._pad_sensitivity_update is not None:
                self._sensitivity_profile = profile
                self._pad_sensitivity_update.set_pad(self._pad_id, profile)

    sensitivity_profile = property(_get_sensitivity_profile, _set_sensitivity_profile)

    def reset(self):
        self.sensitivity_profile = 'default'
        super(PadButtonElement, self).reset()