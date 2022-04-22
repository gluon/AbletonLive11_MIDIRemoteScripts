# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_UserScript/__init__.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 15063 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import range
from future import standard_library
from past.utils import old_div
import logging, os
from ast import parse
from functools import partial
from ableton.v2.base import PY3
if PY3:
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser
import Live
from _Generic.GenericScript import TRANSPORT_BUTTON_SPECIFICATIONS, GenericScript
from .DeviceComponent import DeviceComponent
standard_library.install_aliases()
logger = logging.getLogger(__name__)
HIDE_SCRIPT = True

def get_name_for_script(script_path):
    folder_name = str(script_path.split(os.path.sep)[(-2)].replace(' ', '_'))
    try:
        parse('{}= None'.format(folder_name))
        script_name = folder_name
    except Exception:
        script_name = 'GenericScript'

    return script_name


def parse_map_mode(config_parser, section_name, option_name):
    result = Live.MidiMap.MapMode.absolute
    if config_parser.has_option(section_name, option_name):
        map_mode_name = config_parser.get(section_name, option_name)
        if map_mode_name == 'Absolute14Bit':
            result = Live.MidiMap.MapMode.absolute_14_bit
        elif map_mode_name == 'AccelSignedBit':
            result = Live.MidiMap.MapMode.relative_signed_bit
        elif map_mode_name == 'LinearSignedBit':
            result = Live.MidiMap.MapMode.relative_smooth_signed_bit
        elif map_mode_name == 'AccelSignedBit2':
            result = Live.MidiMap.MapMode.relative_signed_bit2
        elif map_mode_name == 'LinearSignedBit2':
            result = Live.MidiMap.MapMode.relative_smooth_signed_bit2
        elif map_mode_name == 'AccelBinaryOffset':
            result = Live.MidiMap.MapMode.relative_binary_offset
        elif map_mode_name == 'LinearBinaryOffset':
            result = Live.MidiMap.MapMode.relative_smooth_binary_offset
        elif map_mode_name == 'AccelTwoCompliment':
            result = Live.MidiMap.MapMode.relative_two_compliment
        elif map_mode_name == 'LinearTwoCompliment':
            result = Live.MidiMap.MapMode.relative_smooth_two_compliment
    return result


def parse_int(config_parser, integer_range, section_name, option_name):
    integer = -1
    if config_parser.has_option(section_name, option_name):
        try:
            option_value = config_parser.getint(section_name, option_name)
            if option_value in range(integer_range):
                integer = option_value
        except ValueError as e:
            try:
                logger.error('Error while parsing integer value %s', str(e))
            finally:
                e = None
                del e

        return integer


open_file = open

