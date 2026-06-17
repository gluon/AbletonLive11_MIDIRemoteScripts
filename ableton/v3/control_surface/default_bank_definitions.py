# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\default_bank_definitions.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 136106 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base.collection import IndexedDict
from . import BANK_MAIN_KEY, BANK_PARAMETERS_KEY, use
BANK_DEFINITIONS = {}
RACK_BANKS = IndexedDict((
 (
  'Macros',
  {BANK_PARAMETERS_KEY: ('Macro 1', 'Macro 2', 'Macro 3', 'Macro 4', 'Macro 5', 'Macro 6', 'Macro 7', 'Macro 8')}),
 (
  'Macros 2',
  {BANK_PARAMETERS_KEY: ('Macro 9', 'Macro 10', 'Macro 11', 'Macro 12', 'Macro 13', 'Macro 14', 'Macro 15',
 'Macro 16')})))
BANK_DEFINITIONS['AudioEffectGroupDevice'] = RACK_BANKS
BANK_DEFINITIONS['MidiEffectGroupDevice'] = RACK_BANKS
BANK_DEFINITIONS['InstrumentGroupDevice'] = RACK_BANKS
BANK_DEFINITIONS['DrumGroupDevice'] = RACK_BANKS
BANK_DEFINITIONS['Amp'] = IndexedDict((
 (
  'Global',
  {BANK_PARAMETERS_KEY: ('Amp Type', 'Bass', 'Middle', 'Treble', 'Presence', 'Gain', 'Volume', 'Dry/Wet')}),
 (
  'Dual/Mono', {BANK_PARAMETERS_KEY: ('Dual Mono', '', '', '', '', '', '', '')})))
BANK_DEFINITIONS['UltraAnalog'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('F1 Freq', 'F1 Resonance', 'OSC1 Shape', 'OSC1 Octave', 'OSC2 Shape', 'OSC2 Octave',
 'OSC2 Detune', 'Volume')}),
 (
  'Oscillators',
  {BANK_PARAMETERS_KEY: ('OSC1 Level', 'OSC1 Octave', 'OSC1 Semi', 'OSC1 Shape', 'OSC2 Level', 'OSC2 Octave',
 'OSC2 Semi', 'OSC2 Shape')}),
 (
  'Filters',
  {BANK_PARAMETERS_KEY: ('OSC1 Balance', 'F1 Freq', 'F1 Resonance', 'F1 Type', 'OSC2 Balance', 'F2 Freq', 'F2 Resonance',
 'F2 Type')}),
 (
  'Filter Envelopes',
  {BANK_PARAMETERS_KEY: ('FEG1 Attack', 'FEG1 Decay', 'FEG1 Sustain', 'FEG1 Rel', 'FEG2 Attack', 'FEG2 Decay',
 'FEG2 Sustain', 'FEG2 Rel')}),
 (
  'Filter Modulation',
  {BANK_PARAMETERS_KEY: ('F1 On/Off', 'F1 Freq < LFO', 'F1 Freq < Env', 'F1 Res < LFO', 'F2 On/Off', 'F2 Freq < LFO',
 'F2 Freq < Env', 'F2 Res < LFO')}),
 (
  'Volume Envelopes',
  {BANK_PARAMETERS_KEY: ('AEG1 Attack', 'AEG1 Decay', 'AEG1 Sustain', 'AEG1 Rel', 'AEG2 Attack', 'AEG2 Decay',
 'AEG2 Sustain', 'AEG2 Rel')}),
 (
  'Mix',
  {BANK_PARAMETERS_KEY: (
                         'AMP1 Level',
                         'AMP1 Pan',
                         'LFO1 Shape',
                         use('LFO1 Speed').if_parameter('LFO1 Sync').has_value('Hertz').else_use('LFO1 SncRate'),
                         'AMP2 Level',
                         'AMP2 Pan',
                         'LFO2 Shape',
                         use('LFO2 Speed').if_parameter('LFO2 Sync').has_value('Hertz').else_use('LFO2 SncRate'))}),
 (
  'Output',
  {BANK_PARAMETERS_KEY: ('Volume', 'Noise On/Off', 'Noise Level', 'Noise Color', 'Unison On/Off', 'Unison Detune',
 'Vib On/Off', 'Vib Amount')})))
BANK_DEFINITIONS['MidiArpeggiator'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Style',
                         use('Synced Rate').if_parameter('Sync On').has_value('On').else_use('Free Rate'),
                         'Gate',
                         'Offset',
                         'Hold On',
                         'Tranpose Key',
                         'Transp. Steps',
                         'Transp. Dist.')}),
 (
  'Rhythm',
  {BANK_PARAMETERS_KEY: (
                         'Sync On',
                         use('Synced Rate').if_parameter('Sync On').has_value('On').else_use('Free Rate'),
                         'Groove',
                         'Offset',
                         'Repeats',
                         'Gate',
                         'Retrigger Mode',
                         'Ret. Interval')}),
 (
  'Pitch/Vel.',
  {BANK_PARAMETERS_KEY: ('Tranpose Mode', 'Tranpose Key', 'Transp. Steps', 'Transp. Dist.', 'Velocity On',
 'Vel. Retrigger', 'Velocity Decay', 'Velocity Target')})))
BANK_DEFINITIONS['AutoFilter'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         use('Filter Type').if_parameter('Filter Type').is_available(True).else_use('Filter Type (Legacy)'),
                         use('Frequency'),
                         use('Resonance').if_parameter('Resonance').is_available(True).else_use('Resonance (Legacy)'),
                         use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value_in(('Lowpass',
                                                                        'Highpass')).else_use('Filter Circuit - BP/NO/Morph'),
                         use('Morph').if_parameter('Filter Type').has_value('Morph').else_use('Drive').if_parameter('Drive').is_available(True),
                         'LFO Amount',
                         'LFO Sync',
                         use('LFO Frequency').if_parameter('LFO Sync').has_value('Free').else_use('LFO Sync Rate'))}),
 (
  'Envelope',
  {BANK_PARAMETERS_KEY: (
                         use('Filter Type').if_parameter('Filter Type').is_available(True).else_use('Filter Type (Legacy)'),
                         use('Frequency'),
                         use('Resonance').if_parameter('Resonance').is_available(True).else_use('Resonance (Legacy)'),
                         use('Morph').if_parameter('Filter Type').has_value('Morph').else_use('Drive').if_parameter('Drive').is_available(True),
                         use('Slope').if_parameter('Slope').is_available(True),
                         'Env. Attack',
                         'Env. Release',
                         'Env. Modulation')}),
 (
  'LFO',
  {BANK_PARAMETERS_KEY: (
                         'LFO Amount',
                         'LFO Waveform',
                         'LFO Sync',
                         use('LFO Frequency').if_parameter('LFO Sync').has_value('Free').else_use('LFO Sync Rate'),
                         use('LFO Offset').if_parameter('LFO Sync').has_value('Sync').else_use('LFO Stereo Mode'),
                         use('LFO Phase').if_parameter('LFO Sync').has_value('Sync').or_parameter('LFO Stereo Mode').has_value('Phase').else_use('LFO Spin'),
                         'LFO Quantize On',
                         'LFO Quantize Rate')}),
 (
  'Sidechain',
  {BANK_PARAMETERS_KEY: ('S/C On', 'S/C Mix', 'S/C Gain', '', '', '', '', '')})))
BANK_DEFINITIONS['AutoPan'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Amount',
                         'Shape',
                         'Invert',
                         'Waveform',
                         'LFO Type',
                         use('Sync Rate').if_parameter('LFO Type').has_value('Beats').else_use('Frequency'),
                         use('Stereo Mode').if_parameter('LFO Type').has_value('Frequency').else_use('Offset'),
                         use('Width (Random)').if_parameter('Waveform').has_value('S&H Width').else_use('Phase').if_parameter('LFO Type').has_value('Beats').else_use('Spin').if_parameter('Stereo Mode').has_value('Spin').else_use('Phase'))}),))
BANK_DEFINITIONS['BeatRepeat'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Grid', 'Interval', 'Offset', 'Gate', 'Pitch', 'Pitch Decay', 'Variation', 'Chance')}),
 (
  'Filt/Mix',
  {BANK_PARAMETERS_KEY: ('Filter On', 'Filter Freq', 'Filter Width', '', 'Mix Type', 'Volume', 'Decay', 'Chance')}),
 (
  'Repeat Rate',
  {BANK_PARAMETERS_KEY: ('Repeat', 'Interval', 'Offset', 'Gate', 'Grid', 'Block Triplets', 'Variation', 'Variation Type')})))
BANK_DEFINITIONS['Cabinet'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Cabinet Type', 'Microphone Type', 'Microphone Position', 'Dual Mono', '', '', '',
 'Dry/Wet')}),))
BANK_DEFINITIONS['ChannelEq'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Highpass On',
                         use('Low Gain').with_name('Low'),
                         use('Mid Gain').with_name('Mid'),
                         'Mid Freq',
                         use('High Gain').with_name('High'),
                         use('Gain').with_name('Output'),
                         '',
                         '')}),))
BANK_DEFINITIONS['MidiChord'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Shift1', 'Shift2', 'Shift3', 'Shift4', 'Shift5', 'Velocity5', 'Shift6', 'Velocity6')}),
 (
  'Shift',
  {BANK_PARAMETERS_KEY: ('Shift1', 'Shift2', 'Shift3', 'Shift4', 'Shift5', 'Shift6', '', '')}),
 (
  'Shift %',
  {BANK_PARAMETERS_KEY: ('Velocity1', 'Velocity2', 'Velocity3', 'Velocity4', 'Velocity5', 'Velocity6', '',
 '')})))
