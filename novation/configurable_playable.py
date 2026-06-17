# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\configurable_playable.py
# Compiled at: 2022-11-28 08:01:32
# Size of source mod 2**32: 569 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import PlayableComponent

class ConfigurablePlayableComponent(PlayableComponent):

    def __init__(self, translation_channel, *a, **k):
        self._translation_channel = translation_channel
        (super(ConfigurablePlayableComponent, self).__init__)(*a, **k)

    def _note_translation_for_button(self, button):
        return (
         button.identifier, self._translation_channel)