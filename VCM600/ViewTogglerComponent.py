<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/VCM600/ViewTogglerComponent.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 8466 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import Live
import _Framework.ButtonElement as ButtonElement
import _Framework.ControlSurfaceComponent as ControlSurfaceComponent

class ViewTogglerComponent(ControlSurfaceComponent):

    def __init__(self, num_tracks):
        ControlSurfaceComponent.__init__(self)
        self._num_tracks = num_tracks
        self._chain_buttons = None
        self._clip_buttons = None
        self._ignore_track_selection = False
        self.application().view.add_is_view_visible_listener('Detail', self._on_detail_view_changed)
        self.application().view.add_is_view_visible_listener('Detail/Clip', self._on_views_changed)

    def disconnect(self):
        self.application().view.remove_is_view_visible_listener('Detail', self._on_detail_view_changed)
        self.application().view.remove_is_view_visible_listener('Detail/Clip', self._on_views_changed)
        if self._chain_buttons != None:
            for button in self._chain_buttons:
                button.remove_value_listener(self._chain_value)

            self._chain_buttons = None
        if self._clip_buttons != None:
            for button in self._clip_buttons:
                button.remove_value_listener(self._clip_value)

            self._clip_buttons = None

    def set_buttons(self, chain_buttons, clip_buttons):
        if self._chain_buttons != None:
            for button in self._chain_buttons:
                button.remove_value_listener(self._chain_value)

        self._chain_buttons = chain_buttons
        if self._chain_buttons != None:
            for button in self._chain_buttons:
                button.add_value_listener((self._chain_value), identify_sender=True)

        if self._clip_buttons != None:
            for button in self._clip_buttons:
                button.remove_value_listener(self._clip_value)

        self._clip_buttons = clip_buttons
        if self._clip_buttons != None:
            for button in self._clip_buttons:
                button.add_value_listener((self._clip_value), identify_sender=True)

        self.on_selected_track_changed()

    def on_selected_track_changed(self):
        self._update_buttons()

    def on_enabled_changed(self):
        self.update()

    def update(self):
        super(ViewTogglerComponent, self).update()
        if self.is_enabled():
            self._update_buttons()
        else:
            if self._chain_buttons != None:
                for button in self._chain_buttons:
                    button.turn_off()

            if self._clip_buttons != None:
                for button in self._clip_buttons:
                    button.turn_off()

    def _on_detail_view_changed(self):
        self._update_buttons()

    def _on_views_changed(self):
        self._update_buttons()

    def _update_buttons(self):
        tracks = self.song().visible_tracks
        for index in range(self._num_tracks):
            if len(tracks) > index:
                if tracks[index] == self.song().view.selected_track and self.application().view.is_view_visible('Detail'):
                    if self.application().view.is_view_visible('Detail/DeviceChain'):
                        self._chain_buttons[index].turn_on()
                    else:
                        self._chain_buttons[index].turn_off()
                    if self.application().view.is_view_visible('Detail/Clip'):
                        self._clip_buttons[index].turn_on()
                    else:
                        self._clip_buttons[index].turn_off()
                else:
                    if self._chain_buttons != None:
                        self._chain_buttons[index].turn_off()
                    if self._clip_buttons != None:
                        self._clip_buttons[index].turn_off()

    def _chain_value(self, value, sender):
        tracks = self.song().visible_tracks
        if not sender.is_momentary() or value != 0:
            index = list(self._chain_buttons).index(sender)
            self._ignore_track_selection = True
            if len(tracks) > index:
                if self.song().view.selected_track != tracks[index]:
                    self.song().view.selected_track = tracks[index]
                    if not (self.application().view.is_view_visible('Detail') and self.application().view.is_view_visible('Detail/DeviceChain')):
                        self.application().view.show_view('Detail')
                        self.application().view.show_view('Detail/DeviceChain')
<<<<<<< HEAD
                else:
                    if self.application().view.is_view_visible('Detail/DeviceChain') and self.application().view.is_view_visible('Detail'):
                        self.application().view.hide_view('Detail')
                    else:
                        self.application().view.show_view('Detail')
                        self.application().view.show_view('Detail/DeviceChain')
=======
                elif self.application().view.is_view_visible('Detail/DeviceChain') and self.application().view.is_view_visible('Detail'):
                    self.application().view.hide_view('Detail')
                else:
                    self.application().view.show_view('Detail')
                    self.application().view.show_view('Detail/DeviceChain')
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
            self._ignore_track_selection = False

    def _clip_value(self, value, sender):
        tracks = self.song().visible_tracks
        if not sender.is_momentary() or value != 0:
            index = list(self._clip_buttons).index(sender)
            self._ignore_track_selection = True
            if len(tracks) > index:
                if self.song().view.selected_track != tracks[index]:
                    self.song().view.selected_track = tracks[index]
                    if not (self.application().view.is_view_visible('Detail') and self.application().view.is_view_visible('Detail/Clip')):
                        self.application().view.show_view('Detail')
                        self.application().view.show_view('Detail/Clip')
<<<<<<< HEAD
                else:
                    if self.application().view.is_view_visible('Detail/Clip') and self.application().view.is_view_visible('Detail'):
                        self.application().view.hide_view('Detail')
                    else:
                        self.application().view.show_view('Detail')
                        self.application().view.show_view('Detail/Clip')
=======
                elif self.application().view.is_view_visible('Detail/Clip') and self.application().view.is_view_visible('Detail'):
                    self.application().view.hide_view('Detail')
                else:
                    self.application().view.show_view('Detail')
                    self.application().view.show_view('Detail/Clip')
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
            self._ignore_track_selection = False