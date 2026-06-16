# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\tension.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 3302 bytes
from __future__ import absolute_import, print_function, unicode_literals
from enum import IntEnum
from ableton.v2.base import EventObject, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name

class TensionDeviceDecorator(LiveObjectDecorator, EventObject):

    class SectionSelect(IntEnum):
        exc = 0
        str = 1
        damp = 2
        term = 3
        body = 4

    class VibSelect(IntEnum):
        vib = 0
        uni = 1

    class ModSrcSelect(IntEnum):
        key = 0
        vel = 1
        pb = 2
        press = 3
        slide = 4

    class KeyTargetSelect(IntEnum):
        exc = 0
        damp = 1
        term = 2

    class VelTargetSelect(IntEnum):
        exc = 0
        term = 1
        env = 2

    def __init__(self, *a, **k):
        (super(TensionDeviceDecorator, self).__init__)(*a, **k)
        self._add_enum_parameter(name='Section',
          values=[
         'Exciter','String','Damper','Termination','Body'],
          default_value=(self.SectionSelect.exc))
        self._add_enum_parameter(name='Vib & Uni',
          values=['Vib', 'Uni'],
          default_value=(self.VibSelect.vib))
        self._add_enum_parameter(name='Mod Source',
          values=[
         'Key','Vel','PB','Press','Slide'],
          default_value=(self.ModSrcSelect.key))
        self._add_enum_parameter(name='Key Dest',
          values=[
         'Exciter', 'Damper', 'Term/String'],
          default_value=(self.KeyTargetSelect.exc))
        self._add_enum_parameter(name='Vel Dest',
          values=[
         'Exciter', 'Term/Damp', 'Env'],
          default_value=(self.VelTargetSelect.exc))
        self._add_switch_option(name='LFO Sync On',
          pname='LFO Sync On',
          labels=['Hertz', 'Beat'])
        self._add_switch_option(name='Key Priority',
          pname='Key Priority',
          labels=['High', 'Low', 'Last'])
        self._add_on_off_option(name='Exciter', pname='Exc On/Off')
        self._add_on_off_option(name='Fixed Exc', pname='E Pos Abs')
        self._add_on_off_option(name='Pickup', pname='Pickup On/Off')
        self._add_on_off_option(name='Damper', pname='Damper On')
        self._add_on_off_option(name='Gated', pname='Damper Gated')
        self._add_on_off_option(name='Fixed Damp', pname='D Pos Abs')
        self._add_on_off_option(name='Termination', pname='Term On/Off')
        self._add_on_off_option(name='Body', pname='Body On/Off')
        self._add_on_off_option(name='Filter', pname='Filter On/Off')
        self._add_on_off_option(name='Filt Env', pname='FEG On/Off')
        self._add_on_off_option(name='LFO', pname='LFO On/Off')
        self._add_on_off_option(name='Vibrato', pname='Vibrato On/Off')
        self._add_on_off_option(name='Unison', pname='Unison On/Off')
        self._add_on_off_option(name='Portamento', pname='Porta On/Off')
        self._add_on_off_option(name='Legato', pname='Porta Legato')
        self._add_on_off_option(name='Proportional', pname='Porta Prop')
        self.register_disconnectables(self.options)