#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/control_surface.py
from __future__ import absolute_import, print_function, unicode_literals
from future.utils import itervalues
import logging
import traceback
from builtins import filter
from builtins import map
from future.utils import iteritems, itervalues
from collections import OrderedDict
from contextlib import contextmanager
from functools import partial
from itertools import chain
from pickle import loads, dumps
import Live
from ..base import BooleanContext, EventObject, const, find_if, first, in_range, inject, lazy_attribute, liveobj_valid, old_hasattr, task
from . import defaults
from . import midi
from .control_element import OptimizedOwnershipHandler
from .device_bank_registry import DeviceBankRegistry
from .device_provider import DeviceProvider
from .elements import PhysicalDisplayElement
from .input_control_element import InputControlElement, MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, MIDI_SYSEX_TYPE, ScriptForwarding
from .message_scheduler import MessageScheduler
from .profile import profile
__all__ = (u'SimpleControlSurface', u'ControlSurface')
logger = logging.getLogger(__name__)
CS_LIST_KEY = u'control_surfaces'

def publish_control_surface(control_surface):
    get_control_surfaces().append(control_surface)


def get_control_surfaces():
    if isinstance(__builtins__, dict):
        if CS_LIST_KEY not in __builtins__.keys():
            __builtins__[CS_LIST_KEY] = []
        return __builtins__[CS_LIST_KEY]
    else:
        if not old_hasattr(__builtins__, CS_LIST_KEY):
            setattr(__builtins__, CS_LIST_KEY, [])
        return getattr(__builtins__, CS_LIST_KEY)


