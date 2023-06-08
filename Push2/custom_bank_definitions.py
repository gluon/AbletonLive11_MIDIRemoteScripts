<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/custom_bank_definitions.py
# Compiled at: 2022-01-28 05:06:23
# Size of source mod 2**32: 344428 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base.collection import IndexedDict
from ableton.v2.control_surface import BANK_MAIN_KEY, BANK_PARAMETERS_KEY, use
OPTIONS_KEY = 'Options'
VIEW_DESCRIPTION_KEY = 'view_description'
RACK_BANKS = IndexedDict((
 (
  'Macros',
  {BANK_PARAMETERS_KEY: ('Macro 1', 'Macro 2', 'Macro 3', 'Macro 4', 'Macro 5', 'Macro 6', 'Macro 7', 'Macro 8')}),))
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
<<<<<<< HEAD
                          use('F1 Freq').with_name('F1 Frequency').if_parameter('F1 On/Off').has_value('On').else_use('F2 Freq').with_name('F2 Frequency').if_parameter('F2 On/Off').has_value('On'),
=======
                          use('F1 Freq').if_parameter('F1 On/Off').has_value('On').else_use('F2 Freq').if_parameter('F2 On/Off').has_value('On'),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          use('F1 Resonance').if_parameter('F1 On/Off').has_value('On').else_use('F2 Resonance').if_parameter('F2 On/Off').has_value('On'),
                          'Volume')}),
  (
   'Osc. 1 Shape',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('OSC1 On/Off').with_name('Oscillator 1'),
                          use('OSC1 Shape').with_name('Shape').if_parameter('OSC1 On/Off').has_value('On'),
                          use('').if_parameter('OSC1 On/Off').has_value('Off').else_use('OSC1 PW').with_name('Pulse Width').if_parameter('OSC1 Shape').has_value('Rect'),
                          use('').if_parameter('OSC1 On/Off').has_value('Off').else_use('O1 PW < LFO').with_name('LFO → PW').if_parameter('OSC1 Shape').has_value('Rect').else_use('').if_parameter('LFO1 On/Off').has_value('Off'),
                          use('').if_parameter('OSC1 On/Off').has_value('Off').else_use('').if_parameter('OSC1 Shape').has_value('Noise').else_use('').if_parameter('OSC1 Shape').has_value('Sine').else_use('OSC1 Mode').with_name('Mode'),
                          use('').if_parameter('OSC1 On/Off').has_value('Off').else_use('').if_parameter('OSC1 Shape').has_value('Noise').else_use('O1 Sub/Sync').with_name('Sub/Sync'),
                          use('OSC1 Balance').with_name('Balance').if_parameter('OSC1 On/Off').has_value('On'),
                          use('OSC1 Level').with_name('Level').if_parameter('OSC1 On/Off').has_value('On'))}),
  (
   'Osc. 1 Pitch',
   {BANK_PARAMETERS_KEY: (
                          use('OSC1 On/Off').with_name('Oscillator 1'),
                          use('OSC1 Octave').with_name('Octave').if_parameter('OSC1 On/Off').has_value('On'),
                          use('OSC1 Semi').with_name('Semi').if_parameter('OSC1 On/Off').has_value('On'),
                          use('OSC1 Detune').with_name('Detune').if_parameter('OSC1 On/Off').has_value('On'),
                          use('PEG1 Amount').with_name('Env 1 Amount').if_parameter('OSC1 On/Off').has_value('On'),
                          use('PEG1 Time').with_name('Env 1 Time').if_parameter('OSC1 On/Off').has_value('On'),
                          use('O1 Keytrack').with_name('Keytracking').if_parameter('OSC1 On/Off').has_value('On'),
                          use('').if_parameter('OSC1 On/Off').has_value('Off').else_use('').if_parameter('LFO1 On/Off').has_value('Off').else_use('OSC1 < LFO').with_name('LFO → Osc 1'))}),
  (
   'Osc. 2 Shape',
   {BANK_PARAMETERS_KEY: (
                          use('OSC2 On/Off').with_name('Oscillator 2'),
                          use('OSC2 Shape').with_name('Shape').if_parameter('OSC2 On/Off').has_value('On'),
                          use('').if_parameter('OSC2 On/Off').has_value('Off').else_use('OSC2 PW').with_name('Pulse Width').if_parameter('OSC2 Shape').has_value('Rect'),
                          use('').if_parameter('OSC2 On/Off').has_value('Off').else_use('O2 PW < LFO').with_name('LFO → PW').if_parameter('OSC2 Shape').has_value('Rect').else_use('').if_parameter('LFO2 On/Off').has_value('Off'),
                          use('').if_parameter('OSC2 On/Off').has_value('Off').else_use('').if_parameter('OSC2 Shape').has_value('Noise').else_use('').if_parameter('OSC2 Shape').has_value('Sine').else_use('OSC2 Mode').with_name('Mode'),
                          use('').if_parameter('OSC2 On/Off').has_value('Off').else_use('').if_parameter('OSC2 Shape').has_value('Noise').else_use('O2 Sub/Sync').with_name('Sub/Sync'),
                          use('OSC2 Balance').with_name('Balance').if_parameter('OSC2 On/Off').has_value('On'),
                          use('OSC2 Level').with_name('Level').if_parameter('OSC2 On/Off').has_value('On'))}),
  (
   'Osc. 2 Pitch',
   {BANK_PARAMETERS_KEY: (
                          use('OSC2 On/Off').with_name('Oscillator 2'),
                          use('OSC2 Octave').with_name('Octave').if_parameter('OSC2 On/Off').has_value('On'),
                          use('OSC2 Semi').with_name('Semi').if_parameter('OSC2 On/Off').has_value('On'),
                          use('OSC2 Detune').with_name('Detune').if_parameter('OSC2 On/Off').has_value('On'),
                          use('PEG2 Amount').with_name('Env 2 Amount').if_parameter('OSC2 On/Off').has_value('On'),
                          use('PEG2 Time').with_name('Env 2 Time').if_parameter('OSC2 On/Off').has_value('On'),
                          use('O2 Keytrack').with_name('Keytracking').if_parameter('OSC2 On/Off').has_value('On'),
                          use('').if_parameter('OSC2 On/Off').has_value('Off').else_use('').if_parameter('LFO2 On/Off').has_value('Off').else_use('OSC2 < LFO').with_name('LFO → Osc 2'))}),
  (
   'Filter 1',
   {BANK_PARAMETERS_KEY: (
                          use('F1 On/Off').with_name('Filter 1'),
                          use('F1 Type').if_parameter('F1 On/Off').has_value('On'),
                          use('F1 Freq').if_parameter('F1 On/Off').has_value('On'),
                          use('F1 Resonance').with_name('Resonance').if_parameter('F1 On/Off').has_value('On'),
                          use('F1 Freq < LFO').with_name('LFO → Freq').if_parameter('F1 On/Off').has_value('On'),
                          use('F1 Freq < Env').with_name('Env → Freq').if_parameter('F1 On/Off').has_value('On'),
                          use('F1 Res < LFO').with_name('LFO → Res').if_parameter('F1 On/Off').has_value('On'),
                          '')}),
  (
   'Filt. 1 Env.',
   {BANK_PARAMETERS_KEY: (
                          use('F1 On/Off').with_name('Filter 1'),
                          use('FEG1 < Vel').with_name('Vel → Env').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 A < Vel').with_name('Vel → Attack').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Attack').with_name('Attack').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Decay').with_name('Decay').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Sustain').with_name('Sustain').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 S Time').with_name('Sustain Time').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Rel').with_name('Release').if_parameter('F1 On/Off').has_value('On'))}),
  (
   'Filter 2',
   {BANK_PARAMETERS_KEY: (
                          use('F2 On/Off').with_name('Filter 2'),
                          use('F2 Type').if_parameter('F2 On/Off').has_value('On'),
                          use('F2 Freq').if_parameter('F2 On/Off').has_value('On'),
                          use('F2 Resonance').if_parameter('F2 On/Off').has_value('On'),
                          use('F2 Freq < LFO').with_name('LFO → Freq').if_parameter('F2 On/Off').has_value('On'),
                          use('F2 Freq < Env').with_name('Env → Freq').if_parameter('F2 On/Off').has_value('On'),
                          use('F2 Res < LFO').with_name('LFO → Res').if_parameter('F2 On/Off').has_value('On'),
                          '')}),
  (
   'Filt. 2 Env.',
   {BANK_PARAMETERS_KEY: (
                          use('F2 On/Off').with_name('Filter 2'),
                          use('FEG2 < Vel').with_name('Vel → Env').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 A < Vel').with_name('Vel → Attack').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Attack').with_name('Attack').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Decay').with_name('Decay').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Sustain').with_name('Sustain').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 S Time').with_name('Sustain Time').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Rel').with_name('Release').if_parameter('F2 On/Off').has_value('On'))}),
  (
   'Amp',
   {BANK_PARAMETERS_KEY: (
                          use('AMP1 Level').with_name('Amp 1 Level').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AMP1 Pan').with_name('Amp 1 Pan').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AMP1 < LFO').if_parameter('AMP1 On/Off').has_value('On'),
                          use('').if_parameter('LFO1 On/Off').has_value('Off').else_use('LFO1 Speed').with_name('LFO 1 Speed').if_parameter('LFO1 Sync').has_value('Hertz').else_use('LFO1 SncRate').with_name('LFO 1 Sync Rate'),
                          use('AMP2 Level').with_name('Amp 2 Level').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AMP2 Pan').with_name('Amp 2 Pan').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AMP2 < LFO').if_parameter('AMP2 On/Off').has_value('On'),
                          use('').if_parameter('LFO2 On/Off').has_value('Off').else_use('LFO2 Speed').with_name('LFO 2 Speed').if_parameter('LFO2 Sync').has_value('Hertz').else_use('LFO2 SncRate').with_name('LFO 2 Sync Rate'))}),
  (
   'Amp 1 Envelope',
   {BANK_PARAMETERS_KEY: (
                          use('AMP1 On/Off').with_name('Amp 1'),
                          use('AEG1 < Vel').with_name('Vel → Env').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 A < Vel').with_name('Vel → Attack').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Attack').with_name('Attack').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Decay').with_name('Decay').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Sustain').with_name('Sustain').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 S Time').with_name('Sustain Time').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Rel').with_name('Release').if_parameter('AMP1 On/Off').has_value('On'))}),
  (
   'Amp 2 Envelope',
   {BANK_PARAMETERS_KEY: (
                          use('AMP2 On/Off').with_name('Amp 2'),
                          use('AEG2 < Vel').with_name('Vel → Env').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 A < Vel').with_name('Vel → Attack').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Attack').with_name('Attack').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Decay').with_name('Decay').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Sustain').with_name('Sustain').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 S Time').with_name('Sustain Time').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Rel').with_name('Release').if_parameter('AMP2 On/Off').has_value('On'))}),
  (
   'Noise & Unison',
   {BANK_PARAMETERS_KEY: (
                          use('Noise On/Off').with_name('Noise'),
                          use('Noise Level').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Color').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Balance').if_parameter('Noise On/Off').has_value('On'),
                          use('Unison On/Off').with_name('Unison'),
=======
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
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          use('Unison Detune').if_parameter('Unison On/Off').has_value('On'),
                          use('Unison Voices').if_parameter('Unison On/Off').has_value('On'),
                          use('Unison Delay').if_parameter('Unison On/Off').has_value('On'))}),
  (
   'LFO 1',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('LFO1 On/Off').with_name('LFO 1'),
                          use('LFO1 Sync').with_name('Sync').if_parameter('LFO1 On/Off').has_value('On'),
                          use('').if_parameter('LFO1 On/Off').has_value('Off').else_use('LFO1 Speed').with_name('Speed').if_parameter('LFO1 Sync').has_value('Hertz').else_use('LFO1 SncRate').with_name('Sync Rate'),
                          use('LFO1 Shape').with_name('Shape').if_parameter('LFO1 On/Off').has_value('On'),
                          use('').if_parameter('LFO1 On/Off').has_value('Off').else_use('LFO1 PW').with_name('Pulse Width').if_parameter('LFO1 Shape').has_value('Rect').else_use('LFO1 PW').with_name('Pulse Width').if_parameter('LFO1 Shape').has_value('Tri'),
                          use('LFO1 Phase').with_name('Phase').if_parameter('LFO1 On/Off').has_value('On'),
                          use('LFO1 Delay').with_name('Delay').if_parameter('LFO1 On/Off').has_value('On'),
                          use('LFO1 Fade In').with_name('Fade In').if_parameter('LFO1 On/Off').has_value('On'))}),
  (
   'LFO 2',
   {BANK_PARAMETERS_KEY: (
                          use('LFO2 On/Off').with_name('LFO 2'),
                          use('LFO2 Sync').with_name('Sync').if_parameter('LFO2 On/Off').has_value('On'),
                          use('').if_parameter('LFO2 On/Off').has_value('Off').else_use('LFO2 Speed').with_name('Speed').if_parameter('LFO2 Sync').has_value('Hertz').else_use('LFO2 SncRate').with_name('Sync Rate'),
                          use('LFO2 Shape').with_name('Shape').if_parameter('LFO2 On/Off').has_value('On'),
                          use('').if_parameter('LFO2 On/Off').has_value('Off').else_use('LFO2 PW').with_name('Pulse Width').if_parameter('LFO2 Shape').has_value('Rect').else_use('LFO2 PW').with_name('Pulse Width').if_parameter('LFO2 Shape').has_value('Tri'),
                          use('LFO2 Phase').with_name('Phase').if_parameter('LFO2 On/Off').has_value('On'),
                          use('LFO2 Delay').with_name('Delay').if_parameter('LFO2 On/Off').has_value('On'),
                          use('LFO2 Fade In').with_name('Fade In').if_parameter('LFO2 On/Off').has_value('On'))}),
  (
   'Glide',
   {BANK_PARAMETERS_KEY: (
                          use('Glide On/Off').with_name('Glide'),
                          use('Glide Time').with_name('Time').if_parameter('Glide On/Off').has_value('On'),
                          use('Glide Mode').with_name('Mode').if_parameter('Glide On/Off').has_value('On'),
                          use('Glide Legato').with_name('Legato').if_parameter('Glide On/Off').has_value('On'),
=======
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
   'Glide',
   {BANK_PARAMETERS_KEY: (
                          'Glide On/Off',
                          use('Glide Time').if_parameter('Glide On/Off').has_value('On'),
                          use('Glide Mode').if_parameter('Glide On/Off').has_value('On'),
                          use('Glide Legato').if_parameter('Glide On/Off').has_value('On'),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          '',
                          '',
                          '',
                          '')}),
  (
   'Keyboard',
   {BANK_PARAMETERS_KEY: ('Octave', 'Semitone', 'Detune', 'PB Range', 'Key Stretch', 'Key Error', 'Key Priority',
 'Voices')}),
  (
   'Vibrato',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('Vib On/Off').with_name('Vibrato'),
                          use('Vib Amount').with_name('Amount').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib Speed').with_name('Speed').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib Delay').with_name('Delay').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib Fade-In').with_name('Fade-in').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib Error').with_name('Error').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib < ModWh').with_name('Mod → Vibrato').if_parameter('Vib On/Off').has_value('On'),
=======
                          'Vib On/Off',
                          use('Vib Amount').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib Speed').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib Delay').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib Fade-In').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib Error').if_parameter('Vib On/Off').has_value('On'),
                          use('Vib < ModWh').if_parameter('Vib On/Off').has_value('On'),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          '')}),
  (
   'Filt. 1 Other',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('F1 On/Off').with_name('Filter 1'),
                          use('FEG1 Exp').with_name('Exp Slope').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Legato').with_name('Legato Mode').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Free').with_name('Free Run Mode').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Loop').with_name('Env Loop Mode').if_parameter('F1 On/Off').has_value('On'),
                          use('F1 Drive').with_name('Drive').if_parameter('F1 On/Off').has_value('On'),
=======
                          'F1 On/Off',
                          use('FEG1 Exp').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Legato').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Free').if_parameter('F1 On/Off').has_value('On'),
                          use('FEG1 Loop').if_parameter('F1 On/Off').has_value('On'),
                          use('F1 Drive').if_parameter('F1 On/Off').has_value('On'),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          '',
                          '')}),
  (
   'Filt. 2 Other',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('F2 On/Off').with_name('Filter 2'),
                          use('FEG2 Exp').with_name('Exp Slope').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Legato').with_name('Legato Mode').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Free').with_name('Free Run Mode').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Loop').with_name('Env Loop Mode').if_parameter('F2 On/Off').has_value('On'),
                          use('F2 Drive').with_name('Drive').if_parameter('F2 On/Off').has_value('On'),
=======
                          'F2 On/Off',
                          use('FEG2 Exp').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Legato').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Free').if_parameter('F2 On/Off').has_value('On'),
                          use('FEG2 Loop').if_parameter('F2 On/Off').has_value('On'),
                          use('F2 Drive').if_parameter('F2 On/Off').has_value('On'),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          '',
                          '')}),
  (
   'Amp 1 Other',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('AMP1 On/Off').with_name('Amp 1'),
                          use('AEG1 Exp').with_name('Exp Slope').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Legato').with_name('Legato Mode').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Free').with_name('Free Run Mode').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Loop').with_name('Env Loop Mode').if_parameter('AMP1 On/Off').has_value('On'),
                          use('A1 Pan < LFO').with_name('LFO → Pan').if_parameter('AMP1 On/Off').has_value('On'),
                          use('A1 Pan < Key').with_name('Pitch → Pan').if_parameter('AMP1 On/Off').has_value('On'),
                          use('A1 Pan < Env').with_name('Env → Pan').if_parameter('AMP1 On/Off').has_value('On'))}),
  (
   'Amp 2 Other',
   {BANK_PARAMETERS_KEY: (
                          use('AMP2 On/Off').with_name('Amp 2'),
                          use('AEG2 Exp').with_name('Exp Slope').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Legato').with_name('Legato Mode').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Free').with_name('Free Run Mode').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Loop').with_name('Env Loop Mode').if_parameter('AMP2 On/Off').has_value('On'),
                          use('A2 Pan < LFO').with_name('LFO → Pan').if_parameter('AMP2 On/Off').has_value('On'),
                          use('A2 Pan < Key').with_name('Pitch → Pan').if_parameter('AMP2 On/Off').has_value('On'),
                          use('A2 Pan < Env').with_name('Env → Pan').if_parameter('AMP2 On/Off').has_value('On'))}))), 
=======
                          'AMP1 On/Off',
                          use('AEG1 Exp').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Legato').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Free').if_parameter('AMP1 On/Off').has_value('On'),
                          use('AEG1 Loop').if_parameter('AMP1 On/Off').has_value('On'),
                          use('A1 Pan < LFO').if_parameter('AMP1 On/Off').has_value('On'),
                          use('A1 Pan < Key').if_parameter('AMP1 On/Off').has_value('On'),
                          use('A1 Pan < Env').if_parameter('AMP1 On/Off').has_value('On'))}),
  (
   'Amp 2 Other',
   {BANK_PARAMETERS_KEY: (
                          'AMP2 On/Off',
                          use('AEG2 Exp').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Legato').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Free').if_parameter('AMP2 On/Off').has_value('On'),
                          use('AEG2 Loop').if_parameter('AMP2 On/Off').has_value('On'),
                          use('A2 Pan < LFO').if_parameter('AMP2 On/Off').has_value('On'),
                          use('A2 Pan < Key').if_parameter('AMP2 On/Off').has_value('On'),
                          use('A2 Pan < Env').if_parameter('AMP2 On/Off').has_value('On'))}))), 
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
 'ChannelEq':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Highpass On',
                          use('Low Gain').with_name('Low'),
                          use('Mid Gain').with_name('Mid'),
                          'Mid Freq',
                          use('High Gain').with_name('High'),
                          '',
                          '',
                          use('Gain').with_name('Output'))}),)), 
 'Collision':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('Res 1 Type').if_parameter('Res 1 On/Off').has_value('On'),
<<<<<<< HEAD
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Brightness').with_name('Brightness'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Opening').with_name('Opening').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Inharmonics').with_name('Inharmonics'),
                          use('Res 1 Decay').with_name('Decay').if_parameter('Res 1 On/Off').has_value('On'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('Res 1 Radius').with_name('Radius').if_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Radius').with_name('Radius').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Material').with_name('Material'),
                          use('Mallet Stiffness').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Amount').with_name('Mallet Noise').if_parameter('Mallet On/Off').has_value('On'),
