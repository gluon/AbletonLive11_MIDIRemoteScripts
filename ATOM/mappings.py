from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import LOW_PRIORITY
from ableton.v3.control_surface.mode import LatchingBehaviour, MomentaryBehaviour

def create_mappings(control_surface):
    mappings = {}
    mappings['Modifier_Background'] = dict(shift='shift_button')
    mappings['Undo_Redo'] = dict(undo_button='stop_button_with_shift')
    mappings['View_Toggle'] = dict(detail_view_toggle_button='show_hide_button',
      main_view_toggle_button='preset_button')
    mappings['Transport'] = dict(play_button='play_button',
      loop_button='play_button_with_shift',
      stop_button='stop_button',
      metronome_button='click_button',
      view_based_record_button='record_button')
    mappings['Session_Navigation_Modes'] = dict(cycle_mode_button='bank_button',
      default=dict(component='Session_Navigation',
      up_button='up_button',
      down_button='down_button',
      left_button='left_button',
      right_button='right_button',
      priority=LOW_PRIORITY),
      paged=dict(component='Session_Navigation',
      page_up_button='up_button',
      page_down_button='down_button',
      page_left_button='left_button',
      page_right_button='right_button',
      priority=LOW_PRIORITY))
    mappings['Encoder_Modes'] = dict(volume=dict(component='Mixer', volume_controls='encoders'),
      pan=dict(component='Mixer', pan_controls='encoders'),
      send_a=dict(component='Mixer', send_a_controls='encoders'),
      send_b=dict(component='Mixer', send_b_controls='encoders'))
    mappings['Note_Modes'] = dict(enable=False,
      drum=dict(component='Drum_Group',
      matrix='pads',
      scroll_page_up_button='up_button',
      scroll_page_down_button='down_button'),
      keyboard=dict(component='Keyboard',
      matrix='pads',
      scroll_up_button='up_button',
      scroll_down_button='down_button'))
    mappings['Pad_Modes'] = dict(default_behaviour=(LatchingBehaviour()),
      session_button='full_level_button',
      note_button='note_repeat_button',
      channel_button='select_button',
      encoder_modes_button='setup_button',
      session=dict(modes=[
     dict(component='Background', unused_pads='pads_with_shift'),
     dict(component='Session',
       clip_launch_buttons='pads',
       scene_launch_buttons='pads_column_3_with_shift'),
     dict(component='Session_Overview', matrix='pads_with_zoom'),
     dict(component='Modifier_Background', zoom='zoom_button')]),
      note=dict(component='Note_Modes'),
      channel=dict(modes=[
     dict(component='Mixer',
       arm_buttons='pads_row_0',
       solo_buttons='pads_row_1',
       track_select_buttons='pads_row_2'),
     dict(component='Session', stop_track_clip_buttons='pads_row_3')]),
      encoder_modes=dict(component='Encoder_Modes',
      volume_button='pads_raw[0]',
      pan_button='pads_raw[1]',
      send_a_button='pads_raw[2]',
      send_b_button='pads_raw[3]',
      behaviour=(MomentaryBehaviour())))
    mappings['Top_Level_Modes'] = dict(support_momentary_mode_cycling=False,
      cycle_mode_button='editor_button',
      default=(control_surface.refresh_state),
      user=dict(component='Translating_Background',
      note_repeat_button='note_repeat_button',
      full_level_button='full_level_button',
      bank_button='bank_button',
      preset_button='preset_button',
      show_hide_button='show_hide_button',
      nudge_button='nudge_button',
      set_loop_button='set_loop_button',
      setup_button='setup_button',
      up_button='up_button',
      down_button='down_button',
      left_button='left_button',
      right_button='right_button',
      select_button='select_button',
      click_button='click_button',
      record_button='record_button',
      play_button='play_button',
      stop_button='stop_button',
      pads='pads',
      encoders='encoders'))
    return mappings