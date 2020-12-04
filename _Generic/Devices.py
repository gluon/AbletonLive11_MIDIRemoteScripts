#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Generic/Devices.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from builtins import str
from builtins import map
from builtins import filter
from builtins import range
from past.utils import old_div
from functools import partial
from _Framework.Util import group
RCK_BANK1 = (u'Macro 1', u'Macro 2', u'Macro 3', u'Macro 4', u'Macro 5', u'Macro 6', u'Macro 7', u'Macro 8')
RCK_BANK2 = (u'Macro 9', u'Macro 10', u'Macro 11', u'Macro 12', u'Macro 13', u'Macro 14', u'Macro 15', u'Macro 16')
RCK_BANKS = (RCK_BANK1, RCK_BANK2)
RCK_BOBS = (RCK_BANK1,)
RCK_BNK_NAMES = (u'Macros', u'Macros 2')
ALG_BANK1 = (u'OSC1 Level', u'OSC1 Octave', u'OSC1 Semi', u'OSC1 Shape', u'OSC2 Level', u'OSC2 Octave', u'OSC2 Semi', u'OSC2 Shape')
ALG_BANK2 = (u'OSC1 Balance', u'F1 Freq', u'F1 Resonance', u'F1 Type', u'OSC2 Balance', u'F2 Freq', u'F2 Resonance', u'F2 Type')
ALG_BANK3 = (u'FEG1 Attack', u'FEG1 Decay', u'FEG1 Sustain', u'FEG1 Rel', u'FEG2 Attack', u'FEG2 Decay', u'FEG2 Sustain', u'FEG2 Rel')
ALG_BANK4 = (u'F1 On/Off', u'F1 Freq < LFO', u'F1 Freq < Env', u'F1 Res < LFO', u'F2 On/Off', u'F2 Freq < LFO', u'F2 Freq < Env', u'F2 Res < LFO')
ALG_BANK5 = (u'AEG1 Attack', u'AEG1 Decay', u'AEG1 Sustain', u'AEG1 Rel', u'AEG2 Attack', u'AEG2 Decay', u'AEG2 Sustain', u'AEG2 Rel')
ALG_BANK6 = (u'AMP1 Level', u'AMP1 Pan', u'LFO1 Shape', u'LFO1 Speed', u'AMP2 Level', u'AMP2 Pan', u'LFO2 Shape', u'LFO2 Speed')
ALG_BANK7 = (u'Volume', u'Noise On/Off', u'Noise Level', u'Noise Color', u'Unison On/Off', u'Unison Detune', u'Vib On/Off', u'Vib Amount')
ALG_BOB = (u'F1 Freq', u'F1 Resonance', u'OSC1 Shape', u'OSC1 Octave', u'OSC2 Shape', u'OSC2 Octave', u'OSC2 Detune', u'Volume')
ALG_BANKS = (ALG_BANK1,
 ALG_BANK2,
 ALG_BANK3,
 ALG_BANK4,
 ALG_BANK5,
 ALG_BANK6,
 ALG_BANK7)
ALG_BOBS = (ALG_BOB,)
ALG_BNK_NAMES = (u'Oscillators', u'Filters', u'Filter Envelopes', u'Filter Modulation', u'Volume Envelopes', u'Mix', u'Output')
COL_BANK1 = (u'Mallet On/Off', u'Mallet Volume', u'Mallet Noise Amount', u'Mallet Stiffness', u'Mallet Noise Color', u'', u'', u'')
COL_BANK2 = (u'Noise Volume', u'Noise Filter Type', u'Noise Filter Freq', u'Noise Filter Q', u'Noise Attack', u'Noise Decay', u'Noise Sustain', u'Noise Release')
COL_BANK3 = (u'Res 1 Decay', u'Res 1 Material', u'Res 1 Type', u'Res 1 Quality', u'Res 1 Tune', u'Res 1 Fine Tune', u'Res 1 Pitch Env.', u'Res 1 Pitch Env. Time')
COL_BANK4 = (u'Res 1 Listening L', u'Res 1 Listening R', u'Res 1 Hit', u'Res 1 Brightness', u'Res 1 Inharmonics', u'Res 1 Radius', u'Res 1 Opening', u'Res 1 Ratio')
COL_BANK5 = (u'Res 2 Decay', u'Res 2 Material', u'Res 2 Type', u'Res 2 Quality', u'Res 2 Tune', u'Res 2 Fine Tune', u'Res 2 Pitch Env.', u'Res 2 Pitch Env. Time')
COL_BANK6 = (u'Res 2 Listening L', u'Res 2 Listening R', u'Res 2 Hit', u'Res 2 Brightness', u'Res 2 Inharmonics', u'Res 2 Radius', u'Res 2 Opening', u'Res 2 Ratio')
COL_BOB = (u'Res 1 Brightness', u'Res 1 Type', u'Mallet Stiffness', u'Mallet Noise Amount', u'Res 1 Inharmonics', u'Res 1 Decay', u'Res 1 Tune', u'Volume')
COL_BANKS = (COL_BANK1,
 COL_BANK2,
 COL_BANK3,
 COL_BANK4,
 COL_BANK5,
 COL_BANK6)
COL_BOBS = (COL_BOB,)
COL_BNK_NAMES = (u'Mallet', u'Noise', u'Resonator 1, Set A', u'Resonator 1, Set B', u'Resonator 2, Set A', u'Resonator 2, Set B')
ELC_BANK1 = (u'M Stiffness', u'M Force', u'Noise Pitch', u'Noise Decay', u'Noise Amount', u'F Tine Color', u'F Tine Decay', u'F Tine Vol')
ELC_BANK2 = (u'F Tone Decay', u'F Tone Vol', u'F Release', u'Damp Tone', u'Damp Balance', u'Damp Amount', u'', u'')
ELC_BANK3 = (u'P Symmetry', u'P Distance', u'P Amp In', u'P Amp Out', u'Pickup Model', u'', u'', u'')
ELC_BANK4 = (u'M Stiff < Vel', u'M Stiff < Key', u'M Force < Vel', u'M Force < Key', u'Noise < Key', u'F Tine < Key', u'P Amp < Key', u'')
ELC_BANK5 = (u'Volume', u'Voices', u'Semitone', u'Detune', u'KB Stretch', u'PB Range', u'', u'')
ELC_BOB = (u'M Stiffness', u'M Force', u'Noise Amount', u'F Tine Vol', u'F Tone Vol', u'F Release', u'P Symmetry', u'Volume')
ELC_BANKS = (ELC_BANK1,
 ELC_BANK2,
 ELC_BANK3,
 ELC_BANK4,
 ELC_BANK5)