=======
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Brightness'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Opening').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Inharmonics'),
                          use('Res 1 Decay').if_parameter('Res 1 On/Off').has_value('On'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('Res 1 Radius').if_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Radius').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Material'),
                          use('Mallet Stiffness').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Amount').if_parameter('Mallet On/Off').has_value('On'),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
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
<<<<<<< HEAD
                          use('Mallet On/Off').with_name('Mallet'),
                          use('Mallet Volume').with_name('Volume').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Amount').with_name('Noise Amount').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Stiffness').with_name('Stiffness').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Color').with_name('Noise Color').if_parameter('Mallet On/Off').has_value('On'),
                          '',
                          use('Mallet Volume < Vel').with_name('Vel → Volume').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Amount < Vel').with_name('Vel → Noise').if_parameter('Mallet On/Off').has_value('On'))}),
  (
   'Noise Envelope',
   {BANK_PARAMETERS_KEY: (
                          use('Noise On/Off').with_name('Noise'),
                          use('Noise Volume').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Volume < Key').with_name('Pitch → Noise').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Volume < Vel').with_name('Vel → Noise').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Attack').with_name('Attack').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Decay').with_name('Decay').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Sustain').with_name('Sustain').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Release').with_name('Release').if_parameter('Noise On/Off').has_value('On'))}),
  (
   'Noise Filter',
   {BANK_PARAMETERS_KEY: (
                          use('Noise On/Off').with_name('Noise'),
                          use('Noise Volume').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Filter Type').with_name('Type').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Filter Freq').with_name('Frequency').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Filter Q').with_name('Resonance').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Freq < Key').with_name('Pitch → Freq').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Freq < Vel').with_name('Vel → Freq').if_parameter('Noise On/Off').has_value('On'),
                          use('Noise Freq < Env').with_name('Env → Freq').if_parameter('Noise On/Off').has_value('On'))}),
  (
   'Res. 1 Body',
   {BANK_PARAMETERS_KEY: (
                          use('Res 1 On/Off').with_name('Resonator 1'),
                          use('Res 1 Type').with_name('Type').if_parameter('Res 1 On/Off').has_value('On'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('Res 1 Ratio').with_name('Ratio').if_parameter('Res 1 Type').has_value('Plate').else_use('Res 1 Ratio').with_name('Ratio').if_parameter('Res 1 Type').has_value('Membrane'),
                          use('Res 1 Decay').with_name('Decay').if_parameter('Res 1 On/Off').has_value('On'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('Res 1 Radius').with_name('Radius').if_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Radius').with_name('Radius').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Material').with_name('Material'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Listening L').with_name('Listening L'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Listening R').with_name('Listening R'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Hit').with_name('Hit'))}),
  (
   'Res. 1 Tune',
   {BANK_PARAMETERS_KEY: (
                          use('Res 1 On/Off').with_name('Resonator 1'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Brightness').with_name('Brightness'),
                          use('Res 1 Quality').with_name('Quality').if_parameter('Res 1 On/Off').has_value('On'),
                          use('').if_parameter('Res 1 On/Off').has_value('Off').else_use('').if_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Opening').with_name('Opening').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Inharmonics').with_name('Inharmonics'),
                          use('Res 1 Tune').with_name('Tune').if_parameter('Res 1 On/Off').has_value('On'),
                          use('Res 1 Fine Tune').with_name('Fine Tune').if_parameter('Res 1 On/Off').has_value('On'),
                          use('Res 1 Pitch Env.').with_name('Pitch Envelope').if_parameter('Res 1 On/Off').has_value('On'),
                          use('Res 1 Pitch Env. Time').with_name('Pitch Env Time').if_parameter('Res 1 On/Off').has_value('On'))}),
  (
   'Res. 2 Body',
   {BANK_PARAMETERS_KEY: (
                          use('Res 2 On/Off').with_name('Resonator 2'),
                          use('Res 2 Type').with_name('Type').if_parameter('Res 2 On/Off').has_value('On'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('Res 2 Ratio').with_name('Ratio').if_parameter('Res 2 Type').has_value('Plate').else_use('Res 2 Ratio').with_name('Ratio').if_parameter('Res 2 Type').has_value('Membrane'),
                          use('Res 2 Decay').with_name('Decay').if_parameter('Res 2 On/Off').has_value('On'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('Res 2 Radius').with_name('Radius').if_parameter('Res 2 Type').has_value('Tube').else_use('Res 2 Radius').with_name('Radius').if_parameter('Res 2 Type').has_value('Pipe').else_use('Res 2 Material').with_name('Material'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('').if_parameter('Res 2 Type').has_value('Tube').else_use('').if_parameter('Res 2 Type').has_value('Pipe').else_use('Res 2 Listening L').with_name('Listening L'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('').if_parameter('Res 2 Type').has_value('Tube').else_use('').if_parameter('Res 2 Type').has_value('Pipe').else_use('Res 2 Listening R').with_name('Listening R'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('').if_parameter('Res 2 Type').has_value('Tube').else_use('').if_parameter('Res 2 Type').has_value('Pipe').else_use('Res 2 Hit').with_name('Hit'))}),
  (
   'Res. 2 Tune',
   {BANK_PARAMETERS_KEY: (
                          use('Res 2 On/Off').with_name('Resonator 2'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('').if_parameter('Res 2 Type').has_value('Tube').else_use('').if_parameter('Res 2 Type').has_value('Pipe').else_use('Res 2 Brightness').with_name('Brightness'),
                          use('Res 2 Quality').with_name('Quality').if_parameter('Res 2 On/Off').has_value('On'),
                          use('').if_parameter('Res 2 On/Off').has_value('Off').else_use('').if_parameter('Res 2 Type').has_value('Tube').else_use('Res 2 Opening').with_name('Opening').if_parameter('Res 2 Type').has_value('Pipe').else_use('Res 2 Inharmonics').with_name('Inharmonics'),
                          use('Res 2 Tune').with_name('Tune').if_parameter('Res 2 On/Off').has_value('On'),
                          use('Res 2 Fine Tune').with_name('Fine Tune').if_parameter('Res 2 On/Off').has_value('On'),
                          use('Res 2 Pitch Env.').with_name('Pitch Envelope').if_parameter('Res 2 On/Off').has_value('On'),
                          use('Res 2 Pitch Env. Time').with_name('Pitch Env Time').if_parameter('Res 2 On/Off').has_value('On'))}),
  (
   'LFO 1',
   {BANK_PARAMETERS_KEY: (
                          use('LFO 1 On/Off').with_name('LFO 1'),
                          use('LFO 1 Depth').with_name('Depth').if_parameter('LFO 1 On/Off').has_value('On'),
                          use('LFO 1 Shape').with_name('Shape').if_parameter('LFO 1 On/Off').has_value('On'),
                          use('LFO 1 Sync').with_name('Sync').if_parameter('LFO 1 On/Off').has_value('On'),
                          use('').if_parameter('LFO 1 On/Off').has_value('Off').else_use('LFO 1 Sync Rate').with_name('Sync Rate').if_parameter('LFO 1 Sync').has_value('Sync').else_use('LFO 1 Rate').with_name('Rate'),
                          use('LFO 1 Offset').with_name('Offset').if_parameter('LFO 1 On/Off').has_value('On'),
                          use('LFO 1 Destination A').with_name('Destination A').if_parameter('LFO 1 On/Off').has_value('On'),
                          use('LFO 1 Destination A Amount').with_name('Dest A Amount').if_parameter('LFO 1 On/Off').has_value('On'))}),
  (
   'LFO 2',
   {BANK_PARAMETERS_KEY: (
                          use('LFO 2 On/Off').with_name('LFO 2'),
                          use('LFO 2 Depth').with_name('Depth').if_parameter('LFO 2 On/Off').has_value('On'),
                          use('LFO 2 Shape').with_name('Shape').if_parameter('LFO 2 On/Off').has_value('On'),
                          use('LFO 2 Sync').with_name('Sync').if_parameter('LFO 2 On/Off').has_value('On'),
                          use('').if_parameter('LFO 2 On/Off').has_value('Off').else_use('LFO 2 Sync Rate').with_name('Sync Rate').if_parameter('LFO 2 Sync').has_value('Sync').else_use('LFO 2 Rate').with_name('Rate'),
                          use('LFO 2 Offset').with_name('Offset').if_parameter('LFO 2 On/Off').has_value('On'),
                          use('LFO 2 Destination A').with_name('Destination A').if_parameter('LFO 2 On/Off').has_value('On'),
                          use('LFO 2 Destination A Amount').with_name('Dest A Amount').if_parameter('LFO 2 On/Off').has_value('On'))}),
  (
   'Mallet Mod.',
   {BANK_PARAMETERS_KEY: (
                          use('Mallet On/Off').with_name('Mallet'),
                          use('Mallet Volume < Key').with_name('Pitch → Vol').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Volume < Vel').with_name('Vel → Vol').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Amount < Key').with_name('Pitch → Noise').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Amount < Vel').with_name('Vel → Noise').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Stiffness < Key').with_name('Pitch → Stiffness').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Stiffness < Vel').with_name('Vel → Stiffness').if_parameter('Mallet On/Off').has_value('On'),
=======
                          'Mallet On/Off',
                          use('Mallet Volume').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Amount').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Stiffness').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Noise Color').if_parameter('Mallet On/Off').has_value('On'),
                          use('Mallet Modulation').if_parameter('Mallet On/Off').has_value('On'),
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
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          '')}))), 
 'DrumBuss':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Drive', 'Drive Type', 'Transients', 'Crunch', 'Boom Freq', 'Boom Amt', 'Boom Decay',
 'Boom Audition'), 
    
    OPTIONS_KEY: ('Compressor', '', '', '', '', '', '')}),
  (
   'Gains',
   {BANK_PARAMETERS_KEY: ('Trim', '', '', '', '', 'Damping Freq', 'Output Gain', 'Dry/Wet')}))), 
 'LoungeLizard':IndexedDict((
  (
   BANK_MAIN_KEY,
<<<<<<< HEAD
   {BANK_PARAMETERS_KEY: (
                          use('M Stiffness').with_name('Mallet Stiffness'),
                          use('M Force').with_name('Mallet Force'),
                          'Noise Amount',
                          use('F Tine Vol').with_name('Tine Level'),
                          use('F Tone Vol').with_name('Tone Bar Level'),
                          use('F Release').with_name('Fork Release'),
                          use('P Symmetry').with_name('Pickup Symmetry'),
                          'Volume')}),
  (
   'Mallet',
   {BANK_PARAMETERS_KEY: (
                          use('M Stiffness').with_name('Stiffness'),
                          use('M Force').with_name('Force'),
                          'Noise Pitch',
                          'Noise Decay',
                          'Noise Amount',
                          use('M Stiff < Vel').with_name('Vel → Stiffness'),
                          use('M Force < Vel').with_name('Vel → Force'),
                          'Volume')}),
  (
   'Fork',
   {BANK_PARAMETERS_KEY: (
                          use('F Tine Color').with_name('Tine Color'),
                          use('F Tine Decay').with_name('Tine Decay'),
                          use('F Tine Vol').with_name('Tine Level'),
                          use('F Tone Vol').with_name('Tone Bar Level'),
                          use('F Tone Decay').with_name('Tone Decay'),
                          use('F Release').with_name('Tone Release'),
                          use('F Tine < Key').with_name('Pitch → Tine'),
                          'Volume')}),
  (
   'Damper',
   {BANK_PARAMETERS_KEY: (
                          use('Damp Tone').with_name('Tone'),
                          use('Damp Balance').with_name('Att/Rel'),
                          use('Damp Amount').with_name('Level'),
                          '',
                          '',
                          '',
                          '',
                          'Volume')}),
  (
   'Pickup',
   {BANK_PARAMETERS_KEY: (
                          use('P Symmetry').with_name('Symmetry'),
                          use('P Distance').with_name('Distance'),
                          use('P Amp In').with_name('Pickup Input'),
                          use('P Amp Out').with_name('Pickup Output'),
                          use('Pickup Model').with_name('Pickup Model'),
                          use('P Amp < Key').with_name('Pitch → Output'),
                          '',
                          'Volume')}),
  (
   'Modulation',
   {BANK_PARAMETERS_KEY: (
                          use('M Stiff < Vel').with_name('Vel → Stiffness'),
                          use('M Stiff < Key').with_name('Pitch → Stiffness'),
                          use('M Force < Vel').with_name('Vel → Force'),
                          use('M Force < Key').with_name('Pitch → Force'),
                          use('Noise < Key').with_name('Pitch → Noise'),
                          use('F Tine < Key').with_name('Pitch → Tine'),
                          use('P Amp < Key').with_name('Pitch → Output'),
                          'Volume')}),
=======
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
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('KB Stretch', 'PB Range', '', '', 'Voices', 'Semitone', 'Detune', 'Volume')}))), 
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
   {BANK_PARAMETERS_KEY: ('1 Filter Type', '1 Filter Freq', '1 Filter Res', '1 Filter <- Vel', '1 Filter <- Random',
 '1 Pan', '1 Pan <- Vel', '1 Pan <- Random')}),
  (
   'Pad 2',
   {BANK_PARAMETERS_KEY: ('2 Start', '2 Envelope Decay', '2 Stretch Factor', '2 Saturator Drive', '2 Envelope Type',
 '2 Transpose', '2 Volume <- Vel', '2 Volume')}),
  (
   '2 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('2 Filter Type', '2 Filter Freq', '2 Filter Res', '2 Filter <- Vel', '2 Filter <- Random',
 '2 Pan', '2 Pan <- Vel', '2 Pan <- Random')}),
  (
   'Pad 3',
   {BANK_PARAMETERS_KEY: ('3 Start', '3 Envelope Decay', '3 Stretch Factor', '3 Saturator Drive', '3 Envelope Type',
 '3 Transpose', '3 Volume <- Vel', '3 Volume')}),
  (
   '3 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('3 Filter Type', '3 Filter Freq', '3 Filter Res', '3 Filter <- Vel', '3 Filter <- Random',
 '3 Pan', '3 Pan <- Vel', '3 Pan <- Random')}),
  (
   'Pad 4',
   {BANK_PARAMETERS_KEY: ('4 Start', '4 Envelope Decay', '4 Stretch Factor', '4 Saturator Drive', '4 Envelope Type',
 '4 Transpose', '4 Volume <- Vel', '4 Volume')}),
  (
   '4 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('4 Filter Type', '4 Filter Freq', '4 Filter Res', '4 Filter <- Vel', '4 Filter <- Random',
 '4 Pan', '4 Pan <- Vel', '4 Pan <- Random')}),
  (
   'Pad 5',
   {BANK_PARAMETERS_KEY: ('5 Start', '5 Envelope Decay', '5 Stretch Factor', '5 Saturator Drive', '5 Envelope Type',
 '5 Transpose', '5 Volume <- Vel', '5 Volume')}),
  (
   '5 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('5 Filter Type', '5 Filter Freq', '5 Filter Res', '5 Filter <- Vel', '5 Filter <- Random',
 '5 Pan', '5 Pan <- Vel', '5 Pan <- Random')}),
  (
   'Pad 6',
   {BANK_PARAMETERS_KEY: ('6 Start', '6 Envelope Decay', '6 Stretch Factor', '6 Saturator Drive', '6 Envelope Type',
 '6 Transpose', '6 Volume <- Vel', '6 Volume')}),
  (
   '6 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('6 Filter Type', '6 Filter Freq', '6 Filter Res', '6 Filter <- Vel', '6 Filter <- Random',
 '6 Pan', '6 Pan <- Vel', '6 Pan <- Random')}),
  (
   'Pad 7',
   {BANK_PARAMETERS_KEY: ('7 Start', '7 Envelope Decay', '7 Stretch Factor', '7 Saturator Drive', '7 Envelope Type',
 '7 Transpose', '7 Volume <- Vel', '7 Volume')}),
  (
   '7 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('7 Filter Type', '7 Filter Freq', '7 Filter Res', '7 Filter <- Vel', '7 Filter <- Random',
 '7 Pan', '7 Pan <- Vel', '7 Pan <- Random')}),
  (
   'Pad 8',
   {BANK_PARAMETERS_KEY: ('8 Start', '8 Envelope Decay', '8 Stretch Factor', '8 Saturator Drive', '8 Envelope Type',
 '8 Transpose', '8 Volume <- Vel', '8 Volume')}),
  (
   '8 Filt/Mod/Pan',
   {BANK_PARAMETERS_KEY: ('8 Filter Type', '8 Filter Freq', '8 Filter Res', '8 Filter <- Vel', '8 Filter <- Random',
 '8 Pan', '8 Pan <- Vel', '8 Pan <- Random')}),
  (
   'Stretch Modes',
   {BANK_PARAMETERS_KEY: ('1 Stretch Mode', '2 Stretch Mode', '3 Stretch Mode', '4 Stretch Mode', '5 Stretch Mode',
 '6 Stretch Mode', '7 Stretch Mode', '8 Stretch Mode')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Global Time', 'Global Transpose', 'Global Volume', '', '', '', '', '')}))), 
 'Operator':IndexedDict((
  (
   'Oscillators',
   {BANK_PARAMETERS_KEY: (
                          'Oscillator',
                          use('Osc-A On').if_parameter('Oscillator').has_value('A').else_use('Osc-B On').if_parameter('Oscillator').has_value('B').else_use('Osc-C On').if_parameter('Oscillator').has_value('C').else_use('Osc-D On').if_parameter('Oscillator').has_value('D'),
                          use('Osc-A Wave').if_parameter('Oscillator').has_value('A').else_use('Osc-B Wave').if_parameter('Oscillator').has_value('B').else_use('Osc-C Wave').if_parameter('Oscillator').has_value('C').else_use('Osc-D Wave').if_parameter('Oscillator').has_value('D'),
                          use('A Fix On ').if_parameter('Oscillator').has_value('A').else_use('B Fix On ').if_parameter('Oscillator').has_value('B').else_use('C Fix On ').if_parameter('Oscillator').has_value('C').else_use('D Fix On ').if_parameter('Oscillator').has_value('D'),
                          use('A Fix Freq').if_parameter('Oscillator').has_value('A').and_parameter('A Fix On ').has_value('On').else_use('A Coarse').if_parameter('Oscillator').has_value('A').else_use('B Fix Freq').if_parameter('Oscillator').has_value('B').and_parameter('B Fix On ').has_value('On').else_use('B Coarse').if_parameter('Oscillator').has_value('B').else_use('C Fix Freq').if_parameter('Oscillator').has_value('C').and_parameter('C Fix On ').has_value('On').else_use('C Coarse').if_parameter('Oscillator').has_value('C').else_use('D Fix Freq').if_parameter('Oscillator').has_value('D').and_parameter('D Fix On ').has_value('On').else_use('D Coarse').if_parameter('Oscillator').has_value('D'),
                          use('A Fix Freq Mul').if_parameter('Oscillator').has_value('A').and_parameter('A Fix On ').has_value('On').else_use('A Fine').if_parameter('Oscillator').has_value('A').else_use('B Fix Freq Mul').if_parameter('Oscillator').has_value('B').and_parameter('B Fix On ').has_value('On').else_use('B Fine').if_parameter('Oscillator').has_value('B').else_use('C Fix Freq Mul').if_parameter('Oscillator').has_value('C').and_parameter('C Fix On ').has_value('On').else_use('C Fine').if_parameter('Oscillator').has_value('C').else_use('D Fix Freq Mul').if_parameter('Oscillator').has_value('D').and_parameter('D Fix On ').has_value('On').else_use('D Fine').if_parameter('Oscillator').has_value('D'),
                          use('Osc-A Level').if_parameter('Oscillator').has_value('A').else_use('Osc-B Level').if_parameter('Oscillator').has_value('B').else_use('Osc-C Level').if_parameter('Oscillator').has_value('C').else_use('Osc-D Level').if_parameter('Oscillator').has_value('D'),
                          'Algorithm')}),
  (
   'Osc. Envelopes',
   {BANK_PARAMETERS_KEY: (
                          'Oscillator',
                          use('Osc-A On').if_parameter('Oscillator').has_value('A').else_use('Osc-B On').if_parameter('Oscillator').has_value('B').else_use('Osc-C On').if_parameter('Oscillator').has_value('C').else_use('Osc-D On').if_parameter('Oscillator').has_value('D'),
                          use('Envelope Feature Time/Level').with_name('Env Type'),
                          use('Ae Attack').with_name('Attack').if_parameter('Oscillator').has_value('A').and_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Ae Init').with_name('Initial').if_parameter('Oscillator').has_value('A').else_use('Be Attack').with_name('Attack').if_parameter('Oscillator').has_value('B').and_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Be Init').with_name('Initial').if_parameter('Oscillator').has_value('B').else_use('Ce Attack').with_name('Attack').if_parameter('Oscillator').has_value('C').and_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Ce Init').with_name('Initial').if_parameter('Oscillator').has_value('C').else_use('De Attack').with_name('Attack').if_parameter('Oscillator').has_value('D').and_parameter('Envelope Feature Time/Level').has_value('Time').else_use('De Init').with_name('Initial').if_parameter('Oscillator').has_value('D'),
                          use('Ae Decay').with_name('Decay').if_parameter('Oscillator').has_value('A').and_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Ae Peak').with_name('Peak').if_parameter('Oscillator').has_value('A').else_use('Be Decay').with_name('Decay').if_parameter('Oscillator').has_value('B').and_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Be Peak').with_name('Peak').if_parameter('Oscillator').has_value('B').else_use('Ce Decay').with_name('Decay').if_parameter('Oscillator').has_value('C').and_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Ce Peak').with_name('Peak').if_parameter('Oscillator').has_value('C').else_use('De Decay').with_name('Decay').if_parameter('Oscillator').has_value('D').and_parameter('Envelope Feature Time/Level').has_value('Time').else_use('De Peak').with_name('Peak').if_parameter('Oscillator').has_value('D'),
                          use('Ae Sustain').with_name('Sustain').if_parameter('Oscillator').has_value('A').else_use('Be Sustain').with_name('Sustain').if_parameter('Oscillator').has_value('B').else_use('Ce Sustain').with_name('Sustain').if_parameter('Oscillator').has_value('C').else_use('De Sustain').with_name('Sustain').if_parameter('Oscillator').has_value('D'),
                          use('Ae Release').with_name('Release').if_parameter('Oscillator').has_value('A').and_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Osc-A Lev < Vel').with_name('Velocity').if_parameter('Oscillator').has_value('A').else_use('Be Release').with_name('Release').if_parameter('Oscillator').has_value('B').and_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Osc-B Lev < Vel').with_name('Velocity').if_parameter('Oscillator').has_value('B').else_use('Ce Release').with_name('Release').if_parameter('Oscillator').has_value('C').and_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Osc-C Lev < Vel').with_name('Velocity').if_parameter('Oscillator').has_value('C').else_use('De Release').with_name('Release').if_parameter('Oscillator').has_value('D').and_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Osc-D Lev < Vel').with_name('Velocity').if_parameter('Oscillator').has_value('D'),
                          use('Osc-A Level').if_parameter('Oscillator').has_value('A').else_use('Osc-B Level').if_parameter('Oscillator').has_value('B').else_use('Osc-C Level').if_parameter('Oscillator').has_value('C').else_use('Osc-D Level').if_parameter('Oscillator').has_value('D'))}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: (
                          'Filter On',
                          use('Filter Type').if_parameter('Filter Type').is_available(True).else_use('Filter Type (Legacy)'),
                          use('Filter Freq'),
                          use('Filter Res').if_parameter('Filter Res').is_available(True).else_use('Filter Res (Legacy)'),
                          use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Lowpass').else_use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Highpass').else_use('Filter Circuit - BP/NO/Morph'),
                          use('Filter Morph').if_parameter('Filter Type').has_value('Morph').else_use('').if_parameter('Filter Type').has_value('Lowpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Highpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Bandpass').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Notch').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('Filter Drive'),
                          'Filt < Vel',
                          'Filt < Key'), 
    
    OPTIONS_KEY: (
                  use('Filter Slope').if_parameter('Filter On').has_value('On').and_parameter('Filter Slope').is_available(True),
                  '',
                  '',
                  '',
                  '',
                  '',
                  '')}),
  (
   'Filter Envelope',
   {BANK_PARAMETERS_KEY: (
                          'Filter On',
                          use('Envelope Feature Time/Slope/Level').with_name('Env Type'),
                          use('Fe Attack').with_name('Attack').if_parameter('Envelope Feature Time/Slope/Level').has_value('Time').else_use('Fe A Slope').with_name('A. Slope').if_parameter('Envelope Feature Time/Slope/Level').has_value('Slope').else_use('Fe Init').with_name('Initial'),
                          use('Fe Decay').with_name('Decay').if_parameter('Envelope Feature Time/Slope/Level').has_value('Time').else_use('Fe D Slope').with_name('D. Slope').if_parameter('Envelope Feature Time/Slope/Level').has_value('Slope').else_use('Fe Peak').with_name('Peak'),
                          use('Fe Sustain').with_name('Sustain'),
                          use('Fe Release').with_name('Release').if_parameter('Envelope Feature Time/Slope/Level').has_value('Time').else_use('Fe R Slope').with_name('R. Slope').if_parameter('Envelope Feature Time/Slope/Level').has_value('Slope').else_use('Fe End').with_name('End'),
                          'Fe R < Vel',
                          'Fe Amount')}),
  (
   'Filter Other',
   {BANK_PARAMETERS_KEY: (
                          'Filter On',
                          'Shaper Type',
                          'Shaper Drive',
                          'Shaper Mix',
                          'Fe Mode',
                          use('Fe Retrig').if_parameter('Fe Mode').has_value('Beat').else_use('Fe Retrig').if_parameter('Fe Mode').has_value('Sync').else_use('Fe Loop').if_parameter('Fe Mode').has_value('Loop').else_use(''),
                          '',
                          '')}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          'LFO On',
                          'LFO Type',
                          'LFO Range',
                          use('LFO Sync').if_parameter('LFO Range').has_value('Sync').else_use('LFO Rate'),
                          'LFO Retrigger',
                          'LFO Amt',
                          '',
                          '')}),
  (
   'LFO Envelope',
   {BANK_PARAMETERS_KEY: (
                          'LFO On',
                          use('Envelope Feature Time/Level').with_name('Env Type'),
                          use('Le Attack').with_name('Attack').if_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Le Init').with_name('Initial'),
                          use('Le Decay').with_name('Decay').if_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Le Peak').with_name('Peak'),
                          use('Le Sustain').with_name('Sustain'),
                          use('Le Release').with_name('Release').if_parameter('Envelope Feature Time/Level').has_value('Time').else_use('Le End').with_name('End'),
                          'Le Mode',
                          use('Le Retrig').if_parameter('Le Mode').has_value('Beat').else_use('Le Retrig').if_parameter('Le Mode').has_value('Sync').else_use('Le Loop').if_parameter('Le Mode').has_value('Loop').else_use('LFO Amt'))}),
  (
   'LFO Target',
   {BANK_PARAMETERS_KEY: (
                          'Oscillator',
                          use('Osc-A < LFO').if_parameter('Oscillator').has_value('A').else_use('Osc-B < LFO').if_parameter('Oscillator').has_value('B').else_use('Osc-C < LFO').if_parameter('Oscillator').has_value('C').else_use('Osc-D < LFO').if_parameter('Oscillator').has_value('D'),
                          'Filt < LFO',
                          'LFO Amt A',
                          'LFO Dst B',
                          'LFO Amt B',
                          'LFO R < K',
                          'LFO < Vel')}),
  (
   'Pitch Envelope',
   {BANK_PARAMETERS_KEY: (
                          'Pe On',
                          use('Envelope Feature Time/Slope/Level').with_name('Env Type'),
                          use('Pe Attack').with_name('Attack').if_parameter('Envelope Feature Time/Slope/Level').has_value('Time').else_use('Pe A Slope').with_name('A. Slope').if_parameter('Envelope Feature Time/Slope/Level').has_value('Slope').else_use('Pe Init').with_name('Initial'),
                          use('Pe Decay').with_name('Decay').if_parameter('Envelope Feature Time/Slope/Level').has_value('Time').else_use('Pe D Slope').with_name('D. Slope').if_parameter('Envelope Feature Time/Slope/Level').has_value('Slope').else_use('Pe Peak').with_name('Peak'),
                          use('Pe Sustain').with_name('Sustain'),
                          use('Pe Release').with_name('Release').if_parameter('Envelope Feature Time/Slope/Level').has_value('Time').else_use('Pe R Slope').with_name('R. Slope').if_parameter('Envelope Feature Time/Slope/Level').has_value('Slope').else_use('Pe End').with_name('End'),
                          'Pe R < Vel',
                          'Pe Amount')}),
  (
   'Aux',
   {BANK_PARAMETERS_KEY: (
                          'Oscillator',
                          use('Osc-A < Pe').if_parameter('Oscillator').has_value('A').else_use('Osc-B < Pe').if_parameter('Oscillator').has_value('B').else_use('Osc-C < Pe').if_parameter('Oscillator').has_value('C').else_use('Osc-D < Pe').if_parameter('Oscillator').has_value('D'),
                          'LFO < Pe',
                          'Pe Amt A',
                          'Pe Dst B',
                          'Pe Amt B',
                          'Glide On',
                          'Glide Time')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Transpose', 'Spread', 'Tone', 'Time', 'Panorama', 'Pan < Rnd', 'Pan < Key', 'Volume')}),
  (
   'Osc. Other',
   {BANK_PARAMETERS_KEY: (
                          'Oscillator',
                          use('Osc-A Lev < Vel').if_parameter('Oscillator').has_value('A').else_use('Osc-B Lev < Vel').if_parameter('Oscillator').has_value('B').else_use('Osc-C Lev < Vel').if_parameter('Oscillator').has_value('C').else_use('Osc-D Lev < Vel').if_parameter('Oscillator').has_value('D'),
                          use('A Freq<Vel').if_parameter('Oscillator').has_value('A').else_use('B Freq<Vel').if_parameter('Oscillator').has_value('B').else_use('C Freq<Vel').if_parameter('Oscillator').has_value('C').else_use('D Freq<Vel').if_parameter('Oscillator').has_value('D'),
                          use('A Quantize').if_parameter('Oscillator').has_value('A').else_use('B Quantize').if_parameter('Oscillator').has_value('B').else_use('C Quantize').if_parameter('Oscillator').has_value('C').else_use('D Quantize').if_parameter('Oscillator').has_value('D'),
                          use('Osc-A Retrig').if_parameter('Oscillator').has_value('A').else_use('Osc-B Retrig').if_parameter('Oscillator').has_value('B').else_use('Osc-C Retrig').if_parameter('Oscillator').has_value('C').else_use('Osc-D Retrig').if_parameter('Oscillator').has_value('D'),
                          use('Osc-A Phase').if_parameter('Oscillator').has_value('A').else_use('Osc-B Phase').if_parameter('Oscillator').has_value('B').else_use('Osc-C Phase').if_parameter('Oscillator').has_value('C').else_use('Osc-D Phase').if_parameter('Oscillator').has_value('D'),
                          use('Ae Mode').if_parameter('Oscillator').has_value('A').else_use('Be Mode').if_parameter('Oscillator').has_value('B').else_use('Ce Mode').if_parameter('Oscillator').has_value('C').else_use('De Mode').if_parameter('Oscillator').has_value('D'),
                          use('Ae Retrig').if_parameter('Oscillator').has_value('A').and_parameter('Ae Mode').has_value('Beat').else_use('Ae Retrig').if_parameter('Oscillator').has_value('A').and_parameter('Ae Mode').has_value('Sync').else_use('Ae Loop').if_parameter('Oscillator').has_value('A').and_parameter('Ae Mode').has_value('Loop').else_use('Be Retrig').if_parameter('Oscillator').has_value('B').and_parameter('Be Mode').has_value('Beat').else_use('Be Retrig').if_parameter('Oscillator').has_value('B').and_parameter('Be Mode').has_value('Sync').else_use('Be Loop').if_parameter('Oscillator').has_value('B').and_parameter('Be Mode').has_value('Loop').else_use('Ce Retrig').if_parameter('Oscillator').has_value('C').and_parameter('Ce Mode').has_value('Beat').else_use('Ce Retrig').if_parameter('Oscillator').has_value('C').and_parameter('Ce Mode').has_value('Sync').else_use('Ce Loop').if_parameter('Oscillator').has_value('C').and_parameter('Ce Mode').has_value('Loop').else_use('De Retrig').if_parameter('Oscillator').has_value('D').and_parameter('De Mode').has_value('Beat').else_use('De Retrig').if_parameter('Oscillator').has_value('D').and_parameter('De Mode').has_value('Sync').else_use('De Loop').if_parameter('Oscillator').has_value('D').and_parameter('De Mode').has_value('Loop').else_use(''))}),
  (
   'Velocity',
   {BANK_PARAMETERS_KEY: (
                          'Oscillator',
                          use('Ae R < Vel').if_parameter('Oscillator').has_value('A').else_use('Be R < Vel').if_parameter('Oscillator').has_value('B').else_use('Ce R < Vel').if_parameter('Oscillator').has_value('C').else_use('De R < Vel').if_parameter('Oscillator').has_value('D'),
                          use('Osc-A Lev < Vel').if_parameter('Oscillator').has_value('A').else_use('Osc-B Lev < Vel').if_parameter('Oscillator').has_value('B').else_use('Osc-C Lev < Vel').if_parameter('Oscillator').has_value('C').else_use('Osc-D Lev < Vel').if_parameter('Oscillator').has_value('D'),
                          'LFO < Vel',
                          'Filt < Vel',
                          'Pe R < Vel',
                          'Fe R < Vel',
                          'Le R < Vel')}),
  (
   'Keyboard',
   {BANK_PARAMETERS_KEY: (
                          'Oscillator',
                          use('Osc-A Lev < Key').if_parameter('Oscillator').has_value('A').else_use('Osc-B Lev < Key').if_parameter('Oscillator').has_value('B').else_use('Osc-C Lev < Key').if_parameter('Oscillator').has_value('C').else_use('Osc-D Lev < Key').if_parameter('Oscillator').has_value('D'),
                          'Filt < Key',
                          'Pan < Key',
                          'Time < Key',
                          'LFO R < K',
                          '',
                          '')}))), 
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
                          use('Filter Type').if_parameter('Filter Type').is_available(True).else_use('Filter Type (Legacy)'),
                          use('Filter Freq'),
                          use('Filter Res').if_parameter('Filter Res').is_available(True).else_use('Filter Res (Legacy)'),
                          use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Lowpass').else_use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Highpass').else_use('Filter Circuit - BP/NO/Morph'),
                          use('Filter Morph').if_parameter('Filter Type').has_value('Morph').else_use('').if_parameter('Filter Type').has_value('Lowpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Highpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Bandpass').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Notch').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('Filter Drive'),
                          'Filt < Vel',
                          'Filt < Key'), 
    
    OPTIONS_KEY: (
                  use('Filter Slope').if_parameter('F On').has_value('On').and_parameter('Filter Slope').is_available(True),
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '')}),
  (
   'Filt. Env',
   {BANK_PARAMETERS_KEY: ('Fe On', 'Fe < Env', 'Fe Init', 'Fe Attack', 'Fe Decay', 'Fe Peak', 'Fe Sustain',
 'Fe Release')}),
  (
   'Shaper',
   {BANK_PARAMETERS_KEY: (
                          'Fe On',
                          'Fe End',
                          'Fe Mode',
                          use('Fe Loop').if_parameter('Fe Mode').has_value('Loop').else_use('Fe Retrig').if_parameter('Fe Mode').has_value('Beat').else_use('Fe Retrig').if_parameter('Fe Mode').has_value('Sync').else_use(''),
                          'Fe R < Vel',
                          'Shaper On',
                          'Shaper Type',
                          'Shaper Amt')}),
  (
   'Osc. pg. 1',
   {BANK_PARAMETERS_KEY: ('Osc On', 'O Mode', 'Oe Init', 'Oe Attack', 'Oe Peak', 'Oe Decay', 'Oe Sustain', 'Oe Release')}),
  (
   'Osc. pg. 2',
   {BANK_PARAMETERS_KEY: (
                          'Oe End',
                          'Oe Mode',
                          use('Oe Loop').if_parameter('Oe Mode').has_value('Loop').else_use('Oe Retrig').if_parameter('Oe Mode').has_value('Beat').else_use('Oe Retrig').if_parameter('Oe Mode').has_value('Sync').else_use(''),
                          'O Type',
                          'O Volume',
                          'O Fix On',
                          use('O Coarse').if_parameter('O Fix On').has_value('Off').else_use('O Fix Freq'),
                          use('O Fine').if_parameter('O Fix On').has_value('Off').else_use('O Fix Freq Mul'))}),
  (
   'Pitch Env.',
   {BANK_PARAMETERS_KEY: ('Pe On', 'Pe < Env', 'Pe Init', 'Pe Attack', 'Pe Peak', 'Pe Decay', 'Pe Sustain',
 'Pe Release')}),
  (
   'Pitch Env. 2',
   {BANK_PARAMETERS_KEY: (
                          'Pe On',
                          'Pe End',
                          'Pe R < Vel',
                          'Pe Mode',
                          use('Pe Loop').if_parameter('Pe Mode').has_value('Loop').else_use('Pe Retrig').if_parameter('Pe Mode').has_value('Beat').else_use('Pe Retrig').if_parameter('Pe Mode').has_value('Sync').else_use(''),
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
                          'L 1 Wave',
                          'L 1 Sync',
                          use('L 1 Sync Rate').if_parameter('L 1 Sync').has_value('Sync').else_use('L 1 Rate'),
                          'Vol < LFO',
                          'Filt < LFO',
                          'Pan < LFO',
                          'Pitch < LFO')}),
  (
   'LFO1 pg. 2',
   {BANK_PARAMETERS_KEY: ('L 1 On', 'L 1 Retrig', 'L 1 Offset', 'L 1 Attack', '', '', '', '')}),
  (
   'LFO2 pg. 1',
   {BANK_PARAMETERS_KEY: (
                          'L 2 On',
                          'L 2 Wave',
                          'L 2 Sync',
                          use('L 2 Sync Rate').if_parameter('L 2 Sync').has_value('Sync').else_use('L 2 Rate'),
                          'L 2 Retrig',
                          'L 2 Offset',
                          'L 2 Attack',
                          '')}),
  (
   'LFO2 pg. 2',
   {BANK_PARAMETERS_KEY: (
                          'L 2 On',
                          'L 2 St Mode',
                          use('L 2 Spin').if_parameter('L 2 St Mode').has_value('Spin').else_use('L 2 Phase'),
                          '',
                          '',
                          '',
                          '',
                          '')}),
  (
   'LFO3 pg. 1',
   {BANK_PARAMETERS_KEY: (
                          'L 3 On',
                          'L 3 Wave',
                          'L 3 Sync',
                          use('L 3 Sync Rate').if_parameter('L 3 Sync').has_value('Sync').else_use('L 3 Rate'),
                          'L 3 Retrig',
                          'L 3 Offset',
                          'L 3 Attack',
                          '')}),
  (
   'LFO3 pg. 2',
   {BANK_PARAMETERS_KEY: (
                          'L 3 On',
                          'L 3 St Mode',
                          use('L 3 Spin').if_parameter('L 3 St Mode').has_value('Spin').else_use('L 3 Phase'),
                          '',
                          '',
                          '',
                          '',
                          '')}),
  (
   'Aux Env. 1',
   {BANK_PARAMETERS_KEY: (
                          'Ae On',
                          'Ae Init',
                          'Ae Peak',
                          'Ae Sustain',
                          'Ae End',
                          'Ae Mode',
                          use('Ae Loop').if_parameter('Ae Mode').has_value('Loop').else_use('Ae Retrig').if_parameter('Ae Mode').has_value('Beat').else_use('Ae Retrig').if_parameter('Ae Mode').has_value('Sync'),
                          '')}),
  (
   'Aux Env. 2',
   {BANK_PARAMETERS_KEY: ('Ae On', 'Ae Attack', 'Ae Decay', 'Ae Release', 'Ae A Slope', 'Ae D Slope', 'Ae R Slope',
 '')}))), 
 'OriginalSimpler':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('Ve Attack').if_parameter('Multi Sample').has_value('On').else_use('Zoom'),
                          use('Ve Decay').if_parameter('Multi Sample').has_value('On').else_use('Start'),
                          use('Ve Sustain').if_parameter('Multi Sample').has_value('On').else_use('End'),
                          use('Ve Release').if_parameter('Multi Sample').has_value('On').else_use('Fade In').if_parameter('Mode').has_value('One-Shot').else_use('Nudge').if_parameter('Mode').has_value('Slicing').else_use('S Start').if_parameter('Mode').has_value('Classic'),
                          use('Pan').if_parameter('Multi Sample').has_value('On').else_use('Fade Out').if_parameter('Mode').has_value('One-Shot').else_use('Playback').if_parameter('Mode').has_value('Slicing').else_use('S Length').if_parameter('Mode').has_value('Classic'),
                          use('Transpose').if_parameter('Multi Sample').has_value('On').else_use('Transpose').if_parameter('Mode').has_value('One-Shot').else_use('Slice by').if_parameter('Mode').has_value('Slicing').else_use('S Loop Length').if_parameter('Mode').has_value('Classic'),
                          use('Detune').if_parameter('Multi Sample').has_value('On').else_use('Gain').if_parameter('Mode').has_value('One-Shot').else_use('Sensitivity').if_parameter('Slice by').has_value('Transient').and_parameter('Mode').has_value('Slicing').else_use('Division').if_parameter('Slice by').has_value('Beat').and_parameter('Mode').has_value('Slicing').else_use('Regions').if_parameter('Slice by').has_value('Region').and_parameter('Mode').has_value('Slicing').else_use('Pad Slicing').if_parameter('Slice by').has_value('Manual').and_parameter('Mode').has_value('Slicing').else_use('Sensitivity').if_parameter('Mode').has_value('Slicing').else_use('S Loop Fade').if_parameter('Mode').has_value('Classic').and_parameter('Warp').has_value('Off').else_use('Detune'),
                          use('Volume').if_parameter('Multi Sample').has_value('On').else_use('Mode')), 
    
    OPTIONS_KEY: (
                  use('').if_parameter('Multi Sample').has_value('On').else_use('Loop').if_parameter('Mode').has_value('Classic').else_use('Trigger Mode'),
                  use('').if_parameter('Multi Sample').has_value('On').else_use('Warp as X Bars'),
                  use('').if_parameter('Multi Sample').has_value('On').else_use(':2'),
                  use('').if_parameter('Multi Sample').has_value('On').else_use('x2'),
                  use('').if_parameter('Multi Sample').has_value('On').else_use('Clear Slices').if_parameter('Slice by').has_value('Manual').and_parameter('Mode').has_value('Slicing').else_use('Reset Slices').if_parameter('Mode').has_value('Slicing'),
                  use('').if_parameter('Multi Sample').has_value('On').else_use('Split Slice').if_parameter('Mode').has_value('Slicing').else_use('Crop'),
                  use('').if_parameter('Multi Sample').has_value('On').else_use('Reverse')), 
    
    VIEW_DESCRIPTION_KEY: 'waveform'}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: (
                          'Glide Mode',
                          'Glide Time',
                          use('').if_parameter('Mode').has_value('One-Shot').else_use('Voices').if_parameter('Mode').has_value('Classic').else_use('Voices').if_parameter('Mode').has_value('Slicing').and_parameter('Playback').has_value('Poly'),
                          'Transpose',
                          'Detune',
                          'Vol < Vel',
                          'Gain',
                          'Volume'), 
    
    OPTIONS_KEY: (
                  '',
                  use('').if_parameter('Mode').has_value('One-Shot').else_use('Retrigger').if_parameter('Mode').has_value('Classic').else_use('Retrigger').if_parameter('Mode').has_value('Slicing').and_parameter('Playback').has_value('Poly'),
                  '',
                  '',
                  '',
                  '',
                  ''), 
    
    VIEW_DESCRIPTION_KEY: 'waveform'}),
  (
   'Envelopes',
   {BANK_PARAMETERS_KEY: (
                          'Env. Type',
                          use('Fe On').if_parameter('Env. Type').has_value('Filter').else_use('Pe On').if_parameter('Env. Type').has_value('Pitch').else_use('Ve Attack').if_parameter('Mode').has_value('Classic').else_use('Fade In'),
                          use('Fe Attack').if_parameter('Env. Type').has_value('Filter').else_use('Pe Attack').if_parameter('Env. Type').has_value('Pitch').else_use('Ve Decay').if_parameter('Mode').has_value('Classic').else_use('Fade Out'),
                          use('Fe Decay').if_parameter('Env. Type').has_value('Filter').else_use('Pe Decay').if_parameter('Env. Type').has_value('Pitch').else_use('Ve Sustain').if_parameter('Mode').has_value('Classic').else_use('Volume'),
                          use('Fe Sustain').if_parameter('Env. Type').has_value('Filter').else_use('Pe Sustain').if_parameter('Env. Type').has_value('Pitch').else_use('Ve Release').if_parameter('Mode').has_value('Classic'),
                          use('Fe Release').if_parameter('Env. Type').has_value('Filter').else_use('Pe Release').if_parameter('Env. Type').has_value('Pitch').else_use('Ve Mode').if_parameter('Env. Type').has_value('Volume'),
                          use('Fe < Env').if_parameter('Env. Type').has_value('Filter').else_use('Pe < Env').if_parameter('Env. Type').has_value('Pitch').else_use('Ve Retrig').if_parameter('Env. Type').has_value('Volume').and_parameter('Ve Mode').has_value('Beat').or_parameter('Ve Mode').has_value('Sync').else_use('Ve Loop').if_parameter('Ve Mode').has_value('Loop'),
                          use('Filter Freq').if_parameter('Env. Type').has_value('Filter').else_use('Transpose').if_parameter('Env. Type').has_value('Pitch')), 
    
    OPTIONS_KEY: ('', '', '', '', '', '', ''), 
    VIEW_DESCRIPTION_KEY: ''}),
  (
   'Warp',
   {BANK_PARAMETERS_KEY: (
                          use('').if_parameter('Multi Sample').has_value('On').else_use('Zoom'),
                          use('').if_parameter('Multi Sample').has_value('On').else_use('Start'),
                          use('').if_parameter('Multi Sample').has_value('On').else_use('End'),
                          use('').if_parameter('Multi Sample').has_value('On').else_use('Warp'),
                          use('').if_parameter('Multi Sample').has_value('On').else_use('').if_parameter('Warp').has_value('Off').else_use('Warp Mode'),
                          use('').if_parameter('Multi Sample').has_value('On').else_use('').if_parameter('Warp').has_value('Off').else_use('Preserve').if_parameter('Warp Mode').has_value('Beats').else_use('Grain Size Tones').if_parameter('Warp Mode').has_value('Tones').else_use('Grain Size Texture').if_parameter('Warp Mode').has_value('Texture').else_use('Formants').if_parameter('Warp Mode').has_value('Pro'),
                          use('').if_parameter('Multi Sample').has_value('On').else_use('').if_parameter('Warp').has_value('Off').else_use('Loop Mode').if_parameter('Warp Mode').has_value('Beats').else_use('Flux').if_parameter('Warp Mode').has_value('Texture').else_use('Envelope Complex Pro').if_parameter('Warp Mode').has_value('Pro'),
                          use('').if_parameter('Multi Sample').has_value('On').else_use('').if_parameter('Warp').has_value('Off').else_use('Envelope').if_parameter('Warp Mode').has_value('Beats')), 
    
    OPTIONS_KEY: (
                  use('').if_parameter('Multi Sample').has_value('On').else_use('Warp as X Bars'),
                  use('').if_parameter('Multi Sample').has_value('On').else_use(':2'),
                  use('').if_parameter('Multi Sample').has_value('On').else_use('x2'),
                  '',
                  '',
                  '',
                  '',
                  ''), 
    
    VIEW_DESCRIPTION_KEY: 'waveform'}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: (
                          'F On',
                          use('Filter Type').if_parameter('Filter Type').is_available(True).else_use('Filter Type (Legacy)'),
                          'Filter Freq',
                          use('Filter Res').if_parameter('Filter Res').is_available(True).else_use('Filter Res (Legacy)'),
                          use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Lowpass').else_use('Filter Circuit - LP/HP').if_parameter('Filter Type').has_value('Highpass').else_use('Filter Circuit - BP/NO/Morph'),
                          use('Filter Morph').if_parameter('Filter Type').has_value('Morph').else_use('').if_parameter('Filter Type').has_value('Lowpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Highpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Bandpass').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Notch').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('Filter Drive'),
                          'Filt < Vel',
                          'Filt < LFO'), 
    
    OPTIONS_KEY: (
                  use('Filter Slope').if_parameter('F On').has_value('On').and_parameter('Filter Slope').is_available(True),
                  '',
                  '',
                  '',
                  '',
                  '',
                  '')}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          'L On',
                          'L Wave',
                          use('L Rate').if_parameter('L Sync').has_value('Free').else_use('L Sync Rate'),
                          'L Attack',
                          'L R < Key',
                          'Vol < LFO',
                          'L Retrig',
                          'L Offset'), 
    
    OPTIONS_KEY: (
                  '',
                  use('LFO Sync Type').if_parameter('L On').has_value('On'),
                  '',
                  '',
                  '',
                  '',
                  '')}),
  (
   'Pan',
   {BANK_PARAMETERS_KEY: ('Pan', 'Spread', 'Pan < Rnd', 'Pan < LFO', '', '', '', ''), 
    
    OPTIONS_KEY: ('', '', '', '', '', '', '')}))), 
 'StringStudio':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('Exciter Type').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc ForceMassProt').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc FricStiff').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Velocity').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos').with_name('Exc Position').if_parameter('Exc On/Off').has_value('On'),
                          'String Decay',
                          use('Str Damping').with_name('String Damping').if_parameter('Exciter Type').does_not_have_value('Bow').else_use(''),
                          'Volume')}),
  (
   'Exciter',
   {BANK_PARAMETERS_KEY: (
                          use('Exc On/Off').with_name('Exciter'),
                          use('Exciter Type').with_name('Type').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc ForceMassProt').with_name('Force').if_parameter('Exciter Type').has_value('Bow').and_parameter('Exc On/Off').has_value('On').else_use('Exc ForceMassProt').with_name('Mass').if_parameter('Exciter Type').has_value('Hammer').and_parameter('Exc On/Off').has_value('On').else_use('Exc ForceMassProt').with_name('Mass').if_parameter('Exciter Type').has_value('Hammer (bouncing)').and_parameter('Exc On/Off').has_value('On').else_use('Exc ForceMassProt').with_name('Protrusion').if_parameter('Exciter Type').has_value('Plectrum').and_parameter('Exc On/Off').has_value('On'),
                          use('Exc FricStiff').with_name('Friction').if_parameter('Exc On/Off').has_value('On').and_parameter('Exciter Type').has_value('Bow').else_use('Exc FricStiff').with_name('Stiffness').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Velocity').with_name('Velocity').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos').with_name('Position').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos Abs').with_name('Fixed Position').if_parameter('Exc On/Off').has_value('On'),
=======
                          use('Excitator Type').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc ForceMassProt').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc FricStiff').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Velocity').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos').if_parameter('Exc On/Off').has_value('On'),
                          'String Decay',
                          'Str Damping',
                          'Volume')}),
  (
   'Excitator',
   {BANK_PARAMETERS_KEY: (
                          'Exc On/Off',
                          use('Excitator Type').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc ForceMassProt').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc FricStiff').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Velocity').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos Abs').if_parameter('Exc On/Off').has_value('On'),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          'Volume')}),
  (
   'String & Pickup',
   {BANK_PARAMETERS_KEY: (
                          'String Decay',
<<<<<<< HEAD
                          use('S Decay < Key').with_name('Pitch → Decay'),
                          use('S Decay Ratio').with_name('Decay Ratio'),
                          use('Str Inharmon').with_name('Inharmonicity'),
                          use('Str Damping').with_name('Damping'),
                          use('S Damp < Key').with_name('Pitch → Damping'),
=======
                          'S Decay < Key',
                          'S Decay Ratio',
                          'Str Inharmon',
                          'Str Damping',
                          'S Damp < Key',
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          'Pickup On/Off',
                          use('Pickup Pos').if_parameter('Pickup On/Off').has_value('On'))}),
  (
   'Damper',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('Damper On').with_name('Damper'),
                          use('Damper Mass').with_name('Mass').if_parameter('Damper On').has_value('On'),
                          use('D Stiffness').with_name('Stiffness').if_parameter('Damper On').has_value('On'),
                          use('Damp Pos').with_name('Position').if_parameter('Damper On').has_value('On'),
                          use('D Damping').with_name('Damping').if_parameter('Damper On').has_value('On'),
                          use('Damper Gated').with_name('Gated Damper').if_parameter('Damper On').has_value('On'),
                          use('').if_parameter('Damper On').has_value('Off').else_use('D Velocity').with_name('Velocity').if_parameter('Damper Gated').has_value('On').else_use(''),
                          use('D Pos Abs').with_name('Fixed Position').if_parameter('Damper On').has_value('On'))}),
  (
   'Termination',
   {BANK_PARAMETERS_KEY: (
                          use('Term On/Off').with_name('Termination'),
                          use('Term Mass').with_name('Finger Mass').if_parameter('Term On/Off').has_value('On'),
                          use('Term Fng Stiff').with_name('Finger Stiffness').if_parameter('Term On/Off').has_value('On'),
                          use('Term Fret Stiff').with_name('Fret Stiffness').if_parameter('Term On/Off').has_value('On'),
                          use('T Mass < Vel').with_name('Vel → Fing Mass').if_parameter('Term On/Off').has_value('On'),
                          use('T Mass < Key').with_name('Pitch → Fing Mass').if_parameter('Term On/Off').has_value('On'),
=======
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
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          '',
                          'Volume')}),
  (
   'Body',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('Body On/Off').with_name('Body'),
                          use('Body Type').with_name('Type').if_parameter('Body On/Off').has_value('On'),
                          use('Body Size').with_name('Size').if_parameter('Body On/Off').has_value('On'),
                          use('Body Decay').with_name('Decay').if_parameter('Body On/Off').has_value('On'),
                          use('Body Low-Cut').with_name('Low-cut').if_parameter('Body On/Off').has_value('On'),
                          use('Body High-Cut').with_name('High-cut').if_parameter('Body On/Off').has_value('On'),
                          use('Body Mix').with_name('Mix').if_parameter('Body On/Off').has_value('On'),
=======
                          'Body On/Off',
                          use('Body Type').if_parameter('Body On/Off').has_value('On'),
                          use('Body Size').if_parameter('Body On/Off').has_value('On'),
                          use('Body Decay').if_parameter('Body On/Off').has_value('On'),
                          use('Body Low-Cut').if_parameter('Body On/Off').has_value('On'),
                          use('Body High-Cut').if_parameter('Body On/Off').has_value('On'),
                          use('Body Mix').if_parameter('Body On/Off').has_value('On'),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          'Volume')}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('Filter On/Off').with_name('Filter'),
                          use('Filter Type').with_name('Type').if_parameter('Filter On/Off').has_value('On'),
                          use('Filter Freq').with_name('Frequency').if_parameter('Filter On/Off').has_value('On'),
                          use('Filter Reso').with_name('Resonance').if_parameter('Filter On/Off').has_value('On'),
                          use('Freq < Env').with_name('Env → Freq').if_parameter('Filter On/Off').has_value('On'),
                          use('Freq < LFO').with_name('LFO → Freq').if_parameter('Filter On/Off').has_value('On'),
                          use('Reso < Env').with_name('Env → Res').if_parameter('Filter On/Off').has_value('On'),
                          use('Reso < LFO').with_name('LFO → Res').if_parameter('Filter On/Off').has_value('On'))}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          use('LFO On/Off').with_name('LFO'),
                          use('LFO Shape').with_name('Shape').if_parameter('LFO On/Off').has_value('On'),
                          use('LFO Sync On').with_name('Rate Mode').if_parameter('LFO On/Off').has_value('On'),
                          use('').if_parameter('LFO On/Off').has_value('Off').else_use('LFO SyncRate').with_name('Sync Rate').if_parameter('LFO Sync On').has_value('Beat').else_use('LFO Speed').with_name('Speed'),
                          use('LFO Delay').with_name('Delay').if_parameter('LFO On/Off').has_value('On'),
                          use('LFO Fade In').with_name('Fade In').if_parameter('LFO On/Off').has_value('On'),
