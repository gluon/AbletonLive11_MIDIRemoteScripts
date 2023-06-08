from __future__ import absolute_import, print_function, unicode_literals
from weakref import ref
import Live
from ableton.v2.base import listenable_property, nop
from ableton.v2.control_surface import Component, ControlElement
from pushbase.message_box_component import Notification, strip_restriction_markup_and_format
from model.repr import strip_formatted_string

class NotificationComponent(Component):

    def __init__(self, default_notification_time=2.5, *a, **k):
        (super(NotificationComponent, self).__init__)(*a, **k)
        self._visible = False
        self._message = ''
        self.show_notification = self._show_notification
        self._notification_timer = None
        self._default_notification_time = default_notification_time
        self._dummy_control_element = ControlElement()
        self._dummy_control_element.reset = nop

    def disconnect(self):
        self.hide_notification()
        self.show_notification = nop
        super(NotificationComponent, self).disconnect()

    @listenable_property
    def visible(self):
        return self._visible

    @listenable_property
    def message(self):
        return self._message

    def _show_notification(self, text, blink_text=None, notification_time=None):
        text = strip_restriction_markup_and_format(text)
        self._message = strip_formatted_string(text)
        if notification_time is None:
            notification_time = self._default_notification_time
        if self._notification_timer:
            self._notification_timer.stop()
        if notification_time != -1:
            component_ref = ref(self)

            def timer_callback():
                if component_ref():
                    component_ref().hide_notification()

            self._notification_timer = Live.Base.Timer(callback=timer_callback,
              interval=(int(1000 * notification_time)),
              repeat=False)
            self._notification_timer.start()
        if not self._visible:
            self._visible = True
            self.notify_visible()
        self.notify_message()
        self._current_notification = Notification(self)
        return ref(self._current_notification)

    def hide_notification(self):
        if self._notification_timer:
            self._notification_timer.stop()
            self._notification_timer = None
        if self._visible:
            self._visible = False
            self.notify_visible()

    def use_single_line(self, *a):
        return self._dummy_control_element

    def use_full_display(self, *a):
        return self._dummy_control_element