# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Generic\GenericScript.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 17117 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from future.utils import iteritems
from functools import partial
import Live
import _Framework.ButtonElement as ButtonElement
import _Framework.ButtonMatrixElement as ButtonMatrixElement
import _Framework.ControlSurface as ControlSurface
import _Framework.DeviceComponent as DeviceComponent
import _Framework.EncoderElement as EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
import _Framework.Layer as Layer
import _Framework.TransportComponent as TransportComponent
from _Framework.Util import NamedTuple
from .SpecialMixerComponent import SpecialMixerComponent

def is_valid_midi_channel(integer):
    return 0 <= integer < 16


def is_valid_midi_identifier(integer):
    return 0 <= integer < 128


def has_specification_for(control, specifications):
    return is_valid_midi_identifier(specifications.get(control, -1))


class TransportButton(NamedTuple):
    control_name = ''
    layer_name = ''


TRANSPORT_BUTTON_SPECIFICATIONS = {'Stop':TransportButton(control_name='Stop', layer_name='stop'), 
 'Play':TransportButton(control_name='Play', layer_name='play'), 
 'Rec':TransportButton(control_name='Record', layer_name='record'), 
 'SessionRec':TransportButton(control_name='Session_Record', layer_name='overdub'), 
 'Over':TransportButton(control_name='Arrangement_Overdub',
   layer_name='arrangement_overdub'), 
 'Metro':TransportButton(control_name='Metronome', layer_name='metronome'), 
 'Loop':TransportButton(control_name='Loop', layer_name='loop'), 
 'Rwd':TransportButton(control_name='Rwd', layer_name='seek_backward'), 
 'Ffwd':TransportButton(control_name='FFwd', layer_name='seek_forward'), 
 'PunchIn':TransportButton(control_name='Punch_In', layer_name='punch_in'), 
 'PunchOut':TransportButton(control_name='Punch_Out', layer_name='punch_out'), 
 'NudgeUp':TransportButton(control_name='Nudge_Up', layer_name='nudge_up'), 
 'NudgeDown':TransportButton(control_name='Nudge_Down', layer_name='nudge_down'), 
 'TapTempo':TransportButton(control_name='Tap_Tempo', layer_name='tap_tempo')}