=======
                          'Filter On/Off',
                          use('Filter Type').if_parameter('Filter On/Off').has_value('On'),
                          use('Filter Freq').if_parameter('Filter On/Off').has_value('On'),
                          use('Filter Reso').if_parameter('Filter On/Off').has_value('On'),
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
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          '',
                          '')}),
  (
   'Vibrato',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('Vibrato On/Off').with_name('Vibrato'),
                          use('Vib Delay').with_name('Delay').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib Fade-In').with_name('Fade-in').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib Speed').with_name('Speed').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib Amount').with_name('Amount').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib < ModWh').with_name('ModWh → Vibrato').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib Error').with_name('Error').if_parameter('Vibrato On/Off').has_value('On'),
=======
                          'Vibrato On/Off',
                          use('Vib Delay').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib Fade-In').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib Speed').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib Amount').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib < ModWh').if_parameter('Vibrato On/Off').has_value('On'),
                          use('Vib Error').if_parameter('Vibrato On/Off').has_value('On'),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          '')}),
  (
   'Unison & Portamento',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('Unison On/Off').with_name('Unison'),
                          use('Unison Voices').with_name('Voices').if_parameter('Unison On/Off').has_value('On'),
                          use('Uni Delay').with_name('Delay').if_parameter('Unison On/Off').has_value('On'),
                          use('Uni Detune').with_name('Detune').if_parameter('Unison On/Off').has_value('On'),
                          use('Porta On/Off').with_name('Portamento'),
                          use('Porta Time').with_name('Time').if_parameter('Porta On/Off').has_value('On'),
                          use('Porta Legato').with_name('Legato').if_parameter('Porta On/Off').has_value('On'),
                          use('Porta Prop').with_name('Proportional').if_parameter('Porta On/Off').has_value('On'))}),
