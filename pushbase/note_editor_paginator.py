# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/note_editor_paginator.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 2310 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from ableton.v2.base import forward_property, listens, listens_group
from ableton.v2.control_surface import Component
from .loop_selector_component import Paginator

class NoteEditorPaginator(Component, Paginator):

    def __init__(self, note_editors=None, *a, **k):
        (super(NoteEditorPaginator, self).__init__)(*a, **k)
        self._note_editors = note_editors
        self._last_page_index = -1
        self._on_page_length_changed.subject = self._reference_editor
        self._on_active_steps_changed.replace_subjects(note_editors)

    @property
    def _reference_editor(self):
        return self._note_editors[0]

    page_index = forward_property('_reference_editor')('page_index')
    page_length = forward_property('_reference_editor')('page_length')

    def update(self):
        super(NoteEditorPaginator, self).update()
        if self.is_enabled():
            self.notify_page_index()
            self.notify_page()
            self.notify_page_length()

    def _update_from_page_index(self):
        needed_update = self._last_page_index != self.page_index
        if needed_update:
            self._last_page_index = self.page_index
            if self.is_enabled():
                self.notify_page_index()
        return needed_update

    @listens_group('active_steps')
    def _on_active_steps_changed(self, editor):
        if self.is_enabled():
            self.notify_page()

    @listens('page_length')
    def _on_page_length_changed(self):
        if self.is_enabled():
            self.notify_page()
            self.notify_page_length()
            self._update_from_page_index()

    @property
    def can_change_page(self):
        return all([e.can_change_page for e in self._note_editors])

    def select_page_in_point(self, value):
        can_change_page = self.can_change_page
        if can_change_page:
            list(map(lambda e: e.set_selected_page_point(value), self._note_editors))
            if self._update_from_page_index():
                if self.is_enabled():
                    self.notify_page()
        return can_change_page