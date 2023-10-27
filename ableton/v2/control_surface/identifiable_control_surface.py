# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\identifiable_control_surface.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 2969 bytes
from __future__ import absolute_import, print_function, unicode_literals
import logging
from ..base import task
from . import midi
from .control_surface import ControlSurface
logger = logging.getLogger(__name__)

class IdentifiableControlSurface(ControlSurface):
    identity_request_delay = 0.0
    identity_request = midi.SYSEX_IDENTITY_REQUEST_MESSAGE

    def __init__(self, product_id_bytes=None, *a, **k):
        (super(IdentifiableControlSurface, self).__init__)(*a, **k)
        self._product_id_bytes = product_id_bytes
        self._identity_response_pending = False
        self._request_task = self._tasks.add(task.sequence(task.wait(self.identity_request_delay), task.run(self._send_identity_request)))
        self._request_task.kill()

    def on_identified(self, response_bytes):
        self.refresh_state()

    def port_settings_changed(self):
        self._request_task.restart()

    def process_midi_bytes(self, midi_bytes, midi_processor):
        if midi.is_sysex(midi_bytes) and self._is_identity_response(midi_bytes):
            product_id_bytes = self._extract_product_id_bytes(midi_bytes)
            if product_id_bytes == self._product_id_bytes:
                self._request_task.kill()
                if self._identity_response_pending:
                    self.on_identified(midi_bytes)
                    self._identity_response_pending = False
            else:
                logger.error('MIDI device responded with wrong product id (%s != %s).', str(self._product_id_bytes), str(product_id_bytes))
        else:
            super(IdentifiableControlSurface, self).process_midi_bytes(midi_bytes, midi_processor)

    def _is_identity_response(self, midi_bytes):
        return midi_bytes[3:5] == (
         midi.SYSEX_GENERAL_INFO,
         midi.SYSEX_IDENTITY_RESPONSE_ID)

    def _extract_product_id_bytes(self, midi_bytes):
        return midi_bytes[5:5 + len(self._product_id_bytes)]

    def _send_identity_request(self):
        self._identity_response_pending = True
        self._send_midi(self.identity_request)