=======
                          'Unison On/Off',
                          use('Unison Voices').if_parameter('Unison On/Off').has_value('On'),
                          use('Uni Delay').if_parameter('Unison On/Off').has_value('On'),
                          use('Uni Detune').if_parameter('Unison On/Off').has_value('On'),
                          'Porta On/Off',
                          use('Porta Time').if_parameter('Porta On/Off').has_value('On'),
                          use('Porta Legato').if_parameter('Porta On/Off').has_value('On'),
                          use('Porta Prop').if_parameter('Porta On/Off').has_value('On'))}),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Octave', 'Semitone', 'Fine Tune', 'Voices', 'PB Depth', 'Stretch', 'Error', 'Key Priority')}),
  (
   'Filt. Env.',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          use('FEG On/Off').with_name('Filter Envelope'),
                          use('FEG Attack').with_name('Attack').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG Decay').with_name('Decay').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG Sustain').with_name('Sustain').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG Release').with_name('Release').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG Att < Vel').with_name('Vel → Attack').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG < Vel').with_name('Vel → Env').if_parameter('FEG On/Off').has_value('On'),
                          '')}),
  (
   'Exciter Mod.',
   {BANK_PARAMETERS_KEY: (
                          use('Exc ForceMassProt < Vel').with_name('Vel → Protrusion').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc ForceMassProt < Key').with_name('Pitch → Protrusion').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc FricStiff < Vel').with_name('Vel → Stiffness').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc FricStiff < Key').with_name('Pitch → Stiffness').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Vel < Vel').with_name('Vel → Exc Vel').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Vel < Key').with_name('Pitch → Exc Vel').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos < Vel').with_name('Vel → Position').if_parameter('Exc On/Off').has_value('On'),
                          use('E Pos < Key').with_name('Pitch → Position').if_parameter('Exc On/Off').has_value('On'))}),
  (
   'Mass Mod.',
   {BANK_PARAMETERS_KEY: (
                          use('D Mass < Key').with_name('Pitch → Mass').if_parameter('Damper On').has_value('On'),
                          use('D Stiff < Key').with_name('Pitch → Stiffness').if_parameter('Damper On').has_value('On'),
                          use('D Pos < Key').with_name('Pitch → Damp Pos').if_parameter('Damper On').has_value('On'),
                          use('D Pos < Vel').with_name('Vel → Damp Pos').if_parameter('Damper On').has_value('On'),
                          use('Damper Gated').with_name('Gated Damper').if_parameter('Damper On').has_value('On'),
                          use('').if_parameter('Damper On').has_value('Off').else_use('D Velo < Key').with_name('Pitch → Damp Vel').if_parameter('Damper Gated').has_value('On').else_use(''),
=======
                          'FEG On/Off',
                          use('FEG Attack').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG Decay').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG Sustain').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG Release').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG Att < Vel').if_parameter('FEG On/Off').has_value('On'),
                          use('FEG < Vel').if_parameter('FEG On/Off').has_value('On'),
                          '')}),
  (
   'Excitator Mod.',
   {BANK_PARAMETERS_KEY: (
                          use('Exc Prot < Vel').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Prot < Key').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Stiff < Vel').if_parameter('Exc On/Off').has_value('On'),
                          use('Exc Stiff < Key').if_parameter('Exc On/Off').has_value('On'),
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
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          '',
                          '')}))), 
 'Hybrid':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Section',
                          use('IR').if_parameter('Section').has_value('Convolution').else_use('Algo Type').with_name('Type').if_parameter('Section').has_value('Algo').else_use('EQ On').if_parameter('Section').has_value('EQ').else_use('Send Gain').with_name('Send').if_parameter('Section').has_value('Mix').else_use(''),
                          use('Ir Attack Time').with_name('Attack').if_parameter('Section').has_value('Convolution').else_use('Decay').if_parameter('Section').has_value('Algo').else_use('EQ Low Freq').with_name('Low Freq').if_parameter('Section').has_value('EQ').else_use('Blend').if_parameter('Section').has_value('Mix').else_use(''),
                          use('Ir Decay Time').with_name('Decay').if_parameter('Section').has_value('Convolution').else_use('Size').if_parameter('Section').has_value('Algo').else_use('EQ Low Gain').with_name('Low Gain').if_parameter('EQ Low Type').has_value('Shelf').and_parameter('Section').has_value('EQ').else_use('EQ Low Slope').with_name('Low Slope').if_parameter('EQ Low Type').has_value('Cut').and_parameter('Section').has_value('EQ').else_use('P.Dly Time').with_name('Predelay').if_parameter('P.Dly Sync').has_value('Off').else_use('P.Dly 16th').with_name('Predelay').if_parameter('P.Dly Sync').has_value('On').else_use(''),
                          use('Ir Size Factor').with_name('Size').if_parameter('Section').has_value('Convolution').else_use('Pr Low Mult').with_name('Low Mult').if_parameter('Algo Type').has_value('Prism').and_parameter('Section').has_value('Algo').else_use('Damping').if_parameter('Section').has_value('Algo').else_use('EQ High Freq').with_name('High Freq').if_parameter('Section').has_value('EQ').else_use('P.Dly Fb Time').with_name('Feedback').if_parameter('P.Dly Sync').has_value('Off').else_use('P.Dly Fb 16th').with_name('Feedback').if_parameter('P.Dly Sync').has_value('On').else_use(''),
                          use('').if_parameter('Section').has_value('Convolution').else_use('EQ High Gain').with_name('High Gain').if_parameter('EQ High Type').has_value('Shelf').and_parameter('Section').has_value('EQ').else_use('EQ High Slope').with_name('High Slope').if_parameter('EQ High Type').has_value('Cut').and_parameter('Section').has_value('EQ').else_use('Width').if_parameter('Section').has_value('Mix').else_use('Sh Shimmer').with_name('Shimmer').if_parameter('Algo Type').has_value('Shimmer').else_use('DH BassMult').with_name('Bass Mult').if_parameter('Algo Type').has_value('Dark Hall').else_use('Ti Rate').with_name('Rate').if_parameter('Algo Type').has_value('Tides').else_use('Pr High Mult').with_name('High Mult').if_parameter('Algo Type').has_value('Prism').else_use('Qz Low Damp').with_name('Low Damping').if_parameter('Algo Type').has_value('Quartz').else_use(''),
                          use('Routing Eq Off').with_name('Routing').if_parameter('EQ On').has_value('Off').else_use('Routing Eq On PreAlgo Off').with_name('Routing').if_parameter('EQ Pre Algo').has_value('Off').else_use('Routing Eq On PreAlgo On').with_name('Routing').if_parameter('EQ Pre Algo').has_value('On').else_use(''),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: (
                  '',
                  use('Shape').if_parameter('Section').has_value('Convolution').else_use('Low Type Switch').if_parameter('Section').has_value('EQ').else_use(''),
                  use('Ms Sync Switch').if_parameter('Section').has_value('Mix').else_use(''),
                  use('High Type Switch').if_parameter('Section').has_value('EQ').else_use(''),
                  '',
                  'Pre Algo',
                  '')}),
  (
   'Convolution',
   {BANK_PARAMETERS_KEY: (
                          'IR Category',
                          'IR',
                          use('Ir Attack Time').with_name('Attack'),
                          use('Ir Decay Time').with_name('Decay'),
                          use('Ir Size Factor').with_name('Size'),
                          'Blend',
                          use('Routing Eq Off').with_name('Routing').if_parameter('EQ On').has_value('Off').else_use('Routing Eq On PreAlgo Off').with_name('Routing').if_parameter('EQ Pre Algo').has_value('Off').else_use('Routing Eq On PreAlgo On').with_name('Routing').if_parameter('EQ Pre Algo').has_value('On').else_use(''),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: ('', 'Shape', '', '', '', 'Pre Algo', '')}),
  (
   'Algorithm Pg 1',
   {BANK_PARAMETERS_KEY: (
                          use('Algo Type').with_name('Type'),
                          use('Algo Delay').with_name('Delay'),
                          'Decay',
                          'Size',
                          use('DH Shape').with_name('Shape').if_parameter('Algo Type').has_value('Dark Hall').else_use('Qz Distance').with_name('Distance').if_parameter('Algo Type').has_value('Quartz').else_use('Sh Shimmer').with_name('Shimmer').if_parameter('Algo Type').has_value('Shimmer').else_use('Ti Tide').with_name('Tide').if_parameter('Algo Type').has_value('Tides').else_use('Pr Low Mult').with_name('Low Mult').if_parameter('Algo Type').has_value('Prism').else_use(''),
                          use('DH BassMult').with_name('Bass Mult').if_parameter('Algo Type').has_value('Dark Hall').else_use('Diffusion').if_parameter('Algo Type').has_value('Quartz').else_use('Diffusion').if_parameter('Algo Type').has_value('Shimmer').else_use('Ti Rate').with_name('Rate').if_parameter('Algo Type').has_value('Tides').else_use('Pr High Mult').with_name('High Mult').if_parameter('Algo Type').has_value('Prism').else_use(''),
                          use('Ti Waveform').with_name('Wave').if_parameter('Algo Type').has_value('Tides').else_use('Pr X Over').with_name('X Over').if_parameter('Algo Type').has_value('Prism').else_use('Modulation').with_name('Mod'),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: ('Freeze In', 'Freeze', '', '', '', '', '')}),
  (
   'Algorithm Pg 2',
   {BANK_PARAMETERS_KEY: (
                          use('Algo Type').with_name('Type'),
                          use('').if_parameter('Algo Type').has_value('Prism').else_use('Damping'),
                          use('DH Bass X').with_name('Bass X').if_parameter('Algo Type').has_value('Dark Hall').else_use('Qz Low Damp').with_name('Low Damping').if_parameter('Algo Type').has_value('Quartz').else_use('Sh Pitch Shift').with_name('Pitch').if_parameter('Algo Type').has_value('Shimmer').else_use('Ti Phase').with_name('Phase').if_parameter('Algo Type').has_value('Tides').else_use(''),
                          '',
                          use('Send Gain').with_name('Send'),
                          'Blend',
                          use('Routing Eq Off').with_name('Routing').if_parameter('EQ On').has_value('Off').else_use('Routing Eq On PreAlgo Off').with_name('Routing').if_parameter('EQ Pre Algo').has_value('Off').else_use('Routing Eq On PreAlgo On').with_name('Routing').if_parameter('EQ Pre Algo').has_value('On').else_use(''),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: ('Freeze In', 'Freeze', '', '', '', 'Pre Algo', '')}),
  (
   'EQ',
   {BANK_PARAMETERS_KEY: (
                          'Band',
                          use('EQ Low Freq').with_name('Low Freq').if_parameter('Band').has_value('1&4').else_use('EQ P1 Freq').with_name('2 Freq'),
                          use('').if_parameter('Band').has_value('1&4').else_use('EQ P1 Q').with_name('2 Q'),
                          use('EQ Low Gain').with_name('Low Gain').if_parameter('Band').has_value('1&4').and_parameter('EQ Low Type').has_value('Shelf').else_use('EQ Low Slope').with_name('Low Slope').if_parameter('Band').has_value('1&4').and_parameter('EQ Low Type').has_value('Cut').else_use('EQ P1 Gain').with_name('2 Gain'),
                          use('EQ High Freq').with_name('High Freq').if_parameter('Band').has_value('1&4').else_use('EQ P2 Freq').with_name('3 Freq'),
                          use('').if_parameter('Band').has_value('1&4').else_use('EQ P2 Q').with_name('3 Q'),
                          use('EQ High Gain').with_name('High Gain').if_parameter('Band').has_value('1&4').and_parameter('EQ High Type').has_value('Shelf').else_use('EQ High Slope').with_name('High Slope').if_parameter('Band').has_value('1&4').and_parameter('EQ High Type').has_value('Cut').else_use('EQ P2 Gain').with_name('3 Gain'),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: (
                  'EQ',
                  'Pre Algo',
                  use('Low Type Switch').if_parameter('Band').has_value('1&4').else_use(''),
                  '',
                  '',
                  use('High Type Switch').if_parameter('Band').has_value('1&4').else_use(''),
                  '')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: (
                          use('Send Gain').with_name('Send'),
                          use('P.Dly Time').with_name('Predelay').if_parameter('P.Dly Sync').has_value('Off').else_use('P.Dly 16th').with_name('Predelay'),
                          use('P.Dly Fb Time').with_name('Feedback').if_parameter('P.Dly Sync').has_value('Off').else_use('P.Dly Fb 16th').with_name('Feedback'),
                          use('Vintage Copy').with_name('Vintage'),
                          use('Width').with_name('Stereo'),
                          'Blend',
                          use('Routing Eq Off').with_name('Routing').if_parameter('EQ On').has_value('Off').else_use('Routing Eq On PreAlgo Off').with_name('Routing').if_parameter('EQ Pre Algo').has_value('Off').else_use('Routing Eq On PreAlgo On').with_name('Routing').if_parameter('EQ Pre Algo').has_value('On').else_use(''),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: ('Ms Sync Switch', 'EQ', 'Bass Mono', 'Freeze In', 'Freeze', 'Pre Algo', '')}))), 
 'InstrumentVector':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Oscillator',
                          use('Osc 1 Table').with_name('Table').if_parameter('Oscillator').has_value('1').else_use('Osc 2 Table').with_name('Table').if_parameter('Oscillator').has_value('2').else_use('Sub Gain').with_name('Gain').if_parameter('Oscillator').has_value('S').else_use('Osc 1 Gain').with_name('Gain 1').if_parameter('Oscillator').has_value('Mix').else_use(''),
                          use('Osc 1 Pos').with_name('Position').if_parameter('Oscillator').has_value('1').else_use('Osc 2 Pos').with_name('Position').if_parameter('Oscillator').has_value('2').else_use('Sub Tone').with_name('Tone').if_parameter('Oscillator').has_value('S').else_use('Osc 2 Gain').with_name('Gain 2').if_parameter('Oscillator').has_value('Mix').else_use(''),
                          use('Filter 1 Type').with_name('Filter Type').if_parameter('Internal Filter').has_value('1').else_use('Filter 2 Type').with_name('Filter Type').if_parameter('Internal Filter').has_value('2').else_use('Sub Transpose').with_name('Octave').if_parameter('Oscillator').has_value('S').else_use('Sub Gain').with_name('Gain Sub').if_parameter('Oscillator').has_value('Mix').else_use(''),
                          use('Filter 1 Freq').with_name('Frequency').if_parameter('Internal Filter').has_value('1').else_use('Filter 2 Freq').with_name('Frequency'),
                          use('Filter 1 Res').with_name('Resonance').if_parameter('Internal Filter').has_value('1').else_use('Filter 2 Res').with_name('Resonance'),
                          use('Time').with_name('Mod Time'),
                          use('Global Mod Amount').with_name('Mod Amt')), 
    
    OPTIONS_KEY: (
                  use('Osc').if_parameter('Oscillator').has_value('1').or_parameter('Oscillator').has_value('2').else_use('Sub').if_parameter('Oscillator').has_value('S'),
                  '',
                  'Filter Switch',
                  'Filter',
                  '',
                  '',
                  'Add to Matrix'), 
    
    VIEW_DESCRIPTION_KEY: 'mainbank_visualisation'}),
  (
   'Oscillators',
   {BANK_PARAMETERS_KEY: (
                          'Oscillator',
                          use('Osc 1 Category').with_name('Category').if_parameter('Oscillator').has_value('1').else_use('Osc 2 Category').with_name('Category').if_parameter('Oscillator').has_value('2').else_use('Sub Gain').with_name('Gain').if_parameter('Oscillator').has_value('S').else_use('Osc 1 Pitch').with_name('Pitch 1').if_parameter('Oscillator').has_value('Mix').else_use(''),
                          use('Osc 1 Table').with_name('Table').if_parameter('Oscillator').has_value('1').else_use('Osc 2 Table').with_name('Table').if_parameter('Oscillator').has_value('2').else_use('Sub Tone').with_name('Tone').if_parameter('Oscillator').has_value('S').else_use('Osc 2 Pitch').with_name('Pitch 2').if_parameter('Oscillator').has_value('Mix').else_use(''),
                          use('Osc 1 Pos').with_name('Position').if_parameter('Oscillator').has_value('1').else_use('Osc 2 Pos').with_name('Position').if_parameter('Oscillator').has_value('2').else_use('Sub Transpose').with_name('Octave').if_parameter('Oscillator').has_value('S').else_use('Sub Transpose').with_name('Octave Sub').if_parameter('Oscillator').has_value('Mix').else_use(''),
                          use('Osc 1 Gain').with_name('Gain 1').if_parameter('Oscillator').has_value('Mix').else_use('Osc 1 Pitch').with_name('Pitch').if_parameter('Oscillator').has_value('1').else_use('Osc 2 Pitch').with_name('Pitch').if_parameter('Oscillator').has_value('2'),
                          use('Osc 1 Effect Type').with_name('Effect Type').if_parameter('Oscillator').has_value('1').else_use('Osc 2 Effect Type').with_name('Effect Type').if_parameter('Oscillator').has_value('2').else_use('Osc 2 Gain').with_name('Gain 2').if_parameter('Oscillator').has_value('Mix').else_use(''),
                          use('Osc 1 Effect 1').with_name('Pulse Width').if_parameter('Oscillator').has_value('1').and_parameter('Osc 1 Effect Type').has_value('Classic').else_use('Osc 1 Effect 1').with_name('Warp').if_parameter('Oscillator').has_value('1').and_parameter('Osc 1 Effect Type').has_value('Modern').else_use('Osc 1 Effect 1').with_name('Pitch').if_parameter('Oscillator').has_value('1').and_parameter('Osc 1 Effect Type').has_value('Fm').else_use('Osc 2 Effect 1').with_name('Pulse Width').if_parameter('Oscillator').has_value('2').and_parameter('Osc 2 Effect Type').has_value('Classic').else_use('Osc 2 Effect 1').with_name('Warp').if_parameter('Oscillator').has_value('2').and_parameter('Osc 2 Effect Type').has_value('Modern').else_use('Osc 2 Effect 1').with_name('Pitch').if_parameter('Oscillator').has_value('2').and_parameter('Osc 2 Effect Type').has_value('Fm').else_use(''),
                          use('Osc 1 Effect 2').with_name('Sync').if_parameter('Oscillator').has_value('1').and_parameter('Osc 1 Effect Type').has_value('Classic').else_use('Osc 1 Effect 2').with_name('Fold').if_parameter('Oscillator').has_value('1').and_parameter('Osc 1 Effect Type').has_value('Modern').else_use('Osc 1 Effect 2').with_name('Amount').if_parameter('Oscillator').has_value('1').and_parameter('Osc 1 Effect Type').has_value('Fm').else_use('Osc 2 Effect 2').with_name('Sync').if_parameter('Oscillator').has_value('2').and_parameter('Osc 2 Effect Type').has_value('Classic').else_use('Osc 2 Effect 2').with_name('Fold').if_parameter('Oscillator').has_value('2').and_parameter('Osc 2 Effect Type').has_value('Modern').else_use('Osc 2 Effect 2').with_name('Amount').if_parameter('Oscillator').has_value('2').and_parameter('Osc 2 Effect Type').has_value('Fm').else_use('Sub Gain').with_name('Gain Sub').if_parameter('Oscillator').has_value('Mix').else_use('')), 
    
    OPTIONS_KEY: (
                  use('Osc').if_parameter('Oscillator').has_value('1').or_parameter('Oscillator').has_value('2').else_use('Sub').if_parameter('Oscillator').has_value('S'),
                  '',
                  '',
                  '',
                  '',
                  '',
                  'Add to Matrix'), 
    
    VIEW_DESCRIPTION_KEY: 'oscillators_visualisation'}),
  (
   'Filters',
   {BANK_PARAMETERS_KEY: (
                          'Filter',
                          use('Filter 1 On').with_name('Filter On').if_parameter('Filter').has_value('1').else_use('Filter 2 On').with_name('Filter On').if_parameter('Filter').has_value('2'),
                          use('Filter 1 Type').with_name('Filter Type').if_parameter('Filter').has_value('1').else_use('Filter 2 Type').with_name('Filter Type').if_parameter('Filter').has_value('2'),
                          use('Filter 1 Freq').with_name('Frequency').if_parameter('Filter').has_value('1').else_use('Filter 2 Freq').with_name('Frequency').if_parameter('Filter').has_value('2'),
                          use('Filter 1 Res').with_name('Resonance').if_parameter('Filter').has_value('1').else_use('Filter 2 Res').with_name('Resonance').if_parameter('Filter').has_value('2'),
                          use('Filter 1 LP/HP').with_name('Filter Circuit').if_parameter('Filter').has_value('1').and_parameter('Filter 1 Type').has_value('Lowpass').or_parameter('Filter 1 Type').has_value('Highpass').and_parameter('Filter').has_value('1').else_use('Filter 1 BP/NO/Morph').with_name('Filter Circuit').if_parameter('Filter').has_value('1').else_use('Filter 2 LP/HP').with_name('Filter Circuit').if_parameter('Filter').has_value('2').and_parameter('Filter 2 Type').has_value('Lowpass').or_parameter('Filter 2 Type').has_value('Highpass').and_parameter('Filter').has_value('2').else_use('Filter 2 BP/NO/Morph').with_name('Filter Circuit').if_parameter('Filter').has_value('2'),
                          use('Filter 1 Morph').with_name('Morph').if_parameter('Filter').has_value('1').and_parameter('Filter 1 Type').has_value('Morph').else_use('Filter 2 Morph').with_name('Morph').if_parameter('Filter').has_value('2').and_parameter('Filter 2 Type').has_value('Morph').else_use('Filter 1 Drive').with_name('Drive').if_parameter('Filter').has_value('1').and_parameter('Filter 1 Type').has_value('Lowpass').or_parameter('Filter 1 Type').has_value('Highpass').and_parameter('Filter 1 LP/HP').does_not_have_value('Clean').else_use('Filter 1 Drive').with_name('Drive').if_parameter('Filter').has_value('1').and_parameter('Filter 1 Type').has_value('Bandpass').or_parameter('Filter 1 Type').has_value('Notch').and_parameter('Filter 1 BP/NO/Morph').does_not_have_value('Clean').else_use('Filter 2 Drive').with_name('Drive').if_parameter('Filter').has_value('2').and_parameter('Filter 2 Type').has_value('Lowpass').or_parameter('Filter 2 Type').has_value('Highpass').and_parameter('Filter 2 LP/HP').does_not_have_value('Clean').else_use('Filter 2 Drive').with_name('Drive').if_parameter('Filter').has_value('2').and_parameter('Filter 2 Type').has_value('Bandpass').or_parameter('Filter 2 Type').has_value('Notch').and_parameter('Filter 2 BP/NO/Morph').does_not_have_value('Clean').else_use(''),
                          use('Filter Routing').with_name('Routing')), 
    
    OPTIONS_KEY: (
                  '',
                  use('Filter 1 Slope').if_parameter('Filter').has_value('1').else_use('Filter 2 Slope').if_parameter('Filter').has_value('2'),
                  '',
                  '',
                  '',
                  '',
                  'Add to Matrix')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: (
                          'Mono On',
                          use('Glide').if_parameter('Mono On').has_value('On').else_use('Poly Voices'),
                          'Unison Mode',
                          'Unison Voices',
                          'Unison Amount',
                          'Transpose',
                          '',
                          'Volume'), 
    
    OPTIONS_KEY: ('', '', '', '', '', '', 'Add to Matrix')}),
  (
   'Envelopes',
   {BANK_PARAMETERS_KEY: (
                          'Envelopes',
                          use('Amp Env View').with_name('Env View').if_parameter('Envelopes').has_value('Amp').else_use('Mod Env View').with_name('Env View'),
                          use('Amp Attack').with_name('Attack').if_parameter('Envelopes').has_value('Amp').and_parameter('Amp Env View').has_value('Time').else_use('Amp A Slope').with_name('Attack').if_parameter('Envelopes').has_value('Amp').and_parameter('Amp Env View').has_value('Slope').else_use('Env 2 Attack').with_name('Attack').if_parameter('Envelopes').has_value('Env2').and_parameter('Mod Env View').has_value('Time').else_use('Env 2 A Slope').with_name('Attack').if_parameter('Envelopes').has_value('Env2').and_parameter('Mod Env View').has_value('Slope').else_use('Env 2 Initial').with_name('Init').if_parameter('Envelopes').has_value('Env2').and_parameter('Mod Env View').has_value('Value').else_use('Env 3 Attack').with_name('Attack').if_parameter('Envelopes').has_value('Env3').and_parameter('Mod Env View').has_value('Time').else_use('Env 3 A Slope').with_name('Attack').if_parameter('Envelopes').has_value('Env3').and_parameter('Mod Env View').has_value('Slope').else_use('Env 3 Initial').with_name('Init').if_parameter('Envelopes').has_value('Env3').and_parameter('Mod Env View').has_value('Value'),
                          use('Amp Decay').with_name('Decay').if_parameter('Envelopes').has_value('Amp').and_parameter('Amp Env View').has_value('Time').else_use('Amp D Slope').with_name('Decay').if_parameter('Envelopes').has_value('Amp').and_parameter('Amp Env View').has_value('Slope').else_use('Env 2 Decay').with_name('Decay').if_parameter('Envelopes').has_value('Env2').and_parameter('Mod Env View').has_value('Time').else_use('Env 2 D Slope').with_name('Decay').if_parameter('Envelopes').has_value('Env2').and_parameter('Mod Env View').has_value('Slope').else_use('Env 2 Peak').with_name('Peak').if_parameter('Envelopes').has_value('Env2').and_parameter('Mod Env View').has_value('Value').else_use('Env 3 Decay').with_name('Decay').if_parameter('Envelopes').has_value('Env3').and_parameter('Mod Env View').has_value('Time').else_use('Env 3 D Slope').with_name('Decay').if_parameter('Envelopes').has_value('Env3').and_parameter('Mod Env View').has_value('Slope').else_use('Env 3 Peak').with_name('Peak').if_parameter('Envelopes').has_value('Env3').and_parameter('Mod Env View').has_value('Value'),
                          use('Amp Sustain').with_name('Sustain').if_parameter('Envelopes').has_value('Amp').else_use('Env 2 Sustain').with_name('Sustain').if_parameter('Envelopes').has_value('Env2').else_use('Env 3 Sustain').with_name('Sustain').if_parameter('Envelopes').has_value('Env3'),
                          use('Amp Release').with_name('Release').if_parameter('Envelopes').has_value('Amp').and_parameter('Amp Env View').has_value('Time').else_use('Amp R Slope').with_name('Release').if_parameter('Envelopes').has_value('Amp').and_parameter('Amp Env View').has_value('Slope').else_use('Env 2 Release').with_name('Release').if_parameter('Envelopes').has_value('Env2').and_parameter('Mod Env View').has_value('Time').else_use('Env 2 R Slope').with_name('Release').if_parameter('Envelopes').has_value('Env2').and_parameter('Mod Env View').has_value('Slope').else_use('Env 2 Final').with_name('Final').if_parameter('Envelopes').has_value('Env2').and_parameter('Mod Env View').has_value('Value').else_use('Env 3 Release').with_name('Release').if_parameter('Envelopes').has_value('Env3').and_parameter('Mod Env View').has_value('Time').else_use('Env 3 R Slope').with_name('Release').if_parameter('Envelopes').has_value('Env3').and_parameter('Mod Env View').has_value('Slope').else_use('Env 3 Final').with_name('Final').if_parameter('Envelopes').has_value('Env3').and_parameter('Mod Env View').has_value('Value'),
                          use('Amp Loop Mode').with_name('Loop').if_parameter('Envelopes').has_value('Amp').else_use('Env 2 Loop Mode').with_name('Loop').if_parameter('Envelopes').has_value('Env2').else_use('Env 3 Loop Mode').with_name('Loop').if_parameter('Envelopes').has_value('Env3'),
                          ''), 
    
    OPTIONS_KEY: ('', '', '', '', '', '', 'Add to Matrix')}),
  (
   'LFOs',
   {BANK_PARAMETERS_KEY: (
                          'LFO',
                          use('LFO 1 Shape').with_name('LFO Type').if_parameter('LFO').has_value('LFO1').else_use('LFO 2 Shape').with_name('LFO Type').if_parameter('LFO').has_value('LFO2'),
                          use('LFO 1 Shaping').with_name('Shape').if_parameter('LFO').has_value('LFO1').else_use('LFO 2 Shaping').with_name('Shape').if_parameter('LFO').has_value('LFO2'),
                          use('LFO 1 Rate').with_name('Rate').if_parameter('LFO').has_value('LFO1').and_parameter('LFO 1 Sync').has_value('Free').else_use('LFO 1 S. Rate').with_name('Rate').if_parameter('LFO').has_value('LFO1').and_parameter('LFO 1 Sync').has_value('Tempo').else_use('LFO 2 Rate').with_name('Rate').if_parameter('LFO').has_value('LFO2').and_parameter('LFO 2 Sync').has_value('Free').else_use('LFO 2 S. Rate').with_name('Rate').if_parameter('LFO').has_value('LFO2').and_parameter('LFO 2 Sync').has_value('Tempo'),
                          use('LFO 1 Amount').with_name('Amount').if_parameter('LFO').has_value('LFO1').else_use('LFO 2 Amount').with_name('Amount').if_parameter('LFO').has_value('LFO2'),
                          use('LFO 1 Attack Time').with_name('Attack').if_parameter('LFO').has_value('LFO1').else_use('LFO 2 Attack Time').with_name('Attack').if_parameter('LFO').has_value('LFO2'),
                          use('LFO 1 Phase Offset').with_name('Offset').if_parameter('LFO').has_value('LFO1').else_use('LFO 2 Phase Offset').with_name('Offset').if_parameter('LFO').has_value('LFO2'),
                          use('LFO 1 Retrigger').with_name('Retrigger').if_parameter('LFO').has_value('LFO1').else_use('LFO 2 Retrigger').with_name('Retrigger').if_parameter('LFO').has_value('LFO2')), 
    
    OPTIONS_KEY: (
                  '',
                  '',
                  use('LFO 1 Sync').if_parameter('LFO').has_value('LFO1').else_use('LFO 2 Sync').if_parameter('LFO').has_value('LFO2'),
                  '',
                  '',
                  '',
                  'Add to Matrix')}),
  (
   'Matrix',
   {BANK_PARAMETERS_KEY: (
                          'Modulation Target Names',
                          'Current Mod Target',
                          '',
                          use('Amp Env Mod Amount').with_name('Amp Env'),
                          use('Env 2 Mod Amount').with_name('Env 2'),
                          use('Env 3 Mod Amount').with_name('Env 3'),
                          use('Lfo 1 Mod Amount').with_name('LFO 1'),
                          use('Lfo 2 Mod Amount').with_name('LFO 2')), 
    
    OPTIONS_KEY: ('Back', '', 'Go to Amp Env', 'Go to Env 2', 'Go to Env 3', 'Go to LFO 1', 'Go to LFO 2')}),
  (
   'MIDI',
   {BANK_PARAMETERS_KEY: (
                          'Modulation Target Names',
                          'Current Mod Target',
                          use('MIDI Velocity Mod Amount').with_name('Velocity'),
                          use('MIDI Note Mod Amount').with_name('Pitch'),
                          use('MIDI Pitch Bend Mod Amount').with_name('Pitch Bend'),
                          use('MIDI Aftertouch Mod Amount').with_name('Aftertouch'),
                          use('MIDI Mod Wheel Mod Amount').with_name('Mod Wheel'),
                          use('MIDI Random On Note On').with_name('Random')), 
    
    OPTIONS_KEY: ('Back', '', '', '', '', '', '')}))), 
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
                          'Groove',
                          'Offset',
                          'Repeats',
                          'Gate',
                          'Retrigger Mode',
                          use('Ret. Interval').if_parameter('Retrigger Mode').has_value('Beat'))}),
  (
   'Pitch/Vel.',
   {BANK_PARAMETERS_KEY: ('Tranpose Mode', 'Tranpose Key', 'Transp. Steps', 'Transp. Dist.', 'Velocity On',
 'Vel. Retrigger', 'Velocity Decay', 'Velocity Target')}))), 
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
                          'On/Off-Balance',
                          'Decay Time',
                          'Decay Key Scale',
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
   {BANK_PARAMETERS_KEY: ('Mode', 'Drive', 'Compand', 'Out Hi', 'Out Low', 'Range', 'Lowest', 'Random')}),)), 
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
                          use('Morph').if_parameter('Filter Type').has_value('Morph').else_use('').if_parameter('Filter Type').has_value('Lowpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Highpass').and_parameter('Filter Circuit - LP/HP').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Bandpass').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('').if_parameter('Filter Type').has_value('Notch').and_parameter('Filter Circuit - BP/NO/Morph').has_value('Clean').else_use('Drive'),
                          'LFO Amount',
                          'LFO Sync',
                          use('LFO Frequency').if_parameter('LFO Sync').has_value('Free').else_use('LFO Sync Rate')), 
    
    OPTIONS_KEY: (
                  use('Slope').if_parameter('Slope').is_available(True),
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '')}),
  (
   'Envelope',
   {BANK_PARAMETERS_KEY: (
                          use('Filter Type').if_parameter('Filter Type').is_available(True).else_use('Filter Type (Legacy)'),
                          use('Frequency'),
                          use('Resonance').if_parameter('Resonance').is_available(True).else_use('Resonance (Legacy)'),
                          use('Morph').if_parameter('Filter Type').has_value('Morph SVF').else_use('Drive'),
                          'Env. Attack',
                          'Env. Release',
                          'Env. Modulation',
                          '')}),
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
                          'LFO Quantize Rate')}),
  (
   'Sidechain',
   {BANK_PARAMETERS_KEY: ('S/C On', 'S/C Mix', 'S/C Gain', '', '', '', '', '')}))), 
