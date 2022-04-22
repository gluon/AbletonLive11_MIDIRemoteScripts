# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/__init__.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 1246 bytes
from __future__ import absolute_import, print_function, unicode_literals

def get_capabilities():
    import ableton.v2.control_surface as caps
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=10626,
                               product_ids=[6503],
                               model_name='Ableton Push 2'), 
     
     caps.PORTS_KEY: [
                      caps.inport(props=[caps.HIDDEN, caps.NOTES_CC, caps.SCRIPT]),
                      caps.inport(props=[]),
                      caps.outport(props=[caps.HIDDEN, caps.NOTES_CC, caps.SYNC, caps.SCRIPT]),
                      caps.outport(props=[])], 
     
     caps.TYPE_KEY: 'push2', 
     caps.AUTO_LOAD_KEY: True}


def create_instance(c_instance):
    from .push2 import Push2
    from .push2_model import Root, Sender
    root = Root(sender=Sender(message_sink=(c_instance.send_model_update),
      process_connected=(c_instance.process_connected)))
    return Push2(c_instance=c_instance,
      model=root,
      decoupled_parameter_list_change_notifications=True)