BANK_DEFINITIONS['Chorus'] = IndexedDict((
 (
  'Chorus',
  {BANK_PARAMETERS_KEY: ('LFO Amount', 'LFO Rate', 'Delay 1 Time', 'Delay 1 HiPass', 'Delay 2 Mode', 'Delay 2 Time',
 'Feedback', 'Dry/Wet')}),
 (
  'Other',
  {BANK_PARAMETERS_KEY: ('LFO Extend On', 'Polarity', 'Link On', '', '', '', '', '')})))
BANK_DEFINITIONS['Chorus2'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Mode',
                         'Rate',
                         'Amount',
                         'Feedback',
                         use('Offset').if_parameter('Mode').has_value('Vibrato').else_use('Width'),
                         'Gain',
                         'Warmth',
                         'Dry/Wet')}),))
BANK_DEFINITIONS['Collision'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Res 1 Brightness',
                         'Res 1 Type',
                         'Mallet Stiffness',
                         'Mallet Noise Amount',
                         use('Res 1 Opening').if_parameter('Res 1 Type').has_value_in(('Tube', 'Pipe')).else_use('Res 1 Inharmonics'),
                         'Res 1 Decay',
                         'Res 1 Tune',
                         'Volume')}),
 (
  'Mallet',
  {BANK_PARAMETERS_KEY: ('Mallet On/Off', 'Mallet Volume', 'Mallet Noise Amount', 'Mallet Stiffness', 'Mallet Noise Color',
 '', '', '')}),
 (
  'Noise',
  {BANK_PARAMETERS_KEY: ('Noise Volume', 'Noise Filter Type', 'Noise Filter Freq', 'Noise Filter Q', 'Noise Attack',
 'Noise Decay', 'Noise Sustain', 'Noise Release')}),
 (
  'Resonator 1, Set A',
  {BANK_PARAMETERS_KEY: (
                         'Res 1 Decay',
                         use('Res 1 Radius').if_parameter('Res 1 Type').has_value_in(('Tube', 'Pipe')).else_use('Res 1 Material'),
                         'Res 1 Type',
                         'Res 1 Quality',
                         'Res 1 Tune',
                         'Res 1 Fine Tune',
                         'Res 1 Pitch Env.',
                         'Res 1 Pitch Env. Time')}),
 (
  'Resonator 1, Set B',
  {BANK_PARAMETERS_KEY: (
                         'Res 1 Listening L',
                         'Res 1 Listening R',
                         'Res 1 Hit',
                         'Res 1 Brightness',
                         'Res 1 Decay',
                         use('Res 1 Radius').if_parameter('Res 1 Type').has_value_in(('Tube', 'Pipe')).else_use('Res 1 Material'),
                         use('Res 1 Opening').if_parameter('Res 1 Type').has_value_in(('Tube', 'Pipe')).else_use('Res 1 Inharmonics'),
                         'Res 1 Ratio')}),
 (
  'Resonator 2, Set A',
  {BANK_PARAMETERS_KEY: (
                         'Res 2 Decay',
                         use('Res 2 Radius').if_parameter('Res 2 Type').has_value_in(('Tube', 'Pipe')).else_use('Res 2 Material'),
                         'Res 2 Type',
                         'Res 2 Quality',
                         'Res 2 Tune',
                         'Res 2 Fine Tune',
                         'Res 2 Pitch Env.',
                         'Res 2 Pitch Env. Time')}),
 (
  'Resonator 2, Set B',
  {BANK_PARAMETERS_KEY: (
                         'Res 2 Listening L',
                         'Res 2 Listening R',
                         'Res 2 Hit',
                         'Res 2 Brightness',
                         'Res 2 Decay',
                         use('Res 2 Radius').if_parameter('Res 2 Type').has_value_in(('Tube', 'Pipe')).else_use('Res 2 Material'),
                         use('Res 2 Opening').if_parameter('Res 2 Type').has_value_in(('Tube', 'Pipe')).else_use('Res 2 Inharmonics'),
                         'Res 2 Ratio')})))
BANK_DEFINITIONS['Compressor2'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Threshold',
                         use('Expansion Ratio').if_parameter('Model').has_value('Expand').else_use('Ratio'),
                         'Model',
                         'Knee',
                         'Attack',
                         'Release',
                         'Dry/Wet',
                         'Output Gain')}),
 (
  'Sidechain',
  {BANK_PARAMETERS_KEY: (
                         'S/C On',
                         'S/C Gain',
                         'S/C Mix',
                         'S/C Listen',
                         'S/C EQ On',
                         'S/C EQ Type',
                         'S/C EQ Freq',
                         use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value_in(('Low Shelf', 'High Shelf',
                                                             'Bell')).else_use('S/C EQ Q'))}),
 (
  'Global',
  {BANK_PARAMETERS_KEY: (
                         'Auto Release On/Off',
                         'Env Mode',
                         use('Makeup').if_parameter('S/C On').has_value('Off'),
                         'LookAhead',
                         '',
                         '',
                         'Dry/Wet',
                         'Output Gain')})))
BANK_DEFINITIONS['Corpus'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Resonance Type',
                         'Brightness',
                         'Decay',
                         use('Radius').if_parameter('Resonance Type').has_value_in(('Tube', 'Pipe')).else_use('Material'),
                         use('Opening').if_parameter('Resonance Type').has_value_in(('Tube', 'Pipe')).else_use('Inharmonics'),
                         'Ratio',
                         use('Transpose').if_parameter('MIDI Frequency').has_value('On').else_use('Tune'),
                         use('Dry Wet').with_name('Dry/Wet'))}),
 (
  'Body',
  {BANK_PARAMETERS_KEY: (
                         'Resonance Type',
                         'Ratio',
                         'Decay',
                         use('Radius').if_parameter('Resonance Type').has_value_in(('Tube', 'Pipe')).else_use('Material'),
                         use('Opening').if_parameter('Resonance Type').has_value_in(('Tube', 'Pipe')).else_use('Inharmonics'),
                         'Listening L',
                         'Listening R',
                         'Hit')}),
 (
  'LFO',
  {BANK_PARAMETERS_KEY: (
                         'LFO On/Off',
                         'LFO Shape',
                         'LFO Amount',
                         'LFO Sync',
                         use('LFO Rate').if_parameter('LFO Sync').has_value('Free').else_use('LFO Sync Rate'),
                         use('LFO Stereo Mode').if_parameter('LFO Sync').has_value('Free').else_use('Offset'),
                         use('Phase').if_parameter('LFO Sync').has_value('Sync').or_parameter('LFO Stereo Mode').has_value('Phase').else_use('Spin'),
                         '')}),
 (
  'Tune & Sidechain',
  {BANK_PARAMETERS_KEY: (
                         'MIDI Frequency',
                         'MIDI Mode',
                         use('Transpose').if_parameter('MIDI Frequency').has_value('On').else_use('Tune'),
                         'Fine',
                         'Spread',
                         'Brightness',
                         'Note Off',
                         'Off Decay')}),
 (
  'Filter & Mix',
  {BANK_PARAMETERS_KEY: (
                         'Filter On/Off',
                         'Mid Freq',
                         'Width',
                         'Resonator Quality',
                         'Bleed',
                         'Gain',
                         use('Dry Wet').with_name('Dry/Wet'),
                         '')})))
BANK_DEFINITIONS['Delay'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         use('L Sync Enum').with_name('DlayMd L'),
                         use('L 16th').if_parameter('L Sync').has_value('On').else_use('L Time'),
                         'L Offset',
                         use('R Sync Enum').with_name('DlayMd R').if_parameter('Link').has_value('Off').else_use('L Sync Enum').with_name('DlayMd L'),
                         use('R 16th').if_parameter('R Sync').has_value('On').and_parameter('Link').has_value('Off').else_use('R Time').if_parameter('Link').has_value('Off').else_use('L 16th').if_parameter('L Sync').has_value('On').else_use('L Time'),
                         'R Offset',
                         'Feedback',
                         'Dry/Wet')}),
 (
  'Time',
  {BANK_PARAMETERS_KEY: (
                         use('Delay Mode').with_name('DlayMd'),
                         'Link',
                         'Ping Pong',
                         'L Offset',
                         'R Offset',
                         'Freeze',
                         'Feedback',
                         'Dry/Wet')}),
 (
  'Filter/Mod',
  {BANK_PARAMETERS_KEY: (
                         'Filter On',
                         'Filter Freq',
                         'Filter Width',
                         use('Mod Freq').with_name('Filter Mod Rate'),
                         'Filter < Mod',
                         'Dly < Mod',
                         'Feedback',
                         'Dry/Wet')})))
