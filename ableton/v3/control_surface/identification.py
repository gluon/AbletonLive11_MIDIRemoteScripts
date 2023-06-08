<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/identification.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 7637 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
import logging
from abc import ABC, abstractmethod
from ..base import depends, listenable_property, nop, task
from . import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, Component, InputControlElement, midi
from .controls import InputControl
from .elements import SysexElement
logger = logging.getLogger(__name__)
NON_REALTIME_HEADER = (
 midi.SYSEX_START, midi.SYSEX_NON_REALTIME)
STANDARD_RESPONSE_BYTES = (midi.SYSEX_GENERAL_INFO, midi.SYSEX_IDENTITY_RESPONSE_ID)
PRODUCT_ID_BYTES_START_INDEX = 3

def status_byte_to_msg_type(status_byte):
    status_byte = 240 & status_byte
    msg_type = MIDI_CC_TYPE
    if status_byte == midi.NOTE_ON_STATUS:
        msg_type = MIDI_NOTE_TYPE
<<<<<<< HEAD
    else:
        if status_byte == midi.PB_STATUS:
            msg_type = MIDI_PB_TYPE
    return msg_type


=======
    elif status_byte == midi.PB_STATUS:
        msg_type = MIDI_PB_TYPE
    return msg_type


def is_standard_identity_response(midi_bytes):
    return midi_bytes[1:PRODUCT_ID_BYTES_START_INDEX] == STANDARD_RESPONSE_BYTES


>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
def create_responder(identity_response_id_bytes, custom_identity_response):
    if identity_response_id_bytes is not None:
        return StandardResponder(identity_response_id_bytes)
    if custom_identity_response[0] == midi.SYSEX_START:
        return CustomSysexResponder(custom_identity_response)
    return PlainMidiResponder(custom_identity_response)


class Responder(ABC):

    def __init__(self, response_bytes, *a, **k):
        (super().__init__)(*a, **k)
        self._response_bytes = tuple(response_bytes)

    @abstractmethod
    def create_response_element(self):
        pass

    @abstractmethod
    def is_valid_response(self, response_bytes):
        pass


class CustomSysexResponder(Responder):

    def create_response_element(self):
        return SysexElement(sysex_identifier=(self._response_bytes))

    def is_valid_response(self, _):
        return True


class PlainMidiResponder(Responder):

    def __init__(self, response_bytes, *a, **k):
        (super().__init__)(response_bytes, *a, **k)
        self._expected_response_value_bytes = midi.extract_value(response_bytes)

    def create_response_element(self):
        first_byte = self._response_bytes[0]
        element = InputControlElement(msg_type=(status_byte_to_msg_type(first_byte)),
          channel=(15 & first_byte),
          identifier=(self._response_bytes[1]))
        element.reset = nop
        return element

    def is_valid_response(self, response_bytes):
        return self._expected_response_value_bytes == response_bytes


class StandardResponder(Responder):

    def create_response_element(self):
        return SysexElement(sysex_identifier=NON_REALTIME_HEADER)

    def is_valid_response(self, response_bytes):
<<<<<<< HEAD
        if response_bytes[1:PRODUCT_ID_BYTES_START_INDEX] == STANDARD_RESPONSE_BYTES:
=======
        if is_standard_identity_response(response_bytes):
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
            product_id_bytes = self._extract_product_id_bytes(response_bytes)
            if product_id_bytes != self._response_bytes:
                raise IdentityResponseError(expected_bytes=(self._response_bytes),
                  actual_bytes=product_id_bytes)
            return True
        return False

    def _extract_product_id_bytes(self, midi_bytes):
        return midi_bytes[PRODUCT_ID_BYTES_START_INDEX:PRODUCT_ID_BYTES_START_INDEX + len(self._response_bytes)]


class IdentityResponseError(Exception):

    def __init__(self, expected_bytes=None, actual_bytes=None):
<<<<<<< HEAD
        super().__init__('Hardware controller responded with wrong identity bytes: ({} != {}).'.format(expected_bytes, actual_bytes))
=======
        super().__init__('MIDI device responded with wrong identity bytes: ({} != {}).'.format(expected_bytes, actual_bytes))
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34


class IdentificationComponent(Component):
    identity_response_control = InputControl()
    is_identified = listenable_property.managed(False)
    received_response_bytes = listenable_property.managed(None)

    @depends(send_midi=None)
    def __init__(self, name='Identification', identity_request=midi.SYSEX_IDENTITY_REQUEST_MESSAGE, identity_request_delay=0.0, identity_response_id_bytes=None, custom_identity_response=None, send_midi=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._send_midi = send_midi
        self._identity_request = identity_request
        self._responder = create_responder(identity_response_id_bytes, custom_identity_response)
        response_element = self._responder.create_response_element()
        response_element.name = 'identity_control'
<<<<<<< HEAD
        response_element.is_private = True
=======
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        self.identity_response_control.set_control_element(response_element)
        self._request_task = self._tasks.add(task.sequence(task.run(self._send_identity_request), task.wait(identity_request_delay), task.run(self._send_identity_request)))
        self._request_task.kill()

    @identity_response_control.value
    def identity_response_control(self, response_bytes, _):
        try:
            if self._responder.is_valid_response(response_bytes):
                self._request_task.kill()
                self.identity_response_control.enabled = False
                self.received_response_bytes = response_bytes
                self.is_identified = True
        except IdentityResponseError as e:
            try:
                logger.error(e)
            finally:
                e = None
                del e

    def request_identity(self):
        self._request_task.restart()
        self.received_response_bytes = None
        self.is_identified = False

    def _send_identity_request(self):
        self.identity_response_control.enabled = True
        self._send_midi(self._identity_request)