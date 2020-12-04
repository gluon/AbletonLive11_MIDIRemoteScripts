#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/loop_selector_component.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from builtins import map
from builtins import range
from past.utils import old_div
from contextlib import contextmanager
from functools import partial
from ableton.v2.base import EventObject, clamp, listenable_property, listens, liveobj_changed, liveobj_valid, nop, task
from ableton.v2.control_surface import defaults, Component
from ableton.v2.control_surface.control import ButtonControl, control_matrix, PlayableControl
from .step_duplicator import NullStepDuplicator, set_loop
from .consts import MessageBoxText
from .message_box_component import Messenger
from .pad_control import PadControl

def create_clip_in_selected_slot(creator, song, clip_length = None):
    u"""
    Create a new clip in the selected slot of if none exists, using a
    given creator object.  Fires it if the song is playing and
    displays it in the detail view.
    """
    selected_slot = song.view.highlighted_clip_slot
    if creator and selected_slot and not selected_slot.has_clip:
        creator.create(selected_slot, clip_length, legato_launch=True)
        song.view.detail_clip = selected_slot.clip
    return selected_slot.clip


def clip_is_new_recording(clip):
    return clip.is_recording and not clip.is_overdubbing


class Paginator(EventObject):
    u"""
    Paginator interface for objects that split continuous time into
    discrete pages.  This can be used as trivial paginator splits time
    into one single infinite-length page.
    """
    __events__ = (u'page', u'page_index', u'page_length')

    @property
    def can_change_page(self):
        return True

    @property
    def page_length(self):
        u"""
        Length of a given page.
        """
        return 2147483648.0

    @property
    def page_index(self):
        u"""
        Index of the currently selected page.
        """
        return 0

    def select_page_in_point(self, value):
        u"""
        Select the page that falls in the given time point. Returns True if page was
        selected.
        """
        return True


