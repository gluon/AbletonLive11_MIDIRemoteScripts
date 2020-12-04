#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/real_time_channel.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Component
from ableton.v2.base import depends, listenable_property, liveobj_changed, liveobj_valid

def update_real_time_attachments(real_time_data_components):
    u"""
    Updates all the real-time channels. We need to explicitly detach all
    channels before attaching them again, otherwise we could end up in a situation
    where we try to attach to a channel that's already occupied.
    """
    for d in real_time_data_components:
        d.detach()

    for d in real_time_data_components:
        d.attach()


class RealTimeDataComponent(Component):
    __events__ = (u'attached',)

    @depends(real_time_mapper=None, register_real_time_data=None)
    def __init__(self, real_time_mapper = None, register_real_time_data = None, channel_type = None, *a, **k):
        assert channel_type is not None
        assert liveobj_valid(real_time_mapper)
        super(RealTimeDataComponent, self).__init__(*a, **k)
        self._channel_type = channel_type
        self._real_time_channel_id = u''
        self._object_id = u''
        self._real_time_mapper = real_time_mapper
        self._data = None
        self._valid = True
        register_real_time_data(self)

    def disconnect(self):
        super(RealTimeDataComponent, self).disconnect()
        self._data = None

    @listenable_property
    def channel_id(self):
        return self._real_time_channel_id

    @listenable_property
    def object_id(self):
        return self._object_id

    @property
    def attached_object(self):
        return self._data

    def on_enabled_changed(self):
        super(RealTimeDataComponent, self).on_enabled_changed()
        self.invalidate()
        self._update_attachment()

    def _update_attachment(self):
        self.detach()
        self.attach()

    def set_data(self, data):
        if liveobj_changed(data, self._data):
            self._data = data
            self.invalidate()

    def invalidate(self):
        self._valid = False

    def detach(self):
        if not self._valid and self._real_time_channel_id != u'':
            self._real_time_mapper.detach_channel(self._real_time_channel_id)
            self._real_time_channel_id = u''

    def device_visualisation(self):
        return self._real_time_mapper.device_visualisation

    def attach(self):
        if not self._valid:
            data = self._data if self.is_enabled() else None
            if data != None:
                self._real_time_channel_id, self._object_id = self._real_time_mapper.attach_object(data, self._channel_type)
            self.notify_channel_id()
            self.notify_object_id()
            self._valid = True
            self.notify_attached()
