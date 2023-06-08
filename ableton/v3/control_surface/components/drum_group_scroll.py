from __future__ import absolute_import, print_function, unicode_literals
from ...base import liveobj_valid
from .page import Pageable, PageComponent
MAX_DRUM_GROUP_SCROLL_POSITION = 28

class DrumGroupScrollComponent(PageComponent, Pageable):
    position_count = 32
    page_length = 4
    page_offset = 1

    def __init__(self, *a, **k):
        self._drum_group_device = None
        (super().__init__)(a, scroll_skin_name='DrumGroup.Scroll', **k)

    def set_scroll_encoder(self, encoder):
        self._position_scroll.set_scroll_encoder(encoder)

    def set_drum_group_device(self, drum_group_device):
        self._drum_group_device = drum_group_device
        self.update()

    @property
    def position(self):
        if liveobj_valid(self._drum_group_device):
            return self._drum_group_device.view.drum_pads_scroll_position
        return 0

    @position.setter
    def position(self, index):
        if liveobj_valid(self._drum_group_device):
            self._drum_group_device.view.drum_pads_scroll_position = index

    def can_scroll_page_up(self):
        if not liveobj_valid(self._drum_group_device):
            return False
        return super().can_scroll_page_up()