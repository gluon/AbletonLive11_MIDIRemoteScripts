#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/KeyLab_mkII/view_control.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import find_if, listens, liveobj_valid
from ableton.v2.control_surface.control import ButtonControl
from KeyLab_Essential.view_control import ViewControlComponent as ViewControlComponentBase
MAIN_VIEWS = (u'Session', u'Arranger')

class ViewControlComponent(ViewControlComponentBase):
    document_view_toggle_button = ButtonControl()

    def __init__(self, *a, **k):
        super(ViewControlComponent, self).__init__(*a, **k)
        self.__on_focused_document_view_changed.subject = self.application.view
        self.__on_focused_document_view_changed()

    @document_view_toggle_button.pressed
    def document_view_toggle_button(self, _):
        is_session_visible = self.application.view.is_view_visible(u'Session', main_window_only=True)
        self.show_view(u'Arranger' if is_session_visible else u'Session')

    @listens(u'focused_document_view')
    def __on_focused_document_view_changed(self):
        self.document_view_toggle_button.color = u'View.{}'.format(self.application.view.focused_document_view)
