# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/settings.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 689 bytes
from __future__ import absolute_import, print_function, unicode_literals
from pushbase.setting import OnOffSetting

def create_settings(preferences=None):
    preferences = preferences if preferences is not None else {}
    return {'workflow':OnOffSetting(name='Workflow',
       value_labels=[
      'Scene', 'Clip'],
       default_value=True,
       preferences=preferences), 
     'aftertouch_mode':OnOffSetting(name='Pressure',
       value_labels=[
      'Mono', 'Polyphonic'],
       default_value=True,
       preferences=preferences)}