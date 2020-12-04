#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/note_settings_component.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
import Live
from builtins import filter
from builtins import str
from builtins import map
from builtins import range
from builtins import round
from past.utils import old_div
import math
from functools import partial
from itertools import chain
from ableton.v2.base import clamp, find_if, forward_property, listenable_property, listens, listens_group, liveobj_valid, task
from ableton.v2.control_surface import defaults, Component
from ableton.v2.control_surface.control import ButtonControl, ControlManager, control_list, EncoderControl, StepEncoderControl
from ableton.v2.control_surface.elements import DisplayDataSource
from ableton.v2.control_surface.mode import ModesComponent, Mode, AddLayerMode
from .consts import CHAR_ELLIPSIS, GRAPH_VOL

class NoteSettingBase(ControlManager):
    __events__ = (u'setting_changed',)
    attribute_index = -1
    encoder = EncoderControl()

    def __init__(self, grid_resolution = None, *a, **k):
        super(NoteSettingBase, self).__init__(*a, **k)
        self._min_max_value = None
        self._grid_resolution = grid_resolution

    def encoder_value_to_attribute(self, value):
        raise NotImplementedError

    @property
    def step_length(self):
        if self._grid_resolution:
            return self._grid_resolution.step_length
        return 1.0

    def set_min_max(self, min_max_value):
        self._min_max_value = min_max_value

    @encoder.value
    def encoder(self, value, _):
        self._on_encoder_value_changed(value)

    def _on_encoder_value_changed(self, value):
        self.notify_setting_changed(self.attribute_index, self.encoder_value_to_attribute(value))


class NoteSetting(NoteSettingBase):

    def __init__(self, *a, **k):
        super(NoteSetting, self).__init__(*a, **k)
        self.value_source = DisplayDataSource()
        self.label_source = DisplayDataSource()
        self.label_source.set_display_string(self.get_label())

    def get_label(self):
        raise NotImplementedError

    def attribute_min_max_to_string(self, min_value, max_value):
        raise NotImplementedError

    def set_min_max(self, min_max_value):
        self.value_source.set_display_string(self.attribute_min_max_to_string(min_max_value[0], min_max_value[1]) if min_max_value else u'-')


RANGE_STRING_FLOAT = u'%.1f' + CHAR_ELLIPSIS + u'%.1f'
RANGE_STRING_INT = u'%d' + CHAR_ELLIPSIS + u'%d'
RANGE_STRING_PERCENT = u'%d %%' + CHAR_ELLIPSIS + u'%d %%'

def step_offset_percentage(step_length, value):
    return int(round(old_div(value - int(old_div(value, step_length)) * step_length, step_length) * 100))


def step_offset_min_max_to_string(step_length, min_value, max_value):
    min_value = step_offset_percentage(step_length, min_value)
    max_value = step_offset_percentage(step_length, max_value)
    if min_value == max_value:
        return u'%d%%' % min_value
    return (RANGE_STRING_INT + u'%%') % (min_value, max_value)


def convert_value_to_graphic(value, value_range):
    value_bar = GRAPH_VOL
    graph_range = float(len(value_bar))
    value = clamp(int(old_div(value, value_range) * graph_range), 0, len(value_bar) - 1)
    display_string = value_bar[value]
    return display_string


class NoteNudgeSetting(NoteSetting):
    attribute_index = 1

    def get_label(self):
        return u'Nudge'

    def encoder_value_to_attribute(self, value):
        return self.step_length * value

    def attribute_min_max_to_string(self, min_value, max_value):
        return step_offset_min_max_to_string(self.step_length, min_value, max_value)


class NoteLengthCoarseSetting(NoteSetting):
    attribute_index = 2
    encoder = StepEncoderControl()

    def get_label(self):
        return u'Length -'

    def attribute_min_max_to_string(self, min_value, max_value):
        min_value = old_div(min_value, self.step_length)
        max_value = old_div(max_value, self.step_length)

        def format_string(value):
            num_non_decimal_figures = int(math.log10(value)) if value > 0 else 0
            return u'%%.%dg' % (num_non_decimal_figures + 2,)

        if min_value == max_value:
            return (format_string(min_value) + u' stp') % min_value
        return (format_string(min_value) + CHAR_ELLIPSIS + format_string(max_value)) % (min_value, max_value)

    def encoder_value_to_attribute(self, value):
        return self.step_length * value

    @encoder.value
    def encoder(self, value, _):
        self._on_encoder_value_changed(value)


