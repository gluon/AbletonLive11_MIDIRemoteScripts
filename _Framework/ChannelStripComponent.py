# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\ChannelStripComponent.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 18403 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from itertools import chain
import Live
from .ControlSurfaceComponent import ControlSurfaceComponent
from .DisplayDataSource import DisplayDataSource
from .Util import nop

def release_control(control):
    if control != None:
        control.release_parameter()


def reset_button(button):
    if button != None:
        button.reset()


class ChannelStripComponent(ControlSurfaceComponent):
    _active_instances = []

    def number_of_arms_pressed():
        result = 0
        for strip in ChannelStripComponent._active_instances:
            if strip.arm_button_pressed():
                result += 1

        return result

    number_of_arms_pressed = staticmethod(number_of_arms_pressed)

    def number_of_solos_pressed():
        result = 0
        for strip in ChannelStripComponent._active_instances:
            if strip.solo_button_pressed():
                result += 1

        return result

    number_of_solos_pressed = staticmethod(number_of_solos_pressed)
    empty_color = None

    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        ChannelStripComponent._active_instances.append(self)
        self._track = None
        self._send_controls = []
        self._pan_control = None
        self._volume_control = None
        self._select_button = None
        self._mute_button = None
        self._solo_button = None
        self._arm_button = None
        self._shift_button = None
        self._crossfade_toggle = None
        self._shift_pressed = False
        self._solo_pressed = False
        self._arm_pressed = False
        self._invert_mute_feedback = False
        self._track_name_data_source = DisplayDataSource()
        self._update_track_name_data_source()
        self._empty_control_slots = self.register_slot_manager()

        def make_property_slot(name, alias=None):
            alias = alias or name
            return self.register_slot(None, getattr(self, '_on_%s_changed' % alias), name)

        self._track_property_slots = [
         make_property_slot('mute'),
         make_property_slot('solo'),
         make_property_slot('arm'),
         make_property_slot('input_routing_type', 'input_routing'),
         make_property_slot('name', 'track_name')]
        self._mixer_device_property_slots = [
         make_property_slot('crossfade_assign', 'cf_assign'),
         make_property_slot('sends')]

        def make_button_slot(name):
            return self.register_slot(None, getattr(self, '_%s_value' % name), 'value')

        self._select_button_slot = make_button_slot('select')
        self._mute_button_slot = make_button_slot('mute')
        self._solo_button_slot = make_button_slot('solo')
        self._arm_button_slot = make_button_slot('arm')
        self._shift_button_slot = make_button_slot('shift')
        self._crossfade_toggle_slot = make_button_slot('crossfade_toggle')

    def disconnect(self):
        ChannelStripComponent._active_instances.remove(self)
        for button in [
         self._select_button,
         self._mute_button,
         self._solo_button,
         self._arm_button,
         self._shift_button,
         self._crossfade_toggle]:
            reset_button(button)

        for control in self._all_controls():
            release_control(control)

        self._track_name_data_source.set_display_string('')
        self._select_button = None
        self._mute_button = None
        self._solo_button = None
        self._arm_button = None
        self._shift_button = None
        self._crossfade_toggle = None
        self._track_name_data_source = None
        self._pan_control = None
        self._volume_control = None
        self._send_controls = None
        self._track = None
        super(ChannelStripComponent, self).disconnect()

    def set_track(self, track):
        for control in self._all_controls():
            release_control(control)

        self._track = track
        for slot in self._track_property_slots:
            slot.subject = track

        for slot in self._mixer_device_property_slots:
            slot.subject = track.mixer_device if track != None else None

        if self._track != None:
            for button in (
             self._select_button,
             self._mute_button,
             self._solo_button,
             self._arm_button,
             self._crossfade_toggle):
                if button != None:
                    button.turn_off()

        self._update_track_name_data_source()
        self.update()

    def reset_button_on_exchange(self, button):
        reset_button(button)

    def _update_track_name_data_source(self):
        self._track_name_data_source.set_display_string(self._track.name if self._track != None else ' - ')

    def set_send_controls(self, controls):
        for control in list(self._send_controls or []):
            release_control(control)

        self._send_controls = controls
        self.update()

    def set_pan_control(self, control):
        if control != self._pan_control:
            release_control(self._pan_control)
            self._pan_control = control
            self.update()

    def set_volume_control(self, control):
        if control != self._volume_control:
            release_control(self._volume_control)
            self._volume_control = control
            self.update()

    def set_select_button(self, button):
        if button != self._select_button:
            self.reset_button_on_exchange(self._select_button)
            self._select_button = button
            self._select_button_slot.subject = button
            self.update()

    def set_mute_button(self, button):
        if button != self._mute_button:
            self.reset_button_on_exchange(self._mute_button)
            self._mute_button = button
            self._mute_button_slot.subject = button
            self.update()

    def set_solo_button(self, button):
        if button != self._solo_button:
            self.reset_button_on_exchange(self._solo_button)
            self._solo_pressed = False
            self._solo_button = button
            self._solo_button_slot.subject = button
            self.update()

    def set_arm_button(self, button):
        if button != self._arm_button:
            self.reset_button_on_exchange(self._arm_button)
            self._arm_pressed = False
            self._arm_button = button
            self._arm_button_slot.subject = button
            self.update()

    def set_shift_button(self, button):
        if button != self._shift_button:
            self.reset_button_on_exchange(self._shift_button)
            self._shift_button = button
            self._shift_button_slot.subject = button
            self.update()

    def set_crossfade_toggle(self, button):
        if button != self._crossfade_toggle:
            self.reset_button_on_exchange(self._crossfade_toggle)
            self._crossfade_toggle = button
            self._crossfade_toggle_slot.subject = button
            self.update()

    def set_invert_mute_feedback(self, invert_feedback):
        if invert_feedback != self._invert_mute_feedback:
            self._invert_mute_feedback = invert_feedback
            self.update()

    def on_enabled_changed(self):
        self.update()

    def on_selected_track_changed(self):
        if self.is_enabled():
            if self._select_button != None:
                if self._track != None or self.empty_color == None:
                    if self.song().view.selected_track == self._track:
                        self._select_button.turn_on()
                    else:
                        self._select_button.turn_off()
                else:
                    self._select_button.set_light(self.empty_color)

    def solo_button_pressed(self):
        return self._solo_pressed

    def arm_button_pressed(self):
        return self._arm_pressed

    def track_name_data_source(self):
        return self._track_name_data_source

    @property
    def track(self):
        return self._track

    def _connect_parameters(self):
        if self._pan_control != None:
            self._pan_control.connect_to(self._track.mixer_device.panning)
        if self._volume_control != None:
            self._volume_control.connect_to(self._track.mixer_device.volume)
        if self._send_controls != None:
            index = 0
            for send_control in self._send_controls:
                if send_control != None:
                    if index < len(self._track.mixer_device.sends):
                        send_control.connect_to(self._track.mixer_device.sends[index])
                    else:
                        send_control.release_parameter()
                        self._empty_control_slots.register_slot(send_control, nop, 'value')
                index += 1

    def _all_controls(self):
        return [self._pan_control, self._volume_control] + list(self._send_controls or [])

    def _disconnect_parameters(self):
        for control in self._all_controls():
            release_control(control)
            self._empty_control_slots.register_slot(control, nop, 'value')

    def update(self):
        super(ChannelStripComponent, self).update()
        if self._allow_updates:
            if self.is_enabled():
                self._empty_control_slots.disconnect()
                if self._track != None:
                    self._connect_parameters()
                else:
                    self._disconnect_parameters()
                self.on_selected_track_changed()
                self._on_mute_changed()
                self._on_solo_changed()
                self._on_arm_changed()
                self._on_cf_assign_changed()
            else:
                self._disconnect_parameters()
        else:
            self._update_requests += 1

    def _select_value(self, value):
        if not self.is_enabled() or self._track != None:
            if not (value != 0 or self._select_button.is_momentary()):
                if self.song().view.selected_track != self._track:
                    self.song().view.selected_track = self._track

    def _mute_value(self, value):
        if self.is_enabled():
            if self._track != None:
                if self._track != self.song().master_track:
                    if not self._mute_button.is_momentary() or value != 0:
                        self._track.mute = not self._track.mute

    def update_solo_state--- This code section failed: ---

 L. 379         0  LOAD_FAST                'track'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _track
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_TRUE     20  'to 20'

 L. 380        10  LOAD_FAST                'respect_multi_selection'
               12  POP_JUMP_IF_FALSE    28  'to 28'
               14  LOAD_FAST                'track'
               16  LOAD_ATTR                is_part_of_selection
               18  POP_JUMP_IF_FALSE    28  'to 28'
             20_0  COME_FROM             8  '8'

 L. 382        20  LOAD_FAST                'new_value'
               22  LOAD_FAST                'track'
               24  STORE_ATTR               solo
               26  JUMP_FORWARD         44  'to 44'
             28_0  COME_FROM            18  '18'
             28_1  COME_FROM            12  '12'

 L. 383        28  LOAD_FAST                'solo_exclusive'
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  LOAD_FAST                'track'
               34  LOAD_ATTR                solo
               36  POP_JUMP_IF_FALSE    44  'to 44'

 L. 384        38  LOAD_CONST               False
               40  LOAD_FAST                'track'
               42  STORE_ATTR               solo
             44_0  COME_FROM            36  '36'
             44_1  COME_FROM            30  '30'
             44_2  COME_FROM            26  '26'