BANK_DEFINITIONS['Drift'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Osc 1 Wave', 'Osc 1 Shape', 'Osc 1 Oct', 'Osc 1 Gain', 'Osc 2 Gain', 'LP Freq', 'LP Reso',
 'Volume')}),
 (
  'Oscillator',
  {BANK_PARAMETERS_KEY: ('Osc 1 Wave', 'Osc 1 Shape', 'Osc 1 Oct', 'Osc 1 Gain', 'Osc 2 Wave', 'Osc 2 Detune',
 'Osc 2 Oct', 'Osc 2 Gain')}),
 (
  'Filter',
  {BANK_PARAMETERS_KEY: ('LP Type', 'LP Freq', 'LP Reso', 'HP Freq', 'LP Mod Src 1', 'LP Mod Amt 1', 'LP Mod Src 2',
 'LP Mod Amt 2')}),
 (
  'Envelopes',
  {BANK_PARAMETERS_KEY: ('Env 1 Attack', 'Env 1 Decay', 'Env 1 Sustain', 'Env 1 Release', 'Env 2 Attack', 'Env 2 Decay',
 'Env 2 Sustain', 'Env 2 Release')}),
 (
  'LFO',
  {BANK_PARAMETERS_KEY: (
                         'LFO Wave',
                         'LFO Time Mode',
                         use('LFO Rate').if_parameter('LFO Time Mode').has_value('Freq').else_use('LFO Ratio').if_parameter('LFO Time Mode').has_value('Ratio').else_use('LFO Time').if_parameter('LFO Time Mode').has_value('Time').else_use('LFO Synced'),
                         'LFO Amt',
                         'Cyc Env Tilt',
                         'Cyc Env Hold',
                         'Cyc Env Time Mode',
                         use('Cyc Env Rate').if_parameter('Cyc Env Time Mode').has_value('Freq').else_use('Cyc Env Ratio').if_parameter('Cyc Env Time Mode').has_value('Ratio').else_use('Cyc Env Time').if_parameter('Cyc Env Time Mode').has_value('Time').else_use('Cyc Env Synced'))}),
 (
  'Modulation',
  {BANK_PARAMETERS_KEY: ('Osc 1 Shape Mod Amt', 'Pitch Mod Amt 1', 'Pitch Mod Amt 2', 'LP Mod Amt 1', 'LP Mod Amt 2',
 'LFO Mod Amt', 'Vel > Vol', '')}),
 (
  'Global',
  {BANK_PARAMETERS_KEY: (
                         'Voice Mode',
                         use('').if_parameter('Voice Mode').has_value('Poly').else_use('Thickness').if_parameter('Voice Mode').has_value('Mono').else_use('Spread').if_parameter('Voice Mode').has_value('Stereo').else_use('Strength').if_parameter('Voice Mode').has_value('Unison'),
                         'Voice Count',
                         'Glide Time',
                         'Drift',
                         'Transpose',
                         'Noise Gain',
                         'Volume')})))
BANK_DEFINITIONS['DrumBuss'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Drive', 'Drive Type', 'Crunch', 'Boom Amt', 'Trim', 'Damping Freq', 'Output Gain',
 'Dry/Wet')}),
 (
  'Drive',
  {BANK_PARAMETERS_KEY: ('Drive', 'Drive Type', 'Transients', 'Crunch', 'Boom Freq', 'Boom Amt', 'Boom Decay',
 'Boom Audition')}),
 (
  'Gain',
  {BANK_PARAMETERS_KEY: ('Trim', 'Output Gain', 'Dry/Wet', 'Compressor On', 'Damping Freq', '', '', '')})))
BANK_DEFINITIONS['Tube'] = IndexedDict((
 (
  'Character',
  {BANK_PARAMETERS_KEY: ('Drive', 'Tube Type', 'Bias', 'Tone', 'Attack', 'Release', 'Envelope', 'Dry/Wet')}),
 (
  'Output', {BANK_PARAMETERS_KEY: ('', '', '', '', '', '', 'Output', 'Dry/Wet')})))
BANK_DEFINITIONS['FilterEQ3'] = IndexedDict((
 (
  'EQ',
  {BANK_PARAMETERS_KEY: ('LowOn', 'MidOn', 'HighOn', 'GainLo', 'GainMid', 'GainHi', 'FreqLo', 'FreqHi')}),
 (
  'Slope', {BANK_PARAMETERS_KEY: ('Slope', '', '', '', '', '', '', '')})))
BANK_DEFINITIONS['Eq8'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('1 Frequency A', '1 Gain A', '2 Frequency A', '2 Gain A', '3 Frequency A', '3 Gain A',
 '4 Frequency A', '4 Gain A')}),
 (
  'Band On/Off',
  {BANK_PARAMETERS_KEY: ('1 Filter On A', '2 Filter On A', '3 Filter On A', '4 Filter On A', '5 Filter On A',
 '6 Filter On A', '7 Filter On A', '8 Filter On A')}),
 (
  'Frequency',
  {BANK_PARAMETERS_KEY: ('1 Frequency A', '2 Frequency A', '3 Frequency A', '4 Frequency A', '5 Frequency A',
 '6 Frequency A', '7 Frequency A', '8 Frequency A')}),
 (
  'Gain',
  {BANK_PARAMETERS_KEY: ('1 Gain A', '2 Gain A', '3 Gain A', '4 Gain A', '5 Gain A', '6 Gain A', '7 Gain A',
 '8 Gain A')}),
 (
  'Resonance',
  {BANK_PARAMETERS_KEY: ('1 Resonance A', '2 Resonance A', '3 Resonance A', '4 Resonance A', '5 Resonance A',
 '6 Resonance A', '7 Resonance A', '8 Resonance A')}),
 (
  'Filter Type',
  {BANK_PARAMETERS_KEY: ('1 Filter Type A', '2 Filter Type A', '3 Filter Type A', '4 Filter Type A', '5 Filter Type A',
 '6 Filter Type A', '7 Filter Type A', '8 Filter Type A')}),
 (
  'Output',
  {BANK_PARAMETERS_KEY: ('Adaptive Q', '', '', '', '', '', 'Scale', 'Output Gain')}),
 (
  'EQs 3-5',
  {BANK_PARAMETERS_KEY: ('3 Gain A', '3 Frequency A', '3 Resonance A', '4 Gain A', '4 Frequency A', '4 Resonance A',
 '5 Gain A', '5 Frequency A')})))
BANK_DEFINITIONS['Echo'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         use('L Time').with_name('M Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync').has_value('Off').else_use('L Time').if_parameter('L Sync').has_value('Off').else_use('L 16th').with_name('M 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync Mode').has_value('16th').else_use('L 16th').if_parameter('L Sync Mode').has_value('16th').else_use('L Division').with_name('M Division').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Division'),
                         use('L Sync').with_name('M Sync').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync'),
                         use('L Sync Mode').with_name('M Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync Mode'),
                         'HP Freq',
                         'LP Freq',
                         'Feedback',
                         'Input Gain',
                         use('Dry Wet').with_name('Dry/Wet'))}),
 (
  'L/Mid',
  {BANK_PARAMETERS_KEY: (
                         use('L Time').with_name('M Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync').has_value('Off').else_use('L Time').if_parameter('L Sync').has_value('Off').else_use('L 16th').with_name('M 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync Mode').has_value('16th').else_use('L 16th').if_parameter('L Sync Mode').has_value('16th').else_use('L Division').with_name('M Division').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Division'),
                         use('L Sync').with_name('M Sync').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync'),
                         use('L Sync Mode').with_name('M Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync Mode'),
                         use('L Offset').with_name('M Offset').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Offset'),
                         'Link',
                         'Feedback',
                         'Feedback Inv',
                         use('Dry Wet').with_name('Dry/Wet'))}),
 (
  'R/Side',
  {BANK_PARAMETERS_KEY: (
                         use('R Time').with_name('S Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('R Sync').has_value('Off').and_parameter('Link').has_value('Off').else_use('R Time').if_parameter('R Sync').has_value('Off').and_parameter('Link').has_value('Off').else_use('R 16th').with_name('S 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('R Sync Mode').has_value('16th').and_parameter('Link').has_value('Off').else_use('R 16th').if_parameter('R Sync Mode').has_value('16th').and_parameter('Link').has_value('Off').else_use('R Division').with_name('S Division').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('Link').has_value('Off').else_use('R Division').if_parameter('Link').has_value('Off').else_use('L Time').with_name('M Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync').has_value('Off').else_use('L Time').if_parameter('L Sync').has_value('Off').else_use('L 16th').with_name('M 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync Mode').has_value('16th').else_use('L 16th').if_parameter('L Sync Mode').has_value('16th').else_use('L Division').with_name('M Division').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Division'),
                         use('R Sync').with_name('S Sync').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('Link').has_value('Off').else_use('R Sync').if_parameter('Link').has_value('Off').else_use('L Sync').with_name('M Sync').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync'),
                         use('R Sync Mode').with_name('S Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('Link').has_value('Off').else_use('R Sync Mode').if_parameter('Link').has_value('Off').else_use('L Sync Mode').with_name('M Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync Mode'),
                         use('R Offset').with_name('S Offset').if_parameter('Channel Mode').has_value('Mid/Side').else_use('R Offset'),
                         'Link',
                         'Feedback',
                         'Feedback Inv',
                         use('Dry Wet').with_name('Dry/Wet'))}),
 (
  'Global',
  {BANK_PARAMETERS_KEY: (
                         'Repitch',
                         'Channel Mode',
                         'Stereo Width',
                         '',
                         'Clip Dry',
                         'Input Gain',
                         'Output Gain',
                         use('Dry Wet').with_name('Dry/Wet'))}),
 (
  'Filter',
  {BANK_PARAMETERS_KEY: (
                         'Filter On',
                         'HP Freq',
                         'HP Res',
                         'LP Freq',
                         'LP Res',
                         'Input Gain',
                         'Output Gain',
                         use('Dry Wet').with_name('Dry/Wet'))}),
 (
  'Modulation',
  {BANK_PARAMETERS_KEY: (
                         'Mod Wave',
                         'Mod Sync',
                         use('Mod Rate').if_parameter('Mod Sync').has_value('On').else_use('Mod Freq'),
                         'Mod Phase',
                         'Env Mix',
                         'Dly < Mod',
                         'Flt < Mod',
                         'Mod 4x')}),
 (
  'Reverb',
  {BANK_PARAMETERS_KEY: ('Reverb Level', 'Reverb Loc', 'Reverb Decay', '', '', '', '', '')}),
 (
  'Gate/Ducking',
  {BANK_PARAMETERS_KEY: ('Gate On', 'Gate Thr', 'Gate Release', '', 'Duck On', 'Duck Thr', 'Duck Release',
 '')}),
 (
  'Noise/Wobble',
  {BANK_PARAMETERS_KEY: ('Noise On', 'Noise Amt', 'Noise Mrph', '', 'Wobble On', 'Wobble Amt', 'Wobble Mrph',
 '')})))
