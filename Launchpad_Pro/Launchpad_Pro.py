#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Pro/Launchpad_Pro.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from builtins import range
from functools import partial
import Live
from _Framework.Util import const
from _Framework.Dependency import inject
from _Framework.SubjectSlot import subject_slot
from _Framework.Layer import Layer
from _Framework.ControlSurface import OptimizedControlSurface
from _Framework.IdentifiableControlSurface import IdentifiableControlSurface
from _Framework.ModesComponent import ModesComponent, LayerMode, AddLayerMode, ReenterBehaviour
from _Framework.InputControlElement import MIDI_NOTE_TYPE, MIDI_CC_TYPE
from _Framework.ComboElement import ComboElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from .Colors import LIVE_COLORS_TO_MIDI_VALUES, RGB_COLOR_TABLE
from .SkinDefault import make_default_skin
from .SpecialMidiMap import SpecialMidiMap, make_button, make_multi_button, make_slider
from .BackgroundComponent import ModifierBackgroundComponent, BackgroundComponent
from .ActionsComponent import ActionsComponent
from .ClipActionsComponent import ClipActionsComponent
from .LedLightingComponent import LedLightingComponent
from .TranslationComponent import TranslationComponent
from .TargetTrackComponent import TargetTrackComponent
from .SpecialDeviceComponent import SpecialDeviceComponent
from .DeviceNavigationComponent import DeviceNavigationComponent
from .SpecialSessionRecordingComponent import SpecialSessionRecordingComponent
from .DrumGroupFinderComponent import DrumGroupFinderComponent
from .DrumGroupComponent import DrumGroupComponent
from .SpecialMixerComponent import SpecialMixerComponent
from .SpecialSessionComponent import SpecialSessionComponent as SessionComponent, SpecialClipSlotComponent, SpecialSessionZoomingComponent as SessionZoomingComponent, SessionZoomingManagerComponent
from .SpecialModesComponent import SpecialModesComponent, SpecialReenterBehaviour, CancelingReenterBehaviour
from .UserMatrixComponent import UserMatrixComponent
from . import consts
NUM_TRACKS = 8
NUM_SCENES = 8

