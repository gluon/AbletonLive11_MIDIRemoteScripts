<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchkey_MK3/__init__.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 1030 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from .launchkey_mk3 import Launchkey_MK3

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661,
                          product_ids=[
<<<<<<< HEAD
                         308,309,310,311,320],
=======
                         308, 309, 310, 311],
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
                          model_name=[
                         'Launchkey MK3 25',
                         'Launchkey MK3 37',
                         'Launchkey MK3 49',
<<<<<<< HEAD
                         'Launchkey MK3 61',
                         'Launchkey MK3 88']), 
=======
                         'Launchkey MK3 61']), 
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, REMOTE]),
                 inport(props=[NOTES_CC, SCRIPT]),
                 outport(props=[SYNC, REMOTE]),
                 outport(props=[NOTES_CC, SCRIPT])]}


def create_instance(c_instance):
    return Launchkey_MK3(c_instance=c_instance)