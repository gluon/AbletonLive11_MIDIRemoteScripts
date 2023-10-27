# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\handshake_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 7319 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from functools import partial
import Live
from ableton.v2.base import NamedTuple, listens, task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.elements import ToggleElement
from .firmware_handling import get_version_number_from_string
HANDSHAKE_TIMEOUT = 10.0
DONGLE_DELAY = 0.2
DONGLE_SIZE = 16

def to_bytes(dongle):
    return tuple([dongle >> 4 * (7 - index) & 15 for index in range(8)])


def to_integral(dongle):
    length = len(dongle)
    return sum([int(dongle[index] & 15) << 4 * (length - 1 - index) for index in range(length)])


def make_dongle_message(dongle_prefix, random_generator=Live.Application):
    dongle_one = random_generator.get_random_int(0, 2000000)
    dongle_two = random_generator.get_random_int(2000001, 4000000)
    return (
     dongle_prefix + (0, DONGLE_SIZE) + to_bytes(dongle_one) + to_bytes(dongle_two) + (247, ),
     (
      dongle_one, dongle_two))


class HardwareIdentity(NamedTuple):
    firmware = None
    serial = None
    manufacturing = None

    @property
    def major_version(self):
        return self.firmware[0] * 10 + self.firmware[1]

    @property
    def minor_version(self):
        return self.firmware[2] * 10 + self.firmware[3]


class HandshakeComponent(Component):
    __events__ = ('success', 'failure')
    encryptor = partial((Live.Application.encrypt_challenge), key_index=1)
    _handshake_succeeded = None
    _hardware_identity = None

    def __init__(self, identity_control=None, presentation_control=None, dongle_control=None, dongle=(0, 0), *a, **k):
        (super(HandshakeComponent, self).__init__)(*a, **k)
        self._identity_control = identity_control
        self._presentation_control = presentation_control
        self._dongle_one, self._dongle_two = dongle
        self._on_identity_value.subject = identity_control
        self._on_dongle_value.subject = dongle_control
        self._delay_dongle_task = self._tasks.add(task.sequence(task.wait(DONGLE_DELAY), task.run(dongle_control.enquire_value)))
        self._delay_dongle_task.kill()
        self._identification_timeout_task = self._tasks.add(task.sequence(task.wait(HANDSHAKE_TIMEOUT), task.run(self._do_fail)))
        self._identification_timeout_task.kill()

    @property
    def handshake_succeeded(self):
        return self._handshake_succeeded

    @property
    def hardware_identity(self):
        return self._hardware_identity

    @property
    def firmware_version(self):
        version_bytes = self._hardware_identity.firmware if self._hardware_identity != None else (0,
                                                                                                  0,
                                                                                                  0,
                                                                                                  0)
        return get_version_number_from_string(' %d %d %d %d' % version_bytes)

    def has_version_requirements(self, major_version, minor_version):
        if self._hardware_identity is None:
            return False
        return (self._hardware_identity.major_version > major_version) or ((self._hardware_identity.major_version == major_version) and (self._hardware_identity.minor_version >= minor_version))

    def on_enabled_changed(self):
        super(HandshakeComponent, self).on_enabled_changed()
        if self._handshake_succeeded == None:
            self._do_fail()

    def _start_handshake(self):
        self._handshake_succeeded = None
        self._identification_timeout_task.restart()
        self._identity_control.enquire_value()

    @listens('value')
    def _on_identity_value(self, value):
        if len(value) == 25:
            if value[9:] == tuple(range(1, 17)):
                self._do_fail(bootloader_mode=True)
            else:
                self._hardware_identity = HardwareIdentity(firmware=(value[:4]),
                  serial=(value[4:8]),
                  manufacturing=(value[8:25]))
                self._presentation_control.enquire_value()
                self._delay_dongle_task.restart()
        else:
            self._do_fail()

    @listens('value')
    def _on_dongle_value(self, value):
        success = False
        if len(value) >= 18:
            result = (
             to_integral(value[2:10]), to_integral(value[10:18]))
            expected = self.encryptor(self._dongle_one, self._dongle_two)
            success = tuple(expected) == tuple(result)
        if success:
            self._do_succeed()
        else:
            self._do_fail()

    def _do_succeed(self):
        if self._handshake_succeeded == None:
            self._handshake_succeeded = True
            self._delay_dongle_task.kill()
            self._identification_timeout_task.kill()
            self.notify_success()

    def _do_fail(self, bootloader_mode=False):
        if self._handshake_succeeded == None:
            self._handshake_succeeded = False
            self._delay_dongle_task.kill()
            self._identification_timeout_task.kill()
            self.notify_failure(bootloader_mode)


class MinimumFirmwareVersionElement(ToggleElement):

    def __init__(self, major_version=0, minor_version=0, wrapped_element=None, handshake_component=None, *a, **k):
        (super(MinimumFirmwareVersionElement, self).__init__)(a, on_control=wrapped_element, off_control=None, wrapped_control=wrapped_element, **k)
        self._major_version = major_version
        self._minor_version = minor_version
        self._handshake_component = handshake_component
        self._on_handshake_success.subject = handshake_component
        self._on_handshake_failure.subject = handshake_component

    @listens('success')
    def _on_handshake_success(self):
        self.set_toggled(self._handshake_component.has_version_requirements(self._major_version, self._minor_version))

    @listens('failure')
    def _on_handshake_failure(self, _):
        self.set_toggled(False)