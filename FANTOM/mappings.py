# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\FANTOM\mappings.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 2277 bytes
from __future__ import absolute_import, print_function, unicode_literals

def create_mappings(_):
    mappings = {}
    mappings['Undo_Redo'] = dict(undo_button='undo_button')
    mappings['Device'] = dict(parameter_controls='device_controls')
    mappings['Drum_Group'] = dict(matrix='drum_pads')
    mappings['Recording'] = dict(arrangement_record_button='record_button',
      arrangement_overdub_button='arrangement_overdub_button',
      session_record_button='session_record_button')
    mappings['Transport'] = dict(play_button='play_button',
      stop_button='stop_button',
      re_enable_automation_button='automation_re-enable_button',
      automation_arm_button='automation_arm_button',
      metronome_button='metronome_button',
      tap_tempo_button='tap_tempo_button',
      capture_midi_button='capture_midi_button',
      tempo_coarse_encoder='tempo_coarse_control',
      tempo_fine_encoder='tempo_fine_control',
      beat_time_display='beat_time_display',
      tempo_display='tempo_display')
    mappings['Mixer'] = dict(volume_controls='volume_controls',
      pan_controls='pan_controls',
      send_a_controls='send_a_controls',
      send_b_controls='send_b_controls',
      track_select_control='track_select_control',
      arm_buttons='arm_buttons',
      solo_buttons='solo_buttons',
      mute_buttons='mute_buttons',
      track_info_display='track_info_display',
      master_track_volume_control='master_volume_control',
      master_track_pan_control='master_pan_control')
    mappings['Session_Navigation'] = dict(up_button='up_button',
      down_button='down_button',
      left_button='left_button',
      right_button='right_button')
    mappings['Session'] = dict(clip_launch_buttons='clip_launch_buttons',
      scene_launch_buttons='scene_launch_buttons',
      stop_track_clip_buttons='stop_track_buttons',
      stop_all_clips_button='stop_all_clips_button',
      track_select_control='track_select_control',
      scene_name_display='scene_name_display')
    return mappings