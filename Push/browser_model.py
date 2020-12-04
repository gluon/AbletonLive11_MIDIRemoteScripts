#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/browser_model.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from builtins import object
import os
from functools import partial
from itertools import chain
import Live
from ableton.v2.base import first, nop, find_if, index_if, in_range, lazy_attribute, BooleanContext, EventObject
from pushbase.scrollable_list import ActionList, ActionListItem
from pushbase.browser_util import filter_type_for_hotswap_target
from .special_physical_display import SpecialPhysicalDisplay

def filter_type_for_browser(browser):
    filter_type = filter_type_for_hotswap_target(browser.hotswap_target)
    if filter_type == Live.Browser.FilterType.disabled:
        filter_type = browser.filter_type
    return filter_type


class VirtualBrowserItem(object):
    u"""
    Quacks like a Live.Browser.BrowserItem
    """
    source = u''
    is_device = False
    is_loadable = False

    def __init__(self, name = u'', children_query = nop, is_folder = False):
        self.name = name
        self.is_folder = is_folder
        self.children_query = children_query

    @lazy_attribute
    def children(self):
        return self.children_query()

    @property
    def is_selected(self):
        return find_if(lambda x: x.is_selected, self.children)

    def __str__(self):
        return self.name


class BrowserListItem(ActionListItem):
    u"""
    List item representing a browser element
    """
    URI_TO_NAME_FALLBACK = {u'query:Synths': u'Instruments',
     u'query:Drums': u'Drums',
     u'query:UserLibrary': u'User Library',
     u'query:Plugins': u'Plug-Ins'}

    def __str__(self):
        return self._item_name

    @lazy_attribute
    def _item_name(self):
        item_name = os.path.splitext(self.content.name)[0] if self.content else u''
        can_be_displayed = SpecialPhysicalDisplay.can_be_translated(SpecialPhysicalDisplay.ascii_translations, item_name)
        if not can_be_displayed:
            uri = getattr(self.content, u'uri', u'')
            return self.URI_TO_NAME_FALLBACK.get(uri, item_name)
        return item_name

    def action(self):
        if self.container and self.container.browser:
            self.container.browser.load_item(self.content)

    def preview(self):
        if self.container and self.container.browser and not isinstance(self.content, VirtualBrowserItem):
            self.container.browser.preview_item(self.content)

    @property
    def supports_action(self):
        return self.container and self.container.browser and self.content != None and self.content.is_loadable


class BrowserList(ActionList):
    u"""
    Component for representing lists of browser items
    """
    browser = None
    item_type = BrowserListItem

    def __init__(self, browser = None, *a, **k):
        super(BrowserList, self).__init__(*a, **k)
        self.browser = browser


class BrowserModel(EventObject):
    u"""
    A browser model provides the data to a browser component as a
    sequence of BrowserLists.
    
    The BrowserComponent will use equality to discard equivalent
    models and prevent unnecessary updating, override it when
    neccesary.
    """
    __events__ = (u'content_lists', u'selection_updated')
    empty_list_messages = []

    def __init__(self, browser = None, *a, **k):
        super(BrowserModel, self).__init__(*a, **k)
        self._browser = browser

    def can_be_exchanged(self, model):
        return isinstance(model, BrowserModel)

    def exchange_model(self, model):
        u"""
        Tries to replace itself with the settings of a given
        model. Returns true if it succeeds or false if the current
        model can not represent the same set of values.
        """
        if self.can_be_exchanged(model):
            self._browser = model._browser
            return True
        return False

    @property
    def content_lists(self):
        u"""
        Returns a set of ActionLists that hold the hierarchy of
        content for the browser.
        """
        return NotImplementedError

    def update_content(self):
        u"""
        Called when the browser contents have changed.
        """
        raise NotImplementedError

    def update_selection(self):
        u"""
        Called when the browser selection might have changed.
        """
        raise NotImplementedError

    @property
    def browser(self):
        return self._browser

    def make_content_list(self):
        return BrowserList(browser=self._browser)


class EmptyBrowserModel(BrowserModel):
    u"""
    A browser model that never returns anything, to be used for
    hotswap targets that do not make sense in Push.
    """
    empty_list_messages = [u'Nothing to browse']

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
    u"""
    A browser model that provides an abstract hierarchical query model
    for simpler implementation.  Note that this can result in endless
    nesting, which the BrowserComponent does not support so far.
    It always provides at least two columns.
    """
    empty_list_messages = [u'<no tags>',
     u'<no devices>',
     u'<no presets>',
     u'<no presets>']

    def __init__(self, *a, **k):
        super(FullBrowserModel, self).__init__(*a, **k)
        self._contents = []
        self._num_contents = 0
        self._push_content_list()
        self._inside_item_activated_notification = BooleanContext()

    def get_root_children(self):
        u"""
        Query for the initial items.
        """
        return [self.browser.sounds,
         self.browser.drums,
         self.browser.instruments,
         self.browser.audio_effects,
         self.browser.midi_effects,
         self.browser.max_for_live,
         self.browser.plugins,
         self.browser.clips,
         self.browser.samples]

    def get_children(self, item, level):
        u"""
        Query for children of node.
        """
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
                index = index_if(lambda x: x.content.is_selected, items)
                if in_range(index, 0, len(items)):
                    content_list.select_item_index_with_offset(index, 2)
                    last_seleced_list_index = list_index
                list_index += 1

        if last_seleced_list_index != None:
            self.notify_selection_updated(last_seleced_list_index)

    def _push_content_list(self):
        if self._num_contents < len(self._contents):
            self._num_contents += 1
            content = self._contents[self._num_contents - 1]
        else:
            assert self._num_contents == len(self._contents)
            content = self.make_content_list()
            level = len(self._contents)
            slot = self.register_slot(content, partial(self._on_item_activated, level), u'item_activated')
            self._contents.append((content, slot))
            self._num_contents = len(self._contents)
        return content

    def _pop_content_list(self):
        assert self._num_contents > 1
        self._num_contents -= 1

    def _fit_content_lists(self, requested_lists):
        u"""
        Ensures that there are exactly 'request_lists' number of
        content lists. Returns whether a change was needed or not.
        """
        assert requested_lists > 0
        if requested_lists != self._num_contents:
            while requested_lists < self._num_contents:
                self._pop_content_list()

            while requested_lists > self._num_contents:
                self._push_content_list()

    def _finalize_content_lists_change(self):
        u"""
        After a series of push/pop/fit operations, this makes sure
        that we only have as many content lists referenced as
        necessary.
        """
        while self._num_contents < len(self._contents):
            _, slot = self._contents.pop()
            self.disconnect_disconnectable(slot)

        assert self._num_contents == len(self._contents)

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
    u"""
    Browser model that takes query objects to build up the model hierarchy
    """
    empty_list_messages = [u'<no devices>',
     u'<no presets>',
     u'<no presets>',
     u'<no presets>']

    def __init__(self, queries = [], *a, **k):
        super(QueryingBrowserModel, self).__init__(*a, **k)
        self.queries = queries

    def get_root_children(self):
        browser = self.browser
        return chain.from_iterable(map(lambda q: q(browser), self.queries))

    def can_be_exchanged(self, model):
        return isinstance(model, QueryingBrowserModel) and super(QueryingBrowserModel, self).can_be_exchanged(model)

    def exchange_model(self, model):
        if super(QueryingBrowserModel, self).exchange_model(model):
            self.queries = model.queries
            return True