<<<<<<< HEAD
 'SubZero':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('Oscillator1 Type').with_name('Osc 1 Wave'),
                          use('Oscillator1 Shape').with_name('Osc 1 Shape'),
                          use('Oscillator1 ShapeMod').with_name('Shape Mod'),
                          use('Osc Gain 2').with_name('Osc 2 Gain '),
                          use('Filter Freq').with_name('LP Freq'),
                          use('Filter Res').with_name('LP Reso'),
                          use('EG1 Attack').with_name('Env 1 Attack'),
                          use('EG1 Release').with_name('Env 1 Release')), 
    
    OPTIONS_KEY: ('', '', 'Oscillator2 Type', '', '', '', '')}),
  (
   'Oscillator',
   {BANK_PARAMETERS_KEY: (
                          use('Oscillator1 Type').with_name('Osc 1 Wave'),
                          use('Oscillator1 Shape').with_name('Osc 1 Shape'),
                          use('Oscillator1 Transpose').with_name('Osc 1 Octave'),
                          use('Oscillator2 Transpose').with_name('Osc 2 Octave'),
                          use('Oscillator2 Detune').with_name('Osc 2 Detune'),
                          use('Osc Gain 1').with_name('Osc 1 Gain'),
                          use('Osc Gain 2').with_name('Osc 2 Gain'),
                          use('Noise Level').with_name('Noise Gain')), 
    
    OPTIONS_KEY: ('Osc Retrig', '', 'Oscillator2 Type', '', 'Osc 1', 'Osc 2', 'Noise')}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: (
                          '',
                          use('Filter Freq').with_name('LP Freq'),
                          use('Filter Res').with_name('LP Reso'),
                          use('Filter HiPassFreq').with_name('HP Freq'),
                          '',
                          use('Filter ModAmount1').with_name('LP Mod Amt 1'),
                          '',
                          use('Filter ModAmount2').with_name('LP Mod Amt 2')), 
    
    OPTIONS_KEY: ('Osc 1 Flt', 'Osc 2 Flt', 'Filter Noise', '', '', '')}),
  (
   'Envelopes',
   {BANK_PARAMETERS_KEY: (
                          use('EG1 Attack').with_name('Env 1 Attack'),
                          use('EG1 Decay').with_name('Env 1 Decay'),
                          use('EG1 Sustain').with_name('Env 1 Sustain'),
                          use('EG1 Release').with_name('Env 1 Release'),
                          use('EG2 Attack').with_name('Env 2 Attack'),
                          use('EG2 Decay').with_name('Env 2 Decay'),
                          use('EG2 Sustain').with_name('Env 2 Sustain'),
                          use('EG2 Release').with_name('Env 2 Release'))}),
  (
   'LFOs',
   {BANK_PARAMETERS_KEY: (
                          use('Lfo Shape').with_name('LFO Wave'),
                          '',
                          use('Lfo Rate').with_name('LFO Rate'),
                          use('Lfo Amount').with_name('LFO Amount'),
                          use('Lfo ModAmount').with_name('LFO Mod Amt'),
                          use('CyclingEG MidPoint').with_name('Cyc Env Tilt'),
                          use('CyclingEG Hold').with_name('Cyc Env Hold'),
                          use('CyclingEG Rate').with_name('Cyc Env Rate')), 
    
    OPTIONS_KEY: ('LFO Retrig', '', '', '', '', '', '')}),
  (
   'Modulation',
   {BANK_PARAMETERS_KEY: (
                          use('Oscillator1 ShapeMod').with_name('Shape Mod Amt'),
                          use('PitchMod Amt1').with_name('P Mod Amt 1'),
                          use('PitchMod Amt2').with_name('P Mod Amt 2'),
                          use('Filter ModAmount1').with_name('LP Mod Amt 1'),
                          use('Filter ModAmount2').with_name('LP Mod Amt 2'),
                          use('Lfo ModAmount').with_name('LFO Mod Amt'),
                          use('ModMatrix Amount 1').with_name('Custom Mod 1'),
                          use('ModMatrix Amount 2').with_name('Custom Mod 2'))}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: (
                          '',
                          '',
                          '',
                          use('Global Glide').with_name('Glide Time'),
                          '',
                          use('Global Drift Depth').with_name('Drift'),
                          use('Global Transpose').with_name('Transpose'),
                          use('Global Volume').with_name('Volume')), 
    
    OPTIONS_KEY: ('', '', 'Legato', '', '', '', '')}))), 
