#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/ModeSelectorComponent.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from .ButtonElement import ButtonElement
from .ControlSurfaceComponent import ControlSurfaceComponent
from .MomentaryModeObserver import MomentaryModeObserver

class ModeSelectorComponent(ControlSurfaceComponent):
    u""" Class for switching between modes, handle several functions with few controls """

    def __init__(self, *a, **k):
        super(ModeSelectorComponent, self).__init__(*a, **k)
        self._modes_buttons = []
        self._mode_toggle = None
        self._mode_listeners = []
        self.__mode_index = -1
        self._modes_observers = {}
        self._modes_heap = []

    def _get_protected_mode_index(self):
        return self.__mode_index

    def _set_protected_mode_index(self, mode):
        assert isinstance(mode, int)
        self.__mode_index = mode
        for listener in self._mode_listeners:
            listener()

    _mode_index = property(_get_protected_mode_index, _set_protected_mode_index)

    def _get_public_mode_index(self):
        return self.__mode_index

    def _set_public_mode_index(self, mode):
        assert False

    mode_index = property(_get_public_mode_index, _set_public_mode_index)

    def disconnect(self):
        self._clean_heap()
        if self._mode_toggle != None:
            self._mode_toggle.remove_value_listener(self._toggle_value)
            self._mode_toggle = None
        self._modes_buttons = None
        self._mode_listeners = None
        super(ModeSelectorComponent, self).disconnect()

    def on_enabled_changed(self):
        self.update()

    def set_mode_toggle(self, button):
        assert button == None or isinstance(button, ButtonElement)
        if self._mode_toggle != None:
            self._mode_toggle.remove_value_listener(self._toggle_value)
        self._mode_toggle = button
        if self._mode_toggle != None:
            self._mode_toggle.add_value_listener(self._toggle_value)
        self.set_mode(0)

    def set_mode_buttons(self, buttons):
        assert buttons != None
        assert isinstance(buttons, tuple)
        assert len(buttons) - 1 in range(16)
        for button in buttons:
            assert isinstance(button, ButtonElement)
            identify_sender = True
            button.add_value_listener(self._mode_value, identify_sender)
            self._modes_buttons.append(button)

        self.set_mode(0)

    def set_mode(self, mode):
        self._clean_heap()
        self._modes_heap = [(mode, None, None)]
        if self._mode_index != mode:
            self._update_mode()

    def _update_mode(self):
        mode = self._modes_heap[-1][0]
        assert mode in range(self.number_of_modes())
        if self._mode_index != mode:
            self._mode_index = mode
            self.update()

    def _clean_heap(self):
        for _, _, observer in self._modes_heap:
            if observer != None:
                observer.disconnect()

        self._modes_heap = []

    def number_of_modes(self):
        raise NotImplementedError

    def mode_index_has_listener(self, listener):
        return listener in self._mode_listeners

    def add_mode_index_listener(self, listener):
        assert listener not in self._mode_listeners
        self._mode_listeners.append(listener)

    def remove_mode_index_listener(self, listener):
        assert listener in self._mode_listeners
        self._mode_listeners.remove(listener)

    def _mode_value(self, value, sender):
        assert len(self._modes_buttons) > 0
        assert isinstance(value, int)
        assert sender in self._modes_buttons
        new_mode = self._modes_buttons.index(sender)
        if sender.is_momentary():
            if value > 0:
                mode_observer = MomentaryModeObserver()
                mode_observer.set_mode_details(new_mode, self._controls_for_mode(new_mode), self._get_public_mode_index)
                self._modes_heap.append((new_mode, sender, mode_observer))
                self._update_mode()
            elif self._modes_heap[-1][1] == sender and not self._modes_heap[-1][2].is_mode_momentary():
                self.set_mode(new_mode)
            else:
                for mode, button, observer in self._modes_heap:
                    if button == sender:
                        self._modes_heap.remove((mode, button, observer))
                        break

                self._update_mode()
        else:
            self.set_mode(new_mode)

    def _toggle_value(self, value):
        assert self._mode_toggle != None
        assert isinstance(value, int)
        if value is not 0 or not self._mode_toggle.is_momentary():
            self.set_mode((self._mode_index + 1) % self.number_of_modes())

    def _controls_for_mode(self, mode):
        return None

    def _on_timer(self):
        for _, _, mode_observer in self._modes_heap:
            if mode_observer != None:
                mode_observer.on_timer()
