# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC_Key_25_mk2\mappings.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 3335 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import HIGH_PRIORITY
from ableton.v3.control_surface.mode import ImmediateBehaviour, MomentaryBehaviour, make_reenter_behaviour

def create_mappings(control_surface):
    mappings = {}
    mappings['Transport'] = dict(play_toggle_button='play_button')
    mappings['Session'] = dict(clip_launch_buttons='clip_launch_buttons',
      stop_all_clips_button='stop_all_clips_button',
      clip_slot_select_button='shift_button')
    mappings['Track_Button_Modes'] = dict(clip_stop=dict(component='Session', stop_track_clip_buttons='track_buttons'),
      solo=dict(component='Mixer', solo_buttons='track_buttons'),
      mute=dict(component='Mixer', mute_buttons='track_buttons'),
      arm=dict(component='Mixer', arm_buttons='track_buttons'),
      track_select=dict(component='Mixer', track_select_buttons='track_buttons'))
    mappings['Encoder_Modes'] = dict(volume=dict(component='Mixer', volume_controls='encoders'),
      pan=dict(component='Mixer', pan_controls='encoders'),
      send=dict(component='Mixer',
      send_controls='encoders',
      behaviour=make_reenter_behaviour(ImmediateBehaviour,
      on_reenter=(control_surface.component_map['Mixer'].cycle_send_index))),
      device=dict(component='Device', parameter_controls='encoders'))
    mappings['Main_Modes'] = dict(shift_button='shift_button',
      default=dict(modes=[
     dict(component='View_Based_Recording', record_button='record_button'),
     dict(component='Session', scene_launch_buttons='scene_launch_buttons')]),
      shift=dict(modes=[
     dict(component='Transport', capture_midi_button='record_button'),
     dict(component='Track_Button_Modes',
       clip_stop_button='scene_launch_buttons_raw[0]',
       solo_button='scene_launch_buttons_raw[1]',
       mute_button='scene_launch_buttons_raw[2]',
       arm_button='scene_launch_buttons_raw[3]',
       track_select_button='scene_launch_buttons_raw[4]'),
     dict(component='Session_Navigation',
       up_button='track_buttons_raw[0]',
       down_button='track_buttons_raw[1]',
       left_button='track_buttons_raw[2]',
       right_button='track_buttons_raw[3]',
       priority=HIGH_PRIORITY),
     dict(component='Encoder_Modes',
       volume_button='track_buttons_raw[4]',
       pan_button='track_buttons_raw[5]',
       send_button='track_buttons_raw[6]',
       device_button='track_buttons_raw[7]',
       priority=HIGH_PRIORITY)],
      behaviour=(MomentaryBehaviour())))
    return mappings