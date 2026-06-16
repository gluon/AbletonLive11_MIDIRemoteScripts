# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\clipboard.py
# Compiled at: 2023-09-22 14:37:57
# Size of source mod 2**32: 3170 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import listenable_property
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.control_surface.display import Renderable

class ClipboardComponent(Component, Renderable):
    copy_button = ButtonControl(color='Clipboard.Empty', on_color='Clipboard.Filled')
    has_content = listenable_property.managed(False)

    def __init__(self, name='Clipboard', *a, **k):
        (super().__init__)(a, name=name, **k)
        self._source_obj = None
        self._did_paste = False
        self._pending_clear = False

    def set_copy_button(self, button):
        self.clear()
        self.copy_button.set_control_element(button)

    def copy_or_paste(self, obj):
        if self.has_content:
            if self._is_source_valid():
                self._did_paste = self._do_paste(obj)
                if self._did_paste:
                    self.copy_button.is_pressed or self.clear()
            else:
                self.clear(notify=True)
        else:
            self._source_obj = self._do_copy(obj)
            self.update()

    def clear(self, notify=False):
        self._source_obj = None
        self._pending_clear = False
        self.update()
        if notify:
            self.notify(self.notifications.Clipboard.clear)

    @copy_button.pressed
    def copy_button(self, _):
        self._pending_clear = self.has_content

    @copy_button.released
    def copy_button(self, _):
        if self._did_paste or self._pending_clear:
            self.clear(notify=True)

    def update(self):
        super().update()
        self._did_paste = False
        self.has_content = self._source_obj is not None
        self.copy_button.is_on = self.has_content

    def _do_copy(self, obj):
        self._source_obj = obj
        return self._source_obj

    def _do_paste(self, obj):
        self._did_paste = obj is not None
        return self._did_paste

    def _is_source_valid(self):
        return self._source_obj is not None