=======
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
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
                          use('Width (Random)').if_parameter('Waveform').has_value('S&H Width').else_use('Stereo Mode').if_parameter('LFO Type').has_value('Frequency').else_use('Offset'),
                          use('').if_parameter('Waveform').has_value('S&H Width').else_use('Phase').if_parameter('LFO Type').has_value('Beats').else_use('Spin').if_parameter('Stereo Mode').has_value('Spin').else_use('Phase'))}),)), 
 'BeatRepeat':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Grid', 'Interval', 'Offset', 'Gate', 'Pitch', 'Pitch Decay', 'Variation', 'Chance')}),
  (
   'Filt/Mix',
   {BANK_PARAMETERS_KEY: ('Filter On', 'Filter Freq', 'Filter Width', '', 'Mix Type', 'Volume', 'Decay', 'Chance')}),
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
 'Chorus2':IndexedDict((
  (
   'Main',
   {BANK_PARAMETERS_KEY: (
                          'Mode',
                          'Rate',
                          'Amount',
                          use('Offset').if_parameter('Mode').has_value('Vibrato').else_use('Width'),
<<<<<<< HEAD
                          use('Shape').if_parameter('Mode').has_value('Vibrato').else_use(''),
=======
                          use('Shaping').if_parameter('Mode').has_value('Vibrato').else_use(''),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          use('HPF Freq').with_name('HP Freq'),
                          use('').if_parameter('Mode').has_value('Vibrato').else_use('Feedback'),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: (
                  '',
                  '',
                  '',
                  '',
                  'High Pass',
                  use('').if_parameter('Mode').has_value('Vibrato').else_use('FB Inv'),
                  '')}),
  (
   'Mix',
   {BANK_PARAMETERS_KEY: ('Gain', 'Warmth', '', '', '', '', '', 'Dry/Wet')}))), 
 'Compressor2':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('Expansion Ratio').if_parameter('Model').has_value('Expand').else_use('Ratio'),
                          'Threshold',
                          'Attack',
                          'Release',
                          'Knee',
                          'Model',
                          'Dry/Wet',
                          'Output Gain'), 
    
    OPTIONS_KEY: ('', '', 'Auto Release', '', '', '', 'Makeup'), 
    VIEW_DESCRIPTION_KEY: 'activity'}),
  (
   'Sidechain',
   {BANK_PARAMETERS_KEY: ('Input Type', 'Input Channel', 'Input Channel', 'Input Channel', 'Input Channel',
 'Position', 'S/C Mix', 'S/C Gain'), 
    
    OPTIONS_KEY: ('Sidechain', 'Listen', '', '', '', '', ''), 
    VIEW_DESCRIPTION_KEY: 'routing'}),
  (
   'Sidechain EQ',
   {BANK_PARAMETERS_KEY: (
                          'S/C EQ On',
                          'S/C EQ Type',
                          'S/C EQ Freq',
                          use('S/C EQ Q').if_parameter('S/C EQ Type').has_value('Low pass').or_parameter('S/C EQ Type').has_value('Peak').or_parameter('S/C EQ Type').has_value('High pass').else_use('S/C EQ Gain'),
                          '',
                          '',
                          'S/C Mix',
                          'S/C Gain'), 
    
    OPTIONS_KEY: ('Sidechain', 'Listen', '', '', '', '', '')}))), 
 'Corpus':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Resonance Type',
                          'Decay',
                          use('Radius').if_parameter('Resonance Type').has_value('Tube').or_parameter('Resonance Type').has_value('Pipe').else_use('Material'),
                          use('').if_parameter('Resonance Type').has_value('Tube').else_use('').if_parameter('Resonance Type').has_value('Pipe').else_use('Brightness'),
                          use('').if_parameter('Resonance Type').has_value('Tube').else_use('Opening').if_parameter('Resonance Type').has_value('Pipe').else_use('Inharmonics'),
                          use('Transpose').if_parameter('MIDI Frequency').has_value('On').else_use('Tune'),
                          use('Fine').if_parameter('MIDI Frequency').has_value('On').else_use(''),
                          'Dry Wet')}),
  (
   'Body',
   {BANK_PARAMETERS_KEY: (
                          'Width',
                          use('').if_parameter('Resonance Type').has_value('Tube').or_parameter('Resonance Type').has_value('Pipe').else_use('Hit'),
                          use('').if_parameter('Resonance Type').has_value('Tube').or_parameter('Resonance Type').has_value('Pipe').else_use('Listening L'),
                          use('').if_parameter('Resonance Type').has_value('Tube').or_parameter('Resonance Type').has_value('Pipe').else_use('Listening R'),
                          use('Ratio').if_parameter('Resonance Type').has_value('Plate').or_parameter('Resonance Type').has_value('Membrane'),
                          use('').if_parameter('Resonance Type').has_value('Tube').or_parameter('Resonance Type').has_value('Pipe').else_use('Resonator Quality').with_name('Res Quality'),
                          '',
                          'Dry Wet')}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          'LFO On/Off',
                          use('LFO Shape').if_parameter('LFO On/Off').has_value('On').else_use(''),
                          use('LFO Amount').if_parameter('LFO On/Off').has_value('On').else_use(''),
                          use('LFO Sync').if_parameter('LFO On/Off').has_value('On').else_use(''),
                          use('').if_parameter('LFO On/Off').has_value('Off').else_use('LFO Rate').if_parameter('LFO Sync').has_value('Free').else_use('LFO Sync Rate'),
                          use('').if_parameter('LFO On/Off').has_value('Off').else_use('LFO Stereo Mode').if_parameter('LFO Sync').has_value('Free').else_use('Offset'),
                          use('').if_parameter('LFO On/Off').has_value('Off').else_use('Phase').if_parameter('LFO Sync').has_value('Sync').else_use('Spin').if_parameter('LFO Stereo Mode').has_value('Spin'),
                          '')}),
  (
   'Tune & Sidechain',
   {BANK_PARAMETERS_KEY: (
                          use('MIDI Frequency').with_name('MIDI Freq'),
                          'MIDI Mode',
                          use('PB Range').if_parameter('MIDI Frequency').has_value('On').else_use(''),
                          use('Off Decay').if_parameter('Note Off').has_value('On').else_use(''),
                          '',
                          use('Transpose').if_parameter('MIDI Frequency').has_value('On').else_use('Tune'),
                          use('Fine').if_parameter('MIDI Frequency').has_value('On').else_use(''),
                          'Spread'), 
    
    OPTIONS_KEY: ('', '', 'Off Decay', '', '', '', '', '')}),
  (
   'Filter & Mix',
   {BANK_PARAMETERS_KEY: (
                          'Filter On/Off',
<<<<<<< HEAD
                          use('Mid Freq').with_name('Frequency').if_parameter('Filter On/Off').has_value('On').else_use(''),
                          use('Width').with_name('Bandwidth').if_parameter('Filter On/Off').has_value('On').else_use(''),
=======
                          use('Mid Freq').with_name('Frequency').else_use(''),
                          use('Width').with_name('Bandwidth').else_use(''),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          '',
                          '',
                          'Bleed',
                          'Gain',
                          'Dry Wet')}))), 
 'Delay':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Channel',
                          use('L Sync Enum').with_name('Sync').if_parameter('Channel').has_value('L+R').else_use('L Sync Enum').with_name('L Sync').if_parameter('Channel').has_value('Left').else_use('R Sync Enum').with_name('R Sync').if_parameter('Channel').has_value('Right'),
                          use('L 16th').with_name('16th').if_parameter('L Sync').has_value('On').and_parameter('Channel').has_value('L+R').else_use('L Time').with_name('Time').if_parameter('Channel').has_value('L+R').else_use('L 16th').if_parameter('L Sync').has_value('On').and_parameter('Channel').has_value('Left').else_use('L Time').if_parameter('Channel').has_value('Left').else_use('R 16th').if_parameter('R Sync').has_value('On').and_parameter('Channel').has_value('Right').else_use('R Time').if_parameter('Channel').has_value('Right'),
                          use('L Offset').with_name('Offset').if_parameter('Channel').has_value('L+R').else_use('L Offset').if_parameter('Channel').has_value('Left').else_use('R Offset').if_parameter('Channel').has_value('Right'),
                          'Filter Freq',
                          'Filter Width',
                          'Feedback',
                          'Dry/Wet'), 
    
    OPTIONS_KEY: ('', '', '', 'Filter', '', 'Freeze', '')}),
  (
   'Time',
   {BANK_PARAMETERS_KEY: (
                          use('Link Switch').with_name('Channel'),
                          use('L 16th').if_parameter('L Sync').has_value('On').else_use('L Time'),
                          use('L Offset'),
                          use('R 16th').if_parameter('R Sync').has_value('On').else_use('R Time'),
                          'R Offset',
                          'Ping Pong',
                          'Feedback',
                          'Dry/Wet'), 
    
    OPTIONS_KEY: ('L Delay Sync', '', 'R Delay Sync', '', 'Delay Mode', 'Freeze', '')}),
  (
   'Filter/Mod',
   {BANK_PARAMETERS_KEY: ('Filter Freq', 'Filter Width', 'Mod Freq', 'Dly < Mod', 'Filter < Mod', 'Ping Pong',
 'Feedback', 'Dry/Wet'), 
    
    OPTIONS_KEY: ('Filter', '', '', '', '', 'Freeze', '')}))), 
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
                          use('R Time').with_name('S Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('Channel Toggle').has_value('Right').and_parameter('Link').has_value('Off').and_parameter('R Sync').has_value('Off').else_use('R Time').if_parameter('Channel Toggle').has_value('Right').and_parameter('Link').has_value('Off').and_parameter('R Sync').has_value('Off').else_use('R 16th').with_name('S 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('Channel Toggle').has_value('Right').and_parameter('Link').has_value('Off').and_parameter('R Sync Mode').has_value('16th').else_use('R 16th').if_parameter('Channel Toggle').has_value('Right').and_parameter('Link').has_value('Off').and_parameter('R Sync Mode').has_value('16th').else_use('R Division').with_name('S Division').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('Channel Toggle').has_value('Right').and_parameter('Link').has_value('Off').else_use('R Division').if_parameter('Channel Toggle').has_value('Right').and_parameter('Link').has_value('Off').else_use('L Time').with_name('M Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync').has_value('Off').else_use('L Time').if_parameter('L Sync').has_value('Off').else_use('L 16th').with_name('M 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync Mode').has_value('16th').else_use('L 16th').if_parameter('L Sync Mode').has_value('16th').else_use('L Division').with_name('M Division').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Division'),
                          use('R Sync Mode').with_name('S Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('Channel Toggle').has_value('Right').and_parameter('Link').has_value('Off').else_use('R Sync Mode').if_parameter('Channel Toggle').has_value('Right').and_parameter('Link').has_value('Off').else_use('L Sync Mode').with_name('M Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync Mode'),
                          'Feedback',
                          'Input Gain',
                          'HP Freq',
                          'LP Freq',
                          'Output Gain',
                          'Dry Wet'), 
    
    OPTIONS_KEY: (
                  use('M/S Switch').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('Link').has_value('Off').else_use('L/R Switch').if_parameter('Link').has_value('Off').else_use('M Sync').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync'),
                  'Invert',
                  'Clip Dry',
                  'Filter',
                  '',
                  '',
                  '')}),
  (
   'Delay',
   {BANK_PARAMETERS_KEY: (
                          use('L Time').with_name('M Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync').has_value('Off').else_use('L Time').if_parameter('L Sync').has_value('Off').else_use('L 16th').with_name('M 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync Mode').has_value('16th').else_use('L 16th').if_parameter('L Sync Mode').has_value('16th').else_use('L Division').with_name('M Division').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Division'),
                          use('L Sync Mode').with_name('M Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync Mode'),
                          use('L Offset').with_name('M Offset').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Offset'),
                          'Channel Mode',
                          'Feedback',
                          use('R Offset').with_name('S Offset').if_parameter('Channel Mode').has_value('Mid/Side').else_use('R Offset'),
                          use('R Sync Mode').with_name('S Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('Link').has_value('Off').else_use('R Sync Mode').if_parameter('Link').has_value('Off').else_use('L Sync Mode').with_name('M Sync Mode').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync Mode'),
                          use('R Time').with_name('S Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('R Sync').has_value('Off').and_parameter('Link').has_value('Off').else_use('R Time').if_parameter('R Sync').has_value('Off').and_parameter('Link').has_value('Off').else_use('R 16th').with_name('S 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('R Sync Mode').has_value('16th').and_parameter('Link').has_value('Off').else_use('R 16th').if_parameter('R Sync Mode').has_value('16th').and_parameter('Link').has_value('Off').else_use('R Division').with_name('S Division').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('R Sync Mode').does_not_have_value('16th').and_parameter('Link').has_value('Off').else_use('R Division').if_parameter('R Sync Mode').does_not_have_value('16th').and_parameter('Link').has_value('Off').else_use('L Time').with_name('M Time').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync').has_value('Off').else_use('L Time').if_parameter('L Sync').has_value('Off').else_use('L 16th').with_name('M 16th').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('L Sync Mode').has_value('16th').else_use('L 16th').if_parameter('L Sync Mode').has_value('16th').else_use('L Division').with_name('M Division').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Division')), 
    
    OPTIONS_KEY: (
                  use('M Sync').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync'),
                  '',
                  'Link',
                  'Invert',
                  '',
                  use('S Sync').if_parameter('Channel Mode').has_value('Mid/Side').and_parameter('Link').has_value('Off').else_use('R Sync').if_parameter('Link').has_value('Off').else_use('M Sync').if_parameter('Channel Mode').has_value('Mid/Side').else_use('L Sync'),
                  '')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Repitch', 'Reverb Level', 'Reverb Decay', 'Channel Mode', 'Stereo Width', 'Input Gain',
 'Output Gain', 'Dry Wet'), 
    
    OPTIONS_KEY: ('', 'Reverb Loc', '', '', 'Clip Dry', '', '')}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: ('Filter On', 'HP Freq', 'HP Res', 'LP Freq', 'LP Res', 'Input Gain', 'Output Gain',
 'Dry Wet'), 
    
    OPTIONS_KEY: ('', '', '', '', 'Clip Dry', '', '')}),
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
                          'Dry Wet'), 
    
    OPTIONS_KEY: ('', '', '', '', 'Mod 4x', '', '')}),
  (
   'Character',
   {BANK_PARAMETERS_KEY: ('Gate Thr', 'Gate Release', 'Duck Thr', 'Duck Release', 'Noise Amt', 'Noise Mrph',
 'Wobble Amt', 'Wobble Mrph'), 
    
    OPTIONS_KEY: ('Gate', 'Duck', '', 'Noise', '', 'Wobble', '')}))), 
 'Eq8':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Band',
                          use('1 Filter On B').if_parameter('Band').has_value('1').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Filter On A').if_parameter('Band').has_value('1').else_use('2 Filter On B').if_parameter('Band').has_value('2').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Filter On A').if_parameter('Band').has_value('2').else_use('3 Filter On B').if_parameter('Band').has_value('3').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Filter On A').if_parameter('Band').has_value('3').else_use('4 Filter On B').if_parameter('Band').has_value('4').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Filter On A').if_parameter('Band').has_value('4').else_use('5 Filter On B').if_parameter('Band').has_value('5').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('5 Filter On A').if_parameter('Band').has_value('5').else_use('6 Filter On B').if_parameter('Band').has_value('6').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('6 Filter On A').if_parameter('Band').has_value('6').else_use('7 Filter On B').if_parameter('Band').has_value('7').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('7 Filter On A').if_parameter('Band').has_value('7').else_use('8 Filter On B').if_parameter('Band').has_value('8').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('8 Filter On A').if_parameter('Band').has_value('8'),
                          use('1 Filter Type B').if_parameter('Band').has_value('1').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Filter Type A').if_parameter('Band').has_value('1').else_use('2 Filter Type B').if_parameter('Band').has_value('2').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Filter Type A').if_parameter('Band').has_value('2').else_use('3 Filter Type B').if_parameter('Band').has_value('3').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Filter Type A').if_parameter('Band').has_value('3').else_use('4 Filter Type B').if_parameter('Band').has_value('4').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Filter Type A').if_parameter('Band').has_value('4').else_use('5 Filter Type B').if_parameter('Band').has_value('5').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('5 Filter Type A').if_parameter('Band').has_value('5').else_use('6 Filter Type B').if_parameter('Band').has_value('6').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('6 Filter Type A').if_parameter('Band').has_value('6').else_use('7 Filter Type B').if_parameter('Band').has_value('7').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('7 Filter Type A').if_parameter('Band').has_value('7').else_use('8 Filter Type B').if_parameter('Band').has_value('8').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('8 Filter Type A').if_parameter('Band').has_value('8'),
                          use('1 Frequency B').if_parameter('Band').has_value('1').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Frequency A').if_parameter('Band').has_value('1').else_use('2 Frequency B').if_parameter('Band').has_value('2').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Frequency A').if_parameter('Band').has_value('2').else_use('3 Frequency B').if_parameter('Band').has_value('3').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Frequency A').if_parameter('Band').has_value('3').else_use('4 Frequency B').if_parameter('Band').has_value('4').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Frequency A').if_parameter('Band').has_value('4').else_use('5 Frequency B').if_parameter('Band').has_value('5').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('5 Frequency A').if_parameter('Band').has_value('5').else_use('6 Frequency B').if_parameter('Band').has_value('6').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('6 Frequency A').if_parameter('Band').has_value('6').else_use('7 Frequency B').if_parameter('Band').has_value('7').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('7 Frequency A').if_parameter('Band').has_value('7').else_use('8 Frequency B').if_parameter('Band').has_value('8').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('8 Frequency A').if_parameter('Band').has_value('8'),
                          use('1 Resonance B').if_parameter('Band').has_value('1').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Resonance A').if_parameter('Band').has_value('1').else_use('2 Resonance B').if_parameter('Band').has_value('2').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Resonance A').if_parameter('Band').has_value('2').else_use('3 Resonance B').if_parameter('Band').has_value('3').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Resonance A').if_parameter('Band').has_value('3').else_use('4 Resonance B').if_parameter('Band').has_value('4').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Resonance A').if_parameter('Band').has_value('4').else_use('5 Resonance B').if_parameter('Band').has_value('5').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('5 Resonance A').if_parameter('Band').has_value('5').else_use('6 Resonance B').if_parameter('Band').has_value('6').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('6 Resonance A').if_parameter('Band').has_value('6').else_use('7 Resonance B').if_parameter('Band').has_value('7').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('7 Resonance A').if_parameter('Band').has_value('7').else_use('8 Resonance B').if_parameter('Band').has_value('8').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('8 Resonance A').if_parameter('Band').has_value('8'),
                          use('1 Gain B').if_parameter('Band').has_value('1').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Gain A').if_parameter('Band').has_value('1').else_use('2 Gain B').if_parameter('Band').has_value('2').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Gain A').if_parameter('Band').has_value('2').else_use('3 Gain B').if_parameter('Band').has_value('3').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Gain A').if_parameter('Band').has_value('3').else_use('4 Gain B').if_parameter('Band').has_value('4').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Gain A').if_parameter('Band').has_value('4').else_use('5 Gain B').if_parameter('Band').has_value('5').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('5 Gain A').if_parameter('Band').has_value('5').else_use('6 Gain B').if_parameter('Band').has_value('6').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('6 Gain A').if_parameter('Band').has_value('6').else_use('7 Gain B').if_parameter('Band').has_value('7').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('7 Gain A').if_parameter('Band').has_value('7').else_use('8 Gain B').if_parameter('Band').has_value('8').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('8 Gain A').if_parameter('Band').has_value('8'),
                          'Scale',
                          'Output Gain'), 
    
    OPTIONS_KEY: (
                  use('Left/Right').if_parameter('Eq Mode').has_value('Left/Right').else_use('Mid/Side').if_parameter('Eq Mode').has_value('Mid/Side').else_use(''),
                  '',
                  '',
                  '',
                  '',
                  '',
                  '')}),
  (
   '4 Band',
   {BANK_PARAMETERS_KEY: (
                          use('1 Frequency B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Frequency A'),
                          use('1 Gain B').if_parameter('1 Filter Type B').has_value('Low Shelf').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Gain B').if_parameter('1 Filter Type B').has_value('Bell').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Gain B').if_parameter('1 Filter Type B').has_value('High Shelf').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Resonance B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Gain A').if_parameter('1 Filter Type A').has_value('Low Shelf').or_parameter('1 Filter Type A').has_value('Bell').or_parameter('1 Filter Type A').has_value('High Shelf').else_use('1 Resonance A'),
                          use('2 Frequency B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Frequency A'),
                          use('2 Gain B').if_parameter('2 Filter Type B').has_value('Low Shelf').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Gain B').if_parameter('2 Filter Type B').has_value('Bell').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Gain B').if_parameter('2 Filter Type B').has_value('High Shelf').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Resonance B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Gain A').if_parameter('2 Filter Type A').has_value('Low Shelf').or_parameter('2 Filter Type A').has_value('Bell').or_parameter('2 Filter Type A').has_value('High Shelf').else_use('2 Resonance A'),
                          use('3 Frequency B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Frequency A'),
                          use('3 Gain B').if_parameter('3 Filter Type B').has_value('Low Shelf').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Gain B').if_parameter('3 Filter Type B').has_value('Bell').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Gain B').if_parameter('3 Filter Type B').has_value('High Shelf').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Resonance B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Gain A').if_parameter('3 Filter Type A').has_value('Low Shelf').or_parameter('3 Filter Type A').has_value('Bell').or_parameter('3 Filter Type A').has_value('High Shelf').else_use('3 Resonance A'),
                          use('4 Frequency B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Frequency A'),
                          use('4 Gain B').if_parameter('4 Filter Type B').has_value('Low Shelf').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Gain B').if_parameter('4 Filter Type B').has_value('Bell').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Gain B').if_parameter('4 Filter Type B').has_value('High Shelf').and_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Resonance B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Gain A').if_parameter('4 Filter Type A').has_value('Low Shelf').or_parameter('4 Filter Type A').has_value('Bell').or_parameter('4 Filter Type A').has_value('High Shelf').else_use('4 Resonance A')), 
    
    OPTIONS_KEY: (
                  use('Left/Right').if_parameter('Eq Mode').has_value('Left/Right').else_use('Mid/Side').if_parameter('Eq Mode').has_value('Mid/Side').else_use(''),
                  '',
                  '',
                  '',
                  '',
                  '',
                  '')}),
  (
   '8 x Frequency',
   {BANK_PARAMETERS_KEY: (
                          use('1 Frequency B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Frequency A'),
                          use('2 Frequency B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Frequency A'),
                          use('3 Frequency B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Frequency A'),
                          use('4 Frequency B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Frequency A'),
                          use('5 Frequency B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('5 Frequency A'),
                          use('6 Frequency B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('6 Frequency A'),
                          use('7 Frequency B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('7 Frequency A'),
                          use('8 Frequency B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('8 Frequency A')), 
    
    OPTIONS_KEY: (
                  use('Left/Right').if_parameter('Eq Mode').has_value('Left/Right').else_use('Mid/Side').if_parameter('Eq Mode').has_value('Mid/Side').else_use(''),
                  '',
                  '',
                  '',
                  '',
                  '',
                  '')}),
  (
   '8 x Gain',
   {BANK_PARAMETERS_KEY: (
                          use('1 Gain B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Gain A'),
                          use('2 Gain B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Gain A'),
                          use('3 Gain B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Gain A'),
                          use('4 Gain B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Gain A'),
                          use('5 Gain B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('5 Gain A'),
                          use('6 Gain B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('6 Gain A'),
                          use('7 Gain B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('7 Gain A'),
                          use('8 Gain B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('8 Gain A')), 
    
    OPTIONS_KEY: (
                  use('Left/Right').if_parameter('Eq Mode').has_value('Left/Right').else_use('Mid/Side').if_parameter('Eq Mode').has_value('Mid/Side').else_use(''),
                  '',
                  '',
                  '',
                  '',
                  '',
                  '')}),
  (
   '8 x Resonance',
   {BANK_PARAMETERS_KEY: (
                          use('1 Resonance B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('1 Resonance A'),
                          use('2 Resonance B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('2 Resonance A'),
                          use('3 Resonance B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('3 Resonance A'),
                          use('4 Resonance B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('4 Resonance A'),
                          use('5 Resonance B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('5 Resonance A'),
                          use('6 Resonance B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('6 Resonance A'),
                          use('7 Resonance B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('7 Resonance A'),
                          use('8 Resonance B').if_parameter('Edit Mode').has_value('On').and_parameter('Eq Mode').does_not_have_value('Stereo').else_use('8 Resonance A')), 
    
    OPTIONS_KEY: (
                  use('Left/Right').if_parameter('Eq Mode').has_value('Left/Right').else_use('Mid/Side').if_parameter('Eq Mode').has_value('Mid/Side').else_use(''),
                  '',
                  '',
                  '',
                  '',
                  '',
                  '')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Eq Mode', 'Oversampling', 'Adaptive Q', '', '', '', 'Scale', 'Output Gain'), 
    
    OPTIONS_KEY: (
                  use('Left/Right').if_parameter('Eq Mode').has_value('Left/Right').else_use('Mid/Side').if_parameter('Eq Mode').has_value('Mid/Side').else_use(''),
                  '',
                  '',
                  '',
                  '',
                  '',
                  '')}))), 
 'FilterEQ3':IndexedDict((
  (
   'EQ',
   {BANK_PARAMETERS_KEY: ('LowOn', 'MidOn', 'HighOn', 'GainLo', 'GainMid', 'GainHi', 'FreqLo', 'FreqHi')}),
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
                          '2 Filter Freq',
                          '2 Filter Width',
                          '2 Delay Mode',
                          use('2 Time Delay').if_parameter('2 Delay Mode').has_value('Off').else_use('2 Beat Delay'),
                          '2 Feedback',
                          use('1 Volume').if_parameter('1 Input On').has_value('On').else_use('2 Pan'),
                          '2 Volume',
                          use('3 Volume').if_parameter('3 Input On').has_value('On').else_use('Dry'))}),
  (
   'L Filter',
   {BANK_PARAMETERS_KEY: (
                          '1 Input On',
                          '1 Filter Freq',
                          '1 Filter Width',
                          '1 Feedback',
                          '1 Delay Mode',
                          use('1 Time Delay').if_parameter('1 Delay Mode').has_value('Off').else_use('1 Beat Delay'),
                          use('1 Beat Swing').if_parameter('1 Delay Mode').has_value('On').else_use(''),
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
                          use('2 Beat Swing').if_parameter('2 Delay Mode').has_value('On').else_use(''),
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
                          use('3 Beat Swing').if_parameter('3 Delay Mode').has_value('On').else_use(''),
                          '3 Volume')}),
  (
   'Mix',
   {BANK_PARAMETERS_KEY: ('1 Pan', '2 Pan', '3 Pan', '', '1 Volume', '2 Volume', '3 Volume', 'Dry')}))), 
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
                          'S/C Gain',
                          'S/C Mix',
                          'S/C Listen',
                          'S/C EQ On',
                          'S/C EQ Type',
                          'S/C EQ Freq',
                          use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('Low Shelf').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('High Shelf').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('Bell').else_use('S/C EQ Q'))}))), 
 'GlueCompressor':IndexedDict((
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
                          use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('Low Shelf').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('High Shelf').else_use('S/C EQ Gain').if_parameter('S/C EQ Type').has_value('Bell').else_use('S/C EQ Q'))}))), 
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
 'Limiter':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Gain', 'Ceiling', 'Link Channels', 'Lookahead', 'Auto', 'Release time', '', '')}),)), 
 'Looper':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('State', 'Speed', 'Reverse', 'Quantization', 'Monitor', 'Song Control', 'Tempo Control',
 'Feedback')}),)), 
 'MultibandDynamics':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Above Threshold (Low)', 'Above Ratio (Low)', 'Above Threshold (Mid)', 'Above Ratio (Mid)',
 'Above Threshold (High)', 'Above Ratio (High)', 'Master Output', 'Amount')}),
  (
   'Low Band',
   {BANK_PARAMETERS_KEY: ('Band Activator (Low)', 'Input Gain (Low)', 'Below Threshold (Low)', 'Below Ratio (Low)',
 'Above Threshold (Low)', 'Above Ratio (Low)', 'Attack Time (Low)', 'Release Time (Low)')}),
  (
   'Mid Band',
   {BANK_PARAMETERS_KEY: ('Band Activator (Mid)', 'Input Gain (Mid)', 'Below Threshold (Mid)', 'Below Ratio (Mid)',
 'Above Threshold (Mid)', 'Above Ratio (Mid)', 'Attack Time (Mid)', 'Release Time (Mid)')}),
  (
   'High Band',
   {BANK_PARAMETERS_KEY: ('Band Activator (High)', 'Input Gain (High)', 'Below Threshold (High)', 'Below Ratio (High)',
 'Above Threshold (High)', 'Above Ratio (High)', 'Attack Time (High)', 'Release Time (High)')}),
  (
   'Mix & Split',
   {BANK_PARAMETERS_KEY: ('Output Gain (Low)', 'Low-Mid Crossover', 'Output Gain (Mid)', 'Mid-High Crossover',
 'Output Gain (High)', 'Peak/RMS Mode', 'Amount', 'Master Output')}),
  (
   'Sidechain',
   {BANK_PARAMETERS_KEY: ('S/C On', 'S/C Mix', 'S/C Gain', '', 'Time Scaling', 'Soft Knee On/Off', '', '')}))), 
 'Overdrive':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Filter Freq', 'Filter Width', 'Drive', 'Tone', 'Preserve Dynamics', '', '', 'Dry/Wet')}),)), 
 'Pedal':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Type', 'Gain', 'Output', 'Bass', 'Mid', 'Treble', 'Sub', 'Dry/Wet'), 
    
    OPTIONS_KEY: ('', '', '', 'Mid Freq', '', '', '')}),)), 
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
   {BANK_PARAMETERS_KEY: ('Poles', 'Type', 'Color', 'Frequency', 'Feedback', 'Env. Modulation', 'Env. Attack',
 'Env. Release')}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          'LFO Amount',
                          'LFO Waveform',
                          'LFO Sync',
                          use('LFO Frequency').if_parameter('LFO Sync').has_value('Free').else_use('LFO Sync Rate'),
                          use('LFO Width (Random)').if_parameter('LFO Waveform').has_value('S&H Width').else_use('LFO Stereo Mode').if_parameter('LFO Sync').has_value('Free').else_use('LFO Offset'),
                          use('').if_parameter('LFO Waveform').has_value('S&H Width').else_use('LFO Phase').if_parameter('LFO Sync').has_value('Sync').else_use('LFO Phase').if_parameter('LFO Stereo Mode').has_value('Phase').else_use('LFO Spin'),
                          '',
                          '')}))), 
 'PhaserNew':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          'Mode',
                          use('Mod Rate').with_name('Rate').if_parameter('Mod Sync').has_value('On').else_use('Mod Freq').with_name('Freq'),
                          'Amount',
                          'Feedback',
                          use('Notches').if_parameter('Mode').has_value('Phaser').else_use('Flange Time').with_name('Time').if_parameter('Mode').has_value('Flanger').else_use('Doubler Time').with_name('Time').if_parameter('Mode').has_value('Doubler'),
