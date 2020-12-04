#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Akai_Force_MPC/device_navigation.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import index_if, listens, liveobj_valid
from ableton.v2.control_surface.components import DeviceNavigationComponent, FlattenedDeviceChain
from ableton.v2.control_surface.control import ButtonControl, SendValueControl, TextDisplayControl

def get_item(item_with_nesting_level):
    return item_with_nesting_level[0]


class ScrollableDeviceChain(FlattenedDeviceChain):

    def __init__(self, *a, **k):
        super(ScrollableDeviceChain, self).__init__(*a, **k)
        self._selected_index = None
        self.__on_selected_item_changed.subject = self
        self.__on_selected_item_changed()

    @property
    def selected_index(self):
        return self._selected_index

    def can_scroll_left(self):
        return self._can_scroll_selection() and self.selected_index > 0

    def can_scroll_right(self):
        return self._can_scroll_selection() and self.selected_index < len(self.items) - 1

    def scroll_left(self):
        if self.can_scroll_left():
            self.selected_item = get_item(self.items[self.selected_index - 1])

    def scroll_right(self):
        if self.can_scroll_right():
            self.selected_item = get_item(self.items[self.selected_index + 1])

    def _can_scroll_selection(self):
        return not self.has_invalid_selection and self.selected_index is not None

    def _update_devices(self, *_):
        self._devices = self._collect_devices(self._device_parent)
        self._update_selected_item_index()
        self._update_listeners()
        self.notify_items()

    @listens(u'selected_item')
    def __on_selected_item_changed(self):
        self._update_selected_item_index()

    def _update_selected_item_index(self):
        new_index = None
        if not self.has_invalid_selection:
            items = self.items
            index = index_if(lambda i: get_item(i) == self.selected_item, items)
            if index < len(items):
                new_index = index
        self._selected_index = new_index


class ScrollingDeviceNavigationComponent(DeviceNavigationComponent):
    prev_device_button = ButtonControl(color=u'Action.Off', pressed_color=u'Action.On')
    next_device_button = ButtonControl(color=u'Action.Off', pressed_color=u'Action.On')
    num_devices_control = SendValueControl()
    device_index_control = SendValueControl()
    device_name_display = TextDisplayControl()

    def __init__(self, *a, **k):
        super(ScrollingDeviceNavigationComponent, self).__init__(item_provider=ScrollableDeviceChain(), *a, **k)

    @prev_device_button.pressed
    def prev_device_button(self, value):
        self.item_provider.scroll_left()

    @next_device_button.pressed
    def next_device_button(self, value):
        self.item_provider.scroll_right()

    def _on_selection_changed(self):
        selected_item = self.item_provider.selected_item
        self._select_item(selected_item)
        self._update_device_index_control()

    def _on_items_changed(self):
        self.num_devices_control.value = len(self.item_provider.items)
        self._update_device_index_control()

    def _update_device(self):
        device = self._device_component.device()
        live_device = getattr(device, u'proxied_object', device)
        self._update_item_provider(live_device if liveobj_valid(live_device) else None)
        self.__on_appointed_device_name_changed.subject = device
        self.__on_appointed_device_name_changed()

    @listens(u'name')
    def __on_appointed_device_name_changed(self):
        self._update_device_name_display()

    def _update_device_index_control(self):
        selected_index = self.item_provider.selected_index
        if selected_index is not None:
            self.device_index_control.value = selected_index

    def _update_device_name_display(self):
        device = self._device_component.device()
        self.device_name_display[0] = device.name if liveobj_valid(device) else u'No Device'
