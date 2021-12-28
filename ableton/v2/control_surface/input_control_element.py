#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/input_control_element.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import contextlib
import logging
from ..base import const, depends, Disconnectable, in_range, nop, Signal, Event, task
from . import midi
from .control_element import NotifyingControlElement
logger = logging.getLogger(__name__)
MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
MIDI_PB_TYPE = 2
MIDI_SYSEX_TYPE = 3
MIDI_INVALID_TYPE = 4
MIDI_MSG_TYPES = (MIDI_NOTE_TYPE,
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
    u"""
    Maintains the connection between a parameter and
    InputControlElement. Keeps the invariant that whenever both
    parameter and control are set, the parameter is connected to the
    control.  Whenever any of them is changed, they are disconnected
    and reconnected to the new one, in a similar fashion to a
    Slot.
    """
    _parameter = None
    _control = None

    def __init__(self, parameter = None, control = None, *a, **k):
        super(ParameterSlot, self).__init__(*a, **k)
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
        if self._control != None and self._parameter != None:
            self._control.connect_to(self._parameter)

    def soft_disconnect(self):
        if self._control != None and self._parameter != None:
            self._control.release_parameter()

    def disconnect(self):
        self.parameter = None
        self.control = None
        super(ParameterSlot, self).disconnect()


class InputSignal(Signal):
    u"""
    Special signal type that makes sure that interaction with input
    works properly. Special input control elements that define
    value-dependent properties should use this kind of signal.
    """

    def __init__(self, sender = None, *a, **k):
        super(InputSignal, self).__init__(sender=sender, *a, **k)
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
            super(InputSignal, self).connect(*a, **k)

    def disconnect(self, *a, **k):
        with self._listeners_update():
            super(InputSignal, self).disconnect(*a, **k)

    def disconnect_all(self, *a, **k):
        with self._listeners_update():
            super(InputSignal, self).disconnect_all(*a, **k)


class InputControlElement(NotifyingControlElement):
    u"""
    Base class for all classes representing control elements on a controller
    """

    class ProxiedInterface(NotifyingControlElement.ProxiedInterface):
        send_value = nop
        receive_value = nop
        use_default_message = nop
        set_channel = nop
        message_channel = const(None)
        mapped_parameter = nop
        mapping_sensitivity = const(None)
        reset_state = nop

    __events__ = (Event(name=u'value', signal=InputSignal, override=True),)
    _input_signal_listener_count = 0
    num_delayed_messages = 1
    allow_receiving_chunks = False

    @depends(request_rebuild_midi_map=const(nop))
    def __init__(self, msg_type = None, channel = None, identifier = None, sysex_identifier = None, request_rebuild_midi_map = None, send_should_depend_on_forwarding = True, *a, **k):
        assert msg_type in MIDI_MSG_TYPES
        assert midi.is_valid_channel(channel) or channel is None
        assert midi.is_valid_identifier(identifier) or identifier is None
        assert msg_type != MIDI_SYSEX_TYPE or channel is None
        assert msg_type != MIDI_SYSEX_TYPE or identifier is None
        assert msg_type == MIDI_SYSEX_TYPE or sysex_identifier is None
        super(InputControlElement, self).__init__(*a, **k)
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
        self._send_delayed_messages_task = self._tasks.add(task.run(self._send_delayed_messages))
        self._send_delayed_messages_task.kill()
        self._parameter_to_map_to = None
        self._in_parameter_gesture = False
        self._last_sent_message = None
        self._report_input = False
        self._report_output = False

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
        assert isinstance(value, ScriptForwarding)
        if self._script_forwarding != value:
            self._script_forwarding = value
            self._request_rebuild()

    def force_next_send(self):
        u"""
        Enforces sending the next value regardless of whether the
        control is mapped to the script.
        """
        self._force_next_send = True

    def set_channel(self, channel):
        assert self._msg_type != MIDI_SYSEX_TYPE
        assert midi.is_valid_channel(channel) or channel is None
        if self._msg_channel != channel:
            self._msg_channel = channel
            self._request_rebuild()

    def set_identifier(self, identifier):
        assert self._msg_type != MIDI_SYSEX_TYPE
        assert midi.is_valid_identifier(identifier) or identifier is None
        if self._msg_identifier != identifier:
            self._msg_identifier = identifier
            self._request_rebuild()

    def set_needs_takeover(self, needs_takeover):
        assert self.message_type() != MIDI_NOTE_TYPE
        self._needs_takeover = needs_takeover

    def set_feedback_delay(self, delay):
        assert delay >= -1
        self._mapping_feedback_delay = delay

    def needs_takeover(self):
        assert self.message_type() != MIDI_NOTE_TYPE
        return self._needs_takeover

    def use_default_message(self):
        if (self._msg_channel, self._msg_identifier) != (self._original_channel, self._original_identifier):
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
        if self._parameter_to_map_to != None:
            self._is_mapped = install_mapping(self, self._parameter_to_map_to, self._mapping_feedback_delay, self._mapping_feedback_values())
        if self.script_wants_forwarding():
            self._is_being_forwarded = install_forwarding(self, self.script_forwarding)
            if self._is_being_forwarded and self.send_depends_on_forwarding:
                self._send_delayed_messages_task.restart()

    def script_wants_forwarding(self):
        u"""
        Returns whether the script wants to receive the values,
        otherwise, the control will be mapped to the track.
        
        Subclasses that overload this should _request_rebuild()
        whenever the property changes.
        """
        forwarding_should_be_installed = self._script_forwarding in (ScriptForwarding.exclusive, ScriptForwarding.non_consuming)
        return forwarding_should_be_installed and self._input_signal_listener_count > 0 or self._report_input

    def begin_gesture(self):
        u"""
        Begins a modification on the input control element,
        meaning that we should consider the next flow of input data as
        a consistent gesture from the user.
        """
        if self._parameter_to_map_to and not self._in_parameter_gesture:
            self._in_parameter_gesture = True
            self._parameter_to_map_to.begin_gesture()

    def end_gesture(self):
        u"""
        Ends a modification of the input control element. See
        begin_gesture.
        """
        if self._parameter_to_map_to and self._in_parameter_gesture:
            self._in_parameter_gesture = False
            self._parameter_to_map_to.end_gesture()

    def connect_to(self, parameter):
        u""" parameter is a Live.Device.DeviceParameter """
        if self._parameter_to_map_to != parameter:
            if parameter == None:
                self.release_parameter()
            else:
                self._parameter_to_map_to = parameter
                self._request_rebuild()

    def release_parameter(self):
        if self._parameter_to_map_to != None:
            self.end_gesture()
            self._parameter_to_map_to = None
            self._request_rebuild()

    def mapped_parameter(self):
        return self._parameter_to_map_to

    def _status_byte(self, channel):
        status_byte = channel
        if self._msg_type == MIDI_NOTE_TYPE:
            status_byte += midi.NOTE_ON_STATUS
        elif self._msg_type == MIDI_CC_TYPE:
            status_byte += midi.CC_STATUS
        elif self._msg_type == MIDI_PB_TYPE:
            status_byte += midi.PB_STATUS
        else:
            raise NotImplementedError
        return status_byte

    def identifier_bytes(self):
        u"""
        Returns a list with all the MIDI message prefixes that
        identify this control element.
        """
        if self._msg_type == MIDI_PB_TYPE:
            return ((self._status_byte(self._msg_channel),),)
        elif self._msg_type == MIDI_SYSEX_TYPE:
            return (self.message_sysex_identifier(),)
        elif self._msg_type == MIDI_NOTE_TYPE:
            return ((self._status_byte(self._msg_channel), self.message_identifier()), (self._status_byte(self._msg_channel) - 16, self.message_identifier()))
        else:
            return ((self._status_byte(self._msg_channel), self.message_identifier()),)

    def _send_delayed_messages(self):
        self.clear_send_cache()
        for value, channel in self._delayed_messages:
            self._do_send_value(value, channel=channel)

        self._delayed_messages[:] = []

    def send_value(self, value, force = False, channel = None):
        value = int(value)
        self._verify_value(value)
        if force or self._force_next_send:
            self._do_send_value(value, channel)
        elif self.send_depends_on_forwarding and not self._is_being_forwarded or self._send_delayed_messages_task.is_running:
            first = 1 - self.num_delayed_messages
            self._delayed_messages = self._delayed_messages[first:] + [(value, channel)]
        elif (value, channel) != self._last_sent_message:
            self._do_send_value(value, channel)
        self._force_next_send = False

    def _do_send_value(self, value, channel = None):
        data_byte1 = self._original_identifier
        data_byte2 = value
        status_byte = self._status_byte(self._original_channel if channel is None else channel)
        if self._msg_type == MIDI_PB_TYPE:
            data_byte1 = value & 127
            data_byte2 = value >> 7 & 127
        if self.send_midi((status_byte, data_byte1, data_byte2)):
            self._last_sent_message = (value, channel)
            if self._report_output:
                is_input = True
                self._report_value(value, not is_input)

    def clear_send_cache(self):
        self._last_sent_message = None

    def reset(self):
        u""" Send 0 to reset motorized faders and turn off LEDs """
        self.send_value(0)

    def reset_state(self):
        self.use_default_message()
        self.script_forwarding = ScriptForwarding.exclusive
        self.release_parameter()

    def receive_value(self, value):
        value = getattr(value, u'midi_value', value)
        self._verify_value(value)
        self._last_sent_message = None
        self.notify_value(value)
        if self._report_input:
            is_input = True
            self._report_value(value, is_input)

    def receive_chunk(self, chunk):
        u"""
        Is called when a chunk of MIDI is received in a defined time interval.
        Chunks are only sent if allow_receiving_chunks is True. Otherwise receive_value
        is called for each MIDI message.
        """
        for value in chunk:
            self.receive_value(value)

    def set_report_values(self, report_input, report_output):
        u"""
        Set boolean values report_input and report_output enabling
        debug information.
        """
        self._report_input = report_input
        self._report_output = report_output

    def _verify_value(self, value):
        if self._msg_type < MIDI_SYSEX_TYPE:
            upper_bound = 16384 if self._msg_type == MIDI_PB_TYPE else 128
            assert in_range(value, 0, upper_bound)

    def _report_value(self, value, is_input):
        self._verify_value(value)
        message = u'('
        if self._msg_type == MIDI_NOTE_TYPE:
            message += u'Note ' + str(self._msg_identifier) + u', '
        elif self._msg_type == MIDI_CC_TYPE:
            message += u'CC ' + str(self._msg_identifier) + u', '
        else:
            message += u'PB '
        message += u'Chan. ' + str(self._msg_channel)
        message += u') '
        message += u'received value ' if is_input else u'sent value '
        message += str(value)
        logger.debug(message)

    @property
    def _last_sent_value(self):
        if self._last_sent_message:
            return self._last_sent_message[0]
        return -1