class NoteLengthFineSetting(NoteSetting):
    attribute_index = 2

    def get_label(self):
        return u'Fine'

    def encoder_value_to_attribute(self, value):
        return self.step_length * value

    def attribute_min_max_to_string(self, min_value, max_value):
        value = step_offset_percentage(self.step_length, min_value)
        return convert_value_to_graphic(value, 100.0)


class NoteVelocitySetting(NoteSetting):
    attribute_index = 3

    def get_label(self):
        return u'Velocity'

    def encoder_value_to_attribute(self, value):
        return value * 128

    def attribute_min_max_to_string(self, min_value, max_value):
        if int(min_value) == int(max_value):
            return str(int(min_value))
        return RANGE_STRING_INT % (min_value, max_value)


class NoteVelocityDeviationSetting(NoteSetting):
    attribute_index = 4

    def get_label(self):
        return u'VelRange'

    def encoder_value_to_attribute(self, value):
        return value * 128

    def attribute_min_max_to_string(self, min_value, max_value):

        def sign_of(x):
            if x > 0:
                return u'+'
            return u''

        if int(min_value) == int(max_value):
            return sign_of(min_value) + str(int(min_value))
        return RANGE_STRING_INT % (min_value, max_value)


class NoteProbabilitySetting(NoteSetting):
    attribute_index = 5

    def get_label(self):
        return u'Problty'

    def encoder_value_to_attribute(self, value):
        return value * 128

    def attribute_min_max_to_string(self, min_value, max_value):
        min_value_percent = round(min_value * 100)
        max_value_percent = round(max_value * 100)
        if min_value_percent == max_value_percent:
            return u'%d %%' % min_value_percent
        return RANGE_STRING_PERCENT % (min_value_percent, max_value_percent)


class NoteSettingsComponentBase(Component):
    __events__ = (u'setting_changed', u'full_velocity')
    full_velocity_button = ButtonControl()

    def __init__(self, grid_resolution = None, *a, **k):
        super(NoteSettingsComponentBase, self).__init__(*a, **k)
        self._settings = []
        self._encoders = []
        self._create_settings(grid_resolution)

    def _create_settings(self, grid_resolution):
        self._add_setting(NoteNudgeSetting(grid_resolution=grid_resolution))
        self._add_setting(NoteLengthCoarseSetting(grid_resolution=grid_resolution))
        self._add_setting(NoteLengthFineSetting(grid_resolution=grid_resolution))
        self._add_setting(NoteVelocitySetting(grid_resolution=grid_resolution))
        if self.show_velocity_ranges_and_probabilities:
            self._add_setting(NoteVelocityDeviationSetting(grid_resolution=grid_resolution))
            self._add_setting(NoteProbabilitySetting(grid_resolution=grid_resolution))

    def _add_setting(self, setting):
        assert len(self._settings) < 8, u'Cannot show more than 8 settings'
        self._settings.append(setting)
        self._update_encoders()
        self.register_disconnectable(setting)
        self.register_slot(setting, self.notify_setting_changed, u'setting_changed')

    @property
    def number_of_settings(self):
        return len(self._settings)

    @property
    def settings(self):
        return self._settings

    @property
    def show_velocity_ranges_and_probabilities(self):
        return Live.Application.UnavailableFeature.note_velocity_ranges_and_probabilities not in Live.Application.get_application().unavailable_features

    def set_info_message(self, message):
        pass

    def set_encoder_controls(self, encoders):
        self._encoders = encoders or []
        self._update_encoders()

    def set_min_max(self, index, min_max_value):
        setting_for_index = [ i for i in self._settings if i.attribute_index == index ]
        for setting in setting_for_index:
            setting.set_min_max(min_max_value)

    @full_velocity_button.pressed
    def full_velocity_button(self, button):
        if self.is_enabled():
            self.notify_full_velocity()

    def _update_encoders(self):
        u"""
        This assigns each encoder to a setting in the same order
        as the settings are created in _create_settings, which means:
        0 - Nudge
        1 - Length
        2 - Fine
        3 - Velocity
        4 - Velocity Deviation
        5 - Probability
        """
        if self.is_enabled() and self._encoders:
            for index, setting in enumerate(self._settings):
                setting.encoder.set_control_element(self._encoders[index])

        else:
            list(map(lambda setting: setting.encoder.set_control_element(None), self._settings))

    def update(self):
        super(NoteSettingsComponentBase, self).update()
        self._update_encoders()


