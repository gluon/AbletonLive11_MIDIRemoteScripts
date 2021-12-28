#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/Capabilities.py
from __future__ import absolute_import, print_function, unicode_literals
from past.builtins import basestring
GENERIC_SCRIPT_KEY = u'generic_script'
PORTS_KEY = u'ports'
CONTROLLER_ID_KEY = u'controller_id'
TYPE_KEY = u'surface_type'
FIRMWARE_KEY = u'firmware_version'
AUTO_LOAD_KEY = u'auto_load'
VENDORID = u'vendor_id'
PRODUCTIDS = u'product_ids'
MODEL_NAMES = u'model_names'
DIRECTIONKEY = u'direction'
PORTNAMEKEY = u'name'
MACNAMEKEY = u'mac_name'
PROPSKEY = u'props'
HIDDEN = u'hidden'
SYNC = u'sync'
SCRIPT = u'script'
NOTES_CC = u'notes_cc'
REMOTE = u'remote'
PLAIN_OLD_MIDI = u'plain_old_midi'

def __create_port_dict(direction, port_name, mac_name, props):
    assert isinstance(direction, basestring)
    assert isinstance(port_name, basestring)
    assert props == None or type(props) is list
    if props:
        for prop in props:
            assert isinstance(prop, basestring)

    assert mac_name == None or isinstance(mac_name, basestring)
    capabilities = {DIRECTIONKEY: direction,
     PORTNAMEKEY: port_name,
     PROPSKEY: props}
    if mac_name:
        capabilities[MACNAMEKEY] = mac_name
    return capabilities


def inport(port_name = u'', props = [], mac_name = None):
    u""" Generate a ..."""
    return __create_port_dict(u'in', port_name, mac_name, props)


def outport(port_name = u'', props = [], mac_name = None):
    u""" Generate a ..."""
    return __create_port_dict(u'out', port_name, mac_name, props)


def controller_id(vendor_id, product_ids, model_name):
    u""" Generate a hardwareId dict"""
    assert type(vendor_id) is int
    assert type(product_ids) is list
    for product_id in product_ids:
        assert type(product_id) is int

    assert isinstance(model_name, (basestring, list))
    if isinstance(model_name, basestring):
        model_names = [model_name]
    else:
        model_names = model_name
    return {VENDORID: vendor_id,
     PRODUCTIDS: product_ids,
     MODEL_NAMES: model_names}
