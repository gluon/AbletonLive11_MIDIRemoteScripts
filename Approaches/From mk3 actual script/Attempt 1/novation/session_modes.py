#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/session_modes.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import lazy_attribute, task
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface.mode import ModesComponent

class QuickDoubleClickButton(ButtonControl):

    class State(ButtonControl.State):

        @lazy_attribute
        def _double_click_task(self):
            return self.tasks.add(task.wait(0.3))


class SessionModesComponent(ModesComponent):
    cycle_mode_button = QuickDoubleClickButton()
    mode_button_color_control = ButtonControl()

    def __init__(self, *a, **k):
        super(SessionModesComponent, self).__init__(*a, **k)
        self._last_selected_main_mode = u'launch'

    def revert_to_main_mode(self):
        self.selected_mode = self._last_selected_main_mode

    @cycle_mode_button.pressed
    def cycle_mode_button(self, _):
        if self._last_selected_main_mode and self.selected_mode == u'overview':
            self.selected_mode = self._last_selected_main_mode
        elif len(self._mode_list) > 2:
            self.selected_mode = u'mixer' if self.selected_mode == u'launch' else u'launch'

    @cycle_mode_button.double_clicked
    def cycle_mode_button(self, _):
        self.selected_mode = u'overview'

    def _do_enter_mode(self, name):
        super(SessionModesComponent, self)._do_enter_mode(name)
        if self.selected_mode != u'overview':
            self._last_selected_main_mode = self.selected_mode

    def _update_cycle_mode_button(self, selected):
        if selected == u'overview':
            self.mode_button_color_control.color = u'Mode.Session.Overview'
        else:
            self.mode_button_color_control.color = u'Mode.Session.Mixer' if selected == u'mixer' else u'Mode.Session.Launch'
