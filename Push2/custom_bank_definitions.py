# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\custom_bank_definitions.py
# Compiled at: 2023-10-06 16:19:02
# Size of source mod 2**32: 390578 bytes
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
   {BANK_PARAMETERS_KEY: ('OSC1 Shape', 'OSC1 Octave', 'OSC2 Shape', 'OSC2 Octave', 'F1 Type', 'F1 Freq', 'F1 Resonance',
 'Volume')}),
  (
   'Oscillators',
   {BANK_PARAMETERS_KEY: (
                          'Osc Select',
                          use('OSC1 Shape').if_parameter('Osc Select').has_value('Osc 1').else_use('OSC2 Shape').if_parameter('Osc Select').has_value('Osc 2'),
                          use('OSC1 PW').if_parameter('Osc Select').has_value('Osc 1').else_use('OSC2 PW'),
                          use('O1 PW < LFO').if_parameter('Osc Select').has_value('Osc 1').else_use('O2 PW < LFO'),
                          use('O1 Sub/Sync').if_parameter('Osc Select').has_value('Osc 1').and_parameter('OSC1 Shape').has_value('Rect').else_use('O2 Sub/Sync'),
                          use('OSC1 Octave').if_parameter('Osc Select').has_value('Osc 1').else_use('OSC2 Octave'),
                          use('OSC1 Semi').if_parameter('Osc Select').has_value('Osc 1').else_use('OSC2 Semi'),
                          use('OSC1 Detune').if_parameter('Osc Select').has_value('Osc 1').else_use('OSC2 Detune')), 
    
    OPTIONS_KEY: (
                  use('Osc 1').if_parameter('Osc Select').has_value('Osc 1').else_use('Osc 2'),
                  '',
                  '',
                  use('OSC1 Mode').if_parameter('Osc Select').has_value('Osc 1').else_use('OSC2 Mode'),
                  '',
                  '',
                  '')}),
  (
   'Mix',
   {BANK_PARAMETERS_KEY: (
                          'Osc / Amp',
                          use('OSC1 Level').if_parameter('Osc / Amp').has_value('Osc').else_use('AMP1 Level'),
                          use('OSC1 Balance').if_parameter('Osc / Amp').has_value('Osc').else_use('AMP1 Pan'),
                          use('OSC2 Level').if_parameter('Osc / Amp').has_value('Osc').else_use('AMP2 Level'),
                          use('OSC2 Balance').if_parameter('Osc / Amp').has_value('Osc').else_use('AMP2 Pan'),
                          use('Noise Level').if_parameter('Osc / Amp').has_value('Osc').else_use(''),
                          use('Noise Balance').if_parameter('Osc / Amp').has_value('Osc').else_use(''),
                          use('Noise Color').if_parameter('Osc / Amp').has_value('Osc').else_use('')), 
    
    OPTIONS_KEY: (
                  use('Osc 1').if_parameter('Osc / Amp').has_value('Osc').else_use('Amp 1'),
                  '',
                  use('Osc 2').if_parameter('Osc / Amp').has_value('Osc').else_use('Amp 2'),
                  '',
                  use('Noise').if_parameter('Osc / Amp').has_value('Osc').else_use(''),
                  '',
                  '')}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: ('F1 Type', 'F1 Freq', 'F1 Resonance', 'F1 Drive', 'F2 Type', 'F2 Freq', 'F2 Resonance',
 'F2 Drive'), 
    
    OPTIONS_KEY: ('Filter 1', '', '', '', 'Filter 2', '', 'Flt 2 Follow')}),
  (
   'Envelopes',
   {BANK_PARAMETERS_KEY: (
                          'Env Select',
                          use('AEG1 Attack').if_parameter('Env Select').has_value('Amp 1').else_use('AEG2 Attack').if_parameter('Env Select').has_value('Amp 2').else_use('FEG1 Attack').if_parameter('Env Select').has_value('Flt 1').else_use('FEG2 Attack').if_parameter('Env Select').has_value('Flt 2'),
                          use('AEG1 Decay').if_parameter('Env Select').has_value('Amp 1').else_use('AEG2 Decay').if_parameter('Env Select').has_value('Amp 2').else_use('FEG1 Decay').if_parameter('Env Select').has_value('Flt 1').else_use('FEG2 Decay').if_parameter('Env Select').has_value('Flt 2'),
                          use('AEG1 Sustain').if_parameter('Env Select').has_value('Amp 1').else_use('AEG2 Sustain').if_parameter('Env Select').has_value('Amp 2').else_use('FEG1 Sustain').if_parameter('Env Select').has_value('Flt 1').else_use('FEG2 Sustain').if_parameter('Env Select').has_value('Flt 2'),
                          use('AEG1 S Time').if_parameter('Env Select').has_value('Amp 1').else_use('AEG2 S Time').if_parameter('Env Select').has_value('Amp 2').else_use('FEG1 S Time').if_parameter('Env Select').has_value('Flt 1').else_use('FEG2 S Time').if_parameter('Env Select').has_value('Flt 2'),
                          use('AEG1 Rel').if_parameter('Env Select').has_value('Amp 1').else_use('AEG2 Rel').if_parameter('Env Select').has_value('Amp 2').else_use('FEG1 Rel').if_parameter('Env Select').has_value('Flt 1').else_use('FEG2 Rel').if_parameter('Env Select').has_value('Flt 2'),
                          use('AEG1 Loop').if_parameter('Env Select').has_value('Amp 1').else_use('AEG2 Loop').if_parameter('Env Select').has_value('Amp 2').else_use('FEG1 Loop').if_parameter('Env Select').has_value('Flt 1').else_use('FEG2 Loop').if_parameter('Env Select').has_value('Flt 2'),
                          use('AEG1 A < Vel').if_parameter('Env Select').has_value('Amp 1').else_use('AEG2 A < Vel').if_parameter('Env Select').has_value('Amp 2').else_use('FEG1 A < Vel').if_parameter('Env Select').has_value('Flt 1').else_use('FEG2 A < Vel').if_parameter('Env Select').has_value('Flt 2')), 
    
    OPTIONS_KEY: (
                  use('Osc 1').if_parameter('Env Select').has_value('Amp 1').else_use('Osc 2').if_parameter('Env Select').has_value('Amp 2').else_use('Filter 1').if_parameter('Env Select').has_value('Flt 1').else_use('Filter 2').if_parameter('Env Select').has_value('Flt 2'),
                  use('AEG1 Exp').if_parameter('Env Select').has_value('Amp 1').else_use('AEG2 Exp').if_parameter('Env Select').has_value('Amp 2').else_use('FEG1 Exp').if_parameter('Env Select').has_value('Flt 1').else_use('FEG2 Exp').if_parameter('Env Select').has_value('Flt 2'),
                  use('Amp 1 Legato').if_parameter('Env Select').has_value('Amp 1').else_use('Amp 2 Legato').if_parameter('Env Select').has_value('Amp 2').else_use('Flt 1 Legato').if_parameter('Env Select').has_value('Flt 1').else_use('Flt 2 Legato').if_parameter('Env Select').has_value('Flt 2'),
                  use('Amp 1 Free').if_parameter('Env Select').has_value('Amp 1').else_use('Amp 2 Free').if_parameter('Env Select').has_value('Amp 2').else_use('Flt 1 Free').if_parameter('Env Select').has_value('Flt 1').else_use('Flt 2 Free').if_parameter('Env Select').has_value('Flt 2'),
                  '',
                  '',
                  '')}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          'LFO Select',
                          use('LFO1 Shape').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO2 Shape'),
                          use('LFO1 PW').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO2 PW'),
                          use('LFO1 Speed').if_parameter('LFO Select').has_value('LFO 1').and_parameter('LFO1 Sync').has_value('Hertz').else_use('LFO1 SncRate').if_parameter('LFO Select').has_value('LFO 1').and_parameter('LFO1 Sync').has_value('Beat').else_use('LFO2 Speed').if_parameter('LFO Select').has_value('LFO 2').and_parameter('LFO2 Sync').has_value('Hertz').else_use('LFO2 SncRate').if_parameter('LFO Select').has_value('LFO 2').and_parameter('LFO2 Sync').has_value('Beat'),
                          use('LFO1 Phase').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO2 Phase'),
                          use('LFO1 Delay').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO2 Delay'),
                          use('LFO1 Fade In').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO2 Fade In'),
                          ''), 
    
    OPTIONS_KEY: (
                  use('LFO 1').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO 2'),
                  '',
                  use('LFO1 Sync').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO2 Sync'),
                  use('LFO 1 Retrig').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO 2 Retrig'),
                  '',
                  '',
                  '')}),
  (
   'Modulation',
   {BANK_PARAMETERS_KEY: (
                          'Mod Source',
                          use('PB Range').if_parameter('Mod Source').has_value('PB').else_use('Press Dest A').if_parameter('Mod Source').has_value('Press').else_use('Slide Dest A').if_parameter('Mod Source').has_value('Slide').else_use('Mod Dest'),
                          use('AMP1 < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Amp').else_use('F1 Freq < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Filter').else_use('O1 Keytrack').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Osc').else_use('F1 Freq < Env').if_parameter('Mod Source').has_value('Env').and_parameter('Mod Dest').has_value('Filter').else_use('PEG1 Amount').if_parameter('Mod Source').has_value('Env').and_parameter('Mod Dest').has_value('Osc').else_use('AMP1 < LFO').if_parameter('Mod Source').has_value('LFO').and_parameter('Mod Dest').has_value('Amp').else_use('F1 Freq < LFO').if_parameter('Mod Source').has_value('LFO').and_parameter('Mod Dest').has_value('Filter').else_use('OSC1 < LFO').if_parameter('Mod Source').has_value('LFO').and_parameter('Mod Dest').has_value('Osc').else_use('Note PB Range').if_parameter('Mod Source').has_value('PB').else_use('Press Amt A').if_parameter('Mod Source').has_value('Press').else_use('Slide Amt A').if_parameter('Mod Source').has_value('Slide').else_use(''),
                          use('AMP2 < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Amp').else_use('F2 Freq < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Filter').else_use('O2 Keytrack').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Osc').else_use('F2 Freq < Env').if_parameter('Mod Source').has_value('Env').and_parameter('Mod Dest').has_value('Filter').else_use('PEG1 Time').if_parameter('Mod Source').has_value('Env').and_parameter('Mod Dest').has_value('Osc').else_use('AMP2 < LFO').if_parameter('Mod Source').has_value('LFO').and_parameter('Mod Dest').has_value('Amp').else_use('F2 Freq < LFO').if_parameter('Mod Source').has_value('LFO').and_parameter('Mod Dest').has_value('Filter').else_use('OSC2 < LFO').if_parameter('Mod Source').has_value('LFO').and_parameter('Mod Dest').has_value('Osc').else_use('Press Dest B').if_parameter('Mod Source').has_value('Press').else_use('Slide Dest B').if_parameter('Mod Source').has_value('Slide').else_use(''),
                          use('A1 Pan < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Amp').else_use('F1 Reso < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Filter').else_use('A1 Pan < Env').if_parameter('Mod Source').has_value('Env').and_parameter('Mod Dest').has_value('Amp').else_use('F1 Res < Env').if_parameter('Mod Source').has_value('Env').and_parameter('Mod Dest').has_value('Filter').else_use('PEG2 Amount').if_parameter('Mod Source').has_value('Env').and_parameter('Mod Dest').has_value('Osc').else_use('A1 Pan < LFO').if_parameter('Mod Source').has_value('LFO').and_parameter('Mod Dest').has_value('Amp').else_use('F1 Res < LFO').if_parameter('Mod Source').has_value('LFO').and_parameter('Mod Dest').has_value('Filter').else_use('O1 PW < LFO').if_parameter('Mod Source').has_value('LFO').and_parameter('Mod Dest').has_value('Osc').else_use('Press Amt B').if_parameter('Mod Source').has_value('Press').else_use('Slide Amt B').if_parameter('Mod Source').has_value('Slide').else_use(''),
                          use('A2 Pan < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Amp').else_use('F2 Reso < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Filter').else_use('A2 Pan < Env').if_parameter('Mod Source').has_value('Env').and_parameter('Mod Dest').has_value('Amp').else_use('F2 Res < Env').if_parameter('Mod Source').has_value('Env').and_parameter('Mod Dest').has_value('Filter').else_use('PEG2 Time').if_parameter('Mod Source').has_value('Env').and_parameter('Mod Dest').has_value('Osc').else_use('A2 Pan < LFO').if_parameter('Mod Source').has_value('LFO').and_parameter('Mod Dest').has_value('Amp').else_use('F2 Res < LFO').if_parameter('Mod Source').has_value('LFO').and_parameter('Mod Dest').has_value('Filter').else_use('O2 PW < LFO').if_parameter('Mod Source').has_value('LFO').and_parameter('Mod Dest').has_value('Osc').else_use(''),
                          '',
                          '')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: (
                          'Select',
                          use('Voices').if_parameter('Select').has_value('Voice').else_use('Octave').if_parameter('Select').has_value('Pitch').else_use('Unison Detune').if_parameter('Select').has_value('Unison').else_use('Vib Amount').if_parameter('Select').has_value('Vibrato'),
                          use('Key Stretch').if_parameter('Select').has_value('Voice').else_use('Semitone').if_parameter('Select').has_value('Pitch').else_use('Unison Voices').if_parameter('Select').has_value('Unison').else_use('Vib Speed').if_parameter('Select').has_value('Vibrato'),
                          use('Key Error').if_parameter('Select').has_value('Voice').else_use('Detune').if_parameter('Select').has_value('Pitch').else_use('Unison Delay').if_parameter('Select').has_value('Unison').else_use('Vib Delay').if_parameter('Select').has_value('Vibrato'),
                          use('Key Priority').if_parameter('Select').has_value('Voice').else_use('Vib Fade-In').if_parameter('Select').has_value('Vibrato').else_use(''),
                          use('Glide Time').if_parameter('Select').has_value('Voice').else_use('Vib Error').if_parameter('Select').has_value('Vibrato').else_use(''),
                          use('Glide Mode').if_parameter('Select').has_value('Voice').else_use('Vib < ModWh').if_parameter('Select').has_value('Vibrato').else_use(''),
                          ''), 
    
    OPTIONS_KEY: (
                  use('Vibrato').if_parameter('Select').has_value('Vibrato').else_use('Unison').if_parameter('Select').has_value('Unison'),
                  '',
                  '',
                  '',
                  use('Glide').if_parameter('Select').has_value('Voice'),
                  use('Legato').if_parameter('Select').has_value('Voice'),
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
                          '',
                          '',
                          use('Gain').with_name('Output'))}),)), 
 'Collision':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Res 1 Type',
                          'Res 1 Brightness',
                          use('Res 1 Opening').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Opening').if_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Inharmonics'),
                          'Res 1 Decay',
                          use('Res 1 Radius').if_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Radius').if_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Material'),
                          'Mallet Stiffness',
                          'Mallet Noise Amount',
                          'Volume')}),
  (
   'Mallet',
   {BANK_PARAMETERS_KEY: ('Mallet Noise Amount', 'Mallet Noise Color', 'Mallet Stiffness', '', '', '', '', 'Mallet Volume'), 
    
    OPTIONS_KEY: ('Mallet', '', '', '', '', '', '')}),
  (
   'Noise',
   {BANK_PARAMETERS_KEY: ('Noise Filter Type', 'Noise Filter Freq', 'Noise Filter Q', 'Noise Attack', 'Noise Decay',
 'Noise Sustain', 'Noise Release', 'Noise Volume'), 
    
    OPTIONS_KEY: ('Noise', '', '', '', '', '', '')}),
  (
   'Res Body',
   {BANK_PARAMETERS_KEY: (
                          'Resonator',
                          use('Res 1 Type').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Type'),
                          use('Res 1 Quality').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Quality'),
                          use('Res 1 Decay').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Decay'),
                          use('Res 1 Radius').if_parameter('Res 1 Type').has_value('Pipe').and_parameter('Resonator').has_value('Res 1').else_use('Res 1 Radius').if_parameter('Res 1 Type').has_value('Tube').and_parameter('Resonator').has_value('Res 1').else_use('Res 1 Material').if_parameter('Res 1 Type').has_value('Beam').and_parameter('Resonator').has_value('Res 1').else_use('Res 1 Material').if_parameter('Res 1 Type').has_value('Marimba').and_parameter('Resonator').has_value('Res 1').else_use('Res 1 Material').if_parameter('Res 1 Type').has_value('String').and_parameter('Resonator').has_value('Res 1').else_use('Res 1 Material').if_parameter('Res 1 Type').has_value('Membrane').and_parameter('Resonator').has_value('Res 1').else_use('Res 1 Material').if_parameter('Res 1 Type').has_value('Plate').and_parameter('Resonator').has_value('Res 1').else_use('Res 2 Radius').if_parameter('Res 2 Type').has_value('Pipe').and_parameter('Resonator').has_value('Res 2').else_use('Res 2 Radius').if_parameter('Res 2 Type').has_value('Tube').and_parameter('Resonator').has_value('Res 2').else_use('Res 2 Material').if_parameter('Res 2 Type').has_value('Beam').and_parameter('Resonator').has_value('Res 2').else_use('Res 2 Material').if_parameter('Res 2 Type').has_value('Marimba').and_parameter('Resonator').has_value('Res 2').else_use('Res 2 Material').if_parameter('Res 2 Type').has_value('String').and_parameter('Resonator').has_value('Res 2').else_use('Res 2 Material').if_parameter('Res 2 Type').has_value('Membrane').and_parameter('Resonator').has_value('Res 2').else_use('Res 2 Material').if_parameter('Res 2 Type').has_value('Plate').and_parameter('Resonator').has_value('Res 2'),
                          use('Res 1 Listening L').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Listening L'),
                          use('Res 1 Listening R').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Listening R'),
                          use('Res 1 Volume').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Volume')), 
    
    OPTIONS_KEY: (
                  use('Res 1').if_parameter('Resonator').has_value('Res 1').else_use('Res 2'),
                  '',
                  '',
                  '',
                  '',
                  '',
                  'Structure')}),
  (
   'Res Tone',
   {BANK_PARAMETERS_KEY: (
                          'Resonator',
                          use('Res 1 Brightness').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Brightness'),
                          use('Res 1 Opening').if_parameter('Resonator').has_value('Res 1').and_parameter('Res 1 Type').has_value('Pipe').else_use('Res 1 Opening').if_parameter('Resonator').has_value('Res 1').and_parameter('Res 1 Type').has_value('Tube').else_use('Res 1 Inharmonics').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Opening').if_parameter('Resonator').has_value('Res 2').and_parameter('Res 1 Type').has_value('Pipe').else_use('Res 2 Opening').if_parameter('Resonator').has_value('Res 2').and_parameter('Res 1 Type').has_value('Tube').else_use('Res 2 Inharmonics').if_parameter('Resonator').has_value('Res 2'),
                          use('Res 1 Ratio').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Ratio'),
                          use('Res 1 Hit').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Hit'),
                          use('Res 1 Hit < Random').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Hit < Random'),
                          use('Res 1 Tune').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Tune'),
                          use('Res 1 Fine Tune').if_parameter('Resonator').has_value('Res 1').else_use('Res 2 Fine Tune')), 
    
    OPTIONS_KEY: (
                  use('Res 1').if_parameter('Resonator').has_value('Res 1').else_use('Res 2'),
                  '',
                  '',
                  '',
                  '',
                  '',
                  'Structure')}),
  (
   'Mix',
   {BANK_PARAMETERS_KEY: ('Volume', 'Res 1 Volume', 'Res 1 Pan', 'Res 1 Bleed', 'Res 2 Volume', 'Res 2 Pan',
 'Res 2 Bleed', ''), 
    
    OPTIONS_KEY: ('Res 1', '', '', 'Res 2', '', '', '')}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          'LFO Select',
                          use('LFO 1 Shape').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO 2 Shape'),
                          use('LFO 1 Sync').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO 2 Sync'),
                          use('LFO 1 Rate').if_parameter('LFO Select').has_value('LFO 1').and_parameter('LFO 1 Sync').has_value('Free').else_use('LFO 1 Sync Rate').if_parameter('LFO Select').has_value('LFO 1').and_parameter('LFO 1 Sync').has_value('Sync').else_use('LFO 2 Rate').if_parameter('LFO Select').has_value('LFO 2').and_parameter('LFO 2 Sync').has_value('Free').else_use('LFO 2 Sync Rate').if_parameter('LFO Select').has_value('LFO 2').and_parameter('LFO 2 Sync').has_value('Sync'),
                          use('LFO 1 Depth').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO 2 Depth'),
                          use('LFO 1 Offset').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO 2 Offset'),
                          use('LFO 1 Dest A').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO 2 Dest A'),
                          use('LFO 1 Amt A').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO 2 Amt A')), 
    
    OPTIONS_KEY: (
                  use('LFO 1').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO 2'),
                  '',
                  use('LFO 1 Retrig').if_parameter('LFO Select').has_value('LFO 1').else_use('LFO 2 Retrig'),
                  '',
                  '',
                  '')}),
  (
   'Modulation',
   {BANK_PARAMETERS_KEY: (
                          'Mod Source',
                          use('Res 1 Pitch Env.').if_parameter('Mod Source').has_value('Env').else_use('LFO 1 Dest A').if_parameter('Mod Source').has_value('LFO 1').else_use('LFO 2 Dest A').if_parameter('Mod Source').has_value('LFO 2').else_use('PB Dest A').if_parameter('Mod Source').has_value('PB').else_use('MW Dest A').if_parameter('Mod Source').has_value('Modwheel').else_use('Press Dest A').if_parameter('Mod Source').has_value('Press').else_use('Slide Dest A').if_parameter('Mod Source').has_value('Slide').else_use('Mod Dest'),
                          use('Mallet Volume < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Mallet').else_use('Noise Volume < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Noise').else_use('Res 1 Decay < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Res 1').else_use('Res 2 Decay < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Res 2').else_use('LFO 1 Rate < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('LFO').else_use('Mallet Volume < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Mallet').else_use('Noise Volume < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Noise').else_use('Res 1 Decay < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Res 1').else_use('Res 2 Decay < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Res 2').else_use('LFO 1 Depth < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('LFO').else_use('Res 1 Pitch Env. Time').if_parameter('Mod Source').has_value('Env').else_use('LFO 1 Amt A').if_parameter('Mod Source').has_value('LFO 1').else_use('LFO 2 Amt A').if_parameter('Mod Source').has_value('LFO 2').else_use('PB Amt A').if_parameter('Mod Source').has_value('PB').else_use('MW Amt A').if_parameter('Mod Source').has_value('Modwheel').else_use('Press Amt A').if_parameter('Mod Source').has_value('Press').else_use('Slide Amt A').if_parameter('Mod Source').has_value('Slide'),
                          use('Mallet Stiffness < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Mallet').else_use('Noise Freq < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Noise').else_use('Res 1 Material < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Res 1').else_use('Res 2 Material < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Res 2').else_use('LFO 2 Rate < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('LFO').else_use('Mallet Stiffness < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Mallet').else_use('Noise Freq < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Noise').else_use('Res 1 Material < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Res 1').else_use('Res 2 Material < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Res 2').else_use('LFO 2 Depth < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('LFO').else_use('Res 2 Pitch Env.').if_parameter('Mod Source').has_value('Env').else_use('LFO 1 Dest B').if_parameter('Mod Source').has_value('LFO 1').else_use('LFO 2 Dest B').if_parameter('Mod Source').has_value('LFO 2').else_use('PB Range').if_parameter('Mod Source').has_value('PB').else_use('MW Dest B').if_parameter('Mod Source').has_value('Modwheel').else_use('Press Dest B').if_parameter('Mod Source').has_value('Press').else_use('Slide Dest B').if_parameter('Mod Source').has_value('Slide'),
                          use('Mallet Noise Amount < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Mallet').else_use('Res 1 Tune < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Res 1').else_use('Res 2 Tune < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Res 2').else_use('Mallet Noise Amount < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Mallet').else_use('Res 1 Pitch Env. < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Res 1').else_use('Res 2 Pitch Env. < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Res 2').else_use('Res 2 Pitch Env. Time').if_parameter('Mod Source').has_value('Env').else_use('LFO 1 Amt B').if_parameter('Mod Source').has_value('LFO 1').else_use('LFO 2 Amt B').if_parameter('Mod Source').has_value('LFO 2').else_use('Note PB Range').if_parameter('Mod Source').has_value('PB').else_use('MW Amt B').if_parameter('Mod Source').has_value('Modwheel').else_use('Press Amt B').if_parameter('Mod Source').has_value('Press').else_use('Slide Amt B').if_parameter('Mod Source').has_value('Slide').else_use(''),
                          use('Res 1 Pan < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Res 1').else_use('Res 2 Pan < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Mod Dest').has_value('Res 2').else_use('Res 1 Inharmonics < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Res 1').else_use('Res 2 Inharmonics < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Mod Dest').has_value('Res 2').else_use(''),
                          '',
                          ''), 
    
    OPTIONS_KEY: ('', '', '', '', '', '', '')}))), 
 'DrumBuss':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Drive', 'Drive Type', 'Transients', 'Crunch', 'Boom Freq', 'Boom Amt', 'Boom Decay',
 'Boom Audition'), 
    
    OPTIONS_KEY: ('Compressor', '', '', '', '', '', '')}),
  (
   'Gains',
   {BANK_PARAMETERS_KEY: ('Trim', '', '', '', '', 'Damping Freq', 'Output Gain', 'Dry/Wet')}))), 
 'DrumCell':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Select',
                          use('Attack').if_parameter('Select').has_value('Env').else_use('Flt Type').if_parameter('Select').has_value('Filter').else_use('').if_parameter('Select').has_value('Mod').else_use('Start').if_parameter('Select').has_value('Sample'),
                          use('Hold').if_parameter('Select').has_value('Env').else_use('Flt Freq').if_parameter('Select').has_value('Filter').else_use('').if_parameter('Select').has_value('Mod').else_use('Transpose').if_parameter('Select').has_value('Sample'),
                          use('Decay').if_parameter('Select').has_value('Env').else_use('Flt Reso').if_parameter('Select').has_value('Filter').else_use('Vel > Vol').if_parameter('Select').has_value('Mod').else_use('Detune').if_parameter('Select').has_value('Sample'),
                          'Volume',
                          '',
                          '',
                          ''), 
    
    OPTIONS_KEY: (
                  use('Filter').if_parameter('Select').has_value('Filter').else_use('Env Mode').if_parameter('Select').has_value('Env').else_use(''),
                  '',
                  '',
                  '',
                  '',
                  '',
                  '')}),)), 
 'LoungeLizard':IndexedDict((
  (
   BANK_MAIN_KEY,
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
                          'Section',
                          use('Exciter Type').if_parameter('Section').has_value('Exciter').else_use('String Decay').if_parameter('Section').has_value('String').else_use('Damper Mass').if_parameter('Section').has_value('Damper').else_use('Term Mass').if_parameter('Section').has_value('Termination').else_use('Body Type').if_parameter('Section').has_value('Body'),
                          use('Exc ForceMassProt').with_name('Force').if_parameter('Exciter Type').has_value('Bow').and_parameter('Section').has_value('Exciter').else_use('Exc ForceMassProt').with_name('Mass').if_parameter('Exciter Type').has_value('Hammer').and_parameter('Section').has_value('Exciter').else_use('Exc ForceMassProt').with_name('Mass').if_parameter('Exciter Type').has_value('Hammer (bouncing)').and_parameter('Section').has_value('Exciter').else_use('Exc ForceMassProt').with_name('Protrusion').if_parameter('Exciter Type').has_value('Plectrum').and_parameter('Section').has_value('Exciter').else_use('S Decay Ratio').if_parameter('Section').has_value('String').else_use('D Stiffness').if_parameter('Section').has_value('Damper').else_use('Term Fng Stiff').if_parameter('Section').has_value('Termination').else_use('Body Size').if_parameter('Section').has_value('Body'),
                          use('Exc FricStiff').with_name('Friction').if_parameter('Exciter Type').has_value('Bow').and_parameter('Section').has_value('Exciter').else_use('Exc FricStiff').with_name('Stiffness').if_parameter('Exciter Type').has_value('Plectrum').and_parameter('Section').has_value('Exciter').else_use('Exc FricStiff').with_name('Stiffness').if_parameter('Exciter Type').has_value('Hammer').and_parameter('Section').has_value('Exciter').else_use('Exc FricStiff').with_name('Stiffness').if_parameter('Exciter Type').has_value('Hammer (bouncing)').and_parameter('Section').has_value('Exciter').else_use('Str Inharmon').if_parameter('Section').has_value('String').else_use('D Velocity').if_parameter('Section').has_value('Damper').else_use('Term Fret Stiff').if_parameter('Section').has_value('Termination').else_use('Body Mix').if_parameter('Section').has_value('Body'),
                          use('Exc Velocity').if_parameter('Section').has_value('Exciter').else_use('Str Damping').if_parameter('Section').has_value('String').else_use('Damp Pos').if_parameter('Section').has_value('Damper').else_use('Pickup Pos').if_parameter('Section').has_value('Termination').else_use('Body Decay').if_parameter('Section').has_value('Body'),
                          use('E Pos').if_parameter('Section').has_value('Exciter').else_use('D Damping').if_parameter('Section').has_value('Damper').else_use('Body Low-Cut').if_parameter('Section').has_value('Body'),
                          use('Exc Damping').if_parameter('Section').has_value('Exciter').else_use('Body High-Cut').if_parameter('Section').has_value('Body'),
                          'Volume'), 
    
    OPTIONS_KEY: (
                  use('Exciter').if_parameter('Section').has_value('Exciter').else_use('Damper').if_parameter('Section').has_value('Damper').else_use('Termination').if_parameter('Section').has_value('Termination').else_use('Body').if_parameter('Section').has_value('Body'),
                  '',
                  use('Gated').if_parameter('Section').has_value('Damper'),
                  use('Pickup').if_parameter('Section').has_value('Termination'),
                  use('Fixed Exc').if_parameter('Section').has_value('Exciter').else_use('Fixed Damp').if_parameter('Section').has_value('Damper'),
                  '',
                  '')}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: ('Filter Type', 'Filter Freq', 'Filter Reso', 'Freq < Env', 'FEG Attack', 'FEG Decay',
 'FEG Sustain', 'FEG Release'), 
    
    OPTIONS_KEY: ('Filter', '', '', 'Filt Env', '', '', '')}),
  (
   'LFO',
   {BANK_PARAMETERS_KEY: (
                          'LFO Shape',
                          use('LFO Speed').if_parameter('LFO Sync On').has_value('Hertz').else_use('LFO SyncRate'),
                          'LFO Fade In',
                          'LFO Delay',
                          '',
                          '',
                          '',
                          ''), 
    
    OPTIONS_KEY: ('LFO Sync On', 'LFO', '', '', '', '', '')}),
  (
   'Vib & Uni',
   {BANK_PARAMETERS_KEY: (
                          'Vib & Uni',
                          use('Vib Delay').if_parameter('Vib & Uni').has_value('Vib').else_use('Uni Delay'),
                          use('Vib Fade-In').if_parameter('Vib & Uni').has_value('Vib').else_use('Unison Voices'),
                          use('Vib Speed').if_parameter('Vib & Uni').has_value('Vib').else_use('Uni Detune'),
                          use('Vib Amount').if_parameter('Vib & Uni').has_value('Vib').else_use('Porta Time'),
                          use('Vib Error').if_parameter('Vib & Uni').has_value('Vib'),
                          use('Vib < ModWh').if_parameter('Vib & Uni').has_value('Vib'),
                          ''), 
    
    OPTIONS_KEY: (
                  use('Vibrato').if_parameter('Vib & Uni').has_value('Vib').else_use('Unison'),
                  use('Unison Voices').if_parameter('Vib & Uni').has_value('Uni'),
                  '',
                  use('Portamento').if_parameter('Vib & Uni').has_value('Uni'),
                  use('Proportional').if_parameter('Vib & Uni').has_value('Uni'),
                  use('Legato').if_parameter('Vib & Uni').has_value('Uni'),
                  '')}),
  (
   'Modulation',
   {BANK_PARAMETERS_KEY: (
                          'Mod Source',
                          use('Key Dest').if_parameter('Mod Source').has_value('Key').else_use('Vel Dest').if_parameter('Mod Source').has_value('Vel').else_use('PB Range').if_parameter('Mod Source').has_value('PB').else_use('Press Dest A').if_parameter('Mod Source').has_value('Press').else_use('Slide Dest A').if_parameter('Mod Source').has_value('Slide'),
                          use('Exc ForceMassProt < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Key Dest').has_value('Exciter').else_use('D Mass < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Key Dest').has_value('Damper').else_use('T Mass < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Key Dest').has_value('Term/String').else_use('Exc ForceMassProt < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Vel Dest').has_value('Exciter').else_use('T Mass < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Vel Dest').has_value('Term/Damp').else_use('FEG Att < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Vel Dest').has_value('Env').else_use('Note PB Range').if_parameter('Mod Source').has_value('PB').else_use('Press Amt A').if_parameter('Mod Source').has_value('Press').else_use('Slide Amt A').if_parameter('Mod Source').has_value('Slide'),
                          use('Exc FricStiff < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Key Dest').has_value('Exciter').else_use('D Stiff < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Key Dest').has_value('Damper').else_use('S Decay < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Key Dest').has_value('Term/String').else_use('Exc FricStiff < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Vel Dest').has_value('Exciter').else_use('D Pos < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Vel Dest').has_value('Term/Damp').else_use('FEG < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Vel Dest').has_value('Env').else_use('Press Dest B').if_parameter('Mod Source').has_value('Press').else_use('Slide Dest B').if_parameter('Mod Source').has_value('Slide'),
                          use('Exc Vel < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Key Dest').has_value('Exciter').else_use('D Velo < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Key Dest').has_value('Damper').else_use('S Damp < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Key Dest').has_value('Term/String').else_use('Exc Vel < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Vel Dest').has_value('Exciter').else_use('Press Amt B').if_parameter('Mod Source').has_value('Press').else_use('Slide Amt B').if_parameter('Mod Source').has_value('Slide'),
                          use('E Pos < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Key Dest').has_value('Exciter').else_use('D Pos < Key').if_parameter('Mod Source').has_value('Key').and_parameter('Key Dest').has_value('Damper').else_use('E Pos < Vel').if_parameter('Mod Source').has_value('Vel').and_parameter('Vel Dest').has_value('Exciter'),
                          '',
                          '')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: ('Octave', 'Semitone', 'Fine Tune', 'PB Range', 'Note PB Range', 'Voices', 'Stretch',
 'Error'), 
    
    OPTIONS_KEY: ('', '', '', '', 'Key Priority', '', '')}))), 
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
                          use('MIDI Note Mod Amount').with_name('Key'),
                          use('MIDI Pitch Bend Mod Amount').with_name('PB Range'),
                          use('MIDI Aftertouch Mod Amount').with_name('Pressure'),
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
   {BANK_PARAMETERS_KEY: ('Amp Type', 'Bass', 'Middle', 'Treble', 'Presence', 'Gain', 'Volume', 'Dry/Wet'), 
    
    OPTIONS_KEY: ('', '', '', '', '', '', 'Dual Mono')}),)), 
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
 'Drift':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Osc Select',
                          use('Osc 1 Wave').if_parameter('Osc Select').has_value('Osc 1').else_use('Osc 2 Wave'),
                          use('Osc 1 Shape').if_parameter('Osc Select').has_value('Osc 1').else_use('Osc 2 Detune'),
                          use('Osc 1 Oct').if_parameter('Osc Select').has_value('Osc 1').else_use('Osc 2 Oct'),
                          use('Osc 1 Gain').if_parameter('Osc Select').has_value('Osc 1').else_use('Osc 2 Gain'),
                          'LP Freq',
                          'LP Reso',
                          'Volume'), 
    
    OPTIONS_KEY: (
                  'Osc Retrig',
                  '',
                  '',
                  use('Osc 1').if_parameter('Osc Select').has_value('Osc 1').else_use('Osc 2'),
                  '',
                  '',
                  '')}),
  (
   'Oscillator',
   {BANK_PARAMETERS_KEY: (
                          'Osc Select',
                          use('Osc 1 Wave').if_parameter('Osc Select').has_value('Osc 1').else_use('Osc 2 Wave'),
                          use('Osc 1 Shape').if_parameter('Osc Select').has_value('Osc 1').else_use('Osc 2 Detune'),
                          use('Osc 1 Oct').if_parameter('Osc Select').has_value('Osc 1').else_use('Osc 2 Oct'),
                          use('Osc 1 Gain').if_parameter('Osc Select').has_value('Osc 1').else_use('Osc 2 Gain'),
                          use('Shape Mod Src').if_parameter('Osc Select').has_value('Osc 1').else_use(''),
                          use('Osc 1 Shape Mod Amt').if_parameter('Osc Select').has_value('Osc 1').else_use(''),
                          'Noise Gain'), 
    
    OPTIONS_KEY: (
                  'Osc Retrig',
                  '',
                  '',
                  use('Osc 1').if_parameter('Osc Select').has_value('Osc 1').else_use('Osc 2'),
                  '',
                  '',
                  'Noise')}),
  (
   'Filter',
   {BANK_PARAMETERS_KEY: ('LP Type', 'LP Freq', 'LP Reso', 'HP Freq', 'LP Mod Src 1', 'LP Mod Amt 1', 'LP Mod Src 2',
 'LP Mod Amt 2'), 
    
    OPTIONS_KEY: ('Osc 1 Flt', 'Osc 2 Flt', 'Noise Flt', '', '', '', '')}),
  (
   'Envelopes',
   {BANK_PARAMETERS_KEY: (
                          'Env 1 Attack',
                          'Env 1 Decay',
                          'Env 1 Sustain',
                          'Env 1 Release',
                          use('Env 2 Attack').if_parameter('Env 2 Cyc On').has_value('Env').else_use('Cyc Env Tilt'),
                          use('Env 2 Decay').if_parameter('Env 2 Cyc On').has_value('Env').else_use('Cyc Env Hold'),
                          use('Env 2 Sustain').if_parameter('Env 2 Cyc On').has_value('Env').else_use('Cyc Env Time Mode'),
                          use('Env 2 Release').if_parameter('Env 2 Cyc On').has_value('Env').else_use('Cyc Env Rate').if_parameter('Env 2 Cyc On').has_value('Cyc').and_parameter('Cyc Env Time Mode').has_value('Freq').else_use('Cyc Env Ratio').if_parameter('Env 2 Cyc On').has_value('Cyc').and_parameter('Cyc Env Time Mode').has_value('Ratio').else_use('Cyc Env Time').if_parameter('Env 2 Cyc On').has_value('Cyc').and_parameter('Cyc Env Time Mode').has_value('Time').else_use('Cyc Env Synced').if_parameter('Env 2 Cyc On').has_value('Cyc').and_parameter('Cyc Env Time Mode').has_value('Sync')), 
    
    OPTIONS_KEY: ('', '', '', 'Env 2 Cyc On', '', '', '')}),
  (
   'LFOs',
   {BANK_PARAMETERS_KEY: (
                          'LFO Wave',
                          'LFO Time Mode',
                          use('LFO Rate').if_parameter('LFO Time Mode').has_value('Freq').else_use('LFO Ratio').if_parameter('LFO Time Mode').has_value('Ratio').else_use('LFO Time').if_parameter('LFO Time Mode').has_value('Time').else_use('LFO Synced').if_parameter('LFO Time Mode').has_value('Sync'),
                          'LFO Amt',
                          'LFO Mod Src',
                          'LFO Mod Amt',
                          '',
                          ''), 
    
    OPTIONS_KEY: ('LFO Retrig', '', '', '', '', '', '')}),
  (
   'Fixed Mod',
   {BANK_PARAMETERS_KEY: (
                          'Mod Dest',
                          use('Shape Mod Src').if_parameter('Mod Dest').has_value('Shape').else_use('LP Mod Src 1').if_parameter('Mod Dest').has_value('Filter').else_use('Pitch Mod Src 1').if_parameter('Mod Dest').has_value('Pitch').else_use('LFO Mod Src').if_parameter('Mod Dest').has_value('LFO'),
                          use('Osc 1 Shape Mod Amt').if_parameter('Mod Dest').has_value('Shape').else_use('LP Mod Amt 1').if_parameter('Mod Dest').has_value('Filter').else_use('Pitch Mod Amt 1').if_parameter('Mod Dest').has_value('Pitch').else_use('LFO Mod Amt').if_parameter('Mod Dest').has_value('LFO'),
                          use('LP Mod Src 2').if_parameter('Mod Dest').has_value('Filter').else_use('Pitch Mod Src 2').if_parameter('Mod Dest').has_value('Pitch').else_use(''),
                          use('LP Mod Amt 2').if_parameter('Mod Dest').has_value('Filter').else_use('Pitch Mod Amt 2').if_parameter('Mod Dest').has_value('Pitch').else_use(''),
                          use('Key > LPF').if_parameter('Mod Dest').has_value('Filter').else_use(''),
                          '',
                          'Vel > Vol')}),
  (
   'Custom Mod',
   {BANK_PARAMETERS_KEY: (
                          'Mod Slot',
                          use('Mod Source 1').if_parameter('Mod Slot').has_value('1').else_use('Mod Source 2').if_parameter('Mod Slot').has_value('2').else_use('Mod Source 3').if_parameter('Mod Slot').has_value('3'),
                          use('Mod Matrix Amt 1').if_parameter('Mod Slot').has_value('1').else_use('Mod Matrix Amt 2').if_parameter('Mod Slot').has_value('2').else_use('Mod Matrix Amt 3').if_parameter('Mod Slot').has_value('3'),
                          use('Mod Dest 1').if_parameter('Mod Slot').has_value('1').else_use('Mod Dest 2').if_parameter('Mod Slot').has_value('2').else_use('Mod Dest 3').if_parameter('Mod Slot').has_value('3'),
                          '',
                          '',
                          '',
                          '')}),
  (
   'Global',
   {BANK_PARAMETERS_KEY: (
                          'Voice Mode',
                          use('').if_parameter('Voice Mode').has_value('Poly').else_use('Thickness').if_parameter('Voice Mode').has_value('Mono').else_use('Spread').if_parameter('Voice Mode').has_value('Stereo').else_use('Strength').if_parameter('Voice Mode').has_value('Unison'),
                          'Voice Count',
                          'Glide Time',
                          'PB Range',
                          'Drift',
                          'Transpose',
                          'Volume'), 
    
    OPTIONS_KEY: ('', '', 'Legato', 'Note PB', '', '', '')}))), 
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
   {BANK_PARAMETERS_KEY: ('Interval', 'Offset', 'Grid', 'Variation', 'Variation Type', 'Gate', 'Chance', 'Volume'), 
    
    OPTIONS_KEY: ('', 'Triplets', '', '', '', 'Repeat', 'Mix Type')}),
  (
   'Filt/Pitch',
   {BANK_PARAMETERS_KEY: ('Interval', 'Filter Freq', 'Filter Width', 'Pitch', 'Pitch Decay', 'Decay', 'Chance',
 'Volume'), 
    
    OPTIONS_KEY: ('Filter', '', '', '', '', '', '')}))), 
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
                          use('Shape').if_parameter('Mode').has_value('Vibrato').else_use(''),
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
                          use('Mid Freq').with_name('Frequency').if_parameter('Filter On/Off').has_value('On').else_use(''),
                          use('Width').with_name('Bandwidth').if_parameter('Filter On/Off').has_value('On').else_use(''),
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
   {BANK_PARAMETERS_KEY: ('FreqLo', 'GainLo', 'GainMid', 'GainHi', 'FreqHi', '', '', ''), 
    
    OPTIONS_KEY: ('Low', 'Mid', 'High', 'Slope', '', '', '')}),)), 
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
                          'Chan Select',
                          use('1 Filter Freq').if_parameter('Chan Select').has_value('L').else_use('2 Filter Freq').if_parameter('Chan Select').has_value('L+R').else_use('3 Filter Freq').if_parameter('Chan Select').has_value('R').else_use(''),
                          use('1 Filter Width').if_parameter('Chan Select').has_value('L').else_use('2 Filter Width').if_parameter('Chan Select').has_value('L+R').else_use('3 Filter Width').if_parameter('Chan Select').has_value('R').else_use(''),
                          use('1 Beat Delay').if_parameter('Chan Select').has_value('L').and_parameter('1 Delay Mode').has_value('On').else_use('1 Time Delay').if_parameter('Chan Select').has_value('L').and_parameter('1 Delay Mode').has_value('Off').else_use('2 Beat Delay').if_parameter('Chan Select').has_value('L+R').and_parameter('2 Delay Mode').has_value('On').else_use('2 Time Delay').if_parameter('Chan Select').has_value('L+R').and_parameter('2 Delay Mode').has_value('Off').else_use('3 Beat Delay').if_parameter('Chan Select').has_value('R').and_parameter('3 Delay Mode').has_value('On').else_use('3 Time Delay').if_parameter('Chan Select').has_value('R').and_parameter('3 Delay Mode').has_value('Off').else_use(''),
                          use('1 Beat Swing').if_parameter('Chan Select').has_value('L').and_parameter('1 Delay Mode').has_value('On').else_use('2 Beat Swing').if_parameter('Chan Select').has_value('L+R').and_parameter('2 Delay Mode').has_value('On').else_use('3 Beat Swing').if_parameter('Chan Select').has_value('R').and_parameter('3 Delay Mode').has_value('On').else_use(''),
                          use('1 Feedback').if_parameter('Chan Select').has_value('L').else_use('2 Feedback').if_parameter('Chan Select').has_value('L+R').else_use('3 Feedback').if_parameter('Chan Select').has_value('R').else_use(''),
                          use('1 Pan').if_parameter('Chan Select').has_value('L').else_use('2 Pan').if_parameter('Chan Select').has_value('L+R').else_use('3 Pan').if_parameter('Chan Select').has_value('R').else_use(''),
                          use('1 Volume').if_parameter('Chan Select').has_value('L').else_use('2 Volume').if_parameter('Chan Select').has_value('L+R').else_use('3 Volume').if_parameter('Chan Select').has_value('R').else_use('Dry')), 
    
    OPTIONS_KEY: (
                  use('L Filter').if_parameter('Chan Select').has_value('L').else_use('L+R Filter').if_parameter('Chan Select').has_value('L+R').else_use('R Filter').if_parameter('Chan Select').has_value('R').else_use(''),
                  '',
                  use('L Sync').if_parameter('Chan Select').has_value('L').else_use('L+R Sync').if_parameter('Chan Select').has_value('L+R').else_use('R Sync').if_parameter('Chan Select').has_value('R').else_use(''),
                  '',
                  '',
                  '',
                  use('L Channel').if_parameter('Chan Select').has_value('L').else_use('L+R Channel').if_parameter('Chan Select').has_value('L+R').else_use('R Channel').if_parameter('Chan Select').has_value('R').else_use(''))}),)), 
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
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: (
                          'Spray',
                          'Frequency',
                          'Pitch',
                          'Random',
                          'Feedback',
                          use('Time Delay').if_parameter('Delay Mode').has_value('Off').else_use('Beat Delay'),
                          'Beat Swing',
                          'DryWet'), 
    
    OPTIONS_KEY: ('', '', '', '', 'Sync', '', '')}),)), 
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
                          'Mode',
                          use('Mod Rate').with_name('Rate').if_parameter('Mod Sync').has_value('On').else_use('Mod Freq').with_name('Freq'),
                          'Amount',
                          'Feedback',
                          use('Notches').if_parameter('Mode').has_value('Phaser').else_use('Flange Time').with_name('Time').if_parameter('Mode').has_value('Flanger').else_use('Doubler Time').with_name('Time').if_parameter('Mode').has_value('Doubler'),
                          'Warmth',
                          use('Output Gain').with_name('Gain'),
                          'Dry/Wet'), 
    
    OPTIONS_KEY: ('Sync', '', 'FB Inv', '', '', '', '')}),
  (
   'Details',
   {BANK_PARAMETERS_KEY: (
                          'Mode',
                          use('Mod Rate').with_name('Rate').if_parameter('Mod Sync').has_value('On').else_use('Mod Freq').with_name('Freq'),
                          'Amount',
                          'Feedback',
                          use('Notches').if_parameter('Mode').has_value('Phaser').else_use('Flange Time').with_name('Time').if_parameter('Mode').has_value('Flanger').else_use('Doubler Time').with_name('Time').if_parameter('Mode').has_value('Doubler'),
                          use('Center Freq').with_name('Center').if_parameter('Mode').has_value('Phaser').else_use(''),
                          use('Spread').if_parameter('Mode').has_value('Phaser').else_use('Output Gain').with_name('Gain'),
                          use('Mod Blend').with_name('Blend').if_parameter('Mode').has_value('Phaser').else_use('Dry/Wet')), 
    
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
                          'Dry/Wet'), 
    
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
 'Saturator':IndexedDict((
  (
   BANK_MAIN_KEY,
   {BANK_PARAMETERS_KEY: ('Type', 'Drive', 'Base', 'Frequency', 'Width', 'Depth', 'Output', 'Dry/Wet'), 
    
    OPTIONS_KEY: ('', 'Color', '', '', '', 'Soft Clip', '')}),
  (
   'Waveshaper',
   {BANK_PARAMETERS_KEY: ('Type', 'WS Drive', 'WS Curve', 'WS Depth', 'WS Lin', 'WS Damp', 'WS Period', 'Dry/Wet')}))), 
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
   {BANK_PARAMETERS_KEY: (
                          'Module',
                          use('Tracing Drive').if_parameter('Module').has_value('Tracing').else_use('Pinch Drive'),
                          use('Tracing Freq.').if_parameter('Module').has_value('Tracing').else_use('Pinch Freq.'),
                          use('Tracing Width').if_parameter('Module').has_value('Tracing').else_use('Pinch Width'),
                          '',
                          'Global Drive',
                          'Crackle Density',
                          'Crackle Volume'), 
    
    OPTIONS_KEY: (
                  use('Tracing').if_parameter('Module').has_value('Tracing').else_use('Pinch'),
                  use('Pinch Mode').if_parameter('Module').has_value('Pinch').else_use(''),
                  use('Pinch Ch').if_parameter('Module').has_value('Pinch').else_use(''),
                  '',
                  '',
                  '',
                  '',
                  '')}),)), 
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
  'Delay': ('Channel', 'L Sync Enum', 'R Sync Enum', 'Link Switch'),
  'Drift': ('Osc Select', 'LP Mod Src 1', 'LP Mod Src 2', 'LFO Mod Src', 'Mod Dest', 'Mod Slot', 'Voice Mode', 'Voice Count', 'PB Range', 'Shape Mod Src', 'Pitch Mod Src 1', 'Pitch Mod Src 2', 'Mod Source 1', 'Mod Source 2', 'Mod Source 3', 'Mod Dest 1', 'Mod Dest 2', 'Mod Dest 3'),
  'UltraAnalog': ('Osc Select', 'Osc / Amp', 'Env Select', 'LFO Select', 'Mod Source', 'Mod Dest', 'Select'),
  'Collision': ('Resonator', 'LFO Select', 'Mod Source', 'Mod Dest'),
  'StringStudio': ('Section', 'Vib & Uni', 'Mod Source'),
  'FilterDelay': 'Chan Select',
  'Vinyl': 'Module',
  'DrumCell': 'Select'}