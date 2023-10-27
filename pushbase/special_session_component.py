# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\special_session_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 10938 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
from ableton.v2.base import const, depends, forward_property, inject, listens, liveobj_valid
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import ClipSlotComponent, SceneComponent, SessionComponent
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface.mode import EnablingModesComponent
from pushbase.touch_strip_element import TouchStripModes, TouchStripStates
from .actions import clip_name_from_clip_slot, scene_description
from .consts import MessageBoxText
from .message_box_component import Messenger

class ClipSlotCopyHandler(Messenger):

    def __init__(self, *a, **k):
        (super(ClipSlotCopyHandler, self).__init__)(*a, **k)
        self._is_copying = False
        self._source_clip_slot = None
        self._last_shown_notification_ref = const(None)

    @property
    def is_copying(self):
        return self._is_copying

    def duplicate(self, clip_slot):
        if self._is_copying:
            self._finish_copying(clip_slot)
        else:
            self._start_copying(clip_slot)

    def stop_copying(self):
        self._reset_copying_state()
        notification_ref = self._last_shown_notification_ref()
        if notification_ref is not None:
            notification_ref.hide()

    def _show_notification(self, notification):
        self._last_shown_notification_ref = self.show_notification(notification)

    def _start_copying(self, source_clip_slot):
        if not source_clip_slot.is_group_slot:
            if liveobj_valid(source_clip_slot.clip):
                if not source_clip_slot.clip.is_recording:
                    self._is_copying = True
                    self._source_clip_slot = source_clip_slot
                    clip_name = clip_name_from_clip_slot(source_clip_slot)
                    self._show_notification((MessageBoxText.COPIED_CLIP, clip_name))
                else:
                    self._show_notification(MessageBoxText.CANNOT_COPY_RECORDING_CLIP)
            else:
                self._show_notification(MessageBoxText.CANNOT_COPY_EMPTY_CLIP)
        else:
            self._show_notification(MessageBoxText.CANNOT_COPY_GROUP_SLOT)

    def _finish_copying(self, target_clip_slot):
        if not target_clip_slot.is_group_slot:
            source_is_audio = self._source_clip_slot.clip.is_audio_clip
            target_track = target_clip_slot.canonical_parent
            if source_is_audio:
                if target_track.has_audio_input:
                    self._perform_copy(target_clip_slot)
                else:
                    self._show_notification(MessageBoxText.CANNOT_COPY_AUDIO_CLIP_TO_MIDI_TRACK)
            else:
                if not target_track.has_audio_input:
                    self._perform_copy(target_clip_slot)
                else:
                    self._show_notification(MessageBoxText.CANNOT_COPY_MIDI_CLIP_TO_AUDIO_TRACK)
        else:
            self._show_notification(MessageBoxText.CANNOT_PASTE_INTO_GROUP_SLOT)

    def _perform_copy(self, target_clip_slot):
        self._source_clip_slot.duplicate_clip_to(target_clip_slot)
        self._on_duplicated(self._source_clip_slot, target_clip_slot)
        self._reset_copying_state()

    def _reset_copying_state(self):
        self._source_clip_slot = None
        self._is_copying = False

    def _on_duplicated(self, source_clip_slot, target_clip_slot):
        clip_name = clip_name_from_clip_slot(source_clip_slot)
        track_name = target_clip_slot.canonical_parent.name
        self._show_notification((MessageBoxText.PASTED_CLIP, clip_name, track_name))


class DuplicateSceneComponent(Component, Messenger):

    def __init__(self, session_ring=None, *a, **k):
        (super(DuplicateSceneComponent, self).__init__)(*a, **k)
        self._session_ring = session_ring
        self._scene_buttons = None

    def set_scene_buttons(self, buttons):
        self._scene_buttons = buttons
        self._on_scene_value.subject = buttons

    @listens('value')
    def _on_scene_value(self, value, index, _, is_momentary):
        if not (self.is_enabled() and value or is_momentary):
            try:
                self.song.duplicate_scene(self._session_ring.scene_offset + index)
                self.show_notification(MessageBoxText.DUPLICATE_SCENE % scene_description(self.song.view.selected_scene, self.song))
            except Live.Base.LimitationError:
                self.expect_dialog(MessageBoxText.SCENE_LIMIT_REACHED)
            except RuntimeError:
                self.expect_dialog(MessageBoxText.SCENE_DUPLICATION_FAILED)
            except IndexError:
                pass


