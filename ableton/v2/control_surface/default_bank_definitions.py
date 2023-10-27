# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\default_bank_definitions.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 264959 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base.collection import IndexedDict
from ableton.v2.control_surface import BANK_MAIN_KEY, BANK_PARAMETERS_KEY, use
RACK_BANKS = IndexedDict((
 (
  'Macros',
  {BANK_PARAMETERS_KEY: ('Macro 1', 'Macro 2', 'Macro 3', 'Macro 4', 'Macro 5', 'Macro 6', 'Macro 7', 'Macro 8')}),
 (
  'Macros 2',
  {BANK_PARAMETERS_KEY: ('Macro 9', 'Macro 10', 'Macro 11', 'Macro 12', 'Macro 13', 'Macro 14', 'Macro 15',
 'Macro 16')})))
BANK_DEFINITIONS = {'AudioEffectGroupDevice':RACK_BANKS, 
 'MidiEffectGroupDevice':RACK_BANKS, 
 'InstrumentGroupDevice':RACK_BANKS, 
 'DrumGroupDevice':RACK_BANKS, 
 'UltraAnalog':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('OSC1 Shape').if_parameter('OSC1 On/Off').has_value('On').else_use('OSC2 Shape').if_parameter('OSC2 On/Off').has_value('On'),
                          use('OSC1 Octave').if_parameter('OSC1 On/Off').has_value('On').else_use('OSC2 Octave').if_parameter('OSC2 On/Off').has_value('On'),
                          use('OSC2 Shape').if_parameter('OSC1 On/Off').has_value('On').and_parameter('OSC2 On/Off').has_value('On').else_use('OSC1 Semi').if_parameter('OSC1 On/Off').has_value('On').else_use('OSC2 Semi').if_parameter('OSC2 On/Off').has_value('On'),
                          use('OSC2 Octave').if_parameter('OSC1 On/Off').has_value('On').and_parameter('OSC2 On/Off').has_value('On').else_use('OSC1 Detune').if_parameter('OSC1 On/Off').has_value('On').else_use('OSC2 Detune').if_parameter('OSC2 On/Off').has_value('On'),
                          use('F1 Type').if_parameter('F1 On/Off').has_value('On').else_use('F2 Type').if_parameter('F2 On/Off').has_value('On'),
                          use('F1 Freq').if_parameter('F1 On/Off').has_value('On').else_use('F2 Freq').if_parameter('F2 On/Off').has_value('On'),
                          use('F1 Resonance').if_parameter('F1 On/Off').has_value('On').else_use('F2 Resonance').if_parameter('F2 On/Off').has_value('On'),
                          'Volume')}),
  (
   'Osc. 1 Shape',
   {BANK_PARAMETERS_KEY: (
                          'OSC1 On/Off',
                          use('OSC1 Shape').if_parameter('OSC1 On/Off').has_value('On'),
                          use('').if_parameter('OSC1 On/Off').has_value('Off').else_use('OSC1 PW').if_parameter('OSC1 Shape').has_value('Rect'),
                          use('').if_parameter('OSC1 On/Off').has_value('Off').else_use('O1 PW < LFO').if_parameter('OSC1 Shape').has_value('Rect').else_use('').if_parameter('LFO1 On/Off').has_value('Off'),
                          use('').if_parameter('OSC1 On/Off').has_value('Off').else_use('').if_parameter('OSC1 Shape').has_value('Noise').else_use('').if_parameter('OSC1 Shape').has_value('Sine').else_use('OSC1 Mode'),
                          use('').if_parameter('OSC1 On/Off').has_value('Off').else_use('').if_parameter('OSC1 Shape').has_value('Noise').else_use('O1 Sub/Sync'),
                          use('OSC1 Balance').if_parameter('OSC1 On/Off').has_value('On'),
                          use('OSC1 Level').if_parameter('OSC1 On/Off').has_value('On'))}),
  (
   'Osc. 1 Pitch',
   {BANK_PARAMETERS_KEY: (
                          'OSC1 On/Off',
                          use('OSC1 Octave').if_parameter('OSC1 On/Off').has_value('On'),
                          use('OSC1 Semi').if_parameter('OSC1 On/Off').has_value('On'),
                          use('OSC1 Detune').if_parameter('OSC1 On/Off').has_value('On'),
                          use('PEG1 Amount').if_parameter('OSC1 On/Off').has_value('On'),
                          use('PEG1 Time').if_parameter('OSC1 On/Off').has_value('On'),
                          use('O1 Keytrack').if_parameter('OSC1 On/Off').has_value('On'),
                          use('').if_parameter('OSC1 On/Off').has_value('Off').else_use('').if_parameter('LFO1 On/Off').has_value('Off').else_use('OSC1 < LFO'))}),
  (
   'Osc. 2 Shape',
   {BANK_PARAMETERS_KEY: (
                          'OSC2 On/Off',
                          use('OSC2 Shape').if_parameter('OSC2 On/Off').has_value('On'),
                          use('').if_parameter('OSC2 On/Off').has_value('Off').else_use('OSC2 PW').if_parameter('OSC2 Shape').has_value('Rect'),
                          use('').if_parameter('OSC2 On/Off').has_value('Off').else_use('O2 PW < LFO').if_parameter('OSC2 Shape').has_value('Rect').else_use('').if_parameter('LFO2 On/Off').has_value('Off'),
                          use('').if_parameter('OSC2 On/Off').has_value('Off').else_use('').if_parameter('OSC2 Shape').has_value('Noise').else_use('').if_parameter('OSC2 Shape').has_value('Sine').else_use('OSC2 Mode'),
                          use('').if_parameter('OSC2 On/Off').has_value('Off').else_use('').if_parameter('OSC2 Shape').has_value('Noise').else_use('O2 Sub/Sync'),
                          use('OSC2 Balance').if_parameter('OSC2 On/Off').has_value('On'),
                          use('OSC2 Level').if_parameter('OSC2 On/Off').has_value('On'))}),
  (
   'Osc. 2 Pitch',
   {BANK_PARAMETERS_KEY: (
                          'OSC2 On/Off',
                          use('OSC2 Octave').if_parameter('OSC2 On/Off').has_value('On'),
                          use('OSC2 Semi').if_parameter('OSC2 On/Off').has_value('On'),
                          use('OSC2 Detune').if_parameter('OSC2 On/Off').has_value('On'),
                          use('PEG2 Amount').if_parameter('OSC2 On/Off').has_value('On'),
                          use('PEG2 Time').if_parameter('OSC2 On/Off').has_value('On'),
                          use('O2 Keytrack').if_parameter('OSC2 On/Off').has_value('On'),
                          use('').if_parameter('OSC2 On/Off').has_value('Off').else_use('').if_parameter('LFO2 On/Off').has_value('Off').else_use('OSC2 < LFO'))}),
  (
   'Filters',
   {BANK_PARAMETERS_KEY: (
                          'F1 On/Off',
                          use('F1 Type').if_parameter('F1 On/Off').has_value('On'),
                          use('F1 Freq').if_parameter('F1 On/Off').has_value('On'),
                          use('F1 Resonance').if_parameter('F1 On/Off').has_value('On'),
                          'F2 On/Off',
                          use('F2 Type').if_parameter('F2 On/Off').has_value('On'),
                          use('F2 Freq').if_parameter('F2 On/Off').has_value('On'),
                          use('F2 Resonance').if_parameter('F2 On/Off').has_value('On'))}),
  (
   'Filt. 1 Env.',
   {BANK_PARAMETERS_KEY: (
                          'F1 On/Off',
                          use('FEG1 < Vel').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 A < Vel').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Attack').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Decay').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Sustain').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 S Time').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Rel').if_parameter('F1 On/Off').has_value('On'))}),
  (
   'Filt. 2 Env.',
   {BANK_PARAMETERS_KEY: (
                          'F2 On/Off',
                          use('FEG2 < Vel').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 A < Vel').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Attack').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Decay').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Sustain').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 S Time').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Rel').if_parameter('F2 On/Off').has_value('On'))}),
  (
   'Filt. Modulation',
   {BANK_PARAMETERS_KEY: (
                          'F1 On/Off',
                          use('F1 Freq < LFO').if_parameter('F1 On/Off').has_value('On'),
                          use('F1 Freq < Env').if_parameter('F1 On/Off').has_value('On'),
                          use('F1 Res < LFO').if_parameter('F1 On/Off').has_value('On'),
                          'F2 On/Off',
                          use('F2 Freq < LFO').if_parameter('F2 On/Off').has_value('On'),
                          use('F2 Freq < Env').if_parameter('F2 On/Off').has_value('On'),
                          use('F2 Res < LFO').if_parameter('F2 On/Off').has_value('On'))}),
  (
   'Amp',
   {BANK_PARAMETERS_KEY: (
                          use('AMP1 Level').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AMP1 Pan').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AMP1 < LFO').if_parameter('AMP1 On/Off').has_value('On'),
                          use('').if_parameter('LFO1 On/Off').has_value('Off').else_use('LFO1 Speed').if_parameter('LFO1 Sync').has_value('Hertz').else_use('LFO1 SncRate'),
                          use('AMP2 Level').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AMP2 Pan').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AMP2 < LFO').if_parameter('AMP2 On/Off').has_value('On'),
                          use('').if_parameter('LFO2 On/Off').has_value('Off').else_use('LFO2 Speed').if_parameter('LFO2 Sync').has_value('Hertz').else_use('LFO2 SncRate'))}),
  (
   'Amp 1 Envelope',
   {BANK_PARAMETERS_KEY: (
                          'AMP1 On/Off',
                          use('AEG1 < Vel').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 A < Vel').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Attack').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Decay').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Sustain').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 S Time').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Rel').if_parameter('AMP1 On/Off').has_value('On'))}),
  (
   'Amp 2 Envelope',
   {BANK_PARAMETERS_KEY: (
                          'AMP2 On/Off',
                          use('AEG2 < Vel').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 A < Vel').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Attack').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Decay').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Sustain').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 S Time').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Rel').if_parameter('AMP2 On/Off').has_value('On'))}),
  (
   'Noise & Unison',
   {BANK_PARAMETERS_KEY: (
                          'Noise On/Off',
                          use('Noise Level').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Color').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Balance').if_parameter('Noise On/Off').has_value('On'),
                          'Unison On/Off',
                          use('Unison Detune').if_parameter('Unison On/Off').has_value('On'),
                          use('Unison Delay').if_parameter('Unison On/Off').has_value('On'),
                          '')}),
  (
   'Performance',
   {BANK_PARAMETERS_KEY: (
                          'Glide On/Off',
                          use('Glide Time').if_parameter('Glide On/Off').has_value('On'),
                          use('Glide Mode').if_parameter('Glide On/Off').has_value('On'),
                          use('Glide Legato').if_parameter('Glide On/Off').has_value('On'),
                          'PB Range',
                          'Key Stretch',
                          'Key Error',
                          'Voices')}),
  (
   'LFO 1',
   {BANK_PARAMETERS_KEY: (
                          'LFO1 On/Off',
                          use('LFO1 Sync').if_parameter('LFO1 On/Off').has_value('On'),
                          use('').if_parameter('LFO1 On/Off').has_value('Off').else_use('LFO1 Speed').if_parameter('LFO1 Sync').has_value('Hertz').else_use('LFO1 SncRate'),
                          use('LFO1 Shape').if_parameter('LFO1 On/Off').has_value('On'),
                          use('').if_parameter('LFO1 On/Off').has_value('Off').else_use('LFO1 PW').if_parameter('LFO1 Shape').has_value('Rect').else_use('LFO1 PW').if_parameter('LFO1 Shape').has_value('Tri'),
                          use('LFO1 Phase').if_parameter('LFO1 On/Off').has_value('On'),
                          use('LFO1 Delay').if_parameter('LFO1 On/Off').has_value('On'),
                          use('LFO1 Fade In').if_parameter('LFO1 On/Off').has_value('On'))}),
  (
   'LFO 2',
   {BANK_PARAMETERS_KEY: (
                          'LFO2 On/Off',
                          use('LFO2 Sync').if_parameter('LFO2 On/Off').has_value('On'),
                          use('').if_parameter('LFO2 On/Off').has_value('Off').else_use('LFO2 Speed').if_parameter('LFO2 Sync').has_value('Hertz').else_use('LFO2 SncRate'),
                          use('LFO2 Shape').if_parameter('LFO2 On/Off').has_value('On'),
                          use('').if_parameter('LFO2 On/Off').has_value('Off').else_use('LFO2 PW').if_parameter('LFO2 Shape').has_value('Rect').else_use('LFO2 PW').if_parameter('LFO2 Shape').has_value('Tri'),
                          use('LFO2 Phase').if_parameter('LFO2 On/Off').has_value('On'),
                          use('LFO2 Delay').if_parameter('LFO2 On/Off').has_value('On'),
                          use('LFO2 Fade In').if_parameter('LFO2 On/Off').has_value('On'))}),
  (
   'Vibrato',
   {BANK_PARAMETERS_KEY: (
                          'Vib On/Off',
                          use('Vib Amount').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib Speed').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib Delay').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib Fade-In').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib Error').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib < ModWh').if_parameter('Vib On/Off').has_value('On'),
                          '')}))), 
 'ChannelEq':IndexedDict((
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
                          '')}),)), 
 'Collision':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('Res 1 Type').if_parameter('Res 1 On/Off').has_value('On'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Brightness'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Opening').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Inharmonics'),
                          use('Res 1 Decay').if_parameter('Res 1 On/Off').has_value('On'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('Res 1 Radius').if_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Radius').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Material'),
                          use('Mallet Stiffness').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Amount').if_parameter('Mallet On/Off').has_value('On'),
                          'Volume')}),
  (
   'Mix',
   {BANK_PARAMETERS_KEY: (
                          use('Res 1 Volume').if_parameter('Res 1 On/Off').has_value('On'),
                          use('Panorama').if_parameter('Res 1 On/Off').has_value('On'),
                          use('Res 1 Bleed').if_parameter('Res 1 On/Off').has_value('On'),
                          use('Res 2 Volume').if_parameter('Res 2 On/Off').has_value('On'),
                          use('Res 2 Panorama').if_parameter('Res 2 On/Off').has_value('On'),
                          use('Res 2 Bleed').if_parameter('Res 2 On/Off').has_value('On'),
                          'Structure',
                          'Volume')}),
  (
   'Mallet',
   {BANK_PARAMETERS_KEY: (
                          'Mallet On/Off',
                          use('Mallet Volume').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Amount').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Stiffness').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Color').if_parameter('Mallet On/Off').has_value('On'),
                          '',
                          use('Mallet Volume < Vel').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Amount < Vel').if_parameter('Mallet On/Off').has_value('On'))}),
  (
   'Noise Envelope',
   {BANK_PARAMETERS_KEY: (
                          'Noise On/Off',
                          use('Noise Volume').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Volume < Key').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Volume < Vel').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Attack').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Sustain').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Decay').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Release').if_parameter('Noise On/Off').has_value('On'))}),
  (
   'Noise Filter',
   {BANK_PARAMETERS_KEY: (
                          'Noise On/Off',
                          use('Noise Volume').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Filter Type').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Filter Freq').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Filter Q').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Freq < Key').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Freq < Vel').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Freq < Env').if_parameter('Noise On/Off').has_value('On'))}),
  (
   'Res. 1 Body',
   {BANK_PARAMETERS_KEY: (
                          'Res 1 On/Off',
                          use('Res 1 Type').if_parameter('Res 1 On/Off').has_value('On'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('Res 1 Ratio').if_parameter('Res 1 Type').has_value('Plate').else_use('Res 1 Ratio').if_parameter('Res 1 Type').has_value('Membrane'),
                          use('Res 1 Decay').if_parameter('Res 1 On/Off').has_value('On'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('Res 1 Radius').if_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Radius').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Material'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Listening L'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Listening R'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Hit'))}),
  (
   'Res. 1 Tune',
   {BANK_PARAMETERS_KEY: (
                          'Res 1 On/Off',
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Brightness'),
                          use('Res 1 Quality').if_parameter('Res 1 On/Off').has_value('On'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Opening').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Inharmonics'),
                          use('Res 1 Tune').if_parameter('Res 1 On/Off').has_value('On'),
                          use('Res 1 Fine Tune').if_parameter('Res 1 On/Off').has_value('On'),
                          use('Res 1 Pitch Env.').if_parameter('Res 1 On/Off').has_value('On'),
                          use('Res 1 Pitch Env. Time').if_parameter('Res 1 On/Off').has_value('On'))}),
  (
   'Res. 2 Body',
   {BANK_PARAMETERS_KEY: (
                          'Res 2 On/Off',
                          use('Res 2 Type').if_parameter('Res 2 On/Off').has_value('On'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('Res 2 Ratio').if_parameter('Res 2 Type').has_value('Plate').else_use('Res 2 Ratio').if_parameter('Res 2 Type').has_value('Membrane'),
                          use('Res 2 Decay').if_parameter('Res 2 On/Off').has_value('On'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('Res 2 Radius').if_parameter('Res 2 Type').has_value('Tube').else_use('Res 2 Radius').if_parameter('Res 2 Type').has_value('Pipe').else_use('Res 2 Material'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('').if_parameter('Res 2 Type').has_value('Tube').else_use('').if_parameter('Res 2 Type').has_value('Pipe').else_use('Res 2 Listening L'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('').if_parameter('Res 2 Type').has_value('Tube').else_use('').if_parameter('Res 2 Type').has_value('Pipe').else_use('Res 2 Listening R'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('').if_parameter('Res 2 Type').has_value('Tube').else_use('').if_parameter('Res 2 Type').has_value('Pipe').else_use('Res 2 Hit'))}),
  (
   'Res. 2 Tune',
   {BANK_PARAMETERS_KEY: (
                          'Res 2 On/Off',
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('').if_parameter('Res 2 Type').has_value('Tube').else_use('').if_parameter('Res 2 Type').has_value('Pipe').else_use('Res 2 Brightness'),
                          use('Res 2 Quality').if_parameter('Res 2 On/Off').has_value('On'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('').if_parameter('Res 2 Type').has_value('Tube').else_use('Res 2 Opening').if_parameter('Res 2 Type').has_value('Pipe').else_use('Res 2 Inharmonics'),
                          use('Res 2 Tune').if_parameter('Res 2 On/Off').has_value('On'),
                          use('Res 2 Fine Tune').if_parameter('Res 2 On/Off').has_value('On'),
                          use('Res 2 Pitch Env.').if_parameter('Res 2 On/Off').has_value('On'),
                          use('Res 2 Pitch Env. Time').if_parameter('Res 2 On/Off').has_value('On'))}),
  (
   'LFO 1',
   {BANK_PARAMETERS_KEY: (
                          'LFO 1 On/Off',
                          use('LFO 1 Depth').if_parameter('LFO 1 On/Off').has_value('On'),
                          use('LFO 1 Shape').if_parameter('LFO 1 On/Off').has_value('On'),
                          use('LFO 1 Sync').if_parameter('LFO 1 On/Off').has_value('On'),
                          use('').if_parameter('LFO 1 On/Off').has_value('Off').else_use('LFO 1 Sync Rate').if_parameter('LFO 1 Sync').has_value('Sync').else_use('LFO 1 Rate'),
                          use('LFO 1 Offset').if_parameter('LFO 1 On/Off').has_value('On'),
                          use('LFO 1 Destination A').if_parameter('LFO 1 On/Off').has_value('On'),
                          use('LFO 1 Destination A Amount').if_parameter('LFO 1 On/Off').has_value('On'))}),
  (
   'LFO 2',
   {BANK_PARAMETERS_KEY: (
                          'LFO 2 On/Off',
                          use('LFO 2 Depth').if_parameter('LFO 2 On/Off').has_value('On'),
                          use('LFO 2 Shape').if_parameter('LFO 2 On/Off').has_value('On'),
                          use('LFO 2 Sync').if_parameter('LFO 2 On/Off').has_value('On'),
                          use('').if_parameter('LFO 2 On/Off').has_value('Off').else_use('LFO 2 Sync Rate').if_parameter('LFO 2 Sync').has_value('Sync').else_use('LFO 2 Rate'),
                          use('LFO 2 Offset').if_parameter('LFO 2 On/Off').has_value('On'),
                          use('LFO 2 Destination A').if_parameter('LFO 2 On/Off').has_value('On'),
                          use('LFO 2 Destination A Amount').if_parameter('LFO 2 On/Off').has_value('On'))}),
  (
   'Mallet Mod.',
   {BANK_PARAMETERS_KEY: (
                          'Mallet On/Off',
                          use('Mallet Volume < Key').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Volume < Vel').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Amount < Key').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Amount < Vel').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Stiffness < Key').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Stiffness < Vel').if_parameter('Mallet On/Off').has_value('On'),
                          '')}))), 
 'Drift':IndexedDict((
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
                          'Volume')}))), 
 'LoungeLizard':IndexedDict((
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
   {BANK_PARAMETERS_KEY: ('KB Stretch', 'PB Range', 'Note PB Range', '', 'Voices', 'Semitone', 'Detune', 'Volume')}))), 
 'InstrumentImpulse':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('1 Transpose', '1 Volume', '3 Transpose', '3 Volume', '7 Transpose', '7 Volume', '8 Transpose',
 '8 Volume')}),
  (
   'Pad 1',
   {BANK_PARAMETERS_KEY: ('1 Start', '1 Envelope Decay', '1 Stretch Factor', '1 Saturator Drive', '1 Envelope Type',
 '1 Transpose', '1 Volume <- Vel', '1 Volume')}),
  (
   '1 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('1 Filter Freq', '1 Filter Res', '1 Filter Type', '1 Filter <- Vel', '1 Filter <- Random',
 '1 Pan', '1 Pan <- Vel', '1 Pan <- Random')}),
  (
   'Pad 2',
   {BANK_PARAMETERS_KEY: ('2 Start', '2 Envelope Decay', '2 Stretch Factor', '2 Saturator Drive', '2 Envelope Type',
 '2 Transpose', '2 Volume <- Vel', '2 Volume')}),
  (
   '2 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('2 Filter Freq', '2 Filter Res', '2 Filter Type', '2 Filter <- Vel', '2 Filter <- Random',
 '2 Pan', '2 Pan <- Vel', '2 Pan <- Random')}),
  (
   'Pad 3',
   {BANK_PARAMETERS_KEY: ('3 Start', '3 Envelope Decay', '3 Stretch Factor', '3 Saturator Drive', '3 Envelope Type',
 '3 Transpose', '3 Volume <- Vel', '3 Volume')}),
  (
   '3 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('3 Filter Freq', '3 Filter Res', '3 Filter Type', '3 Filter <- Vel', '3 Filter <- Random',
 '3 Pan', '3 Pan <- Vel', '3 Pan <- Random')}),
  (
   'Pad 4',
   {BANK_PARAMETERS_KEY: ('4 Start', '4 Envelope Decay', '4 Stretch Factor', '4 Saturator Drive', '4 Envelope Type',
 '4 Transpose', '4 Volume <- Vel', '4 Volume')}),
  (
   '4 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('4 Filter Freq', '4 Filter Res', '4 Filter Type', '4 Filter <- Vel', '4 Filter <- Random',
 '4 Pan', '4 Pan <- Vel', '4 Pan <- Random')}),
  (
   'Pad 5',
   {BANK_PARAMETERS_KEY: ('5 Start', '5 Envelope Decay', '5 Stretch Factor', '5 Saturator Drive', '5 Envelope Type',
 '5 Transpose', '5 Volume <- Vel', '5 Volume')}),
  (
   '5 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('5 Filter Freq', '5 Filter Res', '5 Filter Type', '5 Filter <- Vel', '5 Filter <- Random',
 '5 Pan', '5 Pan <- Vel', '5 Pan <- Random')}),
  (
   'Pad 6',
   {BANK_PARAMETERS_KEY: ('6 Start', '6 Envelope Decay', '6 Stretch Factor', '6 Saturator Drive', '6 Envelope Type',
 '6 Transpose', '6 Volume <- Vel', '6 Volume')}),
  (
   '6 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('6 Filter Freq', '6 Filter Res', '6 Filter Type', '6 Filter <- Vel', '6 Filter <- Random',
 '6 Pan', '6 Pan <- Vel', '6 Pan <- Random')}),
  (
   'Pad 7',
   {BANK_PARAMETERS_KEY: ('7 Start', '7 Envelope Decay', '7 Stretch Factor', '7 Saturator Drive', '7 Envelope Type',
 '7 Transpose', '7 Volume <- Vel', '7 Volume')}),
  (
   '7 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('7 Filter Freq', '7 Filter Res', '7 Filter Type', '7 Filter <- Vel', '7 Filter <- Random',
 '7 Pan', '7 Pan <- Vel', '7 Pan <- Random')}),
  (
   'Pad 8',
   {BANK_PARAMETERS_KEY: ('8 Start', '8 Envelope Decay', '8 Stretch Factor', '8 Saturator Drive', '8 Envelope Type',
 '8 Transpose', '8 Volume <- Vel', '8 Volume')}),
  (
   '8 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('8 Filter Freq', '8 Filter Res', '8 Filter Type', '8 Filter <- Vel', '8 Filter <- Random',
 '8 Pan', '8 Pan <- Vel', '8 Pan <- Random')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Global Time', 'Global Transpose', 'Global Volume', '', '', '', '', '')}))), 
 'Operator':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('Algorithm').if_parameter('Filter On').has_value('Off').else_use('Filter Freq'),
                          use('Filter Res (Legacy)').if_parameter('Filter Res').is_available(False).and_parameter('Filter On').has_value('On').else_use('Filter Res').if_parameter('Filter On').has_value('On').else_use('Tone'),
                          use('').if_parameter('Osc-A On').has_value('Off').else_use('A Coarse').if_parameter('A Fix On ').has_value('Off').else_use('A Fix Freq'),
                          use('').if_parameter('Osc-A On').has_value('Off').else_use('A Fine').if_parameter('A Fix On ').has_value('Off').else_use('A Fix Freq Mul'),
                          use('').if_parameter('Osc-B On').has_value('Off').else_use('B Coarse').if_parameter('B Fix On ').has_value('Off').else_use('B Fix Freq'),
                          use('').if_parameter('Osc-B On').has_value('Off').else_use('B Fine').if_parameter('B Fix On ').has_value('Off').else_use('B Fix Freq Mul'),
                          use('Osc-B Level').if_parameter('Osc-B On').has_value('On'),
                          'Volume')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Time', 'Time < Key', 'Tone', 'Algorithm', 'Panorama', 'Pan < Key', 'Pan < Rnd', 'Volume')}),
  (
   'Osc. A',
   {BANK_PARAMETERS_KEY: (
                          'Osc-A On',
                          use('Osc-A Level').if_parameter('Osc-A On').has_value('On'),
                          use('A Fix On ').if_parameter('Osc-A On').has_value('On'),
                          use('').if_parameter('Osc-A On').has_value('Off').else_use('A Coarse').if_parameter('A Fix On ').has_value('Off').else_use('A Fix Freq'),
                          use('').if_parameter('Osc-A On').has_value('Off').else_use('A Fine').if_parameter('A Fix On ').has_value('Off').else_use('A Fix Freq Mul'),
                          use('Osc-A Wave').if_parameter('Osc-A On').has_value('On'),
                          use('Osc-A Retrig').if_parameter('Osc-A On').has_value('On'),
                          use('').if_parameter('Osc-A On').has_value('Off').else_use('Osc-A Phase').if_parameter('Osc-A Retrig').has_value('On'))}),
  (
   'Osc. A Env.',
   {BANK_PARAMETERS_KEY: (
                          'Osc-A On',
                          use('Ae Init').if_parameter('Osc-A On').has_value('On'),
                          use('Ae Attack').if_parameter('Osc-A On').has_value('On'),
                          use('Ae Peak').if_parameter('Osc-A On').has_value('On'),
                          use('Ae Decay').if_parameter('Osc-A On').has_value('On'),
                          use('Ae Sustain').if_parameter('Osc-A On').has_value('On'),
                          use('Ae Release').if_parameter('Osc-A On').has_value('On'),
                          use('Osc-A Lev < Vel').if_parameter('Osc-A On').has_value('On'))}),
  (
   'Osc. B',
   {BANK_PARAMETERS_KEY: (
                          'Osc-B On',
                          use('Osc-B Level').if_parameter('Osc-B On').has_value('On'),
                          use('B Fix On ').if_parameter('Osc-B On').has_value('On'),
                          use('').if_parameter('Osc-B On').has_value('Off').else_use('B Coarse').if_parameter('B Fix On ').has_value('Off').else_use('B Fix Freq'),
                          use('').if_parameter('Osc-B On').has_value('Off').else_use('B Fine').if_parameter('B Fix On ').has_value('Off').else_use('B Fix Freq Mul'),
                          use('Osc-B Wave').if_parameter('Osc-B On').has_value('On'),
                          use('Osc-B Retrig').if_parameter('Osc-B On').has_value('On'),
                          use('').if_parameter('Osc-B On').has_value('Off').else_use('Osc-B Phase').if_parameter('Osc-B Retrig').has_value('On'))}),
  (
   'Osc. B Env.',
   {BANK_PARAMETERS_KEY: (
                          'Osc-B On',
                          use('Be Init').if_parameter('Osc-B On').has_value('On'),
                          use('Be Attack').if_parameter('Osc-B On').has_value('On'),
                          use('Be Peak').if_parameter('Osc-B On').has_value('On'),
                          use('Be Decay').if_parameter('Osc-B On').has_value('On'),
                          use('Be Sustain').if_parameter('Osc-B On').has_value('On'),
                          use('Be Release').if_parameter('Osc-B On').has_value('On'),
                          use('Osc-B Lev < Vel').if_parameter('Osc-B On').has_value('On'))}),
  (
   'Osc. C',
   {BANK_PARAMETERS_KEY: (
                          'Osc-C On',
                          use('Osc-C Level').if_parameter('Osc-C On').has_value('On'),
                          use('C Fix On ').if_parameter('Osc-C On').has_value('On'),
                          use('').if_parameter('Osc-C On').has_value('Off').else_use('C Coarse').if_parameter('C Fix On ').has_value('Off').else_use('C Fix Freq'),
                          use('').if_parameter('Osc-C On').has_value('Off').else_use('C Fine').if_parameter('C Fix On ').has_value('Off').else_use('C Fix Freq Mul'),
                          use('Osc-C Wave').if_parameter('Osc-C On').has_value('On'),
                          use('Osc-C Retrig').if_parameter('Osc-C On').has_value('On'),
                          use('').if_parameter('Osc-C On').has_value('Off').else_use('Osc-C Phase').if_parameter('Osc-C Retrig').has_value('On'))}),
  (
   'Osc. C Env.',
   {BANK_PARAMETERS_KEY: (
                          'Osc-C On',
                          use('Ce Init').if_parameter('Osc-C On').has_value('On'),
                          use('Ce Attack').if_parameter('Osc-C On').has_value('On'),
                          use('Ce Peak').if_parameter('Osc-C On').has_value('On'),
                          use('Ce Decay').if_parameter('Osc-C On').has_value('On'),
                          use('Ce Sustain').if_parameter('Osc-C On').has_value('On'),
                          use('Ce Release').if_parameter('Osc-C On').has_value('On'),
                          use('Osc-C Lev < Vel').if_parameter('Osc-C On').has_value('On'))}),
  (
   'Osc. D',
   {BANK_PARAMETERS_KEY: (
                          'Osc-D On',
                          use('Osc-D Level').if_parameter('Osc-D On').has_value('On'),
                          use('D Fix On ').if_parameter('Osc-D On').has_value('On'),
                          use('').if_parameter('Osc-D On').has_value('Off').else_use('D Coarse').if_parameter('D Fix On ').has_value('Off').else_use('D Fix Freq'),
                          use('').if_parameter('Osc-D On').has_value('Off').else_use('D Fine').if_parameter('D Fix On ').has_value('Off').else_use('D Fix Freq Mul'),
                          use('Osc-D Wave').if_parameter('Osc-D On').has_value('On'),
                          use('Osc-D Retrig').if_parameter('Osc-D On').has_value('On'),
                          use('').if_parameter('Osc-D On').has_value('Off').else_use('Osc-D Phase').if_parameter('Osc-D Retrig').has_value('On'))}),
  (
   'Osc. D Env.',
   {BANK_PARAMETERS_KEY: (
                          'Osc-D On',
                          use('De Init').if_parameter('Osc-D On').has_value('On'),
                          use('De Attack').if_parameter('Osc-D On').has_value('On'),
                          use('De Peak').if_parameter('Osc-D On').has_value('On'),
                          use('De Decay').if_parameter('Osc-D On').has_value('On'),
                          use('De Sustain').if_parameter('Osc-D On').has_value('On'),
                          use('De Release').if_parameter('Osc-D On').has_value('On'),
                          use('Osc-D Lev < Vel').if_parameter('Osc-D On').has_value('On'))}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: (
                          'Filter On',
                          use('').if_parameter('Filter On').has_value('Off').else_use('Filter Type').if_parameter('Filter Type').is_available(True).else_use('Filter Type (Legacy)'),
                          use('Filter Freq').if_parameter('Filter On').has_value('On'),
                          use('').if_parameter('Filter On').has_value('Off').else_use('Filter Res').if_parameter('Filter Res').is_available(True).else_use('Filter Res (Legacy)'),
                          use('').if_parameter('Filter On').has_value('Off').else_use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Lowpass').else_use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Highpass').else_use('Filter Circuit - BP/NO/Morph'),
                          use('').if_parameter('Filter On').has_value('Off').else_use('Filter Morph').if_parameter('Filter Type').has_value('Morph').else_use('').if_parameter('Filter Type').has_value('Lowpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Highpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Bandpass').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Notch').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('Filter Drive'),
                          use('Filter Slope').if_parameter('Filter On').has_value('On').and_parameter('Filter Slope').is_available(True),
                          use('Filt < Vel').if_parameter('Filter On').has_value('On'))}),
  (
   'Filt. Env.',
   {BANK_PARAMETERS_KEY: (
                          use('Fe Amount').if_parameter('Filter On').has_value('On'),
                          use('Fe Init').if_parameter('Filter On').has_value('On'),
                          use('Fe Attack').if_parameter('Filter On').has_value('On'),
                          use('Fe Peak').if_parameter('Filter On').has_value('On'),
                          use('Fe Decay').if_parameter('Filter On').has_value('On'),
                          use('Fe Sustain').if_parameter('Filter On').has_value('On'),
                          use('Fe Release').if_parameter('Filter On').has_value('On'),
                          use('Fe End').if_parameter('Filter On').has_value('On'))}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          'LFO On',
                          use('LFO Type').if_parameter('LFO On').has_value('On'),
                          use('LFO Range').if_parameter('LFO On').has_value('On'),
                          use('').if_parameter('LFO On').has_value('Off').else_use('LFO Sync').if_parameter('LFO Range').has_value('Sync').else_use('LFO Rate'),
                          use('LFO Retrigger').if_parameter('LFO On').has_value('On'),
                          use('LFO Amt').if_parameter('LFO On').has_value('On'),
                          '',
                          '')}),
  (
   'LFO Env.',
   {BANK_PARAMETERS_KEY: (
                          'LFO On',
                          use('Le Init').if_parameter('LFO On').has_value('On'),
                          use('Le Attack').if_parameter('LFO On').has_value('On'),
                          use('Le Peak').if_parameter('LFO On').has_value('On'),
                          use('Le Decay').if_parameter('LFO On').has_value('On'),
                          use('Le Sustain').if_parameter('LFO On').has_value('On'),
                          use('Le Release').if_parameter('LFO On').has_value('On'),
                          use('Le End').if_parameter('LFO On').has_value('On'))}),
  (
   'Pitch',
   {BANK_PARAMETERS_KEY: (
                          'Transpose',
                          'Spread',
                          'Glide On',
                          use('Glide Time').if_parameter('Glide On').has_value('On'),
                          'Pe On',
                          use('Pe Amount').if_parameter('Pe On').has_value('On'),
                          use('LFO < Pe').if_parameter('Pe On').has_value('On'),
                          use('Pe Dst B').if_parameter('Pe On').has_value('On'))}),
  (
   'Pitch Env.',
   {BANK_PARAMETERS_KEY: (
                          'Pe On',
                          use('Pe Attack').if_parameter('Pe On').has_value('On'),
                          use('Pe Peak').if_parameter('Pe On').has_value('On'),
                          use('Pe Decay').if_parameter('Pe On').has_value('On'),
                          use('Pe Sustain').if_parameter('Pe On').has_value('On'),
                          use('Pe Release').if_parameter('Pe On').has_value('On'),
                          use('Pe End').if_parameter('Pe On').has_value('On'),
                          use('Pe R < Vel').if_parameter('Pe On').has_value('On'))}))), 
 'MultiSampler':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Ve Attack',
                          'Ve Decay',
                          'Ve Sustain',
                          'Ve Release',
                          use('Pan').if_parameter('F On').has_value('Off').else_use('Filter Type').if_parameter('Filter Type').is_available(True).else_use('Filter Type (Legacy)'),
                          use('Transpose').if_parameter('F On').has_value('Off').else_use('Filter Freq'),
                          use('Detune').if_parameter('F On').has_value('Off').else_use('Filter Res').if_parameter('Filter Res').is_available(True).else_use('Filter Res (Legacy)'),
                          'Volume')}),
  (
   'Volume Env.',
   {BANK_PARAMETERS_KEY: ('Ve Init', 'Ve Attack', 'Ve Peak', 'Ve Decay', 'Ve Sustain', 'Ve Release', 'Vol < Vel',
 'Volume')}),
  (
   'Env. Loop & Pan',
   {BANK_PARAMETERS_KEY: (
                          'Ve Mode',
                          use('Ve Loop').if_parameter('Ve Mode').has_value('Loop').else_use('Ve Retrig').if_parameter('Ve Mode').has_value('Beat').else_use('Ve Retrig').if_parameter('Ve Mode').has_value('Sync').else_use(''),
                          'Ve R < Vel',
                          '',
                          'Pan',
                          'Pan < Rnd',
                          'Time',
                          'Time < Key')}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: (
                          'F On',
                          use('').if_parameter('F On').has_value('Off').else_use('Filter Type').if_parameter('Filter Type').is_available(True).else_use('Filter Type (Legacy)'),
                          use('').if_parameter('F On').has_value('Off').else_use('Filter Freq'),
                          use('').if_parameter('F On').has_value('Off').else_use('Filter Res').if_parameter('Filter Res').is_available(True).else_use('Filter Res (Legacy)'),
                          use('').if_parameter('F On').has_value('Off').else_use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Lowpass').else_use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Highpass').else_use('Filter Circuit - BP/NO/Morph'),
                          use('').if_parameter('F On').has_value('Off').else_use('Filter Morph').if_parameter('Filter Type').has_value('Morph').else_use('').if_parameter('Filter Type').has_value('Lowpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Highpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Bandpass').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Notch').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('Filter Drive'),
                          use('Filter Slope').if_parameter('F On').has_value('On').and_parameter('Filter Slope').is_available(True),
                          use('Filt < Vel').if_parameter('F On').has_value('On'))}),
  (
   'Filt. Env',
   {BANK_PARAMETERS_KEY: (
                          'Fe On',
                          use('Fe < Env').if_parameter('Fe On').has_value('On'),
                          use('Fe Init').if_parameter('Fe On').has_value('On'),
                          use('Fe Attack').if_parameter('Fe On').has_value('On'),
                          use('Fe Decay').if_parameter('Fe On').has_value('On'),
                          use('Fe Peak').if_parameter('Fe On').has_value('On'),
                          use('Fe Sustain').if_parameter('Fe On').has_value('On'),
                          use('Fe Release').if_parameter('Fe On').has_value('On'))}),
  (
   'Shaper',
   {BANK_PARAMETERS_KEY: (
                          'Fe On',
                          use('Fe End').if_parameter('Fe On').has_value('On'),
                          use('Fe Mode').if_parameter('Fe On').has_value('On'),
                          use('').if_parameter('Fe On').has_value('Off').else_use('Fe Loop').if_parameter('Fe Mode').has_value('Loop').else_use('Fe Retrig').if_parameter('Fe Mode').has_value('Beat').else_use('Fe Retrig').if_parameter('Fe Mode').has_value('Sync').else_use(''),
                          use('Fe R < Vel').if_parameter('Fe On').has_value('On'),
                          'Shaper On',
                          use('Shaper Type').if_parameter('Shaper On').has_value('On'),
                          use('Shaper Amt').if_parameter('Shaper On').has_value('On'))}),
  (
   'Osc. pg. 1',
   {BANK_PARAMETERS_KEY: (
                          'Osc On',
                          use('O Mode').if_parameter('Osc On').has_value('On'),
                          use('Oe Init').if_parameter('Osc On').has_value('On'),
                          use('Oe Attack').if_parameter('Osc On').has_value('On'),
                          use('Oe Peak').if_parameter('Osc On').has_value('On'),
                          use('Oe Decay').if_parameter('Osc On').has_value('On'),
                          use('Oe Sustain').if_parameter('Osc On').has_value('On'),
                          use('Oe Release').if_parameter('Osc On').has_value('On'))}),
  (
   'Osc. pg. 2',
   {BANK_PARAMETERS_KEY: (
                          use('Oe End').if_parameter('Osc On').has_value('On'),
                          use('Oe Mode').if_parameter('Osc On').has_value('On'),
                          use('').if_parameter('Osc On').has_value('Off').else_use('Oe Loop').if_parameter('Oe Mode').has_value('Loop').else_use('Oe Retrig').if_parameter('Oe Mode').has_value('Beat').else_use('Oe Retrig').if_parameter('Oe Mode').has_value('Sync').else_use(''),
                          use('O Type').if_parameter('Osc On').has_value('On'),
                          use('O Volume').if_parameter('Osc On').has_value('On'),
                          use('O Fix On').if_parameter('Osc On').has_value('On'),
                          use('').if_parameter('Osc On').has_value('Off').else_use('O Coarse').if_parameter('O Fix On').has_value('Off').else_use('O Fix Freq'),
                          use('').if_parameter('Osc On').has_value('Off').else_use('O Fine').if_parameter('O Fix On').has_value('Off').else_use('O Fix Freq Mul'))}),
  (
   'Pitch Env.',
   {BANK_PARAMETERS_KEY: (
                          'Pe On',
                          use('Pe < Env').if_parameter('Pe On').has_value('On'),
                          use('Pe Init').if_parameter('Pe On').has_value('On'),
                          use('Pe Attack').if_parameter('Pe On').has_value('On'),
                          use('Pe Peak').if_parameter('Pe On').has_value('On'),
                          use('Pe Decay').if_parameter('Pe On').has_value('On'),
                          use('Pe Sustain').if_parameter('Pe On').has_value('On'),
                          use('Pe Release').if_parameter('Pe On').has_value('On'))}),
  (
   'Pitch Env. 2',
   {BANK_PARAMETERS_KEY: (
                          'Pe On',
                          use('Pe End').if_parameter('Pe On').has_value('On'),
                          use('Pe R < Vel').if_parameter('Pe On').has_value('On'),
                          use('Pe Mode').if_parameter('Pe On').has_value('On'),
                          use('').if_parameter('Pe On').has_value('Off').else_use('Pe Loop').if_parameter('Pe Mode').has_value('Loop').else_use('Pe Retrig').if_parameter('Pe Mode').has_value('Beat').else_use('Pe Retrig').if_parameter('Pe Mode').has_value('Sync').else_use(''),
                          '',
                          '',
                          '')}),
  (
   'Pitch/Glide',
   {BANK_PARAMETERS_KEY: (
                          'Pe On',
                          'Spread',
                          'Transpose',
                          'Detune',
                          'Key Zone Shift',
                          'Glide Mode',
                          use('Glide Time').if_parameter('Glide Mode').has_value('On'),
                          '')}),
  (
   'LFO1 pg. 1',
   {BANK_PARAMETERS_KEY: (
                          'L 1 On',
                          use('L 1 Wave').if_parameter('L 1 On').has_value('On'),
                          use('L 1 Sync').if_parameter('L 1 On').has_value('On'),
                          use('').if_parameter('L 1 On').has_value('Off').else_use('L 1 Sync Rate').if_parameter('L 1 Sync').has_value('Sync').else_use('L 1 Rate'),
                          use('Vol < LFO').if_parameter('L 1 On').has_value('On'),
                          use('Filt < LFO').if_parameter('L 1 On').has_value('On'),
                          use('Pan < LFO').if_parameter('L 1 On').has_value('On'),
                          use('Pitch < LFO').if_parameter('L 1 On').has_value('On'))}),
  (
   'LFO1 pg. 2',
   {BANK_PARAMETERS_KEY: (
                          'L 1 On',
                          use('L 1 Retrig').if_parameter('L 1 On').has_value('On'),
                          use('').if_parameter('L 1 On').has_value('Off').else_use('L 1 Offset').if_parameter('L 1 Retrig').has_value('On').else_use(''),
                          use('L 1 Attack').if_parameter('L 1 On').has_value('On'),
                          '',
                          '',
                          '',
                          '')}),
  (
   'LFO2 pg. 1',
   {BANK_PARAMETERS_KEY: (
                          'L 2 On',
                          use('L 2 Wave').if_parameter('L 2 On').has_value('On'),
                          use('L 2 Sync').if_parameter('L 2 On').has_value('On'),
                          use('').if_parameter('L 2 On').has_value('Off').else_use('L 2 Sync Rate').if_parameter('L 2 Sync').has_value('Sync').else_use('L 2 Rate'),
                          use('L 2 Retrig').if_parameter('L 2 On').has_value('On'),
                          use('').if_parameter('L 2 On').has_value('Off').else_use('L 2 Offset').if_parameter('L 2 Retrig').has_value('On').else_use(''),
                          use('L 2 Attack').if_parameter('L 2 On').has_value('On'),
                          '')}),
  (
   'LFO2 pg. 2',
   {BANK_PARAMETERS_KEY: (
                          'L 2 On',
                          use('L 2 St Mode').if_parameter('L 2 On').has_value('On'),
                          use('').if_parameter('L 2 On').has_value('Off').else_use('L 2 Spin').if_parameter('L 2 St Mode').has_value('Spin').else_use('L 2 Phase'),
                          '',
                          '',
                          '',
                          '',
                          '')}),
  (
   'LFO3 pg. 1',
   {BANK_PARAMETERS_KEY: (
                          'L 3 On',
                          use('L 3 Wave').if_parameter('L 3 On').has_value('On'),
                          use('L 3 Sync').if_parameter('L 3 On').has_value('On'),
                          use('').if_parameter('L 3 On').has_value('Off').else_use('L 3 Sync Rate').if_parameter('L 3 Sync').has_value('Sync').else_use('L 3 Rate'),
                          use('L 3 Retrig').if_parameter('L 3 On').has_value('On'),
                          use('').if_parameter('L 3 On').has_value('Off').else_use('L 3 Offset').if_parameter('L 3 Retrig').has_value('On').else_use(''),
                          use('L 3 Attack').if_parameter('L 3 On').has_value('On'),
                          '')}),
  (
   'LFO3 pg. 2',
   {BANK_PARAMETERS_KEY: (
                          'L 3 On',
                          use('L 3 St Mode').if_parameter('L 3 On').has_value('On'),
                          use('').if_parameter('L 3 On').has_value('Off').else_use('L 3 Spin').if_parameter('L 3 St Mode').has_value('Spin').else_use('L 3 Phase'),
                          '',
                          '',
                          '',
                          '',
                          '')}),
  (
   'Aux Env.',
   {BANK_PARAMETERS_KEY: (
                          'Ae On',
                          use('Ae < Env').if_parameter('Ae On').has_value('On'),
                          use('Ae Init').if_parameter('Ae On').has_value('On'),
                          use('Ae Attack').if_parameter('Ae On').has_value('On'),
                          use('Ae Peak').if_parameter('Ae On').has_value('On'),
                          use('Ae Decay').if_parameter('Ae On').has_value('On'),
                          use('Ae Sustain').if_parameter('Ae On').has_value('On'),
                          use('Ae Release').if_parameter('Ae On').has_value('On'))}),
  (
   'Aux Env. 2',
   {BANK_PARAMETERS_KEY: (
                          'Ae On',
                          use('Ae End').if_parameter('Ae On').has_value('Off'),
                          use('Ae R < Vel').if_parameter('Ae On').has_value('Off'),
                          use('Ae Mode').if_parameter('Ae On').has_value('Off'),
                          use('').if_parameter('Ae On').has_value('Off').else_use('Ae Loop').if_parameter('Ae Mode').has_value('Loop').else_use('Ae Retrig').if_parameter('Ae Mode').has_value('Beat').else_use('Ae Retrig').if_parameter('Ae Mode').has_value('Sync').else_use(''),
                          '',
                          '',
                          '')}))), 
 'OriginalSimpler':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('Ve Attack').if_parameter('Multi Sample').has_value('On').else_use('Start'),
                          use('Ve Decay').if_parameter('Multi Sample').has_value('On').else_use('End'),
                          use('Ve Sustain').if_parameter('Multi Sample').has_value('On').else_use('Fade In').if_parameter('Mode').has_value('One-Shot').else_use('Nudge').if_parameter('Mode').has_value('Slicing').else_use('S Start').if_parameter('Mode').has_value('Classic'),
                          use('Ve Release').if_parameter('Multi Sample').has_value('On').else_use('Fade Out').if_parameter('Mode').has_value('One-Shot').else_use('Playback').if_parameter('Mode').has_value('Slicing').else_use('S Length').if_parameter('Mode').has_value('Classic'),
                          use('Pan').if_parameter('Multi Sample').has_value('On').and_parameter('F On').has_value('Off').else_use('Filter Type').if_parameter('Filter Type').is_available(True).and_parameter('Multi Sample').has_value('On').else_use('Filter Type (Legacy)').if_parameter('Multi Sample').has_value('On').else_use('Transpose').if_parameter('Mode').has_value('One-Shot').else_use('S Loop On').if_parameter('Mode').has_value('Classic'),
                          use('Filter Freq').if_parameter('Multi Sample').has_value('On').and_parameter('F On').has_value('On').else_use('Transpose').if_parameter('Multi Sample').has_value('On').else_use('Gain').if_parameter('Mode').has_value('One-Shot').else_use('Slice by').if_parameter('Mode').has_value('Slicing').else_use('S Loop Length').if_parameter('Mode').has_value('Classic').and_parameter('S Loop On').has_value('On').else_use('Transpose'),
                          use('Detune').if_parameter('Multi Sample').has_value('On').and_parameter('F On').has_value('Off').else_use('Filter Res').if_parameter('Filter Res').is_available(True).and_parameter('Multi Sample').has_value('On').else_use('Filter Res (Legacy)').if_parameter('Multi Sample').has_value('On').else_use('Trigger Mode').if_parameter('Mode').has_value('One-Shot').else_use('Sensitivity').if_parameter('Slice by').has_value('Transient').and_parameter('Mode').has_value('Slicing').else_use('Division').if_parameter('Slice by').has_value('Beat').and_parameter('Mode').has_value('Slicing').else_use('Regions').if_parameter('Slice by').has_value('Region').and_parameter('Mode').has_value('Slicing').else_use('Pad Slicing').if_parameter('Slice Style').has_value('Manual').and_parameter('Mode').has_value('Slicing').else_use('Trigger Mode').if_parameter('Mode').has_value('Slicing').else_use('S Loop Fade').if_parameter('Mode').has_value('Classic').and_parameter('Warp').has_value('Off').else_use('Detune'),
                          use('Volume').if_parameter('Multi Sample').has_value('On').else_use('Mode'))}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: (
                          'Glide Mode',
                          use('').if_parameter('Glide Mode').has_value('Off').else_use('Glide Time'),
                          'Voices',
                          'Transpose',
                          'Detune',
                          'Vol < Vel',
                          'Gain',
                          'Volume')}),
  (
   'Volume Envelope',
   {BANK_PARAMETERS_KEY: (
                          use('Ve Attack').if_parameter('Mode').has_value('Classic').else_use('Fade In'),
                          use('Ve Decay').if_parameter('Mode').has_value('Classic').else_use('Fade Out'),
                          use('Ve Sustain').if_parameter('Mode').has_value('Classic'),
                          use('Ve Release').if_parameter('Mode').has_value('Classic'),
                          'Filt < Vel',
                          'Vol < Vel',
                          'Vol < LFO',
                          'Volume')}),
  (
   'Warp',
   {BANK_PARAMETERS_KEY: (
                          use('').if_parameter('Multi Sample').has_value('On').else_use('Warp'),
                          use('').if_parameter('Multi Sample').has_value('On').else_use('').if_parameter('Warp').has_value('Off').else_use('Warp Mode'),
                          use('').if_parameter('Multi Sample').has_value('On').else_use('').if_parameter('Warp').has_value('Off').else_use('Preserve').if_parameter('Warp Mode').has_value('Beats').else_use('Grain Size Tones').if_parameter('Warp Mode').has_value('Tones').else_use('Grain Size Texture').if_parameter('Warp Mode').has_value('Texture').else_use('Formants').if_parameter('Warp Mode').has_value('Pro'),
                          use('').if_parameter('Multi Sample').has_value('On').else_use('').if_parameter('Warp').has_value('Off').else_use('Loop Mode').if_parameter('Warp Mode').has_value('Beats').else_use('Flux').if_parameter('Warp Mode').has_value('Texture').else_use('Envelope Complex Pro').if_parameter('Warp Mode').has_value('Pro'),
                          use('').if_parameter('Multi Sample').has_value('On').else_use('').if_parameter('Warp').has_value('Off').else_use('Envelope').if_parameter('Warp Mode').has_value('Beats'),
                          '',
                          '',
                          '')}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: (
                          'F On',
                          use('').if_parameter('F On').has_value('Off').else_use('Filter Type').if_parameter('Filter Type').is_available(True).else_use('Filter Type (Legacy)'),
                          use('Filter Freq').if_parameter('F On').has_value('On'),
                          use('').if_parameter('F On').has_value('Off').else_use('Filter Res').if_parameter('Filter Res').is_available(True).else_use('Filter Res (Legacy)'),
                          use('').if_parameter('F On').has_value('Off').else_use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Lowpass').else_use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Highpass').else_use('Filter Circuit - BP/NO/Morph'),
                          use('').if_parameter('F On').has_value('Off').else_use('Filter Morph').if_parameter('Filter Type').has_value('Morph').else_use('').if_parameter('Filter Type').has_value('Lowpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Highpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Bandpass').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Notch').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('Filter Drive'),
                          use('Filter Slope').if_parameter('F On').has_value('On').and_parameter('Filter Slope').is_available(True),
                          use('Filt < LFO').if_parameter('F On').has_value('On'))}),
  (
   'Filter Envelope',
   {BANK_PARAMETERS_KEY: (
                          'Fe On',
                          use('Fe Attack').if_parameter('Fe On').has_value('On'),
                          use('Fe Decay').if_parameter('Fe On').has_value('On'),
                          use('Fe Sustain').if_parameter('Fe On').has_value('On'),
                          use('Fe Release').if_parameter('Fe On').has_value('On'),
                          use('Filter Freq').if_parameter('Fe On').has_value('On').and_parameter('F On').has_value('On'),
                          use('Filter Res').if_parameter('Fe On').has_value('On').and_parameter('F On').has_value('On'),
                          use('Fe < Env').if_parameter('Fe On').has_value('On'))}),
  (
   'Pitch Envelope',
   {BANK_PARAMETERS_KEY: (
                          'Pe On',
                          use('Pe Attack').if_parameter('Pe On').has_value('On'),
                          use('Pe Decay').if_parameter('Pe On').has_value('On'),
                          use('Pe Sustain').if_parameter('Pe On').has_value('On'),
                          use('Pe Release').if_parameter('Pe On').has_value('On'),
                          use('Pe < Env').if_parameter('Pe On').has_value('On'),
                          '',
                          '')}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          'L On',
                          use('L Wave').if_parameter('L On').has_value('On'),
                          use('L Sync').if_parameter('L On').has_value('On'),
                          use('').if_parameter('L On').has_value('Off').else_use('L Rate').if_parameter('L Sync').has_value('Free').else_use('L Sync Rate'),
                          use('L Attack').if_parameter('L On').has_value('On'),
                          use('L R < Key').if_parameter('L On').has_value('On'),
                          use('L Retrig').if_parameter('L On').has_value('On'),
                          use('L Offset').if_parameter('L On').has_value('On'))}),
  (
   'Pan',
   {BANK_PARAMETERS_KEY: ('Pan', 'Spread', 'Pan < Rnd', 'Pan < LFO', '', '', '', '')}))), 
 'StringStudio':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('Exciter Type').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc ForceMassProt').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc FricStiff').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Velocity').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos').if_parameter('Exc On/Off').has_value('On'),
                          'String Decay',
                          'Str Damping',
                          'Volume')}),
  (
   'Exciter',
   {BANK_PARAMETERS_KEY: (
                          'Exc On/Off',
                          use('Exciter Type').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc ForceMassProt').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc FricStiff').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Velocity').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos Abs').if_parameter('Exc On/Off').has_value('On'),
                          'Volume')}),
  (
   'String & Pickup',
   {BANK_PARAMETERS_KEY: (
                          'String Decay',
                          'S Decay < Key',
                          'S Decay Ratio',
                          'Str Inharmon',
                          'Str Damping',
                          'S Damp < Key',
                          'Pickup On/Off',
                          use('Pickup Pos').if_parameter('Pickup On/Off').has_value('On'))}),
  (
   'Damper',
   {BANK_PARAMETERS_KEY: (
                          'Damper On',
                          use('Damper Mass').if_parameter('Damper On').has_value('On'),
                          use('D Stiffness').if_parameter('Damper On').has_value('On'),
                          use('Damp Pos').if_parameter('Damper On').has_value('On'),
                          use('D Damping').if_parameter('Damper On').has_value('On'),
                          use('Damper Gated').if_parameter('Damper On').has_value('On'),
                          use('').if_parameter('Damper On').has_value('Off').else_use('D Velocity').if_parameter('Damper Gated').has_value('On').else_use(''),
                          use('D Pos Abs').if_parameter('Damper On').has_value('On'))}),
  (
   'Termination',
   {BANK_PARAMETERS_KEY: (
                          'Term On/Off',
                          use('Term Mass').if_parameter('Term On/Off').has_value('On'),
                          use('Term Fng Stiff').if_parameter('Term On/Off').has_value('On'),
                          use('Term Fret Stiff').if_parameter('Term On/Off').has_value('On'),
                          use('T Mass < Vel').if_parameter('Term On/Off').has_value('On'),
                          use('T Mass < Key').if_parameter('Term On/Off').has_value('On'),
                          '',
                          'Volume')}),
  (
   'Body',
   {BANK_PARAMETERS_KEY: (
                          'Body On/Off',
                          use('Body Type').if_parameter('Body On/Off').has_value('On'),
                          use('Body Size').if_parameter('Body On/Off').has_value('On'),
                          use('Body Decay').if_parameter('Body On/Off').has_value('On'),
                          use('Body Low-Cut').if_parameter('Body On/Off').has_value('On'),
                          use('Body High-Cut').if_parameter('Body On/Off').has_value('On'),
                          use('Body Mix').if_parameter('Body On/Off').has_value('On'),
                          'Volume')}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: (
                          'Filter On/Off',
                          use('Filter Freq').if_parameter('Filter On/Off').has_value('On'),
                          use('Filter Reso').if_parameter('Filter On/Off').has_value('On'),
                          use('Filter Type').if_parameter('Filter On/Off').has_value('On'),
                          use('Freq < Env').if_parameter('Filter On/Off').has_value('On'),
                          use('Freq < LFO').if_parameter('Filter On/Off').has_value('On'),
                          use('Reso < Env').if_parameter('Filter On/Off').has_value('On'),
                          use('Reso < LFO').if_parameter('Filter On/Off').has_value('On'))}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          'LFO On/Off',
                          use('LFO Shape').if_parameter('LFO On/Off').has_value('On'),
                          use('LFO Sync On').if_parameter('LFO On/Off').has_value('On'),
                          use('').if_parameter('LFO On/Off').has_value('Off').else_use('LFO SyncRate').if_parameter('LFO Sync On').has_value('Beat').else_use('LFO Speed'),
                          use('LFO Delay').if_parameter('LFO On/Off').has_value('On'),
                          use('LFO Fade In').if_parameter('LFO On/Off').has_value('On'),
                          '',
                          '')}),
  (
   'Vibrato',
   {BANK_PARAMETERS_KEY: (
                          'Vibrato On/Off',
                          use('Vib Delay').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib Fade-In').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib Speed').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib Amount').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib < ModWh').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib Error').if_parameter('Vibrato On/Off').has_value('On'),
                          '')}),
  (
   'Unison & Portamento',
   {BANK_PARAMETERS_KEY: (
                          'Unison On/Off',
                          use('Unison Voices').if_parameter('Unison On/Off').has_value('On'),
                          use('Uni Delay').if_parameter('Unison On/Off').has_value('On'),
                          use('Uni Detune').if_parameter('Unison On/Off').has_value('On'),
                          'Porta On/Off',
                          use('Porta Time').if_parameter('Porta On/Off').has_value('On'),
                          use('Porta Legato').if_parameter('Porta On/Off').has_value('On'),
                          use('Porta Prop').if_parameter('Porta On/Off').has_value('On'))}),
  (
   'Global 1',
   {BANK_PARAMETERS_KEY: (
                          'Octave',
                          'Semitone',
                          'Fine Tune',
                          'PB Range',
                          use('Note PB Range').with_name('Note PB'),
                          '',
                          '',
                          '')}),
  (
   'Global 2',
   {BANK_PARAMETERS_KEY: ('Voices', 'Stretch', 'Error', 'Key Priority', '', '', '', '')}),
  (
   'Filt. Env.',
   {BANK_PARAMETERS_KEY: (
                          'FEG On/Off',
                          use('FEG Attack').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG Decay').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG Sustain').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG Release').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG Att < Vel').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG < Vel').if_parameter('FEG On/Off').has_value('On'),
                          '')}),
  (
   'Exciter Mod.',
   {BANK_PARAMETERS_KEY: (
                          use('Exc ForceMassProt < Vel').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc ForceMassProt < Key').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc FricStiff < Vel').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc FricStiff < Key').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Vel < Vel').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Vel < Key').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos < Vel').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos < Key').if_parameter('Exc On/Off').has_value('On'))}),
  (
   'Mass Mod.',
   {BANK_PARAMETERS_KEY: (
                          use('D Mass < Key').if_parameter('Damper On').has_value('On'),
                          use('D Stiff < Key').if_parameter('Damper On').has_value('On'),
                          use('D Pos < Key').if_parameter('Damper On').has_value('On'),
                          use('D Pos < Vel').if_parameter('Damper On').has_value('On'),
                          use('Damper Gated').if_parameter('Damper On').has_value('On'),
                          use('').if_parameter('Damper On').has_value('Off').else_use('D Velo < Key').if_parameter('Damper Gated').has_value('On').else_use(''),
                          '',
                          '')}),
  (
   'MIDI Mod.',
   {BANK_PARAMETERS_KEY: ('Press Dest A', 'Press Amt A', 'Press Dest B', 'Press Amt B', 'Slide Dest A', 'Slide Amt A',
 'Slide Dest B', 'Slide Amt B')}))), 
 'InstrumentVector':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('Osc 1 Pos').with_name('Pos 1').if_parameter('Osc 1 On').has_value('On').else_use('Osc 2 Pos').with_name('Pos 2').if_parameter('Osc 2 On').has_value('On').else_use('Sub Tone').if_parameter('Sub On').has_value('On').else_use(''),
                          use('Filter 1 Freq').with_name('Freq 1').if_parameter('Filter 1 On').has_value('On').else_use('Filter 2 Freq').with_name('Freq 2').if_parameter('Filter 2 On').has_value('On').else_use('Osc 1 Effect 1').with_name('FX 1').if_parameter('Osc 1 On').has_value('On').else_use('Osc 2 Effect 1').with_name('FX 1').if_parameter('Osc 2 On').has_value('On').else_use('Osc 1 Effect 1').with_name('Osc1 FX1').if_parameter('Osc 1 On').has_value('Osc2 FX1').else_use('Osc 2 Effect 1').with_name('FX 1').if_parameter('Osc 2 On').has_value('On').else_use('Sub Transpose').if_parameter('Sub On').has_value('On').else_use(''),
                          use('Filter 1 Res').with_name('Res 1').if_parameter('Filter 1 On').has_value('On').else_use('Filter 2 Res').with_name('Res 2').if_parameter('Filter 2 On').has_value('On').else_use('Osc 1 Effect 2').with_name('FX 2').if_parameter('Osc 1 On').has_value('On').else_use('Osc 2 Effect 2').with_name('FX 2').if_parameter('Osc 2 On').has_value('On').else_use('Amp Decay').with_name('Decay'),
                          use('Amp Release').with_name('Release'),
                          'Unison Amount',
                          'Time',
                          'Global Mod Amount',
                          'Volume')}),
  (
   'Osc 1',
   {BANK_PARAMETERS_KEY: (
                          'Osc 1 On',
                          use('Osc 1 Pitch').with_name('Pitch'),
                          use('Osc 1 Category').with_name('Category'),
                          use('Osc 1 Table').with_name('Table'),
                          use('Osc 1 Pos').with_name('Position'),
                          use('Osc 1 Effect Type').with_name('Effect Type'),
                          use('Osc 1 Effect 1').with_name('FX 1'),
                          use('Osc 1 Effect 2').with_name('FX 2'))}),
  (
   'Osc 2',
   {BANK_PARAMETERS_KEY: (
                          'Osc 2 On',
                          use('Osc 2 Pitch').with_name('Pitch'),
                          use('Osc 2 Category').with_name('Category'),
                          use('Osc 2 Table').with_name('Table'),
                          use('Osc 2 Pos').with_name('Position'),
                          use('Osc 2 Effect Type').with_name('Effect Type'),
                          use('Osc 2 Effect 1').with_name('FX 1'),
                          use('Osc 2 Effect 2').with_name('FX 2'))}),
  (
   'Sub',
   {BANK_PARAMETERS_KEY: (
                          'Sub On',
                          use('Sub Transpose').with_name('Transp'),
                          use('Sub Tone').with_name('Tone'),
                          '',
                          '',
                          '',
                          '',
                          use('Sub Gain').with_name('Gain'))}),
  (
   'Mix',
   {BANK_PARAMETERS_KEY: (
                          use('Osc 1 Pitch').with_name('Pitch 1'),
                          use('Osc 2 Pitch').with_name('Pitch 2'),
                          use('Sub Transpose').with_name('Octave Sub'),
                          use('Osc 1 Pan').with_name('Pan 1'),
                          use('Osc 2 Pan').with_name('Pan 2'),
                          use('Osc 1 Gain').with_name('Gain 1'),
                          use('Osc 2 Gain').with_name('Gain 2'),
                          use('Sub Gain').with_name('Gain Sub'))}),
  (
   'Filter 1',
   {BANK_PARAMETERS_KEY: (
                          use('Filter 1 On').with_name('F1 On'),
                          use('Filter 1 Type').with_name('Type'),
                          use('Filter 1 LP/HP').with_name('Circuit').if_parameter('Filter 1 Type').has_value('Lowpass').or_parameter('Filter 1 Type').has_value('Highpass').else_use('Filter 1 BP/NO/Morph').with_name('Circuit').if_parameter('Filter 1 Type').has_value('Bandpass').or_parameter('Filter 1 Type').has_value('Notch').or_parameter('Filter 1 Type').has_value('Morph').else_use(''),
                          use('Filter 1 Slope').with_name('Slope'),
                          use('Filter 1 Freq').with_name('Freq'),
                          use('Filter 1 Res').with_name('Res'),
                          use('Filter 1 Drive').with_name('Drive').if_parameter('Filter 1 Type').has_value('Lowpass').or_parameter('Filter 1 Type').has_value('Highpass').or_parameter('Filter 1 Type').has_value('Notch').or_parameter('Filter 1 Type').has_value('Bandpass').and_parameter('Filter 1 LP/HP').does_not_have_value('Clean').else_use('Filter 1 Morph').with_name('Morph').if_parameter('Filter 1 Type').has_value('Morph').else_use(''),
                          '')}),
  (
   'Filter 2',
   {BANK_PARAMETERS_KEY: (
                          use('Filter 2 On').with_name('F2 On'),
                          use('Filter 2 Type').with_name('Type'),
                          use('Filter 2 LP/HP').with_name('Circuit').if_parameter('Filter 2 Type').has_value('Lowpass').or_parameter('Filter 2 Type').has_value('Highpass').else_use('Filter 2 BP/NO/Morph').with_name('Circuit').if_parameter('Filter 2 Type').has_value('Bandpass').or_parameter('Filter 2 Type').has_value('Notch').or_parameter('Filter 2 Type').has_value('Morph').else_use(''),
                          use('Filter 2 Slope').with_name('Slope'),
                          use('Filter 2 Freq').with_name('Freq'),
                          use('Filter 2 Res').with_name('Res'),
                          use('Filter 2 Drive').with_name('Drive').if_parameter('Filter 2 Type').has_value('Lowpass').or_parameter('Filter 2 Type').has_value('Highpass').or_parameter('Filter 2 Type').has_value('Notch').or_parameter('Filter 2 Type').has_value('Bandpass').and_parameter('Filter 2 LP/HP').does_not_have_value('Clean').else_use('Filter 2 Morph').with_name('Morph').if_parameter('Filter 2 Type').has_value('Morph').else_use(''),
                          '')}),
  (
   'Amp Env',
   {BANK_PARAMETERS_KEY: (
                          use('Amp Attack').with_name('Attack'),
                          use('Amp Decay').with_name('Decay'),
                          use('Amp Sustain').with_name('Sustain'),
                          use('Amp Release').with_name('Release'),
                          use('Amp A Slope').with_name('A Slope'),
                          use('Amp D Slope').with_name('D Slope'),
                          use('Amp R Slope').with_name('R Slope'),
                          use('Amp Loop Mode').with_name('Mode'))}),
  (
   'Env 2',
   {BANK_PARAMETERS_KEY: (
                          use('Env 2 Attack').with_name('Attack'),
                          use('Env 2 Decay').with_name('Decay'),
                          use('Env 2 Sustain').with_name('Sustain'),
                          use('Env 2 Release').with_name('Release'),
                          use('Env 2 A Slope').with_name('A Slope'),
                          use('Env 2 D Slope').with_name('D Slope'),
                          use('Env 2 R Slope').with_name('R Slope'),
                          use('Env 2 Loop Mode').with_name('Mode'))}),
  (
   'Env 3',
   {BANK_PARAMETERS_KEY: (
                          use('Env 3 Attack').with_name('Attack'),
                          use('Env 3 Decay').with_name('Decay'),
                          use('Env 3 Sustain').with_name('Sustain'),
                          use('Env 3 Release').with_name('Release'),
                          use('Env 3 A Slope').with_name('A Slope'),
                          use('Env 3 D Slope').with_name('D Slope'),
                          use('Env 3 R Slope').with_name('R Slope'),
                          use('Env 3 Loop Mode').with_name('Mode'))}),
  (
   'LFO 1',
   {BANK_PARAMETERS_KEY: (
                          use('LFO 1 Shape').with_name('Shape'),
                          use('LFO 1 Sync').with_name('Sync'),
                          use('LFO 1 S. Rate').with_name('SyncRate').if_parameter('LFO 1 Sync').has_value('Tempo').else_use('LFO 1 Rate').with_name('Rate'),
                          use('LFO 1 Shaping').with_name('Shape'),
                          use('LFO 1 Attack Time').with_name('Attack'),
                          use('LFO 1 Amount').with_name('Amount'),
                          use('LFO 1 Phase Offset').with_name('Phase'),
                          use('LFO 1 Retrigger').with_name('Retrigger'))}),
  (
   'LFO 2',
   {BANK_PARAMETERS_KEY: (
                          use('LFO 2 Shape').with_name('Shape'),
                          use('LFO 2 Sync').with_name('Sync'),
                          use('LFO 2 S. Rate').with_name('SyncRate').if_parameter('LFO 2 Sync').has_value('Tempo').else_use('LFO 2 Rate').with_name('Rate'),
                          use('LFO 2 Shaping').with_name('Shape'),
                          use('LFO 2 Attack Time').with_name('Attack'),
                          use('LFO 2 Amount').with_name('Amount'),
                          use('LFO 2 Phase Offset').with_name('Phase'),
                          use('LFO 2 Retrigger').with_name('Retrigger'))}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Time', 'Global Mod Amount', 'Unison Mode', 'Unison Amount', 'Mono On', 'Glide', 'Transpose',
 'Volume')}))), 
 'MidiArpeggiator':IndexedDict((
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
                          use('Groove').if_parameter('Sync On').has_value('On'),
                          'Offset',
                          'Repeats',
                          'Gate',
                          'Retrigger Mode',
                          use('Ret. Interval').if_parameter('Retrigger Mode').has_value('Beat'))}),
  (
   'Pitch/Vel.',
   {BANK_PARAMETERS_KEY: (
                          'Tranpose Mode',
                          use('').if_parameter('Tranpose Mode').has_value('Shift').else_use('Tranpose Key'),
                          use('').if_parameter('Tranpose Mode').has_value('Shift').else_use('Transp. Steps'),
                          use('').if_parameter('Tranpose Mode').has_value('Shift').else_use('Transp. Dist.'),
                          'Velocity On',
                          use('Vel. Retrigger').if_parameter('Velocity On').has_value('On'),
                          use('Velocity Decay').if_parameter('Velocity On').has_value('On'),
                          use('Velocity Target').if_parameter('Velocity On').has_value('On'))}))), 
 'MidiChord':IndexedDict((
  (
   'Shift',
   {BANK_PARAMETERS_KEY: ('Shift1', 'Shift2', 'Shift3', 'Shift4', 'Shift5', 'Shift6', '', '')}),
  (
   'Velocity',
   {BANK_PARAMETERS_KEY: ('Velocity1', 'Velocity2', 'Velocity3', 'Velocity4', 'Velocity5', 'Velocity6', '',
 '')}))), 
 'MidiNoteLength':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Trigger Mode',
                          'Sync On',
                          use('Synced Length').if_parameter('Sync On').has_value('On').else_use('Time Length'),
                          'Gate',
                          use('On/Off-Balance').if_parameter('Trigger Mode').has_value('On'),
                          use('Decay Time').if_parameter('Trigger Mode').has_value('On'),
                          use('Decay Key Scale').if_parameter('Trigger Mode').has_value('On'),
                          '')}),)), 
 'MidiPitcher':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Pitch', 'Range', 'Lowest', '', '', '', '', '')}),)), 
 'MidiRandom':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Chance', 'Choices', 'Mode', 'Scale', 'Sign', '', '', '')}),)), 
 'MidiScale':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Base', 'Transpose', 'Range', 'Lowest', 'Fold', '', '', '')}),)), 
 'MidiVelocity':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Mode',
                          use('').if_parameter('Mode').has_value('Fixed').else_use('Drive'),
                          use('').if_parameter('Mode').has_value('Fixed').else_use('Compand'),
                          'Out Hi',
                          use('').if_parameter('Mode').has_value('Fixed').else_use('Out Low'),
                          use('').if_parameter('Mode').has_value('Fixed').else_use('Range'),
                          use('').if_parameter('Mode').has_value('Fixed').else_use('Lowest'),
                          'Random')}),)), 
 'Amp':IndexedDict((
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Amp Type', 'Bass', 'Middle', 'Treble', 'Presence', 'Gain', 'Volume', 'Dry/Wet')}),
  (
   'Dual/Mono',
   {BANK_PARAMETERS_KEY: ('Dual Mono', '', '', '', '', '', '', '')}))), 
 'AutoFilter':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('Filter Type').if_parameter('Filter Type').is_available(True).else_use('Filter Type (Legacy)'),
                          use('Frequency'),
                          use('Resonance').if_parameter('Resonance').is_available(True).else_use('Resonance (Legacy)'),
                          use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Lowpass').else_use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Highpass').else_use('Filter Circuit - BP/NO/Morph'),
                          use('Morph').if_parameter('Filter Type').has_value('Morph').else_use('').if_parameter('Filter Type').has_value('Lowpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Highpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Bandpass').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Notch').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('Drive').if_parameter('Drive').is_available(True),
                          'LFO Amount',
                          'LFO Sync',
                          use('LFO Frequency').if_parameter('LFO Sync').has_value('Free').else_use('LFO Sync Rate'))}),
  (
   'Envelope',
   {BANK_PARAMETERS_KEY: (
                          use('Filter Type').if_parameter('Filter Type').is_available(True).else_use('Filter Type (Legacy)'),
                          use('Frequency'),
                          use('Resonance').if_parameter('Resonance').is_available(True).else_use('Resonance (Legacy)'),
                          use('Slope').if_parameter('Slope').is_available(True),
                          use('Morph').if_parameter('Filter Type').has_value('Morph').else_use('').if_parameter('Filter Type').has_value('Lowpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Highpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Bandpass').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Notch').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('Drive').if_parameter('Drive').is_available(True),
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
                          use('').if_parameter('LFO Waveform').has_value('S&H Mono').else_use('LFO Offset').if_parameter('LFO Sync').has_value('Sync').else_use('LFO Stereo Mode'),
                          use('').if_parameter('LFO Waveform').has_value('S&H Mono').else_use('LFO Phase').if_parameter('LFO Sync').has_value('Sync').else_use('LFO Phase').if_parameter('LFO Stereo Mode').has_value('Phase').else_use('LFO Spin'),
                          'LFO Quantize On',
                          use('LFO Quantize Rate').if_parameter('LFO Quantize On').has_value('On'))}),
  (
   'Sidechain',
   {BANK_PARAMETERS_KEY: (
                          'S/C On',
                          use('S/C Mix').if_parameter('S/C On').has_value('On'),
                          use('S/C Gain').if_parameter('S/C On').has_value('On'),
                          '',
                          '',
                          '',
                          '',
                          '')}))), 
 'AutoPan':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Amount',
                          'Shape',
                          'Invert',
                          'Waveform',
                          'LFO Type',
                          use('Sync Rate').if_parameter('LFO Type').has_value('Beats').else_use('Frequency'),
                          use('').if_parameter('Waveform').has_value('S&H Width').else_use('Stereo Mode').if_parameter('LFO Type').has_value('Frequency').else_use('Offset'),
                          use('Width (Random)').if_parameter('Waveform').has_value('S&H Width').else_use('Phase').if_parameter('LFO Type').has_value('Beats').else_use('Spin').if_parameter('Stereo Mode').has_value('Spin').else_use('Phase'))}),)), 
 'BeatRepeat':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Grid', 'Interval', 'Offset', 'Gate', 'Pitch', 'Pitch Decay', 'Variation', 'Chance')}),
  (
   'Filt/Mix',
   {BANK_PARAMETERS_KEY: (
                          'Filter On',
                          use('Filter Freq').if_parameter('Filter On').has_value('On'),
                          use('Filter Width').if_parameter('Filter On').has_value('On'),
                          '',
                          'Mix Type',
                          'Volume',
                          'Decay',
                          'Chance')}),
  (
   'Repeat Rate',
   {BANK_PARAMETERS_KEY: ('Repeat', 'Interval', 'Offset', 'Gate', 'Grid', 'Block Triplets', 'Variation', 'Variation Type')}))), 
 'Cabinet':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Cabinet Type', 'Microphone Type', 'Microphone Position', 'Dual Mono', '', '', '',
 'Dry/Wet')}),)), 
 'Chorus':IndexedDict((
  (
   'Chorus',
   {BANK_PARAMETERS_KEY: (
                          'LFO Amount',
                          'LFO Rate',
                          'Delay 1 Time',
                          'Delay 1 HiPass',
                          'Delay 2 Mode',
                          use('').if_parameter('Delay 2 Mode').has_value('Off').else_use('Delay 2 Time'),
                          'Feedback',
                          'Dry/Wet')}),
  (
   'Other',
   {BANK_PARAMETERS_KEY: ('LFO Extend On', 'Polarity', 'Link On', '', '', '', '', '')}))), 
 'Compressor2':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Threshold',
                          use('Expansion Ratio').if_parameter('Model').has_value('Expand').else_use('Ratio'),
                          'Model',
                          'Knee',
                          'Attack',
                          use('Release').if_parameter('Auto Release On/Off').has_value('Off').else_use('Makeup').if_parameter('S/C On').has_value('Off'),
                          'Dry/Wet',
                          'Output Gain')}),
  (
   'Sidechain',
   {BANK_PARAMETERS_KEY: (
                          'S/C On',
                          use('S/C Gain').if_parameter('S/C On').has_value('On'),
                          use('S/C Mix').if_parameter('S/C On').has_value('On'),
                          'S/C Listen',
                          'S/C EQ On',
                          use('S/C EQ Type').if_parameter('S/C EQ On').has_value('On'),
                          use('S/C EQ Freq').if_parameter('S/C EQ On').has_value('On'),
                          use('').if_parameter('S/C EQ On').has_value('Off').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('Low Shelf').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('High Shelf').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('Bell').else_use('S/C EQ Q'))}),
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
                          'Output Gain')}))), 
 'Corpus':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Resonance Type',
                          use('').if_parameter('Resonance Type').has_value('Tube').else_use('').if_parameter('Resonance Type').has_value('Pipe').else_use('Brightness'),
                          'Decay',
                          use('Radius').if_parameter('Resonance Type').has_value('Tube').else_use('Radius').if_parameter('Resonance Type').has_value('Pipe').else_use('Material'),
                          use('').if_parameter('Resonance Type').has_value('Tube').else_use('Opening').if_parameter('Resonance Type').has_value('Pipe').else_use('Inharmonics'),
                          use('Ratio').if_parameter('Resonance Type').has_value('Plate').else_use('Ratio').if_parameter('Resonance Type').has_value('Membrane').else_use(''),
                          use('Transpose').if_parameter('MIDI Frequency').has_value('On').else_use('Tune'),
                          'Dry Wet')}),
  (
   'Body',
   {BANK_PARAMETERS_KEY: (
                          'Resonance Type',
                          use('Ratio').if_parameter('Resonance Type').has_value('Plate').else_use('Ratio').if_parameter('Resonance Type').has_value('Membrane'),
                          'Decay',
                          use('Radius').if_parameter('Resonance Type').has_value('Tube').else_use('Radius').if_parameter('Resonance Type').has_value('Pipe').else_use('Material'),
                          use('').if_parameter('Resonance Type').has_value('Tube').else_use('Opening').if_parameter('Resonance Type').has_value('Pipe').else_use('Inharmonics'),
                          use('').if_parameter('Resonance Type').has_value('Tube').else_use('').if_parameter('Resonance Type').has_value('Pipe').else_use('Listening L'),
                          use('').if_parameter('Resonance Type').has_value('Tube').else_use('').if_parameter('Resonance Type').has_value('Pipe').else_use('Listening R'),
                          use('').if_parameter('Resonance Type').has_value('Tube').else_use('').if_parameter('Resonance Type').has_value('Pipe').else_use('Hit'))}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          'LFO On/Off',
                          use('LFO Shape').if_parameter('LFO On/Off').has_value('On'),
                          use('LFO Amount').if_parameter('LFO On/Off').has_value('On'),
                          use('LFO Sync').if_parameter('LFO On/Off').has_value('On'),
                          use('').if_parameter('LFO On/Off').has_value('Off').else_use('LFO Rate').if_parameter('LFO Sync').has_value('Free').else_use('LFO Sync Rate'),
                          use('').if_parameter('LFO On/Off').has_value('Off').else_use('LFO Stereo Mode').if_parameter('LFO Sync').has_value('Free').else_use('Offset'),
                          use('').if_parameter('LFO On/Off').has_value('Off').else_use('Phase').if_parameter('LFO Sync').has_value('Sync').else_use('Spin').if_parameter('LFO Stereo Mode').has_value('Spin'),
                          '')}),
  (
   'Tune & Sidechain',
   {BANK_PARAMETERS_KEY: (
                          'MIDI Frequency',
                          'MIDI Mode',
                          use('Transpose').if_parameter('MIDI Frequency').has_value('On').else_use('Tune'),
                          use('Fine').if_parameter('MIDI Frequency').has_value('On'),
                          'Spread',
                          use('').if_parameter('Resonance Type').has_value('Tube').else_use('').if_parameter('Resonance Type').has_value('Pipe').else_use('Brightness'),
                          'Note Off',
                          use('Off Decay').if_parameter('Note Off').has_value('On'))}),
  (
   'Filter & Mix',
   {BANK_PARAMETERS_KEY: (
                          'Filter On/Off',
                          use('Mid Freq').if_parameter('Filter On/Off').has_value('On'),
                          use('Width').if_parameter('Filter On/Off').has_value('On'),
                          use('').if_parameter('Resonance Type').has_value('Tube').else_use('').if_parameter('Resonance Type').has_value('Pipe').else_use('Resonator Quality'),
                          'Bleed',
                          'Gain',
                          'Dry Wet',
                          '')}))), 
 'Delay':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('L Sync Enum').with_name('DlayMd L'),
                          use('L 16th').with_name('Beat Delay').if_parameter('L Sync').has_value('On').else_use('L Time').with_name('Beat Delay'),
                          'L Offset',
                          use('R Sync Enum').with_name('DlayMd R'),
                          use('R 16th').with_name('Beat Delay').if_parameter('R Sync').has_value('On').else_use('R Time').with_name('Beat Delay'),
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
                          'Dry/Wet')}))), 
 'DrumBuss':IndexedDict((
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
   {BANK_PARAMETERS_KEY: ('Trim', 'Output Gain', 'Dry/Wet', 'Compressor On', 'Damping Freq', '', '', '')}))), 
 'Tube':IndexedDict((
  (
   'Character',
   {BANK_PARAMETERS_KEY: ('Drive', 'Tube Type', 'Bias', 'Tone', 'Attack', 'Release', 'Envelope', 'Dry/Wet')}),
  (
   'Output',
   {BANK_PARAMETERS_KEY: ('', '', '', '', '', '', 'Output', 'Dry/Wet')}))), 
 'Echo':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('L Time').with_name('M Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync').has_value('Off').else_use('L Time').if_parameter('L Sync').has_value('Off').else_use('L 16th').with_name('M 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync Mode').has_value('16th').else_use('L 16th').if_parameter('L Sync Mode').has_value('16th').else_use('L Division').with_name('M Division').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Division'),
                          use('L Sync').with_name('M Sync').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync'),
                          use('L Sync Mode').with_name('M Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync').has_value('On').else_use('L Sync Mode').if_parameter('L Sync').has_value('On'),
                          'HP Freq',
                          'LP Freq',
                          'Feedback',
                          'Input Gain',
                          'Dry Wet')}),
  (
   'L/Mid',
   {BANK_PARAMETERS_KEY: (
                          use('L Time').with_name('M Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync').has_value('Off').else_use('L Time').if_parameter('L Sync').has_value('Off').else_use('L 16th').with_name('M 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync Mode').has_value('16th').else_use('L 16th').if_parameter('L Sync Mode').has_value('16th').else_use('L Division').with_name('M Division').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Division'),
                          use('L Sync').with_name('M Sync').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync'),
                          use('L Sync Mode').with_name('M Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync').has_value('On').else_use('L Sync Mode').if_parameter('L Sync').has_value('On'),
                          use('L Offset').with_name('M Offset').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Offset'),
                          'Link',
                          'Feedback',
                          'Feedback Inv',
                          'Dry Wet')}),
  (
   'R/Side',
   {BANK_PARAMETERS_KEY: (
                          use('R Time').with_name('S Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('R Sync').has_value('Off').and_parameter('Link').has_value('Off').else_use('R Time').if_parameter('R Sync').has_value('Off').and_parameter('Link').has_value('Off').else_use('R 16th').with_name('S 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('R Sync Mode').has_value('16th').and_parameter('Link').has_value('Off').else_use('R 16th').if_parameter('R Sync Mode').has_value('16th').and_parameter('Link').has_value('Off').else_use('R Division').with_name('S Division').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('Link').has_value('Off').else_use('R Division').if_parameter('Link').has_value('Off').else_use('L Time').with_name('M Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync').has_value('Off').else_use('L Time').if_parameter('L Sync').has_value('Off').else_use('L 16th').with_name('M 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync Mode').has_value('16th').else_use('L 16th').if_parameter('L Sync Mode').has_value('16th').else_use('L Division').with_name('M Division').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Division'),
                          use('R Sync').with_name('S Sync').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('Link').has_value('Off').else_use('R Sync').if_parameter('Link').has_value('Off').else_use('L Sync').with_name('M Sync').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync'),
                          use('R Sync Mode').with_name('S Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('R Sync').has_value('On').and_parameter('Link').has_value('Off').else_use('R Sync Mode').if_parameter('R Sync').has_value('On').and_parameter('Link').has_value('Off').else_use('L Sync Mode').with_name('M Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync').has_value('On').else_use('L Sync Mode').if_parameter('L Sync').has_value('On'),
                          use('R Offset').with_name('S Offset').if_parameter('Channel Mode').has_value('Mid/Side').else_use('R Offset'),
                          'Link',
                          'Feedback',
                          'Feedback Inv',
                          'Dry Wet')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Repitch', 'Channel Mode', 'Stereo Width', '', 'Clip Dry', 'Input Gain', 'Output Gain',
 'Dry Wet')}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: ('Filter On', 'HP Freq', 'HP Res', 'LP Freq', 'LP Res', 'Input Gain', 'Output Gain',
 'Dry Wet')}),
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
 '')}))), 
 'Eq8':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('1 Frequency A').if_parameter('1 Filter On A').has_value('On'),
                          use('').if_parameter('1 Filter On A').has_value('Off').else_use('1 Gain A').if_parameter('1 Filter Type A').has_value('Low Shelf').else_use('1 Gain A').if_parameter('1 Filter Type A').has_value('Bell').else_use('1 Gain A').if_parameter('1 Filter Type A').has_value('High Shelf').else_use('1 Resonance A'),
                          use('2 Frequency A').if_parameter('2 Filter On A').has_value('On'),
                          use('').if_parameter('2 Filter On A').has_value('Off').else_use('2 Gain A').if_parameter('2 Filter Type A').has_value('Low Shelf').else_use('2 Gain A').if_parameter('2 Filter Type A').has_value('Bell').else_use('2 Gain A').if_parameter('2 Filter Type A').has_value('High Shelf').else_use('2 Resonance A'),
                          use('3 Frequency A').if_parameter('3 Filter On A').has_value('On'),
                          use('').if_parameter('3 Filter On A').has_value('Off').else_use('3 Gain A').if_parameter('3 Filter Type A').has_value('Low Shelf').else_use('3 Gain A').if_parameter('3 Filter Type A').has_value('Bell').else_use('3 Gain A').if_parameter('3 Filter Type A').has_value('High Shelf').else_use('3 Resonance A'),
                          use('4 Frequency A').if_parameter('4 Filter On A').has_value('On'),
                          use('').if_parameter('4 Filter On A').has_value('Off').else_use('4 Gain A').if_parameter('4 Filter Type A').has_value('Low Shelf').else_use('4 Gain A').if_parameter('4 Filter Type A').has_value('Bell').else_use('4 Gain A').if_parameter('4 Filter Type A').has_value('High Shelf').else_use('4 Resonance A'))}),
  (
   'EQ Band 1',
   {BANK_PARAMETERS_KEY: (
                          '1 Filter On A',
                          use('1 Filter Type A').if_parameter('1 Filter On A').has_value('On'),
                          use('1 Frequency A').if_parameter('1 Filter On A').has_value('On'),
                          use('1 Gain A').if_parameter('1 Filter On A').has_value('On'),
                          use('1 Resonance A').if_parameter('1 Filter On A').has_value('On'),
                          'Adaptive Q',
                          'Scale',
                          'Output Gain')}),
  (
   'EQ Band 2',
   {BANK_PARAMETERS_KEY: (
                          '2 Filter On A',
                          use('2 Filter Type A').if_parameter('2 Filter On A').has_value('On'),
                          use('2 Frequency A').if_parameter('2 Filter On A').has_value('On'),
                          use('2 Gain A').if_parameter('2 Filter On A').has_value('On'),
                          use('2 Resonance A').if_parameter('2 Filter On A').has_value('On'),
                          'Adaptive Q',
                          'Scale',
                          'Output Gain')}),
  (
   'EQ Band 3',
   {BANK_PARAMETERS_KEY: (
                          '3 Filter On A',
                          use('3 Filter Type A').if_parameter('3 Filter On A').has_value('On'),
                          use('3 Frequency A').if_parameter('3 Filter On A').has_value('On'),
                          use('3 Gain A').if_parameter('3 Filter On A').has_value('On'),
                          use('3 Resonance A').if_parameter('3 Filter On A').has_value('On'),
                          'Adaptive Q',
                          'Scale',
                          'Output Gain')}),
  (
   'EQ Band 4',
   {BANK_PARAMETERS_KEY: (
                          '4 Filter On A',
                          use('4 Filter Type A').if_parameter('4 Filter On A').has_value('On'),
                          use('4 Frequency A').if_parameter('4 Filter On A').has_value('On'),
                          use('4 Gain A').if_parameter('4 Filter On A').has_value('On'),
                          use('4 Resonance A').if_parameter('4 Filter On A').has_value('On'),
                          'Adaptive Q',
                          'Scale',
                          'Output Gain')}),
  (
   'EQ Band 5',
   {BANK_PARAMETERS_KEY: (
                          '5 Filter On A',
                          use('5 Filter Type A').if_parameter('5 Filter On A').has_value('On'),
                          use('5 Frequency A').if_parameter('5 Filter On A').has_value('On'),
                          use('5 Gain A').if_parameter('5 Filter On A').has_value('On'),
                          use('5 Resonance A').if_parameter('5 Filter On A').has_value('On'),
                          'Adaptive Q',
                          'Scale',
                          'Output Gain')}),
  (
   'EQ Band 6',
   {BANK_PARAMETERS_KEY: (
                          '6 Filter On A',
                          use('6 Filter Type A').if_parameter('6 Filter On A').has_value('On'),
                          use('6 Frequency A').if_parameter('6 Filter On A').has_value('On'),
                          use('6 Gain A').if_parameter('6 Filter On A').has_value('On'),
                          use('6 Resonance A').if_parameter('6 Filter On A').has_value('On'),
                          'Adaptive Q',
                          'Scale',
                          'Output Gain')}),
  (
   'EQ Band 7',
   {BANK_PARAMETERS_KEY: (
                          '7 Filter On A',
                          use('7 Filter Type A').if_parameter('7 Filter On A').has_value('On'),
                          use('7 Frequency A').if_parameter('7 Filter On A').has_value('On'),
                          use('7 Gain A').if_parameter('7 Filter On A').has_value('On'),
                          use('7 Resonance A').if_parameter('7 Filter On A').has_value('On'),
                          'Adaptive Q',
                          'Scale',
                          'Output Gain')}),
  (
   'EQ Band 8',
   {BANK_PARAMETERS_KEY: (
                          '8 Filter On A',
                          use('8 Filter Type A').if_parameter('8 Filter On A').has_value('On'),
                          use('8 Frequency A').if_parameter('8 Filter On A').has_value('On'),
                          use('8 Gain A').if_parameter('8 Filter On A').has_value('On'),
                          use('8 Resonance A').if_parameter('8 Filter On A').has_value('On'),
                          'Adaptive Q',
                          'Scale',
                          'Output Gain')}),
  (
   '8 x Frequency',
   {BANK_PARAMETERS_KEY: (
                          use('1 Frequency A').if_parameter('1 Filter On A').has_value('On'),
                          use('2 Frequency A').if_parameter('2 Filter On A').has_value('On'),
                          use('3 Frequency A').if_parameter('3 Filter On A').has_value('On'),
                          use('4 Frequency A').if_parameter('4 Filter On A').has_value('On'),
                          use('5 Frequency A').if_parameter('5 Filter On A').has_value('On'),
                          use('6 Frequency A').if_parameter('6 Filter On A').has_value('On'),
                          use('7 Frequency A').if_parameter('7 Filter On A').has_value('On'),
                          use('8 Frequency A').if_parameter('8 Filter On A').has_value('On'))}),
  (
   '8 x Gain',
   {BANK_PARAMETERS_KEY: (
                          use('').if_parameter('1 Filter On A').has_value('Off').else_use('1 Gain A').if_parameter('1 Filter Type A').has_value('Low Shelf').else_use('1 Gain A').if_parameter('1 Filter Type A').has_value('Bell').else_use('1 Gain A').if_parameter('1 Filter Type A').has_value('High Shelf').else_use(''),
                          use('').if_parameter('2 Filter On A').has_value('Off').else_use('2 Gain A').if_parameter('2 Filter Type A').has_value('Low Shelf').else_use('2 Gain A').if_parameter('2 Filter Type A').has_value('Bell').else_use('2 Gain A').if_parameter('2 Filter Type A').has_value('High Shelf').else_use(''),
                          use('').if_parameter('3 Filter On A').has_value('Off').else_use('3 Gain A').if_parameter('3 Filter Type A').has_value('Low Shelf').else_use('3 Gain A').if_parameter('3 Filter Type A').has_value('Bell').else_use('3 Gain A').if_parameter('3 Filter Type A').has_value('High Shelf').else_use(''),
                          use('').if_parameter('4 Filter On A').has_value('Off').else_use('4 Gain A').if_parameter('4 Filter Type A').has_value('Low Shelf').else_use('4 Gain A').if_parameter('4 Filter Type A').has_value('Bell').else_use('4 Gain A').if_parameter('4 Filter Type A').has_value('High Shelf').else_use(''),
                          use('').if_parameter('5 Filter On A').has_value('Off').else_use('5 Gain A').if_parameter('5 Filter Type A').has_value('Low Shelf').else_use('5 Gain A').if_parameter('5 Filter Type A').has_value('Bell').else_use('5 Gain A').if_parameter('5 Filter Type A').has_value('High Shelf').else_use(''),
                          use('').if_parameter('6 Filter On A').has_value('Off').else_use('6 Gain A').if_parameter('6 Filter Type A').has_value('Low Shelf').else_use('6 Gain A').if_parameter('6 Filter Type A').has_value('Bell').else_use('6 Gain A').if_parameter('6 Filter Type A').has_value('High Shelf').else_use(''),
                          use('').if_parameter('7 Filter On A').has_value('Off').else_use('7 Gain A').if_parameter('7 Filter Type A').has_value('Low Shelf').else_use('7 Gain A').if_parameter('7 Filter Type A').has_value('Bell').else_use('7 Gain A').if_parameter('7 Filter Type A').has_value('High Shelf').else_use(''),
                          use('').if_parameter('8 Filter On A').has_value('Off').else_use('8 Gain A').if_parameter('8 Filter Type A').has_value('Low Shelf').else_use('8 Gain A').if_parameter('8 Filter Type A').has_value('Bell').else_use('8 Gain A').if_parameter('8 Filter Type A').has_value('High Shelf').else_use(''))}),
  (
   '8 x Resonance',
   {BANK_PARAMETERS_KEY: ('1 Resonance A', '2 Resonance A', '3 Resonance A', '4 Resonance A', '5 Resonance A',
 '6 Resonance A', '7 Resonance A', '8 Resonance A')}))), 
 'FilterEQ3':IndexedDict((
  (
   'EQ',
   {BANK_PARAMETERS_KEY: (
                          'LowOn',
                          'MidOn',
                          'HighOn',
                          use('GainLo').if_parameter('LowOn').has_value('On'),
                          use('GainMid').if_parameter('MidOn').has_value('On'),
                          use('GainHi').if_parameter('HighOn').has_value('On'),
                          'FreqLo',
                          'FreqHi')}),
  (
   'Slope', {BANK_PARAMETERS_KEY: ('Slope', '', '', '', '', '', '', '')}))), 
 'Erosion':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Mode',
                          'Frequency',
                          use('').if_parameter('Mode').has_value('Sine').else_use('Width'),
                          'Amount',
                          '',
                          '',
                          '',
                          '')}),)), 
 'ProxyAudioEffectDevice':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Input Gain', 'Output Gain', 'Dry/Wet', '', '', '', '', '')}),)), 
 'FilterDelay':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('2 Filter Freq').if_parameter('2 Input On').has_value('On'),
                          use('2 Filter Width').if_parameter('2 Input On').has_value('On'),
                          use('2 Delay Mode').if_parameter('2 Input On').has_value('On'),
                          use('').if_parameter('2 Input On').has_value('Off').else_use('2 Time Delay').if_parameter('2 Delay Mode').has_value('Off').else_use('2 Beat Delay'),
                          use('2 Feedback').if_parameter('2 Input On').has_value('On'),
                          use('1 Volume').if_parameter('1 Input On').has_value('On').else_use('2 Pan'),
                          use('2 Volume').if_parameter('2 Input On').has_value('On'),
                          use('3 Volume').if_parameter('3 Input On').has_value('On').else_use('Dry'))}),
  (
   'L Filter',
   {BANK_PARAMETERS_KEY: (
                          '1 Input On',
                          use('1 Filter Freq').if_parameter('1 Input On').has_value('On'),
                          use('1 Filter Width').if_parameter('1 Input On').has_value('On'),
                          use('1 Feedback').if_parameter('1 Input On').has_value('On'),
                          use('1 Delay Mode').if_parameter('1 Input On').has_value('On'),
                          use('').if_parameter('1 Input On').has_value('Off').else_use('1 Time Delay').if_parameter('1 Delay Mode').has_value('Off').else_use('1 Beat Delay'),
                          use('').if_parameter('1 Input On').has_value('Off').else_use('1 Beat Swing').if_parameter('1 Delay Mode').has_value('On').else_use(''),
                          use('1 Volume').if_parameter('1 Input On').has_value('Off'))}),
  (
   'L+R Filter',
   {BANK_PARAMETERS_KEY: (
                          '2 Input On',
                          use('2 Filter Freq').if_parameter('2 Input On').has_value('On'),
                          use('2 Filter Width').if_parameter('2 Input On').has_value('On'),
                          use('2 Feedback').if_parameter('2 Input On').has_value('On'),
                          use('2 Delay Mode').if_parameter('2 Input On').has_value('On'),
                          use('').if_parameter('2 Input On').has_value('Off').else_use('2 Time Delay').if_parameter('2 Delay Mode').has_value('Off').else_use('2 Beat Delay'),
                          use('').if_parameter('2 Input On').has_value('Off').else_use('2 Beat Swing').if_parameter('2 Delay Mode').has_value('On').else_use(''),
                          use('2 Volume').if_parameter('2 Input On').has_value('On'))}),
  (
   'R Filter',
   {BANK_PARAMETERS_KEY: (
                          '3 Input On',
                          use('3 Filter Freq').if_parameter('3 Input On').has_value('On'),
                          use('3 Filter Width').if_parameter('3 Input On').has_value('On'),
                          use('3 Feedback').if_parameter('3 Input On').has_value('On'),
                          use('3 Delay Mode').if_parameter('3 Input On').has_value('On'),
                          use('').if_parameter('3 Input On').has_value('Off').else_use('3 Time Delay').if_parameter('3 Delay Mode').has_value('Off').else_use('3 Beat Delay'),
                          use('').if_parameter('3 Input On').has_value('Off').else_use('3 Beat Swing').if_parameter('3 Delay Mode').has_value('On').else_use(''),
                          use('3 Volume').if_parameter('3 Input On').has_value('On'))}),
  (
   'Mix',
   {BANK_PARAMETERS_KEY: (
                          use('1 Pan').if_parameter('1 Input On').has_value('On'),
                          use('2 Pan').if_parameter('2 Input On').has_value('On'),
                          use('3 Pan').if_parameter('3 Input On').has_value('On'),
                          '',
                          use('1 Volume').if_parameter('1 Input On').has_value('On'),
                          use('2 Volume').if_parameter('2 Input On').has_value('On'),
                          use('3 Volume').if_parameter('3 Input On').has_value('On'),
                          'Dry')}))), 
 'Flanger':IndexedDict((
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
                          use('').if_parameter('LFO Waveform').has_value('S&H Width').else_use('LFO Stereo Mode').if_parameter('Sync').has_value('Free').else_use('LFO Offset'),
                          use('LFO Width (Random)').if_parameter('LFO Waveform').has_value('S&H Width').else_use('LFO Phase').if_parameter('Sync').has_value('Sync').else_use('LFO Phase').if_parameter('LFO Stereo Mode').has_value('Phase').else_use('LFO Spin'),
                          '',
                          '')}))), 
 'FrequencyShifter':IndexedDict((
  (
   'FreqDrive',
   {BANK_PARAMETERS_KEY: (
                          'Mode',
                          use('Ring Mod Frequency').if_parameter('Mode').has_value('Ring Modulation').else_use('Coarse'),
                          'Wide',
                          'Fine',
                          use('Drive On/Off').if_parameter('Mode').has_value('Ring Modulation'),
                          use('Drive').if_parameter('Drive On/Off').has_value('On').and_parameter('Mode').has_value('Ring Modulation'),
                          'LFO Amount',
                          'Dry/Wet')}),
  (
   'LFO / S&H',
   {BANK_PARAMETERS_KEY: (
                          'LFO Amount',
                          'LFO Waveform',
                          'Sync',
                          use('LFO Frequency').if_parameter('Sync').has_value('Free').else_use('Sync Rate'),
                          use('').if_parameter('LFO Waveform').has_value('S&H Width').else_use('LFO Stereo Mode').if_parameter('Sync').has_value('Free').else_use('LFO Offset'),
                          use('LFO Width (Random)').if_parameter('LFO Waveform').has_value('S&H Width').else_use('LFO Phase').if_parameter('Sync').has_value('Sync').else_use('LFO Phase').if_parameter('LFO Stereo Mode').has_value('Phase').else_use('LFO Spin'),
                          '',
                          '')}))), 
 'Gate':IndexedDict((
  (
   'Gate',
   {BANK_PARAMETERS_KEY: ('Threshold', 'Return', 'FlipMode', 'LookAhead', 'Attack', 'Hold', 'Release', 'Floor')}),
  (
   'Sidechain',
   {BANK_PARAMETERS_KEY: (
                          'S/C On',
                          use('S/C Gain').if_parameter('S/C On').has_value('On'),
                          use('S/C Mix').if_parameter('S/C On').has_value('On'),
                          'S/C Listen',
                          'S/C EQ On',
                          use('S/C EQ Type').if_parameter('S/C EQ On').has_value('On'),
                          use('S/C EQ Freq').if_parameter('S/C EQ On').has_value('On'),
                          use('').if_parameter('S/C EQ On').has_value('Off').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('Low Shelf').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('High Shelf').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('Bell').else_use('S/C EQ Q'))}))), 
 'GlueCompressor':IndexedDict((
  (
   'Compression',
   {BANK_PARAMETERS_KEY: ('Threshold', 'Ratio', 'Attack', 'Release', 'Peak Clip In', 'Range', 'Makeup', 'Dry/Wet')}),
  (
   'Sidechain',
   {BANK_PARAMETERS_KEY: (
                          'S/C On',
                          use('S/C Gain').if_parameter('S/C On').has_value('On'),
                          use('S/C Mix').if_parameter('S/C On').has_value('On'),
                          '',
                          'S/C EQ On',
                          use('S/C EQ Type').if_parameter('S/C EQ On').has_value('On'),
                          use('S/C EQ Freq').if_parameter('S/C EQ On').has_value('On'),
                          use('').if_parameter('S/C EQ On').has_value('Off').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('Low Shelf').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('High Shelf').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('Bell').else_use('S/C EQ Q'))}))), 
 'GrainDelay':IndexedDict((
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
                          'DryWet')}))), 
 'Hybrid':IndexedDict((
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
                          'Dry/Wet')}))), 
 'Limiter':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Gain',
                          'Ceiling',
                          'Link Channels',
                          'Lookahead',
                          'Auto',
                          use('Release time').if_parameter('Auto').has_value('Off'),
                          '',
                          '')}),)), 
 'Looper':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('State', 'Speed', 'Reverse', 'Quantization', 'Monitor', 'Song Control', 'Tempo Control',
 'Feedback')}),)), 
 'MultibandDynamics':IndexedDict((
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
                          use('Input Gain (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                          use('Below Threshold (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                          use('Below Ratio (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                          use('Above Threshold (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                          use('Above Ratio (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                          use('Attack Time (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                          use('Release Time (Low)').if_parameter('Band Activator (Low)').has_value('On'))}),
  (
   'Mid Band',
   {BANK_PARAMETERS_KEY: (
                          'Band Activator (Mid)',
                          use('Input Gain (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                          use('Below Threshold (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                          use('Below Ratio (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                          use('Above Threshold (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                          use('Above Ratio (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                          use('Attack Time (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                          use('Release Time (Mid)').if_parameter('Band Activator (Mid)').has_value('On'))}),
  (
   'High Band',
   {BANK_PARAMETERS_KEY: (
                          'Band Activator (High)',
                          use('Input Gain (High)').if_parameter('Band Activator (High)').has_value('On'),
                          use('Below Threshold (High)').if_parameter('Band Activator (High)').has_value('On'),
                          use('Below Ratio (High)').if_parameter('Band Activator (High)').has_value('On'),
                          use('Above Threshold (High)').if_parameter('Band Activator (High)').has_value('On'),
                          use('Above Ratio (High)').if_parameter('Band Activator (High)').has_value('On'),
                          use('Attack Time (High)').if_parameter('Band Activator (High)').has_value('On'),
                          use('Release Time (High)').if_parameter('Band Activator (High)').has_value('On'))}),
  (
   'Mix & Split',
   {BANK_PARAMETERS_KEY: (
                          use('Output Gain (Low)').if_parameter('Band Activator (Low)').has_value('On'),
                          'Low-Mid Crossover',
                          use('Output Gain (Mid)').if_parameter('Band Activator (Mid)').has_value('On'),
                          'Mid-High Crossover',
                          use('Output Gain (High)').if_parameter('Band Activator (High)').has_value('On'),
                          'Peak/RMS Mode',
                          'Amount',
                          'Master Output')}),
  (
   'Sidechain',
   {BANK_PARAMETERS_KEY: (
                          'S/C On',
                          use('S/C Mix').if_parameter('S/C On').has_value('On'),
                          use('S/C Gain').if_parameter('S/C On').has_value('On'),
                          '',
                          'Time Scaling',
                          'Soft Knee On/Off',
                          '',
                          '')}))), 
 'Overdrive':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Filter Freq', 'Filter Width', 'Drive', 'Tone', 'Preserve Dynamics', '', '', 'Dry/Wet')}),)), 
 'Pedal':IndexedDict((
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Type', 'Gain', 'Output', 'Bass', 'Mid', 'Treble', 'Sub', 'Dry/Wet')}),
  (
   'EQ',
   {BANK_PARAMETERS_KEY: ('', '', '', 'Bass', 'Mid', 'Treble', '', 'Mid Freq')}))), 
 'Phaser':IndexedDict((
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
   {BANK_PARAMETERS_KEY: (
                          'Poles',
                          'Type',
                          use('').if_parameter('Type').has_value('Space').else_use('Color'),
                          'Frequency',
                          'Feedback',
                          'Env. Modulation',
                          'Env. Attack',
                          'Env. Release')}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          'LFO Amount',
                          'LFO Waveform',
                          'LFO Sync',
                          use('LFO Frequency').if_parameter('LFO Sync').has_value('Free').else_use('LFO Sync Rate'),
                          use('').if_parameter('LFO Waveform').has_value('S&H Width').else_use('LFO Stereo Mode').if_parameter('LFO Sync').has_value('Free').else_use('LFO Offset'),
                          use('LFO Width (Random)').if_parameter('LFO Waveform').has_value('S&H Width').else_use('LFO Phase').if_parameter('LFO Sync').has_value('Sync').else_use('LFO Phase').if_parameter('LFO Stereo Mode').has_value('Phase').else_use('LFO Spin'),
                          '',
                          '')}))), 
 'PhaserNew':IndexedDict((
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
                          'Dry/Wet')}))), 
 'Redux':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Bit On',
                          use('Bit Depth').if_parameter('Bit On').has_value('On'),
                          'Sample Mode',
                          use('Sample Hard').if_parameter('Sample Mode').has_value('Hard').else_use('Sample Soft'),
                          '',
                          '',
                          '',
                          '')}),)), 
 'Redux2':IndexedDict((
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
                          'Dry/Wet')}),)), 
 'Resonator':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('Frequency').if_parameter('Filter On').has_value('On'),
                          'Decay',
                          'Color',
                          use('I Gain').if_parameter('I On').has_value('On'),
                          use('II Gain').if_parameter('II On').has_value('On'),
                          use('III Gain').if_parameter('III On').has_value('On'),
                          'Width',
                          'Dry/Wet')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Mode', 'Decay', 'Const', 'Color', '', 'Width', 'Global Gain', 'Dry/Wet')}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: (
                          'Filter On',
                          use('Frequency').if_parameter('Filter On').has_value('On'),
                          use('Filter Type').if_parameter('Filter On').has_value('On'),
                          '',
                          '',
                          '',
                          '',
                          '')}),
  (
   'Mode I & II',
   {BANK_PARAMETERS_KEY: (
                          'I On',
                          use('I Note').if_parameter('I On').has_value('On'),
                          use('I Tune').if_parameter('I On').has_value('On'),
                          use('I Gain').if_parameter('I On').has_value('On'),
                          'II On',
                          use('II Pitch').if_parameter('II On').has_value('On'),
                          use('II Tune').if_parameter('II On').has_value('On'),
                          use('II Gain').if_parameter('II On').has_value('On'))}),
  (
   'Mode III & IV',
   {BANK_PARAMETERS_KEY: (
                          'III On',
                          use('III Pitch').if_parameter('III On').has_value('On'),
                          use('III Tune').if_parameter('III On').has_value('On'),
                          use('III Gain').if_parameter('III On').has_value('On'),
                          'IV On',
                          use('IV Pitch').if_parameter('IV On').has_value('On'),
                          use('IV Tune').if_parameter('IV On').has_value('On'),
                          use('IV Gain').if_parameter('IV On').has_value('On'))}),
  (
   'Mode V',
   {BANK_PARAMETERS_KEY: (
                          'V On',
                          use('V Pitch').if_parameter('V On').has_value('On'),
                          use('V Tune').if_parameter('V On').has_value('On'),
                          use('V Gain').if_parameter('V On').has_value('On'),
                          '',
                          '',
                          '',
                          '')}),
  (
   'Mix',
   {BANK_PARAMETERS_KEY: (
                          use('I Gain').if_parameter('I On').has_value('On'),
                          use('II Gain').if_parameter('II On').has_value('On'),
                          use('III Gain').if_parameter('III On').has_value('On'),
                          use('IV Gain').if_parameter('IV On').has_value('On'),
                          use('V Gain').if_parameter('V On').has_value('On'),
                          '',
                          '',
                          '')}),
  (
   'Pitch',
   {BANK_PARAMETERS_KEY: (
                          use('I Note').if_parameter('I On').has_value('On'),
                          use('II Pitch').if_parameter('II On').has_value('On'),
                          use('III Pitch').if_parameter('III On').has_value('On'),
                          use('IV Pitch').if_parameter('IV On').has_value('On'),
                          use('V Pitch').if_parameter('V On').has_value('On'),
                          '',
                          '',
                          '')}))), 
 'Reverb':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Predelay',
                          use('In Filter Freq').if_parameter('In LowCut On').has_value('On').else_use('ER Shape').if_parameter('In HighCut On').has_value('Off').else_use('In Filter Freq'),
                          use('Chorus Amount').if_parameter('Chorus On').has_value('On').else_use('Reflect Level'),
                          'Stereo Image',
                          'Room Size',
                          'Decay Time',
                          use('HiShelf Gain').if_parameter('HiFilter On').has_value('On').else_use('Diffuse Level'),
                          'Dry/Wet')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: (
                          'Chorus On',
                          use('Chorus Rate').if_parameter('Chorus On').has_value('On'),
                          use('Chorus Amount').if_parameter('Chorus On').has_value('On'),
                          'Density',
                          'Freeze On',
                          'Flat On',
                          'Reflect Level',
                          'Diffuse Level')}),
  (
   'Diffusion Network',
   {BANK_PARAMETERS_KEY: (
                          'HiFilter On',
                          use('HiFilter Freq').if_parameter('HiFilter On').has_value('On'),
                          use('HiShelf Gain').if_parameter('HiFilter On').has_value('On'),
                          'LowShelf On',
                          use('LowShelf Freq').if_parameter('LowShelf On').has_value('On'),
                          use('LowShelf Gain').if_parameter('LowShelf On').has_value('On'),
                          'Diffusion',
                          'Scale')}),
  (
   'Input/Reflections',
   {BANK_PARAMETERS_KEY: (
                          'In LowCut On',
                          'In HighCut On',
                          use('In Filter Freq').if_parameter('In LowCut On').has_value('On').else_use('').if_parameter('In HighCut On').has_value('Off').else_use('In Filter Freq'),
                          use('In Filter Width').if_parameter('In LowCut On').has_value('On').else_use('').if_parameter('In HighCut On').has_value('Off').else_use('In Filter Width'),
                          'ER Spin On',
                          use('ER Spin Rate').if_parameter('ER Spin On').has_value('On'),
                          use('ER Spin Amount').if_parameter('ER Spin On').has_value('On'),
                          'ER Shape')}))), 
 'Saturator':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Drive',
                          'Type',
                          'Color',
                          use('Base').if_parameter('Color').has_value('On'),
                          use('Frequency').if_parameter('Color').has_value('On'),
                          use('Width').if_parameter('Color').has_value('On'),
                          use('Depth').if_parameter('Color').has_value('On'),
                          'Output')}),
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
   {BANK_PARAMETERS_KEY: ('', '', '', '', '', 'Soft Clip', 'Output', 'Dry/Wet')}))), 
 'StereoGain':IndexedDict((
  (
   'Utility',
   {BANK_PARAMETERS_KEY: (
                          use('').if_parameter('Channel Mode').has_value('Right').else_use('Left Inv').if_parameter('Mute').has_value('Off'),
                          use('').if_parameter('Channel Mode').has_value('Left').else_use('Right Inv').if_parameter('Mute').has_value('Off'),
                          use('Channel Mode').if_parameter('Mute').has_value('Off'),
                          use('').if_parameter('Mute').has_value('On').else_use('').if_parameter('Channel Mode').has_value('Left').else_use('').if_parameter('Channel Mode').has_value('Right').else_use('').if_parameter('Mono').is_available(True).and_parameter('Mono').has_value('On').else_use('Stereo Width').if_parameter('Stereo Width').is_available(True).else_use('Mid/Side Balance'),
                          use('').if_parameter('Mute').has_value('On').else_use('').if_parameter('Channel Mode').has_value('Left').else_use('').if_parameter('Channel Mode').has_value('Right').else_use('Mono'),
                          use('Balance').if_parameter('Mute').has_value('Off'),
                          use('').if_parameter('Mute').has_value('On').else_use('Gain').if_parameter('Gain').is_available(True).else_use('Gain (Legacy)'),
                          'Mute')}),
  (
   'Low Freq',
   {BANK_PARAMETERS_KEY: (
                          use('').if_parameter('Mute').has_value('On').else_use('').if_parameter('Channel Mode').has_value('Left').else_use('').if_parameter('Channel Mode').has_value('Right').else_use('').if_parameter('Mono').is_available(True).and_parameter('Mono').has_value('On').else_use('Bass Mono').if_parameter('Bass Mono').is_available(True),
                          use('').if_parameter('Mute').has_value('On').else_use('').if_parameter('Channel Mode').has_value('Left').else_use('').if_parameter('Channel Mode').has_value('Right').else_use('').if_parameter('Mono').is_available(True).and_parameter('Mono').has_value('On').else_use('Bass Freq').if_parameter('Bass Freq').is_available(True),
                          '',
                          use('DC Filter').if_parameter('Mute').has_value('Off'),
                          '',
                          '',
                          '',
                          '')}))), 
 'Vinyl':IndexedDict((
  (
   'Global',
   {BANK_PARAMETERS_KEY: (
                          'Tracing On',
                          use('Tracing Drive').if_parameter('Tracing On').has_value('On'),
                          use('Tracing Freq.').if_parameter('Tracing On').has_value('On'),
                          use('Tracing Width').if_parameter('Tracing On').has_value('On'),
                          'Pinch On',
                          'Global Drive',
                          'Crackle Density',
                          'Crackle Volume')}),
  (
   'Pinch',
   {BANK_PARAMETERS_KEY: (
                          'Pinch On',
                          use('Pinch Soft On').if_parameter('Pinch On').has_value('On'),
                          use('Pinch Mono On').if_parameter('Pinch On').has_value('On'),
                          use('Pinch Width').if_parameter('Pinch On').has_value('On'),
                          use('Pinch Drive').if_parameter('Pinch On').has_value('On'),
                          use('Pinch Freq.').if_parameter('Pinch On').has_value('On'),
                          'Crackle Density',
                          'Crackle Volume')}))), 
 'Vocoder':IndexedDict((
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
 'Unvoiced Sensitivity', 'Unvoiced Speed', 'Enhance')})))}
PARAMETERS_BLACKLIST_FOR_CPP_SANITY_CHECK = {
  'OriginalSimpler': ('Start', 'End', 'Sensitivity', 'Mode', 'Playback', 'Pad Slicing', 'Multi Sample', 'Warp', 'Warp Mode', 'Voices', 'Preserve', 'Loop Mode', 'Envelope', 'Grain Size Tones', 'Grain Size Texture', 'Flux', 'Formants', 'Envelope Complex Pro', 'Gain'),
  'InstrumentVector': ('Osc 1 Effect Type', 'Osc 2 Effect Type', 'Osc 1 Table', 'Osc 2 Table', 'Osc 1 Category', 'Osc 2 Category', 'Osc 1 Pitch', 'Osc 2 Pitch', 'Unison Mode', 'Mono On'),
  'Delay': ('L Sync Enum', 'R Sync Enum'),
  'Drift': ('Voice Mode', 'Voice Count', 'LP Mod Src 1', 'LP Mod Src 2')}