class MidiMap(SpecialMidiMap):

    def __init__(self, *a, **k):
        super(MidiMap, self).__init__(*a, **k)
        left_button_names = (u'Session_Record_Button', u'Double_Loop_Button', u'Duplicate_Button', u'Quantize_Button', u'Delete_Button', u'Undo_Button', u'Click_Button', u'Shift_Button')
        default_states = {True: u'DefaultButton.On',
         False: u'DefaultButton.Off'}
        rec_states = {True: u'Recording.On',
         False: u'Recording.Off'}
        shift_states = {True: u'Misc.ShiftOn',
         False: u'Misc.Shift'}
        for index, val in enumerate(left_button_names):
            if val in (u'Session_Record_Button', u'Undo_Button', u'Click_Button'):
                self.add_button(val, 0, (index + 1) * 10, MIDI_CC_TYPE, default_states=rec_states if val == u'Session_Record_Button' else default_states)
            else:
                self.add_modifier_button(val, 0, (index + 1) * 10, MIDI_CC_TYPE, default_states=shift_states if val == u'Shift_Button' else default_states)

        self.add_button(u'Record_Arm_Mode_Button', 0, 1, MIDI_CC_TYPE, default_states={True: u'Mode.RecordArm.On',
         False: u'Mode.RecordArm.Off'})
        self.add_button(u'Track_Select_Mode_Button', 0, 2, MIDI_CC_TYPE, default_states={True: u'Mode.TrackSelect.On',
         False: u'Mode.TrackSelect.Off'})
        self.add_button(u'Mute_Mode_Button', 0, 3, MIDI_CC_TYPE, default_states={True: u'Mode.Mute.On',
         False: u'Mode.Mute.Off'})
        self.add_button(u'Solo_Mode_Button', 0, 4, MIDI_CC_TYPE, default_states={True: u'Mode.Solo.On',
         False: u'Mode.Solo.Off'})
        self.add_button(u'Volume_Mode_Button', 0, 5, MIDI_CC_TYPE, default_states={True: u'Mode.Volume.On',
         False: u'Mode.Volume.Off'})
        self.add_button(u'Pan_Mode_Button', 0, 6, MIDI_CC_TYPE, default_states={True: u'Mode.Pan.On',
         False: u'Mode.Pan.Off'})
        self.add_button(u'Sends_Mode_Button', 0, 7, MIDI_CC_TYPE, default_states={True: u'Mode.Sends.On',
         False: u'Mode.Sends.Off'})
        self.add_button(u'Stop_Clip_Mode_Button', 0, 8, MIDI_CC_TYPE, default_states={True: u'Mode.StopClip.On',
         False: u'Mode.StopClip.Off'})
        self._arrow_button_names = [u'Arrow_Up_Button',
         u'Arrow_Down_Button',
         u'Arrow_Left_Button',
         u'Arrow_Right_Button']
        arrow_button_states = {u'Pressed': u'DefaultButton.On',
         u'Enabled': u'DefaultButton.Off',
         True: u'DefaultButton.On',
         False: u'DefaultButton.Disabled'}
        for index, val in enumerate(self._arrow_button_names):
            self.add_button(val, 0, index + 91, MIDI_CC_TYPE, default_states=arrow_button_states)

        self.add_modifier_button(u'Session_Mode_Button', 0, 95, MIDI_CC_TYPE, default_states={True: u'Mode.Session.On',
         False: u'Mode.Session.Off'}, element_factory=make_multi_button)
        self.add_button(u'Note_Mode_Button', 0, 96, MIDI_CC_TYPE, element_factory=make_multi_button)
        self.add_button(u'Device_Mode_Button', 0, 97, MIDI_CC_TYPE, default_states={True: u'Mode.Device.On',
         False: u'Mode.Device.Off'}, element_factory=make_multi_button)
        self.add_button(u'User_Mode_Button', 0, 98, MIDI_CC_TYPE, default_states={True: u'Mode.User.On',
         False: u'Mode.User.Off'}, element_factory=make_multi_button, color_slaves=True)
        self.add_matrix(u'Scene_Launch_Button_Matrix', make_button, 0, [[ identifier for identifier in range(89, 18, -10) ]], MIDI_CC_TYPE)
        self[u'Scene_Stop_Button_Matrix'] = self[u'Scene_Launch_Button_Matrix'].submatrix[:7, :]
        self[u'Scene_Stop_Button_Matrix'].name = u'Scene_Stop_Button_Matrix'
        self[u'Stop_All_Clips_Button'] = self[u'Scene_Launch_Button_Matrix_Raw'][0][7]
        self.add_matrix(u'Main_Button_Matrix', make_button, 0, [ [ identifier for identifier in range(start, start + NUM_TRACKS) ] for start in range(81, 10, -10) ], MIDI_NOTE_TYPE)
        self[u'Mixer_Button_Matrix'] = self[u'Main_Button_Matrix'].submatrix[:, 7:]
        self[u'Mixer_Button_Matrix'].name = u'Mixer_Button_Matrix'
        matrix_rows_with_session_button_raw = [ [ self.with_session_button(self[u'Main_Button_Matrix_Raw'][row][column]) for column in range(8) ] for row in range(8) ]
        self[u'Main_Button_Matrix_With_Session_Button'] = ButtonMatrixElement(rows=matrix_rows_with_session_button_raw, name=u'Main_Button_Matrix_With_Session_Button')
        note_buttons_raw = []
        for identifier in range(128):
            if identifier not in self[u'Main_Button_Matrix_Ids']:
                button = make_button(u'Note_Button_' + str(identifier), 0, identifier, MIDI_NOTE_TYPE)
                button.set_enabled(False)
                button.set_channel(consts.CHROM_MAP_CHANNEL)
                note_buttons_raw.append(button)

        self[u'Note_Button_Matrix'] = ButtonMatrixElement(rows=[note_buttons_raw], name=u'Note_Button_Matrix')

        def make_raw_drum_matrix():
            result = []
            for row in range(7, -1, -1):
                button_row = []
                row_offset = 8 + (7 - row) * 4
                for column in range(8):
                    column_offset = 28 if column >= 4 else 0
                    identifier = row * 8 + column + row_offset + column_offset
                    matrix_coords = self[u'Main_Button_Matrix_Ids'].get(identifier)
                    if matrix_coords:
                        button_row.append(self[u'Main_Button_Matrix_Raw'][matrix_coords[1]][matrix_coords[0]])
                    else:
                        button_row.append(make_button(u'Drum_Note_Button_' + str(identifier), 0, identifier, MIDI_NOTE_TYPE))

                result.append(button_row)

            return result

        self[u'Drum_Button_Matrix'] = ButtonMatrixElement(rows=make_raw_drum_matrix(), name=u'Drum_Button_Matrix')
        self.add_matrix(u'Slider_Button_Matrix', make_slider, 0, [[ identifier for identifier in range(21, 29) ]], MIDI_CC_TYPE)
        for index, slider in enumerate(self[u'Slider_Button_Matrix_Raw'][0]):
            slider.set_index(index)

        self.create_user_mode_controls()

    def create_user_mode_controls(self):
        u"""
        Creates control elements that aren't used in the script
        but need to exist so they can be grabbed and observed
        via Max for Live.
        """
        for channel in consts.USER_MODE_CHANNELS:
            channel_name = channel + 1
            self.add_matrix(u'User_Button_Matrix_Ch_%d' % (channel_name,), make_button, channel, consts.USER_MATRIX_IDENTIFIERS, MIDI_NOTE_TYPE)
            self.add_matrix(u'User_Left_Side_Button_Matrix_Ch_%d' % (channel_name,), make_button, channel, [ [identifier] for identifier in range(108, 116) ], MIDI_NOTE_TYPE)
            self.add_matrix(u'User_Right_Side_Button_Matrix_Ch_%d' % (channel_name,), make_button, channel, [ [identifier] for identifier in range(100, 108) ], MIDI_NOTE_TYPE)
            self.add_matrix(u'User_Bottom_Button_Matrix_Ch_%d' % (channel_name,), make_button, channel, [[ identifier for identifier in range(116, 124) ]], MIDI_NOTE_TYPE)
            self.add_matrix(u'User_Arrow_Button_Matrix_Ch_%d' % (channel_name,), make_button, channel, [[ identifier for identifier in range(91, 95) ]], MIDI_CC_TYPE)

    def with_shift(self, button_name):
        return ComboElement(self[button_name], modifiers=[self[u'Shift_Button']], name=u'Shifted_' + button_name)

    def with_session_button(self, button):
        return ComboElement(button, modifiers=[self[u'Session_Mode_Button']], name=button.name + u'_With_Session_Button')


