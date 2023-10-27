# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\mappings.py
# Compiled at: 2023-09-17 09:50:55
# Size of source mod 2**32: 8863 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import ACTIVE_PARAMETER_TIMEOUT, LOW_PRIORITY
from ableton.v3.control_surface.mode import LatchingBehaviour, MomentaryBehaviour, make_reenter_behaviour

def create_mappings(control_surface):
    mappings = {}
    mappings['Modifier_Background'] = dict(clear_button='clear_button',
      duplicate_button='duplicate_button',
      quantize_button='quantize_button')
    mappings['Settings'] = dict(fixed_length_button='fixed_length_button')
    mappings['Active_Parameter'] = dict(touch_controls='touch_elements')
    mappings['Transport'] = dict(stop_button='stop_button',
      tap_tempo_button='tempo_button',
      record_quantize_button='quantize_button_with_shift')
    mappings['Mixer'] = dict(shift_button='shift_button')
    mappings['Session'] = dict(select_button='shift_button',
      delete_button='clear_button',
      duplicate_button='duplicate_button',
      scene_launch_buttons='scene_launch_buttons')
    mappings['View_Control'] = dict(prev_track_button='left_button',
      next_track_button='right_button',
      prev_track_page_button='left_button_with_shift',
      next_track_page_button='right_button_with_shift')
    mappings['Render_To_Clip'] = dict(start_control='render_to_clip_start_element',
      data_control='render_to_clip_data_element',
      end_control='render_to_clip_end_element')
    mappings['Touch_Strip_Modes'] = dict(default_behaviour=(LatchingBehaviour()),
      device_button='device_button',
      volume_button='volume_button',
      pan_button='pan_button',
      send_button='send_button',
      channel_strip_button='channel_strip_button',
      off_button='off_button',
      device=dict(modes=[
     dict(component='Device',
       parameter_controls='touch_strips',
       prev_bank_button='up_button_with_device',
       next_bank_button='down_button_with_device'),
     dict(component='Device_Navigation',
       prev_button='left_button_with_device',
       next_button='right_button_with_device')]),
      volume=dict(component='Mixer', volume_controls='touch_strips'),
      pan=dict(component='Mixer', pan_controls='touch_strips'),
      send=dict(component='Mixer',
      send_controls='touch_strips',
      behaviour=make_reenter_behaviour(LatchingBehaviour,
      on_reenter=(control_surface.component_map['Mixer'].cycle_send_index))),
      channel_strip=dict(component='Mixer',
      target_track_volume_control='touch_strips_raw[0]',
      target_track_pan_control='touch_strips_raw[1]',
      target_track_send_controls='touch_strips_2_thru_7',
      behaviour=make_reenter_behaviour(LatchingBehaviour,
      on_reenter=(control_surface.component_map['Mixer'].target_strip.cycle_send_index))),
      off=None)
    mappings['Encoder_Modes'] = dict(default_behaviour=MomentaryBehaviour(entry_delay=0.1),
      tempo_button='tempo_button',
      fixed_length_button='fixed_length_button',
      quantize_button='quantize_button',
      swing_button='tempo_button_with_shift',
      default=dict(modes=[
     dict(component='View_Control',
       track_encoder='encoder',
       priority=LOW_PRIORITY),
     dict(component='View_Control', track_page_encoder='encoder_with_shift'),
     dict(component='Transport', metronome_button='encoder_button')]),
      tempo=dict(component='Transport',
      tempo_coarse_encoder='encoder',
      behaviour=MomentaryBehaviour(entry_delay=0,
      immediate_exit_delay=ACTIVE_PARAMETER_TIMEOUT)),
      fixed_length=dict(component='Settings', fixed_length_encoder='encoder'),
      quantize=dict(component='Settings', quantization_encoder='encoder'),
      swing=dict(modes=[], behaviour=(MomentaryBehaviour())))
    mappings['Track_State_Modes'] = dict(default_behaviour=(LatchingBehaviour()),
      mute_button='mute_button',
      arm_button='record_arm_button',
      solo_button='solo_button',
      clip_stop_button='clip_stop_button',
      mute=dict(component='Mixer', mute_buttons='track_state_buttons'),
      arm=dict(component='Mixer', arm_buttons='track_state_buttons'),
      solo=dict(component='Mixer', solo_buttons='track_state_buttons'),
      clip_stop=dict(component='Session',
      stop_track_clip_buttons='track_state_buttons'))
    session_navigation = dict(component='Session_Navigation',
      up_button='up_button',
      down_button='down_button',
      left_button='left_button',
      right_button='right_button',
      page_up_button='up_button_with_shift',
      page_down_button='down_button_with_shift',
      page_left_button='left_button_with_shift',
      page_right_button='right_button_with_shift')
    encoder_background = dict(component='Background',
      bg_encoder='encoder',
      encoder_with_shift='encoder_with_shift')
    mappings['Pad_Modes'] = dict(mode_selection_control='firmware_mode_element',
      session=dict(modes=[
     dict(component='Session', clip_launch_buttons='pads'),
     session_navigation]),
      session_overview=dict(modes=[
     dict(component='Session_Overview', matrix='pads'),
     session_navigation.copy()]),
      note=None,
      chord=None,
      note_config=None,
      drum=dict(component='Drum_Group',
      matrix='pads',
      scroll_up_button='up_button',
      scroll_down_button='down_button',
      scroll_page_up_button='up_button_with_shift',
      scroll_page_down_button='down_button_with_shift',
      select_button='shift_button',
      delete_button='clear_button'),
      step_seq=encoder_background,
      step_seq_config=(encoder_background.copy()),
      project=None,
      custom=dict(component='Background', bg_touch_elements='touch_elements'),
      globals=None)
    mappings['Global_Modes'] = dict(shift_button='shift_button',
      default=dict(modes=[
     dict(component='View_Based_Recording', record_button='record_button'),
     dict(component='Transport', play_button='play_button'),
     dict(component='Undo_Redo', undo_button='undo_button'),
     dict(component='Session', quantize_button='quantize_button'),
     dict(component='Mixer', track_select_buttons='track_select_buttons')]),
      shift=dict(modes=[
     dict(component='View_Based_Recording', overdub_button='record_button'),
     dict(component='Transport', play_pause_button='play_button'),
     dict(component='Undo_Redo', redo_button='undo_button'),
     dict(component='Session',
       stop_all_clips_button='scene_launch_buttons_raw[7]'),
     dict(component='Global_Quantization',
       rate_buttons='track_select_buttons')],
      behaviour=(MomentaryBehaviour())))
    return mappings