=======
                          'Ph/Fl Mode',
                          use('Mod Rate').with_name('Rate').if_parameter('Mod Sync').has_value('On').else_use('Mod Freq').with_name('Freq'),
                          'Amount',
                          'Feedback',
                          use('Notches').if_parameter('Ph/Fl Mode').has_value('Phaser').else_use('Flange Time').with_name('Time').if_parameter('Ph/Fl Mode').has_value('Flanger').else_use('Doubler Time').with_name('Time').if_parameter('Ph/Fl Mode').has_value('Doubler'),
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          'Warmth',
                          use('Output Gain').with_name('Gain'),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: ('Sync', '', 'FB Inv', '', '', '', '')}),
  (
   'Details',
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          'Mode',
                          use('Mod Rate').with_name('Rate').if_parameter('Mod Sync').has_value('On').else_use('Mod Freq').with_name('Freq'),
                          'Amount',
                          'Feedback',
                          use('Notches').if_parameter('Mode').has_value('Phaser').else_use('Flange Time').with_name('Time').if_parameter('Mode').has_value('Flanger').else_use('Doubler Time').with_name('Time').if_parameter('Mode').has_value('Doubler'),
                          use('Center Freq').with_name('Center').if_parameter('Mode').has_value('Phaser').else_use(''),
                          use('Spread').if_parameter('Mode').has_value('Phaser').else_use('Output Gain').with_name('Gain'),
                          use('Mod Blend').with_name('Blend').if_parameter('Mode').has_value('Phaser').else_use('Dry/Wet')), 
=======
                          'Ph/Fl Mode',
                          use('Mod Rate').with_name('Rate').if_parameter('Mod Sync').has_value('On').else_use('Mod Freq').with_name('Freq'),
                          'Amount',
                          'Feedback',
                          use('Notches').if_parameter('Ph/Fl Mode').has_value('Phaser').else_use('Flange Time').with_name('Time').if_parameter('Ph/Fl Mode').has_value('Flanger').else_use('Doubler Time').with_name('Time').if_parameter('Ph/Fl Mode').has_value('Doubler'),
                          use('Center Freq').with_name('Center').if_parameter('Ph/Fl Mode').has_value('Phaser').else_use(''),
                          use('Spread').if_parameter('Ph/Fl Mode').has_value('Phaser').else_use('Output Gain').with_name('Gain'),
                          use('Mod Blend').with_name('Blend').if_parameter('Ph/Fl Mode').has_value('Phaser').else_use('Dry/Wet')), 
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    
    OPTIONS_KEY: ('Sync', '', 'FB Inv', '', '', '', '')}),
  (
   'LFO 2',
   {BANK_PARAMETERS_KEY: (
                          use('Lfo Blend').with_name('LFO2 Mix'),
                          use('Mod Wave').with_name('Waveform'),
                          use('Duty Cycle').with_name('Duty'),
                          use('Spin').if_parameter('Spin Enabled').has_value('On').else_use('Mod Phase').with_name('Phase'),
                          use('Mod Rate 2').with_name('LFO2 Rate').if_parameter('Mod Sync 2').has_value('On').else_use('Mod Freq 2').with_name('LFO2 Freq'),
                          use('Safe Freq').with_name('Safe Bass'),
                          use('Output Gain').with_name('Gain'),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: ('', '', 'Spin', use('Sync 2'), '', '')}),
  (
   'LFO 2 Env',
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
                          'Bit Depth',
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
<<<<<<< HEAD
                          'Dry/Wet'), 
=======
                          use('Dry Wet').with_name('Dry/Wet')), 
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    
    OPTIONS_KEY: ('', '', '', '', '', 'Post-Filter', '')}),)), 
 'Transmute':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Decay',
                          use('Transpose').if_parameter('Pitch Mode').has_value('MIDI').else_use('Freq. Hz').with_name('Freq').if_parameter('Frequency Dial Mode').has_value('ModulationHertz').else_use('Note').with_name('Freq'),
                          'LF Damp',
                          'HF Damp',
                          'Stretch',
                          'Shift',
                          'Input Send Gain',
                          'Dry Wet'), 
    
    OPTIONS_KEY: ('frequency_dial_mode_opt', '', '', '', '', '')}),
  (
   'Details',
   {BANK_PARAMETERS_KEY: (
                          'Mod Mode',
                          use('').if_parameter('Mod Mode').has_value('None').else_use('Mod Rate'),
                          use('').if_parameter('Mod Mode').has_value('None').else_use('Pitch Mod'),
                          'Harmonics',
                          'Unison',
                          use('Unison Amount').with_name('Unison Amt'),
                          use('Input Send Gain').with_name('Input Send'),
                          'Dry Wet')}),
  (
   'Sidechain',
   {BANK_PARAMETERS_KEY: (
                          use('Pitch Mode').with_name('Mode'),
                          use('Midi Gate').if_parameter('Pitch Mode').has_value('MIDI').and_parameter('Mono Poly').has_value('Mono').else_use(''),
                          use('Mono Poly').with_name('Mono/Poly').if_parameter('Pitch Mode').has_value('MIDI').else_use(''),
                          use('Glide').if_parameter('Pitch Mode').has_value('MIDI').and_parameter('Mono Poly').has_value('Mono').else_use('Polyphony').with_name('Voices').if_parameter('Pitch Mode').has_value('MIDI').and_parameter('Mono Poly').has_value('Poly').else_use(''),
                          use('Pitch Bend Range').with_name('PBend Range').if_parameter('Pitch Mode').has_value('MIDI').else_use(''),
                          '',
                          use('Input Send Gain').with_name('Input Send'),
                          'Dry Wet')}))), 
 'Resonator':IndexedDict((
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
   {BANK_PARAMETERS_KEY: ('I Note', 'II Pitch', 'III Pitch', 'IV Pitch', 'V Pitch', '', '', '')}))), 
 'Reverb':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