BANK_DEFINITIONS['LoungeLizard'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('M Stiffness', 'M Force', 'Noise Amount', 'F Tine Vol', 'F Tone Vol', 'F Release',
 'P Symmetry', 'Volume')}),
 (
  'Mallet',
  {BANK_PARAMETERS_KEY: ('M Stiffness', 'M Force', 'Noise Pitch', 'Noise Decay', 'Noise Amount', 'M Stiff < Vel',
 'M Force < Vel', 'Volume')}),
 (
  'Fork',
  {BANK_PARAMETERS_KEY: ('F Tine Color', 'F Tine Decay', 'F Tine Vol', 'F Tone Vol', 'F Tone Decay', 'F Release',
 'F Tine < Key', 'Volume')}),
 (
  'Damper',
  {BANK_PARAMETERS_KEY: ('Damp Tone', 'Damp Balance', 'Damp Amount', '', '', '', '', 'Volume')}),
 (
  'Pickup',
  {BANK_PARAMETERS_KEY: ('P Symmetry', 'P Distance', 'P Amp In', 'P Amp Out', 'Pickup Model', 'P Amp < Key',
 '', 'Volume')}),
 (
  'Modulation',
  {BANK_PARAMETERS_KEY: ('M Stiff < Vel', 'M Stiff < Key', 'M Force < Vel', 'M Force < Key', 'Noise < Key',
 'F Tine < Key', 'P Amp < Key', 'Volume')}),
 (
  'Global',
  {BANK_PARAMETERS_KEY: ('KB Stretch', 'PB Range', '', '', 'Voices', 'Semitone', 'Detune', 'Volume')})))
BANK_DEFINITIONS['Erosion'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Mode', 'Frequency', 'Width', 'Amount', '', '', '', '')}),))
BANK_DEFINITIONS['ProxyAudioEffectDevice'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Input Gain', 'Output Gain', 'Dry/Wet', '', '', '', '', '')}),))
BANK_DEFINITIONS['FilterDelay'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         '2 Filter Freq',
                         '2 Filter Width',
                         use('2 Time Delay').if_parameter('2 Delay Mode').has_value('Off').else_use('2 Beat Delay'),
                         '2 Feedback',
                         '1 Volume',
                         '2 Volume',
                         '3 Volume',
                         'Dry')}),
 (
  'L Filter',
  {BANK_PARAMETERS_KEY: (
                         '1 Input On',
                         '1 Filter Freq',
                         '1 Filter Width',
                         '1 Feedback',
                         '1 Delay Mode',
                         use('1 Time Delay').if_parameter('1 Delay Mode').has_value('Off').else_use('1 Beat Delay'),
                         '1 Beat Swing',
                         '1 Volume')}),
 (
  'L+R Filter',
  {BANK_PARAMETERS_KEY: (
                         '2 Input On',
                         '2 Filter Freq',
                         '2 Filter Width',
                         '2 Feedback',
                         '2 Delay Mode',
                         use('2 Time Delay').if_parameter('2 Delay Mode').has_value('Off').else_use('2 Beat Delay'),
                         '2 Beat Swing',
                         '2 Volume')}),
 (
  'R Filter',
  {BANK_PARAMETERS_KEY: (
                         '3 Input On',
                         '3 Filter Freq',
                         '3 Filter Width',
                         '3 Feedback',
                         '3 Delay Mode',
                         use('3 Time Delay').if_parameter('3 Delay Mode').has_value('Off').else_use('3 Beat Delay'),
                         '3 Beat Swing',
                         '3 Volume')}),
 (
  'Mix',
  {BANK_PARAMETERS_KEY: ('1 Pan', '2 Pan', '3 Pan', '', '1 Volume', '2 Volume', '3 Volume', 'Dry')})))
BANK_DEFINITIONS['Flanger'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'LFO Amount',
                         'Sync',
                         use('Frequency').if_parameter('Sync').has_value('Free').else_use('Sync Rate'),
                         'Delay Time',
                         'Hi Pass',
                         'Env. Modulation',
                         'Feedback',
                         'Dry/Wet')}),
 (
  'Envelope',
  {BANK_PARAMETERS_KEY: ('Env. Attack', 'Env. Release', 'Env. Modulation', 'Hi Pass', 'Delay Time', 'Feedback',
 'Polarity', 'Dry/Wet')}),
 (
  'LFO / S&H',
  {BANK_PARAMETERS_KEY: (
                         'LFO Amount',
                         'LFO Waveform',
                         'Sync',
                         use('Frequency').if_parameter('Sync').has_value('Free').else_use('Sync Rate'),
                         use('LFO Stereo Mode').if_parameter('Sync').has_value('Free').else_use('LFO Offset'),
                         use('LFO Width (Random)').if_parameter('LFO Waveform').has_value('S&H Width').else_use('LFO Phase').if_parameter('Sync').has_value('Sync').or_parameter('LFO Stereo Mode').has_value('Phase').else_use('LFO Spin'),
                         '',
                         '')})))
BANK_DEFINITIONS['FrequencyShifter'] = IndexedDict((
 (
  'FreqDrive',
  {BANK_PARAMETERS_KEY: (
                         'Mode',
                         use('Ring Mod Frequency').if_parameter('Mode').has_value('Ring Modulation').else_use('Coarse'),
                         'Wide',
                         'Fine',
                         'Drive On/Off',
                         'Drive',
                         'LFO Amount',
                         'Dry/Wet')}),
 (
  'LFO / S&H',
  {BANK_PARAMETERS_KEY: (
                         'LFO Amount',
                         'LFO Waveform',
                         'Sync',
                         use('LFO Frequency').if_parameter('Sync').has_value('Free').else_use('Sync Rate'),
                         use('LFO Stereo Mode').if_parameter('Sync').has_value('Free').else_use('LFO Offset'),
                         use('LFO Width (Random)').if_parameter('LFO Waveform').has_value('S&H Width').else_use('LFO Phase').if_parameter('Sync').has_value('Sync').or_parameter('LFO Stereo Mode').has_value('Phase').else_use('LFO Spin'),
                         '',
                         '')})))
BANK_DEFINITIONS['Gate'] = IndexedDict((
 (
  'Gate',
  {BANK_PARAMETERS_KEY: ('Threshold', 'Return', 'FlipMode', 'LookAhead', 'Attack', 'Hold', 'Release', 'Floor')}),
 (
  'Sidechain',
  {BANK_PARAMETERS_KEY: (
                         'S/C On',
                         'S/C Gain',
                         'S/C Mix',
                         'S/C Listen',
                         'S/C EQ On',
                         'S/C EQ Type',
                         'S/C EQ Freq',
                         use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value_in(('Low Shelf', 'High Shelf',
                                                             'Bell')).else_use('S/C EQ Q'))})))
BANK_DEFINITIONS['GlueCompressor'] = IndexedDict((
 (
  'Compression',
  {BANK_PARAMETERS_KEY: ('Threshold', 'Ratio', 'Attack', 'Release', 'Peak Clip In', 'Range', 'Makeup', 'Dry/Wet')}),
 (
  'Sidechain',
  {BANK_PARAMETERS_KEY: (
                         'S/C On',
                         'S/C Gain',
                         'S/C Mix',
                         '',
                         'S/C EQ On',
                         'S/C EQ Type',
                         'S/C EQ Freq',
                         use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value_in(('Low Shelf', 'High Shelf',
                                                             'Bell')).else_use('S/C EQ Q'))})))
BANK_DEFINITIONS['GrainDelay'] = IndexedDict((
 (
  'Pitch',
  {BANK_PARAMETERS_KEY: (
                         'Frequency',
                         'Pitch',
                         'Delay Mode',
                         use('Time Delay').if_parameter('Delay Mode').has_value('Off').else_use('Beat Delay'),
                         'Random',
                         'Spray',
                         'Feedback',
                         'DryWet')}),
 (
  'Time',
  {BANK_PARAMETERS_KEY: (
                         'Delay Mode',
                         use('Time Delay').if_parameter('Delay Mode').has_value('Off').else_use('Beat Delay'),
                         'Beat Swing',
                         'Feedback',
                         '',
                         '',
                         '',
                         'DryWet')})))
