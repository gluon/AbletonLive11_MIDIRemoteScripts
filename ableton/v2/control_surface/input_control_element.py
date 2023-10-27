# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\input_control_element.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 19728 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import contextlib, logging
from ..base import Disconnectable, Event, Signal, const, depends, in_range, liveobj_valid, nop, task
from . import midi
from .control_element import NotifyingControlElement
logger = logging.getLogger(__name__)
MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
MIDI_PB_TYPE = 2
MIDI_SYSEX_TYPE = 3
MIDI_INVALID_TYPE = 4
MIDI_MSG_TYPES = (
 MIDI_NOTE_TYPE,
 MIDI_CC_TYPE,
 MIDI_PB_TYPE,
 MIDI_SYSEX_TYPE,
 MIDI_INVALID_TYPE)

class ScriptForwarding(int):
    pass


ScriptForwarding.none = ScriptForwarding(0)
ScriptForwarding.exclusive = ScriptForwarding(1)
ScriptForwarding.non_consuming = ScriptForwarding(2)

class ParameterSlot(Disconnectable):
    _parameter = None
    _control = None

    def __init__(self, parameter=None, control=None, *a, **k):
        (super(ParameterSlot, self).__init__)(*a, **k)
        self.parameter = parameter
        self.control = control

    @property
    def control(self):
        return self._control

    @control.setter
    def control(self, control):
        if control != self._control:
            self.soft_disconnect()
            self._control = control
            self.connect()

    @property
    def parameter(self):
        return self._parameter

    @parameter.setter
    def parameter(self, parameter):
        if parameter != self._parameter:
            self.soft_disconnect()
            self._parameter = parameter
            self.connect()

    def connect(self):
        if self._control is not None:
            if liveobj_valid(self._parameter):
                self._control.connect_to(self._parameter)

    def soft_disconnect(self):
        if self._control is not None:
            if liveobj_valid(self._parameter):
                self._control.release_parameter()

    def disconnect(self):
        self.parameter = None
        self.control = None
        super(ParameterSlot, self).disconnect()


class InputSignal(Signal):

    def __init__(self, sender=None, *a, **k):
        (super(InputSignal, self).__init__)(a, sender=sender, **k)
        self._input_control = sender

    @contextlib.contextmanager
    def _listeners_update(self):
        try:
            control = self._input_control
            old_count = self.count
            old_wants_forwarding = control.script_wants_forwarding()
            yield
        finally:
            diff_count = self.count - old_count
            control._input_signal_listener_count += diff_count
            if old_wants_forwarding != control.script_wants_forwarding():
                self._input_control._request_rebuild()

    def connect(self, *a, **k):
        with self._listeners_update():
            (super(InputSignal, self).connect)(*a, **k)

    def disconnect(self, *a, **k):
        with self._listeners_update():
            (super(InputSignal, self).disconnect)(*a, **k)

    def disconnect_all(self, *a, **k):
        with self._listeners_update():
            (super(InputSignal, self).disconnect_all)(*a, **k)


