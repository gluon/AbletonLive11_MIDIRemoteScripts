# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\components\channel_strip.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 18161 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from ...base import EventObject, listens, liveobj_valid, nop
from ..component import Component
from ..control import ButtonControl
from ..elements import DisplayDataSource

def release_control(control):
    if control is not None:
        control.release_parameter()


def reset_button(button):
    if button is not None:
        button.reset()


class ChannelStripComponent(Component):
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
    select_button = ButtonControl()

    def __init__(self, *a, **k):
        (super(ChannelStripComponent, self).__init__)(self, *a, **k)
        ChannelStripComponent._active_instances.append(self)
        self._track = None
        self._send_controls = []
        self._pan_control = None
        self._volume_control = None
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
        self._empty_control_slots = self.register_disconnectable(EventObject())
        self._ChannelStripComponent__on_selected_track_changed.subject = self.song.view

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

        self._mute_button_slot = make_button_slot('mute')
        self._solo_button_slot = make_button_slot('solo')
        self._arm_button_slot = make_button_slot('arm')
        self._shift_button_slot = make_button_slot('shift')
        self._crossfade_toggle_slot = make_button_slot('crossfade_toggle')

    def disconnect(self):
        ChannelStripComponent._active_instances.remove(self)
        for button in [
         self._mute_button,
         self._solo_button,
         self._arm_button,
         self._shift_button,
         self._crossfade_toggle]:
            reset_button(button)

        for control in self._all_controls():
            release_control(control)

        self._track_name_data_source.set_display_string('')
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
            slot.subject = track.mixer_device if liveobj_valid(track) else None

        if liveobj_valid(self._track):
            for button in (
             self._mute_button,
             self._solo_button,
             self._arm_button,
             self._crossfade_toggle):
                if button is not None:
                    button.set_light(False)

        self.select_button.enabled = True if self._track else False
        self._update_track_name_data_source()
        self.update()

    def reset_button_on_exchange(self, button):
        reset_button(button)

    def _update_track_name_data_source(self):
        self._track_name_data_source.set_display_string(self._track.name if liveobj_valid(self._track) else ' - ')

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
        self.select_button.set_control_element(button)
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

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self._update_select_button()

    def _update_select_button(self):
        if liveobj_valid(self._track) or self.empty_color is None:
            if self.song.view.selected_track == self._track:
                self.select_button.color = 'DefaultButton.On'
            else:
                self.select_button.color = 'DefaultButton.Off'
        else:
            self.select_button.color = self.empty_color

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
        if self._pan_control is not None:
            self._pan_control.connect_to(self._track.mixer_device.panning)
        if self._volume_control is not None:
            self._volume_control.connect_to(self._track.mixer_device.volume)
        if self._send_controls is not None:
            index = 0
            for send_control in self._send_controls:
                if send_control is not None:
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
        if self.is_enabled():
            self._empty_control_slots.disconnect()
            if liveobj_valid(self._track):
                self._connect_parameters()
            else:
                self._disconnect_parameters()
            self._ChannelStripComponent__on_selected_track_changed()
            self._on_mute_changed()
            self._on_solo_changed()
            self._on_arm_changed()
            self._on_cf_assign_changed()
        else:
            self._disconnect_parameters()

    @select_button.pressed
    def select_button(self, button):
        self._on_select_button_pressed(button)

    def _on_select_button_pressed(self, button):
        if liveobj_valid(self._track):
            if self.song.view.selected_track != self._track:
                self.song.view.selected_track = self._track

    @select_button.pressed_delayed
    def select_button(self, button):
        self._on_select_button_pressed_delayed(button)

    def _on_select_button_pressed_delayed(self, button):
        pass

    @select_button.released
    def select_button(self, button):
        self._on_select_button_released(button)

    def _on_select_button_released(self, button):
        pass

    @select_button.double_clicked
    def select_button(self, button):
        self._on_select_button_double_clicked(button)

    def _on_select_button_double_clicked(self, button):
        pass

    def _mute_value(self, value):
        if self.is_enabled():
            if liveobj_valid(self._track):
                if self._track != self.song.master_track:
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
            if not liveobj_valid(self._track) or self._track != self.song.master_track:
                self._solo_pressed = value != 0 and self._solo_button.is_momentary()
                if not (value != 0 or self._solo_button.is_momentary()):
                    expected_solos_pressed = 1 if self._solo_pressed else 0
                    solo_exclusive = self.song.exclusive_solo != self._shift_pressed and (not self._solo_button.is_momentary() or ChannelStripComponent.number_of_solos_pressed() == expected_solos_pressed)
                    new_value = not self._track.solo
                    respect_multi_selection = self._track.is_part_of_selection
                    for track in chain(self.song.tracks, self.song.return_tracks):
                        self.update_solo_state(solo_exclusive, new_value, respect_multi_selection, track)

    def _arm_value--- This code section failed: ---

 L. 412         0  LOAD_FAST                'self'
                2  LOAD_METHOD              is_enabled
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_JUMP_IF_FALSE   202  'to 202'

 L. 413         8  LOAD_GLOBAL              liveobj_valid
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _track
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  POP_JUMP_IF_FALSE   202  'to 202'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _track
               22  LOAD_ATTR                can_be_armed
               24  POP_JUMP_IF_FALSE   202  'to 202'

 L. 414        26  LOAD_FAST                'value'
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

 L. 416        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _arm_button
               50  LOAD_METHOD              is_momentary
               52  CALL_METHOD_0         0  '0 positional arguments'
               54  POP_JUMP_IF_FALSE    64  'to 64'
               56  LOAD_FAST                'value'
               58  LOAD_CONST               0
               60  COMPARE_OP               !=
               62  POP_JUMP_IF_FALSE   202  'to 202'
             64_0  COME_FROM            54  '54'

 L. 417        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _arm_pressed
               68  POP_JUMP_IF_FALSE    74  'to 74'
               70  LOAD_CONST               1
               72  JUMP_FORWARD         76  'to 76'
             74_0  COME_FROM            68  '68'
               74  LOAD_CONST               0
             76_0  COME_FROM            72  '72'
               76  STORE_FAST               'expected_arms_pressed'

 L. 419        78  LOAD_FAST                'self'
               80  LOAD_ATTR                song
               82  LOAD_ATTR                exclusive_arm
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _shift_pressed
               88  COMPARE_OP               !=
               90  JUMP_IF_FALSE_OR_POP   114  'to 114'

 L. 420        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _arm_button
               96  LOAD_METHOD              is_momentary
               98  CALL_METHOD_0         0  '0 positional arguments'
              100  UNARY_NOT        
              102  JUMP_IF_TRUE_OR_POP   114  'to 114'

 L. 421       104  LOAD_GLOBAL              ChannelStripComponent
              106  LOAD_METHOD              number_of_arms_pressed
              108  CALL_METHOD_0         0  '0 positional arguments'

 L. 422       110  LOAD_FAST                'expected_arms_pressed'
              112  COMPARE_OP               ==
            114_0  COME_FROM           102  '102'
            114_1  COME_FROM            90  '90'
              114  STORE_FAST               'arm_exclusive'

 L. 425       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _track
              120  LOAD_ATTR                arm
              122  UNARY_NOT        
              124  STORE_FAST               'new_value'

 L. 426       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _track
              130  LOAD_ATTR                is_part_of_selection
              132  STORE_FAST               'respect_multi_selection'

 L. 429       134  SETUP_LOOP          202  'to 202'
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                song
              140  LOAD_ATTR                tracks
              142  GET_ITER         
            144_0  COME_FROM           198  '198'
            144_1  COME_FROM           190  '190'
            144_2  COME_FROM           184  '184'
            144_3  COME_FROM           180  '180'
            144_4  COME_FROM           152  '152'
              144  FOR_ITER            200  'to 200'
              146  STORE_FAST               'track'

 L. 430       148  LOAD_FAST                'track'
              150  LOAD_ATTR                can_be_armed
              152  POP_JUMP_IF_FALSE_LOOP   144  'to 144'

 L. 431       154  LOAD_FAST                'track'
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _track
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_TRUE    174  'to 174'

 L. 432       164  LOAD_FAST                'respect_multi_selection'
              166  POP_JUMP_IF_FALSE   182  'to 182'
              168  LOAD_FAST                'track'
              170  LOAD_ATTR                is_part_of_selection
              172  POP_JUMP_IF_FALSE   182  'to 182'
            174_0  COME_FROM           162  '162'

 L. 434       174  LOAD_FAST                'new_value'
              176  LOAD_FAST                'track'
              178  STORE_ATTR               arm
              180  JUMP_LOOP           144  'to 144'
            182_0  COME_FROM           172  '172'
            182_1  COME_FROM           166  '166'

 L. 436       182  LOAD_FAST                'arm_exclusive'
              184  POP_JUMP_IF_FALSE_LOOP   144  'to 144'
              186  LOAD_FAST                'track'
              188  LOAD_ATTR                arm
              190  POP_JUMP_IF_FALSE_LOOP   144  'to 144'

 L. 437       192  LOAD_CONST               False
              194  LOAD_FAST                'track'
              196  STORE_ATTR               arm
              198  JUMP_LOOP           144  'to 144'
              200  POP_BLOCK        
            202_0  COME_FROM_LOOP      134  '134'
            202_1  COME_FROM            62  '62'
            202_2  COME_FROM            24  '24'
            202_3  COME_FROM            16  '16'
            202_4  COME_FROM             6  '6'

