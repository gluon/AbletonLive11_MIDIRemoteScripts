#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/special_chan_strip_component.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from builtins import zip
from builtins import map
from builtins import str
from builtins import range
from past.utils import old_div
import Live
from ableton.v2.base import flatten, listens, listens_group, liveobj_valid, old_hasattr, task
from ableton.v2.control_surface import components, ParameterSlot
from ableton.v2.control_surface.elements import DisplayDataSource
from pushbase import consts
from pushbase.consts import MessageBoxText
from pushbase.message_box_component import Messenger
from pushbase.mixer_utils import is_set_to_split_stereo
from pushbase.selected_track_parameter_provider import SEND_PARAMETER_NAMES, toggle_arm
from pushbase.song_utils import delete_track_or_return_track
from .parameter_mapping_sensitivities import CONTINUOUS_MAPPING_SENSITIVITY, FINE_GRAINED_CONTINUOUS_MAPPING_SENSITIVITY
TRACK_FOLD_DELAY = 0.5

def param_value_to_graphic(param, graphic):
    if param != None:
        param_range = param.max - param.min
        graph_range = len(graphic) - 1
        value = int(old_div(param.value - param.min, param_range) * graph_range)
        graphic_display_string = graphic[value]
    else:
        graphic_display_string = u' '
    return graphic_display_string