ELC_BOBS = (ELC_BOB,)
ELC_BNK_NAMES = (u'Mallet and Tine', u'Tone and Damper', u'Pickup', u'Modulation', u'Global')
IMP_BANK1 = (u'1 Start', u'1 Transpose', u'1 Stretch Factor', u'1 Saturator Drive', u'1 Filter Freq', u'1 Filter Res', u'1 Pan', u'1 Volume')
IMP_BANK2 = (u'2 Start', u'2 Transpose', u'2 Stretch Factor', u'2 Saturator Drive', u'2 Filter Freq', u'2 Filter Res', u'2 Pan', u'2 Volume')
IMP_BANK3 = (u'3 Start', u'3 Transpose', u'3 Stretch Factor', u'3 Saturator Drive', u'3 Filter Freq', u'3 Filter Res', u'3 Pan', u'3 Volume')
IMP_BANK4 = (u'4 Start', u'4 Transpose', u'4 Stretch Factor', u'4 Saturator Drive', u'4 Filter Freq', u'4 Filter Res', u'4 Pan', u'4 Volume')
IMP_BANK5 = (u'5 Start', u'5 Transpose', u'5 Stretch Factor', u'5 Saturator Drive', u'5 Filter Freq', u'5 Filter Res', u'5 Pan', u'5 Volume')
IMP_BANK6 = (u'6 Start', u'6 Transpose', u'6 Stretch Factor', u'6 Saturator Drive', u'6 Filter Freq', u'6 Filter Res', u'6 Pan', u'6 Volume')
IMP_BANK7 = (u'7 Start', u'7 Transpose', u'7 Stretch Factor', u'7 Saturator Drive', u'7 Filter Freq', u'7 Filter Res', u'7 Pan', u'7 Volume')
IMP_BANK8 = (u'8 Start', u'8 Transpose', u'8 Stretch Factor', u'8 Saturator Drive', u'8 Filter Freq', u'8 Filter Res', u'8 Pan', u'8 Volume')
IMP_BOB = (u'Global Time', u'Global Transpose', u'1 Transpose', u'2 Transpose', u'3 Transpose', u'4 Transpose', u'5 Transpose', u'6 Transpose')
IMP_BANKS = (IMP_BANK1,
 IMP_BANK2,
 IMP_BANK3,
 IMP_BANK4,
 IMP_BANK5,
 IMP_BANK6,
 IMP_BANK7,
 IMP_BANK8)
IMP_BOBS = (IMP_BOB,)
IMP_BNK_NAMES = (u'Pad 1', u'Pad 2', u'Pad 3', u'Pad 4', u'Pad 5', u'Pad 6', u'Pad 7', u'Pad 8')
OPR_BANK1 = (u'Ae Attack', u'Ae Decay', u'Ae Sustain', u'Ae Release', u'A Coarse', u'A Fine', u'Osc-A Lev < Vel', u'Osc-A Level')
OPR_BANK2 = (u'Be Attack', u'Be Decay', u'Be Sustain', u'Be Release', u'B Coarse', u'B Fine', u'Osc-B Lev < Vel', u'Osc-B Level')
OPR_BANK3 = (u'Ce Attack', u'Ce Decay', u'Ce Sustain', u'Ce Release', u'C Coarse', u'C Fine', u'Osc-C Lev < Vel', u'Osc-C Level')
OPR_BANK4 = (u'De Attack', u'De Decay', u'De Sustain', u'De Release', u'D Coarse', u'D Fine', u'Osc-D Lev < Vel', u'Osc-D Level')
OPR_BANK5 = (u'Le Attack', u'Le Decay', u'Le Sustain', u'Le Release', u'LFO Rate', u'LFO Amt', u'LFO Type', u'LFO R < K')
OPR_BANK6 = (u'Fe Attack', u'Fe Decay', u'Fe Sustain', u'Fe Release', u'Filter Freq', u'Filter Res', u'Fe R < Vel', u'Fe Amount')
OPR_BANK7 = (u'Pe Attack', u'Pe Decay', u'Pe Sustain', u'Pe Release', u'Pe Init', u'Glide Time', u'Pe Amount', u'Spread')
OPR_BANK8 = (u'Time < Key', u'Panorama', u'Pan < Key', u'Pan < Rnd', u'Algorithm', u'Time', u'Tone', u'Volume')
OPR_BOB = (u'Filter Freq', u'Filter Res', u'A Coarse', u'A Fine', u'B Coarse', u'B Fine', u'Osc-B Level', u'Volume')
OPR_BANKS = (OPR_BANK1,
 OPR_BANK2,
 OPR_BANK3,
 OPR_BANK4,
 OPR_BANK5,
 OPR_BANK6,
 OPR_BANK7,
 OPR_BANK8)
OPR_BOBS = (OPR_BOB,)
OPR_BNK_NAMES = (u'Oscillator A', u'Oscillator B', u'Oscillator C', u'Oscillator D', u'LFO', u'Filter', u'Pitch Modulation', u'Routing')
SAM_BANK1 = (u'Volume', u'Ve Attack', u'Ve Decay', u'Ve Sustain', u'Ve Release', u'Vol < Vel', u'Ve R < Vel', u'Time')
SAM_BANK2 = (u'Filter Type', u'Filter Morph', u'Filter Freq', u'Filter Res', u'Filt < Vel', u'Filt < Key', u'Fe < Env', u'Shaper Amt')
SAM_BANK3 = (u'Fe Attack', u'Fe Decay', u'Fe Sustain', u'Fe Release', u'Fe End', u'Fe Mode', u'Fe Loop', u'Fe Retrig')
SAM_BANK4 = (u'L 1 Wave', u'L 1 Sync', u'L 1 Sync Rate', u'L 1 Rate', u'Vol < LFO', u'Filt < LFO', u'Pan < LFO', u'Pitch < LFO')
SAM_BANK5 = (u'L 2 Wave', u'L 2 Sync', u'L 2 Sync Rate', u'L 2 Rate', u'L 2 R < Key', u'L 2 St Mode', u'L 2 Spin', u'L 2 Phase')
SAM_BANK6 = (u'L 3 Wave', u'L 3 Sync', u'L 3 Sync Rate', u'L 3 Rate', u'L 3 R < Key', u'L 3 St Mode', u'L 3 Spin', u'L 3 Phase')
SAM_BANK7 = (u'O Mode', u'O Volume', u'O Coarse', u'O Fine', u'Oe Attack', u'Oe Decay', u'Oe Sustain', u'Oe Release')
SAM_BANK8 = (u'Transpose', u'Spread', u'Pe < Env', u'Pe Attack', u'Pe Peak', u'Pe Decay', u'Pe Sustain', u'Pe Release')
SAM_BOB = (u'Filter Freq', u'Filter Res', u'Fe < Env', u'Fe Decay', u'Ve Attack', u'Ve Release', u'Transpose', u'Volume')
SAM_BANKS = (SAM_BANK1,
 SAM_BANK2,
 SAM_BANK3,
 SAM_BANK4,
 SAM_BANK5,
 SAM_BANK6,
 SAM_BANK7,
 SAM_BANK8)
