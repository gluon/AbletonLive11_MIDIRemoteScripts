#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/push2.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from builtins import object
from contextlib import contextmanager
from functools import partial
import json
import logging
import weakref
import Live
import MidiRemoteScript
from ableton.v2.base import const, inject, listens, listens_group, task, OutermostOnlyContext, EventObject, NamedTuple
from ableton.v2.control_surface import BackgroundLayer, Component, IdentifiableControlSurface, Layer, get_element, find_instrument_meeting_requirement
from ableton.v2.control_surface.components import DeviceParameterComponent
from ableton.v2.control_surface.defaults import TIMER_DELAY
from ableton.v2.control_surface.elements import ButtonMatrixElement, ComboElement, SysexElement
from ableton.v2.control_surface.mode import EnablingModesComponent, LayerMode, ModesComponent, LazyEnablingMode, ReenterBehaviour, SetAttributeMode
from pushbase.actions import select_clip_and_get_name_from_slot, select_scene_and_get_name
from pushbase.pad_sensitivity import PadUpdateComponent
from pushbase.quantization_component import QUANTIZATION_NAMES_UNICODE, QuantizationComponent, QuantizationSettingsComponent
from pushbase.selection import PushSelection
from pushbase import consts
from pushbase.push_base import PushBase, NUM_TRACKS, NUM_SCENES
from pushbase.track_frozen_mode import TrackFrozenModesComponent
from pushbase.messenger_mode_component import MessengerModesComponent
from pushbase.undo_step_handler import UndoStepHandler
from . import sysex
from .actions import CaptureAndInsertSceneComponent
from .automation import AutomationComponent
from .elements import Elements
from .browser_component import BrowserComponent, NewTrackBrowserComponent
from .browser_modes import AddDeviceMode, AddTrackMode, BrowseMode, BrowserComponentMode, BrowserModeBehaviour
from .color_chooser import ColorChooserComponent
from .device_decorator_factory import DeviceDecoratorFactory
from .skin_default import make_default_skin
from .mute_solo_stop import MuteSoloStopClipComponent
from .device_component import Push2DeviceProvider
from .device_component_provider import DeviceComponentProvider
from .device_view_component import DeviceViewComponent
from .device_navigation import is_empty_rack, DeviceNavigationComponent
from .drum_group_component import DrumGroupComponent
from .drum_pad_parameter_component import DrumPadParameterComponent
from .clip_control import ClipControlComponent, MatrixModeWatcherComponent, register_matrix_mode
from .clip_decoration import ClipDecoratorFactory
from .colors import COLOR_TABLE
from .convert import ConvertComponent, ConvertEnabler
from .firmware import FirmwareCollector, FirmwareUpdateComponent, FirmwareSwitcher, FirmwareVersion
from .hardware_settings_component import HardwareSettingsComponent
from .master_track import MasterTrackComponent
from .mixer_control_component import MixerControlComponent
from .note_editor import Push2NoteEditorComponent
from .note_settings import NoteSettingsComponent
from .notification_component import NotificationComponent
from .pad_sensitivity import default_profile, loop_selector_profile, MONO_AFTERTOUCH_DISABLED, MONO_AFTERTOUCH_ENABLED, pad_parameter_sender, PadSettings, playing_profile
from .pad_velocity_curve import PadVelocityCurveSender
from .routing import RoutingControlComponent, TrackOrRoutingControlChooserComponent
from .scales_component import ScalesComponent, ScalesEnabler
from .selected_track_parameter_provider import SelectedTrackParameterProvider
from .session_component import DecoratingCopyHandler, SessionComponent
from .session_ring_selection_linking import SessionRingSelectionLinking
from .settings import create_settings
from .sliced_simpler import Push2SlicedSimplerComponent
from .track_mixer_control_component import TrackMixerControlComponent
from .mode_collector import ModeCollector
from .real_time_channel import update_real_time_attachments
from .simple_mode_switcher import SimpleModeSwitcher
from .setup_component import SetupComponent, Settings
from .track_list import TrackListComponent
from .track_selection import SessionRingTrackProvider, ViewControlComponent
from .transport_state import TransportState
from .user_component import UserButtonBehavior, UserComponent
from .custom_bank_definitions import BANK_DEFINITIONS
from .visualisation_settings import VisualisationSettings
logger = logging.getLogger(__name__)
VELOCITY_RANGE_THRESHOLDS = [120, 60, 0]

class QmlError(Exception):
    pass


def make_dialog_layer(priority = consts.DIALOG_PRIORITY, *a, **k):
    return (BackgroundLayer(u'global_param_controls', u'select_buttons', u'track_state_buttons', priority=priority), Layer(priority=priority, *a, **k))


def tracks_to_use_from_song(song):
    return tuple(song.visible_tracks) + tuple(song.return_tracks)


def wrap_button(select_buttons, modifier):
    return [ ComboElement(button, modifier=modifier) for button in get_element(select_buttons) ]


def make_freeze_aware(component, layer, default_mode_extras = [], frozen_mode_extras = []):
    return TrackFrozenModesComponent(default_mode=[component, LayerMode(component, layer)] + default_mode_extras, frozen_mode=[component, LayerMode(component, Layer())] + frozen_mode_extras, is_enabled=False)


class RealTimeClientModel(EventObject):
    __events__ = (u'clientId',)

    def __init__(self):
        self._client_id = u''

    def _get_client_id(self):
        return self._client_id

    def _set_client_id(self, client_id):
        self._client_id = client_id
        self.notify_clientId()

    clientId = property(_get_client_id, _set_client_id)