class GenericScript(ControlSurface):

    def __init__(self, c_instance, macro_map_mode, volume_map_mode, device_controls, transport_controls, volume_controls, trackarm_controls, bank_controls, descriptions=None, mixer_options=None, device_component_class=DeviceComponent):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            global_channel = 0
            if descriptions:
                if 'INPUTPORT' in descriptions:
                    self._suggested_input_port = descriptions['INPUTPORT']
                if 'OUTPUTPORT' in descriptions:
                    self._suggested_output_port = descriptions['OUTPUTPORT']
                if 'CHANNEL' in descriptions:
                    if is_valid_midi_channel(descriptions['CHANNEL']):
                        global_channel = descriptions['CHANNEL']
                if 'PAD_TRANSLATION' in descriptions:
                    self.set_pad_translations(descriptions['PAD_TRANSLATION'])
            self._init_mixer_component(volume_controls, trackarm_controls, mixer_options, global_channel, volume_map_mode)
            self._init_device_component(device_controls, bank_controls, global_channel, macro_map_mode, device_component_class)
            self._init_transport_component(transport_controls, global_channel)

    def handle_sysex(self, midi_bytes):
        pass

    def _init_mixer_component(self, volume_controls, trackarm_controls, mixer_options, global_channel, volume_map_mode):
        momentary_buttons = mixer_options is not None and 'NOTOGGLE' in list(mixer_options.keys())
        sends_map_mode = Live.MidiMap.MapMode.absolute
        if mixer_options:
            if 'SENDMAPMODE' in mixer_options:
                sends_map_mode = mixer_options['SENDMAPMODE']
        MixerButton = partial(ButtonElement, momentary_buttons, MIDI_CC_TYPE, global_channel)

        def make_mixer_encoder(cc, channel, name, map_mode=volume_map_mode):
            if is_valid_midi_identifier(cc):
                if is_valid_midi_channel(channel):
                    return EncoderElement(MIDI_CC_TYPE, channel, cc, map_mode, name=name)

        def make_global_mixer_encoder(identifier_spec, channel_spec, control_name, **k):
            if has_specification_for(identifier_spec, mixer_options):
                channel = global_channel
                if channel_spec in mixer_options:
                    if is_valid_midi_channel(mixer_options[channel_spec]):
                        channel = mixer_options[channel_spec]
                return make_mixer_encoder(
                 (mixer_options[identifier_spec]), channel, control_name, **k)

        def make_mixer_button(control, name):
            return MixerButton((mixer_options[control]), name=name)

        def make_channel_strip_button(control_list, index, name):
            if 0<= index < len(control_list):
                if is_valid_midi_identifier(control_list[index]):
                    return MixerButton((control_list[index]),
                      name=('{}_{}_Button'.format(index, name)))

        if volume_controls is not None:
            if trackarm_controls is not None:
                num_strips = max(len(volume_controls), len(trackarm_controls))
                send_info = []
                mute_controls = []
                solo_controls = []
                select_controls = []
                mixer = SpecialMixerComponent(num_strips,
                  name='Mixer',
                  invert_mute_feedback=(mixer_options and mixer_options.get('INVERTMUTELEDS', True)))
                mixer.master_strip().name = 'Master_Channel_Strip'
                mixer.selected_strip().name = 'Selected_Channel_Strip'
                if mixer_options is not None:
                    master_volume = make_global_mixer_encoder('MASTERVOLUME', 'MASTERVOLUMECHANNEL', 'Master_Volume_Control')
                    if master_volume:
                        mixer.master_strip().layer = Layer(volume_control=master_volume)
                    for send in range(mixer_options.get('NUMSENDS', 0)):
                        send_info.append(mixer_options['SEND{}'.format(send + 1)])

                    layer_specs = {}
                    cue_volume = make_global_mixer_encoder('CUEVOLUME', 'CUEVOLUMECHANNEL', 'Cue_Volume_Control')
                    if cue_volume:
                        layer_specs['prehear_volume_control'] = cue_volume
                    crossfader_map_mode = Live.MidiMap.MapMode.absolute
                    if 'CROSSFADERMAPMODE' in mixer_options:
                        crossfader_map_mode = mixer_options['CROSSFADERMAPMODE']
                    crossfader = make_global_mixer_encoder('CROSSFADER',
                      'CROSSFADERCHANNEL',
                      'Crossfader_Control',
                      map_mode=crossfader_map_mode)
                    if crossfader:
                        layer_specs['crossfader_control'] = crossfader
                        crossfader.set_needs_takeover(False)
                    if has_specification_for('NEXTBANK', mixer_options):
                        layer_specs['bank_up_button'] = make_mixer_button('NEXTBANK', 'Mixer_Next_Bank_Button')
                    if has_specification_for('PREVBANK', mixer_options):
                        layer_specs['bank_down_button'] = make_mixer_button('PREVBANK', 'Mixer_Previous_Bank_Button')
                    mute_controls = mixer_options.get('MUTE', [])
                    solo_controls = mixer_options.get('SOLO', [])
                    select_controls = mixer_options.get('SELECT', [])
                    mixer.layer = Layer(**layer_specs)
                for track in range(num_strips):
                    strip = mixer.channel_strip(track)
                    strip.name = 'Channel_Strip_{}'.format(track)
                    layer_specs = {}
                    if 0<= track < len(volume_controls):
                        channel = global_channel
                        cc = volume_controls[track]
                        if isinstance(volume_controls[track], (tuple, list)):
                            cc = volume_controls[track][0]
                            if is_valid_midi_channel(volume_controls[track][1]):
                                channel = volume_controls[track][1]
                        if is_valid_midi_identifier(cc):
                            if is_valid_midi_channel(channel):
                                layer_specs['volume_control'] = make_mixer_encoder(cc, channel, '{}_Volume_Control'.format(track))
                    arm_button = make_channel_strip_button(trackarm_controls, track, 'Arm')
                    if arm_button:
                        layer_specs['arm_button'] = arm_button
                    else:
                        mute_button = make_channel_strip_button(mute_controls, track, 'Mute')
                        if mute_button:
                            layer_specs['mute_button'] = mute_button
                        solo_button = make_channel_strip_button(solo_controls, track, 'Solo')
                        if solo_button:
                            layer_specs['solo_button'] = solo_button
                        select_button = make_channel_strip_button(select_controls, track, 'Select')
                        if select_button:
                            layer_specs['select_button'] = select_button
                        send_controls_raw = []
                        for index, send in enumerate(send_info):
                            if 0<= track < len(send):
                                channel = global_channel
                                cc = send[track]
                                if isinstance(send[track], (tuple, list)):
                                    cc = send[track][0]
                                    if is_valid_midi_channel(send[track][1]):
                                        channel = send[track][1]
                                if is_valid_midi_identifier(cc):
                                    if is_valid_midi_channel(channel):
                                        send_controls_raw.append(make_mixer_encoder(cc,
                                          channel,
                                          name=('{}_Send_{}_Control'.format(track, index)),
                                          map_mode=sends_map_mode))

                        if len(send_controls_raw) > 0:
                            layer_specs['send_controls'] = ButtonMatrixElement(rows=[
                             send_controls_raw],
                              name=('{}_Send_Controls'.format(track)))
                        strip.layer = Layer(**layer_specs)

    def _init_device_component(self, device_controls, bank_controls, global_channel, macro_map_mode, device_component_class):
        is_momentary = True
        DeviceButton = partial(ButtonElement, is_momentary, MIDI_CC_TYPE)

        def make_bank_button(control, name):
            return DeviceButton(global_channel, (bank_controls[control]), name=name)

        if device_controls:
            layer_specs = {}
            if bank_controls:
                if has_specification_for('NEXTBANK', bank_controls):
                    layer_specs['bank_next_button'] = make_bank_button('NEXTBANK', 'Device_Next_Bank_Button')
                if has_specification_for('PREVBANK', bank_controls):
                    layer_specs['bank_prev_button'] = make_bank_button('PREVBANK', 'Device_Previous_Bank_Button')
                if has_specification_for('TOGGLELOCK', bank_controls):
                    layer_specs['lock_button'] = make_bank_button('TOGGLELOCK', 'Device_Lock_Button')
                if has_specification_for('ONOFF', bank_controls):
                    layer_specs['on_off_button'] = make_bank_button('ONOFF', 'Device_On_Off_Button')
                bank_buttons_raw = []
                for index in range(8):
                    key = 'BANK{}'.format(index + 1)
                    if key in list(bank_controls.keys()):
                        control_info = bank_controls[key]
                        channel = global_channel
                        cc = control_info
                        if isinstance(control_info, (tuple, list)):
                            cc = control_info[0]
                            if is_valid_midi_channel(control_info[1]):
                                channel = control_info[1]
                        if is_valid_midi_identifier(cc):
                            if is_valid_midi_channel(channel):
                                name = 'Device_Bank_{}_Button'.format(index)
                                bank_buttons_raw.append(DeviceButton(channel, cc, name=name))

                if len(bank_buttons_raw) > 0:
                    layer_specs['bank_buttons'] = ButtonMatrixElement(rows=[
                     bank_buttons_raw],
                      name='Device_Bank_Buttons')
            parameter_encoders_raw = []
            for index, control_info in enumerate(device_controls):
                channel = global_channel
                cc = control_info
                if isinstance(control_info, (tuple, list)):
                    cc = control_info[0]
                    if is_valid_midi_channel(control_info[1]):
                        channel = control_info[1]
                if is_valid_midi_identifier(cc):
                    if is_valid_midi_channel(channel):
                        name = 'Device_Parameter_%d_Control' % index
                        parameter_encoders_raw.append(EncoderElement(MIDI_CC_TYPE,
                          channel, cc, macro_map_mode, name=name))

            if len(parameter_encoders_raw) > 0:
                layer_specs['parameter_controls'] = ButtonMatrixElement(rows=[
                 parameter_encoders_raw],
                  name='Device_Parameter_Controls')
            if layer_specs:
                device = device_component_class(device_selection_follows_track_selection=True,
                  name='Device_Component')
                device.layer = Layer(**layer_specs)
                self.set_device_component(device)

    def _init_transport_component(self, transport_controls, global_channel):

        def make_transport_button(control, name, is_momentary=True):
            return ButtonElement(is_momentary,
              MIDI_CC_TYPE,
              global_channel,
              (transport_controls[control]),
              name=name)

        if transport_controls:
            momentary_seek = 'NORELEASE' not in list(transport_controls.keys())
            layer_specs = {}
            for key, spec in iteritems(TRANSPORT_BUTTON_SPECIFICATIONS):
                key_upper = key.upper()
                if has_specification_for(key_upper, transport_controls):
                    layer_specs['{}_button'.format(spec.layer_name)] = make_transport_button(key_upper,
                      ('{}_Button'.format(spec.control_name)),
                      is_momentary=(momentary_seek if key in ('Rwd', 'Ffwd') else True))

            transport = TransportComponent(name='Transport')
            transport.layer = Layer(**layer_specs)