SAM_BOBS = (SAM_BOB,)
SAM_BNK_NAMES = (u'Volume', u'Filter', u'Filter Envelope', u'LFO 1', u'LFO 2', u'LFO 3', u'Oscillator', u'Pitch')
SIM_BANK1 = (u'Ve Attack', u'Ve Decay', u'Ve Sustain', u'Ve Release', u'S Start', u'S Loop Length', u'S Length', u'S Loop Fade')
SIM_BANK2 = (u'Fe Attack', u'Fe Decay', u'Fe Sustain', u'Fe Release', u'Filter Freq', u'Filter Res', u'Filt < Vel', u'Fe < Env')
SIM_BANK3 = (u'L Attack', u'L Rate', u'L R < Key', u'L Wave', u'Vol < LFO', u'Filt < LFO', u'Pitch < LFO', u'Pan < LFO')
SIM_BANK4 = (u'Pe Attack', u'Pe Decay', u'Pe Sustain', u'Pe Release', u'Glide Time', u'Spread', u'Pan', u'Volume')
SIM_BOB = (u'Filter Freq', u'Filter Res', u'S Start', u'S Length', u'Ve Attack', u'Ve Release', u'Transpose', u'Volume')
SIM_BANKS = (SIM_BANK1,
 SIM_BANK2,
 SIM_BANK3,
 SIM_BANK4)
SIM_BOBS = (SIM_BOB,)
SIM_BNK_NAMES = (u'Amplitude', u'Filter', u'LFO', u'Pitch Modifiers')
TNS_BANK1 = (u'Excitator Type', u'String Decay', u'Str Inharmon', u'Str Damping', u'Exc ForceMassProt', u'Exc FricStiff', u'Exc Velocity', u'E Pos')
TNS_BANK2 = (u'Damper On', u'Damper Mass', u'D Stiffness', u'D Velocity', u'Damp Pos', u'D Damping', u'D Pos < Vel', u'D Pos Abs')
TNS_BANK3 = (u'Term On/Off', u'Term Mass', u'Term Fng Stiff', u'Term Fret Stiff', u'Pickup On/Off', u'Pickup Pos', u'T Mass < Vel', u'T Mass < Key')
TNS_BANK4 = (u'Body On/Off', u'Body Type', u'Body Size', u'Body Decay', u'Body Low-Cut', u'Body High-Cut', u'Body Mix', u'Volume')
TNS_BANK5 = (u'Vibrato On/Off', u'Vib Delay', u'Vib Fade-In', u'Vib Speed', u'Vib Amount', u'Vib < ModWh', u'Vib Error', u'Volume')
TNS_BANK6 = (u'Filter On/Off', u'Filter Type', u'Filter Freq', u'Filter Reso', u'Freq < Env', u'Freq < LFO', u'Reso < Env', u'Reso < LFO')
TNS_BANK7 = (u'FEG On/Off', u'FEG Attack', u'FEG Decay', u'FEG Sustain', u'FEG Release', u'LFO On/Off', u'LFO Shape', u'LFO Speed')
TNS_BANK8 = (u'Unison On/Off', u'Uni Detune', u'Porta On/Off', u'Porta Time', u'Voices', u'Octave', u'Semitone', u'Volume')
TNS_BOB = (u'Filter Freq', u'Filter Reso', u'Filter Type', u'Excitator Type', u'E Pos', u'String Decay', u'Str Damping', u'Volume')
TNS_BANKS = (TNS_BANK1,
 TNS_BANK2,
 TNS_BANK3,
 TNS_BANK4,
 TNS_BANK5,
 TNS_BANK6,
 TNS_BANK7,
 TNS_BANK8)
TNS_BOBS = (TNS_BOB,)
TNS_BNK_NAMES = (u'Excitator and String', u'Damper', u'Termination and Pickup', u'Body', u'Vibrato', u'Filter', u'Envelope and LFO', u'Global')
WVT_BANK1 = (u'Osc 1 Transp', u'Osc 1 Detune', u'Osc 1 Pos', u'Osc 1 Effect 1', u'Osc 1 Effect 2', u'Osc 1 Pan', u'Osc 1 Gain', u'Osc 1 On')
WVT_BANK2 = (u'Osc 2 Transp', u'Osc 2 Detune', u'Osc 2 Pos', u'Osc 2 Effect 1', u'Osc 2 Effect 2', u'Osc 2 Pan', u'Osc 2 Gain', u'Osc 2 On')
WVT_BANK3 = (u'Filter 1 On', u'Filter 1 Freq', u'Filter 1 Res', u'Filter 1 Drive', u'Filter 1 Type', u'Filter 1 Slope', u'Filter 1 LP/HP', u'Filter 1 BP/NO/Morph')
WVT_BANK4 = (u'Filter 2 On', u'Filter 2 Freq', u'Filter 2 Res', u'Filter 2 Drive', u'Filter 2 Type', u'Filter 2 Slope', u'Filter 2 LP/HP', u'Filter 2 BP/NO/Morph')
WVT_BANK5 = (u'Amp Attack', u'Amp Decay', u'Amp Sustain', u'Amp Release', u'Amp A Slope', u'Amp D Slope', u'Amp R Slope', u'Amp Loop Mode')
WVT_BANK6 = (u'Env 2 Attack', u'Env 2 Decay', u'Env 2 Sustain', u'Env 2 Release', u'Env 3 Attack', u'Env 3 Decay', u'Env 3 Sustain', u'Env 3 Release')
WVT_BANK7 = (u'LFO 1 Amount', u'LFO 1 Rate', u'LFO 1 S. Rate', u'LFO 1 Sync', u'LFO 2 Amount', u'LFO 2 Rate', u'LFO 2 S. Rate', u'LFO 2 Sync')
WVT_BANK8 = (u'Time', u'Global Mod Amount', u'Unison Amount', u'Transpose', u'Glide', u'Sub Gain', u'Sub Transpose', u'Volume')
WVT_BOB = (u'Osc 1 Pos', u'Osc 1 Transp', u'Osc 2 Pos', u'Osc 2 Transp', u'Filter 1 Freq', u'Filter 1 Res', u'Global Mod Amount', u'Volume')
WVT_BANKS = (WVT_BANK1,
 WVT_BANK2,
 WVT_BANK3,
 WVT_BANK4,
 WVT_BANK5,
 WVT_BANK6,
 WVT_BANK7,
 WVT_BANK8)
