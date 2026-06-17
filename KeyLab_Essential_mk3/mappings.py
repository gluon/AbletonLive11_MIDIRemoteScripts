# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential_mk3\mappings.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 1888 bytes
from __future__ import absolute_import, print_function, unicode_literals

def create_mappings(_):
    mappings = {}
    mappings['Transport'] = dict(play_button='play_button',
      stop_button='stop_button',
      metronome_button='metronome_button',
      loop_button='loop_button',
      tap_tempo_button='tap_button',
      capture_midi_button='save_button',
      rewind_button='rewind_button',
      fastforward_button='fastforward_button')
    mappings['View_Based_Recording'] = dict(record_button='record_button')
    mappings['Undo_Redo'] = dict(undo_button='undo_button', redo_button='redo_button')
    mappings['Clip_Actions'] = dict(quantize_button='punch_button')
    mappings['View_Control'] = dict(prev_track_button='context_button_2',
      next_track_button='context_button_3',
      scene_encoder='display_encoder')
    mappings['Mixer'] = dict(target_track_arm_button='context_button_1',
      target_track_volume_control='fader_9',
      target_track_pan_control='encoder_9')
    mappings['Session'] = dict(selected_scene_launch_button='display_encoder_button',
      clip_launch_buttons='pad_bank_a')
    mappings['Drum_Group'] = dict(matrix='pad_bank_b')
    mappings['Continuous_Control_Modes'] = dict(support_momentary_mode_cycling=False,
      cycle_mode_button='context_button_0',
      device=dict(component='Device',
      parameter_controls='continuous_controls',
      bank_toggle_button='part_button'),
      mixer=dict(component='Mixer',
      volume_controls='faders',
      pan_controls='encoders',
      bank_toggle_button='part_button'))
    return mappings