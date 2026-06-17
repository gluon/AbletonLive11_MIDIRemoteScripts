# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\__init__.py
# Compiled at: 2023-09-13 04:24:51
# Size of source mod 2**32: 4296 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import BANK_FORMAT, BANK_MAIN_KEY, BANK_PARAMETERS_KEY, MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, MIDI_SYSEX_TYPE, CompoundElement, ControlElement, DeviceBankRegistry, DeviceProvider, EnumWrappingParameter, InputControlElement, NotifyingControlElement, NotifyingList, ParameterProvider, PrioritizedResource, RelativeInternalParameter, SharedResource, all_parameters, find_instrument_devices, find_instrument_meeting_requirement, use
from ableton.v2.control_surface.default_bank_definitions import BANK_DEFINITIONS as V2_BANK_DEFINITIONS
from ableton.v2.control_surface.defaults import DOUBLE_CLICK_DELAY
from ableton.v2.control_surface.elements.encoder import ABSOLUTE_MAP_MODES
from ableton.v2.control_surface.input_control_element import ScriptForwarding
from . import midi
from .banking_util import DEFAULT_BANK_SIZE, BankingInfo, create_parameter_bank
from .colors import STANDARD_COLOR_PALETTE, STANDARD_FALLBACK_COLOR_TABLE, BasicColors
from .component import Component
from .consts import ACTIVE_PARAMETER_TIMEOUT, DEFAULT_PRIORITY, HIGH_PRIORITY, LOW_PRIORITY, M4L_PRIORITY, MOMENTARY_DELAY
from .control_surface import ControlSurface, create_control_surface
from .control_surface_specification import ControlSurfaceSpecification
from .default_bank_definitions import BANK_DEFINITIONS
from .default_skin import create_skin, default_skin
from .elements_base import ElementsBase, MapMode, create_button, create_combo_element, create_encoder, create_matrix_identifiers, create_sysex_element, create_sysex_sending_button
from .identification import IdentificationComponent
from .instrument_finder import InstrumentFinderComponent
from .layer import Layer
from .parameter_info import ParameterInfo
from .parameter_mapping_sensitivities import DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY, FINE_GRAIN_SENSITIVITY_FACTOR, parameter_mapping_sensitivities
from .session_ring_selection_linking import SessionRingSelectionLinking
from .skin import LiveObjSkinEntry, OptionalSkinEntry, Skin, merge_skins
__all__ = ('ABSOLUTE_MAP_MODES', 'ACTIVE_PARAMETER_TIMEOUT', 'BANK_DEFINITIONS', 'BANK_FORMAT',
           'BANK_MAIN_KEY', 'BANK_PARAMETERS_KEY', 'DEFAULT_BANK_SIZE', 'DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY',
           'DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY', 'DEFAULT_PRIORITY', 'DOUBLE_CLICK_DELAY',
           'FINE_GRAIN_SENSITIVITY_FACTOR', 'HIGH_PRIORITY', 'LOW_PRIORITY', 'M4L_PRIORITY',
           'MIDI_CC_TYPE', 'MIDI_NOTE_TYPE', 'MIDI_PB_TYPE', 'MIDI_SYSEX_TYPE', 'MOMENTARY_DELAY',
           'STANDARD_COLOR_PALETTE', 'STANDARD_FALLBACK_COLOR_TABLE', 'V2_BANK_DEFINITIONS',
           'BankingInfo', 'BasicColors', 'Component', 'CompoundElement', 'ControlElement',
           'ControlSurface', 'ControlSurfaceSpecification', 'DeviceBankRegistry',
           'DeviceProvider', 'ElementsBase', 'EnumWrappingParameter', 'IdentificationComponent',
           'InputControlElement', 'InstrumentFinderComponent', 'Layer', 'LiveObjSkinEntry',
           'MapMode', 'NotifyingControlElement', 'NotifyingList', 'OptionalSkinEntry',
           'ParameterInfo', 'ParameterProvider', 'PrioritizedResource', 'RelativeInternalParameter',
           'ScriptForwarding', 'SessionRingSelectionLinking', 'SharedResource', 'Skin',
           'all_parameters', 'create_button', 'create_combo_element', 'create_control_surface',
           'create_encoder', 'create_matrix_identifiers', 'create_parameter_bank',
           'create_skin', 'create_sysex_element', 'create_sysex_sending_button',
           'default_skin', 'find_instrument_devices', 'find_instrument_meeting_requirement',
           'merge_skins', 'midi', 'parameter_mapping_sensitivities', 'use')