WVT_BOBS = (WVT_BOB,)
WVT_BANK_NAMES = (u'Oscillator 1', u'Oscillator 2', u'Filter 1', u'Filter 2', u'Amp Envelope', u'Envelope 2/3', u'LFO 1/2', u'Global')
ARP_BANK1 = (u'Style', u'Groove', u'Offset', u'Synced Rate', u'Retrigger Mode', u'Ret. Interval', u'Repeats', u'Gate')
ARP_BANK2 = (u'Tranpose Mode', u'Tranpose Key', u'Transp. Steps', u'Transp. Dist.', u'Velocity Decay', u'Velocity Target', u'Velocity On', u'Vel. Retrigger')
ARP_BOB = (u'Synced Rate', u'Free Rate', u'Transp. Steps', u'Transp. Dist.', u'Gate', u'Tranpose Key', u'Velocity Decay', u'Velocity Target')
ARP_BANKS = (ARP_BANK1, ARP_BANK2)
ARP_BOBS = (ARP_BOB,)
ARP_BNK_NAMES = (u'Style', u'Pitch/Velocity')
CRD_BANK1 = (u'Shift1', u'Shift2', u'Shift3', u'Shift4', u'Shift5', u'Shift6', u'', u'')
CRD_BANK2 = (u'Velocity1', u'Velocity2', u'Velocity3', u'Velocity4', u'Velocity5', u'Velocity6', u'', u'')
CRD_BOB = (u'Shift1', u'Shift2', u'Shift3', u'Shift4', u'Shift5', u'Velocity5', u'Shift6', u'Velocity6')
CRD_BANKS = (CRD_BANK1, CRD_BANK2)
CRD_BOBS = (CRD_BOB,)
CRD_BNK_NAMES = (u'Shift', u'Shift %')
NTL_BANK1 = (u'Sync On', u'Time Length', u'Synced Length', u'Gate', u'On/Off-Balance', u'Decay Time', u'Decay Key Scale', u'')
NTL_BANKS = (NTL_BANK1,)
NTL_BOBS = (NTL_BANK1,)
PIT_BANK1 = (u'Pitch', u'Range', u'Lowest', u'', u'', u'', u'', u'')
PIT_BANKS = (PIT_BANK1,)
PIT_BOBS = (PIT_BANK1,)
RND_BANK1 = (u'Chance', u'Choices', u'Scale', u'Sign', u'', u'', u'', u'')
RND_BANKS = (RND_BANK1,)
RND_BOBS = (RND_BANK1,)
SCL_BANK1 = (u'Base', u'Transpose', u'Range', u'Lowest', u'', u'', u'', u'')
SCL_BANKS = (SCL_BANK1,)
SCL_BOBS = (SCL_BANK1,)
VEL_BANK1 = (u'Drive', u'Compand', u'Random', u'Mode', u'Out Hi', u'Out Low', u'Range', u'Lowest')
VEL_BANKS = (VEL_BANK1,)
VEL_BOBS = (VEL_BANK1,)
AMP_BANK1 = (u'Amp Type', u'Bass', u'Middle', u'Treble', u'Presence', u'Gain', u'Volume', u'Dry/Wet')
AMP_BANK2 = (u'Dual Mono', u'', u'', u'', u'', u'', u'', u'')
AMP_BANKS = (AMP_BANK1, AMP_BANK2)
AMP_BOBS = (AMP_BANK1,)
AMP_BNK_NAMES = (u'Global', u'Dual Mono')
AFL_BANK1 = (u'Frequency', u'Resonance', u'Env. Attack', u'Env. Release', u'Env. Modulation', u'LFO Amount', u'LFO Frequency', u'LFO Phase')
AFL_BANK2 = (u'Filter Type', u'LFO Quantize On', u'LFO Quantize Rate', u'LFO Stereo Mode', u'LFO Spin', u'LFO Sync', u'LFO Sync Rate', u'LFO Offset')
AFL_BANK3 = (u'', u'', u'', u'', u'', u'S/C On', u'S/C Mix', u'S/C Gain')
AFL_BOB = (u'Frequency', u'Resonance', u'Filter Type', u'Env. Modulation', u'LFO Amount', u'LFO Waveform', u'LFO Frequency', u'LFO Phase')
AFL_BANKS = (AFL_BANK1, AFL_BANK2, AFL_BANK3)
AFL_BOBS = (AFL_BOB,)
AFL_BNK_NAMES = (u'Filter', u'Filter Extra', u'Side Chain')
APN_BANK1 = (u'Frequency', u'Phase', u'Shape', u'Waveform', u'Sync Rate', u'Offset', u'Width (Random)', u'Amount')
APN_BANKS = (APN_BANK1,)
APN_BOBS = (APN_BANK1,)
BRP_BANK1 = (u'Interval', u'Offset', u'Grid', u'Variation', u'Filter Freq', u'Filter Width', u'Volume', u'Decay')
BRP_BANK2 = (u'Chance', u'Gate', u'Pitch', u'Pitch Decay', u'Filter Freq', u'Filter Width', u'Volume', u'Decay')
BRP_BOB = (u'Grid', u'Interval', u'Offset', u'Gate', u'Pitch', u'Pitch Decay', u'Variation', u'Chance')
BRP_BANKS = (BRP_BANK1, BRP_BANK2)
BRP_BOBS = (BRP_BOB,)
BRP_BNK_NAMES = (u'Repeat Rate', u'Gate/Pitch')
CAB_BANK1 = (u'Cabinet Type', u'Microphone Position', u'Microphone Type', u'Dual Mono', u'', u'', u'', u'Dry/Wet')
CAB_BANKS = (CAB_BANK1,)
CAB_BOBS = (CAB_BANK1,)
CHR_BANK1 = (u'LFO Amount', u'LFO Rate', u'Delay 1 Time', u'Delay 1 HiPass', u'Delay 2 Time', u'Delay 2 Mode', u'Feedback', u'Dry/Wet')
CHR_BANKS = (CHR_BANK1,)
CHR_BOBS = (CHR_BANK1,)
CP3_BANK1 = (u'Threshold', u'Ratio', u'Attack', u'Release', u'Auto Release On/Off', u'Env Mode', u'Knee', u'Model')
CP3_BANK2 = (u'Threshold', u'Expansion Ratio', u'LookAhead', u'S/C Listen', u'S/C Gain', u'Makeup', u'Dry/Wet', u'Output Gain')
CP3_BANK3 = (u'S/C EQ On', u'S/C EQ Type', u'S/C EQ Freq', u'S/C EQ Q', u'S/C EQ Gain', u'S/C On', u'S/C Mix', u'S/C Gain')
CP3_BOB = (u'Threshold', u'Ratio', u'Attack', u'Release', u'Model', u'Knee', u'Dry/Wet', u'Output Gain')
CP3_BANKS = (CP3_BANK1, CP3_BANK2, CP3_BANK3)
CP3_BOBS = (CP3_BOB,)
CP3_BNK_NAMES = (u'Compression', u'Output', u'Side Chain')
CRP_BANK1 = (u'Decay', u'Material', u'Mid Freq', u'Width', u'Bleed', u'Resonance Type', u'Gain', u'Dry Wet')
CRP_BANK2 = (u'Listening L', u'Listening R', u'Hit', u'Brightness', u'Inharmonics', u'Radius', u'Opening', u'Ratio')
CRP_BANK3 = (u'Resonance Type', u'Tune', u'Transpose', u'Fine', u'Spread', u'Resonator Quality', u'Note Off', u'Off Decay')
CRP_BOB = (u'Brightness', u'Resonance Type', u'Material', u'Inharmonics', u'Decay', u'Ratio', u'Tune', u'Dry Wet')
CRP_BANKS = (CRP_BANK1, CRP_BANK2, CRP_BANK3)
CRP_BOBS = (CRP_BOB,)
CRP_BNK_NAMES = (u'Amount', u'Body', u'Tune')
DRB_BANK1 = (u'Drive', u'Drive Type', u'Transients', u'Crunch', u'Boom Freq', u'Boom Amt', u'Boom Decay', u'Boom Audition')
DRB_BANK2 = (u'Trim', u'Output Gain', u'Dry/Wet', u'Compressor On', u'Damping Freq', u'', u'', u'')
DRB_BOB = (u'Drive', u'Drive Type', u'Crunch', u'Boom Amt', u'Trim', u'Damping Freq', u'Output Gain', u'Dry/Wet')
DRB_BANKS = (DRB_BANK1, DRB_BANK2)
DRB_BOBS = (DRB_BOB,)
DRB_BANK_NAMES = (u'Drive', u'Gain')
DTB_BANK1 = (u'Drive', u'Bias', u'Envelope', u'Tone', u'Attack', u'Release', u'Output', u'Dry/Wet')
DTB_BANKS = (DTB_BANK1,)
DTB_BOBS = (DTB_BANK1,)
ECH_BANK1 = (u'L Division', u'R Division', u'L Sync Mode', u'R Sync Mode', u'L 16th', u'R 16th', u'L Sync', u'R Sync')
ECH_BANK2 = (u'L Time', u'R Time', u'L Offset', u'R Offset', u'Link', u'Channel Mode')
ECH_BANK3 = (u'Gate On', u'Gate Thr', u'Gate Release', u'Duck On', u'Duck Thr', u'Duck Release', u'Env Mix')
ECH_BANK4 = (u'Noise On', u'Noise Amt', u'Noise Mrph', u'Wobble On', u'Wobble Amt', u'Wobble Mrph', u'Repitch')
ECH_BANK5 = (u'Feedback', u'Feedback Inv', u'Input Gain', u'Output Gain', u'Clip Dry', u'Dry Wet')
ECH_BANK6 = (u'Filter On', u'HP Freq', u'HP Res', u'LP Freq', u'LP Res')
ECH_BANK7 = (u'Reverb Level', u'Reverb Decay', u'Reverb Loc', u'Stereo Width')
ECH_BANK8 = (u'Mod Wave', u'Mod Sync', u'Mod Rate', u'Mod Freq', u'Mod Phase', u'Dly < Mod', u'Flt < Mod', u'Mod 4x')
ECH_BOB = (u'L Division', u'R Division', u'L Time', u'R Time', u'Input Gain', u'Feedback', u'Stereo Width', u'Dry Wet')
ECH_BANKS = (ECH_BANK1,
 ECH_BANK2,
 ECH_BANK3,
 ECH_BANK4,
 ECH_BANK5,
 ECH_BANK6,
 ECH_BANK7,
 ECH_BANK8)