Parse error at or near `COME_FROM' instruction at offset 44_1

    def _solo_value(self, value):
        if self.is_enabled():
            if not self._track != None or self._track != self.song().master_track:
                self._solo_pressed = value != 0 and self._solo_button.is_momentary()
                if not (value != 0 or self._solo_button.is_momentary()):
                    expected_solos_pressed = 1 if self._solo_pressed else 0
                    solo_exclusive = self.song().exclusive_solo != self._shift_pressed and (not self._solo_button.is_momentary() or ChannelStripComponent.number_of_solos_pressed() == expected_solos_pressed)
                    new_value = not self._track.solo
                    respect_multi_selection = self._track.is_part_of_selection
                    for track in chain(self.song().tracks, self.song().return_tracks):
                        self.update_solo_state(solo_exclusive, new_value, respect_multi_selection, track)

    def _arm_value--- This code section failed: ---

 L. 418         0  LOAD_FAST                'self'
                2  LOAD_METHOD              is_enabled
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_JUMP_IF_FALSE   206  'to 206'

 L. 419         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _track
               12  LOAD_CONST               None
               14  COMPARE_OP               !=
               16  POP_JUMP_IF_FALSE   206  'to 206'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _track
               22  LOAD_ATTR                can_be_armed
               24  POP_JUMP_IF_FALSE   206  'to 206'

 L. 420        26  LOAD_FAST                'value'
               28  LOAD_CONST               0
               30  COMPARE_OP               !=
               32  JUMP_IF_FALSE_OR_POP    42  'to 42'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _arm_button
               38  LOAD_METHOD              is_momentary
               40  CALL_METHOD_0         0  '0 positional arguments'
             42_0  COME_FROM            32  '32'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _arm_pressed

 L. 422        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _arm_button
               50  LOAD_METHOD              is_momentary
               52  CALL_METHOD_0         0  '0 positional arguments'
               54  POP_JUMP_IF_FALSE    64  'to 64'
               56  LOAD_FAST                'value'
               58  LOAD_CONST               0
               60  COMPARE_OP               !=
               62  POP_JUMP_IF_FALSE   206  'to 206'
             64_0  COME_FROM            54  '54'

 L. 423        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _arm_pressed
               68  POP_JUMP_IF_FALSE    74  'to 74'
               70  LOAD_CONST               1
               72  JUMP_FORWARD         76  'to 76'
             74_0  COME_FROM            68  '68'
               74  LOAD_CONST               0
             76_0  COME_FROM            72  '72'
               76  STORE_FAST               'expected_arms_pressed'

 L. 426        78  LOAD_FAST                'self'
               80  LOAD_METHOD              song
               82  CALL_METHOD_0         0  '0 positional arguments'
               84  LOAD_ATTR                exclusive_arm
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _shift_pressed
               90  COMPARE_OP               !=
               92  JUMP_IF_FALSE_OR_POP   116  'to 116'

 L. 428        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _arm_button
               98  LOAD_METHOD              is_momentary
              100  CALL_METHOD_0         0  '0 positional arguments'
              102  UNARY_NOT        
              104  JUMP_IF_TRUE_OR_POP   116  'to 116'

 L. 429       106  LOAD_GLOBAL              ChannelStripComponent
              108  LOAD_METHOD              number_of_arms_pressed
              110  CALL_METHOD_0         0  '0 positional arguments'

 L. 430       112  LOAD_FAST                'expected_arms_pressed'
              114  COMPARE_OP               ==
            116_0  COME_FROM           104  '104'
            116_1  COME_FROM            92  '92'
              116  STORE_FAST               'arm_exclusive'

 L. 433       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _track
              122  LOAD_ATTR                arm
              124  UNARY_NOT        
              126  STORE_FAST               'new_value'

 L. 434       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _track
              132  LOAD_ATTR                is_part_of_selection
              134  STORE_FAST               'respect_multi_selection'

 L. 437       136  SETUP_LOOP          206  'to 206'
              138  LOAD_FAST                'self'
              140  LOAD_METHOD              song
              142  CALL_METHOD_0         0  '0 positional arguments'
              144  LOAD_ATTR                tracks
              146  GET_ITER         
            148_0  COME_FROM           202  '202'
            148_1  COME_FROM           194  '194'
            148_2  COME_FROM           188  '188'
            148_3  COME_FROM           184  '184'
            148_4  COME_FROM           156  '156'
              148  FOR_ITER            204  'to 204'
              150  STORE_FAST               'track'

 L. 438       152  LOAD_FAST                'track'
              154  LOAD_ATTR                can_be_armed
              156  POP_JUMP_IF_FALSE_LOOP   148  'to 148'

 L. 439       158  LOAD_FAST                'track'
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                _track
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_TRUE    178  'to 178'

 L. 440       168  LOAD_FAST                'respect_multi_selection'
              170  POP_JUMP_IF_FALSE   186  'to 186'
              172  LOAD_FAST                'track'
              174  LOAD_ATTR                is_part_of_selection
              176  POP_JUMP_IF_FALSE   186  'to 186'
            178_0  COME_FROM           166  '166'

 L. 442       178  LOAD_FAST                'new_value'
              180  LOAD_FAST                'track'
              182  STORE_ATTR               arm
              184  JUMP_LOOP           148  'to 148'
            186_0  COME_FROM           176  '176'
            186_1  COME_FROM           170  '170'

 L. 444       186  LOAD_FAST                'arm_exclusive'
              188  POP_JUMP_IF_FALSE_LOOP   148  'to 148'
              190  LOAD_FAST                'track'
              192  LOAD_ATTR                arm
              194  POP_JUMP_IF_FALSE_LOOP   148  'to 148'

 L. 445       196  LOAD_CONST               False
              198  LOAD_FAST                'track'
              200  STORE_ATTR               arm
              202  JUMP_LOOP           148  'to 148'
              204  POP_BLOCK        
            206_0  COME_FROM_LOOP      136  '136'
            206_1  COME_FROM            62  '62'
            206_2  COME_FROM            24  '24'
            206_3  COME_FROM            16  '16'
            206_4  COME_FROM             6  '6'

Parse error at or near `COME_FROM_LOOP' instruction at offset 206_0

    def _shift_value(self, value):
        self._shift_pressed = value != 0

    def _crossfade_toggle_value(self, value):
        if self.is_enabled():
            if self._track != None:
                if not (value != 0 or self._crossfade_toggle.is_momentary()):
                    self._track.mixer_device.crossfade_assign = (self._track.mixer_device.crossfade_assign - 1) % len(self._track.mixer_device.crossfade_assignments.values)

    def _on_sends_changed(self):
        if self.is_enabled():
            self.update()

    def _on_mute_changed(self):
        if not self.is_enabled() or self._mute_button != None and self._track != None or self.empty_color == None:
            if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.mute != self._invert_mute_feedback:
                self._mute_button.turn_on()
            else:
                self._mute_button.turn_off()
        else:
            self._mute_button.set_light(self.empty_color)

    def _on_solo_changed(self):
        if not self.is_enabled() or self._solo_button != None and self._track != None or self.empty_color == None:
            if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.solo:
                self._solo_button.turn_on()
            else:
                self._solo_button.turn_off()
        else:
            self._solo_button.set_light(self.empty_color)

    def _on_arm_changed(self):
        if not self.is_enabled() or self._arm_button != None and self._track != None or self.empty_color == None:
            if self._track in self.song().tracks and self._track.can_be_armed and self._track.arm:
                self._arm_button.turn_on()
            else:
                self._arm_button.turn_off()
        else:
            self._arm_button.set_light(self.empty_color)

    def _on_track_name_changed(self):
        if self._track != None:
            self._update_track_name_data_source()

    def _on_cf_assign_changed(self):
        if self.is_enabled():
            if self._crossfade_toggle != None:
                if self._track != None and self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.mixer_device.crossfade_assign != 1:
                    self._crossfade_toggle.turn_on()
                else:
                    self._crossfade_toggle.turn_off()

    def _on_input_routing_changed(self):
        if self.is_enabled():
            self._on_arm_changed()