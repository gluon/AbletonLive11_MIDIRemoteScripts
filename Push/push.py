# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\push.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 42480 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object, range, str
import logging, weakref
from copy import copy
from functools import partial
from ableton.v2.base import get_slice, listens, listens_group, mixin, nop, task
from ableton.v2.control_surface import BackgroundLayer, DeviceDecoratorFactory, Layer
from ableton.v2.control_surface.default_bank_definitions import BANK_DEFINITIONS
from ableton.v2.control_surface.defaults import TIMER_DELAY
from ableton.v2.control_surface.device_provider import DeviceProvider as DeviceProviderBase
from ableton.v2.control_surface.device_provider import device_to_appoint
from ableton.v2.control_surface.elements import ComboElement, NullFullVelocity, NullPlayhead, NullVelocityLevels
from ableton.v2.control_surface.mode import AddLayerMode, EnablingModesComponent, LazyEnablingMode, ModesComponent
from pushbase import consts
from pushbase.actions import SelectComponent, StopClipComponent
from pushbase.automation_component import AutomationComponent
from pushbase.browser_modes import BrowserHotswapMode
from pushbase.colors import LIVE_COLORS_TO_MIDI_VALUES, RGB_COLOR_TABLE
from pushbase.control_element_factory import create_sysex_element
from pushbase.note_editor_component import NoteEditorComponent
from pushbase.note_settings_component import NoteSettingsComponent
from pushbase.pad_sensitivity import PadUpdateComponent
from pushbase.push_base import PushBase
from pushbase.quantization_component import QuantizationComponent
from pushbase.sliced_simpler_component import SlicedSimplerComponent
from pushbase.special_session_component import SpecialSessionComponent
from pushbase.sysex import LIVE_MODE
from pushbase.undo_step_handler import UndoStepHandler
from . import sysex
from .actions import CreateDefaultTrackComponent, CreateDeviceComponent, CreateInstrumentTrackComponent
from .browser_component import BrowserComponent
from .browser_model_factory import make_browser_model
from .device_component import DeviceComponent
from .device_navigation_component import DeviceNavigationComponent
from .drum_group_component import DrumGroupComponent
from .elements import Elements
from .global_pad_parameters import GlobalPadParameters
from .handshake_component import HandshakeComponent, MinimumFirmwareVersionElement, make_dongle_message
from .mode_behaviours import AlternativeBehaviour, CancellableBehaviour, DynamicBehaviourMixin, ExcludingBehaviourMixin
from .multi_entry_mode import MultiEntryMode
from .navigation_node import ChainNode
from .notification_component import NotificationComponent, align_right
from .pad_sensitivity import pad_parameter_sender
from .quantization_settings import QuantizationSettingsComponent
from .scales_component import InstrumentScalesComponent
from .selected_track_parameter_provider import SelectedTrackParameterProvider
from .settings import CRITICAL_THRESHOLD_LIMIT, action_pad_sensitivity, create_settings, make_pad_parameters
from .special_mixer_component import SpecialMixerComponent
from .user_settings_component import UserComponent
from .with_priority import WithPriority
logger = logging.getLogger(__name__)
HANDSHAKE_DELAY = 1.0

class DeviceProvider(DeviceProviderBase):

    def _appoint_device_from_song(self):
        if isinstance(self.device, ChainNode.RackBank2Device):
            if self.device._rack_device == self.song.appointed_device:
                return
        self.device = device_to_appoint(self.song.appointed_device)


class BrowserMode(MultiEntryMode):

    def __init__(self, create_browser=nop, scales_enabler=None, *a, **k):
        (super(BrowserMode, self).__init__)(LazyEnablingMode(create_browser), *a, **k)
        self._scales_enabler = scales_enabler

    def enter_mode(self):
        super(BrowserMode, self).enter_mode()
        self._scales_enabler.selected_mode = 'disabled'

    @property
    def component(self):
        return self._mode.enableable