class NoteSettingsComponent(NoteSettingsComponentBase):

    def __init__(self, *a, **k):
        super(NoteSettingsComponent, self).__init__(*a, **k)
        self._top_data_sources = [ DisplayDataSource() for _ in range(8) ]
        self._bottom_data_sources = [ DisplayDataSource() for _ in range(8) ]
        self._info_data_source = DisplayDataSource()
        self._create_display_sources()

    def _create_display_sources(self):
        self._top_data_sources = [ s.label_source for s in self._settings ] + [ DisplayDataSource() for _ in range(8 - len(self._settings)) ]
        self._bottom_data_sources = [ s.value_source for s in self._settings ] + [ DisplayDataSource() for _ in range(8 - len(self._settings)) ]

    def set_top_display_line(self, display):
        if self.is_enabled() and display:
            display.set_data_sources(self._top_data_sources)

    def set_bottom_display_line(self, display):
        if self.is_enabled() and display:
            display.set_data_sources(self._bottom_data_sources)

    def set_info_display_line(self, display):
        if self.is_enabled() and display:
            display.set_data_sources([self._info_data_source])

    def set_clear_display_line(self, display):
        if self.is_enabled() and display:
            display.reset()

    def set_info_message(self, message):
        self._info_data_source.set_display_string(message.rjust(62))


class DetailViewRestorerMode(Mode):
    u"""
    Restores the detail view if either only clip view or device view is visible.
    Has no effect if the detail view is hidden at the point the mode is entered.
    """

    def __init__(self, application = None, *a, **k):
        super(DetailViewRestorerMode, self).__init__(*a, **k)
        self._app = application
        self._view_to_restore = None

    def enter_mode(self):
        clip_view_visible = self._app.view.is_view_visible(u'Detail/Clip', False)
        device_chain_visible = self._app.view.is_view_visible(u'Detail/DeviceChain', False)
        if clip_view_visible != device_chain_visible:
            self._view_to_restore = u'Detail/Clip' if clip_view_visible else u'Detail/DeviceChain'

    def leave_mode(self):
        try:
            if self._view_to_restore:
                self._app.view.show_view(self._view_to_restore)
                self._view_to_restore = None
        except RuntimeError:
            pass


def show_clip_view(application):
    try:
        view = application.view
        if view.is_view_visible(u'Detail/DeviceChain', False) and not view.is_view_visible(u'Detail/Clip', False):
            application.view.show_view(u'Detail/Clip')
    except RuntimeError:
        pass


class ModeSelector(Component):
    select_buttons = control_list(ButtonControl, color=u'DefaultButton.Disabled')
    state_buttons = control_list(ButtonControl, color=u'DefaultButton.Disabled')