class LoopSelectorComponent(Component, Messenger):
    u"""
    Component that uses a button matrix to display the timeline of a
    clip. It allows you to select the loop of the clip and a page
    within it of a given Paginator object.
    """
    next_page_button = ButtonControl()
    prev_page_button = ButtonControl()
    delete_button = ButtonControl()
    select_button = ButtonControl()
    loop_selector_matrix = control_matrix(PadControl, sensitivity_profile=u'loop', mode=PlayableControl.Mode.listenable)
    short_loop_selector_matrix = control_matrix(ButtonControl)
    is_following = listenable_property.managed(False)

    def __init__(self, clip_creator = None, measure_length = 4.0, follow_detail_clip = False, paginator = None, default_size = None, *a, **k):
        super(LoopSelectorComponent, self).__init__(*a, **k)
        assert default_size is not None
        self._clip_creator = clip_creator
        self._sequencer_clip = None
        self._paginator = Paginator()
        self._loop_start = 0
        self._loop_end = 0
        self._loop_length = 0
        self._default_size = default_size
        self._pressed_pages = []
        self._page_colors = []
        self._measure_length = measure_length
        self._last_playhead_page = -1

        def set_is_following_true():
            self.is_following = True

        self._follow_task = self._tasks.add(task.sequence(task.wait(defaults.MOMENTARY_DELAY), task.run(set_is_following_true)))
        self._follow_task.kill()
        self.set_step_duplicator(None)
        self._notification_reference = partial(nop, None)
        self.is_deleting = False
        if follow_detail_clip:
            self._on_detail_clip_changed.subject = self.song.view
            self._on_detail_clip_changed()
        self._on_session_record_changed.subject = self.song
        self._on_song_playback_status_changed.subject = self.song
        if paginator is not None:
            self.set_paginator(paginator)

    def set_paginator(self, paginator):
        self._paginator = paginator or Paginator()
        self._on_page_index_changed.subject = paginator
        self._on_page_length_changed.subject = paginator
        self._update_page_colors()

    @listens(u'page_index')
    def _on_page_index_changed(self):
        self._update_page_colors()

    @listens(u'page_length')
    def _on_page_length_changed(self):
        self._update_page_colors()
        self._select_start_page()

    def set_step_duplicator(self, duplicator):
        self._step_duplicator = duplicator or NullStepDuplicator()
        self._step_duplicator.set_clip(self._sequencer_clip)

    @listens(u'detail_clip')
    def _on_detail_clip_changed(self):
        self.set_detail_clip(self.song.view.detail_clip)

    def set_detail_clip(self, clip):
        if liveobj_changed(clip, self._sequencer_clip):
            self.is_following = liveobj_valid(clip) and (self.is_following or clip_is_new_recording(clip))
            self._on_playing_position_changed.subject = clip
            self._on_playing_status_changed.subject = clip
            self._on_loop_start_changed.subject = clip
            self._on_loop_end_changed.subject = clip
            self._on_is_recording_changed.subject = clip
            self._sequencer_clip = clip
            self._step_duplicator.set_clip(clip)
            self._on_loop_changed()

    def _select_start_page(self):
        if liveobj_valid(self._sequencer_clip):
            page_start = self._paginator.page_index * self._paginator.page_length
            to_select = page_start
            if page_start <= self._sequencer_clip.loop_start:
                to_select = self._sequencer_clip.loop_start
            elif page_start >= self._sequencer_clip.loop_end:
                to_select = max(self._sequencer_clip.loop_end - self._paginator.page_length, self._sequencer_clip.loop_start)
            self._paginator.select_page_in_point(to_select)

    @listens(u'loop_start')
    def _on_loop_start_changed(self):
        self._on_loop_changed()

    @listens(u'loop_end')
    def _on_loop_end_changed(self):
        self._on_loop_changed()

    def _on_loop_changed(self):
        if liveobj_valid(self._sequencer_clip):
            self._loop_start = self._sequencer_clip.loop_start
            self._loop_end = self._sequencer_clip.loop_end
            self._loop_length = self._loop_end - self._loop_start
        else:
            self._loop_start = 0
            self._loop_end = 0
            self._loop_length = 0
        self._select_start_page()
        self._update_page_colors()

    def set_loop_selector_matrix(self, matrix):
        self.loop_selector_matrix.set_control_element(matrix)
        self._update_page_colors()

    def set_short_loop_selector_matrix(self, matrix):
        self.short_loop_selector_matrix.set_control_element(matrix)
        self._update_page_colors()

    def update(self):
        super(LoopSelectorComponent, self).update()
        self._update_page_and_playhead_leds()

    @listens(u'is_recording')
    def _on_is_recording_changed(self):
        self.is_following = self.is_following or clip_is_new_recording(self._sequencer_clip)

    @listens(u'playing_position')
    def _on_playing_position_changed(self):
        self._update_page_and_playhead_leds()
        self._update_page_selection()

    @listens(u'playing_status')
    def _on_playing_status_changed(self):
        self._update_page_and_playhead_leds()

    @listens(u'session_record')
    def _on_session_record_changed(self):
        self._update_page_and_playhead_leds()

    @listens(u'is_playing')
    def _on_song_playback_status_changed(self):
        self._update_page_and_playhead_leds()

    def _has_running_clip(self):
        return liveobj_valid(self._sequencer_clip) and (self._sequencer_clip.is_playing or self._sequencer_clip.is_recording)

    def _update_page_selection(self):
        if self.is_enabled() and self.is_following and self._has_running_clip():
            position = self._sequencer_clip.playing_position
            self._paginator.select_page_in_point(position)

    def _update_page_and_playhead_leds(self):

        @contextmanager
        def save_page_color(page_colors, page):
            old_page_value = page_colors[page]
            yield
            page_colors[page] = old_page_value

        @contextmanager
        def replace_and_restore_tail_colors(page_colors, page):
            if clip_is_new_recording(self._sequencer_clip):
                old_tail_values = page_colors[page + 1:]
                page_colors[page + 1:] = [u'LoopSelector.OutsideLoop'] * len(old_tail_values)
            yield
            if clip_is_new_recording(self._sequencer_clip):
                page_colors[page + 1:] = old_tail_values

        if self.is_enabled() and self._has_running_clip():
            position = self._sequencer_clip.playing_position
            visible_page = int(old_div(position, self._page_length_in_beats)) - self.page_offset
            page_colors = self._page_colors
            if 0 <= visible_page < len(page_colors):
                with save_page_color(page_colors, visible_page):
                    if self.song.is_playing:
                        page_colors[visible_page] = u'LoopSelector.PlayheadRecord' if self.song.session_record else u'LoopSelector.Playhead'
                    with replace_and_restore_tail_colors(page_colors, visible_page):
                        self._update_page_leds()
            else:
                self._update_page_leds()
            self._last_playhead_page = visible_page
        else:
            self._update_page_leds()

    def _get_size(self):
        return max(self.loop_selector_matrix.control_count, self.short_loop_selector_matrix.control_count, self._default_size)

    def _get_loop_in_pages(self):
        page_length = self._page_length_in_beats
        loop_start = int(old_div(self._loop_start, page_length))
        loop_end = int(old_div(self._loop_end, page_length))
        loop_length = loop_end - loop_start + int(self._loop_end % page_length != 0)
        return (loop_start, loop_length)

    def _selected_pages_range(self):
        size = self._get_size()
        page_length = self._page_length_in_beats
        seq_page_length = max(old_div(self._paginator.page_length, page_length), 1)
        seq_page_start = int(old_div(self._paginator.page_index * self._paginator.page_length, page_length))
        seq_page_end = int(min(seq_page_start + seq_page_length, self.page_offset + size))
        return (seq_page_start, seq_page_end)

    def _update_page_colors(self):
        u"""
        Update the offline array mapping the timeline of the clip to buttons.
        """
        page_length = self._page_length_in_beats
        size = self._get_size()

        def calculate_page_colors():
            l_start, l_length = self._get_loop_in_pages()
            page_offset = self.page_offset
            pages_per_measure = int(old_div(self._one_measure_in_beats, page_length))

            def color_for_page(absolute_page):
                if l_start <= absolute_page < l_start + l_length:
                    if absolute_page % pages_per_measure == 0:
                        return u'LoopSelector.InsideLoopStartBar'
                    return u'LoopSelector.InsideLoop'
                else:
                    return u'LoopSelector.OutsideLoop'

            return list(map(color_for_page, range(page_offset, page_offset + size)))

        def mark_selected_pages(page_colors):
            for page_index in range(*self._selected_pages_range()):
                button_index = page_index - self.page_offset
                if page_colors[button_index].startswith(u'LoopSelector.InsideLoop'):
                    page_colors[button_index] = u'LoopSelector.SelectedPage'

        page_colors = calculate_page_colors()
        mark_selected_pages(page_colors)
        self._page_colors = page_colors
        self._update_page_and_playhead_leds()

    def _update_page_leds(self):
        self._update_page_leds_in_matrix(self.loop_selector_matrix)
        self._update_page_leds_in_matrix(self.short_loop_selector_matrix)

    def _update_page_leds_in_matrix(self, matrix):
        u""" update hardware leds to match precomputed map """
        if self.is_enabled() and matrix:
            for button, color in zip(matrix, self._page_colors):
                button.color = color

    def _jump_to_page(self, next_page):
        start, length = self._get_loop_in_pages()
        if next_page >= start + length:
            next_page = start
        elif next_page < start:
            next_page = start + length - 1
        self._paginator.select_page_in_point(next_page * self._page_length_in_beats)

    @next_page_button.pressed
    def next_page_button(self, button):
        if self.is_following:
            self.is_following = False
        else:
            _, end = self._selected_pages_range()
            self._jump_to_page(end)
            self._follow_task.restart()

    @next_page_button.released
    def next_page_button(self, button):
        self._follow_task.kill()

    @prev_page_button.pressed
    def prev_page_button(self, button):
        if self.is_following:
            self.is_following = False
        else:
            begin, end = self._selected_pages_range()
            self._jump_to_page(begin - (end - begin))
            self._follow_task.restart()

    @prev_page_button.released
    def prev_page_button(self, button):
        self._follow_task.kill()

    @short_loop_selector_matrix.pressed
    def short_loop_selector_matrix(self, button):
        if self.is_enabled():
            page = self._get_corresponding_page(button, self.short_loop_selector_matrix)
            self._pressed_pages = [page]
            self._try_set_loop()
            self._pressed_pages = []

    @loop_selector_matrix.pressed
    def loop_selector_matrix(self, button):
        if self.is_enabled():
            page = self._get_corresponding_page(button, self.loop_selector_matrix)
            if page not in self._pressed_pages:
                self._on_press_loop_selector_matrix(page)

    @loop_selector_matrix.released
    def loop_selector_matrix(self, button):
        page = self._get_corresponding_page(button, self.loop_selector_matrix)
        if page in self._pressed_pages:
            self._pressed_pages.remove(page)

    def _get_corresponding_page(self, button, matrix):
        y, x = button.coordinate
        return x + y * matrix.width

    def _quantize_page_index(self, page_index, quant):
        page_length = self._page_length_in_beats
        return quant * float(int(old_div(page_length * page_index, quant)))

    def _clear_page(self, page):
        page_start, page_end = self._selected_pages_time_range(page)
        notes = self._sequencer_clip.get_notes_extended(from_time=page_start, from_pitch=0, time_span=page_end, pitch_span=128)
        if len(notes) > 0:
            self._sequencer_clip.remove_notes_extended(from_time=page_start, from_pitch=0, time_span=page_end - page_start, pitch_span=128)
            self._notification_reference = self.show_notification(MessageBoxText.PAGE_CLEARED)
        else:
            self._notification_reference = self.show_notification(MessageBoxText.CANNOT_CLEAR_EMPTY_PAGE)

    def _selected_pages_time_range(self, page):
        page_start = 0
        page_end = 0
        page_length = self._page_length_in_beats
        if self._loop_length > page_length:
            range_start, range_end = self._selected_pages_range()
            page_start = range_start * page_length
            page_end = range_end * page_length
        else:
            page_start = page * page_length
            page_end = page_start + page_length
        return (page_start, page_end)

    def _add_page_to_duplicator(self, page):
        page_start, page_end = self._selected_pages_time_range(page)
        self._step_duplicator.add_step(page_start, page_end, nudge_offset=0, is_page=True)

    def _on_press_loop_selector_matrix(self, page):

        def create_clip(pages):
            measure = self._one_measure_in_beats
            length = self._quantize_page_index(pages, measure) + measure
            create_clip_in_selected_slot(self._clip_creator, self.song, length)

        def handle_page_press_on_clip(page):
            l_start, l_length = self._get_loop_in_pages()
            page_in_loop = l_start <= page < l_start + l_length
            buttons_pressed = len(self._pressed_pages)
            if buttons_pressed == 1 and page_in_loop:
                self._try_select_page(page)
            elif buttons_pressed > 1 or not page_in_loop:
                self._try_set_loop()
            if self._step_duplicator.is_duplicating:
                self._add_page_to_duplicator(page)
            if self.delete_button.is_pressed:
                self._clear_page(page)

        self._pressed_pages.append(page)
        absolute_page = page + self.page_offset
        if not self.select_button.is_pressed:
            if not liveobj_valid(self._sequencer_clip) and not self.song.view.highlighted_clip_slot.has_clip:
                create_clip(absolute_page)
            elif liveobj_valid(self._sequencer_clip):
                handle_page_press_on_clip(absolute_page)
        elif not self.is_following:
            self._try_select_page(absolute_page)

    def _try_select_page(self, page):
        step_time = page * self._page_length_in_beats
        if self._paginator.select_page_in_point(step_time):
            self.is_following = False
            return True
        return False

    def _try_set_loop(self):
        did_set_loop = False
        if liveobj_valid(self._sequencer_clip):
            if not clip_is_new_recording(self._sequencer_clip):
                lowest_page = min(self._pressed_pages) + self.page_offset
                if self._try_select_page(lowest_page):
                    self._set_loop_in_live()
                    did_set_loop = True
            if did_set_loop:
                self.is_following = True
        return did_set_loop

    def _set_loop_in_live(self):
        quant = self._page_length_in_beats
        start_page = min(self._pressed_pages) + self.page_offset
        end_page = max(self._pressed_pages) + self.page_offset
        loop_start = self._quantize_page_index(start_page, quant)
        loop_end = self._quantize_page_index(end_page, quant) + quant
        set_loop(self._sequencer_clip, loop_start, loop_end)
        self._sequencer_clip.view.show_loop()

    @property
    def _page_length_in_beats(self):
        return clamp(self._paginator.page_length, 0.25, self._one_measure_in_beats)

    @property
    def _one_measure_in_beats(self):
        return old_div(self._measure_length * self.song.signature_numerator, self.song.signature_denominator)

    @property
    def page_offset(self):

        def zero_if_none(n):
            if n is None:
                return 0
            return n

        width = zero_if_none(self.loop_selector_matrix.width)
        height = zero_if_none(self.loop_selector_matrix.height)
        size = max(width * height, 1)
        page_index = self._paginator.page_index
        page_length = self._paginator.page_length
        selected_page_index = int(old_div(page_index * page_length, self._page_length_in_beats))
        return size * int(old_div(selected_page_index, size))
