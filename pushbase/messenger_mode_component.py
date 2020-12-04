#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/messenger_mode_component.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import BooleanContext
from ableton.v2.control_surface.mode import ModesComponent
from .message_box_component import Messenger

class MessengerModesComponent(ModesComponent, Messenger):
    notify_when_enabled = False

    def __init__(self, muted = False, *a, **k):
        super(MessengerModesComponent, self).__init__(*a, **k)
        self._mode_message_map = {}
        self._default_and_alternative_mode_map = {}
        self._is_being_enabled = BooleanContext()
        self._muted = muted

    def add_mode(self, name, mode_or_component, message = None, default_mode = None, alternative_mode = None, **k):
        super(MessengerModesComponent, self).add_mode(name, mode_or_component, **k)
        self._mode_message_map[name] = message
        self._default_and_alternative_mode_map[name] = (default_mode, alternative_mode)

    def get_mode_message(self):
        message = self._mode_message_map.get(self.selected_mode, u'')
        return message

    def get_default_mode_and_alternative_mode(self):
        default_mode, alternative_mode = self._default_and_alternative_mode_map.get(self.selected_mode, u'')
        return (default_mode, alternative_mode)

    def on_enabled_changed(self):
        with self._is_being_enabled():
            super(MessengerModesComponent, self).on_enabled_changed()

    def _do_enter_mode(self, name):
        super(MessengerModesComponent, self)._do_enter_mode(name)
        if (not self._is_being_enabled or self.notify_when_enabled) and not self._muted:
            message = self._mode_message_map.get(name, None)
            if message:
                self.show_notification(message)

    @property
    def muted(self):
        return self._muted

    @muted.setter
    def muted(self, muted):
        self._muted = muted
