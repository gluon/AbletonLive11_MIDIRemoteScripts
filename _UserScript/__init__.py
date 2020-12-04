#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_UserScript/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from past.utils import old_div
from ableton.v2.base import PY3
if PY3:
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser
from _Generic.GenericScript import GenericScript
import Live
HIDE_SCRIPT = True

def interpret_map_mode(map_mode_name):
    result = Live.MidiMap.MapMode.absolute
    if map_mode_name == u'Absolute14Bit':
        result = Live.MidiMap.MapMode.absolute_14_bit
    elif map_mode_name == u'AccelSignedBit':
        result = Live.MidiMap.MapMode.relative_signed_bit
    elif map_mode_name == u'LinearSignedBit':
        result = Live.MidiMap.MapMode.relative_smooth_signed_bit
    elif map_mode_name == u'AccelSignedBit2':
        result = Live.MidiMap.MapMode.relative_signed_bit2
    elif map_mode_name == u'LinearSignedBit2':
        result = Live.MidiMap.MapMode.relative_smooth_signed_bit2
    elif map_mode_name == u'AccelBinaryOffset':
        result = Live.MidiMap.MapMode.relative_binary_offset
    elif map_mode_name == u'LinearBinaryOffset':
        result = Live.MidiMap.MapMode.relative_smooth_binary_offset
    elif map_mode_name == u'AccelTwoCompliment':
        result = Live.MidiMap.MapMode.relative_two_compliment
    elif map_mode_name == u'LinearTwoCompliment':
        result = Live.MidiMap.MapMode.relative_smooth_two_compliment
    return result