class Push2(IdentifiableControlSurface, PushBase):
    drum_group_note_editor_skin = u'DrumGroupNoteEditor'
    slicing_note_editor_skin = u'SlicingNoteEditor'
    drum_group_velocity_levels_skin = u'DrumGroupVelocityLevels'
    slicing_velocity_levels_skin = u'VelocityLevels'
    note_layout_button = u'layout_button'
    input_target_name_for_auto_arm = u'Push2 Input'
    note_editor_velocity_range_thresholds = VELOCITY_RANGE_THRESHOLDS
    device_provider_class = Push2DeviceProvider
    selected_track_parameter_provider_class = SelectedTrackParameterProvider
    bank_definitions = BANK_DEFINITIONS
    note_editor_class = Push2NoteEditorComponent
    sliced_simpler_class = Push2SlicedSimplerComponent
    quantization_settings_class = QuantizationSettingsComponent
    note_settings_component_class = NoteSettingsComponent
    automation_component_class = AutomationComponent
    RESEND_MODEL_DATA_TIMEOUT = 5.0
    DEFUNCT_EXTERNAL_PROCESS_RELAUNCH_TIMEOUT = 2.0

    def __init__(self, c_instance = None, model = None, bank_definitions = None, decoupled_parameter_list_change_notifications = False, *a, **k):
        assert model is not None
        self._device_component = None
        self._decoupled_parameter_list_change_notifications = decoupled_parameter_list_change_notifications
        self._model = model
        self._real_time_mapper = c_instance.real_time_mapper
        self._clip_decorator_factory = ClipDecoratorFactory()
        self._real_time_data_list = []
        self._matrix_mode_map = {}
        if bank_definitions is not None:
            self.bank_definitions = bank_definitions
        self._changing_track_context = OutermostOnlyContext()
        super(Push2, self).__init__(c_instance=c_instance, product_id_bytes=sysex.IDENTITY_RESPONSE_PRODUCT_ID_BYTES, *a, **k)
        self._board_revision = 0
        self._firmware_collector = FirmwareCollector()
        self._firmware_version = FirmwareVersion(0, 0, 0)
        self._real_time_client = RealTimeClientModel()
        self._connected = False
        self._identified = False
        self._initialized = False
        self.register_disconnectable(model)
        self.register_disconnectable(self._clip_decorator_factory)
        with self.component_guard():
            self._model.realTimeClient = self._real_time_client
            self._real_time_client.clientId = self._real_time_mapper.client_id
        logger.info(u'Push 2 script loaded')

    def initialize(self):
        if not self._initialized:
            self._initialized = True
            self._init_hardware_settings()
            self._init_pad_curve()
            self._init_visualisation_settings()
            self._hardware_settings.hardware_initialized()
            self._pad_curve_sender.send()
            self._send_color_palette()
            super(Push2, self).initialize()
            self._init_transport_state()
            self.__on_selected_track_frozen_changed.subject = self.song.view
            self.__on_selected_track_frozen_changed()
            self._switch_to_live_mode()
            self.update()
        latest_stable_firmware = self._firmware_collector.latest_stable_firmware
        if latest_stable_firmware is not None and latest_stable_firmware.version > self._firmware_version and self._board_revision > 0 and self._identified:
            self._firmware_update.start(latest_stable_firmware)

    def _try_initialize(self):
        if self._connected and self._identified:
            self.initialize()

    def on_process_state_changed(self, state):
        logger.debug(u'Process state changed %r' % state)
        StateEnum = MidiRemoteScript.Push2ProcessState
        self._connected = state == StateEnum.connected
        if state == StateEnum.died:
            if self._initialized:
                self._setup_component.make_it_go_boom = False
            self._c_instance.launch_external_process()
        elif state == StateEnum.connected:
            with self.component_guard():
                self._try_initialize()
            self._model.commit_changes(send_all=True)
        elif state in (StateEnum.defunct_process_terminated, StateEnum.defunct_process_killed):
            self._tasks.add(task.sequence(task.wait(self.DEFUNCT_EXTERNAL_PROCESS_RELAUNCH_TIMEOUT), task.run(self._c_instance.launch_external_process)))

    def on_user_data_arrived(self, message):
        if self._initialized:
            logger.debug(u'User data arrived %r' % message)
            data = json.loads(message)
            self._process_qml_errors(data)
            self._firmware_update.process_firmware_response(data)

    def _process_qml_errors(self, data):
        qmlerrors = [ entry for entry in data if entry[u'type'] == u'qmlerror' ]
        if qmlerrors:
            first_error = qmlerrors[0]
            line = first_error[u'line']
            url = first_error[u'url']
            description = first_error[u'description'].replace(u'"', u'\\"')
            code = u'\n' * (line - 1) + u'raise QmlError("%s")' % description
            exec compile(code, url, u'exec')

    def disconnect(self):
        super(Push2, self).disconnect()
        self.__dict__.clear()
        logger.info(u'Push 2 script unloaded')

    def register_real_time_data(self, real_time_data):
        self._real_time_data_list.append(real_time_data)

    def _commit_real_time_data_changes(self):
        update_real_time_attachments(self._real_time_data_list)

    def _create_device_decorator_factory(self):
        return DeviceDecoratorFactory()

    def _create_skin(self):
        return self.register_disconnectable(make_default_skin())

    def _create_injector(self):
        return inject(double_press_context=const(self._double_press_context), expect_dialog=const(self.expect_dialog), show_notification=const(self.show_notification), commit_model_changes=const(self._model.commit_changes), register_real_time_data=const(self.register_real_time_data), percussion_instrument_finder=const(self._percussion_instrument_finder), selection=lambda : PushSelection(application=self.application, device_component=self._device_component, navigation_component=self._device_navigation), external_regions_of_interest_creator=lambda : self._clip_control.midi_clip_controller.external_regions_of_interest_creator, external_focusable_object_descriptions=lambda : self._clip_control.midi_clip_controller.external_focusable_object_descriptions)

    def _create_components(self):
        self._init_dialog_modes()
        self._init_clip_control()
        super(Push2, self)._create_components()
        self._init_browser()
        self._init_session_ring_selection_linking()
        self._init_firmware_update()
        self._init_setup_component()
        self._init_convert_enabler()
        self._init_mute_solo_stop()
        self._init_matrix_mode_watcher()

    @contextmanager
    def _component_guard(self):
        with super(Push2, self)._component_guard():
            with inject(real_time_mapper=const(self._c_instance.real_time_mapper)).everywhere():
                yield
                self._commit_real_time_data_changes()
                self._model.commit_changes()

    def _create_notification_component(self):
        notification = NotificationComponent()
        self._model.notificationView = notification
        return notification

    def _create_background_layer(self):
        return super(Push2, self)._create_background_layer() + Layer(mix_button=u'mix_button', page_left_button=u'page_left_button', page_right_button=u'page_right_button', mute_button=u'global_mute_button', solo_button=u'global_solo_button', track_stop_button=u'global_track_stop_button', convert_button=u'convert_button', layout_button=u'layout_button', setup_button=u'setup_button')

    def _create_message_box_background_layer(self):
        return super(Push2, self)._create_message_box_background_layer() + BackgroundLayer(u'mix_button', u'page_left_button', u'page_right_button', u'convert_button', u'layout_button', u'setup_button')

    def _create_message_box_layer(self):
        return Layer(cancel_button=u'track_state_buttons_raw[0]', priority=consts.MESSAGE_BOX_PRIORITY)

    def _create_note_settings_component_layer(self):
        return Layer(full_velocity_button=u'accent_button', priority=consts.MOMENTARY_DIALOG_PRIORITY)

    def _init_message_box(self):
        super(Push2, self)._init_message_box()
        self._model.liveDialogView = self._dialog._message_box

    def _create_convert(self):
        convert = ConvertComponent(decorator_factory=self._device_decorator_factory, name=u'Convert', tracks_provider=self._session_ring, is_enabled=False, layer=make_dialog_layer(action_buttons=u'select_buttons', cancel_button=u'track_state_buttons_raw[0]'))
        self.__on_convert_closed.subject = convert
        self.__on_convert_suceeded.subject = convert
        self._model.convertView = convert
        return convert

    def _select_note_mode(self):
        super(Push2, self)._select_note_mode()
        self._note_editor_settings_component.settings.set_color_mode(u'drum_pad' if self._note_modes.selected_mode == u'drums' else u'clip')

    def _init_note_editor_settings_component(self):
        super(Push2, self)._init_note_editor_settings_component()
        self._model.stepSettingsView = self._note_editor_settings_component.step_settings
        self._model.noteSettingsView = self._note_editor_settings_component.settings
        self._model.stepAutomationSettingsView = self._note_editor_settings_component.automation

    def _init_convert_enabler(self):
        self._convert_enabler = ConvertEnabler(is_enabled=True, enter_dialog_mode=self._enter_dialog_mode, exit_dialog_mode=self._exit_dialog_mode)
        self._convert_enabler.layer = Layer(convert_toggle_button=u'convert_button')

    def _register_matrix_mode(self, name, modes_component = None, parent_path = None):
        register_matrix_mode(self._matrix_mode_map, name, modes_component, parent_path)

    def _init_matrix_mode_watcher(self):
        self._matrix_mode_watcher = MatrixModeWatcherComponent(matrix_mode_map=self._matrix_mode_map)

    @listens(u'cancel')
    def __on_convert_closed(self):
        self._dialog_modes.selected_mode = None

    @listens(u'success')
    def __on_convert_suceeded(self, action_name):
        if action_name == u'audio_clip_to_simpler':
            self._main_modes.selected_mode = u'device'

    def _automateable_main_modes(self):
        return (u'device', u'mix')

    def _init_main_modes(self):
        super(Push2, self)._init_main_modes()
        self._main_modes.add_mode(u'user', [self._user_mode_ui_blocker, SetAttributeMode(obj=self._user, attribute=u'mode', value=sysex.USER_MODE)], behaviour=UserButtonBehavior(user_component=self._user))
        self._model.modeState = self.register_disconnectable(ModeCollector(main_modes=self._main_modes, mix_modes=self._mix_modes, global_mix_modes=self._mixer_control, device_modes=self._device_navigation.modes))
        self.__on_main_mode_button_value.replace_subjects([self.elements.vol_mix_mode_button,
         self.elements.pan_send_mix_mode_button,
         self.elements.single_track_mix_mode_button,
         self.elements.clip_mode_button,
         self.elements.device_mode_button,
         self.elements.browse_mode_button,
         self.elements.create_device_button,
         self.elements.create_track_button])

    @listens_group(u'value')
    def __on_main_mode_button_value(self, value, sender):
        if not value:
            self._exit_modal_modes()

    def _exit_modal_modes(self):
        self._dialog_modes.selected_mode = None
        self._setup_enabler.selected_mode = u'disabled'

    def _create_capture_and_insert_scene_component(self):
        return CaptureAndInsertSceneComponent(name=u'Capture_And_Insert_Scene', decorator_factory=self._clip_decorator_factory)

    def _init_mute_solo_stop(self):
        self._mute_solo_stop = MuteSoloStopClipComponent(item_provider=self._session_ring, track_list_component=self._track_list_component, cancellation_action_performers=[self._device_navigation, self._drum_component] + self._note_editor_settings_component.editors, solo_track_button=u'global_solo_button', mute_track_button=u'global_mute_button', stop_clips_button=u'global_track_stop_button')
        self._mute_solo_stop.layer = Layer(stop_all_clips_button=self._with_shift(u'global_track_stop_button'))
        self._master_selector = MasterTrackComponent(tracks_provider=self._session_ring, is_enabled=False, layer=Layer(toggle_button=u'master_select_button'))
        self._master_selector.set_enabled(True)

    def _create_sequence_instrument_layer(self):
        return super(Push2, self)._create_sequence_instrument_layer() + self._create_loop_navigation_layer()

    def _create_sequence_instrument_layer_with_loop(self):
        return super(Push2, self)._create_sequence_instrument_layer_with_loop() + self._create_loop_navigation_layer()

    def _create_play_instrument_with_loop_layer(self):
        return super(Push2, self)._create_play_instrument_with_loop_layer() + self._create_loop_navigation_layer()

    def _create_drum_step_sequencer_layer(self):
        return super(Push2, self)._create_drum_step_sequencer_layer() + self._create_loop_navigation_layer()

    def _create_slicing_step_sequencer_layer(self):
        return super(Push2, self)._create_slicing_step_sequencer_layer() + self._create_loop_navigation_layer()

    def _create_split_seq_layer(self):
        return super(Push2, self)._create_split_seq_layer() + self._create_loop_navigation_layer()

    def _create_loop_navigation_layer(self):
        return Layer(prev_loop_page_button=u'page_left_button', next_loop_page_button=u'page_right_button')

    def _create_color_chooser(self):
        color_chooser = ColorChooserComponent()
        color_chooser.layer = Layer(matrix=u'matrix', priority=consts.MOMENTARY_DIALOG_PRIORITY)
        return color_chooser

    def _create_session(self):
        session = super(Push2, self)._create_session()
        for scene_ix in range(8):
            scene = session.scene(scene_ix)
            for track_ix in range(8):
                clip_slot = scene.clip_slot(track_ix)
                clip_slot.layer += Layer(select_color_button=u'shift_button')
                clip_slot.set_decorator_factory(self._clip_decorator_factory)

        return session

    def _create_session_navigation_layer(self):
        return Layer(left_button=u'nav_left_button', right_button=u'nav_right_button', up_button=u'nav_up_button', down_button=u'nav_down_button', page_left_button=u'page_left_button', page_right_button=u'page_right_button', page_up_button=u'octave_up_button', page_down_button=u'octave_down_button')

    def on_select_clip_slot(self, clip_slot):
        self.show_notification(u'Clip Selected: ' + select_clip_and_get_name_from_slot(clip_slot, self.song))

    def on_select_scene(self, scene):
        self.show_notification(u'Scene Selected: ' + select_scene_and_get_name(scene, self.song))

    def _create_session_mode(self):
        session_modes = MessengerModesComponent(muted=True, is_enabled=False)
        session_modes.add_mode(u'session', [self._session_mode], message=consts.MessageBoxText.LAYOUT_SESSION_VIEW)
        session_modes.add_mode(u'overview', [self._session_overview_mode], message=consts.MessageBoxText.LAYOUT_SESSION_OVERVIEW)
        session_modes.selected_mode = u'session'
        simple_mode_switcher = SimpleModeSwitcher(session_modes, is_enabled=False, layer=Layer(cycle_button=self.note_layout_button, lock_button=ComboElement(self.note_layout_button, modifier=u'shift_button')))
        return [session_modes, self._session_navigation, simple_mode_switcher]

    def _create_session_overview_layer(self):
        return Layer(button_matrix=u'matrix')

    def _instantiate_session(self):
        return SessionComponent(session_ring=self._session_ring, is_enabled=False, auto_name=True, clip_slot_copy_handler=DecoratingCopyHandler(decorator_factory=self._clip_decorator_factory), fixed_length_recording=self._create_fixed_length_recording(), color_chooser=self._create_color_chooser(), layer=self._create_session_layer())

    def _create_drum_component(self):
        return DrumGroupComponent(name=u'Drum_Group', is_enabled=False, tracks_provider=self._session_ring, device_decorator_factory=self._device_decorator_factory, quantizer=self._quantize, color_chooser=self._create_color_chooser())

    def _init_drum_component(self):
        super(Push2, self)._init_drum_component()
        self._drum_component.layer += Layer(select_color_button=u'shift_button')

    def _create_device_mode(self):
        self._model.deviceVisualisation = self._device_component
        self._drum_pad_parameter_component = DrumPadParameterComponent(device_component=self._device_component, view_model=self._model, is_enabled=False, layer=Layer(choke_encoder=u'parameter_controls_raw[0]', transpose_encoder=u'parameter_controls_raw[1]'))
        self._device_or_pad_parameter_chooser = ModesComponent()
        self._device_or_pad_parameter_chooser.add_mode(u'device', [make_freeze_aware(self._device_parameter_component, self._device_parameter_component.layer), self._device_view])
        self._device_or_pad_parameter_chooser.add_mode(u'drum_pad', [make_freeze_aware(self._drum_pad_parameter_component, self._drum_pad_parameter_component.layer)])
        self._device_or_pad_parameter_chooser.selected_mode = u'device'
        return [partial(self._view_control.show_view, u'Detail/DeviceChain'),
         self._device_component,
         self._device_or_pad_parameter_chooser,
         self._setup_freeze_aware_device_navigation(),
         self._device_note_editor_mode,
         SetAttributeMode(obj=self._note_editor_settings_component, attribute=u'parameter_provider', value=self._device_component),
         self._clip_phase_enabler]

    def _setup_freeze_aware_device_navigation(self):

        def create_layer_setter(layer_name, layer):
            return SetAttributeMode(obj=self._device_navigation, attribute=layer_name, value=layer)

        return make_freeze_aware(self._device_navigation, self._device_navigation.layer, default_mode_extras=[create_layer_setter(u'scroll_right_layer', Layer(button=self.elements.track_state_buttons_raw[-1])), create_layer_setter(u'scroll_left_layer', Layer(button=self.elements.track_state_buttons_raw[0]))], frozen_mode_extras=[lambda : setattr(self._device_navigation.modes, u'selected_mode', u'default'), create_layer_setter(u'scroll_right_layer', Layer()), create_layer_setter(u'scroll_left_layer', Layer())])

    @listens(u'drum_pad_selection')
    def __on_drum_pad_selection_changed(self):
        show_pad_parameters = self._device_navigation.is_drum_pad_selected and self._device_navigation.is_drum_pad_unfolded
        new_mode = u'drum_pad' if show_pad_parameters else u'device'
        if show_pad_parameters:
            selected_pad = self._device_navigation.item_provider.selected_item
            self._drum_pad_parameter_component.drum_pad = selected_pad
        self._device_or_pad_parameter_chooser.selected_mode = new_mode
        self._note_editor_settings_component.automation.set_drum_pad_selected(self._device_navigation.is_drum_pad_selected)
        self._device_component.set_drum_pad_selected(self._device_navigation.is_drum_pad_selected)

    def _init_browser(self):
        self._browser_component_mode = BrowserComponentMode(weakref.ref(self._model), self._create_browser)
        self._new_track_browser_component_mode = BrowserComponentMode(weakref.ref(self._model), self._create_new_track_browser)

    def _init_browse_mode(self):
        application = Live.Application.get_application()
        browser = application.browser
        self._main_modes.add_mode(u'browse', [BrowseMode(application=application, song=self.song, browser=browser, drum_group_component=self._drum_component, enabling_mode=self._browser_component_mode)], behaviour=BrowserModeBehaviour())
        self._main_modes.add_mode(u'add_device', [AddDeviceMode(application=application, song=self.song, browser=browser, drum_group_component=self._drum_component, enabling_mode=self._browser_component_mode)], behaviour=BrowserModeBehaviour())
        self._main_modes.add_mode(u'add_track', [AddTrackMode(browser=browser, enabling_mode=self._new_track_browser_component_mode)], behaviour=BrowserModeBehaviour())

    def _create_browser_layer(self):
        return (BackgroundLayer(u'select_buttons', u'track_state_buttons', priority=consts.DIALOG_PRIORITY), Layer(up_button=u'nav_up_button', down_button=u'nav_down_button', right_button=u'nav_right_button', left_button=u'nav_left_button', back_button=u'track_state_buttons_raw[-2]', open_button=u'track_state_buttons_raw[-1]', load_button=u'select_buttons_raw[-1]', scroll_encoders=self.elements.global_param_controls.submatrix[:-1, :], scroll_focused_encoder=u'parameter_controls_raw[-1]', close_button=u'track_state_buttons_raw[0]', prehear_button=u'track_state_buttons_raw[1]', priority=consts.DIALOG_PRIORITY))

    def _create_browser(self):
        browser = BrowserComponent(name=u'Browser', is_enabled=False, preferences=self.preferences, main_modes_ref=weakref.ref(self._main_modes), layer=self._create_browser_layer())
        self._on_browser_loaded.add_subject(browser)
        self._on_browser_closed.add_subject(browser)
        browser.load_neighbour_overlay.layer = Layer(load_previous_button=u'track_state_buttons_raw[7]', load_next_button=u'select_buttons_raw[7]', priority=consts.DIALOG_PRIORITY)
        return browser

    def _create_new_track_browser(self):
        browser = NewTrackBrowserComponent(name=u'NewTrackBrowser', is_enabled=False, preferences=self.preferences, layer=self._create_browser_layer())
        self._on_browser_loaded.add_subject(browser)
        self._on_browser_closed.add_subject(browser)
        return browser

    @listens_group(u'loaded')
    def _on_browser_loaded(self, sender):
        if sender.browse_for_audio_clip:
            self._main_modes.selected_mode = u'clip'
        else:
            browser = Live.Application.get_application().browser
            if browser.hotswap_target is None:
                self._main_modes.selected_mode = u'device'
            drum_rack = find_instrument_meeting_requirement(lambda i: i.can_have_drum_pads, self.song.view.selected_track)
            if drum_rack and is_empty_rack(drum_rack):
                self._device_navigation.request_drum_pad_selection()
            if drum_rack and self._device_navigation.is_drum_pad_selected:
                if not self._device_navigation.is_drum_pad_unfolded:
                    self._device_navigation.unfold_current_drum_pad()
                self._device_navigation.sync_selection_to_selected_device()

    @listens_group(u'close')
    def _on_browser_closed(self, sender):
        if sender.browse_for_audio_clip:
            self._main_modes.selected_mode = u'clip'
        elif self._main_modes.selected_mode == u'add_track':
            self._main_modes.selected_mode = self._main_modes.active_modes[0]
        else:
            self._main_modes.selected_mode = u'device'

    def _is_on_master(self):
        return self.song.view.selected_track == self.song.master_track

    def _determine_mix_mode(self):
        selected_mode = self._main_modes.selected_mode
        mix_mode = self._mix_modes.selected_mode
        if selected_mode == u'mix':
            if self._is_on_master():
                if mix_mode == u'global':
                    self._mix_modes.push_mode(u'track')
            elif mix_mode == u'track' and u'global' in self._mix_modes.active_modes:
                self._mix_modes.pop_mode(u'track')

    def _on_selected_track_changed(self):
        if self._initialized:
            with self._changing_track_context(self._clip_control.midi_clip_controller.changing_track()):
                super(Push2, self)._on_selected_track_changed()
            self._close_browse_mode()
            self._determine_mix_mode()

    def _close_browse_mode(self):
        selected_mode = self._main_modes.selected_mode
        if selected_mode in (u'browse', u'add_device', u'add_track'):
            self._main_modes.pop_mode(selected_mode)

    @listens(u'selected_track.is_frozen')
    def __on_selected_track_frozen_changed(self):
        frozen = self.song.view.selected_track.is_frozen
        self._main_modes.browse_button.enabled = self._main_modes.add_device_button.enabled = not frozen
        self._close_browse_mode()

    def _create_device_component(self):
        device_component_layer = Layer(parameter_touch_buttons=ButtonMatrixElement(rows=[self.elements.global_param_touch_buttons_raw]), shift_button=u'shift_button')
        return DeviceComponentProvider(device_component_layer=device_component_layer, device_decorator_factory=self._device_decorator_factory, device_bank_registry=self._device_bank_registry, banking_info=self._banking_info, name=u'DeviceComponent', is_enabled=False, delete_button=self.elements.delete_button, decoupled_parameter_list_change_notifications=self._decoupled_parameter_list_change_notifications)

    def _create_device_parameter_component(self):
        return DeviceParameterComponent(parameter_provider=self._device_component, is_enabled=False, layer=Layer(parameter_controls=u'fine_grain_param_controls'))

    def _create_device_navigation(self):
        device_navigation = DeviceNavigationComponent(name=u'DeviceNavigation', device_bank_registry=self._device_bank_registry, banking_info=self._banking_info, device_component=self._device_component, delete_handler=self._delete_component, track_list_component=self._track_list_component, is_enabled=False, layer=Layer(select_buttons=u'track_state_buttons'))
        device_navigation.scroll_left_layer = Layer(button=u'track_state_buttons_raw[0]')
        device_navigation.scroll_right_layer = Layer(button=u'track_state_buttons_raw[-1]')
        device_navigation.move_device.layer = Layer(move_encoders=u'global_param_controls')
        device_navigation.chain_selection.layer = Layer(select_buttons=u'select_buttons', priority=consts.DIALOG_PRIORITY)
        device_navigation.chain_selection.scroll_left_layer = Layer(button=u'select_buttons_raw[0]', priority=consts.DIALOG_PRIORITY)
        device_navigation.chain_selection.scroll_right_layer = Layer(button=u'select_buttons_raw[-1]', priority=consts.DIALOG_PRIORITY)
        device_navigation.bank_selection.layer = Layer(option_buttons=u'track_state_buttons', select_buttons=u'select_buttons', priority=consts.DIALOG_PRIORITY)
        device_navigation.bank_selection.scroll_left_layer = Layer(button=u'select_buttons_raw[0]', priority=consts.DIALOG_PRIORITY)
        device_navigation.bank_selection.scroll_right_layer = Layer(button=u'select_buttons_raw[-1]', priority=consts.DIALOG_PRIORITY)
        self.__on_drum_pad_selection_changed.subject = device_navigation
        self.device_provider.allow_update_callback = lambda : device_navigation.device_selection_update_allowed
        return device_navigation

    def _init_device(self):
        super(Push2, self)._init_device()
        self._device_view = DeviceViewComponent(name=u'DeviceView', device_component=self._device_component, view_model=self._model, is_enabled=False)
        self._model.devicelistView = self._device_navigation
        self._model.chainListView = self._device_navigation.chain_selection
        self._model.parameterBankListView = self._device_navigation.bank_selection
        self._model.editModeOptionsView = self._device_navigation.bank_selection.options

    def _create_view_control_component(self):
        return ViewControlComponent(name=u'View_Control', tracks_provider=self._session_ring)

    def _init_session_ring(self):
        self._session_ring = SessionRingTrackProvider(name=u'Session_Ring', num_tracks=NUM_TRACKS, num_scenes=NUM_SCENES, is_enabled=True)

    def _init_session_ring_selection_linking(self):
        self._sessionring_link = self.register_disconnectable(SessionRingSelectionLinking(session_ring=self._session_ring, selection_changed_notifier=self._view_control))

    def _init_track_list(self):
        self._track_list_component = TrackListComponent(tracks_provider=self._session_ring, trigger_recording_on_release_callback=self._session_recording.set_trigger_recording_on_release, color_chooser=self._create_color_chooser(), is_enabled=False, layer=Layer(track_action_buttons=u'select_buttons', lock_override_button=u'select_button', delete_button=u'delete_button', duplicate_button=u'duplicate_button', arm_button=u'record_button', select_color_button=u'shift_button'))
        self._clip_phase_enabler = self._track_list_component.clip_phase_enabler
        self._track_list_component.set_enabled(True)
        self._model.tracklistView = self._track_list_component

    def _create_main_mixer_modes(self):
        self._mixer_control = MixerControlComponent(name=u'Global_Mix_Component', view_model=self._model.mixerView, tracks_provider=self._session_ring, is_enabled=False, layer=Layer(controls=u'fine_grain_param_controls', volume_button=u'track_state_buttons_raw[0]', panning_button=u'track_state_buttons_raw[1]', send_slot_one_button=u'track_state_buttons_raw[2]', send_slot_two_button=u'track_state_buttons_raw[3]', send_slot_three_button=u'track_state_buttons_raw[4]', send_slot_four_button=u'track_state_buttons_raw[5]', send_slot_five_button=u'track_state_buttons_raw[6]', cycle_sends_button=u'track_state_buttons_raw[7]'))
        self._model.mixerView.realtimeMeterData = self._mixer_control.real_time_meter_handlers
        track_mixer_control = TrackMixerControlComponent(name=u'Track_Mix_Component', is_enabled=False, tracks_provider=self._session_ring, layer=Layer(controls=u'fine_grain_param_controls', scroll_left_button=u'track_state_buttons_raw[6]', scroll_right_button=u'track_state_buttons_raw[7]'))
        routing_control = RoutingControlComponent(is_enabled=False, layer=Layer(monitor_state_encoder=u'parameter_controls_raw[0]', input_output_choice_encoder=u'parameter_controls_raw[1]', routing_type_encoder=u'parameter_controls_raw[2]', routing_channel_encoders=self.elements.global_param_controls.submatrix[3:7, :], routing_channel_position_encoder=u'parameter_controls_raw[7]'))
        track_mix_or_routing_chooser = TrackOrRoutingControlChooserComponent(tracks_provider=self._session_ring, track_mixer_component=track_mixer_control, routing_control_component=routing_control, is_enabled=False, layer=Layer(mix_button=u'track_state_buttons_raw[0]', routing_button=u'track_state_buttons_raw[1]'))
        self._model.mixerView.trackControlView = track_mix_or_routing_chooser
        self._mix_modes = ModesComponent(is_enabled=False)
        self._mix_modes.add_mode(u'global', self._mixer_control)
        self._mix_modes.add_mode(u'track', track_mix_or_routing_chooser)
        self._mix_modes.selected_mode = u'global'
        self._model.mixerSelectView = self._mixer_control
        self._model.trackMixerSelectView = track_mixer_control

        class MixModeBehaviour(ReenterBehaviour):

            def press_immediate(behaviour_self, component, mode):
                if self._is_on_master() and self._mix_modes.selected_mode != u'track':
                    self._mix_modes.selected_mode = u'track'
                super(MixModeBehaviour, behaviour_self).press_immediate(component, mode)

            def on_reenter(behaviour_self):
                if not self._is_on_master():
                    self._mix_modes.cycle_mode()

        self._main_modes.add_mode(u'mix', [self._mix_modes, SetAttributeMode(obj=self._note_editor_settings_component, attribute=u'parameter_provider', value=self._track_parameter_provider), self._clip_phase_enabler], behaviour=MixModeBehaviour())

    def _init_dialog_modes(self):
        self._dialog_modes = ModesComponent()
        self._dialog_modes.add_mode(u'convert', LazyEnablingMode(self._create_convert))
        self.__dialog_mode_button_value.replace_subjects([self.elements.scale_presets_button, self.elements.convert_button])

    @listens_group(u'value')
    def __dialog_mode_button_value(self, value, sender):
        if not value:
            self._setup_enabler.selected_mode = u'disabled'

    def _enter_dialog_mode(self, mode_name):
        self._dialog_modes.selected_mode = None if self._dialog_modes.selected_mode == mode_name else mode_name

    def _exit_dialog_mode(self, mode_name):
        if self._dialog_modes.selected_mode == mode_name:
            self._dialog_modes.selected_mode = None

    def _create_scales(self):
        root_note_buttons = ButtonMatrixElement(rows=[self.elements.track_state_buttons_raw[1:-1], self.elements.select_buttons_raw[1:-1]])
        scales = ScalesComponent(note_layout=self._note_layout, is_enabled=False, layer=make_dialog_layer(root_note_buttons=root_note_buttons, in_key_toggle_button=u'select_buttons_raw[0]', fixed_toggle_button=u'select_buttons_raw[-1]', scale_encoders=self.elements.global_param_controls.submatrix[1:-1, :], layout_encoder=u'parameter_controls_raw[0]', direction_encoder=u'parameter_controls_raw[-1]', up_button=u'nav_up_button', down_button=u'nav_down_button', right_button=u'nav_right_button', left_button=u'nav_left_button'))
        self._model.scalesView = scales
        return scales

    def _init_scales(self):
        self._dialog_modes.add_mode(u'scales', self._create_scales())
        super(Push2, self)._init_scales()

    def _create_scales_enabler(self):
        return ScalesEnabler(enter_dialog_mode=self._enter_dialog_mode, exit_dialog_mode=self._exit_dialog_mode, is_enabled=False, layer=Layer(toggle_button=u'scale_presets_button'))

    def _init_clip_control(self):
        self._clip_control = ClipControlComponent(decorator_factory=self._clip_decorator_factory, is_enabled=False)

    def _create_clip_mode(self):
        base_loop_layer = Layer(shift_button=u'shift_button', loop_button=u'track_state_buttons_raw[1]', crop_button=u'track_state_buttons_raw[2]')
        audio_clip_layer = Layer(warp_mode_encoder=u'parameter_controls_raw[5]', transpose_encoder=u'parameter_controls_raw[6]', detune_encoder=self._with_shift(u'parameter_controls_raw[6]'), gain_encoder=u'parameter_controls_raw[7]', shift_button=u'shift_button')
        self._clip_control.mode_selector.add_mode(u'midi', [make_freeze_aware(self._clip_control.midi_loop_controller, base_loop_layer + Layer(encoders=self.elements.global_param_controls.submatrix[1:4, :], zoom_encoder=u'fine_grain_param_controls_raw[0]')), self._clip_control.midi_clip_controller])
        self._clip_control.mode_selector.add_mode(u'audio', [make_freeze_aware(self._clip_control.audio_loop_controller, base_loop_layer + Layer(encoders=self.elements.global_param_controls.submatrix[1:4, :], zoom_encoder=u'fine_grain_param_controls_raw[0]')), make_freeze_aware(self._clip_control.audio_clip_controller, audio_clip_layer)])
        self._clip_control.mode_selector.add_mode(u'no_clip', [])
        self._clip_control.mode_selector.selected_mode = u'no_clip'
        self._model.midiLoopSettingsView = self._clip_control.midi_loop_controller
        self._model.audioLoopSettingsView = self._clip_control.audio_loop_controller
        self._model.audioClipSettingsView = self._clip_control.audio_clip_controller
        self._model.midiClipSettingsView = self._clip_control.midi_clip_controller
        self._clip_control.midi_clip_controller.set_drum_rack_finder(self._percussion_instrument_finder)
        self._clip_control.midi_clip_controller.set_matrix_mode_watcher(self._matrix_mode_watcher)
        instrument_components = (self._drum_component,
         self._instrument.instrument,
         self._selected_note_instrument,
         self._slicing_component)
        for instrument_component in instrument_components:
            self._clip_control.midi_clip_controller.add_instrument_component(instrument_component)

        paginators = (self._drum_step_sequencer.paginator,
         self._instrument.paginator,
         self._split_melodic_sequencer.paginator,
         self._slicing_step_sequencer.paginator)
        for paginator in paginators:
            self._clip_control.midi_clip_controller.add_paginator(paginator)

        sequencers = (self._drum_step_sequencer,
         self._instrument,
         self._slicing_step_sequencer,
         self._split_melodic_sequencer)
        for sequencer in sequencers:
            self._clip_control.midi_clip_controller.add_sequencer(sequencer)

        self._clip_control.midi_clip_controller.set_note_settings_component(self._note_editor_settings_component.settings)
        self._clip_control.midi_clip_controller.set_note_editor_settings_component(self._note_editor_settings_component)
        self._clip_control.midi_clip_controller.add_mute_during_track_change_component(self._drum_modes)
        self._clip_control.midi_clip_controller.add_mute_during_track_change_component(self._instrument)
        return [partial(self._view_control.show_view, u'Detail/Clip'), self._clip_control, self._clip_phase_enabler]

    def _init_quantize_actions(self):
        self._quantize = self._for_non_frozen_tracks(QuantizationComponent(name=u'Selected_Clip_Quantize', quantization_names=QUANTIZATION_NAMES_UNICODE, settings_class=self.quantization_settings_class, is_enabled=False, layer=Layer(action_button=u'quantize_button')))
        self._quantize.settings.layer = make_dialog_layer(swing_amount_encoder=u'parameter_controls_raw[0]', quantize_to_encoder=u'parameter_controls_raw[1]', quantize_amount_encoder=u'parameter_controls_raw[2]', record_quantization_encoder=u'parameter_controls_raw[4]', record_quantization_toggle_button=u'track_state_buttons_raw[4]', priority=consts.MOMENTARY_DIALOG_PRIORITY)
        self._model.quantizeSettingsView = self._quantize.settings

    def _init_fixed_length(self):
        super(Push2, self)._init_fixed_length()
        self._fixed_length.settings_component.layer = make_dialog_layer(length_option_buttons=u'select_buttons', fixed_length_toggle_button=u'track_state_buttons_raw[0]', legato_launch_toggle_button=u'track_state_buttons_raw[7]', priority=consts.MOMENTARY_DIALOG_PRIORITY)
        self._model.fixedLengthSelectorView = self._fixed_length.settings_component
        self._model.fixedLengthSettings = self._fixed_length_setting

    def _init_value_components(self):
        super(Push2, self)._init_value_components()
        self._model.importantGlobals.swing = self._swing_amount.display
        self._model.importantGlobals.tempo = self._tempo.display
        self._model.importantGlobals.masterVolume = self._master_vol.display
        self._model.importantGlobals.cueVolume = self._master_cue_vol.display

    def _create_main_modes_layer(self):
        return Layer(mix_button=u'mix_button', clip_button=u'clip_mode_button', device_button=u'device_mode_button', browse_button=u'browse_mode_button', add_device_button=u'create_device_button', add_track_button=u'create_track_button') + Layer(user_button=u'user_button', priority=consts.USER_BUTTON_PRIORITY)

    def _should_send_palette(self):
        return self._firmware_version < FirmwareVersion(1, 0, 63)

    def _send_color_palette(self):
        if self._should_send_palette():
            with self.component_guard():
                palette_entry = SysexElement(sysex.make_rgb_palette_entry_message)
                finalize_palette = SysexElement(sysex.make_reapply_palette_message)
                for index, hex_color, white_balance in COLOR_TABLE:
                    palette_entry.send_value(index, hex_color, white_balance)

                finalize_palette.send_value()

    def _init_pad_curve(self):
        self._pad_curve_sender = PadVelocityCurveSender(curve_sysex_element=SysexElement(sysex.make_pad_velocity_curve_message), threshold_sysex_element=SysexElement(sysex.make_pad_threshold_message), settings=self._setup_settings.pad_settings, chunk_size=sysex.PAD_VELOCITY_CURVE_CHUNK_SIZE)

    def _init_visualisation_settings(self):
        self._model.visualisationSettings = VisualisationSettings()

    def _create_user_component(self):
        self._user_mode_ui_blocker = Component(is_enabled=False, layer=self._create_message_box_background_layer())
        sysex_control = SysexElement(send_message_generator=sysex.make_mode_switch_messsage, sysex_identifier=sysex.make_message_identifier(sysex.MODE_SWITCH_MESSAGE_ID))
        user = UserComponent(value_control=sysex_control, is_enabled=True)
        return user

    def _create_settings(self):
        return create_settings(preferences=self.preferences)

    def _init_hardware_settings(self):
        self._setup_settings = self.register_disconnectable(Settings(preferences=self.preferences))
        self._hardware_settings = HardwareSettingsComponent(led_brightness_element=SysexElement(sysex.make_led_brightness_message), display_brightness_element=SysexElement(sysex.make_display_brightness_message), settings=self._setup_settings.hardware)

    def _init_transport_state(self):
        self._model.transportState = TransportState(song=self.song)

    def _init_setup_component(self):
        self._setup_settings.general.workflow = u'scene' if self._settings[u'workflow'].value else u'clip'
        self._setup_settings.general.aftertouch_mode = u'mono' if self._settings[u'aftertouch_mode'].value else u'polyphonic'
        self.__on_workflow_setting_changed.subject = self._setup_settings.general
        self.__on_aftertouch_mode_setting_changed.subject = self._setup_settings.general
        self.__on_aftertouch_mode_setting_changed(self._setup_settings.general.aftertouch_mode)
        setup = SetupComponent(name=u'Setup', settings=self._setup_settings, pad_curve_sender=self._pad_curve_sender, firmware_switcher=self._firmware_switcher, is_enabled=False, layer=make_dialog_layer(category_radio_buttons=u'select_buttons', priority=consts.SETUP_DIALOG_PRIORITY, make_it_go_boom_button=u'track_state_buttons_raw[7]'))
        setup.general.layer = Layer(workflow_encoder=u'parameter_controls_raw[0]', display_brightness_encoder=u'parameter_controls_raw[1]', led_brightness_encoder=u'parameter_controls_raw[2]', aftertouch_mode_encoder=u'parameter_controls_raw[3]', priority=consts.SETUP_DIALOG_PRIORITY)
        setup.info.layer = Layer(install_firmware_button=u'track_state_buttons_raw[6]', priority=consts.SETUP_DIALOG_PRIORITY)
        setup.pad_settings.layer = Layer(sensitivity_encoder=u'parameter_controls_raw[4]', gain_encoder=u'parameter_controls_raw[5]', dynamics_encoder=u'parameter_controls_raw[6]', priority=consts.SETUP_DIALOG_PRIORITY)
        setup.display_debug.layer = Layer(show_row_spaces_button=u'track_state_buttons_raw[0]', show_row_margins_button=u'track_state_buttons_raw[1]', show_row_middle_button=u'track_state_buttons_raw[2]', show_button_spaces_button=u'track_state_buttons_raw[3]', show_unlit_button_button=u'track_state_buttons_raw[4]', show_lit_button_button=u'track_state_buttons_raw[5]', priority=consts.SETUP_DIALOG_PRIORITY)
        self._model.setupView = setup
        self._setup_enabler = EnablingModesComponent(component=setup, enabled_color=u'DefaultButton.On', disabled_color=u'DefaultButton.On')
        self._setup_enabler.layer = Layer(cycle_mode_button=u'setup_button')
        self._setup_component = setup

    def _init_firmware_update(self):
        self._firmware_update = FirmwareUpdateComponent(layer=self._create_message_box_background_layer())
        self._model.firmwareUpdate = self._firmware_update
        self._firmware_switcher = FirmwareSwitcher(firmware_collector=self._firmware_collector, firmware_update=self._firmware_update, installed_firmware_version=self._firmware_version)
        self._model.firmwareSwitcher = self._firmware_switcher

    @listens(u'workflow')
    def __on_workflow_setting_changed(self, value):
        self._settings[u'workflow'].value = value == u'scene'

    @listens(u'aftertouch_mode')
    def __on_aftertouch_mode_setting_changed(self, value):
        self._settings[u'aftertouch_mode'].value = value == u'mono'
        self._instrument.instrument.set_aftertouch_mode(value)
        self._selected_note_instrument.set_aftertouch_mode(value)

    def _create_controls(self):
        self._create_pad_sensitivity_update()

        class Deleter(object):

            @property
            def is_deleting(_):
                return self._delete_default_component.is_deleting

            def delete_clip_envelope(_, param):
                return self._delete_default_component.delete_clip_envelope(param)

        self.elements = Elements(deleter=Deleter(), undo_handler=UndoStepHandler(song=self.song), pad_sensitivity_update=self._pad_sensitivity_update, playhead=self._c_instance.playhead, velocity_levels=self._c_instance.velocity_levels, full_velocity=self._c_instance.full_velocity, model=self._model)
        self.__on_param_encoder_touched.replace_subjects(self.elements.global_param_touch_buttons_raw)
        self._update_encoder_model()

    def _create_pad_sensitivity_update(self):
        all_pad_sysex_control = SysexElement(sysex.make_pad_setting_message)
        pad_sysex_control = SysexElement(sysex.make_pad_setting_message)
        aftertouch_enabled_control = SysexElement(send_message_generator=sysex.make_mono_aftertouch_enabled_message)
        sensitivity_sender = pad_parameter_sender(all_pad_sysex_control, pad_sysex_control, aftertouch_enabled_control)
        self._pad_sensitivity_update = PadUpdateComponent(all_pads=list(range(64)), parameter_sender=sensitivity_sender, default_profile=PadSettings(sensitivity=default_profile, aftertouch_enabled=MONO_AFTERTOUCH_ENABLED), update_delay=TIMER_DELAY)
        self._pad_sensitivity_update.set_profile(u'drums', PadSettings(sensitivity=playing_profile, aftertouch_enabled=MONO_AFTERTOUCH_ENABLED))
        self._pad_sensitivity_update.set_profile(u'instrument', PadSettings(sensitivity=playing_profile, aftertouch_enabled=MONO_AFTERTOUCH_ENABLED))
        self._pad_sensitivity_update.set_profile(u'loop', PadSettings(sensitivity=loop_selector_profile, aftertouch_enabled=MONO_AFTERTOUCH_DISABLED))

    @listens_group(u'value')
    def __on_param_encoder_touched(self, value, encoder):
        self._update_encoder_model()

    def _update_encoder_model(self):
        self._model.controls.encoders = [ NamedTuple(__id__=u'encoder_%i' % i, touched=e.is_pressed()) for i, e in enumerate(self.elements.global_param_touch_buttons_raw) ]

    def _with_firmware_version(self, major_version, minor_version, control_element):
        u"""
        We consider all features to be available for Push 2
        """
        return control_element

    def _send_hardware_settings(self):
        self._hardware_settings.send()
        self._pad_curve_sender.send()
        self._send_color_palette()

    def port_settings_changed(self):
        super(Push2, self).port_settings_changed()
        if self._initialized:
            self._send_hardware_settings()
            self.update()

    def on_identified(self, response_bytes):
        try:
            major, minor, build, sn, board_revision = sysex.extract_identity_response_info(response_bytes)
            self._firmware_version = FirmwareVersion(major, minor, build)
            self._firmware_version.release_type = self._firmware_collector.get_release_type(self._firmware_version)
            self._model.hardwareInfo.firmwareVersion = self._firmware_version
            self._model.hardwareInfo.serialNumber = sn
            logger.info(u'Push 2 identified')
            logger.info(u'Firmware %i.%i Build %i' % (major, minor, build))
            logger.info(u'Serial number %i' % sn)
            logger.info(u'Board Revision %i' % board_revision)
            self._board_revision = board_revision
            self._identified = True
            self._try_initialize()
        except IndexError:
            logger.warning(u"Couldn't identify Push 2 unit")

    def update(self):
        if self._initialized:
            super(Push2, self).update()

    def update_display_hook(self):
        if self._device_component and self._decoupled_parameter_list_change_notifications:
            self._device_component.device_component.update_and_notify_parameters()