class SpecialClipSlotComponent(ClipSlotComponent, Messenger):

    @depends(copy_handler=(const(None)), fixed_length_recording=(const(None)))
    def __init__(self, copy_handler=None, fixed_length_recording=None, *a, **k):
        (super(SpecialClipSlotComponent, self).__init__)(*a, **k)
        self._copy_handler = copy_handler
        self._fixed_length_recording = fixed_length_recording

    def _do_delete_clip(self):
        if self._clip_slot:
            if self._clip_slot.has_clip:
                clip_name = self._clip_slot.clip.name
                self._clip_slot.delete_clip()
                self.show_notification(MessageBoxText.DELETE_CLIP % clip_name)

    def _do_select_clip(self, clip_slot):
        if liveobj_valid(self._clip_slot):
            if self.song.view.highlighted_clip_slot != self._clip_slot:
                self.song.view.highlighted_clip_slot = self._clip_slot

    def _do_duplicate_clip(self):
        self._copy_handler.duplicate(self._clip_slot)

    def _on_clip_duplicated(self, source_clip, destination_clip):
        slot_name = source_clip.name
        self.show_notification(MessageBoxText.DUPLICATE_CLIP % slot_name)

    def _clip_is_recording(self):
        return self.has_clip() and self._clip_slot.clip.is_recording

    def _do_launch_clip--- This code section failed: ---

 L. 171         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _fixed_length_recording
                4  LOAD_METHOD              should_start_fixed_length_recording

 L. 172         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _clip_slot
               10  CALL_METHOD_1         1  '1 positional argument'
               12  STORE_FAST               'should_start_fixed_length_recording'

 L. 174        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _clip_is_recording
               18  CALL_METHOD_0         0  '0 positional arguments'
               20  STORE_FAST               'clip_is_recording'

 L. 177        22  LOAD_FAST                'fire_state'
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L. 178        26  LOAD_FAST                'should_start_fixed_length_recording'
               28  POP_JUMP_IF_TRUE     34  'to 34'

 L. 179        30  LOAD_FAST                'clip_is_recording'
               32  POP_JUMP_IF_FALSE    38  'to 38'
             34_0  COME_FROM            28  '28'
             34_1  COME_FROM            24  '24'

 L. 180        34  LOAD_FAST                'fire_state'
               36  POP_JUMP_IF_TRUE     56  'to 56'
             38_0  COME_FROM            32  '32'

 L. 182        38  LOAD_GLOBAL              super
               40  LOAD_GLOBAL              SpecialClipSlotComponent
               42  LOAD_FAST                'self'
               44  CALL_FUNCTION_2       2  '2 positional arguments'
               46  LOAD_METHOD              _do_launch_clip
               48  LOAD_FAST                'fire_state'
               50  CALL_METHOD_1         1  '1 positional argument'
               52  POP_TOP          
               54  JUMP_FORWARD        118  'to 118'
             56_0  COME_FROM            36  '36'

 L. 183        56  LOAD_FAST                'should_start_fixed_length_recording'
               58  POP_JUMP_IF_FALSE    98  'to 98'

 L. 184        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _clip_slot
               64  LOAD_ATTR                canonical_parent
               66  STORE_FAST               'track'

 L. 185        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _fixed_length_recording
               72  LOAD_METHOD              start_recording_in_slot

 L. 186        74  LOAD_FAST                'track'
               76  LOAD_GLOBAL              list
               78  LOAD_FAST                'track'
               80  LOAD_ATTR                clip_slots
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  LOAD_METHOD              index
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _clip_slot
               90  CALL_METHOD_1         1  '1 positional argument'
               92  CALL_METHOD_2         2  '2 positional arguments'
               94  POP_TOP          
               96  JUMP_FORWARD        118  'to 118'
             98_0  COME_FROM            58  '58'

 L. 188        98  LOAD_FAST                'clip_is_recording'
              100  POP_JUMP_IF_FALSE   118  'to 118'

 L. 189       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _fixed_length_recording
              106  LOAD_METHOD              stop_recording
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _clip_slot
              112  LOAD_ATTR                clip
              114  CALL_METHOD_1         1  '1 positional argument'
              116  POP_TOP          
            118_0  COME_FROM           100  '100'
            118_1  COME_FROM            96  '96'
            118_2  COME_FROM            54  '54'

Parse error at or near `JUMP_FORWARD' instruction at offset 54


class SpecialSceneComponent(SceneComponent, Messenger):
    clip_slot_component_type = SpecialClipSlotComponent

    def _do_delete_scene(self, scene):
        try:
            if self._scene:
                song = self.song
                description = scene_description(self._scene, song, False)
                song.delete_scene(list(song.scenes).index(self._scene))
                self.show_notification(MessageBoxText.DELETE_SCENE % description)
        except RuntimeError:
            pass


class SpecialSessionComponent(SessionComponent):
    _session_component_ends_initialisation = False
    scene_component_type = SpecialSceneComponent
    duplicate_button = ButtonControl()

    def __init__(self, clip_slot_copy_handler=None, fixed_length_recording=None, *a, **k):
        self._clip_copy_handler = clip_slot_copy_handler or ClipSlotCopyHandler()
        self._fixed_length_recording = fixed_length_recording
        with inject(copy_handler=(const(self._clip_copy_handler)),
          fixed_length_recording=(const(self._fixed_length_recording))).everywhere():
            (super(SpecialSessionComponent, self).__init__)(*a, **k)
        self._slot_launch_button = None
        self._duplicate_button = None
        self._duplicate = DuplicateSceneComponent((self._session_ring), parent=self)
        self._duplicate_enabler = EnablingModesComponent(parent=self,
          component=(self._duplicate))
        self._end_initialisation()

    duplicate_layer = forward_property('_duplicate')('layer')

    @duplicate_button.pressed
    def duplicate_button(self, button):
        self._duplicate_enabler.selected_mode = 'enabled'

    @duplicate_button.released
    def duplicate_button(self, button):
        self._duplicate_enabler.selected_mode = 'disabled'
        self._clip_copy_handler.stop_copying()

    def set_slot_launch_button(self, button):
        self._slot_launch_button = button
        self._on_slot_launch_value.subject = button

    def set_clip_launch_buttons(self, buttons):
        if buttons:
            buttons.reset()
        super(SpecialSessionComponent, self).set_clip_launch_buttons(buttons)

    def set_touch_strip(self, touch_strip):
        if touch_strip:
            touch_strip.set_mode(TouchStripModes.CUSTOM_FREE)
            touch_strip.send_state([TouchStripStates.STATE_OFF for _ in range(touch_strip.state_count)])
        self._on_touch_strip_value.subject = touch_strip

    @listens('value')
    def _on_touch_strip_value(self, value):
        pass

    @listens('value')
    def _on_slot_launch_value(self, value):
        if not (self.is_enabled() and value != 0 or self._slot_launch_button.is_momentary()):
            if liveobj_valid(self.song.view.highlighted_clip_slot):
                self.song.view.highlighted_clip_slot.fire()
            self._slot_launch_button.turn_on()
        else:
            self._slot_launch_button.turn_off()