ECH_BOBS = (ECH_BOB,)
ECH_BANK_NAMES = (u'Sync', u'Time', u'Gate/Ducking', u'Noise/Wobble', u'Gain', u'Filter', u'Reverb', u'Modulation')
EQ8_BANK1 = (u'1 Filter On A', u'2 Filter On A', u'3 Filter On A', u'4 Filter On A', u'5 Filter On A', u'6 Filter On A', u'7 Filter On A', u'8 Filter On A')
EQ8_BANK2 = (u'1 Frequency A', u'2 Frequency A', u'3 Frequency A', u'4 Frequency A', u'5 Frequency A', u'6 Frequency A', u'7 Frequency A', u'8 Frequency A')
EQ8_BANK3 = (u'1 Gain A', u'2 Gain A', u'3 Gain A', u'4 Gain A', u'5 Gain A', u'6 Gain A', u'7 Gain A', u'8 Gain A')
EQ8_BANK4 = (u'1 Resonance A', u'2 Resonance A', u'3 Resonance A', u'4 Resonance A', u'5 Resonance A', u'6 Resonance A', u'7 Resonance A', u'8 Resonance A')
EQ8_BANK5 = (u'1 Filter Type A', u'2 Filter Type A', u'3 Filter Type A', u'4 Filter Type A', u'5 Filter Type A', u'6 Filter Type A', u'7 Filter Type A', u'8 Filter Type A')
EQ8_BANK6 = (u'Adaptive Q', u'', u'', u'', u'', u'', u'Scale', u'Output Gain')
EQ8_BANK7 = (u'3 Gain A', u'3 Frequency A', u'3 Resonance A', u'4 Gain A', u'4 Frequency A', u'4 Resonance A', u'5 Gain A', u'5 Frequency A')
EQ8_BOB = (u'1 Frequency A', u'1 Gain A', u'2 Frequency A', u'2 Gain A', u'3 Frequency A', u'3 Gain A', u'4 Frequency A', u'4 Gain A')
EQ8_BANKS = (EQ8_BANK1,
 EQ8_BANK2,
 EQ8_BANK3,
 EQ8_BANK4,
 EQ8_BANK5,
 EQ8_BANK6,
 EQ8_BANK7)