class Push(PushBase):
    input_target_name_for_auto_arm = 'Push Input'
    device_component_class = DeviceComponent
    device_provider_class = DeviceProvider
    selected_track_parameter_provider_class = SelectedTrackParameterProvider
    bank_definitions = BANK_DEFINITIONS
    note_editor_class = NoteEditorComponent
    sliced_simpler_class = SlicedSimplerComponent
    quantization_settings_class = QuantizationSettingsComponent
    note_settings_component_class = NoteSettingsComponent
    automation_component_class = AutomationComponent

    def __init__(self, *a, **k):
        (super(Push, self).__init__)(*a, **k)
        with self.component_guard():
            self.initialize()
        logger.info('Push script loaded')
        self._send_midi(sysex.WELCOME_MESSAGE)

    def disconnect(self):
        super(Push, self).disconnect()
        logger.info('Push script unloaded')
        self._send_midi(sysex.GOOD_BYE_MESSAGE)

    def port_settings_changed(self):
        super(Push, self).port_settings_changed()
        self._start_handshake_task.restart()

    def on_select_clip_slot(self, clip_slot):
        self._selector.on_select_clip(clip_slot)

    def on_select_scene(self, scene):
        self._selector.on_select_scene(scene)

    def on_select_track(self, track):
        self._selector.on_select_track(track)

    def _create_components(self):
        self._init_handshake()
        self._init_selector()
        super(Push, self)._create_components()
        self._init_browser()
        self._init_track_modes()

    def _create_settings(self):
        settings = create_settings(preferences=(self.preferences))
        self._Push__on_pad_curve.subject = settings['curve']
        self._Push__on_pad_threshold.subject = settings['threshold']
        self._Push__on_aftertouch_threshold.subject = settings['aftertouch_threshold']
        self._Push__on_aftertouch_mode.subject = settings['aftertouch_mode']
        return settings

    def _create_device_decorator_factory(self):
        return DeviceDecoratorFactory()

    def _init_settings(self):
        super(Push, self)._init_settings()
        self._init_global_pad_parameters()
        self._update_pad_params()

    def _init_selector(self):
        self._selector = SelectComponent(name='Selector')
        self._selector.layer = Layer(select_button='select_button')
        self._selector.selection_display_layer = Layer(display_line='display_line3',
          priority=(consts.DIALOG_PRIORITY))

    def _init_handshake(self):
        dongle_message, dongle = make_dongle_message(sysex.DONGLE_ENQUIRY_PREFIX)
        identity_control = create_sysex_element(sysex.IDENTITY_PREFIX, sysex.IDENTITY_ENQUIRY)
        dongle_control = create_sysex_element(sysex.DONGLE_PREFIX, dongle_message)
        presentation_control = create_sysex_element(sysex.DONGLE_PREFIX, sysex.make_presentation_message(self.application))
        self._handshake = HandshakeComponent(identity_control=identity_control,
          dongle_control=dongle_control,
          presentation_control=presentation_control,
          dongle=dongle)
        self._on_handshake_success.subject = self._handshake
        self._on_handshake_failure.subject = self._handshake
        self._start_handshake_task = self._tasks.add(task.sequence(task.wait(HANDSHAKE_DELAY), task.run(self._start_handshake)))
        self._start_handshake_task.kill()

    def _init_user(self):
        super(Push, self)._init_user()
        self._on_push_hardware_mode_changed.subject = self._user
        self._update_pad_params()

    def _with_firmware_version(self, major_version, minor_version, control_element):
        return MinimumFirmwareVersionElement(major_version, minor_version, control_element, self._handshake)

    def _start_handshake(self):
        self._start_handshake_task.kill()
        self.elements.playhead_element.proxied_object = self._c_instance.playhead
        self.elements.velocity_levels_element.proxied_object = self._c_instance.velocity_levels
        self.elements.full_velocity_element.proxied_object = self._c_instance.full_velocity
        self._note_repeat_enabler.set_note_repeat(self._c_instance.note_repeat)
        for control in self.controls:
            receive_value_backup = getattr(control, '_receive_value_backup', nop)
            if receive_value_backup != nop:
                control.receive_value = receive_value_backup
            send_midi_backup = getattr(control, '_send_midi_backup', nop)
            if send_midi_backup != nop:
                control.send_midi = send_midi_backup

        self._handshake._start_handshake()
        self.update()

    @listens('success')
    def _on_handshake_success(self):
        logger.info('Handshake succeded with firmware version %.2f!' % self._handshake.firmware_version)
        self.update()
        self._c_instance.set_firmware_version(self._handshake.firmware_version)
        if self._handshake.has_version_requirements(1, 16):
            self._user.settings = self._settings
        else:
            settings = copy(self._settings)
            del settings['aftertouch_threshold']
            self._user.settings = settings
        self._Push__on_aftertouch_mode(self._settings['aftertouch_mode'].value)

    @listens('failure')
    def _on_handshake_failure(self, bootloader_mode):
        logger.error('Handshake failed, performing harakiri!')
        if bootloader_mode:
            self._c_instance.set_firmware_version(0.0)
        self._c_instance.playhead.enabled = False
        self.elements.playhead_element.proxied_object = NullPlayhead()
        self._c_instance.velocity_levels.enabled = False
        self.elements.velocity_levels_element.proxied_object = NullVelocityLevels()
        self._c_instance.full_velocity.enabled = False
        self.elements.full_velocity_element.proxied_object = NullFullVelocity()
        self._note_repeat_enabler.set_note_repeat(None)
        for control in self.controls:
            receive_value_backup = getattr(control, 'receive_value', nop)
            send_midi_backup = getattr(control, 'send_midi', nop)
            try:
                control.receive_value = nop
                if receive_value_backup != nop:
                    control._receive_value_backup = receive_value_backup
                control.send_midi = nop
                if send_midi_backup != nop:
                    control._send_midi_backup = send_midi_backup
            except AttributeError:
                pass

    @listens('mode')
    def _on_push_hardware_mode_changed(self, mode):
        if mode == LIVE_MODE:
            if self._start_handshake_task.is_running:
                self._start_handshake()
            else:
                if self._handshake.handshake_succeeded:
                    self.update()

    def _create_background_layer(self):
        return super(Push, self)._create_background_layer() + Layer(display_line1='display_line1',
          display_line2='display_line2',
          display_line3='display_line3',
          display_line4='display_line4',
          in_button='in_button',
          out_button='out_button',
          pad_parameters=(self._pad_parameter_control))

    def _create_message_box_background_layer(self):
        return super(Push, self)._create_message_box_background_layer() + BackgroundLayer('in_button',
          'out_button', priority=(consts.MESSAGE_BOX_PRIORITY))

    def _create_track_frozen_layer(self):
        return Layer(display='display_line2',
          _notification=(self._notification.use_full_display(1)))

    def _create_notification_component(self):
        return NotificationComponent(display_lines='display_lines', is_enabled=True)

    def _create_message_box_layer(self):
        return Layer(display_line1='display_line1',
          display_line2='display_line2',
          display_line3='display_line3',
          display_line4='display_line4',
          cancel_button='select_buttons_raw[-1]',
          priority=(consts.MESSAGE_BOX_PRIORITY))

    def _create_clip_mode(self):
        return [
         self._track_modes, (self._mixer, self._mixer_layer)] + super(Push, self)._create_clip_mode()

    def _create_clip_loop_layer(self):
        return super(Push, self)._create_clip_loop_layer() + Layer(name_display=(self.elements.display_line1.subdisplay[:36]),
          value_display=(self.elements.display_line2.subdisplay[:36]))

    def _create_clip_audio_layer(self):
        return super(Push, self)._create_clip_audio_layer() + Layer(name_display=(self.elements.display_line1.subdisplay[36:]),
          value_display=(self.elements.display_line2.subdisplay[36:]))

    def _create_clip_name_layer(self):
        return super(Push, self)._create_clip_name_layer() + Layer(display='display_line3')

    def _init_track_modes(self):
        self._track_modes = ModesComponent(name='Track_Modes')
        self._track_modes.set_enabled(False)
        self._track_modes.add_mode('stop', AddLayerMode(self._stop_clips, self._stop_track_clips_layer))
        self._track_modes.add_mode('solo', AddLayerMode(self._mixer, self._mixer_solo_layer))
        self._track_modes.add_mode('mute', AddLayerMode(self._mixer, self._mixer_mute_layer))
        self._track_modes.layer = self._create_track_modes_layer()
        self._track_modes.selected_mode = 'mute'

    def _browser_back_to_top(self):
        self._browser_mode.component.back_to_top()

    def _browser_reset_load_memory(self):
        self._browser_mode.component.reset_load_memory()

    def _init_browser(self):
        self._browser_mode = BrowserMode(self._create_browser, self._scales_enabler)
        self._browser_hotswap_mode = MultiEntryMode(BrowserHotswapMode(application=(self.application)))
        self._on_browse_mode_changed.subject = self.application.view

    def _create_main_mixer_modes(self):
        self._main_modes.add_mode('volumes', [
         self._track_modes,
         (
          self._mixer, self._mixer_volume_layer),
         self._track_note_editor_mode])
        self._main_modes.add_mode('pan_sends', [
         self._track_modes,
         (
          self._mixer, self._mixer_pan_send_layer),
         self._track_note_editor_mode])
        self._main_modes.add_mode('track', [
         self._track_modes,
         self._track_mixer,
         (
          self._mixer, self._mixer_track_layer),
         self._track_note_editor_mode])

    def _init_browse_mode(self):
        self._main_modes.add_mode('browse',
          [
         self._when_track_is_not_frozen(self._enable_stop_mute_solo_as_modifiers, partial(self._view_control.show_view, 'Browser'), self._browser_back_to_top, self._browser_hotswap_mode, self._browser_mode, self._browser_reset_load_memory)],
          groups=[
         'add_effect', 'add_track', 'browse'],
          behaviour=(mixin(DynamicBehaviourMixin, CancellableBehaviour)(lambda: not self._browser_hotswap_mode._mode.can_hotswap() and 'add_effect_left'
)))
        self._main_modes.add_mode('add_effect_right',
          [
         self._when_track_is_not_frozen(self._enable_stop_mute_solo_as_modifiers, self._browser_back_to_top, LazyEnablingMode(self._create_create_device_right))],
          behaviour=(mixin(ExcludingBehaviourMixin, CancellableBehaviour)([
         'add_track', 'browse'])),
          groups=[
         'add_effect'])
        self._main_modes.add_mode('add_effect_left',
          [
         self._when_track_is_not_frozen(self._enable_stop_mute_solo_as_modifiers, self._browser_back_to_top, LazyEnablingMode(self._create_create_device_left))],
          behaviour=(mixin(ExcludingBehaviourMixin, CancellableBehaviour)([
         'add_track', 'browse'])),
          groups=[
         'add_effect'])
        self._main_modes.add_mode('add_instrument_track',
          [
         self._enable_stop_mute_solo_as_modifiers,
         self._browser_back_to_top,
         LazyEnablingMode(self._create_create_instrument_track)],
          behaviour=mixin(ExcludingBehaviourMixin, AlternativeBehaviour)(excluded_groups=[
         'browse', 'add_effect'],
          alternative_mode='add_default_track'),
          groups=[
         'add_track'])
        self._main_modes.add_mode('add_default_track',
          [
         self._enable_stop_mute_solo_as_modifiers,
         self._browser_back_to_top,
         LazyEnablingMode(self._create_create_default_track)],
          groups=[
         'add_track'])
        self._main_modes.add_effect_right_button.mode_unselected_color = self._main_modes.add_effect_left_button.mode_unselected_color = self._main_modes.add_instrument_track_button.mode_unselected_color = 'DefaultButton.On'

    @listens('browse_mode')
    def _on_browse_mode_changed(self):
        if self.application.browser.hotswap_target or self._main_modes.selected_mode == 'browse' or self._browser_hotswap_mode.is_entered:
            self._main_modes.selected_mode = 'device'

    def _create_browser(self):
        state_buttons = self.elements.track_state_buttons.submatrix[:7, :]
        browser = BrowserComponent(name='Browser',
          is_enabled=False,
          layer=Layer(encoder_controls='global_param_controls',
          display_line1='display_line1',
          display_line2='display_line2',
          display_line3='display_line3',
          display_line4='display_line4',
          enter_button='in_button',
          exit_button='out_button',
          select_buttons='select_buttons',
          state_buttons=state_buttons,
          shift_button=(WithPriority(consts.SHARED_PRIORITY, 'shift_button')),
          prehear_button='track_state_buttons_raw[7]',
          _notification=(self._notification.use_full_display(2))),
          make_browser_model=make_browser_model,
          preferences=(self.preferences))
        return browser

    def _create_create_device_right(self):
        return CreateDeviceComponent(name='Create_Device_Right',
          browser_component=(self._browser_mode.component),
          browser_mode=(self._browser_mode),
          browser_hotswap_mode=(self._browser_hotswap_mode),
          insert_left=False,
          is_enabled=False)

    def _create_create_device_left(self):
        return CreateDeviceComponent(name='Create_Device_Right',
          browser_component=(self._browser_mode.component),
          browser_mode=(self._browser_mode),
          browser_hotswap_mode=(self._browser_hotswap_mode),
          insert_left=True,
          is_enabled=False)

    def _create_create_default_track(self):
        create_default_track = CreateDefaultTrackComponent(name='Create_Default_Track',
          is_enabled=False)
        create_default_track.options.layer = Layer(display_line='display_line4',
          label_display_line='display_line3',
          blank_display_line2='display_line2',
          blank_display_line1='display_line1',
          select_buttons='select_buttons',
          state_buttons='track_state_buttons',
          priority=(consts.DIALOG_PRIORITY))
        return create_default_track

    def _create_create_instrument_track(self):
        return CreateInstrumentTrackComponent(name='Create_Instrument_Track',
          browser_component=(self._browser_mode.component),
          browser_mode=(self._browser_mode),
          browser_hotswap_mode=(self._browser_hotswap_mode),
          is_enabled=False)

    def _create_device_mode(self):
        return [
         self._when_track_is_not_frozen(self._enable_stop_mute_solo_as_modifiers, partial(self._view_control.show_view, 'Detail/DeviceChain'), self._device_parameter_component, self._device_navigation, self._device_note_editor_mode)]

    def _create_scales(self):
        scales = InstrumentScalesComponent(note_layout=(self._note_layout),
          is_enabled=False,
          name='Scales',
          layer=(
         BackgroundLayer('display_line1',
           'display_line2', priority=(consts.DIALOG_PRIORITY)),
         Layer(scale_line1=(self.elements.display_line1.subdisplay[:18]),
           scale_line2=(self.elements.display_line2.subdisplay[:18]),
           scale_line3=(self.elements.display_line3.subdisplay[:9]),
           scale_line4=(self.elements.display_line4.subdisplay[:9]),
           top_display_line=(self.elements.display_line3.subdisplay[9:]),
           bottom_display_line=(self.elements.display_line4.subdisplay[9:]),
           top_buttons='select_buttons',
           bottom_buttons='track_state_buttons',
           encoder_controls='global_param_controls',
           _notification=(self._notification.use_single_line(0, get_slice[18:], align_right)),
           priority=(consts.DIALOG_PRIORITY)),
         Layer(presets_toggle_button='shift_button')))
        scales.presets_layer = (
         BackgroundLayer('track_state_buttons',
           'global_param_controls',
           'display_line1',
           'display_line2',
           priority=(consts.DIALOG_PRIORITY)),
         Layer(top_display_line='display_line3',
           bottom_display_line='display_line4',
           top_buttons='select_buttons',
           _notification=(self._notification.use_single_line(0)),
           priority=(consts.DIALOG_PRIORITY)))
        return scales

    def _create_scales_enabler(self):
        return EnablingModesComponent(component=(self._create_scales()),
          enabled_color='DefaultButton.On',
          is_enabled=False,
          layer=Layer(cycle_mode_button='scale_presets_button'))

    def _create_drum_component(self):
        return DrumGroupComponent(name='Drum_Group',
          is_enabled=False,
          quantizer=(self._quantize),
          selector=(self._selector))

    def _create_note_settings_component_layer(self):
        return Layer(top_display_line='display_line1',
          bottom_display_line='display_line2',
          info_display_line='display_line3',
          clear_display_line='display_line4',
          full_velocity_button='accent_button',
          priority=(consts.MOMENTARY_DIALOG_PRIORITY))

    def _create_note_editor_track_automation_layer(self):
        return super(Push, self)._create_note_editor_track_automation_layer() + Layer(name_display_line='display_line1',
          graphic_display_line='display_line2',
          value_display_line='display_line3',
          priority=(consts.MOMENTARY_DIALOG_PRIORITY))

    def _create_note_editor_device_automation_layer(self):
        return super(Push, self)._create_note_editor_device_automation_layer() + Layer(name_display_line='display_line1',
          value_display_line='display_line2',
          graphic_display_line='display_line3',
          priority=(consts.MOMENTARY_DIALOG_PRIORITY))

    def _init_stop_clips_action(self):
        self._stop_clips = StopClipComponent(session_ring=(self._session_ring),
          name='Stop_Clip')
        self._stop_clips.layer = Layer(stop_all_clips_button=(self._with_shift('global_track_stop_button')))
        self._stop_track_clips_layer = Layer(stop_track_clips_buttons='track_state_buttons')

    def _init_quantize_actions(self):
        self._quantize = self._for_non_frozen_tracks(QuantizationComponent(name='Selected_Clip_Quantize',
          settings_class=(self.quantization_settings_class),
          is_enabled=False,
          layer=Layer(action_button='quantize_button')))
        self._quantize.settings.layer = (
         BackgroundLayer('global_param_controls',
           'select_buttons',
           'track_state_buttons',
           priority=(consts.MOMENTARY_DIALOG_PRIORITY)),
         Layer(swing_amount_encoder='parameter_controls_raw[0]',
           quantize_to_encoder='parameter_controls_raw[1]',
           quantize_amount_encoder='parameter_controls_raw[2]',
           record_quantization_encoder='parameter_controls_raw[7]',
           record_quantization_toggle_button='track_state_buttons_raw[7]',
           display_line1='display_line1',
           display_line2='display_line2',
           display_line3='display_line3',
           display_line4='display_line4',
           priority=(consts.MOMENTARY_DIALOG_PRIORITY)))

    def _init_fixed_length(self):
        super(Push, self)._init_fixed_length()
        self._fixed_length.settings_component.layer = (
         BackgroundLayer((self.elements.track_state_buttons.submatrix[:7, :]),
           'display_line1',
           'display_line2',
           priority=(consts.MOMENTARY_DIALOG_PRIORITY)),
         Layer(length_option_buttons='select_buttons',
           label_display_line='display_line3',
           option_display_line='display_line4',
           legato_launch_toggle_button='track_state_buttons_raw[7]',
           _notification=(self._notification.use_single_line(1)),
           priority=(consts.MOMENTARY_DIALOG_PRIORITY)))

    def _create_note_repeat_layer(self):
        return super(Push, self)._create_note_repeat_layer() + Layer(pad_parameters=(self._pad_parameter_control),
          priority=(consts.DIALOG_PRIORITY))

    def _create_user_component(self):
        sysex_control = create_sysex_element(sysex.MODE_CHANGE)
        user = UserComponent(value_control=sysex_control)
        user.layer = Layer(action_button='user_button')
        user.settings_layer = Layer(display_line1='display_line1',
          display_line2='display_line2',
          display_line3='display_line3',
          display_line4='display_line4',
          encoders='global_param_controls')
        user.settings_layer.priority = consts.DIALOG_PRIORITY
        return user

    def _init_value_components(self):
        super(Push, self)._init_value_components()
        self._swing_amount.display.layer = (
         BackgroundLayer('display_line4', priority=(consts.DIALOG_PRIORITY)),
         Layer(label_display='display_line1',
           value_display='display_line3',
           graphic_display='display_line2',
           priority=(consts.DIALOG_PRIORITY)))
        self._tempo.display.layer = (
         BackgroundLayer('display_line3',
           'display_line4', priority=(consts.DIALOG_PRIORITY)),
         Layer(label_display='display_line1',
           value_display='display_line2',
           priority=(consts.DIALOG_PRIORITY)))
        self._master_vol.display.layer = (
         BackgroundLayer('display_line4', priority=(consts.DIALOG_PRIORITY)),
         Layer(label_display='display_line1',
           value_display='display_line3',
           graphic_display='display_line2',
           priority=(consts.DIALOG_PRIORITY)))
        self._master_cue_vol.display.layer = (
         BackgroundLayer('display_line4', priority=(consts.DIALOG_PRIORITY)),
         Layer(label_display='display_line1',
           value_display='display_line3',
           graphic_display='display_line2',
           priority=(consts.DIALOG_PRIORITY)))

    def _create_note_mode(self):
        return super(Push, self)._create_note_mode() + [
         self._percussion_instrument_finder,
         self._global_pad_parameters]

    def _instantiate_session(self):
        return SpecialSessionComponent(session_ring=(self._session_ring),
          is_enabled=False,
          auto_name=True,
          fixed_length_recording=(self._create_fixed_length_recording()),
          layer=(self._create_session_layer()))

    def _create_session_mode(self):
        return [
         self._session_overview_mode, self._session_mode, self._session_navigation]

    def _create_session_overview_layer(self):
        return Layer(button_matrix='shifted_matrix')

    def _set_session_skin(self, session):
        session.set_rgb_mode(LIVE_COLORS_TO_MIDI_VALUES,
          RGB_COLOR_TABLE, clip_slots_only=True)

    def _on_selected_track_changed(self):
        super(Push, self)._on_selected_track_changed()
        self._main_modes.pop_groups(['add_effect'])

    def _init_main_modes(self):
        super(Push, self)._init_main_modes()
        self._Push__on_main_mode_button_value.replace_subjects([
         self.elements.vol_mix_mode_button,
         self.elements.pan_send_mix_mode_button,
         self.elements.single_track_mix_mode_button,
         self.elements.clip_mode_button,
         self.elements.device_mode_button,
         self.elements.browse_mode_button])

    def _create_mixer_layer(self):
        return Layer(track_select_buttons='select_buttons',
          track_names_display='display_line4')

    def _create_mixer_solo_layer(self):
        return Layer(solo_buttons='track_state_buttons')

    def _create_mixer_mute_layer(self):
        return Layer(mute_buttons='track_state_buttons')

    def _create_mixer_pan_send_layer(self):
        return Layer(track_select_buttons='select_buttons',
          pan_send_toggle='pan_send_mix_mode_button',
          pan_send_controls='fine_grain_param_controls',
          track_names_display='display_line4',
          pan_send_names_display='display_line1',
          pan_send_graphics_display='display_line2',
          selected_track_name_display='display_line3',
          pan_send_values_display=(ComboElement('display_line3', 'any_touch_button')))

    def _create_mixer_volume_layer(self):
        return Layer(track_select_buttons='select_buttons',
          volume_controls='fine_grain_param_controls',
          track_names_display='display_line4',
          volume_names_display='display_line1',
          volume_graphics_display='display_line2',
          selected_track_name_display='display_line3',
          volume_values_display=(ComboElement('display_line3', 'any_touch_button')))

    def _create_mixer_track_layer(self):
        return Layer(track_select_buttons='select_buttons',
          selected_track_name_display='display_line3',
          track_names_display='display_line4')

    def _init_mixer(self):
        self._mixer = SpecialMixerComponent(tracks_provider=(self._session_ring))
        self._mixer.set_enabled(False)
        self._mixer.name = 'Mixer'
        self._mixer_layer = self._create_mixer_layer()
        self._mixer_pan_send_layer = self._create_mixer_pan_send_layer()
        self._mixer_volume_layer = self._create_mixer_volume_layer()
        self._mixer_track_layer = self._create_mixer_track_layer()
        self._mixer_solo_layer = self._create_mixer_solo_layer()
        self._mixer_mute_layer = self._create_mixer_mute_layer()
        for track in range(self.elements.matrix.width()):
            strip = self._mixer.channel_strip(track)
            strip.name = 'Channel_Strip_' + str(track)
            strip.set_invert_mute_feedback(True)
            strip.set_delete_handler(self._delete_component)
            strip._do_select_track = self.on_select_track
            strip.layer = Layer(shift_button='shift_button',
              duplicate_button='duplicate_button',
              selector_button='select_button')

        self._mixer.selected_strip().name = 'Selected_Channel_strip'
        self._mixer.master_strip().name = 'Master_Channel_strip'
        self._mixer.master_strip()._do_select_track = self.on_select_track
        self._mixer.master_strip().layer = Layer(select_button='master_select_button',
          selector_button='select_button')
        self._mixer.set_enabled(True)

    def _create_track_mixer_layer(self):
        return super(Push, self)._create_track_mixer_layer() + Layer(name_display_line='display_line1',
          graphic_display_line='display_line2',
          value_display_line=(ComboElement('display_line3', 'any_touch_button')))

    def _create_device_parameter_layer(self):
        return super(Push, self)._create_device_parameter_layer() + Layer(name_display_line='display_line1',
          value_display_line='display_line2',
          graphic_display_line=(ComboElement('display_line3', 'any_touch_button')))

    def _create_device_navigation(self):
        return DeviceNavigationComponent(device_bank_registry=(self._device_bank_registry),
          banking_info=(self._banking_info),
          is_enabled=False,
          session_ring=(self._session_ring),
          layer=Layer(enter_button='in_button',
          exit_button='out_button',
          select_buttons='select_buttons',
          state_buttons='track_state_buttons',
          display_line='display_line4',
          _notification=(self._notification.use_single_line(2))),
          info_layer=Layer(display_line1='display_line1',
          display_line2='display_line2',
          display_line3='display_line3',
          display_line4='display_line4',
          _notification=(self._notification.use_full_display(2))),
          delete_handler=(self._delete_component))

    def _init_device(self):
        super(Push, self)._init_device()
        self._device_component.layer = Layer(shift_button='shift_button')

    @listens_group('value')
    def __on_main_mode_button_value(self, value, sender):
        if not value:
            self._scales_enabler.selected_mode = 'disabled'

    def _create_controls(self):
        self._create_pad_sensitivity_update()
        push_ref = weakref.ref(self)

        class Deleter(object):

            @property
            def is_deleting(_):
                if push_ref():
                    return push_ref()._delete_default_component.is_deleting
                raise RuntimeError('Attempting to check if Push is deleting when the Push instance is dead')

            def delete_clip_envelope(_, param):
                if push_ref():
                    return push_ref()._delete_default_component.delete_clip_envelope(param)
                raise RuntimeError('Attempting to delete clip envelope when Push instance is dead')

        self.elements = Elements(deleter=(Deleter()),
          undo_handler=UndoStepHandler(song=(self.song)),
          pad_sensitivity_update=(self._pad_sensitivity_update),
          playhead=(self._c_instance.playhead),
          velocity_levels=(self._c_instance.velocity_levels),
          full_velocity=(self._c_instance.full_velocity))

    def _create_pad_sensitivity_update(self):
        all_pad_sysex_control = create_sysex_element(sysex.ALL_PADS_SENSITIVITY_PREFIX)
        pad_sysex_control = create_sysex_element(sysex.PAD_SENSITIVITY_PREFIX)
        sensitivity_sender = pad_parameter_sender(all_pad_sysex_control, pad_sysex_control)
        self._pad_sensitivity_update = PadUpdateComponent(all_pads=(list(range(64))),
          parameter_sender=sensitivity_sender,
          default_profile=action_pad_sensitivity,
          update_delay=TIMER_DELAY)

    def _init_global_pad_parameters(self):
        self._pad_parameter_control = self._with_firmware_version(1, 16, create_sysex_element((sysex.PAD_PARAMETER_PREFIX),
          default_value=(sysex.make_pad_parameter_message())))
        aftertouch_threshold = self._settings['aftertouch_threshold'].value
        self._global_pad_parameters = GlobalPadParameters(aftertouch_threshold=aftertouch_threshold,
          is_enabled=False,
          layer=Layer(pad_parameter=(self._pad_parameter_control)))

    @listens('value')
    def __on_pad_curve(self, _value):
        self._update_pad_params()

    @listens('value')
    def __on_pad_threshold(self, value):
        self._user.set_settings_info_text('' if value >= CRITICAL_THRESHOLD_LIMIT else consts.MessageBoxText.STUCK_PAD_WARNING)
        self._update_pad_params()

    @listens('value')
    def __on_aftertouch_threshold(self, value):
        self._global_pad_parameters.aftertouch_threshold = value

    @listens('value')
    def __on_aftertouch_mode(self, value):
        mode = 'mono' if value else 'polyphonic'
        self._instrument.instrument.set_aftertouch_mode(mode)
        self._selected_note_instrument.set_aftertouch_mode(mode)

    def _update_pad_params(self):
        new_pad_parameters = make_pad_parameters(self._settings['curve'].value, self._settings['threshold'].value)
        self._pad_sensitivity_update.set_profile('instrument', new_pad_parameters)
        self._pad_sensitivity_update.set_profile('drums', new_pad_parameters)
        self._pad_sensitivity_update.set_profile('loop', action_pad_sensitivity)

    def _update_calibration(self):
        self._send_midi(sysex.CALIBRATION_SET)

    def update(self):
        self._update_calibration()
        super(Push, self).update()