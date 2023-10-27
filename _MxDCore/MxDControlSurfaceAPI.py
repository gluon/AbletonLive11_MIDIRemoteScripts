# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MxDCore\MxDControlSurfaceAPI.py
# Compiled at: 2023-07-07 03:08:57
# Size of source mod 2**32: 7513 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map, object, str
from future.utils import string_types
from collections import namedtuple
from ableton.v2.base import old_hasattr
from _MxDCore.ControlSurfaceWrapper import WrapperRegistry
from _MxDCore.LomTypes import get_control_surfaces, is_control_surface
RECEIVE_MIDI_TIMEOUT = 0.2

def midi_byte_to_int(byte):
    if isinstance(byte, string_types):
        return int(byte, 0)
    return byte


def midi_bytes_are_sysex(bytes):
    return len(bytes) > 3 and bytes[0] == 240 and bytes[-1] == 247


def check_has_mxd_midi_scheduler(lom_object, shown_name):
    if not old_hasattr(lom_object, 'mxd_midi_scheduler'):
        raise AttributeError("object '{}' has no attribute '{}'".format(type(lom_object).__name__, shown_name))


class MxDControlSurfaceAPI(object):

    def __init__(self, mxdcore, *a, **k):
        (super(MxDControlSurfaceAPI, self).__init__)(*a, **k)
        self._mxdcore = mxdcore
        self._wrapper_registry = WrapperRegistry()

    @property
    def wrapper_registry(self):
        return self._wrapper_registry

    class MxDMidiOwner(namedtuple('Owner', 'device_id object_id mxdcore')):

        def send_reply(self, selector, message):
            message_str = self.mxdcore.str_representation_for_object(message)
            selector_str = {
              'send_receive': 'send_receive_sysex',
              'grab': 'grab_midi',
              'release': 'release_midi',
              'received': 'received_midi'}.get(selector, str(selector))
            try:
                self.mxdcore.manager.send_message(self.device_id, self.object_id, 'obj_output', '"' + selector_str + '"  ' + message_str)
            except:
                pass

        def report_error(self, message):
            self.mxdcore._print_error(self.device_id, self.object_id, message)

        def is_expected_reply(self, message):
            return midi_bytes_are_sysex(message)

    def object_send_midi(self, device_id, object_id, lom_object, parameters):
        check_has_mxd_midi_scheduler(lom_object, 'send_midi')
        midi_message = tuple(map(midi_byte_to_int, parameters[1:]))
        lom_object.mxd_midi_scheduler.send(self.MxDMidiOwner(device_id, object_id, self._mxdcore), midi_message)

    def object_send_receive_sysex(self, device_id, object_id, lom_object, parameters):
        check_has_mxd_midi_scheduler(lom_object, 'send_receive_sysex')
        owner = self.MxDMidiOwner(device_id, object_id, self._mxdcore)
        has_timeout = len(parameters) > 2 and parameters[-2] == 'timeout'
        timeout = parameters[-1] if has_timeout else RECEIVE_MIDI_TIMEOUT
        midi_parameters = parameters[1:-2] if has_timeout else parameters[1:]
        midi_message = tuple(map(midi_byte_to_int, midi_parameters))
        if midi_bytes_are_sysex(midi_message):
            lom_object.mxd_midi_scheduler.send_receive(owner, midi_message, timeout)
        else:
            self._mxdcore._print_error(device_id, object_id, 'non-sysex passed to send_receive_sysex')

    def object_grab_midi(self, device_id, object_id, lom_object, parameters):
        check_has_mxd_midi_scheduler(lom_object, 'grab_midi')
        lom_object.mxd_midi_scheduler.grab(self.MxDMidiOwner(device_id, object_id, self._mxdcore))

    def object_release_midi(self, device_id, object_id, lom_object, parameters):
        check_has_mxd_midi_scheduler(lom_object, 'release_midi')
        lom_object.mxd_midi_scheduler.release(self.MxDMidiOwner(device_id, object_id, self._mxdcore))

    def release_control_surface_midi(self, device_id, object_id):
        for control_surface in map(self._wrapper_registry.wrap, get_control_surfaces()):
            if old_hasattr(control_surface, 'mxd_midi_scheduler'):
                control_surface.mxd_midi_scheduler.disconnect(self.MxDMidiOwner(device_id, object_id, self._mxdcore))

    def object_get_control_names(self, device_id, object_id, lom_object, parameters):
        if not is_control_surface(lom_object):
            raise AttributeError("object '{}' has no attribute get_control_names".format(type(lom_object).__name__))
        control_names = lom_object.control_names
        result = 'control_names %d\n' % len(control_names) + ''.join(['control {}\n'.format(name) for name in control_names]) + 'done'
        self._mxdcore.manager.send_message(device_id, object_id, 'obj_call_result', result)

    def object_get_control(self, device_id, object_id, lom_object, parameters):
        if not is_control_surface(lom_object):
            raise AttributeError("object '{}' has no attribute get_control".format(type(lom_object).__name__))
        cs = lom_object
        name = parameters[1]
        control = cs.get_control_by_name(name)
        result_str = self._mxdcore.str_representation_for_object(control)
        self._mxdcore.manager.send_message(device_id, object_id, 'obj_call_result', result_str)

    def _get_control_or_raise(self, cs, control_or_name, command):
        if not is_control_surface(cs):
            raise AttributeError("object '{}' has no attribute {}".format(type(cs).__name__, command))
        if not control_or_name:
            raise AttributeError('control id or name required for {}'.format(command))
        if isinstance(control_or_name, string_types):
            control = cs.get_control_by_name(control_or_name)
            assert control, "{} is not a control of '{}'".format(control_or_name, type(cs).__name__)
        else:
            control = control_or_name
            if not cs.has_control(control):
                id_str = self._mxdcore.str_representation_for_object(control)
                raise AttributeError("'{}' ({}) is not a control of '{}'".format(type(control).__name__, id_str, type(cs).__name__))
        return control

    def object_grab_control(self, device_id, object_id, lom_object, parameters):
        cs = lom_object
        control_or_name = parameters[1]
        control = self._get_control_or_raise(cs, control_or_name, 'grab_control')
        cs.grab_control(control)

    def object_release_control(self, device_id, object_id, lom_object, parameters):
        cs = lom_object
        control_or_name = parameters[1]
        control = self._get_control_or_raise(cs, control_or_name, 'release_control')
        cs.release_control(control)