EQ8_BOBS = (EQ8_BOB,)
EQ8_BNK_NAMES = (u'Band On/Off', u'Frequency', u'Gain', u'Resonance', u'Filter Type', u'Output', u'EQs 3-5')
EQ3_BANK1 = (u'GainLo', u'GainMid', u'GainHi', u'FreqLo', u'LowOn', u'MidOn', u'HighOn', u'FreqHi')
EQ3_BANKS = (EQ3_BANK1,)
EQ3_BOBS = (EQ3_BANK1,)
ERO_BANK1 = (u'Frequency', u'Width', u'Mode', u'Amount', u'', u'', u'', u'')
ERO_BANKS = (ERO_BANK1,)
ERO_BOBS = (ERO_BANK1,)
FLD_BANK1 = (u'1 Filter Freq', u'1 Filter Width', u'1 Beat Delay', u'1 Beat Swing', u'1 Feedback', u'1 Pan', u'1 Volume', u'Dry')
FLD_BANK2 = (u'2 Filter Freq', u'2 Filter Width', u'2 Beat Delay', u'2 Beat Swing', u'2 Feedback', u'2 Pan', u'2 Volume', u'Dry')
FLD_BANK3 = (u'3 Filter Freq', u'3 Filter Width', u'3 Beat Delay', u'3 Beat Swing', u'3 Feedback', u'3 Pan', u'3 Volume', u'Dry')
FLD_BOB = (u'2 Filter Freq', u'2 Filter Width', u'2 Beat Delay', u'2 Feedback', u'1 Volume', u'3 Volume', u'2 Volume', u'Dry')
FLD_BANKS = (FLD_BANK1, FLD_BANK2, FLD_BANK3)
FLD_BOBS = (FLD_BOB,)
FLD_BNK_NAMES = (u'Input L Filter', u'Input L+R Filter', u'Input R Filter')
FLG_BANK1 = (u'Hi Pass', u'Dry/Wet', u'Delay Time', u'Feedback', u'Env. Modulation', u'Env. Attack', u'Env. Release', u'')
FLG_BANK2 = (u'LFO Amount', u'Frequency', u'LFO Phase', u'Sync', u'LFO Offset', u'Sync Rate', u'LFO Width (Random)', u'LFO Waveform')
FLG_BOB = (u'Hi Pass', u'Delay Time', u'Frequency', u'Sync Rate', u'LFO Amount', u'Env. Modulation', u'Feedback', u'Dry/Wet')
FLG_BANKS = (FLG_BANK1, FLG_BANK2)
FLG_BOBS = (FLG_BOB,)
FLG_BNK_NAMES = (u'Frequency Controls', u'LFO / S&H')
FRS_BANK1 = (u'Coarse', u'Fine', u'Mode', u'Ring Mod Frequency', u'Drive On/Off', u'Drive', u'Wide', u'Dry/Wet')
FRS_BANKS = (FRS_BANK1,)
FRS_BOBS = (FRS_BANK1,)
GTE_BANK1 = (u'Threshold', u'Return', u'FlipMode', u'LookAhead', u'Attack', u'Hold', u'Release', u'Floor')
GTE_BANK2 = (u'S/C EQ On', u'S/C EQ Type', u'S/C EQ Freq', u'S/C EQ Q', u'S/C EQ Gain', u'S/C On', u'S/C Mix', u'S/C Gain')
GTE_BANKS = (GTE_BANK1, GTE_BANK2)
GTE_BOBS = (GTE_BANK1,)
GTE_BNK_NAMES = (u'Gate', u'Side Chain')
GLU_BANK1 = (u'Threshold', u'Ratio', u'Attack', u'Release', u'Peak Clip In', u'Range', u'Dry/Wet', u'Makeup')
GLU_BANK2 = (u'S/C EQ On', u'S/C EQ Type', u'S/C EQ Freq', u'S/C EQ Q', u'S/C EQ Gain', u'S/C On', u'S/C Mix', u'S/C Gain')
GLU_BOB = (u'Threshold', u'Ratio', u'Attack', u'Release', u'Peak Clip In', u'Range', u'Makeup', u'Dry/Wet')
GLU_BANKS = (GLU_BANK1, GLU_BANK2)
GLU_BOBS = (GLU_BOB,)
GLU_BNK_NAMES = (u'Compression', u'Side Chain')
GRD_BANK1 = (u'Frequency', u'Pitch', u'Time Delay', u'Beat Swing', u'Random', u'Spray', u'Feedback', u'DryWet')
GRD_BANKS = (GRD_BANK1,)
GRD_BOBS = (GRD_BANK1,)
LPR_BANK1 = (u'State', u'Speed', u'Reverse', u'Quantization', u'Monitor', u'Song Control', u'Tempo Control', u'Feedback')
LPR_BANKS = (LPR_BANK1,)
LPR_BOBS = (LPR_BANK1,)
MBD_BANK1 = (u'Master Output', u'Amount', u'Time Scaling', u'Soft Knee On/Off', u'Peak/RMS Mode', u'Band Activator (High)', u'Band Activator (Mid)', u'Band Activator (Low)')
MBD_BANK2 = (u'Input Gain (Low)', u'Below Threshold (Low)', u'Below Ratio (Low)', u'Above Threshold (Low)', u'Above Ratio (Low)', u'Attack Time (Low)', u'Release Time (Low)', u'Output Gain (Low)')
MBD_BANK3 = (u'Input Gain (Mid)', u'Below Threshold (Mid)', u'Below Ratio (Mid)', u'Above Threshold (Mid)', u'Above Ratio (Mid)', u'Attack Time (Mid)', u'Release Time (Mid)', u'Output Gain (Mid)')
MBD_BANK4 = (u'Input Gain (High)', u'Below Threshold (High)', u'Below Ratio (High)', u'Above Threshold (High)', u'Above Ratio (High)', u'Attack Time (High)', u'Release Time (High)', u'Output Gain (High)')
MBD_BANK5 = (u'Low-Mid Crossover', u'Mid-High Crossover', u'', u'', u'', u'', u'', u'')
MBD_BANK6 = (u'', u'', u'', u'', u'', u'S/C On', u'S/C Mix', u'S/C Gain')
MBD_BOB = (u'Above Threshold (Low)', u'Above Ratio (Low)', u'Above Threshold (Mid)', u'Above Ratio (Mid)', u'Above Threshold (High)', u'Above Ratio (High)', u'Master Output', u'Amount')
MBD_BANKS = (MBD_BANK1,
 MBD_BANK2,
 MBD_BANK3,
 MBD_BANK4,
 MBD_BANK5,
 MBD_BANK6)