class InputControlElement(NotifyingControlElement):

    class ProxiedInterface(NotifyingControlElement.ProxiedInterface):
        send_value = nop
        receive_value = nop
        use_default_message = nop
        set_channel = nop
        message_channel = const(None)
        mapped_parameter = nop
        mapping_sensitivity = const(None)
        reset_state = nop

    __events__ = (
     Event(name='value', signal=InputSignal, override=True),)
    _input_signal_listener_count = 0
    num_delayed_messages = 1
    allow_receiving_chunks = False

    @depends(request_rebuild_midi_map=(const(nop)))
    def __init__(self, msg_type=None, channel=None, identifier=None, sysex_identifier=None, request_rebuild_midi_map=None, send_should_depend_on_forwarding=True, is_feedback_enabled=True, *a, **k):
        (super(InputControlElement, self).__init__)(*a, **k)
        self._send_depends_on_forwarding = send_should_depend_on_forwarding
        self._request_rebuild = request_rebuild_midi_map
        self._msg_type = msg_type
        self._msg_channel = channel
        self._msg_identifier = identifier
        self._msg_sysex_identifier = sysex_identifier
        self._original_channel = channel
        self._original_identifier = identifier
        self._needs_takeover = True
        self._is_mapped = True
        self._is_being_forwarded = True
        self._delayed_messages = []
        self._force_next_send = False
        self._mapping_feedback_delay = 0
        self._mapping_sensitivity = 1.0
        self._script_forwarding = ScriptForwarding.exclusive
        self._is_feedback_enabled = is_feedback_enabled
        self._send_delayed_messages_task = self._tasks.add(task.run(self._send_delayed_messages))
        self._send_delayed_messages_task.kill()
        self._parameter_to_map_to = None
        self._in_parameter_gesture = False
        self._last_sent_message = None
        self._report_input = False
        self._report_output = False
        self._max_value = pow(2, 14 if self.message_type() == MIDI_PB_TYPE else 7)

    @property
    def send_depends_on_forwarding(self):
        return self._send_depends_on_forwarding

    def message_type(self):
        return self._msg_type

    def message_channel(self):
        return self._msg_channel

    def original_channel(self):
        return self._original_channel

    def message_identifier(self):
        return self._msg_identifier

    def original_identifier(self):
        return self._original_identifier

    def message_sysex_identifier(self):
        return self._msg_sysex_identifier

    def message_map_mode(self):
        raise NotImplementedError

    def max_value(self):
        return self._max_value

    @property
    def mapping_sensitivity(self):
        return self._mapping_sensitivity

    @mapping_sensitivity.setter
    def mapping_sensitivity(self, sensitivity):
        self._mapping_sensitivity = sensitivity
        self._request_rebuild()

    @property
    def suppress_script_forwarding(self):
        return self._script_forwarding == ScriptForwarding.none

    @suppress_script_forwarding.setter
    def suppress_script_forwarding(self, value):
        self.script_forwarding = ScriptForwarding.none if value else ScriptForwarding.exclusive

    @property
    def script_forwarding(self):
        return self._script_forwarding

    @script_forwarding.setter
    def script_forwarding(self, value):
        if self._script_forwarding != value:
            self._script_forwarding = value
            self._request_rebuild()

    @property
    def is_feedback_enabled(self):
        return self._is_feedback_enabled

    def force_next_send(self):
        self._force_next_send = True

    def set_channel(self, channel):
        if self._msg_channel != channel:
            self._msg_channel = channel
            self._request_rebuild()

    def set_identifier(self, identifier):
        if self._msg_identifier != identifier:
            self._msg_identifier = identifier
            self._request_rebuild()

    def set_needs_takeover(self, needs_takeover):
        self._needs_takeover = needs_takeover

    def set_feedback_delay(self, delay):
        self._mapping_feedback_delay = delay

    def needs_takeover(self):
        return self._needs_takeover

    def use_default_message(self):
        if (
         self._msg_channel, self._msg_identifier) != (
         self._original_channel,
         self._original_identifier):
            self._msg_channel = self._original_channel
            self._msg_identifier = self._original_identifier
            self._request_rebuild()

    def _mapping_feedback_values(self):
        value_map = tuple()
        if self._mapping_feedback_delay != 0:
            if self._msg_type != MIDI_PB_TYPE:
                value_map = tuple(range(128))
            else:
                value_pairs = []
                for value in range(16384):
                    value_pairs.append((value >> 7 & 127, value & 127))

                value_map = tuple(value_pairs)
        return value_map

    def install_connections(self, install_translation, install_mapping, install_forwarding):
        self._send_delayed_messages_task.kill()
        self._is_mapped = False
        self._is_being_forwarded = False
        if self._msg_channel != self._original_channel or self._msg_identifier != self._original_identifier:
            install_translation(self._msg_type, self._original_identifier, self._original_channel, self._msg_identifier, self._msg_channel)
        if liveobj_valid(self._parameter_to_map_to):
            self._is_mapped = install_mapping(self, self._parameter_to_map_to, self._mapping_feedback_delay, self._mapping_feedback_values())
        if self.script_wants_forwarding():
            self._is_being_forwarded = install_forwarding(self, self.script_forwarding)
            if self._is_being_forwarded:
                if self.send_depends_on_forwarding:
                    self._send_delayed_messages_task.restart()

    def script_wants_forwarding(self):
        forwarding_should_be_installed = self._script_forwarding in (
         ScriptForwarding.exclusive,
         ScriptForwarding.non_consuming)
        return forwarding_should_be_installed and (self._input_signal_listener_count > 0) or (self._report_input)

    def begin_gesture(self):
        if self._parameter_to_map_to:
            if not self._in_parameter_gesture:
                self._in_parameter_gesture = True
                self._parameter_to_map_to.begin_gesture()

    def end_gesture(self):
        if self._parameter_to_map_to:
            if self._in_parameter_gesture:
                self._in_parameter_gesture = False
                self._parameter_to_map_to.end_gesture()

    def connect_to(self, parameter):
        if self._parameter_to_map_to != parameter:
            if not liveobj_valid(parameter):
                self.release_parameter()
            else:
                self._parameter_to_map_to = parameter
                self._request_rebuild()

    def release_parameter(self):
        if liveobj_valid(self._parameter_to_map_to):
            self.end_gesture()
            self._parameter_to_map_to = None
            self._request_rebuild()

    def mapped_parameter(self):
        return self._parameter_to_map_to

    def _status_byte(self, channel):
        status_byte = channel
        if self._msg_type == MIDI_NOTE_TYPE:
            status_byte += midi.NOTE_ON_STATUS
        else:
            if self._msg_type == MIDI_CC_TYPE:
                status_byte += midi.CC_STATUS
            else:
                if self._msg_type == MIDI_PB_TYPE:
                    status_byte += midi.PB_STATUS
                else:
                    raise NotImplementedError
        return status_byte

    def identifier_bytes(self):
        if self._msg_type == MIDI_PB_TYPE:
            return ((self._status_byte(self._msg_channel),),)
        if self._msg_type == MIDI_SYSEX_TYPE:
            return (self.message_sysex_identifier(),)
        if self._msg_type == MIDI_NOTE_TYPE:
            return (
             (
              self._status_byte(self._msg_channel), self.message_identifier()),
             (
              self._status_byte(self._msg_channel) - 16, self.message_identifier()))
        return (
         (
          self._status_byte(self._msg_channel), self.message_identifier()),)

    def _send_delayed_messages(self):
        self.clear_send_cache()
        for value, channel in self._delayed_messages:
            self._do_send_value(value, channel=channel)

        self._delayed_messages[:] = []

    def send_value(self, value, force=False, channel=None):
        value = int(value)
        self._verify_value(value)
        if force or self._force_next_send:
            self._do_send_value(value, channel)
        else:
            if not self.send_depends_on_forwarding or self._is_being_forwarded and self._send_delayed_messages_task.is_running:
                first = 1 - self.num_delayed_messages
                self._delayed_messages = self._delayed_messages[first:] + [(value, channel)]
            else:
                if (
                 value, channel) != self._last_sent_message:
                    self._do_send_value(value, channel)
        self._force_next_send = False

    def _do_send_value(self, value, channel=None):
        data_byte1 = self._original_identifier
        data_byte2 = value
        status_byte = self._status_byte(self._original_channel if channel is None else channel)
        if self._msg_type == MIDI_PB_TYPE:
            data_byte1 = value & 127
            data_byte2 = value >> 7 & 127
        if self.send_midi((status_byte, data_byte1, data_byte2)):
            self._last_sent_message = (
             value, channel)
            if self._report_output:
                is_input = True
                self._report_value(value, not is_input)

    def clear_send_cache(self):
        self._last_sent_message = None

    def reset(self):
        self.send_value(0)

    def reset_state(self):
        self.use_default_message()
        self.script_forwarding = ScriptForwarding.exclusive
        self.release_parameter()

    def receive_value(self, value):
        value = getattr(value, 'midi_value', value)
        self._verify_value(value)
        self._last_sent_message = None
        self.notify_value(value)
        if self._report_input:
            is_input = True
            self._report_value(value, is_input)

    def receive_chunk(self, chunk):
        for value in chunk:
            self.receive_value(value)

    def set_report_values(self, report_input, report_output):
        self._report_input = report_input
        self._report_output = report_output

    def _verify_value(self, value):
        if self._msg_type < MIDI_SYSEX_TYPE:
            pass

    def _report_value(self, value, is_input):
        self._verify_value(value)
        message = '('
        if self._msg_type == MIDI_NOTE_TYPE:
            message += 'Note ' + str(self._msg_identifier) + ', '
        else:
            if self._msg_type == MIDI_CC_TYPE:
                message += 'CC ' + str(self._msg_identifier) + ', '
            else:
                message += 'PB '
        message += 'Chan. ' + str(self._msg_channel)
        message += ') '
        message += 'received value ' if is_input else 'sent value '
        message += str(value)
        logger.debug(message)

    @property
    def _last_sent_value(self):
        if self._last_sent_message:
            return self._last_sent_message[0]
        return -1