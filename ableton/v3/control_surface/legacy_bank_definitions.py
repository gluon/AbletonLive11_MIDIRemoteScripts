# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\legacy_bank_definitions.py
# Compiled at: 2022-12-08 12:23:09
# Size of source mod 2**32: 2008 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Generic.Devices import BANK_NAME_DICT, DEVICE_BOB_DICT, DEVICE_DICT
from ableton.v2.base.collection import IndexedDict
from ..base import memoize
from . import BANK_PARAMETERS_KEY
BEST_OF_PARAMETERS_KEY = 'Best of Parameters'

@memoize
def banked():
    return {device_name: IndexedDict([(bank_name, {BANK_PARAMETERS_KEY: parameters}) for bank_name, parameters in zip(bank_names, DEVICE_DICT[device_name])]) for device_name, bank_names in BANK_NAME_DICT.items()}


@memoize
def best_of_banks():
    return {device_name: IndexedDict([(BEST_OF_PARAMETERS_KEY, {BANK_PARAMETERS_KEY: parameters[0]})]) for device_name, parameters in DEVICE_BOB_DICT.items()}