MBD_BOBS = (MBD_BOB,)
MBD_BNK_NAMES = (u'Global', u'Low Band', u'Mid Band', u'High Band', u'Split Frequencies', u'Side Chain')
OVR_BANK1 = (u'Filter Freq', u'Filter Width', u'Drive', u'Tone', u'Preserve Dynamics', u'', u'', u'Dry/Wet')
OVR_BANKS = (OVR_BANK1,)
OVR_BOBS = (OVR_BANK1,)
PDL_BANK1 = (u'Type', u'Gain', u'Output', u'Bass', u'Mid', u'Treble', u'Sub', u'Dry/Wet')
PDL_BANK2 = (u'Mid Freq', u'', u'', u'', u'', u'', u'', u'')
PDL_BANKS = (PDL_BANK1, PDL_BANK2)
PDL_BOBS = (PDL_BANK1,)
PDL_BANK_NAMES = (u'General', u'Eq')
PHS_BANK1 = (u'Poles', u'Color', u'Dry/Wet', u'Frequency', u'Env. Modulation', u'Env. Attack', u'Env. Release', u'Feedback')
PHS_BANK2 = (u'LFO Amount', u'LFO Frequency', u'LFO Phase', u'LFO Sync', u'LFO Offset', u'LFO Sync Rate', u'LFO Spin', u'LFO Waveform')
PHS_BOB = (u'Frequency', u'Feedback', u'Poles', u'Env. Modulation', u'Color', u'LFO Amount', u'LFO Frequency', u'Dry/Wet')
PHS_BANKS = (PHS_BANK1, PHS_BANK2)
PHS_BOBS = (PHS_BOB,)
PHS_BNK_NAMES = (u'Frequency Controls', u'LFO / S&H')
PPG_BANK1 = (u'Filter Freq', u'Filter Width', u'Time Delay', u'Beat Delay', u'Beat Swing', u'Delay Mode', u'Feedback', u'Dry/Wet')
PPG_BANKS = (PPG_BANK1,)
PPG_BOBS = (PPG_BANK1,)
RDX_BANK1 = (u'Bit Depth', u'Sample Mode', u'Sample Hard', u'Sample Soft', u'Bit On', u'', u'', u'')
RDX_BANKS = (RDX_BANK1,)
RDX_BOBS = (RDX_BANK1,)
RSN_BANK1 = (u'Frequency', u'Width', u'Global Gain', u'Dry/Wet', u'Decay', u'I Note', u'Color', u'I Gain')
RSN_BANK2 = (u'II Gain', u'III Gain', u'IV Gain', u'V Gain', u'II Pitch', u'III Pitch', u'IV Pitch', u'V Pitch')
RSN_BOB = (u'Decay', u'I Note', u'II Pitch', u'III Pitch', u'IV Pitch', u'V Pitch', u'Global Gain', u'Dry/Wet')
RSN_BANKS = (RSN_BANK1, RSN_BANK2)
RSN_BOBS = (RSN_BOB,)
RSN_BNK_NAMES = (u'General / Mode I', u'Modes II-IV')
RVB_BANK1 = (u'In Filter Freq', u'In Filter Width', u'PreDelay', u'ER Spin On', u'ER Spin Rate', u'ER Spin Amount', u'ER Shape', u'DecayTime')
RVB_BANK2 = (u'HiShelf Freq', u'LowShelf Freq', u'Chorus Rate', u'Density', u'HiShelf Gain', u'LowShelf Gain', u'Chorus Amount', u'Scale')
RVB_BANK3 = (u'DecayTime', u'Freeze On', u'Room Size', u'Stereo Image', u'ER Level', u'Diffuse Level', u'Dry/Wet', u'Quality')
RVB_BOB = (u'DecayTime', u'Room Size', u'PreDelay', u'In Filter Freq', u'ER Level', u'Diffuse Level', u'Stereo Image', u'Dry/Wet')
RVB_BANKS = (RVB_BANK1, RVB_BANK2, RVB_BANK3)
RVB_BOBS = (RVB_BOB,)
RVB_BNK_NAMES = (u'Reflections', u'Diffusion Network', u'Global')
SAT_BANK1 = (u'Drive', u'Base', u'Frequency', u'Width', u'Depth', u'Output', u'Dry/Wet', u'Type')
SAT_BANK2 = (u'WS Drive', u'WS Lin', u'WS Curve', u'WS Damp', u'WS Depth', u'WS Period', u'Dry/Wet', u'')
SAT_BOB = (u'Drive', u'Type', u'Base', u'Frequency', u'Width', u'Depth', u'Output', u'Dry/Wet')
SAT_BANKS = (SAT_BANK1, SAT_BANK2)
SAT_BOBS = (SAT_BOB,)
SAT_BNK_NAMES = (u'General Controls', u'Waveshaper Controls')
SMD_BANK1 = (u'L Beat Delay', u'L Beat Swing', u'L Time Delay', u'R Beat Delay', u'R Beat Swing', u'R Time Delay', u'Feedback', u'Dry/Wet')
SMD_BANKS = (SMD_BANK1,)
SMD_BOBS = (SMD_BANK1,)
UTL_BANK1 = (u'Left Inv', u'Right Inv', u'Channel Mode', u'Stereo Width', u'Mono', u'Balance', u'Gain', u'Mute')
UTL_BANK2 = (u'Bass Mono', u'Bass Freq', u'DC Filter', u'', u'', u'', u'', u'')
UTL_BANKS = (UTL_BANK1, UTL_BANK2)
UTL_BOBS = (UTL_BANK1,)
UTL_BNK_NAMES = (u'General Controls', u'Low Frequency')
VDS_BANK1 = (u'Tracing Freq.', u'Tracing Width', u'Tracing Drive', u'Crackle Density', u'Pinch Freq.', u'Pinch Width', u'Pinch Drive', u'Crackle Volume')
VDS_BANKS = (VDS_BANK1,)
VDS_BOBS = (VDS_BANK1,)
VOC_BANK1 = (u'Formant Shift', u'Attack Time', u'Release Time', u'Mono/Stereo', u'Output Level', u'Gate Threshold', u'Envelope Depth', u'Dry/Wet')
VOC_BANK2 = (u'Filter Bandwidth', u'Upper Filter Band', u'Lower Filter Band', u'Precise/Retro', u'Unvoiced Level', u'Unvoiced Sensitivity', u'Unvoiced Speed', u'Enhance')
VOC_BANK3 = (u'Noise Rate', u'Noise Crackle', u'Upper Pitch Detection', u'Lower Pitch Detection', u'Oscillator Pitch', u'Oscillator Waveform', u'Ext. In Gain', u'')
VOC_BOB = (u'Formant Shift', u'Attack Time', u'Release Time', u'Unvoiced Level', u'Gate Threshold', u'Filter Bandwidth', u'Envelope Depth', u'Dry/Wet')
VOC_BANKS = (VOC_BANK1, VOC_BANK2, VOC_BANK3)
VOC_BOBS = (VOC_BOB,)
VOC_BNK_NAMES = (u'Global', u'Filters/Voicing', u'Carrier')
DEVICE_DICT = {u'AudioEffectGroupDevice': RCK_BANKS,
 u'MidiEffectGroupDevice': RCK_BANKS,
 u'InstrumentGroupDevice': RCK_BANKS,
 u'DrumGroupDevice': RCK_BANKS,
 u'InstrumentImpulse': IMP_BANKS,
 u'Operator': OPR_BANKS,
 u'UltraAnalog': ALG_BANKS,
 u'OriginalSimpler': SIM_BANKS,
 u'MultiSampler': SAM_BANKS,
 u'MidiArpeggiator': ARP_BANKS,
 u'LoungeLizard': ELC_BANKS,
 u'StringStudio': TNS_BANKS,
 u'Collision': COL_BANKS,
 u'MidiChord': CRD_BANKS,
 u'MidiNoteLength': NTL_BANKS,
 u'MidiPitcher': PIT_BANKS,
 u'MidiRandom': RND_BANKS,
 u'MidiScale': SCL_BANKS,
 u'MidiVelocity': VEL_BANKS,
 u'AutoFilter': AFL_BANKS,
 u'AutoPan': APN_BANKS,
 u'BeatRepeat': BRP_BANKS,
 u'Chorus': CHR_BANKS,
 u'Compressor2': CP3_BANKS,
 u'Corpus': CRP_BANKS,
 u'Eq8': EQ8_BANKS,
 u'FilterEQ3': EQ3_BANKS,
 u'Erosion': ERO_BANKS,
 u'FilterDelay': FLD_BANKS,
 u'Flanger': FLG_BANKS,
 u'FrequencyShifter': FRS_BANKS,
 u'GrainDelay': GRD_BANKS,
 u'Looper': LPR_BANKS,
 u'MultibandDynamics': MBD_BANKS,
 u'Overdrive': OVR_BANKS,
 u'Phaser': PHS_BANKS,
 u'Redux': RDX_BANKS,
 u'Saturator': SAT_BANKS,
 u'Resonator': RSN_BANKS,
 u'StereoGain': UTL_BANKS,
 u'Tube': DTB_BANKS,
 u'Reverb': RVB_BANKS,
 u'Vinyl': VDS_BANKS,
 u'Gate': GTE_BANKS,
 u'Vocoder': VOC_BANKS,
 u'Amp': AMP_BANKS,
 u'Cabinet': CAB_BANKS,
 u'GlueCompressor': GLU_BANKS,
 u'Pedal': PDL_BANKS,
 u'DrumBuss': DRB_BANKS,
 u'Echo': ECH_BANKS,
 u'InstrumentVector': WVT_BANKS}
