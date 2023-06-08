from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import MIDI_NOTE_TYPE, ElementsBase, MapMode, PrioritizedResource, create_matrix_identifiers
from . import sysex
from .scene_name_display import SceneNameDisplayElement
from .simple_display import SimpleDisplayElement
from .track_info_display import TrackInfoDisplayElement
NUM_TRACKS = 6
NUM_SCENES = 8

def create_display_element(header, name=None):
    return SimpleDisplayElement(header, (0, sysex.SYSEX_END_BYTE), name=name)


class Elements(ElementsBase):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self.add_button(1, 'Up_Button')
        self.add_button(2, 'Down_Button')
        self.add_button(3, 'Left_Button')
        self.add_button(4, 'Right_Button')
        self.add_button(64, 'Stop_All_Clips_Button')
        self.add_button(80, 'Play_Button')
        self.add_button(81, 'Stop_Button')
        self.add_button(82, 'Record_Button')
        self.add_button(83, 'Undo_Button')
        self.add_button(84, 'Metronome_Button')
        self.add_button(85, 'Session_Record_Button')
        self.add_button(86, 'Capture_Midi_Button')
        self.add_button(87, 'Automation_Re-enable_Button')
        self.add_button(88, 'Automation_Arm_Button')
        self.add_button(89, 'Arrangement_Overdub_Button')
        self.add_button(91, 'Tap_Tempo_Button')
        track_channels = [i + 1 for i in range(NUM_TRACKS)]
        self.add_button_matrix([
         [
          65] * NUM_TRACKS],
          'Arm_Buttons', channels=[track_channels])
        self.add_button_matrix([
         [
          66] * NUM_TRACKS],
          'Solo_Buttons', channels=[track_channels])
        self.add_button_matrix([
         [
          67] * NUM_TRACKS],
          'Mute_Buttons', channels=[track_channels])
        self.add_button_matrix([
         [
          64] * NUM_SCENES],
          'Stop_Track_Buttons',
          channels=[
         [i + 1 for i in range(NUM_SCENES)]])
        self.add_button_matrix([
         range(NUM_SCENES)],
          'Scene_Launch_Buttons', msg_type=MIDI_NOTE_TYPE)
        self.add_button_matrix(create_matrix_identifiers(8, 56, width=NUM_TRACKS),
          'Clip_Launch_Buttons',
          msg_type=MIDI_NOTE_TYPE)
        self.add_button_matrix(create_matrix_identifiers(60, 76, width=4),
          'Drum_Pads',
          msg_type=MIDI_NOTE_TYPE,
          channels=9)
        self.add_encoder(34, 'Tempo_Coarse_Control', map_mode=(MapMode.LinearBinaryOffset))
        self.add_encoder(35, 'Tempo_Fine_Control', map_mode=(MapMode.LinearBinaryOffset))
        self.add_encoder(72, 'Master_Pan_Control', is_feedback_enabled=True)
        self.add_encoder(73, 'Master_Volume_Control', is_feedback_enabled=True)
        self.add_encoder(96, 'Track_Select_Control', resource_type=PrioritizedResource)
        self.add_encoder_matrix([
         [i + 16 for i in range(8)]],
          'Device_Controls', is_feedback_enabled=True)
        self.add_encoder_matrix([
         [
          72] * NUM_TRACKS],
          'Pan_Controls',
          channels=[
         track_channels],
          needs_takeover=False,
          is_feedback_enabled=True)
        self.add_encoder_matrix([
         [
          73] * NUM_TRACKS],
          'Volume_Controls',
          channels=[
         track_channels],
          needs_takeover=False,
          is_feedback_enabled=True)
        self.add_encoder_matrix([
         [
          74] * NUM_TRACKS, [75] * NUM_TRACKS],
          'Send_Controls',
          channels=[
         track_channels, track_channels],
          needs_takeover=False,
          is_feedback_enabled=True)
        for control in self.send_controls_raw:
            control.name = 'Send_{}_Control_{}'.format('A' if control.message_identifier() == 74 else 'B', control.name[0])

        self.add_submatrix((self.send_controls), 'Send_A_Controls', rows=(0, 1))
        self.add_submatrix((self.send_controls), 'Send_B_Controls', rows=(1, 2))
        self.add_element('Beat Time Display', create_display_element, sysex.BEAT_TIME_DISPLAY_HEADER)
        self.add_element('Tempo Display', create_display_element, sysex.TEMPO_DISPLAY_HEADER)
        self.add_element('Track_Info_Display', TrackInfoDisplayElement, sysex.TRACK_INFO_DISPLAY_HEADER, (
         sysex.SYSEX_END_BYTE,))
        self.add_element('Scene_Name_Display', SceneNameDisplayElement, sysex.SCENE_NAME_DISPLAY_HEADER, (
         sysex.SYSEX_END_BYTE,))

    def add_encoder(self, *a, **k):
        (super().add_encoder)(a, needs_takeover=False, **k)