BANK_DEFINITIONS['Hybrid'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         use('Send Gain').with_name('Send'),
                         'Routing',
                         'Blend',
                         use('Algo Type').with_name('Type'),
                         'Decay',
                         'Size',
                         use('').if_parameter('Algo Type').has_value('Prism').else_use('Ti Waveform').with_name('Wave').if_parameter('Algo Type').has_value('Tides').else_use('Modulation').with_name('Mod'),
                         'Dry/Wet')}),
 (
  'Algorithm Pg1',
  {BANK_PARAMETERS_KEY: (
                         use('Algo Type').with_name('Type'),
                         'Decay',
                         'Size',
                         use('DH Shape').with_name('Shape').if_parameter('Algo Type').has_value('Dark Hall').else_use('Qz Low Damp').with_name('Low Damping').if_parameter('Algo Type').has_value('Quartz').else_use('Sh Pitch Shift').with_name('Pitch').if_parameter('Algo Type').has_value('Shimmer').else_use('Ti Tide').with_name('Tide').if_parameter('Algo Type').has_value('Tides').else_use('Pr High Mult').with_name('High Mult'),
                         use('DH BassMult').with_name('Bass Mult').if_parameter('Algo Type').has_value('Dark Hall').else_use('Qz Distance').with_name('Distance').if_parameter('Algo Type').has_value('Quartz').else_use('Sh Shimmer').with_name('Shimmer').if_parameter('Algo Type').has_value('Shimmer').else_use('Ti Rate').with_name('Rate').if_parameter('Algo Type').has_value('Tides').else_use('Pr X Over').with_name('X Over'),
                         use('').if_parameter('Algo Type').has_value('Prism').else_use('Ti Waveform').with_name('Wave').if_parameter('Algo Type').has_value('Tides').else_use('Modulation').with_name('Mod'),
                         use('Width').with_name('Stereo'),
                         'Dry/Wet')}),
 (
  'Algorithm Pg2',
  {BANK_PARAMETERS_KEY: (
                         use('Algo Type').with_name('Type'),
                         use('Pr Low Mult').with_name('Low Mult').if_parameter('Algo Type').has_value('Prism').else_use('Damping'),
                         use('DH Bass X').with_name('Bass X').if_parameter('Algo Type').has_value('Dark Hall').else_use('Diffusion').if_parameter('Algo Type').has_value_in(('Quartz',
                                                                                                                                                    'Shimmer')).else_use('Ti Phase').with_name('Phase').if_parameter('Algo Type').has_value('Tides').else_use(''),
                         use('EQ Pre Algo').with_name('Pre Algo'),
                         use('Send Gain').with_name('Send'),
                         'Blend',
                         'Routing',
                         'Dry/Wet')}),
 (
  'EQ Pg1',
  {BANK_PARAMETERS_KEY: (
                         use('EQ Pre Algo').with_name('Pre Algo'),
                         use('EQ Low Type').with_name('Low Type'),
                         use('EQ Low Freq').with_name('Low Freq'),
                         use('EQ Low Gain').with_name('Low Gain').if_parameter('EQ Low Type').has_value('Shelf').else_use('EQ Low Slope').with_name('Low Slope'),
                         use('EQ High Type').with_name('High Type'),
                         use('EQ High Freq').with_name('High Freq'),
                         use('EQ High Gain').with_name('High Gain').if_parameter('EQ High Type').has_value('Shelf').else_use('EQ High Slope').with_name('High Slope'),
                         'Dry/Wet')}),
 (
  'EQ Pg2',
  {BANK_PARAMETERS_KEY: (
                         use('EQ Pre Algo').with_name('Pre Algo'),
                         use('EQ P1 Freq').with_name('2 Freq'),
                         use('EQ P1 Q').with_name('2 Q'),
                         use('EQ P1 Gain').with_name('2 Gain'),
                         use('EQ P2 Freq').with_name('3 Freq'),
                         use('EQ P2 Q').with_name('3 Q'),
                         use('EQ P2 Gain').with_name('3 Gain'),
                         'Dry/Wet')}),
 (
  'Global',
  {BANK_PARAMETERS_KEY: (
                         use('Send Gain').with_name('Send'),
                         use('P.Dly Sync').with_name('Predelay Type'),
                         use('P.Dly Time').with_name('Predelay').if_parameter('P.Dly Sync').has_value('Off').else_use('P.Dly 16th').with_name('Predelay'),
                         use('P.Dly Fb Time').with_name('Predelay FB').if_parameter('P.Dly Sync').has_value('Off').else_use('P.Dly Fb 16th').with_name('Predelay FB'),
                         'Vintage',
                         use('Width').with_name('Stereo'),
                         'Blend',
                         'Dry/Wet')})))
BANK_DEFINITIONS['InstrumentImpulse'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Global Time', 'Global Transpose', '1 Transpose', '2 Transpose', '3 Transpose', '4 Transpose',
 '5 Transpose', '6 Transpose')}),
 (
  'Pad 1',
  {BANK_PARAMETERS_KEY: ('1 Start', '1 Transpose', '1 Stretch Factor', '1 Saturator Drive', '1 Filter Freq',
 '1 Filter Res', '1 Pan', '1 Volume')}),
 (
  'Pad 2',
  {BANK_PARAMETERS_KEY: ('2 Start', '2 Transpose', '2 Stretch Factor', '2 Saturator Drive', '2 Filter Freq',
 '2 Filter Res', '2 Pan', '2 Volume')}),
 (
  'Pad 3',
  {BANK_PARAMETERS_KEY: ('3 Start', '3 Transpose', '3 Stretch Factor', '3 Saturator Drive', '3 Filter Freq',
 '3 Filter Res', '3 Pan', '3 Volume')}),
 (
  'Pad 4',
  {BANK_PARAMETERS_KEY: ('4 Start', '4 Transpose', '4 Stretch Factor', '4 Saturator Drive', '4 Filter Freq',
 '4 Filter Res', '4 Pan', '4 Volume')}),
 (
  'Pad 5',
  {BANK_PARAMETERS_KEY: ('5 Start', '5 Transpose', '5 Stretch Factor', '5 Saturator Drive', '5 Filter Freq',
 '5 Filter Res', '5 Pan', '5 Volume')}),
 (
  'Pad 6',
  {BANK_PARAMETERS_KEY: ('6 Start', '6 Transpose', '6 Stretch Factor', '6 Saturator Drive', '6 Filter Freq',
 '6 Filter Res', '6 Pan', '6 Volume')}),
 (
  'Pad 7',
  {BANK_PARAMETERS_KEY: ('7 Start', '7 Transpose', '7 Stretch Factor', '7 Saturator Drive', '7 Filter Freq',
 '7 Filter Res', '7 Pan', '7 Volume')}),
 (
  'Pad 8',
  {BANK_PARAMETERS_KEY: ('8 Start', '8 Transpose', '8 Stretch Factor', '8 Saturator Drive', '8 Filter Freq',
 '8 Filter Res', '8 Pan', '8 Volume')})))
BANK_DEFINITIONS['Limiter'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Gain', 'Ceiling', 'Link Channels', 'Lookahead', 'Auto', 'Release time', '', '')}),))
BANK_DEFINITIONS['Looper'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('State', 'Speed', 'Reverse', 'Quantization', 'Monitor', 'Song Control', 'Tempo Control',
 'Feedback')}),))