def create_instance(c_instance, user_path = u''):
    u""" The generic script can be customised by using parameters.
        In this case, the user has written a text file with all necessary info.
        Here we read this file and fill the necessary data structures before
        instantiating the generic script.
    """
    device_map_mode = Live.MidiMap.MapMode.absolute
    volume_map_mode = Live.MidiMap.MapMode.absolute
    sends_map_mode = Live.MidiMap.MapMode.absolute
    if not user_path == u'':
        file_object = open(user_path)
        if file_object:
            file_data = None
            config_parser = ConfigParser()
            config_parser.readfp(file_object, user_path)
            device_controls = [(-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1)]
            transport_controls = {u'STOP': -1,
             u'PLAY': -1,
             u'REC': -1,
             u'LOOP': -1,
             u'RWD': -1,
             u'FFWD': -1}
            volume_controls = [(-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1),
             (-1, -1)]
            trackarm_controls = [-1,
             -1,
             -1,
             -1,
             -1,
             -1,
             -1,
             -1]
            bank_controls = {u'TOGGLELOCK': -1,
             u'NEXTBANK': -1,
             u'PREVBANK': -1,
             u'BANK1': -1,
             u'BANK2': -1,
             u'BANK3': -1,
             u'BANK4': -1,
             u'BANK5': -1,
             u'BANK6': -1,
             u'BANK7': -1,
             u'BANK8': -1}
            controller_descriptions = {u'INPUTPORT': u'',
             u'OUTPUTPORT': u'',
             u'CHANNEL': -1}
            mixer_options = {u'NUMSENDS': 2,
             u'SEND1': [-1,
                        -1,
                        -1,
                        -1,
                        -1,
                        -1,
                        -1,
                        -1],
             u'SEND2': [-1,
                        -1,
                        -1,
                        -1,
                        -1,
                        -1,
                        -1,
                        -1],
             u'MASTERVOLUME': -1,
             u'MASTERVOLUMECHANNEL': -1}
            for index in range(8):
                if config_parser.has_section(u'DeviceControls'):
                    encoder_tuple = [-1, -1]
                    option_name = u'Encoder' + str(index + 1)
                    if config_parser.has_option(u'DeviceControls', option_name):
                        option_value = config_parser.getint(u'DeviceControls', option_name)
                        if option_value in range(128):
                            encoder_tuple[0] = option_value
                    option_name = u'EncoderChannel' + str(index + 1)
                    if config_parser.has_option(u'DeviceControls', option_name):
                        option_value = config_parser.getint(u'DeviceControls', option_name)
                        if option_value in range(128):
                            encoder_tuple[1] = option_value
                    device_controls[index] = tuple(encoder_tuple)
                    option_name = u'Bank' + str(index + 1) + u'Button'
                    if config_parser.has_option(u'DeviceControls', option_name):
                        option_value = config_parser.getint(u'DeviceControls', option_name)
                        if option_value in range(128):
                            option_key = u'BANK' + str(index + 1)
                            bank_controls[option_key] = option_value
                if config_parser.has_section(u'MixerControls'):
                    volume_tuple = [-1, -1]
                    option_name = u'VolumeSlider' + str(index + 1)
                    if config_parser.has_option(u'MixerControls', option_name):
                        option_value = config_parser.getint(u'MixerControls', option_name)
                        if option_value in range(128):
                            volume_tuple[0] = option_value
                    option_name = u'Slider' + str(index + 1) + u'Channel'
                    if config_parser.has_option(u'MixerControls', option_name):
                        option_value = config_parser.getint(u'MixerControls', option_name)
                        if option_value in range(16):
                            volume_tuple[1] = option_value
                    volume_controls[index] = tuple(volume_tuple)
                    option_name = u'TrackArmButton' + str(index + 1)
                    if config_parser.has_option(u'MixerControls', option_name):
                        option_value = config_parser.getint(u'MixerControls', option_name)
                        if option_value in range(128):
                            trackarm_controls[index] = option_value
                    option_name = u'Send1Knob' + str(index + 1)
                    if config_parser.has_option(u'MixerControls', option_name):
                        option_value = config_parser.getint(u'MixerControls', option_name)
                        if option_value in range(128):
                            mixer_options[u'SEND1'][index] = option_value
                    option_name = u'Send2Knob' + str(index + 1)
                    if config_parser.has_option(u'MixerControls', option_name):
                        option_value = config_parser.getint(u'MixerControls', option_name)
                        if option_value in range(128):
                            mixer_options[u'SEND2'][index] = option_value
                if config_parser.has_section(u'Globals'):
                    if config_parser.has_option(u'Globals', u'GlobalChannel'):
                        option_value = config_parser.getint(u'Globals', u'GlobalChannel')
                        if option_value in range(16):
                            controller_descriptions[u'CHANNEL'] = option_value
                    if config_parser.has_option(u'Globals', u'InputName'):
                        controller_descriptions[u'INPUTPORT'] = config_parser.get(u'Globals', u'InputName')
                    if config_parser.has_option(u'Globals', u'OutputName'):
                        controller_descriptions[u'OUTPUTPORT'] = config_parser.get(u'Globals', u'OutputName')
                    pad_translation = []
                    for pad in range(16):
                        pad_info = []
                        note = -1
                        channel = -1
                        option_name = u'Pad' + str(pad + 1) + u'Note'
                        if config_parser.has_option(u'Globals', option_name):
                            note = config_parser.getint(u'Globals', option_name)
                            if note in range(128):
                                option_name = u'Pad' + str(pad + 1) + u'Channel'
                                if config_parser.has_option(u'Globals', option_name):
                                    channel = config_parser.getint(u'Globals', option_name)
                                if channel is -1 and controller_descriptions[u'CHANNEL'] is not -1:
                                    channel = controller_descriptions[u'CHANNEL']
                                if channel in range(16):
                                    pad_info.append(pad % 4)
                                    pad_info.append(int(old_div(pad, 4)))
                                    pad_info.append(note)
                                    pad_info.append(channel)
                                    pad_translation.append(tuple(pad_info))

                    if len(pad_translation) > 0:
                        controller_descriptions[u'PAD_TRANSLATION'] = tuple(pad_translation)
                if config_parser.has_section(u'DeviceControls'):
                    if config_parser.has_option(u'DeviceControls', u'NextBankButton'):
                        option_value = config_parser.getint(u'DeviceControls', u'NextBankButton')
                        if option_value in range(128):
                            bank_controls[u'NEXTBANK'] = option_value
                    if config_parser.has_option(u'DeviceControls', u'PrevBankButton'):
                        option_value = config_parser.getint(u'DeviceControls', u'PrevBankButton')
                        if option_value in range(128):
                            bank_controls[u'PREVBANK'] = option_value
                    if config_parser.has_option(u'DeviceControls', u'LockButton'):
                        option_value = config_parser.getint(u'DeviceControls', u'LockButton')
                        if option_value in range(128):
                            bank_controls[u'TOGGLELOCK'] = option_value
                    if config_parser.has_option(u'DeviceControls', u'EncoderMapMode'):
                        device_map_mode = interpret_map_mode(config_parser.get(u'DeviceControls', u'EncoderMapMode'))
                if config_parser.has_section(u'MixerControls'):
                    if config_parser.has_option(u'MixerControls', u'MasterVolumeSlider'):
                        option_value = config_parser.getint(u'MixerControls', u'MasterVolumeSlider')
                        if option_value in range(128):
                            mixer_options[u'MASTERVOLUME'] = option_value
                    if config_parser.has_option(u'MixerControls', u'MasterSliderChannel'):
                        option_value = config_parser.getint(u'MixerControls', u'MasterSliderChannel')
                        if option_value in range(16):
                            mixer_options[u'MASTERVOLUMECHANNEL'] = option_value
                    if config_parser.has_option(u'MixerControls', u'VolumeMapMode'):
                        volume_map_mode = interpret_map_mode(config_parser.get(u'MixerControls', u'VolumeMapMode'))
                    if config_parser.has_option(u'MixerControls', u'SendsMapMode'):
                        sends_map_mode = interpret_map_mode(config_parser.get(u'MixerControls', u'SendsMapMode'))
                        mixer_options[u'SENDMAPMODE'] = sends_map_mode
                if config_parser.has_section(u'TransportControls'):
                    if config_parser.has_option(u'TransportControls', u'StopButton'):
                        option_value = config_parser.getint(u'TransportControls', u'StopButton')
                        if option_value in range(128):
                            transport_controls[u'STOP'] = option_value
                    if config_parser.has_option(u'TransportControls', u'PlayButton'):
                        option_value = config_parser.getint(u'TransportControls', u'PlayButton')
                        if option_value in range(128):
                            transport_controls[u'PLAY'] = option_value
                    if config_parser.has_option(u'TransportControls', u'RecButton'):
                        option_value = config_parser.getint(u'TransportControls', u'RecButton')
                        if option_value in range(128):
                            transport_controls[u'REC'] = option_value
                    if config_parser.has_option(u'TransportControls', u'LoopButton'):
                        option_value = config_parser.getint(u'TransportControls', u'LoopButton')
                        if option_value in range(128):
                            transport_controls[u'LOOP'] = option_value
                    if config_parser.has_option(u'TransportControls', u'RwdButton'):
                        option_value = config_parser.getint(u'TransportControls', u'RwdButton')
                        if option_value in range(128):
                            transport_controls[u'RWD'] = option_value
                    if config_parser.has_option(u'TransportControls', u'FfwdButton'):
                        option_value = config_parser.getint(u'TransportControls', u'FfwdButton')
                        if option_value in range(128):
                            transport_controls[u'FFWD'] = option_value

    return GenericScript(c_instance, device_map_mode, volume_map_mode, tuple(device_controls), transport_controls, tuple(volume_controls), tuple(trackarm_controls), bank_controls, controller_descriptions, mixer_options)