class SimpleControlSurface(EventObject):
    u"""
    Base class for connecting a hardware controller with Live. It gives access to
    the controller's MIDI input and output ports as well as Live's data model. Together
    it can be used to connect hardware controls with functionality in Live and give
    feedback through MIDI.
    
    This class does not support controlling devices. Use :class:`ControlSurface` if
    you need device support.
    """
    __events__ = (u'received_midi', u'disconnect')
    preferences_key = None

    def __init__(self, c_instance = None, publish_self = True, *a, **k):
        super(SimpleControlSurface, self).__init__(*a, **k)
        assert c_instance
        self.canonical_parent = None
        if publish_self:
            publish_control_surface(self)
        self._c_instance = c_instance
        self._pad_translations = None
        self._components = []
        self._displays = []
        self.controls = []
        self._forwarding_long_identifier_registry = {}
        self._forwarding_registry = {}
        self._is_sending_scheduled_messages = BooleanContext()
        self._remaining_scheduled_messages = []
        self._task_group = task.TaskGroup(auto_kill=False)
        self._in_build_midi_map = BooleanContext()
        self._suppress_requests_counter = 0
        self._rebuild_requests_during_suppression = 0
        self._enabled = True
        self._in_component_guard = BooleanContext()
        self._accumulate_midi_messages = BooleanContext()
        self._midi_message_dict = {}
        self._midi_message_list = []
        self._midi_message_count = 0
        self.mxd_midi_scheduler = MessageScheduler(self._do_send_midi, self._task_group.add(task.TimedCallbackTask()))
        self._ownership_handler = OptimizedOwnershipHandler()
        self._control_surface_injector = inject(element_ownership_handler=const(self._ownership_handler), parent_task_group=const(self._task_group), show_message=const(self.show_message), register_component=const(self._register_component), register_control=const(self._register_control), request_rebuild_midi_map=const(self.request_rebuild_midi_map), set_pad_translations=const(self.set_pad_translations), send_midi=const(self._send_midi), song=const(self.song), set_session_highlight=const(self._c_instance.set_session_highlight)).everywhere()

    @property
    def components(self):
        u"""
        Tuple of all components, that have been registered for this control surface.
        """
        return tuple(filter(lambda comp: not comp.is_private, self._components))

    @property
    def root_components(self):
        u"""
        Tuple of all root components, that have been registered for this control surface.
        """
        return tuple(filter(lambda comp: comp.is_root and not comp.is_private, self._components))

    def _get_tasks(self):
        return self._task_group

    _tasks = property(_get_tasks)

    @property
    def application(self):
        u""" Returns a reference to the application that we are running in """
        return Live.Application.get_application()

    @property
    def song(self):
        u""" Returns a reference to the Live song instance that we control """
        return self._c_instance.song()

    def disconnect(self):
        u"""
        Live -> Script
        
        Is called by Live when the script is unloaded. This happens when the script
        gets unselected from the preferences, automatically when the corresponding MIDI
        ports are gone or Live is shut down.
        
        All listeners to the Live API need to be removed. Cyclic dependencies should be
        broken, so the control surface can be garbage collected.
        """
        self._pre_serialize()
        self.notify_disconnect(self)
        self._disconnect_and_unregister_all_components()
        with self.component_guard():
            for control in self.controls:
                control.disconnect()
                control.canonical_parent = None

        self._forwarding_registry = None
        self.controls = None
        self._displays = None
        self._pad_translations = None
        cs_list = get_control_surfaces()
        if self in cs_list:
            cs_list.remove(self)
        self._task_group.clear()
        super(SimpleControlSurface, self).disconnect()

    def can_lock_to_devices(self):
        u"""
        Live -> Script
        
        Should return True, if the ControlSurface can lock a device.
        SimpleControlSurface does not support controlling devices, so it will always
        be False.
        """
        return False

    def suggest_map_mode(self, cc_no, channel):
        u"""
        Live -> Script
        
        Live can ask for a suitable mapping mode for a given CC
        """
        assert midi.is_valid_value(cc_no)
        assert midi.is_valid_channel(channel)
        suggested_map_mode = -1
        for control in self.controls:
            if isinstance(control, InputControlElement) and control.message_type() == MIDI_CC_TYPE and control.message_identifier() == cc_no and control.message_channel() == channel:
                suggested_map_mode = control.message_map_mode()
                break

        return suggested_map_mode

    def supports_pad_translation(self):
        u"""
        Returns True if pad translations have been installed using
        :meth:`set_pad_translations`.
        """
        return self._pad_translations is not None

    def show_message(self, message):
        u"""
        Displays the given message in Live's status bar.
        """
        assert isinstance(message, (str, unicode))
        self._c_instance.show_message(message)

    def connect_script_instances(self, instanciated_scripts):
        u"""
        Script -> Live
        
        Called by the Application as soon as all scripts are initialized.
        You can connect yourself to other running scripts here.
        """
        pass

    def request_rebuild_midi_map(self):
        u"""
        Script -> Live.
        
        When the internal MIDI controller has changed in a way that
        you need to rebuild the MIDI mappings, request a rebuild
        by calling this function. This is processed as a request,
        to be sure that it's not too often called, because it's
        time-critical.
        """
        assert not self._in_build_midi_map
        if self._suppress_requests_counter > 0:
            self._rebuild_requests_during_suppression += 1
        else:
            self._c_instance.request_rebuild_midi_map()

    def build_midi_map(self, midi_map_handle):
        u"""
        Live -> Script
        
        Build DeviceParameter Mappings, that are processed in Audio time, or
        forward MIDI messages explicitly to our receive_midi_functions.
        Which means that when you are not forwarding MIDI, nor mapping parameters,
        you will never get any MIDI messages at all.
        """
        with self._in_build_midi_map():
            self._forwarding_registry.clear()
            self._forwarding_long_identifier_registry.clear()
            for control in self.controls:
                if isinstance(control, InputControlElement):
                    control.install_connections(self._translate_message, partial(self._install_mapping, midi_map_handle), partial(self._install_forwarding, midi_map_handle))

            if self._pad_translations is not None:
                self._c_instance.set_pad_translation(self._pad_translations)

    def port_settings_changed(self):
        u"""
        Live -> Script
        
        Is called when either the user changes the MIDI ports that are assigned
        to the script, or the port states change due to unplugging/replugging the
        device.
        
        Will always be called initially when setting up the script.
        """
        self.refresh_state()

    def refresh_state(self):
        u"""
        Live -> Script
        
        Send out MIDI to completely update the attached MIDI controller.
        Will be called when exiting MIDI map mode
        """
        self.update()

    def update(self):
        with self.component_guard():
            for control in self.controls:
                control.clear_send_cache()

            for component in self._components:
                component.update()

    @profile
    def update_display(self):
        u"""
        Live -> Script
        
        Aka on_timer. Called every 100 ms and should be used to update display
        relevant parts of the controller
        """
        with self.component_guard():
            self.update_display_hook()
            with self._is_sending_scheduled_messages():
                self._task_group.update(defaults.TIMER_DELAY)

    def update_display_hook(self):
        u"""
        Override this method if there is something that should be updated at the
        same rate of update_display.
        """
        pass

    @profile
    def receive_midi(self, midi_bytes):
        u"""
        Live -> Script
        
        MIDI messages are only received through this function, when explicitly
        forwarded in 'build_midi_map'.
        """
        with self.component_guard():
            self._do_receive_midi(midi_bytes)

    @profile
    def receive_midi_chunk(self, midi_chunk):
        u"""
        Live -> Script
        
        MIDI messages are only received through this function, when explicitly
        forwarded in 'build_midi_map'.
        """
        with self.component_guard():
            self._do_receive_midi_chunk(midi_chunk)

    @staticmethod
    def _receive_midi_data(recipient, data):
        recipient.receive_value(data)

    def _do_receive_midi(self, midi_bytes):
        self.notify_received_midi(*midi_bytes)
        self.mxd_midi_scheduler.handle_message(midi_bytes)
        self.process_midi_bytes(midi_bytes, self._receive_midi_data)

    @staticmethod
    def _merge_midi_data(recipient, data, midi_data):
        if recipient.allow_receiving_chunks:
            _, values = midi_data.setdefault(recipient, (recipient, []))
            values.append(data)
        else:
            midi_data[object()] = (recipient, data)

    def _do_receive_midi_chunk(self, midi_chunk):
        u"""
        The rules for receiving MIDI in chunks are as following:
         - If the recipient has the property allow_receiving_chunks set to True, it
           will receive MIDI in chunks.
         - The order in which MIDI is received is tried to be preserved among recipients
           and is guaranteed for the messages of a recipient.
        
        Example:
            r1.m1, r2.m1, r1.m2, r2.m2, r3.m1, where r1.m1 is the first message and all
            recipients allow receiving MIDI in chunks.
            This would lead to an ordered chunk: [r1.m1, r1.m2], [r2.m1, r2.m2], [r3.m1]
        """
        midi_data_for_recipient = OrderedDict()
        for midi_bytes in midi_chunk:
            self.notify_received_midi(*midi_bytes)
            self.mxd_midi_scheduler.handle_message(midi_bytes)
            self.process_midi_bytes(midi_bytes, partial(self._merge_midi_data, midi_data=midi_data_for_recipient))

        for recipient, data in itervalues(midi_data_for_recipient):
            if recipient.allow_receiving_chunks:
                recipient.receive_chunk(tuple(data))
            else:
                recipient.receive_value(data)

    def process_midi_bytes(self, midi_bytes, midi_processor):
        u"""
        Finds the right recipient for the MIDI message and translates it into the
        expected format. The result is forwarded to the midi_processor.
        """
        if midi.is_sysex(midi_bytes):
            result = self.get_registry_entry_for_sysex_midi_message(midi_bytes)
            if result is not None:
                identifier, recipient = result
                midi_processor(recipient, midi_bytes[len(identifier):-1])
            elif self.received_midi_listener_count() == 0:
                logger.warning(u'Got unknown sysex message: ' + midi.pretty_print_bytes(midi_bytes))
        else:
            recipient = self.get_recipient_for_nonsysex_midi_message(midi_bytes)
            if recipient is not None:
                midi_processor(recipient, midi.extract_value(midi_bytes))
            elif self.received_midi_listener_count() == 0:
                logger.warning(u'Got unknown message: ' + midi.pretty_print_bytes(midi_bytes))

    def get_recipient_for_nonsysex_midi_message(self, midi_bytes):
        forwarding_key = midi_bytes[:1 if midi.is_pitchbend(midi_bytes) else 2]
        if forwarding_key in self._forwarding_registry:
            return self._forwarding_registry[forwarding_key]

    def get_registry_entry_for_sysex_midi_message(self, midi_bytes):
        return find_if(lambda identifier_recipient: midi_bytes[:len(identifier_recipient[0])] == identifier_recipient[0], iteritems(self._forwarding_long_identifier_registry))

    @contextmanager
    def suppressing_rebuild_requests(self):
        u"""
        Delays requesting a MIDI map rebuild, if any, until the scope
        of the context manager is exited.
        """
        try:
            self._set_suppress_rebuild_requests(True)
            yield
        finally:
            self._set_suppress_rebuild_requests(False)

    def _set_suppress_rebuild_requests(self, suppress_requests):
        assert not self._in_build_midi_map
        if suppress_requests:
            self._suppress_requests_counter += 1
        else:
            assert self._suppress_requests_counter > 0
            self._suppress_requests_counter -= 1
            if self._suppress_requests_counter == 0 and self._rebuild_requests_during_suppression > 0:
                self.request_rebuild_midi_map()
                self._rebuild_requests_during_suppression = 0

    def set_pad_translations(self, pad_translations):

        def check_translation(translation):
            assert len(translation) == 4
            assert in_range(translation[0], 0, 4)
            assert in_range(translation[1], 0, 4)
            assert in_range(translation[2], -1, 128)
            assert in_range(translation[3], -1, 16)
            return True

        assert pad_translations is None or all(map(check_translation, pad_translations)) and len(pad_translations) <= 16
        self._pad_translations = pad_translations

    def set_enabled(self, enable):
        bool_enable = bool(enable)
        if self._enabled != bool_enable:
            with self.component_guard():
                self._enabled = bool_enable
                root_components = self.root_components
                components = root_components if len(root_components) > 0 else self._components
                for component in components:
                    component._set_enabled_recursive(bool_enable)

    def schedule_message(self, delay_in_ticks, callback, parameter = None):
        u""" Schedule a callback to be called after a specified time """
        assert delay_in_ticks > 0
        assert callable(callback)
        if not self._is_sending_scheduled_messages:
            delay_in_ticks -= 1
        message_reference = [None]

        def message(delta):
            if parameter:
                callback(parameter)
            else:
                callback()
            self._remaining_scheduled_messages.remove(message_reference)

        message_reference[0] = message
        self._remaining_scheduled_messages.append(message_reference)
        if delay_in_ticks:
            self._task_group.add(task.sequence(task.delay(delay_in_ticks), message))
        else:
            self._task_group.add(message)

    def set_feedback_channels(self, channels):
        self._c_instance.set_feedback_channels(channels)

    def set_controlled_track(self, track):
        u""" Sets the track that will send its feedback to the control surface """
        assert liveobj_valid(track) or isinstance(track, Live.Track.Track)
        self._c_instance.set_controlled_track(track)

    def release_controlled_track(self):
        u""" Sets that no track will send its feedback to the control surface """
        self._c_instance.release_controlled_track()

    def _register_control(self, control):
        u""" puts control into the list of controls for triggering updates """
        assert control is not None
        assert control not in self.controls, u'Control registered twice'
        self.controls.append(control)
        control.canonical_parent = self
        if isinstance(control, PhysicalDisplayElement):
            self._displays.append(control)
        if old_hasattr(control, u'_is_resource_based'):
            control._is_resource_based = True

    def _register_component(self, component):
        u""" puts component into the list of controls for triggering updates """
        assert component is not None
        assert component not in self._components, u'Component registered twice'
        self._components.append(component)
        component.canonical_parent = self

    def _disconnect_and_unregister_all_components(self):
        with self.component_guard():
            for component in self._components:
                component.canonical_parent = None
                component.disconnect()

        self._components = []

    @contextmanager
    def component_guard(self):
        u"""
        Context manager that guards user code.  This prevents
        unnecessary updating and enables several optimizations.  Should
        be used to guard calls to components or control elements.
        """
        if not self._in_component_guard:
            with self._in_component_guard():
                with self._component_guard():
                    yield
        else:
            yield

    @contextmanager
    def _component_guard(self):
        with self._control_surface_injector:
            with self.suppressing_rebuild_requests():
                with self.accumulating_midi_messages():
                    yield
                    self._ownership_handler.commit_ownership_changes()

    @profile
    def call_listeners(self, listeners):
        with self.component_guard():
            for listener in filter(liveobj_valid, listeners):
                listener()

    @contextmanager
    def accumulating_midi_messages(self):
        with self._accumulate_midi_messages():
            try:
                yield
            finally:
                self._flush_midi_messages()

    def get_control_by_name(self, control_name):
        return find_if(lambda c: c.name == control_name, self.controls)

    def get_component_by_name(self, component_name):
        return find_if(lambda c: c.name == component_name, self.components)

    def _send_midi(self, midi_event_bytes, optimized = True):
        u"""
        Script -> Live
        Use this function to send MIDI events through Live to the
        _real_ MIDI devices that this script is assigned to.
        
        When optimized=True it is assumed that messages can be
        dropped -- only the last message within an update for a
        given (channel, key) has visible effects.
        """
        if self._accumulate_midi_messages:
            sysex_status_byte = 240
            entry = (self._midi_message_count, midi_event_bytes)
            if optimized and midi_event_bytes[0] != sysex_status_byte:
                key = (midi_event_bytes[0], midi_event_bytes[1])
                self._midi_message_dict[key] = entry
            else:
                self._midi_message_list.append(entry)
            self._midi_message_count += 1
        else:
            self._do_send_midi(midi_event_bytes)
        return True

    def _flush_midi_messages(self):
        assert self._accumulate_midi_messages
        sorted_messages = sorted(chain(self._midi_message_list, itervalues(self._midi_message_dict)), key=first)
        for _, message in sorted_messages:
            self._do_send_midi(message)

        self._midi_message_dict.clear()
        self._midi_message_list[:] = []
        self._midi_message_count = 0

    def _do_send_midi(self, midi_event_bytes):
        try:
            self._c_instance.send_midi(midi_event_bytes)
        except:
            logger.error(u'Error while sending midi message %s', str(midi_event_bytes))
            traceback.print_exc()
            return False

        return True

    def _install_mapping(self, midi_map_handle, control, parameter, feedback_delay, feedback_map):
        success = False
        feedback_rule = None
        if control.message_type() == MIDI_NOTE_TYPE:
            feedback_rule = Live.MidiMap.NoteFeedbackRule()
            feedback_rule.note_no = control.message_identifier()
            feedback_rule.vel_map = feedback_map
        elif control.message_type() == MIDI_CC_TYPE:
            feedback_rule = Live.MidiMap.CCFeedbackRule()
            feedback_rule.cc_no = control.message_identifier()
            feedback_rule.cc_value_map = feedback_map
        elif control.message_type() == MIDI_PB_TYPE:
            feedback_rule = Live.MidiMap.PitchBendFeedbackRule()
            feedback_rule.value_pair_map = feedback_map
        assert feedback_rule is not None
        feedback_rule.channel = control.message_channel()
        feedback_rule.delay_in_ms = feedback_delay
        if control.message_type() == MIDI_NOTE_TYPE:
            success = Live.MidiMap.map_midi_note_with_feedback_map(midi_map_handle, parameter, control.message_channel(), control.message_identifier(), feedback_rule)
        elif control.message_type() == MIDI_CC_TYPE:
            success = Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, parameter, control.message_channel(), control.message_identifier(), control.message_map_mode(), feedback_rule, not control.needs_takeover(), control.mapping_sensitivity)
        elif control.message_type() == MIDI_PB_TYPE:
            success = Live.MidiMap.map_midi_pitchbend_with_feedback_map(midi_map_handle, parameter, control.message_channel(), feedback_rule, not control.needs_takeover())
        if success:
            Live.MidiMap.send_feedback_for_parameter(midi_map_handle, parameter)
        return success

    def _install_forwarding(self, midi_map_handle, control, forwarding_type = ScriptForwarding.exclusive):
        assert self._in_build_midi_map
        assert control is not None
        assert isinstance(control, InputControlElement)
        assert isinstance(forwarding_type, ScriptForwarding)
        success = False
        should_consume_event = forwarding_type == ScriptForwarding.exclusive
        if control.message_type() == MIDI_NOTE_TYPE:
            success = Live.MidiMap.forward_midi_note(self._c_instance.handle(), midi_map_handle, control.message_channel(), control.message_identifier(), should_consume_event)
        elif control.message_type() == MIDI_CC_TYPE:
            success = Live.MidiMap.forward_midi_cc(self._c_instance.handle(), midi_map_handle, control.message_channel(), control.message_identifier(), should_consume_event)
        elif control.message_type() == MIDI_PB_TYPE:
            success = Live.MidiMap.forward_midi_pitchbend(self._c_instance.handle(), midi_map_handle, control.message_channel())
        else:
            assert control.message_type() == MIDI_SYSEX_TYPE
            success = True
        if success:
            forwarding_keys = control.identifier_bytes()
            for key in forwarding_keys:
                registry = self._forwarding_registry if control.message_type() != MIDI_SYSEX_TYPE else self._forwarding_long_identifier_registry
                assert key not in registry.keys(), u'Registry key %s registered twice. Check Midi messages!' % str(key)
                registry[key] = control

        return success

    def _translate_message(self, type, from_identifier, from_channel, to_identifier, to_channel):
        assert type in (MIDI_CC_TYPE, MIDI_NOTE_TYPE)
        assert midi.is_valid_identifier(from_identifier)
        assert midi.is_valid_channel(from_channel)
        assert midi.is_valid_identifier(to_identifier)
        assert midi.is_valid_identifier(to_channel)
        if type == MIDI_CC_TYPE:
            self._c_instance.set_cc_translation(from_identifier, from_channel, to_identifier, to_channel)
        elif type == MIDI_NOTE_TYPE:
            self._c_instance.set_note_translation(from_identifier, from_channel, to_identifier, to_channel)
        else:
            assert False

    @lazy_attribute
    def preferences(self):
        u"""
        Returns a dictionary of preferences, that is persistent and stored in the
        user's preferences folder. :attr:`preferences_key` is used to uniquely access
        the dictionary.
        
        The preferences are saved whenever the control surface is disconnected,
        Live's preferences dialog is closed or Live is shut down.
        
        Raises a :class:`RuntimeError` if the preferences are accessed but
        preferences_key is not set.
        """
        if self.preferences_key is None:
            raise RuntimeError(u'Trying to access preferences without providing a preference_key')
        preferences = self._c_instance.preferences(self.preferences_key)
        pref_dict = {}
        try:
            pref_dict = loads(bytes(preferences))
        except Exception:
            pass

        preferences.set_serializer(lambda : dumps(pref_dict))
        return pref_dict

    def _pre_serialize(self):
        u"""
        This will pre-serialize all settings, as a later access to
        the control surface objects might cause problems with Pickle
        """
        if self.preferences_key is not None:
            preferences = self._c_instance.preferences(self.preferences_key)
            dump = dumps(self.preferences)
            preferences.set_serializer(lambda : dump)