class Launchpad_Pro(IdentifiableControlSurface, OptimizedControlSurface):
    identity_request = consts.SYSEX_IDENTITY_REQUEST

    def __init__(self, c_instance, *a, **k):
        product_id_bytes = consts.MANUFACTURER_ID + consts.DEVICE_CODE
        super(Launchpad_Pro, self).__init__(c_instance=c_instance, product_id_bytes=product_id_bytes, *a, **k)
        self._challenge = Live.Application.get_random_int(0, 400000000) & 2139062143
        with self.component_guard():
            self._skin = make_default_skin()
            with inject(skin=const(self._skin)).everywhere():
                self._midimap = MidiMap()
            self._target_track_component = TargetTrackComponent(name=u'Target_Track')
            self._create_background()
            self._create_global_component()
            self._last_sent_mode_byte = None
            with inject(layout_setup=const(self._layout_setup), should_arm=const(self._should_arm_track)).everywhere():
                self._create_session()
                self._create_recording()
                self._create_actions()
                self._create_drums()
                self._create_mixer()
                self._create_device()
                self._create_modes()
                self._create_user()
            self._on_session_record_changed.subject = self.song()
        self.set_device_component(self._device)
        self._on_session_record_changed()

    def disconnect(self):
        self._send_midi(consts.TURN_OFF_LEDS)
        self._send_midi(consts.QUIT_MESSAGE)
        super(Launchpad_Pro, self).disconnect()

    def _create_background(self):
        self._modifier_background_component = ModifierBackgroundComponent(name=u'Background_Component', is_enabled=False, layer=Layer(shift_button=self._midimap[u'Shift_Button']))
        self._shifted_background = BackgroundComponent(name=u'No_Op_Shifted_Buttons', is_enabled=False, layer=Layer(click_bitton=self._midimap.with_shift(u'Click_Button'), delete_button=self._midimap.with_shift(u'Delete_Button'), duplicate_button=self._midimap.with_shift(u'Duplicate_Button'), double_button=self._midimap.with_shift(u'Double_Loop_Button'), session_record_button=self._midimap.with_shift(u'Session_Record_Button')))

    def _create_global_component(self):
        self._actions_component = ActionsComponent(name=u'Global_Actions', is_enabled=False, layer=Layer(undo_button=self._midimap[u'Undo_Button'], redo_button=self._midimap.with_shift(u'Undo_Button'), metronome_button=self._midimap[u'Click_Button'], quantization_on_button=self._midimap.with_shift(u'Quantize_Button')))

    def _create_session(self):
        self._session = SessionComponent(NUM_TRACKS, NUM_SCENES, auto_name=True, is_enabled=False, enable_skinning=True, layer=Layer(track_bank_left_button=self._midimap[u'Arrow_Left_Button'], track_bank_right_button=self._midimap[u'Arrow_Right_Button'], scene_bank_up_button=self._midimap[u'Arrow_Up_Button'], scene_bank_down_button=self._midimap[u'Arrow_Down_Button']))
        self._session.set_enabled(True)
        self._session.set_rgb_mode(LIVE_COLORS_TO_MIDI_VALUES, RGB_COLOR_TABLE)
        SpecialClipSlotComponent.quantization_component = self._actions_component
        for scene_index in range(NUM_SCENES):
            scene = self._session.scene(scene_index)
            scene.layer = Layer(select_button=self._midimap[u'Shift_Button'], delete_button=self._midimap[u'Delete_Button'], duplicate_button=self._midimap[u'Duplicate_Button'])
            for track_index in range(NUM_TRACKS):
                slot = scene.clip_slot(track_index)
                slot.layer = Layer(select_button=self._midimap[u'Shift_Button'], delete_button=self._midimap[u'Delete_Button'], duplicate_button=self._midimap[u'Duplicate_Button'], double_loop_button=self._midimap[u'Double_Loop_Button'], quantize_button=self._midimap[u'Quantize_Button'])

        self._session_zoom = SessionZoomingComponent(self._session, name=u'Session_Overview', is_enabled=True, enable_skinning=True)

    def _create_recording(self):
        self._session_record = SpecialSessionRecordingComponent(self._target_track_component, name=u'Session_Recording', is_enabled=False, layer=Layer(record_button=self._midimap[u'Session_Record_Button']))

    def _create_actions(self):
        self._clip_actions_component = ClipActionsComponent(self._target_track_component, name=u'Clip_Actions', is_enabled=False, layer=Layer(duplicate_button=self._midimap[u'Duplicate_Button'], double_button=self._midimap[u'Double_Loop_Button'], quantize_button=self._midimap[u'Quantize_Button']))
        ClipActionsComponent.quantization_component = self._actions_component

    def _create_drums(self):
        self._drum_group_finder = DrumGroupFinderComponent(self._target_track_component, name=u'Drum_Group_Finder', is_enabled=False, layer=None)
        self._on_drum_group_changed.subject = self._drum_group_finder
        self._drum_group_finder.set_enabled(True)
        self._drum_group = DrumGroupComponent(self._clip_actions_component, name=u'Drum_Group_Control', translation_channel=consts.DR_MAP_CHANNEL)
        self._drum_group.set_enabled(True)

    def _create_mixer(self):
        self._mixer = SpecialMixerComponent(NUM_TRACKS, auto_name=True, is_enabled=True, invert_mute_feedback=True)
        self._mixer.name = u'Mixer_Control'
        self._session.set_mixer(self._mixer)

    def _create_device(self):
        self._device = SpecialDeviceComponent(name=u'Device_Control', is_enabled=False, device_selection_follows_track_selection=True)
        self._device_navigation = DeviceNavigationComponent(name=u'Device_Navigation')
        self._device_background = BackgroundComponent(name=u'Device_Background_Component')

    def _setup_drum_group(self):
        self._drum_group.set_drum_group_device(self._drum_group_finder.drum_group)

    def _create_translation(self, comp_name, channel, button_layer, should_enable = True, should_reset = True):
        translation_component = TranslationComponent(name=comp_name, translated_channel=channel, should_enable=should_enable, should_reset=should_reset, is_enabled=False, layer=button_layer)
        setattr(self, u'_' + comp_name.lower(), translation_component)
        return translation_component

    def _create_modes(self):
        self._modes = ModesComponent(name=u'Launchpad_Modes', is_enabled=False)
        self._session_layer_mode = AddLayerMode(self._session, Layer(scene_launch_buttons=self._midimap[u'Scene_Launch_Button_Matrix'], clip_launch_buttons=self._midimap[u'Main_Button_Matrix'], delete_button=self._midimap[u'Delete_Button'], duplicate_button=self._midimap[u'Duplicate_Button'], double_button=self._midimap[u'Double_Loop_Button'], quantize_button=self._midimap[u'Quantize_Button']))
        action_button_background = BackgroundComponent(name=u'No_Op_Buttons')
        self._action_button_background_layer_mode = LayerMode(action_button_background, Layer(delete_button=self._midimap[u'Delete_Button'], quantize_button=self._midimap[u'Quantize_Button'], duplicate_button=self._midimap[u'Duplicate_Button'], double_button=self._midimap[u'Double_Loop_Button']))
        self._clip_delete_layer_mode = AddLayerMode(self._clip_actions_component, layer=Layer(delete_button=self._midimap[u'Delete_Button']))
        self._create_session_zooming_modes()
        self._create_session_mode()
        self._create_note_modes()
        self._create_device_mode()
        self._create_user_mode()
        self._create_record_arm_mode()
        self._create_track_select_mode()
        self._create_mute_mode()
        self._create_solo_mode()
        self._create_volume_mode()
        self._create_pan_mode()
        self._create_sends_mode()
        self._create_stop_clips_mode()
        self._modes.layer = Layer(session_mode_button=self._midimap[u'Session_Mode_Button'], note_mode_button=self._midimap[u'Note_Mode_Button'], device_mode_button=self._midimap[u'Device_Mode_Button'], user_mode_button=self._midimap[u'User_Mode_Button'], record_arm_mode_button=self._midimap[u'Record_Arm_Mode_Button'], track_select_mode_button=self._midimap[u'Track_Select_Mode_Button'], mute_mode_button=self._midimap[u'Mute_Mode_Button'], solo_mode_button=self._midimap[u'Solo_Mode_Button'], volume_mode_button=self._midimap[u'Volume_Mode_Button'], pan_mode_button=self._midimap[u'Pan_Mode_Button'], sends_mode_button=self._midimap[u'Sends_Mode_Button'], stop_clip_mode_button=self._midimap[u'Stop_Clip_Mode_Button'])
        self._modes.selected_mode = u'session_mode'
        self._on_layout_changed.subject = self._modes

    def _create_session_zooming_modes(self):
        session_zoom_layer = Layer(button_matrix=self._midimap[u'Main_Button_Matrix'], nav_left_button=self._midimap[u'Arrow_Left_Button'], nav_right_button=self._midimap[u'Arrow_Right_Button'], nav_up_button=self._midimap[u'Arrow_Up_Button'], nav_down_button=self._midimap[u'Arrow_Down_Button'])
        session_zooming_layer_mode = LayerMode(self._session_zoom, session_zoom_layer)
        self._session_zooming_manager = SessionZoomingManagerComponent(self._modes, is_enabled=False)
        session_zooming_button_layer_mode = LayerMode(self._session_zooming_manager, Layer(session_zooming_button=self._midimap[u'Session_Mode_Button']))
        self._prioritized_session_zooming_button_layer_mode = LayerMode(self._session_zooming_manager, Layer(session_zooming_button=self._midimap[u'Session_Mode_Button'], priority=1))
        self._session_zooming_background = BackgroundComponent(name=u'Session_Zooming_Background')
        session_zooming_background_layer_mode = LayerMode(self._session_zooming_background, Layer(scene_launch_buttons=self._midimap[u'Scene_Launch_Button_Matrix'], delete_button=self._midimap[u'Delete_Button'], quantize_button=self._midimap[u'Quantize_Button'], duplicate_button=self._midimap[u'Duplicate_Button'], double_loop_button=self._midimap[u'Double_Loop_Button']))
        self._modes.add_mode(u'session_zooming_mode', [self._session_zooming_manager,
         session_zooming_button_layer_mode,
         session_zooming_layer_mode,
         session_zooming_background_layer_mode])
        self._modes.add_mode(u'prioritized_session_zooming_mode', [partial(self._layout_switch, consts.SESSION_LAYOUT_SYSEX_BYTE),
         self._session_zooming_manager,
         self._prioritized_session_zooming_button_layer_mode,
         session_zooming_layer_mode,
         session_zooming_background_layer_mode,
         self.update])

    def _create_session_mode(self):
        self._modes.add_mode(u'session_mode', [partial(self._layout_setup, consts.SESSION_LAYOUT_SYSEX_BYTE), self._session_layer_mode, self._session.update_navigation_buttons], behaviour=CancelingReenterBehaviour(u'session_zooming_mode'))

    def _create_note_modes(self):
        note_mode_matrix_translation = self._create_translation(u'Note_Mode_Matrix_Translation', consts.CHROM_MAP_CHANNEL, Layer(button_matrix=self._midimap[u'Main_Button_Matrix'], note_button_matrix=self._midimap[u'Note_Button_Matrix'], drum_matrix=self._midimap[u'Drum_Button_Matrix'], mixer_button_matrix=self._midimap[u'Mixer_Button_Matrix']), should_enable=False)
        note_mode_scene_launch_translation = self._create_translation(u'Note_Mode_Scene_Launch_Translation', consts.CHROM_MAP_CHANNEL, Layer(scene_launch_buttons=self._midimap[u'Scene_Launch_Button_Matrix']))
        scale_setup_mode_button_lighting = LedLightingComponent(name=u'LED_Lighting_Component', is_enabled=False, layer=Layer(button=self._midimap.with_shift(u'Note_Mode_Button')))
        drum_mode_note_matrix_translation = self._create_translation(u'Drum_Mode_Note_Button_Translation', 0, Layer(note_button_matrix=self._midimap[u'Note_Button_Matrix']), should_enable=False, should_reset=False)
        drum_group_layer_mode = LayerMode(self._drum_group, layer=Layer(scroll_up_button=self._midimap[u'Arrow_Left_Button'], scroll_down_button=self._midimap[u'Arrow_Right_Button'], scroll_page_up_button=self._midimap[u'Arrow_Up_Button'], scroll_page_down_button=self._midimap[u'Arrow_Down_Button'], drum_matrix=self._midimap[u'Drum_Button_Matrix'], select_button=self._midimap[u'Shift_Button'], delete_button=self._midimap[u'Delete_Button']))
        self._note_modes = SpecialModesComponent(name=u'Note_Modes')
        self._note_modes.add_mode(u'chromatic_mode', [partial(self._layout_setup, consts.NOTE_LAYOUT_SYSEX_BYTE),
         self._clip_delete_layer_mode,
         note_mode_matrix_translation,
         scale_setup_mode_button_lighting])
        self._note_modes.add_mode(u'drum_mode', [partial(self._layout_setup, consts.DRUM_LAYOUT_SYSEX_BYTE),
         self._setup_drum_group,
         drum_group_layer_mode,
         drum_mode_note_matrix_translation])
        self._note_modes.add_mode(u'audio_mode', [partial(self._layout_setup, consts.AUDIO_LAYOUT_SYSEX_BYTE), self._clip_delete_layer_mode])
        self._note_modes.set_enabled(False)
        self._modes.add_mode(u'note_mode', [note_mode_scene_launch_translation,
         self._note_modes,
         self._select_note_mode,
         self._select_target_track,
         self._clip_actions_component,
         self._show_playing_clip,
         self._set_clip_actions_type], behaviour=ReenterBehaviour(self.toggle_detail_view))
        self._session_record.set_modes_component(self._modes)
        self._session_record.set_note_mode_name(u'note_mode')

    def _create_device_mode(self):
        device_mode_scene_launch_translation = self._create_translation(u'Device_Mode_Scene_Launch_Translation', consts.DEVICE_MAP_CHANNEL, Layer(scene_launch_buttons=self._midimap[u'Scene_Launch_Button_Matrix']))
        device_layer_mode = LayerMode(self._device, layer=Layer(parameter_controls=self._midimap[u'Slider_Button_Matrix']))
        device_nav_layer_mode = LayerMode(self._device_navigation, layer=Layer(device_nav_left_button=self._midimap[u'Arrow_Left_Button'], device_nav_right_button=self._midimap[u'Arrow_Right_Button']))
        device_background_layer_mode = LayerMode(self._device_background, layer=Layer(arrow_up_button=self._midimap[u'Arrow_Up_Button'], arrow_down_button=self._midimap[u'Arrow_Down_Button']))
        self._modes.add_mode(u'device_mode', [partial(self._layout_setup, consts.FADER_LAYOUT_SYSEX_BYTE),
         self._device,
         device_layer_mode,
         device_nav_layer_mode,
         device_background_layer_mode,
         self._clip_actions_component,
         self._clip_delete_layer_mode,
         device_mode_scene_launch_translation,
         self._show_playing_clip,
         self._set_clip_actions_type], behaviour=ReenterBehaviour(self.toggle_detail_view))

    def _create_user_mode(self):
        self._modes.add_mode(u'user_mode', [partial(self._layout_setup, consts.USER_LAYOUT_SYSEX_BYTE)])

    def _create_record_arm_mode(self):
        arm_layer_mode = LayerMode(self._mixer, layer=Layer(arm_buttons=self._midimap[u'Mixer_Button_Matrix']))
        self._modes.add_mode(u'record_arm_mode', [partial(self._layout_setup, consts.SESSION_LAYOUT_SYSEX_BYTE),
         self._session_layer_mode,
         arm_layer_mode,
         self._session_zooming_manager,
         self._prioritized_session_zooming_button_layer_mode,
         self._session.update_navigation_buttons], behaviour=SpecialReenterBehaviour(u'session_mode'))

    def _create_track_select_mode(self):
        track_select_layer_mode = LayerMode(self._mixer, layer=Layer(track_select_buttons=self._midimap[u'Mixer_Button_Matrix']))
        self._modes.add_mode(u'track_select_mode', [partial(self._layout_setup, consts.SESSION_LAYOUT_SYSEX_BYTE),
         self._session_layer_mode,
         track_select_layer_mode,
         self._session_zooming_manager,
         self._prioritized_session_zooming_button_layer_mode,
         self._session.update_navigation_buttons], behaviour=SpecialReenterBehaviour(u'session_mode'))

    def _create_mute_mode(self):
        mute_layer_mode = LayerMode(self._mixer, layer=Layer(mute_buttons=self._midimap[u'Mixer_Button_Matrix']))
        self._modes.add_mode(u'mute_mode', [partial(self._layout_setup, consts.SESSION_LAYOUT_SYSEX_BYTE),
         self._session_layer_mode,
         mute_layer_mode,
         self._session_zooming_manager,
         self._prioritized_session_zooming_button_layer_mode,
         self._session.update_navigation_buttons], behaviour=SpecialReenterBehaviour(u'session_mode'))

    def _create_solo_mode(self):
        solo_layer_mode = LayerMode(self._mixer, layer=Layer(solo_buttons=self._midimap[u'Mixer_Button_Matrix']))
        self._modes.add_mode(u'solo_mode', [partial(self._layout_setup, consts.SESSION_LAYOUT_SYSEX_BYTE),
         self._session_layer_mode,
         solo_layer_mode,
         self._session_zooming_manager,
         self._prioritized_session_zooming_button_layer_mode,
         self._session.update_navigation_buttons], behaviour=SpecialReenterBehaviour(u'session_mode'))

    def _create_volume_mode(self):
        volume_mode_scene_launch_translation = self._create_translation(u'Volume_Mode_Scene_Launch_Translation', consts.VOLUME_MAP_CHANNEL, Layer(scene_launch_buttons=self._midimap[u'Scene_Launch_Button_Matrix']))
        volume_layer_mode = LayerMode(self._mixer, layer=Layer(volume_controls=self._midimap[u'Slider_Button_Matrix']))
        self._modes.add_mode(u'volume_mode', [partial(self._layout_setup, consts.FADER_LAYOUT_SYSEX_BYTE),
         volume_layer_mode,
         self._action_button_background_layer_mode,
         self._session_zooming_manager,
         self._prioritized_session_zooming_button_layer_mode,
         volume_mode_scene_launch_translation,
         self._session.update_navigation_buttons], behaviour=SpecialReenterBehaviour(u'session_mode'))

    def _create_pan_mode(self):
        pan_mode_scene_launch_translation = self._create_translation(u'Pan_Mode_Scene_Launch_Translation', consts.PAN_MAP_CHANNEL, Layer(scene_launch_buttons=self._midimap[u'Scene_Launch_Button_Matrix']))
        pan_layer_mode = LayerMode(self._mixer, layer=Layer(pan_controls=self._midimap[u'Slider_Button_Matrix']))
        self._modes.add_mode(u'pan_mode', [partial(self._layout_setup, consts.FADER_LAYOUT_SYSEX_BYTE),
         pan_layer_mode,
         self._action_button_background_layer_mode,
         self._session_zooming_manager,
         self._prioritized_session_zooming_button_layer_mode,
         pan_mode_scene_launch_translation,
         self._session.update_navigation_buttons], behaviour=SpecialReenterBehaviour(u'session_mode'))

    def _create_sends_mode(self):
        send_layer_mode = LayerMode(self._mixer, layer=Layer(send_controls=self._midimap[u'Slider_Button_Matrix'], send_select_buttons=self._midimap[u'Scene_Launch_Button_Matrix']))
        self._modes.add_mode(u'sends_mode', [partial(self._layout_setup, consts.FADER_LAYOUT_SYSEX_BYTE),
         send_layer_mode,
         self._action_button_background_layer_mode,
         self._session_zooming_manager,
         self._prioritized_session_zooming_button_layer_mode,
         self._session.update_navigation_buttons], behaviour=SpecialReenterBehaviour(u'session_mode'))

    def _create_stop_clips_mode(self):
        stop_layer_mode = AddLayerMode(self._session, Layer(stop_track_clip_buttons=self._midimap[u'Mixer_Button_Matrix'], stop_scene_clip_buttons=self._midimap[u'Scene_Stop_Button_Matrix'], stop_all_clips_button=self._midimap[u'Stop_All_Clips_Button']))
        self._modes.add_mode(u'stop_clip_mode', [partial(self._layout_setup, consts.SESSION_LAYOUT_SYSEX_BYTE),
         self._session_layer_mode,
         stop_layer_mode,
         self._session_zooming_manager,
         self._prioritized_session_zooming_button_layer_mode,
         self._session.update_navigation_buttons], behaviour=SpecialReenterBehaviour(u'session_mode'))

    def toggle_detail_view(self):
        view = self.application().view
        if view.is_view_visible(u'Detail'):
            if view.is_view_visible(u'Detail/DeviceChain'):
                view.show_view(u'Detail/Clip')
            else:
                view.show_view(u'Detail/DeviceChain')

    def _create_user(self):
        self._user_matrix_component = UserMatrixComponent(name=u'User_Matrix_Component', is_enabled=False, layer=Layer(user_button_matrix_ch_6=self._midimap[u'User_Button_Matrix_Ch_6'], user_button_matrix_ch_7=self._midimap[u'User_Button_Matrix_Ch_7'], user_button_matrix_ch_8=self._midimap[u'User_Button_Matrix_Ch_8'], user_button_matrix_ch_14=self._midimap[u'User_Button_Matrix_Ch_14'], user_button_matrix_ch_15=self._midimap[u'User_Button_Matrix_Ch_15'], user_button_matrix_ch_16=self._midimap[u'User_Button_Matrix_Ch_16'], user_left_side_button_matrix_ch_6=self._midimap[u'User_Left_Side_Button_Matrix_Ch_6'], user_left_side_button_matrix_ch_7=self._midimap[u'User_Left_Side_Button_Matrix_Ch_7'], user_left_side_button_matrix_ch_8=self._midimap[u'User_Left_Side_Button_Matrix_Ch_8'], user_left_side_button_matrix_ch_14=self._midimap[u'User_Left_Side_Button_Matrix_Ch_14'], user_left_side_button_matrix_ch_15=self._midimap[u'User_Left_Side_Button_Matrix_Ch_15'], user_left_side_button_matrix_ch_16=self._midimap[u'User_Left_Side_Button_Matrix_Ch_16'], user_right_side_button_matrix_ch_6=self._midimap[u'User_Right_Side_Button_Matrix_Ch_6'], user_right_side_button_matrix_ch_7=self._midimap[u'User_Right_Side_Button_Matrix_Ch_7'], user_right_side_button_matrix_ch_8=self._midimap[u'User_Right_Side_Button_Matrix_Ch_8'], user_right_side_button_matrix_ch_14=self._midimap[u'User_Right_Side_Button_Matrix_Ch_14'], user_right_side_button_matrix_ch_15=self._midimap[u'User_Right_Side_Button_Matrix_Ch_15'], user_right_side_button_matrix_ch_16=self._midimap[u'User_Right_Side_Button_Matrix_Ch_16'], user_bottom_button_matrix_ch_6=self._midimap[u'User_Bottom_Button_Matrix_Ch_6'], user_bottom_button_matrix_ch_7=self._midimap[u'User_Bottom_Button_Matrix_Ch_7'], user_bottom_button_matrix_ch_8=self._midimap[u'User_Bottom_Button_Matrix_Ch_8'], user_bottom_button_matrix_ch_14=self._midimap[u'User_Bottom_Button_Matrix_Ch_14'], user_bottom_button_matrix_ch_15=self._midimap[u'User_Bottom_Button_Matrix_Ch_15'], user_bottom_button_matrix_ch_16=self._midimap[u'User_Bottom_Button_Matrix_Ch_16'], user_arrow_button_matrix_ch_6=self._midimap[u'User_Arrow_Button_Matrix_Ch_6'], user_arrow_button_matrix_ch_7=self._midimap[u'User_Arrow_Button_Matrix_Ch_7'], user_arrow_button_matrix_ch_8=self._midimap[u'User_Arrow_Button_Matrix_Ch_8'], user_arrow_button_matrix_ch_14=self._midimap[u'User_Arrow_Button_Matrix_Ch_14'], user_arrow_button_matrix_ch_15=self._midimap[u'User_Arrow_Button_Matrix_Ch_15'], user_arrow_button_matrix_ch_16=self._midimap[u'User_Arrow_Button_Matrix_Ch_16']))
        self._user_matrix_component.set_enabled(True)

    @subject_slot(u'drum_group')
    def _on_drum_group_changed(self):
        if self._note_modes.selected_mode == u'drum_mode':
            self._drum_group.set_drum_group_device(self._drum_group_finder.drum_group)
        if self._modes.selected_mode == u'note_mode':
            self._select_note_mode()
        else:
            self.release_controlled_track()
        self._update_note_mode_button(self._drum_group_finder.drum_group is not None)

    def _select_note_mode(self):
        u"""
        Selects which note mode to use depending on the kind of
        current target track and its device chain.  Will also
        select the target if specified.
        """
        track = self._target_track_component.target_track
        drum_device = self._drum_group_finder.drum_group
        if track is None or track.is_foldable or track in self.song().return_tracks or track == self.song().master_track or track.is_frozen or track.has_audio_input:
            self._note_modes.selected_mode = u'audio_mode'
        elif drum_device:
            self._note_modes.selected_mode = u'drum_mode'
        else:
            self._note_modes.selected_mode = u'chromatic_mode'
        self._modes.update()
        if self._note_modes.selected_mode == u'audio_mode':
            self.release_controlled_track()
        else:
            self.set_controlled_track(self._target_track_component.target_track)

    def _select_target_track(self):
        track = self._target_track_component.target_track
        if track != self.song().view.selected_track:
            self.song().view.selected_track = track

    def _update_note_mode_button(self, focused_track_is_drum_track):
        button = self._midimap[u'Note_Mode_Button']
        if focused_track_is_drum_track:
            button.default_states = {True: u'Mode.Drum.On',
             False: u'Mode.Drum.Off'}
        else:
            button.default_states = {True: u'Mode.Chromatic.On',
             False: u'Mode.Chromatic.Off'}
        button.reset_state()
        self._modes.update()

    def _show_playing_clip(self):
        track = None
        if self._use_sel_track():
            track = self.song().view.selected_track
        else:
            track = self._target_track_component.target_track
        if track in self.song().tracks:
            slot_index = track.fired_slot_index
            if slot_index < 0:
                slot_index = track.playing_slot_index
            if slot_index >= 0:
                clip_slot = track.clip_slots[slot_index]
                self.song().view.highlighted_clip_slot = clip_slot

    def _set_clip_actions_type(self):
        self._clip_actions_component.use_selected_track(self._use_sel_track())
        self._clip_actions_component.update()

    def _use_sel_track(self):
        return self._modes.selected_mode == u'device_mode'

    def _should_arm_track(self):
        return self._modes.selected_mode == u'record_arm_mode'

    @subject_slot(u'selected_mode')
    def _on_layout_changed(self, mode):
        if mode == u'note_mode':
            self.set_controlled_track(self._target_track_component.target_track)
        else:
            self.release_controlled_track()
        self._session_record.set_enabled(mode != u'user_mode')

    @subject_slot(u'session_record')
    def _on_session_record_changed(self):
        status = self.song().session_record
        feedback_color = int(self._skin[u'Instrument.FeedbackRecord'] if status else self._skin[u'Instrument.Feedback'])
        self._c_instance.set_feedback_velocity(feedback_color)

    def _clear_send_cache(self):
        with self.component_guard():
            for control in self.controls:
                control.clear_send_cache()

    def _update_hardware(self):
        self._clear_send_cache()
        self.update()

    def _update_global_components(self):
        self._actions_component.update()
        self._session_record.update()
        self._modifier_background_component.update()

    def _layout_setup(self, mode):
        self._layout_switch(mode)
        self._clear_send_cache()
        self._update_global_components()

    def _layout_switch(self, mode):
        prefix = consts.SYSEX_STANDARD_PREFIX + consts.SYSEX_PARAM_BYTE_LAYOUT
        suffix = consts.SYSEX_STANDARD_SUFFIX
        self._send_midi(prefix + mode + suffix)
        self._last_sent_mode_byte = mode

    def port_settings_changed(self):
        self.set_highlighting_session_component(None)
        super(Launchpad_Pro, self).port_settings_changed()

    def on_identified(self):
        self._send_challenge()

    def _send_challenge(self):
        challenge_bytes = []
        for index in range(4):
            challenge_bytes.append(self._challenge >> 8 * index & 127)

        challenge = consts.CHALLENGE_PREFIX + tuple(challenge_bytes) + (247,)
        self._send_midi(challenge)

    def _on_handshake_successful(self):
        self._do_send_midi(consts.LIVE_MODE_SWITCH_REQUEST)
        with self.component_guard():
            self._modes.set_enabled(True)
            self._actions_component.set_enabled(True)
            self._session_record.set_enabled(True)
            self._modifier_background_component.set_enabled(True)
            self._shifted_background.set_enabled(True)
            self.release_controlled_track()
            self.set_feedback_channels(consts.FEEDBACK_CHANNELS)
        if self._last_sent_mode_byte is not None:
            self._layout_setup(self._last_sent_mode_byte)
        self.set_highlighting_session_component(self._session)
        self.update()

    def _is_challenge_response(self, midi_bytes):
        return len(midi_bytes) == 10 and midi_bytes[:7] == consts.SYSEX_STANDARD_PREFIX + consts.SYSEX_CHALLENGE_RESPONSE_BYTE

    def _is_response_valid(self, midi_bytes):
        response = int(midi_bytes[7])
        response += int(midi_bytes[8] << 8)
        return response == Live.Application.encrypt_challenge2(self._challenge)

    def handle_sysex(self, midi_bytes):
        if len(midi_bytes) < 7:
            pass
        elif self._is_challenge_response(midi_bytes) and self._is_response_valid(midi_bytes):
            self._on_handshake_successful()
        elif midi_bytes[6] == consts.SYSEX_STATUS_BYTE_LAYOUT and midi_bytes[7] == consts.NOTE_LAYOUT_SYSEX_BYTE[0]:
            self._update_hardware()
        elif midi_bytes[6] in (consts.SYSEX_STATUS_BYTE_MODE, consts.SYSEX_STATUS_BYTE_LAYOUT):
            pass
        else:
            super(Launchpad_Pro, self).handle_sysex(midi_bytes)