Parse error at or near `COME_FROM_LOOP' instruction at offset 202_0

    def _shift_value(self, value):
        self._shift_pressed = value != 0

    def _crossfade_toggle_value(self, value):
        if self.is_enabled():
            if liveobj_valid(self._track):
                if not (value != 0 or self._crossfade_toggle.is_momentary()):
                    self._track.mixer_device.crossfade_assign = (self._track.mixer_device.crossfade_assign - 1) % len(self._track.mixer_device.crossfade_assignments.values)

    def _on_sends_changed(self):
        if self.is_enabled():
            self.update()

    def _on_mute_changed(self):
        if not self.is_enabled() or self._mute_button is not None and liveobj_valid(self._track) or self.empty_color is None:
            if self._track in chain(self.song.tracks, self.song.return_tracks) and self._track.mute != self._invert_mute_feedback:
                self._mute_button.set_light('Mixer.MuteOff')
            else:
                self._mute_button.set_light('Mixer.MuteOn')
        else:
            self._mute_button.set_light(self.empty_color)

    def _on_solo_changed(self):
        if not self.is_enabled() or self._solo_button is not None and liveobj_valid(self._track) or self.empty_color is None:
            if self._track in chain(self.song.tracks, self.song.return_tracks) and self._track.solo:
                self._solo_button.set_light('Mixer.SoloOn')
            else:
                self._solo_button.set_light('Mixer.SoloOff')
        else:
            self._solo_button.set_light(self.empty_color)

    def _on_arm_changed(self):
        if not self.is_enabled() or self._arm_button is not None and liveobj_valid(self._track) or self.empty_color is None:
            if self._track in self.song.tracks and self._track.can_be_armed and self._track.arm:
                self._arm_button.set_light('Mixer.ArmOn')
            else:
                self._arm_button.set_light('Mixer.ArmOff')
        else:
            self._arm_button.set_light(self.empty_color)

    def _on_track_name_changed(self):
        if liveobj_valid(self._track):
            self._update_track_name_data_source()

    def _on_cf_assign_changed(self):
        if self.is_enabled():
            if self._crossfade_toggle is not None:
                if liveobj_valid(self._track) and self._track in chain(self.song.tracks, self.song.return_tracks) and self._track.mixer_device.crossfade_assign != 1:
                    self._crossfade_toggle.set_light(True)
                else:
                    self._crossfade_toggle.set_light(False)

    def _on_input_routing_changed(self):
        if self.is_enabled():
            self._on_arm_changed()