# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\settings.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 713 bytes
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