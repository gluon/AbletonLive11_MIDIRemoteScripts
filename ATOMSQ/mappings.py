from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.mode import LatchingBehaviour

def create_mappings(_):
    mappings = {}
    mappings['Button_Labels'] = dict(display_lines='button_label_displays')
    mappings['Simple_Device'] = dict(device_name_display='device_name_display')
    mappings['Mixer'] = dict(target_track_track_name_display='track_name_display')
    mappings['Modifier_Background'] = dict(shift='shift_button')
    mappings['Undo_Redo'] = dict(undo_button='stop_button_with_shift')
    mappings['Session_Navigation'] = dict(up_button='up_button_with_shift',
      down_button='down_button_with_shift')
    mappings['View_Control'] = dict(next_track_button='right_button',
      prev_track_button='left_button',
      next_scene_button='down_button',
      prev_scene_button='up_button')
    mappings['Transport'] = dict(arrangement_position_encoder='display_encoder',
      tempo_coarse_encoder='display_encoder_with_shift',
      play_button='play_button',
      loop_button='play_button_with_shift',
      stop_button='stop_button',
      view_based_record_button='record_button',
      metronome_button='click_button',
      capture_midi_button='record_button_with_shift',
      prev_cue_button='display_left_button',
      next_cue_button='display_right_button')
    mappings['Lower_Pad_Modes'] = dict(enable=False,
      cycle_mode_button='minus_button',
      select=dict(component='Mixer', track_select_buttons='lower_pads'),
      stop=dict(component='Session', stop_track_clip_buttons='lower_pads'))
    mappings['Main_Modes'] = dict(default_behaviour=(LatchingBehaviour()),
      song_button='song_mode_button',
      instrument_button='instrument_mode_button',
      editor_button='editor_mode_button',
      user_button='user_mode_button',
      instrument=dict(component='Simple_Device', parameter_controls='encoders'),
      song=dict(modes=[
     dict(component='Lower_Pad_Modes'),
     dict(component='View_Toggle',
       main_view_toggle_button='bank_a_button',
       browser_view_toggle_button='bank_b_button',
       detail_view_toggle_button='bank_d_button',
       clip_view_toggle_button='bank_h_button'),
     dict(component='Launch_And_Stop',
       clip_launch_button='display_buttons_raw[3]',
       scene_launch_button='display_buttons_raw[4]',
       track_stop_button='display_buttons_raw[5]'),
     dict(component='Session',
       clip_launch_buttons='upper_pads',
       scene_0_launch_button='plus_button'),
     dict(component='Mixer',
       target_track_volume_control='encoders_raw[0]',
       target_track_pan_control='encoders_raw[1]',
       target_track_send_controls='encoders_2_thru_7',
       target_track_solo_button='display_buttons_raw[0]',
       target_track_mute_button='display_buttons_raw[1]',
       target_track_arm_button='display_buttons_raw[2]',
       crossfader_control='touch_strip')]),
      editor=dict(modes=[
     dict(component='Simple_Device', parameter_controls='encoders'),
     dict(component='Device_Navigation',
       prev_button='display_buttons_raw[1]',
       next_button='display_buttons_raw[2]'),
     dict(component='Simple_Device',
       device_lock_button='display_buttons_raw[0]',
       device_on_off_button='display_buttons_raw[3]',
       prev_bank_button='display_buttons_raw[4]',
       next_bank_button='display_buttons_raw[5]')]),
      user=dict(component='Translating_Background',
      encoders='encoders',
      channel_selection_buttons='display_buttons'))
    return mappings