BANK_DEFINITIONS['MultibandDynamics'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         use('Above Threshold (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                         use('Above Ratio (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                         use('Above Threshold (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                         use('Above Ratio (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                         use('Above Threshold (High)').if_parameter('Band Activator (High)').has_value('On'),
                         use('Above Ratio (High)').if_parameter('Band Activator (High)').has_value('On'),
                         'Master Output',
                         'Amount')}),
 (
  'Low Band',
  {BANK_PARAMETERS_KEY: (
                         'Band Activator (Low)',
                         'Input Gain (Low)',
                         use('Below Threshold (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                         use('Below Ratio (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                         use('Above Threshold (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                         use('Above Ratio (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                         'Attack Time (Low)',
                         'Release Time (Low)')}),
 (
  'Mid Band',
  {BANK_PARAMETERS_KEY: (
                         'Band Activator (Mid)',
                         'Input Gain (Mid)',
                         use('Below Threshold (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                         use('Below Ratio (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                         use('Above Threshold (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                         use('Above Ratio (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                         'Attack Time (Mid)',
                         'Release Time (Mid)')}),
 (
  'High Band',
  {BANK_PARAMETERS_KEY: (
                         'Band Activator (High)',
                         'Input Gain (High)',
                         use('Below Threshold (High)').if_parameter('Band Activator (High)').has_value('On'),
                         use('Below Ratio (High)').if_parameter('Band Activator (High)').has_value('On'),
                         use('Above Threshold (High)').if_parameter('Band Activator (High)').has_value('On'),
                         use('Above Ratio (High)').if_parameter('Band Activator (High)').has_value('On'),
                         'Attack Time (High)',
                         'Release Time (High)')}),
 (
  'Mix & Split',
  {BANK_PARAMETERS_KEY: ('Output Gain (Low)', 'Low-Mid Crossover', 'Output Gain (Mid)', 'Mid-High Crossover',
 'Output Gain (High)', 'Peak/RMS Mode', 'Amount', 'Master Output')}),
 (
  'Sidechain',
  {BANK_PARAMETERS_KEY: ('S/C On', 'S/C Mix', 'S/C Gain', '', 'Time Scaling', 'Soft Knee On/Off', '', '')})))
BANK_DEFINITIONS['MidiNoteLength'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Trigger Mode',
                         'Sync On',
                         use('Synced Length').if_parameter('Sync On').has_value('On').else_use('Time Length'),
                         'Gate',
                         'On/Off-Balance',
                         'Decay Time',
                         'Decay Key Scale',
                         '')}),))
BANK_DEFINITIONS['Operator'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Filter Freq',
                         'Filter Res',
                         use('A Coarse').if_parameter('A Fix On ').has_value('Off').else_use('A Fix Freq'),
                         use('A Fine').if_parameter('A Fix On ').has_value('Off').else_use('A Fix Freq Mul'),
                         use('B Coarse').if_parameter('B Fix On ').has_value('Off').else_use('B Fix Freq'),
                         use('B Fine').if_parameter('B Fix On ').has_value('Off').else_use('B Fix Freq Mul'),
                         'Osc-B Level',
                         'Volume')}),
 (
  'Oscillator A',
  {BANK_PARAMETERS_KEY: (
                         'Ae Attack',
                         'Ae Decay',
                         'Ae Sustain',
                         'Ae Release',
                         use('A Coarse').if_parameter('A Fix On ').has_value('Off').else_use('A Fix Freq'),
                         use('A Fine').if_parameter('A Fix On ').has_value('Off').else_use('A Fix Freq Mul'),
                         'Osc-A Lev < Vel',
                         'Osc-A Level')}),
 (
  'Oscillator B',
  {BANK_PARAMETERS_KEY: (
                         'Be Attack',
                         'Be Decay',
                         'Be Sustain',
                         'Be Release',
                         use('B Coarse').if_parameter('B Fix On ').has_value('Off').else_use('B Fix Freq'),
                         use('B Fine').if_parameter('B Fix On ').has_value('Off').else_use('B Fix Freq Mul'),
                         'Osc-B Lev < Vel',
                         'Osc-B Level')}),
 (
  'Oscillator C',
  {BANK_PARAMETERS_KEY: (
                         'Ce Attack',
                         'Ce Decay',
                         'Ce Sustain',
                         'Ce Release',
                         use('C Coarse').if_parameter('C Fix On ').has_value('Off').else_use('C Fix Freq'),
                         use('C Fine').if_parameter('C Fix On ').has_value('Off').else_use('C Fix Freq Mul'),
                         'Osc-C Lev < Vel',
                         'Osc-C Level')}),
 (
  'Oscillator D',
  {BANK_PARAMETERS_KEY: (
                         'De Attack',
                         'De Decay',
                         'De Sustain',
                         'De Release',
                         use('D Coarse').if_parameter('D Fix On ').has_value('Off').else_use('D Fix Freq'),
                         use('D Fine').if_parameter('D Fix On ').has_value('Off').else_use('D Fix Freq Mul'),
                         'Osc-D Lev < Vel',
                         'Osc-D Level')}),
 (
  'LFO',
  {BANK_PARAMETERS_KEY: (
                         'Le Attack',
                         'Le Decay',
                         'Le Sustain',
                         'Le Release',
                         use('LFO Sync').if_parameter('LFO Range').has_value('Sync').else_use('LFO Rate'),
                         'LFO Amt',
                         'LFO Type',
                         'LFO R < K')}),
 (
  'Filter',
  {BANK_PARAMETERS_KEY: ('Fe Attack', 'Fe Decay', 'Fe Sustain', 'Fe Release', 'Filter Freq', 'Filter Res',
 'Fe R < Vel', 'Fe Amount')}),
 (
  'Pitch Modulation',
  {BANK_PARAMETERS_KEY: ('Pe Attack', 'Pe Decay', 'Pe Sustain', 'Pe Release', 'Pe Init', 'Glide Time', 'Pe Amount',
 'Spread')}),
 (
  'Routing',
  {BANK_PARAMETERS_KEY: ('Time < Key', 'Panorama', 'Pan < Key', 'Pan < Rnd', 'Algorithm', 'Time', 'Tone', 'Volume')})))
BANK_DEFINITIONS['Overdrive'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Filter Freq', 'Filter Width', 'Drive', 'Tone', 'Preserve Dynamics', '', '', 'Dry/Wet')}),))
BANK_DEFINITIONS['Pedal'] = IndexedDict((
 (
  'Global',
  {BANK_PARAMETERS_KEY: ('Type', 'Gain', 'Output', 'Bass', 'Mid', 'Treble', 'Sub', 'Dry/Wet')}),
 (
  'EQ',
  {BANK_PARAMETERS_KEY: ('', '', '', 'Bass', 'Mid', 'Treble', '', 'Mid Freq')})))
BANK_DEFINITIONS['Phaser'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Poles',
                         'Frequency',
                         'Feedback',
                         'Env. Modulation',
                         'LFO Amount',
                         'LFO Sync',
                         use('LFO Frequency').if_parameter('LFO Sync').has_value('Free').else_use('LFO Sync Rate'),
                         'Dry/Wet')}),
 (
  'Envelope',
  {BANK_PARAMETERS_KEY: ('Poles', 'Type', 'Color', 'Frequency', 'Feedback', 'Env. Modulation', 'Env. Attack',
 'Env. Release')}),
 (
  'LFO',
  {BANK_PARAMETERS_KEY: (
                         'LFO Amount',
                         'LFO Waveform',
                         'LFO Sync',
                         use('LFO Frequency').if_parameter('LFO Sync').has_value('Free').else_use('LFO Sync Rate'),
                         use('LFO Stereo Mode').if_parameter('LFO Sync').has_value('Free').else_use('LFO Offset'),
                         use('LFO Width (Random)').if_parameter('LFO Waveform').has_value('S&H Width').else_use('LFO Phase').if_parameter('LFO Sync').has_value('Sync').or_parameter('LFO Stereo Mode').has_value('Phase').else_use('LFO Spin'),
                         '',
                         '')})))
BANK_DEFINITIONS['PhaserNew'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Mode',
                         use('Mod Rate').with_name('Rate').if_parameter('Mod Sync').has_value('On').else_use('Mod Freq').with_name('Freq'),
                         'Amount',
                         'Feedback',
                         use('Notches').if_parameter('Mode').has_value('Phaser').else_use('Flange Time').with_name('Time').if_parameter('Mode').has_value('Flanger').else_use('Doubler Time').with_name('Time').if_parameter('Mode').has_value('Doubler'),
                         'Warmth',
                         use('Output Gain').with_name('Gain'),
                         'Dry/Wet')}),
 (
  'Details',
  {BANK_PARAMETERS_KEY: (
                         'Mode',
                         use('Mod Rate').with_name('Rate').if_parameter('Mod Sync').has_value('On').else_use('Mod Freq').with_name('Freq'),
                         'Amount',
                         'Feedback',
                         use('Notches').if_parameter('Mode').has_value('Phaser').else_use('Flange Time').with_name('Time').if_parameter('Mode').has_value('Flanger').else_use('Doubler Time').with_name('Time').if_parameter('Mode').has_value('Doubler'),
                         use('FB Inv'),
                         use('Output Gain').with_name('Gain'),
                         'Dry/Wet')}),
 (
  'LFO2',
  {BANK_PARAMETERS_KEY: (
                         use('Lfo Blend').with_name('LFO2 Mix'),
                         use('Mod Wave').with_name('Waveform'),
                         use('Duty Cycle').with_name('Duty'),
                         use('Spin Enabled').with_name('Spin On/Off'),
                         use('Spin').if_parameter('Spin Enabled').has_value('On').else_use('Mod Phase').with_name('Phase'),
                         use('Mod Sync 2').with_name('LFO2 Sync'),
                         use('Mod Rate 2').with_name('LFO2 Rate').if_parameter('Mod Sync 2').has_value('On').else_use('Mod Freq 2').with_name('LFO2 Freq'),
                         'Dry/Wet')}),
 (
  'LFO2 Env',
  {BANK_PARAMETERS_KEY: (
                         use('Lfo Blend').with_name('LFO2 Mix'),
                         use('Env Enabled').with_name('Env Follow'),
                         'Env Amount',
                         use('Env Attack').with_name('Attack'),
                         use('Env Release').with_name('Release'),
                         use('Safe Freq').with_name('Safe Bass'),
                         use('Output Gain').with_name('Gain'),
                         'Dry/Wet')})))
BANK_DEFINITIONS['MidiPitcher'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Pitch', 'Range', 'Lowest', '', '', '', '', '')}),))
BANK_DEFINITIONS['MidiRandom'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Chance', 'Choices', 'Mode', 'Scale', 'Sign', '', '', '')}),))
BANK_DEFINITIONS['Redux'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Bit On',
                         'Bit Depth',
                         'Sample Mode',
                         use('Sample Hard').if_parameter('Sample Mode').has_value('Hard').else_use('Sample Soft'),
                         '',
                         '',
                         '',
                         '')}),))
BANK_DEFINITIONS['Redux2'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Sample Rate',
                         'Jitter',
                         'Bit Depth',
                         use('Quantizer Shape').with_name('Shape'),
                         'DC Shift',
                         'Pre-Filter On',
                         'Post-Filter',
                         'Dry/Wet')}),))
