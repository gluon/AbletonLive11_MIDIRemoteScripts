<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import find_if, listens, liveobj_valid
from ableton.v2.control_surface.control import ButtonControl
from KeyLab_Essential.view_control import ViewControlComponent as ViewControlComponentBase
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/KeyLab_mkII/view_control.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 1225 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import find_if, listens, liveobj_valid
from ableton.v2.control_surface.control import ButtonControl
import KeyLab_Essential.view_control as ViewControlComponentBase
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
MAIN_VIEWS = ('Session', 'Arranger')

class ViewControlComponent(ViewControlComponentBase):
    document_view_toggle_button = ButtonControl()

    def __init__(self, *a, **k):
        (super(ViewControlComponent, self).__init__)(*a, **k)
        self._ViewControlComponent__on_focused_document_view_changed.subject = self.application.view
        self._ViewControlComponent__on_focused_document_view_changed()

    @document_view_toggle_button.pressed
    def document_view_toggle_button(self, _):
        is_session_visible = self.application.view.is_view_visible('Session',
          main_window_only=True)
        self.show_view('Arranger' if is_session_visible else 'Session')

    @listens('focused_document_view')
    def __on_focused_document_view_changed(self):
        self.document_view_toggle_button.color = 'View.{}'.format(self.application.view.focused_document_view)