# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_mkII\__init__.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 921 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .keylab_mkii import KeyLabMkII

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=7285,
                          product_ids=[
                         587, 651, 715],
                          model_name=[
                         'KeyLab mkII 49', 'KeyLab mkII 61', 'KeyLab mkII 88']), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, REMOTE]),
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[]),
                 outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return KeyLabMkII(c_instance=c_instance)