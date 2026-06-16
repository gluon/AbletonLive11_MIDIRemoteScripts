# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\browser_model.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 12542 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map, object
import os
from functools import partial
from itertools import chain
import Live
from ableton.v2.base import BooleanContext, EventObject, find_if, first, in_range, index_if, lazy_attribute, nop
from pushbase.browser_util import filter_type_for_hotswap_target
from pushbase.scrollable_list import ActionList, ActionListItem
from .special_physical_display import SpecialPhysicalDisplay

def filter_type_for_browser(browser):
    filter_type = filter_type_for_hotswap_target(browser.hotswap_target)
    if filter_type == Live.Browser.FilterType.disabled:
        filter_type = browser.filter_type
    return filter_type


class VirtualBrowserItem(object):
    source = ''
    is_device = False
    is_loadable = False

    def __init__(self, name='', children_query=nop, is_folder=False):
        self.name = name
        self.is_folder = is_folder
        self.children_query = children_query

    @lazy_attribute
    def children(self):
        return self.children_query()

    @property
    def is_selected(self):
        return find_if(lambda x: x.is_selected
, self.children)

    def __str__(self):
        return self.name


class BrowserListItem(ActionListItem):
    URI_TO_NAME_FALLBACK = {
      'query:Synths': 'Instruments',
      'query:Drums': 'Drums',
      'query:UserLibrary': 'User Library',
      'query:Plugins': 'Plug-Ins'}

    def __str__(self):
        return self._item_name

    @lazy_attribute
    def _item_name(self):
        item_name = os.path.splitext(self.content.name)[0] if self.content else ''
        can_be_displayed = SpecialPhysicalDisplay.can_be_translated(SpecialPhysicalDisplay.ascii_translations, item_name)
        if not can_be_displayed:
            uri = getattr(self.content, 'uri', '')
            return self.URI_TO_NAME_FALLBACK.get(uri, item_name)
        return item_name

    def action(self):
        if self.container:
            if self.container.browser:
                self.container.browser.load_item(self.content)

    def preview(self):
        if self.container:
            if self.container.browser:
                if not isinstance(self.content, VirtualBrowserItem):
                    self.container.browser.preview_item(self.content)

    @property
    def supports_action(self):
        return self.container and self.container.browser and self.content != None and self.content.is_loadable


class BrowserList(ActionList):
    browser = None
    item_type = BrowserListItem

    def __init__(self, browser=None, *a, **k):
        (super(BrowserList, self).__init__)(*a, **k)
        self.browser = browser


class BrowserModel(EventObject):
    __events__ = ('content_lists', 'selection_updated')
    empty_list_messages = []

    def __init__(self, browser=None, *a, **k):
        (super(BrowserModel, self).__init__)(*a, **k)
        self._browser = browser

    def can_be_exchanged(self, model):
        return isinstance(model, BrowserModel)

    def exchange_model(self, model):
        if self.can_be_exchanged(model):
            self._browser = model._browser
            return True
        return False

    @property
    def content_lists(self):
        return NotImplementedError

    def update_content(self):
        raise NotImplementedError

    def update_selection(self):
        raise NotImplementedError

    @property
    def browser(self):
        return self._browser

    def make_content_list(self):
        return BrowserList(browser=(self._browser))


class EmptyBrowserModel(BrowserModel):
    empty_list_messages = [
     'Nothing to browse']

    @property
    def content_lists(self):
        return tuple()

    def update_content(self):
        self.notify_content_lists()

    def update_selection(self):
        pass

    def can_be_exchanged(self, model):
        return isinstance(model, EmptyBrowserModel) and super(EmptyBrowserModel, self).can_be_exchanged(model)


class FullBrowserModel(BrowserModel):
    empty_list_messages = [
     '<no tags>', '<no devices>', '<no presets>', '<no presets>']

    def __init__(self, *a, **k):
        (super(FullBrowserModel, self).__init__)(*a, **k)
        self._contents = []
        self._num_contents = 0
        self._push_content_list()
        self._inside_item_activated_notification = BooleanContext()

    def get_root_children(self):
        return [
         self.browser.sounds,
         self.browser.drums,
         self.browser.instruments,
         self.browser.audio_effects,
         self.browser.midi_effects,
         self.browser.max_for_live,
         self.browser.plugins,
         self.browser.clips,
         self.browser.samples]

    def get_children(self, item, level):
        return item.children

    @property
    def content_lists(self):
        return list(map(first, self._contents[:self._num_contents]))

    def can_be_exchanged(self, model):
        return isinstance(model, FullBrowserModel) and super(FullBrowserModel, self).can_be_exchanged(model)

    def update_content(self):
        root, _ = self._contents[0]
        root.assign_items(self.get_root_children())
        self.update_selection()

    def update_selection(self):
        last_seleced_list_index = None
        if self._browser.hotswap_target != None:
            list_index = 0
            while list_index < self._num_contents:
                content_list, _ = self._contents[list_index]
                items = content_list.items
                index = index_if(lambda x: x.content.is_selected
, items)
                if in_range(index, 0, len(items)):
                    content_list.select_item_index_with_offset(index, 2)
                    last_seleced_list_index = list_index
                else:
                    list_index += 1

        if last_seleced_list_index != None:
            self.notify_selection_updated(last_seleced_list_index)

    def _push_content_list(self):
        if self._num_contents < len(self._contents):
            self._num_contents += 1
            content = self._contents[self._num_contents - 1]
        else:
            content = self.make_content_list()
            level = len(self._contents)
            slot = self.register_slot(content, partial(self._on_item_activated, level), 'item_activated')
            self._contents.append((content, slot))
            self._num_contents = len(self._contents)
        return content

    def _pop_content_list(self):
        self._num_contents -= 1

    def _fit_content_lists(self, requested_lists):
        if requested_lists != self._num_contents:
            while requested_lists < self._num_contents:
                self._pop_content_list()

            while requested_lists > self._num_contents:
                self._push_content_list()

    def _finalize_content_lists_change(self):
        while self._num_contents < len(self._contents):
            _, slot = self._contents.pop()
            self.disconnect_disconnectable(slot)

    def _on_item_activated(self, level):
        old_num_contents = self._num_contents
        with self._inside_item_activated_notification():
            contents, _ = self._contents[level]
            selected = contents.selected_item
            is_folder = selected != None and selected.content.is_folder
            children = self.get_children(selected.content, level) if selected != None else []
            if children or is_folder or level < 1:
                self._fit_content_lists(level + 2)
                child_contents, _ = self._contents[level + 1]
                child_contents.assign_items(children)
            else:
                self._fit_content_lists(level + 1)
        if not self._inside_item_activated_notification:
            self._finalize_content_lists_change()
            if old_num_contents != self._num_contents:
                self.notify_content_lists()


class QueryingBrowserModel(FullBrowserModel):
    empty_list_messages = [
     '<no devices>', '<no presets>', '<no presets>', '<no presets>']

    def __init__(self, queries=[], *a, **k):
        (super(QueryingBrowserModel, self).__init__)(*a, **k)
        self.queries = queries

    def get_root_children(self):
        browser = self.browser
        return chain.from_iterable(map(lambda q: q(browser)
, self.queries))

    def can_be_exchanged(self, model):
        return isinstance(model, QueryingBrowserModel) and super(QueryingBrowserModel, self).can_be_exchanged(model)

    def exchange_model(self, model):
        if super(QueryingBrowserModel, self).exchange_model(model):
            self.queries = model.queries
            return True