def create_instance(c_instance, user_path=''):
    device_map_mode = Live.MidiMap.MapMode.absolute
    volume_map_mode = Live.MidiMap.MapMode.absolute
    if not user_path == '':
        file_object = open_file(user_path)
        if file_object:
            config_parser = ConfigParser()
            if PY3:
                config_parser.read_file(file_object)
            else:
                config_parser.readfp(file_object)
            parse_identifier = partial(parse_int, config_parser, 128)
            parse_channel = partial(parse_int, config_parser, 16)
            device_controls = [
             (-1, -1)] * 16
            transport_controls = {key.upper():-1 for key in TRANSPORT_BUTTON_SPECIFICATIONS}
            volume_controls = [
             (-1, -1)] * 8
            trackarm_controls = [
             -1] * 8
            bank_controls = {'ONOFF':-1, 
             'TOGGLELOCK':-1, 
             'NEXTBANK':-1, 
             'PREVBANK':-1, 
             'BANK1':-1, 
             'BANK2':-1, 
             'BANK3':-1, 
             'BANK4':-1, 
             'BANK5':-1, 
             'BANK6':-1, 
             'BANK7':-1, 
             'BANK8':-1}
            controller_descriptions = {'CHANNEL': -1}
            mixer_options = {'NUMSENDS':2, 
             'INVERTMUTELEDS':True, 
             'SEND1':[
              -1] * 8, 
             'SEND2':[
              -1] * 8, 
             'MUTE':[
              -1] * 8, 
             'SOLO':[
              -1] * 8, 
             'SELECT':[
              -1] * 8, 
             'SENDMAPMODE':Live.MidiMap.MapMode.absolute, 
             'MASTERVOLUME':-1, 
             'MASTERVOLUMECHANNEL':-1, 
             'CUEVOLUME':-1, 
             'CUEVOLUMECHANNEL':-1, 
             'CROSSFADER':-1, 
             'CROSSFADERCHANNEL':-1, 
             'CROSSFADERMAPMODE':Live.MidiMap.MapMode.absolute}
            if config_parser.has_section('DeviceControls'):
                device_controls = [(parse_identifier('DeviceControls', 'Encoder{}'.format(index + 1)), parse_channel('DeviceControls', 'EncoderChannel{}'.format(index + 1))) for index in range(16)]
            for index in range(8):
                friendly_index = index + 1
                if config_parser.has_section('DeviceControls'):
                    bank_controls['BANK{}'.format(friendly_index)] = parse_identifier('DeviceControls', 'Bank{}Button'.format(friendly_index))
                if config_parser.has_section('MixerControls'):
                    volume_controls[index] = tuple([
                     parse_identifier('MixerControls', 'VolumeSlider{}'.format(friendly_index)),
                     parse_channel('MixerControls', 'Slider{}Channel'.format(friendly_index))])
                    trackarm_controls[index] = parse_identifier('MixerControls', 'TrackArmButton{}'.format(friendly_index))
                    mixer_options['MUTE'][index] = parse_identifier('MixerControls', 'TrackMuteButton{}'.format(friendly_index))
                    mixer_options['SOLO'][index] = parse_identifier('MixerControls', 'TrackSoloButton{}'.format(friendly_index))
                    mixer_options['SELECT'][index] = parse_identifier('MixerControls', 'TrackSelectButton{}'.format(friendly_index))
                    mixer_options['SEND1'][index] = parse_identifier('MixerControls', 'Send1Knob{}'.format(friendly_index))
                    mixer_options['SEND2'][index] = parse_identifier('MixerControls', 'Send2Knob{}'.format(friendly_index))
                if config_parser.has_section('Globals'):
                    controller_descriptions['CHANNEL'] = parse_channel('Globals', 'GlobalChannel')
                    pad_translation = []
                    for pad in range(16):
                        pad_info = []
                        note = -1
                        channel = -1
                        option_name = 'Pad{}Note'.format(pad + 1)
                        if config_parser.has_option('Globals', option_name):
                            note = config_parser.getint('Globals', option_name)
                            if note in range(128):
                                option_name = 'Pad{}Channel'.format(pad + 1)
                                if config_parser.has_option('Globals', option_name):
                                    channel = config_parser.getint('Globals', option_name)
                                if channel is -1:
                                    if controller_descriptions['CHANNEL'] is not -1:
                                        channel = controller_descriptions['CHANNEL']
                                if channel in range(16):
                                    pad_info.append(pad % 4)
                                    pad_info.append(int(old_div(pad, 4)))
                                    pad_info.append(note)
                                    pad_info.append(channel)
                                    pad_translation.append(tuple(pad_info))

                    if len(pad_translation) > 0:
                        controller_descriptions['PAD_TRANSLATION'] = tuple(pad_translation)
                if config_parser.has_section('DeviceControls'):
                    bank_controls['NEXTBANK'] = parse_identifier('DeviceControls', 'NextBankButton')
                    bank_controls['PREVBANK'] = parse_identifier('DeviceControls', 'PrevBankButton')
                    bank_controls['TOGGLELOCK'] = parse_identifier('DeviceControls', 'LockButton')
                    bank_controls['ONOFF'] = parse_identifier('DeviceControls', 'OnOffButton')
                    device_map_mode = parse_map_mode(config_parser, 'DeviceControls', 'EncoderMapMode')
                if config_parser.has_section('MixerControls'):
                    mixer_options['MASTERVOLUME'] = parse_identifier('MixerControls', 'MasterVolumeSlider')
                    mixer_options['MASTERVOLUMECHANNEL'] = parse_channel('MixerControls', 'MasterSliderChannel')
                    mixer_options['CUEVOLUME'] = parse_identifier('MixerControls', 'CueVolumeSlider')
                    mixer_options['CUEVOLUMECHANNEL'] = parse_channel('MixerControls', 'CueSliderChannel')
                    mixer_options['CROSSFADER'] = parse_identifier('MixerControls', 'CrossfaderSlider')
                    mixer_options['CROSSFADERCHANNEL'] = parse_channel('MixerControls', 'CrossfaderSliderChannel')
                    volume_map_mode = parse_map_mode(config_parser, 'MixerControls', 'VolumeMapMode')
                    mixer_options['SENDMAPMODE'] = parse_map_mode(config_parser, 'MixerControls', 'SendsMapMode')
                    mixer_options['CROSSFADERMAPMODE'] = parse_map_mode(config_parser, 'MixerControls', 'CrossfaderMapMode')
                    if config_parser.has_option('MixerControls', 'MixerButtonsToggle'):
                        if not config_parser.getboolean('MixerControls', 'MixerButtonsToggle'):
                            mixer_options['NOTOGGLE'] = True
                        if config_parser.has_option('MixerControls', 'InvertMuteButtonFeedback'):
                            mixer_options['INVERTMUTELEDS'] = config_parser.getboolean('MixerControls', 'InvertMuteButtonFeedback')
                    mixer_options['NEXTBANK'] = parse_identifier('MixerControls', 'NextBankButton')
                    mixer_options['PREVBANK'] = parse_identifier('MixerControls', 'PrevBankButton')
                if config_parser.has_section('TransportControls'):
                    for key in TRANSPORT_BUTTON_SPECIFICATIONS:
                        transport_controls[key.upper()] = parse_identifier('TransportControls', '{}Button'.format(key))

        else:
            pass
    else:
        pass
    return type(get_name_for_script(user_path), (GenericScript,), {})(c_instance,
      device_map_mode,
      volume_map_mode,
      (tuple(device_controls)),
      transport_controls,
      (tuple(volume_controls)),
      (tuple(trackarm_controls)),
      bank_controls,
      controller_descriptions,
      mixer_options,
      device_component_class=DeviceComponent)