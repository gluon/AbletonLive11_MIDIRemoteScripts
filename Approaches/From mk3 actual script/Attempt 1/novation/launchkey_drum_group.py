#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/launchkey_drum_group.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface.components import PlayableComponent
from .drum_group import DrumGroupComponent as DrumGroupComponentBase
from .util import get_midi_color_value_for_track

class DrumGroupComponent(DrumGroupComponentBase):

    def __init__(self, *a, **k):
        super(DrumGroupComponent, self).__init__(*a, **k)
        self._track = None
        self._track_color = 0

    def set_parent_track(self, track):
        self._track = track
        self.__on_track_color_changed.subject = track if liveobj_valid(track) else None
        self.__on_track_color_changed()

    def set_drum_group_device(self, drum_group_device):
        super(DrumGroupComponent, self).set_drum_group_device(drum_group_device)
        if not liveobj_valid(self._drum_group_device):
            self._update_assigned_drum_pads()
            self._update_led_feedback()

    def can_scroll_page_up(self):
        u""" Extends standard to return False when no drum rack is present so that
        the related scroll button will be disabled.  This is not needed in the case
        of can_scroll_page_down since that will already return False when no drum
        rack is present. """
        if not liveobj_valid(self._drum_group_device):
            return False
        return super(DrumGroupComponent, self).can_scroll_page_up()

    def _update_led_feedback(self):
        PlayableComponent._update_led_feedback(self)

    def _update_button_color(self, button):
        pad = self._pad_for_button(button)
        color = self._color_for_pad(pad) if pad else self._track_color
        if color in (u'DrumGroup.PadFilled', u'DrumGroup.PadEmpty') and liveobj_valid(self._track):
            color = self._track_color
        button.color = color

    @listens(u'color')
    def __on_track_color_changed(self):
        self._track_color = get_midi_color_value_for_track(self._track)
        self._update_led_feedback()
