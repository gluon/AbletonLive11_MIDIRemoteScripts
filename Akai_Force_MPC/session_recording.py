from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionRecordingComponent as SessionRecordingComponentBase
from ableton.v2.control_surface.control import ToggleButtonControl

class SessionRecordingComponent(SessionRecordingComponentBase):
    mpc_automation_toggle = ToggleButtonControl(toggled_color='Automation.On',
      untoggled_color='Automation.Off')

    def _on_session_automation_record_changed(self):
        super(SessionRecordingComponent, self)._on_session_automation_record_changed()
        self.mpc_automation_toggle.is_toggled = self.song.session_automation_record

    @mpc_automation_toggle.toggled
    def mpc_automation_toggle(self, is_toggled, _):
        self.song.session_automation_record = is_toggled