class NoteEditorSettingsComponent(ModesComponent):
    initial_encoders = control_list(EncoderControl)
    encoders = control_list(EncoderControl)

    def __init__(self, note_settings_component_class = None, automation_component_class = None, grid_resolution = None, initial_encoder_layer = None, encoder_layer = None, *a, **k):
        super(NoteEditorSettingsComponent, self).__init__(*a, **k)
        assert encoder_layer
        assert note_settings_component_class is not None
        assert automation_component_class is not None
        self.settings = note_settings_component_class(grid_resolution=grid_resolution, parent=self, is_enabled=False)
        self.automation = automation_component_class(parent=self, is_enabled=False)
        self._mode_selector = ModeSelector(parent=self, is_enabled=False)
        self._visible_detail_view = u'Detail/DeviceChain'
        self._show_settings_task = self._tasks.add(task.sequence(task.wait(defaults.MOMENTARY_DELAY), task.run(self._show_settings))).kill()
        self._update_infos_task = self._tasks.add(task.run(self._update_note_infos)).kill()
        self._settings_modes = ModesComponent(parent=self)
        self._settings_modes.set_enabled(False)
        self._settings_modes.add_mode(u'automation', [self.automation,
         self._mode_selector,
         partial(self._set_envelope_view_visible, True),
         partial(show_clip_view, self.application)])
        self._settings_modes.add_mode(u'note_settings', [self.settings,
         self._update_note_infos,
         self._mode_selector,
         partial(self._set_envelope_view_visible, False),
         partial(show_clip_view, self.application)])
        self._settings_modes.selected_mode = u'note_settings'
        self.__on_selected_setting_mode_changed.subject = self._settings_modes
        self.add_mode(u'disabled', [])
        self.add_mode(u'about_to_show', [AddLayerMode(self, initial_encoder_layer), (self._show_settings_task.restart, self._show_settings_task.kill)])
        self.add_mode(u'enabled', [DetailViewRestorerMode(self.application), AddLayerMode(self, encoder_layer), self._settings_modes])
        self.selected_mode = u'disabled'
        self._editors = []
        self._on_detail_clip_changed.subject = self.song.view
        self._on_selected_track_changed.subject = self.song.view
        self.__on_full_velocity_changed.subject = self.settings
        self.__on_setting_changed.subject = self.settings

    automation_layer = forward_property(u'automation')(u'layer')
    mode_selector_layer = forward_property(u'_mode_selector')(u'layer')
    selected_setting = forward_property(u'_settings_modes')(u'selected_mode')

    @property
    def step_settings(self):
        return self._settings_modes

    @property
    def editors(self):
        return self._editors

    @listenable_property
    def is_touched(self):
        return any(map(lambda e: e and e.is_touched, filter(lambda e: self._can_notify_is_touched(e), self.encoders)))

    def _is_step_held(self):
        return len(self._active_note_regions()) > 0

    def add_editor(self, editor):
        assert editor != None
        self._editors.append(editor)
        self._on_active_note_regions_changed.add_subject(editor)
        self._on_notes_changed.replace_subjects(self._editors)
        self.__on_modify_all_notes_changed.add_subject(editor)

    def set_encoders(self, encoders):
        self.encoders.set_control_element(encoders)
        self.settings.set_encoder_controls(encoders)
        self.automation.set_parameter_controls(encoders)

    @property
    def parameter_provider(self):
        self.automation.parameter_provider

    @parameter_provider.setter
    def parameter_provider(self, value):
        self.automation.parameter_provider = value

    @listens(u'selected_mode')
    def __on_selected_setting_mode_changed(self, mode):
        if mode == u'automation':
            self.automation.selected_time = self._active_note_regions()

    def update_view_state_based_on_selected_setting(self, setting):
        if self.selected_mode == u'enabled' and self.is_touched or setting is None:
            self._set_settings_view_enabled(False)
        elif self._is_step_held():
            if self.selected_setting == u'automation' and self.automation.can_automate_parameters or self.selected_setting == u'note_settings':
                self._show_settings()

    @listens(u'full_velocity')
    def __on_full_velocity_changed(self):
        for editor in self._editors:
            editor.set_full_velocity()

    @listens(u'setting_changed')
    def __on_setting_changed(self, index, value):
        for editor in self._editors:
            self._modify_note_property_offset(editor, index, value)

    def _modify_note_property_offset(self, editor, index, value):
        if index == 1:
            editor.set_nudge_offset(value)
        elif index == 2:
            editor.set_length_offset(value)
        elif index == 3:
            editor.set_velocity_offset(value)
        elif index == 4:
            editor.set_velocity_deviation_offset(value)
        elif index == 5:
            editor.set_probability_offset(value)

    def _set_envelope_view_visible(self, visible):
        clip = self.song.view.detail_clip
        if liveobj_valid(clip):
            if visible:
                clip.view.show_envelope()
            else:
                clip.view.hide_envelope()

    def _set_settings_view_enabled(self, should_show_view):
        really_show_view = should_show_view and self.automation.can_automate_parameters if self.selected_setting == u'automation' else should_show_view
        if really_show_view:
            if self.selected_mode == u'disabled':
                self.selected_mode = u'about_to_show'
        else:
            self._hide_settings()

    def _active_note_regions(self):
        all_active_regions = list(map(lambda e: e.active_note_regions, self._editors))
        return list(set(chain.from_iterable(all_active_regions)))

    @listens_group(u'active_note_regions')
    def _on_active_note_regions_changed(self, _):
        if self.is_enabled():
            all_steps = self._active_note_regions()
            self.automation.selected_time = all_steps
            self._update_note_infos()
            self._set_settings_view_enabled(len(all_steps) > 0 and self.selected_setting != None or self.is_touched)

    @listens_group(u'modify_all_notes')
    def __on_modify_all_notes_changed(self, editor):
        self.selected_mode = u'about_to_show' if editor.modify_all_notes_enabled else u'disabled'

    @listens_group(u'notes_changed')
    def _on_notes_changed(self, editor):
        self._update_infos_task.restart()

    @listens(u'detail_clip')
    def _on_detail_clip_changed(self):
        self.automation.clip = self.song.view.detail_clip if self.is_enabled() else None

    @listens(u'selected_track')
    def _on_selected_track_changed(self):
        self.selected_mode = u'disabled'

    @initial_encoders.touched
    def initial_encoders(self, encoder):
        if self.selected_mode == u'about_to_show':
            self._show_settings()

    @initial_encoders.value
    def initial_encoders(self, encoder, value):
        if self.selected_mode == u'about_to_show':
            self._show_settings()

    @encoders.touched
    def encoders(self, encoder):
        if self._can_notify_is_touched(encoder):
            self.notify_is_touched()

    @encoders.released
    def encoders(self, encoder):
        if not self.is_touched and not self._is_step_held() and not self._is_edit_all_notes_active():
            self._hide_settings()
        if self._can_notify_is_touched(encoder):
            self.notify_is_touched()

    @encoders.value
    def encoders(self, encoder, value):
        self._notify_modification()

    def _can_notify_is_touched(self, encoder):
        if self.is_enabled():
            return self._settings_modes.selected_mode != u'note_settings' or encoder.index < self.settings.number_of_settings
        return False

    def _is_edit_all_notes_active(self):
        return find_if(lambda e: e.modify_all_notes_enabled, self._editors) != None

    def _notify_modification(self):
        for editor in self._editors:
            editor.notify_modification()

    def _update_note_infos(self):
        if self.settings.is_enabled():

            def min_max(l_min_max, r_min_max):
                l_min, l_max = l_min_max
                r_min, r_max = r_min_max
                return (min(l_min, r_min), max(l_max, r_max))

            all_min_max_attributes = [ _f for _f in map(lambda e: e.get_min_max_note_values(), self._editors) if _f ]
            min_max_values = [(99999, -99999)] * self.settings.number_of_settings if len(all_min_max_attributes) > 0 else None
            for min_max_attribute in all_min_max_attributes:
                for i, attribute in enumerate(min_max_attribute[:self.settings.number_of_settings]):
                    min_max_values[i] = min_max(min_max_values[i], attribute)

            for i in range(self.settings.number_of_settings):
                self.settings.set_min_max(i, min_max_values[i] if min_max_values else None)

            self.settings.set_info_message(u'Tweak to add note' if not self._is_edit_all_notes_active() and not min_max_values else u'')

    def _show_settings(self):
        if self.selected_mode != u'enabled':
            self.selected_mode = u'enabled'
            self._notify_modification()

    def _hide_settings(self):
        self.selected_mode = u'disabled'

    def on_enabled_changed(self):
        super(NoteEditorSettingsComponent, self).on_enabled_changed()
        if not self.is_enabled():
            self.selected_mode = u'disabled'

    def update(self):
        super(NoteEditorSettingsComponent, self).update()
        if self.is_enabled():
            self._on_detail_clip_changed()
