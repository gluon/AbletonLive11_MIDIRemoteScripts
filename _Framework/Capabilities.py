# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\Capabilities.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 2757 bytes
from __future__ import absolute_import, print_function, unicode_literals
from past.builtins import basestring
GENERIC_SCRIPT_KEY = 'generic_script'
PORTS_KEY = 'ports'
CONTROLLER_ID_KEY = 'controller_id'
TYPE_KEY = 'surface_type'
FIRMWARE_KEY = 'firmware_version'
AUTO_LOAD_KEY = 'auto_load'
VENDORID = 'vendor_id'
PRODUCTIDS = 'product_ids'
MODEL_NAMES = 'model_names'
DIRECTIONKEY = 'direction'
PORTNAMEKEY = 'name'
MACNAMEKEY = 'mac_name'
PROPSKEY = 'props'
HIDDEN = 'hidden'
SYNC = 'sync'
SCRIPT = 'script'
NOTES_CC = 'notes_cc'
REMOTE = 'remote'
PLAIN_OLD_MIDI = 'plain_old_midi'

def __create_port_dict(direction, port_name, mac_name, props):
    if props:
        for prop in props:
            pass

    capabilities = {DIRECTIONKEY: direction, PORTNAMEKEY: port_name, PROPSKEY: props}
    if mac_name:
        capabilities[MACNAMEKEY] = mac_name
    return capabilities


def inport(port_name='', props=[], mac_name=None):
    return __create_port_dict('in', port_name, mac_name, props)


def outport(port_name='', props=[], mac_name=None):
    return __create_port_dict('out', port_name, mac_name, props)


def controller_id(vendor_id, product_ids, model_name):
    for product_id in product_ids:
        pass

    if isinstance(model_name, basestring):
        model_names = [
         model_name]
    else:
        model_names = model_name
    return {VENDORID: vendor_id, PRODUCTIDS: product_ids, MODEL_NAMES: model_names}