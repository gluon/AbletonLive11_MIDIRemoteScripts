#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Generic/GenericScript.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from builtins import range
from functools import partial
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.Layer import Layer
from _Framework.TransportComponent import TransportComponent
from .SpecialMixerComponent import SpecialMixerComponent

def is_valid_midi_channel(integer):
    return 0 <= integer < 16


def is_valid_midi_identifier(integer):
    return 0 <= integer < 128


def has_specification_for(control, specifications):
    return is_valid_midi_identifier(specifications.get(control, -1))


class GenericScript(ControlSurface):
    u""" A generic script class with predefined behaviour.
        It can be customised to use/not use certain controls on instantiation.
    """

    def __init__(self, c_instance, macro_map_mode, volume_map_mode, device_controls, transport_controls, volume_controls, trackarm_controls, bank_controls, descriptions = None, mixer_options = None):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            global_channel = 0
            if descriptions:
                if list(descriptions.keys()).count(u'INPUTPORT') > 0:
                    self._suggested_input_port = descriptions[u'INPUTPORT']
                if list(descriptions.keys()).count(u'OUTPUTPORT') > 0:
                    self._suggested_output_port = descriptions[u'OUTPUTPORT']
                if list(descriptions.keys()).count(u'CHANNEL') > 0:
                    global_channel = descriptions[u'CHANNEL']
                    if not is_valid_midi_channel(global_channel):
                        global_channel = 0
                if list(descriptions.keys()).count(u'PAD_TRANSLATION') > 0:
                    self.set_pad_translations(descriptions[u'PAD_TRANSLATION'])
            self._init_mixer_component(volume_controls, trackarm_controls, mixer_options, global_channel, volume_map_mode)
            self._init_device_component(device_controls, bank_controls, global_channel, macro_map_mode)
            self._init_transport_component(transport_controls, global_channel)

    def handle_sysex(self, midi_bytes):
        pass

    def _init_mixer_component(self, volume_controls, trackarm_controls, mixer_options, global_channel, volume_map_mode):
        momentary_buttons = mixer_options is not None and u'NOTOGGLE' in list(mixer_options.keys())
        MixerButton = partial(ButtonElement, momentary_buttons, MIDI_CC_TYPE, global_channel)

        def make_mixer_encoder(cc, channel, name):
            if is_valid_midi_identifier(cc) and is_valid_midi_channel(channel):
                return EncoderElement(MIDI_CC_TYPE, channel, cc, volume_map_mode, name=name)

        def make_mixer_button(control, name):
            return MixerButton(mixer_options[control], name=name)

        if volume_controls != None and trackarm_controls != None:
            num_strips = max(len(volume_controls), len(trackarm_controls))
            send_info = []
            mixer = SpecialMixerComponent(num_strips, name=u'Mixer')
            mixer.master_strip().name = u'Master_Channel_Strip'
            mixer.selected_strip().name = u'Selected_Channel_Strip'
            if mixer_options != None:
                if has_specification_for(u'MASTERVOLUME', mixer_options) and is_valid_midi_identifier(mixer_options[u'MASTERVOLUME']):
                    mixer.master_strip().layer = Layer(volume_control=make_mixer_encoder(mixer_options[u'MASTERVOLUME'], global_channel, u'Master_Volume_Control'))
                for send in range(mixer_options.get(u'NUMSENDS', 0)):
                    send_info.append(mixer_options[u'SEND%d' % (send + 1)])

                layer_specs = {}
                if has_specification_for(u'NEXTBANK', mixer_options):
                    layer_specs[u'bank_up_button'] = make_mixer_button(u'NEXTBANK', u'Mixer_Next_Bank_Button')
                if has_specification_for(u'PREVBANK', mixer_options):
                    layer_specs[u'bank_down_button'] = make_mixer_button(u'PREVBANK', u'Mixer_Previous_Bank_Button')
                mixer.layer = Layer(**layer_specs)
            for track in range(num_strips):
                strip = mixer.channel_strip(track)
                strip.name = u'Channel_Strip_' + str(track)
                layer_specs = {}
                if 0 <= track < len(volume_controls):
                    channel = global_channel
                    cc = volume_controls[track]
                    if isinstance(volume_controls[track], (tuple, list)):
                        cc = volume_controls[track][0]
                        if is_valid_midi_channel(volume_controls[track][1]):
                            channel = volume_controls[track][1]
                    if is_valid_midi_identifier(cc) and is_valid_midi_channel(channel):
                        layer_specs[u'volume_control'] = make_mixer_encoder(cc, channel, str(track) + u'_Volume_Control')
                if 0 <= track < len(trackarm_controls) and is_valid_midi_identifier(trackarm_controls[track]):
                    layer_specs[u'arm_button'] = MixerButton(trackarm_controls[track], name=str(track) + u'_Arm_Button')
                send_controls_raw = []
                for index, send in enumerate(send_info):
                    if 0 <= track < len(send):
                        channel = global_channel
                        cc = send[track]
                        if isinstance(send[track], (tuple, list)):
                            cc = send[track][0]
                            if is_valid_midi_channel(send[track][1]):
                                channel = send[track][1]
                        if is_valid_midi_identifier(cc) and is_valid_midi_channel(channel):
                            send_controls_raw.append(make_mixer_encoder(cc, channel, name=u'%d_Send_%d_Control' % (track, index)))

                if len(send_controls_raw) > 0:
                    layer_specs[u'send_controls'] = ButtonMatrixElement(rows=[send_controls_raw])
                strip.layer = Layer(**layer_specs)

    def _init_device_component(self, device_controls, bank_controls, global_channel, macro_map_mode):
        is_momentary = True
        DeviceButton = partial(ButtonElement, is_momentary, MIDI_CC_TYPE)

        def make_bank_button(control, name, is_momentary = True):
            return DeviceButton(global_channel, bank_controls[control], name=name)

        if device_controls:
            device = DeviceComponent(device_selection_follows_track_selection=True, name=u'Device_Component')
            layer_specs = {}
            if bank_controls:
                if has_specification_for(u'NEXTBANK', bank_controls):
                    layer_specs[u'bank_next_button'] = make_bank_button(u'NEXTBANK', u'Device_Next_Bank_Button')
                if has_specification_for(u'PREVBANK', bank_controls):
                    layer_specs[u'bank_prev_button'] = make_bank_button(u'PREVBANK', u'Device_Previous_Bank_Button')
                if has_specification_for(u'TOGGLELOCK', bank_controls):
                    layer_specs[u'lock_button'] = make_bank_button(u'TOGGLELOCK', u'Device_Lock_Button')
                bank_buttons_raw = []
                for index in range(8):
                    key = u'BANK' + str(index + 1)
                    if key in list(bank_controls.keys()):
                        control_info = bank_controls[key]
                        channel = global_channel
                        cc = control_info
                        if isinstance(control_info, (tuple, list)):
                            cc = control_info[0]
                            if is_valid_midi_channel(control_info[1]):
                                channel = control_info[1]
                        if is_valid_midi_identifier(cc) and is_valid_midi_channel(channel):
                            name = u'Device_Bank_' + str(index) + u'_Button'
                            bank_buttons_raw.append(DeviceButton(channel, cc, name=name))

                if len(bank_buttons_raw) > 0:
                    layer_specs[u'bank_buttons'] = ButtonMatrixElement(rows=[bank_buttons_raw])
            parameter_encoders_raw = []
            for index, control_info in enumerate(device_controls):
                channel = global_channel
                cc = control_info
                if isinstance(control_info, (tuple, list)):
                    cc = control_info[0]
                    if is_valid_midi_channel(control_info[1]):
                        channel = control_info[1]
                if is_valid_midi_identifier(cc) and is_valid_midi_channel(channel):
                    name = u'Device_Parameter_%d_Control' % index
                    parameter_encoders_raw.append(EncoderElement(MIDI_CC_TYPE, channel, cc, macro_map_mode, name=name))

            if len(parameter_encoders_raw) > 0:
                layer_specs[u'parameter_controls'] = ButtonMatrixElement(rows=[parameter_encoders_raw])
            device.layer = Layer(**layer_specs)
            self.set_device_component(device)

    def _init_transport_component(self, transport_controls, global_channel):

        def make_transport_button(control, name, is_momentary = True):
            return ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, transport_controls[control], name=name)

        if transport_controls:
            momentary_seek = u'NORELEASE' not in list(transport_controls.keys())
            layer_specs = {}
            if has_specification_for(u'STOP', transport_controls):
                layer_specs[u'stop_button'] = make_transport_button(u'STOP', u'Stop_Button')
            if has_specification_for(u'PLAY', transport_controls):
                layer_specs[u'play_button'] = make_transport_button(u'PLAY', u'Play_Button')
            if has_specification_for(u'REC', transport_controls):
                layer_specs[u'record_button'] = make_transport_button(u'REC', u'Record_Button')
            if has_specification_for(u'LOOP', transport_controls):
                layer_specs[u'loop_button'] = make_transport_button(u'LOOP', u'Loop_Button')
            if has_specification_for(u'FFWD', transport_controls):
                layer_specs[u'seek_forward_button'] = make_transport_button(u'FFWD', u'FFwd_Button', is_momentary=momentary_seek)
            if has_specification_for(u'RWD', transport_controls):
                layer_specs[u'seek_backward_button'] = make_transport_button(u'RWD', u'Rwd_Button', is_momentary=momentary_seek)
            transport = TransportComponent(name=u'Transport')
            transport.layer = Layer(**layer_specs)