BANK_DEFINITIONS['Resonator'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Frequency', 'Decay', 'Color', 'I Gain', 'II Gain', 'III Gain', 'Width', 'Dry/Wet')}),
 (
  'Global',
  {BANK_PARAMETERS_KEY: ('Mode', 'Decay', 'Const', 'Color', '', 'Width', 'Global Gain', 'Dry/Wet')}),
 (
  'Filter',
  {BANK_PARAMETERS_KEY: ('Filter On', 'Frequency', 'Filter Type', '', '', '', '', '')}),
 (
  'Mode I & II',
  {BANK_PARAMETERS_KEY: ('I On', 'I Note', 'I Tune', 'I Gain', 'II On', 'II Pitch', 'II Tune', 'II Gain')}),
 (
  'Mode III & IV',
  {BANK_PARAMETERS_KEY: ('III On', 'III Pitch', 'III Tune', 'III Gain', 'IV On', 'IV Pitch', 'IV Tune', 'IV Gain')}),
 (
  'Mode V',
  {BANK_PARAMETERS_KEY: ('V On', 'V Pitch', 'V Tune', 'V Gain', '', '', '', '')}),
 (
  'Mix',
  {BANK_PARAMETERS_KEY: ('I Gain', 'II Gain', 'III Gain', 'IV Gain', 'V Gain', '', '', '')}),
 (
  'Pitch',
  {BANK_PARAMETERS_KEY: ('I Note', 'II Pitch', 'III Pitch', 'IV Pitch', 'V Pitch', '', '', '')})))
BANK_DEFINITIONS['Reverb'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Predelay', 'In Filter Freq', 'Chorus Amount', 'Stereo Image', 'Room Size', 'Decay Time',
 'Diffuse Level', 'Dry/Wet')}),
 (
  'Global',
  {BANK_PARAMETERS_KEY: ('Chorus On', 'Chorus Rate', 'Chorus Amount', 'Density', 'Freeze On', 'Flat On', 'Reflect Level',
 'Diffuse Level')}),
 (
  'Diffusion Network',
  {BANK_PARAMETERS_KEY: ('HiFilter On', 'HiFilter Freq', 'HiShelf Gain', 'LowShelf On', 'LowShelf Freq', 'LowShelf Gain',
 'Diffusion', 'Scale')}),
 (
  'Input/Reflections',
  {BANK_PARAMETERS_KEY: ('In LowCut On', 'In HighCut On', 'In Filter Freq', 'In Filter Width', 'ER Spin On',
 'ER Spin Rate', 'ER Spin Amount', 'ER Shape')})))
BANK_DEFINITIONS['MultiSampler'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Filter Freq', 'Filter Res', 'Fe < Env', 'Fe Decay', 'Ve Attack', 'Ve Release', 'Transpose',
 'Volume')}),
 (
  'Volume',
  {BANK_PARAMETERS_KEY: ('Volume', 'Ve Attack', 'Ve Decay', 'Ve Sustain', 'Ve Release', 'Vol < Vel', 'Ve R < Vel',
 'Time')}),
 (
  'Filter',
  {BANK_PARAMETERS_KEY: (
                         'Filter Type',
                         use('Filter Morph').if_parameter('Filter Type').has_value('Morph').else_use('Filter Drive'),
                         'Filter Freq',
                         'Filter Res',
                         'Filt < Vel',
                         'Filt < Key',
                         'Fe < Env',
                         'Shaper Amt')}),
 (
  'Filter Envelope',
  {BANK_PARAMETERS_KEY: (
                         'Fe Attack',
                         'Fe Peak',
                         'Fe Decay',
                         'Fe Sustain',
                         'Fe Release',
                         'Fe End',
                         'Fe Mode',
                         use('Fe Loop').if_parameter('Fe Mode').has_value('Loop').else_use('Fe Retrig'))}),
 (
  'LFO 1',
  {BANK_PARAMETERS_KEY: (
                         'L 1 On',
                         'L 1 Wave',
                         'L 1 Sync',
                         use('L 1 Sync Rate').if_parameter('L 1 Sync').has_value('Sync').else_use('L 1 Rate'),
                         'Vol < LFO',
                         'Filt < LFO',
                         'Pan < LFO',
                         'Pitch < LFO')}),
 (
  'LFO 2',
  {BANK_PARAMETERS_KEY: (
                         'L 2 On',
                         'L 2 Wave',
                         'L 2 Sync',
                         use('L 2 Sync Rate').if_parameter('L 2 Sync').has_value('Sync').else_use('L 2 Rate'),
                         'L 2 R < Key',
                         'L 2 Offset',
                         'L 2 St Mode',
                         use('L 2 Spin').if_parameter('L 2 St Mode').has_value('Spin').else_use('L 2 Phase'))}),
 (
  'LFO 3',
  {BANK_PARAMETERS_KEY: (
                         'L 3 On',
                         'L 3 Wave',
                         'L 3 Sync',
                         use('L 3 Sync Rate').if_parameter('L 3 Sync').has_value('Sync').else_use('L 3 Rate'),
                         'L 3 R < Key',
                         'L 3 Offset',
                         'L 3 St Mode',
                         use('L 3 Spin').if_parameter('L 3 St Mode').has_value('Spin').else_use('L 3 Phase'))}),
 (
  'Oscillator',
  {BANK_PARAMETERS_KEY: ('O Mode', 'O Volume', 'O Coarse', 'O Fine', 'Oe Attack', 'Oe Decay', 'Oe Sustain',
 'Oe Release')}),
 (
  'Pitch',
  {BANK_PARAMETERS_KEY: ('Transpose', 'Spread', 'Pe < Env', 'Pe Attack', 'Pe Peak', 'Pe Decay', 'Pe Sustain',
 'Pe Release')})))
BANK_DEFINITIONS['Saturator'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Drive', 'Type', 'Color', 'Base', 'Frequency', 'Width', 'Depth', 'Output')}),
 (
  'Waveshaper',
  {BANK_PARAMETERS_KEY: (
                         'Type',
                         use('WS Drive').if_parameter('Type').has_value('Waveshaper'),
                         use('WS Curve').if_parameter('Type').has_value('Waveshaper'),
                         use('WS Depth').if_parameter('Type').has_value('Waveshaper'),
                         use('WS Lin').if_parameter('Type').has_value('Waveshaper'),
                         use('WS Damp').if_parameter('Type').has_value('Waveshaper'),
                         use('WS Period').if_parameter('Type').has_value('Waveshaper'),
                         'Dry/Wet')}),
 (
  'Output',
  {BANK_PARAMETERS_KEY: ('', '', '', '', '', 'Soft Clip', 'Output', 'Dry/Wet')})))
BANK_DEFINITIONS['MidiScale'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Base', 'Transpose', 'Range', 'Lowest', 'Fold', '', '', '')}),))
BANK_DEFINITIONS['Shifter'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Mode',
                         use('Pitch Coarse').with_name('Coarse').if_parameter('Mode').has_value('Pitch').else_use('FShift Coarse').with_name('Coarse').if_parameter('Mode').has_value('Freq').else_use('RM Coarse').with_name('Coarse'),
                         use('Pitch Fine').with_name('Spread').if_parameter('Mode').has_value('Pitch').and_parameter('Wide').has_value('On').else_use('Pitch Fine').with_name('Fine').if_parameter('Mode').has_value('Pitch').else_use('Mod Fine').with_name('Spread').if_parameter('Wide').has_value('On').else_use('Mod Fine').with_name('Fine'),
                         use('Lfo Waveform').with_name('Waveform'),
                         'Lfo Sync',
                         use('Lfo S. Rate').with_name('S. Rate').if_parameter('Lfo Sync').has_value('On').else_use('Lfo Rate Hz').with_name('Rate'),
                         use('Lfo Amount St').with_name('Amount').if_parameter('Mode').has_value('Pitch').else_use('Lfo Amount Hz').with_name('Amount'),
                         'Dry/Wet')}),))
BANK_DEFINITIONS['OriginalSimpler'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Filter Freq', 'Filter Res', 'S Start', 'S Length', 'Ve Attack', 'Ve Release', 'Transpose',
 'Volume')}),
 (
  'Amplitude',
  {BANK_PARAMETERS_KEY: ('Ve Attack', 'Ve Decay', 'Ve Sustain', 'Ve Release', 'S Start', 'S Loop Length', 'S Length',
 'S Loop Fade')}),
 (
  'Filter',
  {BANK_PARAMETERS_KEY: ('Fe Attack', 'Fe Decay', 'Fe Sustain', 'Fe Release', 'Filter Freq', 'Filter Res',
 'Filt < Vel', 'Fe < Env')}),
 (
  'LFO',
  {BANK_PARAMETERS_KEY: (
                         'L Attack',
                         use('L Rate').if_parameter('L Sync').has_value('Free').else_use('L Sync Rate'),
                         'L R < Key',
                         'L Wave',
                         'Vol < LFO',
                         'Filt < LFO',
                         'Pitch < LFO',
                         'Pan < LFO')}),
 (
  'Pitch Modifiers',
  {BANK_PARAMETERS_KEY: ('Pe Attack', 'Pe Decay', 'Pe Sustain', 'Pe Release', 'Glide Time', 'Spread', 'Pan',
 'Volume')})))
BANK_DEFINITIONS['Transmute'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         use('Transpose').if_parameter('Pitch Mode').has_value('MIDI').else_use('Freq. Hz').with_name('Freq').if_parameter('Hz/Note Mode').has_value('ModulationHertz').else_use('Note').with_name('Freq'),
                         'Hz/Note Mode',
                         'Decay',
                         'Stretch',
                         'Shift',
                         'Unison',
                         use('Input Send Gain').with_name('Input Send'),
                         use('Dry Wet').with_name('Dry/Wet'))}),))