DEVICE_BOB_DICT = {u'AudioEffectGroupDevice': RCK_BOBS,
 u'MidiEffectGroupDevice': RCK_BOBS,
 u'InstrumentGroupDevice': RCK_BOBS,
 u'DrumGroupDevice': RCK_BOBS,
 u'InstrumentImpulse': IMP_BOBS,
 u'Operator': OPR_BOBS,
 u'UltraAnalog': ALG_BOBS,
 u'OriginalSimpler': SIM_BOBS,
 u'MultiSampler': SAM_BOBS,
 u'MidiArpeggiator': ARP_BOBS,
 u'LoungeLizard': ELC_BOBS,
 u'StringStudio': TNS_BOBS,
 u'Collision': COL_BOBS,
 u'MidiChord': CRD_BOBS,
 u'MidiNoteLength': NTL_BOBS,
 u'MidiPitcher': PIT_BOBS,
 u'MidiRandom': RND_BOBS,
 u'MidiScale': SCL_BOBS,
 u'MidiVelocity': VEL_BOBS,
 u'AutoFilter': AFL_BOBS,
 u'AutoPan': APN_BOBS,
 u'BeatRepeat': BRP_BOBS,
 u'Chorus': CHR_BOBS,
 u'Compressor2': CP3_BOBS,
 u'Corpus': CRP_BOBS,
 u'Eq8': EQ8_BOBS,
 u'FilterEQ3': EQ3_BOBS,
 u'Erosion': ERO_BOBS,
 u'FilterDelay': FLD_BOBS,
 u'Flanger': FLG_BOBS,
 u'FrequencyShifter': FRS_BOBS,
 u'GrainDelay': GRD_BOBS,
 u'Looper': LPR_BOBS,
 u'MultibandDynamics': MBD_BOBS,
 u'Overdrive': OVR_BOBS,
 u'Phaser': PHS_BOBS,
 u'Redux': RDX_BOBS,
 u'Saturator': SAT_BOBS,
 u'Resonator': RSN_BOBS,
 u'StereoGain': UTL_BOBS,
 u'Tube': DTB_BOBS,
 u'Reverb': RVB_BOBS,
 u'Vinyl': VDS_BOBS,
 u'Gate': GTE_BOBS,
 u'Vocoder': VOC_BOBS,
 u'Amp': AMP_BOBS,
 u'Cabinet': CAB_BOBS,
 u'GlueCompressor': GLU_BOBS,
 u'Pedal': PDL_BOBS,
 u'DrumBuss': DRB_BOBS,
 u'Echo': ECH_BOBS,
 u'InstrumentVector': WVT_BOBS}
BANK_NAME_DICT = {u'AudioEffectGroupDevice': RCK_BNK_NAMES,
 u'MidiEffectGroupDevice': RCK_BNK_NAMES,
 u'InstrumentGroupDevice': RCK_BNK_NAMES,
 u'DrumGroupDevice': RCK_BNK_NAMES,
 u'InstrumentImpulse': IMP_BNK_NAMES,
 u'Operator': OPR_BNK_NAMES,
 u'UltraAnalog': ALG_BNK_NAMES,
 u'OriginalSimpler': SIM_BNK_NAMES,
 u'MultiSampler': SAM_BNK_NAMES,
 u'MidiArpeggiator': ARP_BNK_NAMES,
 u'LoungeLizard': ELC_BNK_NAMES,
 u'StringStudio': TNS_BNK_NAMES,
 u'Collision': COL_BNK_NAMES,
 u'MidiChord': CRD_BNK_NAMES,
 u'BeatRepeat': BRP_BNK_NAMES,
 u'Compressor2': CP3_BNK_NAMES,
 u'Corpus': CRP_BNK_NAMES,
 u'Eq8': EQ8_BNK_NAMES,
 u'FilterDelay': FLD_BNK_NAMES,
 u'Flanger': FLG_BNK_NAMES,
 u'Gate': GTE_BNK_NAMES,
 u'MultibandDynamics': MBD_BNK_NAMES,
 u'Phaser': PHS_BNK_NAMES,
 u'Saturator': SAT_BNK_NAMES,
 u'Resonator': RSN_BNK_NAMES,
 u'Reverb': RVB_BNK_NAMES,
 u'Vocoder': VOC_BNK_NAMES,
 u'Amp': AMP_BNK_NAMES,
 u'GlueCompressor': GLU_BNK_NAMES,
 u'AutoFilter': AFL_BNK_NAMES,
 u'StereoGain': UTL_BNK_NAMES,
 u'DrumBuss': DRB_BANK_NAMES,
 u'Echo': ECH_BANK_NAMES,
 u'Pedal': PDL_BANK_NAMES,
 u'InstrumentVector': WVT_BANK_NAMES}
MAX_DEVICES = (u'MxDeviceInstrument', u'MxDeviceAudioEffect', u'MxDeviceMidiEffect')

def device_parameters_to_map(device):
    return tuple(device.parameters[1:])


def parameter_bank_names(device, bank_name_dict = BANK_NAME_DICT):
    u""" Determine the bank names to use for a device """
    if device != None:
        if device.class_name in list(bank_name_dict.keys()):
            return bank_name_dict[device.class_name]
        banks = number_of_parameter_banks(device)

        def _default_bank_name(bank_index):
            return u'Bank ' + str(bank_index + 1)

        if device.class_name in MAX_DEVICES and banks != 0:

            def _is_ascii(c):
                return ord(c) < 128

            def _bank_name(bank_index):
                try:
                    name = device.get_bank_name(bank_index)
                except:
                    name = None

                if name:
                    return u''.join(filter(_is_ascii, name))
                else:
                    return _default_bank_name(bank_index)

            return list(map(_bank_name, list(range(0, banks))))
        else:
            return list(map(_default_bank_name, list(range(0, banks))))
    return []


def parameter_banks(device, device_dict = DEVICE_DICT):
    u""" Determine the parameters to use for a device """
    if device != None:
        if device.class_name in list(device_dict.keys()):

            def names_to_params(bank):
                return list(map(partial(get_parameter_by_name, device), bank))

            return list(map(names_to_params, device_dict[device.class_name]))
        else:
            if device.class_name in MAX_DEVICES:
                try:
                    banks = device.get_bank_count()
                except:
                    banks = 0

                if banks != 0:

                    def _bank_parameters(bank_index):
                        try:
                            parameter_indices = device.get_bank_parameters(bank_index)
                        except:
                            parameter_indices = []

                        if len(parameter_indices) != 8:
                            return [ None for i in range(0, 8) ]
                        else:
                            return [ (device.parameters[i] if i != -1 else None) for i in parameter_indices ]

                    return list(map(_bank_parameters, list(range(0, banks))))
            return group(device_parameters_to_map(device), 8)
    return []


def best_of_parameter_bank(device, device_bob_dict = DEVICE_BOB_DICT):
    if device and device.class_name in device_bob_dict:
        bobs = device_bob_dict[device.class_name]
        assert len(bobs) == 1
        return list(map(partial(get_parameter_by_name, device), bobs[0]))
    if device.class_name in MAX_DEVICES:
        try:
            parameter_indices = device.get_bank_parameters(-1)
            return [ (device.parameters[i] if i != -1 else None) for i in parameter_indices ]
        except:
            return []

    return device.parameters[1:9]


def number_of_parameter_banks(device, device_dict = DEVICE_DICT):
    u""" Determine the amount of parameter banks the given device has """
    if device != None:
        if device.class_name in list(device_dict.keys()):
            device_bank = device_dict[device.class_name]
            return len(device_bank)
        else:
            if device.class_name in MAX_DEVICES:
                try:
                    banks = device.get_bank_count()
                except:
                    banks = 0

                if banks != 0:
                    return banks
            param_count = len(device.parameters[1:])
            return old_div(param_count, 8) + (1 if param_count % 8 else 0)
    return 0


def get_parameter_by_name(device, name):
    u""" Find the given device's parameter that belongs to the given name """
    for i in device.parameters:
        if i.original_name == name:
            return i
