# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\settings.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3804 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range, str
from past.utils import old_div
from collections import OrderedDict
from pushbase.setting import EnumerableSetting, OnOffSetting
from .pad_sensitivity import PadParameters
MIN_OFF_THRESHOLD = 10
MAX_OFF_THRESHOLD = 370
MIN_ON_THRESHOLD = 10
MAX_ON_THRESHOLD = 410
CRITICAL_THRESHOLD_LIMIT = 0
MIN_THRESHOLD_STEP = -20
MAX_THRESHOLD_STEP = 20
INSTRUMENT_AFTERTOUCH_THRESHOLD = 80

def make_pad_parameters(curve_value, threshold_value):
    threshold_range = MAX_THRESHOLD_STEP - MIN_THRESHOLD_STEP
    t = old_div(float(threshold_value - MIN_THRESHOLD_STEP), float(threshold_range))
    return PadParameters(curve_value,
      on_threshold=(int((1 - t) * MIN_ON_THRESHOLD + t * MAX_ON_THRESHOLD)),
      off_threshold=(int((1 - t) * MIN_OFF_THRESHOLD + t * MAX_OFF_THRESHOLD)))


action_pad_sensitivity = PadParameters(off_threshold=190,
  on_threshold=210,
  gain=85000,
  curve1=120000,
  curve2=60000)

def _create_pad_settings():
    return [
     PadParameters(gain=100000, curve1=45000, curve2=0, name='Linear'),
     PadParameters(gain=85000, curve1=120000, curve2=60000, name='Log 1 (Default)'),
     PadParameters(gain=85000, curve1=120000, curve2=50000, name='Log 2'),
     PadParameters(gain=100000, curve1=120000, curve2=50000, name='Log 3'),
     PadParameters(gain=130000, curve1=120000, curve2=50000, name='Log 4'),
     PadParameters(gain=140000, curve1=120000, curve2=0, name='Log 5')]


def _threshold_formatter(value):
    if value != 0:
        return str(value)
    return '0 (Default)'


def create_settings(preferences=None):
    preferences = preferences if preferences is not None else {}
    pad_settings = _create_pad_settings()
    return OrderedDict([
     (
      'threshold',
      EnumerableSetting(name='Pad Threshold',
        values=(list(range(MIN_THRESHOLD_STEP, MAX_THRESHOLD_STEP + 1))),
        default_value=0,
        preferences=preferences,
        value_formatter=_threshold_formatter)),
     (
      'curve',
      EnumerableSetting(name='Velocity Curve',
        values=pad_settings,
        default_value=(pad_settings[1]),
        preferences=preferences)),
     (
      'workflow',
      OnOffSetting(name='Workflow',
        value_labels=[
       'Scene', 'Clip'],
        default_value=True,
        preferences=preferences)),
     (
      'aftertouch_mode',
      OnOffSetting(name='Pressure',
        value_labels=[
       'Mono', 'Polyphonic'],
        default_value=True,
        preferences=preferences)),
     (
      'aftertouch_threshold',
      EnumerableSetting(name='Threshold',
        values=(list(range(128))),
        default_value=INSTRUMENT_AFTERTOUCH_THRESHOLD,
        preferences=preferences))])