BANK_DEFINITIONS['Spectral'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: (
                         'Frozen',
                         use('Delay Time Seconds').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('Time').else_use('Delay Time Divisions').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('Notes').else_use('Delay Time Sixteenths').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('16th').else_use('Delay Time Sixteenths').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('16th Triplet').else_use('Delay Time Sixteenths').with_name('Del. Time'),
                         use('Delay Feedback').with_name('Feedback'),
                         use('Delay Frequency Shift').with_name('Shift'),
                         use('Delay Tilt').with_name('Tilt'),
                         use('Delay Spray').with_name('Spray'),
                         use('Delay Mask').with_name('Mask'),
                         use('Dry Wet').with_name('Dry/Wet'))}),))
BANK_DEFINITIONS['StringStudio'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Filter Freq', 'Filter Reso', 'Filter Type', 'Exciter Type', 'E Pos', 'String Decay',
 'Str Damping', 'Volume')}),
 (
  'Exciter and String',
  {BANK_PARAMETERS_KEY: ('Exciter Type', 'String Decay', 'Str Inharmon', 'Str Damping', 'Exc ForceMassProt',
 'Exc FricStiff', 'Exc Velocity', 'E Pos')}),
 (
  'Damper',
  {BANK_PARAMETERS_KEY: ('Damper On', 'Damper Mass', 'D Stiffness', 'D Velocity', 'Damp Pos', 'D Damping',
 'D Pos < Vel', 'D Pos Abs')}),
 (
  'Termination and Pickup',
  {BANK_PARAMETERS_KEY: ('Term On/Off', 'Term Mass', 'Term Fng Stiff', 'Term Fret Stiff', 'Pickup On/Off',
 'Pickup Pos', 'T Mass < Vel', 'T Mass < Key')}),
 (
  'Body',
  {BANK_PARAMETERS_KEY: ('Body On/Off', 'Body Type', 'Body Size', 'Body Decay', 'Body Low-Cut', 'Body High-Cut',
 'Body Mix', 'Volume')}),
 (
  'Vibrato',
  {BANK_PARAMETERS_KEY: ('Vibrato On/Off', 'Vib Delay', 'Vib Fade-In', 'Vib Speed', 'Vib Amount', 'Vib < ModWh',
 'Vib Error', 'Volume')}),
 (
  'Filter',
  {BANK_PARAMETERS_KEY: ('Filter On/Off', 'Filter Type', 'Filter Freq', 'Filter Reso', 'Freq < Env', 'Freq < LFO',
 'Reso < Env', 'Reso < LFO')}),
 (
  'Envelope and LFO',
  {BANK_PARAMETERS_KEY: (
                         'FEG On/Off',
                         'FEG Attack',
                         'FEG Decay',
                         'FEG Sustain',
                         'FEG Release',
                         'LFO On/Off',
                         'LFO Shape',
                         use('LFO SyncRate').if_parameter('LFO Sync On').has_value('Beat').else_use('LFO Speed'))}),
 (
  'Global',
  {BANK_PARAMETERS_KEY: ('Unison On/Off', 'Uni Detune', 'Porta On/Off', 'Porta Time', 'Voices', 'Octave', 'Semitone',
 'Volume')})))
BANK_DEFINITIONS['StereoGain'] = IndexedDict((
 (
  'Utility',
  {BANK_PARAMETERS_KEY: (
                         'Left Inv',
                         'Right Inv',
                         'Channel Mode',
                         use('Stereo Width').if_parameter('Stereo Width').is_available(True).else_use('Mid/Side Balance'),
                         'Mono',
                         'Balance',
                         use('Gain').if_parameter('Gain').is_available(True).else_use('Gain (Legacy)'),
                         'Mute')}),
 (
  'Low Freq',
  {BANK_PARAMETERS_KEY: (
                         use('Bass Mono').if_parameter('Bass Mono').is_available(True),
                         use('Bass Freq').if_parameter('Bass Freq').is_available(True),
                         '',
                         'DC Filter',
                         '',
                         '',
                         '',
                         '')})))
BANK_DEFINITIONS['MidiVelocity'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Mode', 'Drive', 'Compand', 'Out Hi', 'Out Low', 'Range', 'Lowest', 'Random')}),))
BANK_DEFINITIONS['Vinyl'] = IndexedDict((
 (
  'Global',
  {BANK_PARAMETERS_KEY: ('Tracing On', 'Tracing Drive', 'Tracing Freq.', 'Tracing Width', 'Pinch On', 'Global Drive',
 'Crackle Density', 'Crackle Volume')}),
 (
  'Pinch',
  {BANK_PARAMETERS_KEY: ('Pinch On', 'Pinch Soft On', 'Pinch Mono On', 'Pinch Width', 'Pinch Drive', 'Pinch Freq.',
 'Crackle Density', 'Crackle Volume')})))
BANK_DEFINITIONS['Vocoder'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Formant Shift', 'Attack Time', 'Release Time', 'Unvoiced Level', 'Gate Threshold',
 'Filter Bandwidth', 'Envelope Depth', 'Dry/Wet')}),
 (
  'Carrier',
  {BANK_PARAMETERS_KEY: ('Noise Rate', 'Noise Crackle', 'Upper Pitch Detection', 'Lower Pitch Detection', 'Oscillator Pitch',
 'Oscillator Waveform', '', '')}),
 (
  'Global',
  {BANK_PARAMETERS_KEY: ('Formant Shift', 'Attack Time', 'Release Time', 'Mono/Stereo', 'Output Level', 'Gate Threshold',
 'Envelope Depth', 'Dry/Wet')}),
 (
  'Filters/Voicing',
  {BANK_PARAMETERS_KEY: ('Filter Bandwidth', 'Upper Filter Band', 'Lower Filter Band', 'Precise/Retro', 'Unvoiced Level',
 'Unvoiced Sensitivity', 'Unvoiced Speed', 'Enhance')})))
BANK_DEFINITIONS['InstrumentVector'] = IndexedDict((
 (
  BANK_MAIN_KEY,
  {BANK_PARAMETERS_KEY: ('Osc 1 Pos', 'Osc 1 Transp', 'Osc 2 Pos', 'Osc 2 Transp', 'Filter 1 Freq', 'Filter 1 Res',
 'Global Mod Amount', 'Volume')}),
 (
  'Oscillator 1',
  {BANK_PARAMETERS_KEY: ('Osc 1 Transp', 'Osc 1 Detune', 'Osc 1 Pos', 'Osc 1 Effect 1', 'Osc 1 Effect 2', 'Osc 1 Pan',
 'Osc 1 Gain', 'Osc 1 On')}),
 (
  'Oscillator 2',
  {BANK_PARAMETERS_KEY: ('Osc 2 Transp', 'Osc 2 Detune', 'Osc 2 Pos', 'Osc 2 Effect 1', 'Osc 2 Effect 2', 'Osc 2 Pan',
 'Osc 2 Gain', 'Osc 2 On')}),
 (
  'Filter 1',
  {BANK_PARAMETERS_KEY: (
                         'Filter 1 On',
                         'Filter 1 Freq',
                         'Filter 1 Res',
                         use('Filter 1 Morph').if_parameter('Filter 1 Type').has_value('Morph').else_use('Filter 1 Drive'),
                         'Filter 1 Type',
                         'Filter 1 Slope',
                         use('Filter 1 LP/HP').if_parameter('Filter 1 Type').has_value_in(('Lowpass', 'Highpass')).else_use('Filter 1 BP/NO/Morph'),
                         '')}),
 (
  'Filter 2',
  {BANK_PARAMETERS_KEY: (
                         'Filter 2 On',
                         'Filter 2 Freq',
                         'Filter 2 Res',
                         use('Filter 2 Morph').if_parameter('Filter 2 Type').has_value('Morph').else_use('Filter 2 Drive'),
                         'Filter 2 Type',
                         'Filter 2 Slope',
                         use('Filter 2 LP/HP').if_parameter('Filter 2 Type').has_value_in(('Lowpass', 'Highpass')).else_use('Filter 2 BP/NO/Morph'),
                         '')}),
 (
  'Amp Envelope',
  {BANK_PARAMETERS_KEY: ('Amp Attack', 'Amp Decay', 'Amp Sustain', 'Amp Release', 'Amp A Slope', 'Amp D Slope',
 'Amp R Slope', 'Amp Loop Mode')}),
 (
  'Envelope 2/3',
  {BANK_PARAMETERS_KEY: ('Env 2 Attack', 'Env 2 Decay', 'Env 2 Sustain', 'Env 2 Release', 'Env 3 Attack', 'Env 3 Decay',
 'Env 3 Sustain', 'Env 3 Release')}),
 (
  'LFO 1/2',
  {BANK_PARAMETERS_KEY: (
                         'LFO 1 Amount',
                         'LFO 1 Shape',
                         use('LFO 1 S. Rate').if_parameter('LFO 1 Sync').has_value('Tempo').else_use('LFO 1 Rate'),
                         'LFO 1 Sync',
                         'LFO 2 Amount',
                         'LFO 2 Shape',
                         use('LFO 2 S. Rate').if_parameter('LFO 2 Sync').has_value('Tempo').else_use('LFO 2 Rate'),
                         'LFO 2 Sync')}),
 (
  'Global',
  {BANK_PARAMETERS_KEY: ('Time', 'Global Mod Amount', 'Unison Amount', 'Transpose', 'Glide', 'Sub Gain', 'Sub Transpose',
 'Volume')})))