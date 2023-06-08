from __future__ import absolute_import, print_function, unicode_literals
import Live
import _Framework.EncoderElement as EncoderElement
from _Framework.InputControlElement import *

class PeekableEncoderElement(EncoderElement):

    def __init__(self, msg_type, channel, identifier, map_mode):
        EncoderElement.__init__(self, msg_type, channel, identifier, map_mode)
        self._peek_mode = False

    def set_peek_mode(self, peek_mode):
        if self._peek_mode != peek_mode:
            self._peek_mode = peek_mode
            self._request_rebuild()

    def get_peek_mode(self):
        return self._peek_mode

    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        current_parameter = self._parameter_to_map_to
        if self._peek_mode:
            self._parameter_to_map_to = None
        InputControlElement.install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback)
        self._parameter_to_map_to = current_parameter