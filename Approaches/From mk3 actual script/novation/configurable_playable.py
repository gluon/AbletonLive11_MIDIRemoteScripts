#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/configurable_playable.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import PlayableComponent

class ConfigurablePlayableComponent(PlayableComponent):

    def __init__(self, translation_channel, *a, **k):
        self._translation_channel = translation_channel
        super(ConfigurablePlayableComponent, self).__init__(*a, **k)

    def _note_translation_for_button(self, button):
        return (button.identifier, self._translation_channel)
