# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/IdentifiableControlSurface.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 2662 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from . import Task
from .ControlSurface import ControlSurface
SYSEX_IDENTITY_REQUEST = (240, 126, 0, 6, 1, 247)

class IdentifiableControlSurface(ControlSurface):
    identity_request_delay = 0.5
    identity_request = SYSEX_IDENTITY_REQUEST

    def __init__(self, product_id_bytes=None, *a, **k):
        (super(IdentifiableControlSurface, self).__init__)(*a, **k)
        self._product_id_bytes = product_id_bytes
        self._identity_response_pending = False
        self._request_task = self._tasks.add(Task.sequence(Task.wait(self.identity_request_delay), Task.run(self._send_identity_request)))
        self._request_task.kill()

    def on_identified(self):
        raise NotImplementedError

    def port_settings_changed(self):
        self._request_task.restart()

    def handle_sysex(self, midi_bytes):
        if self._is_identity_response(midi_bytes):
            product_id_bytes = self._extract_product_id_bytes(midi_bytes)
            if product_id_bytes == self._product_id_bytes:
                self._request_task.kill()
                if self._identity_response_pending:
                    self.on_identified()
                    self._identity_response_pending = False
            else:
                self.log_message('MIDI device responded with wrong product id (%s != %s).' % (
                 str(self._product_id_bytes), str(product_id_bytes)))
        else:
            super(IdentifiableControlSurface, self).handle_sysex(midi_bytes)

    def _is_identity_response(self, midi_bytes):
        return midi_bytes[3:5] == (6, 2)

    def _extract_product_id_bytes(self, midi_bytes):
        return midi_bytes[5:5 + len(self._product_id_bytes)]

    def _send_identity_request(self):
        self._identity_response_pending = True
        self._send_midi(self.identity_request)