class SpecialChanStripComponent(components.ChannelStripComponent, Messenger):
    u"""
    Channel strip component with press & hold mute solo and stop
    buttons
    """

    def __init__(self, *a, **k):
        super(SpecialChanStripComponent, self).__init__(*a, **k)
        self.empty_color = u'Option.Unused'
        self._invert_mute_feedback = True
        self._duplicate_button = None
        self._selector_button = None
        self._delete_handler = None
        self._track_parameter_name_sources = [ DisplayDataSource(u' ') for _ in range(14) ]
        self._track_parameter_data_sources = [ DisplayDataSource(u' ') for _ in range(14) ]
        self._track_parameter_graphic_sources = [ DisplayDataSource(u' ') for _ in range(14) ]
        self._on_return_tracks_changed.subject = self.song
        self._on_selected_track_changed.subject = self.song.view
        self._fold_task = self._tasks.add(task.sequence(task.wait(TRACK_FOLD_DELAY), task.run(self._do_fold_track))).kill()
        self._cue_volume_slot = self.register_disconnectable(ParameterSlot())

    def set_delete_handler(self, delete_handler):
        self._delete_handler = delete_handler

    def _update_control_sensitivities(self, control):
        if control:
            if old_hasattr(control, u'set_sensitivities'):
                control.set_sensitivities(CONTINUOUS_MAPPING_SENSITIVITY, FINE_GRAINED_CONTINUOUS_MAPPING_SENSITIVITY)
            else:
                control.mapping_sensitivity = CONTINUOUS_MAPPING_SENSITIVITY

    def set_volume_control(self, control):
        self._update_control_sensitivities(control)
        super(SpecialChanStripComponent, self).set_volume_control(control)

    def set_pan_control(self, control):
        self._update_control_sensitivities(control)
        super(SpecialChanStripComponent, self).set_pan_control(control)

    def set_send_controls(self, controls):
        if controls != None:
            for control in controls:
                self._update_control_sensitivities(control)

        super(SpecialChanStripComponent, self).set_send_controls(controls)

    def set_cue_volume_control(self, control):
        self._update_control_sensitivities(control)
        self._cue_volume_slot.control = control

    def set_duplicate_button(self, duplicate_button):
        self._duplicate_button = duplicate_button

    def set_selector_button(self, selector_button):
        self._selector_button = selector_button

    def track_parameter_data_sources(self, index):
        return self._track_parameter_data_sources[index]

    def track_parameter_graphic_sources(self, index):
        return self._track_parameter_graphic_sources[index]

    def track_parameter_name_sources(self, index):
        return self._track_parameter_name_sources[index]

    def set_track(self, track):
        super(SpecialChanStripComponent, self).set_track(track)
        self._update_track_listeners()
        self._update_parameter_name_sources()
        self._update_parameter_values()
        self._on_panning_mode_changed.subject = track.mixer_device if track else None
        arm_subject = track if track and track.can_be_armed else None
        self._on_explicit_arm_changed.subject = arm_subject
        self._on_implicit_arm_changed.subject = arm_subject

    @listens(u'arm')
    def _on_explicit_arm_changed(self):
        if self.is_enabled() and self._track:
            self._update_track_button()

    @listens(u'implicit_arm')
    def _on_implicit_arm_changed(self):
        if self.is_enabled() and self._track:
            self._update_track_button()

    @listens(u'return_tracks')
    def _on_return_tracks_changed(self):
        self._update_track_listeners()
        self._update_parameter_name_sources()
        self._update_parameter_values()

    @listens(u'selected_track')
    def _on_selected_track_changed(self):
        self._update_track_listeners()
        self._update_track_name_data_source()
        self._update_track_button()

    def _update_track_button(self):
        if self.is_enabled():
            if self._track == None:
                self.select_button.color = self.empty_color
            elif self._track.can_be_armed and (self._track.arm or self._track.implicit_arm):
                if self._track == self.song.view.selected_track:
                    self.select_button.color = u'Mixer.ArmSelected'
                else:
                    self.select_button.color = u'Mixer.ArmUnselected'
            elif self._track == self.song.view.selected_track:
                self.select_button.color = u'Option.Selected'
            else:
                self.select_button.color = u'Option.Unselected'

    def _update_track_listeners(self):
        mixer = self._track.mixer_device if self._track else None
        sends = mixer.sends if mixer and self._track != self.song.master_track else ()
        cue_volume = mixer.cue_volume if self._track == self.song.master_track else None
        self._cue_volume_slot.parameter = cue_volume
        self._on_volume_value_changed.subject = mixer and mixer.volume
        self._on_panning_value_changed.subject = mixer and mixer.panning
        self._on_sends_value_changed.replace_subjects(sends)

    def _update_parameter_name_sources(self):
        num_params = len(self._track.mixer_device.sends) + 2 if self._track else 0
        for index, source in enumerate(self._track_parameter_name_sources):
            if index < num_params:
                track_parameter_names = (u'Volume', u'Pan') + SEND_PARAMETER_NAMES
                source.set_display_string(track_parameter_names[index])
            else:
                source.set_display_string(u' ')

    def _update_track_name_data_source(self):
        if self._track_name_data_source:
            if liveobj_valid(self._track):
                selected = self._track == self.song.view.selected_track
                prefix = consts.CHAR_SELECT if selected else u''
                self._track_name_data_source.set_display_string(prefix + self._track.name)
            else:
                self._track_name_data_source.set_display_string(u' ')

    @property
    def _is_deleting(self):
        return self._delete_handler and self._delete_handler.is_deleting

    def _on_select_button_pressed(self, button):
        if self.is_enabled() and self._track:
            if self._duplicate_button and self._duplicate_button.is_pressed():
                self._do_duplicate_track(self._track)
            elif self._is_deleting:
                self._do_delete_track(self._track)
            elif self._shift_pressed:
                toggle_arm(self._track, self.song, exclusive=False)
            else:
                self._select_value_without_modifier(button)

    def _mute_value(self, value):
        if self.is_enabled() and liveobj_valid(self._track):
            if not self._mute_button.is_momentary() or value != 0:
                if self._is_deleting:
                    self._delete_handler.delete_clip_envelope(self._track.mixer_device.track_activator)
                else:
                    super(SpecialChanStripComponent, self)._mute_value(value)

    def _select_value_without_modifier(self, button):
        if self.song.view.selected_track == self._track:
            song = self.song
            toggle_arm(self._track, song, exclusive=song.exclusive_arm)
        else:
            super(SpecialChanStripComponent, self)._on_select_button_pressed(button)
        if self._track.is_foldable:
            self._fold_task.restart()
        else:
            self._fold_task.kill()

    def _on_select_button_released(self, button):
        self._fold_task.kill()

    def _do_delete_track(self, track):
        try:
            name = track.name
            delete_track_or_return_track(self.song, track)
            self.show_notification(MessageBoxText.DELETE_TRACK % name)
        except RuntimeError:
            self.expect_dialog(MessageBoxText.TRACK_DELETE_FAILED)
        except ValueError:
            pass

    def _do_duplicate_track(self, track):
        try:
            track_index = list(self.song.tracks).index(track)
            self.song.duplicate_track(track_index)
            self.show_notification(MessageBoxText.DUPLICATE_TRACK % track.name)
        except Live.Base.LimitationError:
            self.expect_dialog(MessageBoxText.TRACK_LIMIT_REACHED)
        except RuntimeError:
            self.expect_dialog(MessageBoxText.TRACK_DUPLICATION_FAILED)
        except ValueError:
            pass

    def _do_select_track(self, track):
        pass

    def _do_fold_track(self):
        if self.is_enabled() and liveobj_valid(self._track) and self._track.is_foldable:
            self._track.fold_state = not self._track.fold_state

    @listens(u'value')
    def _on_volume_value_changed(self):
        if self.is_enabled() and liveobj_valid(self._track):
            param = self._track.mixer_device.volume
            text = self._track_parameter_data_sources[0]
            graph = self._track_parameter_graphic_sources[0]
            text.set_display_string(str(param))
            graph.set_display_string(param_value_to_graphic(param, consts.GRAPH_VOL))

    @listens(u'value')
    def _on_panning_value_changed(self):
        if self.is_enabled() and liveobj_valid(self._track):
            param = self._track.mixer_device.panning
            text = self._track_parameter_data_sources[1]
            graph = self._track_parameter_graphic_sources[1]
            text.set_display_string(str(param))
            graph.set_display_string(param_value_to_graphic(param, consts.GRAPH_PAN))

    @listens_group(u'value')
    def _on_sends_value_changed(self, send):
        if self.is_enabled() and liveobj_valid(self._track) and self._track != self.song.master_track and send in list(self._track.mixer_device.sends):
            index = list(self._track.mixer_device.sends).index(send) + 2
            text = self._track_parameter_data_sources[index]
            graph = self._track_parameter_graphic_sources[index]
            text.set_display_string(str(send))
            graph.set_display_string(param_value_to_graphic(send, consts.GRAPH_VOL))

    def _update_parameter_values(self):
        for source in flatten(list(zip(self._track_parameter_data_sources, self._track_parameter_graphic_sources))):
            source.set_display_string(u' ')

        self._on_volume_value_changed()
        self._on_panning_value_changed()
        if self._track and self._track != self.song.master_track:
            list(map(self._on_sends_value_changed, self._track.mixer_device.sends))

    def update(self):
        super(SpecialChanStripComponent, self).update()
        if self.is_enabled():
            self._update_track_button()

    @listens(u'panning_mode')
    def _on_panning_mode_changed(self):
        self.update()

    @listens(u'value')
    def _on_pan_control_value_changed(self, _):
        pass

    def _connect_parameters(self):
        super(SpecialChanStripComponent, self)._connect_parameters()
        if self._pan_control != None and liveobj_valid(self._track):
            if is_set_to_split_stereo(self._track.mixer_device):
                self._pan_control.release_parameter()
                self._on_pan_control_value_changed.subject = self._pan_control
            else:
                self._on_pan_control_value_changed.subject = None

    def _disconnect_parameters(self):
        super(SpecialChanStripComponent, self)._disconnect_parameters()
        self._on_pan_control_value_changed.subject = None