<<<<<<< HEAD
                          'Predelay',
                          'In Filter Freq',
                          'In Filter Width',
                          'Stereo Image',
                          'Room Size',
                          use('Decay Time').with_name('Decay'),
                          use('HiFilter Freq').with_name('Hi Filter Freq'),
                          'Dry/Wet')}),
  (
   'Input/Reflect',
   {BANK_PARAMETERS_KEY: (
                          'ER Shape',
                          'In Filter Freq',
                          'In Filter Width',
                          'Size Smoothing',
                          'Room Size',
                          'ER Spin Rate',
                          'ER Spin Amount',
                          use('Reflect Level').with_name('Reflect')), 
    
    OPTIONS_KEY: ('In LoCut', 'In HiCut', '', '', '', 'ER Spin', '')}),
  (
   'Diffuse',
   {BANK_PARAMETERS_KEY: (
                          use('LowShelf Freq').with_name('Lo Shelf Freq'),
                          use('LowShelf Gain').with_name('Lo Shelf Gain'),
                          use('HiFilter Freq').with_name('Hi Filter Freq'),
                          use('HiShelf Gain').with_name('Hi Shelf Gain'),
                          'Diffusion',
                          'Scale',
                          use('Decay Time').with_name('Decay'),
                          use('Diffuse Level').with_name('Diffuse')), 
    
    OPTIONS_KEY: ('Lo Shelf', 'Hi Filter', 'Hi Fil Type', 'Flat', 'Cut', '', 'Freeze')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: (
                          'Density',
                          'Size Smoothing',
                          'Chorus Rate',
                          'Chorus Amount',
                          'Stereo Image',
                          use('Reflect Level').with_name('Reflect'),
                          use('Diffuse Level').with_name('Diffuse'),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: ('', '', 'Chorus', '', '', '', '')}))), 
=======
                          'PreDelay',
                          use('In Filter Freq').if_parameter('In LowCut On').has_value('On').else_use('ER Shape').if_parameter('In HighCut On').has_value('Off').else_use('In Filter Freq'),
                          use('Chorus Amount').if_parameter('Chorus On').has_value('On').else_use('ER Level'),
                          'Stereo Image',
                          'Room Size',
                          'DecayTime',
                          use('HiShelf Gain').if_parameter('HiShelf On').has_value('On').else_use('Diffuse Level'),
                          'Dry/Wet')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Chorus On', 'Chorus Rate', 'Chorus Amount', 'Quality', 'Freeze On', 'Flat On', 'ER Level',
 'Diffuse Level')}),
  (
   'Diffusion Network',
   {BANK_PARAMETERS_KEY: ('HiShelf On', 'HiShelf Freq', 'HiShelf Gain', 'LowShelf On', 'LowShelf Freq', 'LowShelf Gain',
 'Density', 'Scale')}),
  (
   'Input/Reflections',
   {BANK_PARAMETERS_KEY: ('In LowCut On', 'In HighCut On', 'In Filter Freq', 'In Filter Width', 'ER Spin On',
 'ER Spin Rate', 'ER Spin Amount', 'ER Shape')}))), 
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
 'Saturator':IndexedDict((
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
   {BANK_PARAMETERS_KEY: ('', '', '', '', '', 'Soft Clip', 'Output', 'Dry/Wet')}))), 
 'Shifter':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Mode',
                          use('Pitch Coarse').with_name('Coarse').if_parameter('Mode').has_value('Pitch').else_use('FShift Coarse').with_name('Coarse').if_parameter('Mode').has_value('Freq').else_use('RM Coarse').with_name('Coarse'),
                          use('Pitch Fine').with_name('Spread').if_parameter('Mode').has_value('Pitch').and_parameter('Wide').has_value('On').else_use('Pitch Fine').with_name('Fine').if_parameter('Mode').has_value('Pitch').else_use('Mod Fine').with_name('Spread').if_parameter('Wide').has_value('On').else_use('Mod Fine').with_name('Fine'),
                          use('Delay S. Time').if_parameter('Delay Sync').has_value('On').else_use('Delay Time'),
                          use('Delay Feedback').with_name('Dly Feedback'),
                          'Tone',
                          use('RM Drive Gain').with_name('Drive Gain').if_parameter('Mode').has_value('Ring').else_use('Pitch Window').if_parameter('Mode').has_value('Pitch'),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: (
                  '',
                  'Wide',
                  'Delay',
                  'Delay Sync',
                  '',
                  use('RM Drive').if_parameter('Mode').has_value('Ring'),
                  '')}),
  (
   'LFO / S&H',
   {BANK_PARAMETERS_KEY: (
                          use('Lfo Waveform').with_name('Waveform'),
                          use('Lfo Amount St').with_name('Amount').if_parameter('Mode').has_value('Pitch').else_use('Lfo Amount Hz').with_name('Amount'),
                          use('Lfo S. Rate').with_name('S. Rate').if_parameter('Lfo Sync').has_value('On').else_use('Lfo Rate Hz').with_name('Rate'),
                          use('Lfo Width').with_name('S&H Width').if_parameter('Lfo Waveform').has_value('Random S&H').else_use('Lfo Phase').with_name('Phase').if_parameter('Lfo Waveform').has_value('Random').or_parameter('Lfo Spin').has_value('Off').or_parameter('Lfo Sync').has_value('On').else_use('Lfo Spin Amount').with_name('Spin'),
                          use('Lfo Duty Cycle').with_name('Duty Cycle'),
                          use('Lfo Offset').with_name('Offset').if_parameter('Lfo Sync').has_value('On'),
                          '',
                          'Dry/Wet'), 
    
    OPTIONS_KEY: (
                  '',
                  'Lfo Sync',
                  use('').if_parameter('Lfo Waveform').has_value('Random S&H').or_parameter('Lfo Waveform').has_value('Random').or_parameter('Lfo Sync').has_value('On').else_use('Lfo Spin'),
                  '',
                  '',
                  '',
                  '')}),
  (
   'Env Follow',
   {BANK_PARAMETERS_KEY: (
                          use('Env Amount St').with_name('Amount').if_parameter('Mode').has_value('Pitch').else_use('Env Amount Hz').with_name('Amount'),
                          use('Env Attack').with_name('Attack'),
                          use('Env Release').with_name('Release'),
                          '',
                          '',
                          '',
                          use('RM Drive Gain').with_name('Drive Gain').if_parameter('Mode').has_value('Ring'),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: (
                  'Env. Follow',
                  '',
                  '',
                  '',
                  '',
                  use('RM Drive').if_parameter('Mode').has_value('Ring'),
                  '')}),
  (
   'Sidechain',
   {BANK_PARAMETERS_KEY: (
                          'Pitch Mode',
                          use('MidiPitch Glide').with_name('Glide'),
                          use('Pitch Bend Range').with_name('PBend Amount'),
                          '',
                          '',
                          '',
                          use('RM Drive Gain').with_name('Drive Gain').if_parameter('Mode').has_value('Ring'),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: (
                  '',
                  '',
                  '',
                  '',
                  '',
                  use('RM Drive').if_parameter('Mode').has_value('Ring'),
                  '')}))), 
 'Spectral':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          use('Mode').if_parameter('On').has_value('On').else_use(''),
                          use('Retrigger Mode').with_name('Auto Mode').if_parameter('Mode').has_value('Retrigger').and_parameter('On').has_value('On').else_use(''),
                          use('S.Rate ms').with_name('Interval').if_parameter('Unit').has_value('Milliseconds').and_parameter('Retrigger Mode').has_value('Sync').and_parameter('Mode').has_value('Retrigger').and_parameter('On').has_value('On').else_use('Sync Interval').with_name('Interval').if_parameter('Unit').has_value('ModulationBeat').and_parameter('Retrigger Mode').has_value('Sync').and_parameter('Mode').has_value('Retrigger').and_parameter('On').has_value('On').else_use('Sensitivity').if_parameter('Retrigger Mode').has_value('Onsets').and_parameter('Mode').has_value('Retrigger').and_parameter('On').has_value('On').else_use(''),
                          use('Delay Time Seconds').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('Time').and_parameter('Delay On').has_value('On').else_use('Delay Time Divisions').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('Notes').and_parameter('Delay On').has_value('On').else_use('Delay Time Sixteenths').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('16th').and_parameter('Delay On').has_value('On').else_use('Delay Time Sixteenths').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('16th Triplet').and_parameter('Delay On').has_value('On').else_use('Delay Time Sixteenths').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('16th Dotted').and_parameter('Delay On').has_value('On').else_use(''),
                          use('Delay Feedback').with_name('Feedback').if_parameter('Delay On').has_value('On').else_use(''),
                          use('Delay Frequency Shift').with_name('Shift').if_parameter('Delay On').has_value('On').else_use(''),
                          use('Input Send Gain').with_name('Input Send'),
                          use('Dry Wet').with_name('Dry/Wet')), 
    
    OPTIONS_KEY: (
                  use('Frozen').if_parameter('On').has_value('On').else_use(''),
                  use('Unit').if_parameter('Mode').has_value('Retrigger').and_parameter('Retrigger Mode').has_value('Sync').and_parameter('On').has_value('On').else_use(''),
                  use('Delay Dly. Unit').if_parameter('Delay On').has_value('On').else_use(''),
                  '',
                  '',
                  '',
                  '')}),
  (
   'Freezer',
   {BANK_PARAMETERS_KEY: (
                          'On',
                          use('Mode').if_parameter('On').has_value('On').else_use(''),
                          use('Retrigger Mode').if_parameter('Mode').has_value('Retrigger').and_parameter('On').has_value('On').else_use(''),
                          use('').if_parameter('Mode').has_value('Manual').else_use('S.Rate ms').with_name('Interval').if_parameter('Retrigger Mode').has_value('Sync').and_parameter('Unit').has_value('Milliseconds').and_parameter('On').has_value('On').else_use('Sync Interval').with_name('Interval').if_parameter('Retrigger Mode').has_value('Sync').and_parameter('Unit').has_value('ModulationBeat').and_parameter('On').has_value('On').else_use('Sensitivity').if_parameter('On').has_value('On'),
                          use('XFade %').with_name('XFade').if_parameter('Fade Type').has_value('Crossfade').and_parameter('Mode').has_value('Retrigger').and_parameter('Retrigger Mode').has_value('Sync').and_parameter('On').has_value('On').else_use('Fade In').with_name('XFade').if_parameter('Mode').has_value('Retrigger').and_parameter('Retrigger Mode').has_value('Onsets').and_parameter('Fade Type').has_value('Crossfade').and_parameter('On').has_value('On').else_use('Fade In').if_parameter('On').has_value('On').else_use(''),
                          use('Fade Out').if_parameter('Fade Type').has_value('Envelope').and_parameter('On').has_value('On').or_parameter('Mode').has_value('Manual').and_parameter('On').has_value('On').else_use(''),
                          use('Input Send Gain').with_name('Input Send'),
                          use('Dry Wet').with_name('Dry/Wet')), 
    
    OPTIONS_KEY: (
                  '',
                  use('Frozen').if_parameter('On').has_value('On').else_use(''),
                  use('Unit').if_parameter('Retrigger Mode').has_value('Sync').and_parameter('Mode').has_value('Retrigger').and_parameter('On').has_value('On').else_use(''),
                  use('Fade Type').if_parameter('Mode').has_value('Retrigger').and_parameter('On').has_value('On').else_use(''),
                  '',
                  '',
                  '')}),
  (
   'Delay 1',
   {BANK_PARAMETERS_KEY: (
                          'Delay On',
                          use('Delay Time Seconds').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('Time').and_parameter('Delay On').has_value('On').else_use('Delay Time Divisions').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('Notes').and_parameter('Delay On').has_value('On').else_use('Delay Time Sixteenths').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('16th').and_parameter('Delay On').has_value('On').else_use('Delay Time Sixteenths').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('16th Triplet').and_parameter('Delay On').has_value('On').else_use('Delay Time Sixteenths').with_name('Del. Time').if_parameter('Delay Dly. Unit').has_value('16th Dotted').and_parameter('Delay On').has_value('On').else_use(''),
                          use('Delay Feedback').with_name('Feedback').if_parameter('Delay On').has_value('On').else_use(''),
                          use('Delay Frequency Shift').with_name('Shift').if_parameter('Delay On').has_value('On').else_use(''),
                          use('Delay Tilt').with_name('Tilt').if_parameter('Delay On').has_value('On').else_use(''),
                          use('Delay Spray').with_name('Spray').if_parameter('Delay On').has_value('On').else_use(''),
                          use('Delay Mask').with_name('Mask').if_parameter('Delay On').has_value('On').else_use(''),
                          use('Dry Wet').with_name('Dry/Wet')), 
    
    OPTIONS_KEY: (
                  use('Delay Dly. Unit').if_parameter('Delay On').has_value('On').else_use(''),
                  '',
                  '',
                  '',
                  '',
                  '',
                  '')}),
  (
   'Delay 2',
   {BANK_PARAMETERS_KEY: (
                          'Delay On',
                          use('Delay Stereo Spread').with_name('Stereo').if_parameter('Delay On').has_value('On').else_use(''),
                          use('Delay Mix').with_name('Mix').if_parameter('Delay On').has_value('On').else_use(''),
                          '',
                          '',
                          '',
                          use('Input Send Gain').with_name('Input Send'),
                          use('Dry Wet').with_name('Dry/Wet'))}))), 
 'StereoGain':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Left Inv',
                          'Right Inv',
                          'Channel Mode',
                          use('Stereo Width').if_parameter('Stereo Width').is_available(True).else_use('Mid/Side Balance'),
                          use('Bass Freq').if_parameter('Bass Freq').is_available(True),
                          'Balance',
                          use('Gain').if_parameter('Gain').is_available(True).else_use('Gain (Legacy)'),
                          'Mute'), 
    
    OPTIONS_KEY: (
                  '',
                  '',
                  use('Mono').if_parameter('Mono').is_available(True),
                  use('Bass Mono').if_parameter('Bass Mono').is_available(True),
                  '',
                  '',
                  'DC Filter')}),)), 
 'Vinyl':IndexedDict((
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Tracing On', 'Tracing Drive', 'Tracing Freq.', 'Tracing Width', 'Pinch On', 'Global Drive',
 'Crackle Density', 'Crackle Volume')}),
  (
   'Pinch',
   {BANK_PARAMETERS_KEY: ('Pinch On', 'Pinch Soft On', 'Pinch Mono On', 'Pinch Width', 'Pinch Drive', 'Pinch Freq.',
 'Crackle Density', 'Crackle Volume')}))), 
 'Vocoder':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Formant Shift', 'Attack Time', 'Release Time', 'Unvoiced Level', 'Gate Threshold',
 'Filter Bandwidth', 'Envelope Depth', 'Dry/Wet')}),
  (
   'Carrier',
   {BANK_PARAMETERS_KEY: ('Noise Rate', 'Noise Crackle', 'Lower Pitch Detection', 'Upper Pitch Detection', 'Oscillator Pitch',
 'Oscillator Waveform', 'Enhance', '')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Formant Shift', 'Attack Time', 'Release Time', 'Mono/Stereo', 'Output Level', 'Gate Threshold',
 'Envelope Depth', 'Dry/Wet')}),
  (
   'Filters/Voicing',
   {BANK_PARAMETERS_KEY: ('Filter Bandwidth', 'Upper Filter Band', 'Lower Filter Band', 'Precise/Retro', 'Unvoiced Level',
 'Unvoiced Sensitivity', 'Unvoiced Speed', 'Enhance')})))}
<<<<<<< HEAD
PARAMETERS_BLACKLIST_FOR_CPP_SANITY_CHECK = {
  'OriginalSimpler': ('Start', 'End', 'Sensitivity', 'Mode', 'Playback', 'Pad Slicing', 'Multi Sample', 'Zoom', 'Env. Type', 'Warp', 'Warp Mode', 'Voices', 'Preserve', 'Loop Mode', 'Envelope', 'Grain Size Tones', 'Grain Size Texture', 'Flux', 'Formants', 'Envelope Complex Pro', 'Gain'),
  'Operator': ('Oscillator', 'Envelope Feature Time/Level', 'Envelope Feature Time/Slope/Level'),
  'Eq8': ('Band', 'Eq Mode', 'Edit Mode', 'Oversampling'),
  'Compressor2': ('Input Type', 'Input Channel', 'Position'),
  'InstrumentVector': ('Oscillator', 'Osc 1 Effect Type', 'Osc 2 Effect Type', 'Osc 1 Table', 'Osc 2 Table', 'Osc 1 Pitch', 'Osc 2 Pitch', 'Filter', 'Envelopes', 'LFO', 'Amp Env View', 'Mod Env View', 'Modulation Target Names', 'Amp Env Mod Amount', 'Env 2 Mod Amount', 'Env 3 Mod Amount', 'Lfo 1 Mod Amount', 'Lfo 2 Mod Amount', 'MIDI Velocity Mod Amount', 'MIDI Note Mod Amount', 'MIDI Pitch Bend Mod Amount', 'MIDI Aftertouch Mod Amount', 'MIDI Mod Wheel Mod Amount', 'MIDI Random On Note On', 'Current Mod Target', 'Unison Mode', 'Unison Voices', 'Mono On', 'Poly Voices', 'Filter Routing'),
  'Hybrid': ('Band', 'Section', 'Shape', 'IR', 'IR Category', 'Ir Attack Time', 'Ir Decay Time', 'Ir Size Factor', 'Vintage Copy', 'Routing Eq Off', 'Routing Eq On PreAlgo Off', 'Routing Eq On PreAlgo On'),
  'Shifter': ('Pitch Bend Range', 'Pitch Mode'),
  'Transmute': ('Frequency Dial Mode', 'Midi Gate', 'Mod Mode', 'Mono Poly', 'Pitch Mode', 'Pitch Bend Range', 'Polyphony'),
  'Echo': ('Channel Toggle',),
  'Delay': ('Channel', 'L Sync Enum', 'R Sync Enum', 'Link Switch')}
=======
PARAMETERS_BLACKLIST_FOR_CPP_SANITY_CHECK = {'OriginalSimpler':('Start', 'End', 'Sensitivity', 'Mode', 'Playback', 'Pad Slicing', 'Multi Sample',
 'Zoom', 'Env. Type', 'Warp', 'Warp Mode', 'Voices', 'Preserve', 'Loop Mode', 'Envelope',
 'Grain Size Tones', 'Grain Size Texture', 'Flux', 'Formants', 'Envelope Complex Pro',
 'Gain'), 
 'Operator':('Oscillator', 'Envelope Feature Time/Level', 'Envelope Feature Time/Slope/Level'), 
 'Eq8':('Band', 'Eq Mode', 'Edit Mode', 'Oversampling'), 
 'Compressor2':('Input Type', 'Input Channel', 'Position'), 
 'InstrumentVector':('Oscillator', 'Osc 1 Effect Type', 'Osc 2 Effect Type', 'Osc 1 Table', 'Osc 2 Table',
 'Osc 1 Pitch', 'Osc 2 Pitch', 'Filter', 'Envelopes', 'LFO', 'Amp Env View', 'Mod Env View',
 'Modulation Target Names', 'Amp Env Mod Amount', 'Env 2 Mod Amount', 'Env 3 Mod Amount',
 'Lfo 1 Mod Amount', 'Lfo 2 Mod Amount', 'MIDI Velocity Mod Amount', 'MIDI Note Mod Amount',
 'MIDI Pitch Bend Mod Amount', 'MIDI Aftertouch Mod Amount', 'MIDI Mod Wheel Mod Amount',
 'MIDI Random On Note On', 'Current Mod Target', 'Unison Mode', 'Unison Voices',
 'Mono On', 'Poly Voices', 'Filter Routing'), 
 'Hybrid':('Band', 'Section', 'Shape', 'IR', 'IR Category', 'Ir Attack Time', 'Ir Decay Time',
 'Ir Size Factor', 'Vintage Copy', 'Routing Eq Off', 'Routing Eq On PreAlgo Off',
 'Routing Eq On PreAlgo On'), 
 'Shifter':('Pitch Bend Range', 'Pitch Mode'), 
 'Transmute':('Frequency Dial Mode', 'Midi Gate', 'Mod Mode', 'Mono Poly', 'Pitch Mode', 'Pitch Bend Range',
 'Polyphony'), 
 'Echo':('Channel Toggle', ), 
 'Delay':('Channel', 'L Sync Enum', 'R Sync Enum', 'Link Switch')}
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
