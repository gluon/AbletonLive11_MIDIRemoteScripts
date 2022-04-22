# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/ModeSelectorComponent.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 5408 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from .ButtonElement import ButtonElement
from .ControlSurfaceComponent import ControlSurfaceComponent
from .MomentaryModeObserver import MomentaryModeObserver

class ModeSelectorComponent(ControlSurfaceComponent):

    def __init__(self, *a, **k):
        (super(ModeSelectorComponent, self).__init__)(*a, **k)
        self._modes_buttons = []
        self._mode_toggle = None
        self._mode_listeners = []
        self._ModeSelectorComponent__mode_index = -1
        self._modes_observers = {}
        self._modes_heap = []

    def _get_protected_mode_index(self):
        return self._ModeSelectorComponent__mode_index

    def _set_protected_mode_index(self, mode):
        self._ModeSelectorComponent__mode_index = mode
        for listener in self._mode_listeners:
            listener()

    _mode_index = property(_get_protected_mode_index, _set_protected_mode_index)

    def _get_public_mode_index(self):
        return self._ModeSelectorComponent__mode_index

    def _set_public_mode_index(self, mode):
        pass

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
        if self._mode_toggle != None:
            self._mode_toggle.remove_value_listener(self._toggle_value)
        self._mode_toggle = button
        if self._mode_toggle != None:
            self._mode_toggle.add_value_listener(self._toggle_value)
        self.set_mode(0)

    def set_mode_buttons(self, buttons):
        for button in buttons:
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
        mode = self._modes_heap[(-1)][0]
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
        self._mode_listeners.append(listener)

    def remove_mode_index_listener(self, listener):
        self._mode_listeners.remove(listener)

    def _mode_value(self, value, sender):
        new_mode = self._modes_buttons.index(sender)
        if sender.is_momentary():
            if value > 0:
                mode_observer = MomentaryModeObserver()
                mode_observer.set_mode_details(new_mode, self._controls_for_mode(new_mode), self._get_public_mode_index)
                self._modes_heap.append((new_mode, sender, mode_observer))
                self._update_mode()
            elif self._modes_heap[(-1)][1] == sender and not self._modes_heap[(-1)][2].is_mode_momentary():
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
        if not (value is not 0 or self._mode_toggle.is_momentary()):
            self.set_mode((self._mode_index + 1) % self.number_of_modes())

    def _controls_for_mode(self, mode):
        pass

    def _on_timer(self):
        for _, _, mode_observer in self._modes_heap:
            if mode_observer != None:
                mode_observer.on_timer()