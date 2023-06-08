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