<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/view_toggle.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 2592 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from ...base import MultiSlot
from .. import Component
from ..controls import ToggleButtonControl

class ViewToggleComponent(Component):
<<<<<<< HEAD
    main_view_toggle_button = ToggleButtonControl(color='ViewToggle.SessionOff',
      on_color='ViewToggle.SessionOn')
    detail_view_toggle_button = ToggleButtonControl(color='ViewToggle.DetailOff',
      on_color='ViewToggle.DetailOn')
    clip_view_toggle_button = ToggleButtonControl(color='ViewToggle.ClipOff',
      on_color='ViewToggle.ClipOn')
    browser_view_toggle_button = ToggleButtonControl(color='ViewToggle.BrowserOff',
      on_color='ViewToggle.BrowserOn')
=======
    main_view_toggle_button = ToggleButtonControl(untoggled_color='ViewToggle.SessionOff',
      toggled_color='ViewToggle.SessionOn')
    detail_view_toggle_button = ToggleButtonControl(untoggled_color='ViewToggle.DetailOff',
      toggled_color='ViewToggle.DetailOn')
    clip_view_toggle_button = ToggleButtonControl(untoggled_color='ViewToggle.ClipOff',
      toggled_color='ViewToggle.ClipOn')
    browser_view_toggle_button = ToggleButtonControl(untoggled_color='ViewToggle.BrowserOff',
      toggled_color='ViewToggle.BrowserOn')
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def __init__(self, name='View_Toggle', *a, **k):
        (super().__init__)(a, name=name, **k)
        for view_name in ('Session', 'Detail', 'Detail/Clip', 'Browser'):
            self.register_slot(MultiSlot(subject=(self.application.view),
              listener=(self._ViewToggleComponent__update_view_toggle_buttons),
              event_name_list=('is_view_visible', ),
              extra_args=(
             view_name,)))

        self._ViewToggleComponent__update_view_toggle_buttons()

    @main_view_toggle_button.toggled
    def main_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Session')

    @detail_view_toggle_button.toggled
    def detail_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Detail')

    @clip_view_toggle_button.toggled
    def clip_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Detail/Clip')

    @browser_view_toggle_button.toggled
    def browser_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, 'Browser')

    def _show_or_hide_view(self, show_view, view_name):
        if show_view:
            self.application.view.show_view(view_name)
        else:
            self.application.view.hide_view(view_name)

    def __update_view_toggle_buttons(self):
        view = self.application.view
<<<<<<< HEAD
        self.main_view_toggle_button.is_on = view.is_view_visible('Session')
        self.detail_view_toggle_button.is_on = view.is_view_visible('Detail')
        self.clip_view_toggle_button.is_on = view.is_view_visible('Detail/Clip')
        self.browser_view_toggle_button.is_on = view.is_view_visible('Browser')
=======
        self.main_view_toggle_button.is_toggled = view.is_view_visible('Session')
        self.detail_view_toggle_button.is_toggled = view.is_view_visible('Detail')
        self.clip_view_toggle_button.is_toggled = view.is_view_visible('Detail/Clip')
        self.browser_view_toggle_button.is_toggled = view.is_view_visible('Browser')
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
