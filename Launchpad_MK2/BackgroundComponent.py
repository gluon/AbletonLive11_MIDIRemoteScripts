# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_MK2\BackgroundComponent.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 1018 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.BackgroundComponent import BackgroundComponent as BackgroundComponentBase

class BackgroundComponent(BackgroundComponentBase):

    def _clear_control(self, name, control):
        if control:
            control.add_value_listener(self._on_value_listener)
        super(BackgroundComponent, self)._clear_control(name, control)

    def _on_value_listener(self, *a, **k):
        pass


class TranslatingBackgroundComponent(BackgroundComponent):

    def __init__(self, translation_channel=0, *a, **k):
        (super(TranslatingBackgroundComponent, self).__init__)(*a, **k)
        self._translation_channel = translation_channel

    def _clear_control(self, name, control):
        if control:
            control.set_channel(self._translation_channel)
        super(TranslatingBackgroundComponent, self)._clear_control(name, control)