class ControlSurface(SimpleControlSurface):
    u"""
    Extends :class:`SimpleControlSurface` by support for controlling devices.
    
    This class supports device control, i.e. it supports locking to a device, and
    appoints devices when the selected track/device changes etc. The appointing behavior
    can be customized by overriding device_provider_class.
    """
    device_provider_class = DeviceProvider

    def __init__(self, *a, **k):
        super(ControlSurface, self).__init__(*a, **k)
        self._device_provider = None
        self._device_bank_registry = None
        if self.device_provider_class:
            self._init_device_provider()
        self._device_support_injector = inject(device_provider=const(self.device_provider), device_bank_registry=const(self._device_bank_registry)).everywhere()

    def _init_device_provider(self):
        self._device_provider = self.register_disconnectable(self.device_provider_class(song=self.song))
        self._device_bank_registry = self.register_disconnectable(DeviceBankRegistry())
        self._c_instance.update_locks()
        self._device_provider.update_device_selection()

    @property
    def device_provider(self):
        return self._device_provider

    def disconnect(self):
        self._device_provider = None
        self._device_bank_registry = None
        super(ControlSurface, self).disconnect()

    def can_lock_to_devices(self):
        return True

    def lock_to_device(self, device):
        u"""
        Live -> Script
        
        Called by Live when the user enables the lock to device setting.
        """
        assert self._device_provider is not None
        with self.component_guard():
            self._device_provider.lock_to_device(device)

    def unlock_from_device(self, device):
        u"""
        Live -> Script
        
        Called by Live when the user disables the lock to device setting.
        """
        assert self._device_provider is not None
        assert self._device_provider.is_locked_to_device
        with self.component_guard():
            self._device_provider.unlock_from_device()

    def restore_bank(self, bank_index):
        u"""
        Live -> Script
        
        Live tells the script which bank to use.
        """
        assert self._device_provider is not None
        device = self._device_provider.device
        if self._device_provider.is_locked_to_device and liveobj_valid(device):
            with self.component_guard():
                self._device_bank_registry.set_device_bank(device, bank_index)

    def toggle_lock(self):
        u"""
        Script -> Live
        
        Use this function to toggle the script's lock on devices
        """
        self._c_instance.toggle_lock()

    @contextmanager
    def _component_guard(self):
        with super(ControlSurface, self)._component_guard():
            with self._device_support_injector:
                yield
