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