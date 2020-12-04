#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/browser_query.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import filter
from builtins import map
from builtins import object
from future.utils import string_types
from functools import partial
from ableton.v2.base import first, find_if, const
from .browser_model import VirtualBrowserItem
import Live

class BrowserQuery(object):
    u"""
    Base class for browser queries. Is capable of creating a subfolder for wrapping
    all results of the query.
    """

    def __init__(self, subfolder = None, *a, **k):
        self.subfolder = subfolder

    def __call__(self, browser):
        if self.subfolder:
            return [VirtualBrowserItem(name=self.subfolder, children_query=partial(self.query, browser), is_folder=True)]
        else:
            return self.query(browser)

    def query(self, browser):
        raise NotImplementedError


class PathBrowserQuery(BrowserQuery):
    u"""
    Includes the element for the given path.
    """

    def __init__(self, path = tuple(), root_name = None, *a, **k):
        assert root_name is not None
        assert path
        super(PathBrowserQuery, self).__init__(*a, **k)
        self.path = path
        self.root_name = root_name

    def query(self, browser):
        return self._find_item(self.path, [getattr(browser, self.root_name)], browser) or []

    def _find_item(self, path, items = None, browser = None):
        name = path[0]
        elem = find_if(lambda x: x.name == name, items)
        if elem:
            if len(path) == 1:
                return [elem]
            return self._find_item(path[1:], elem.children)


class TagBrowserQuery(BrowserQuery):
    u"""
    Query that merges the contents of the specified subtrees of
    the browser.  It will first merge the contents of all the paths
    specified in the 'include' list. A path is either the name of a
    tag or a list with the name of the tag/folders that describe the
    path. Then it drops the items that are in the 'exclude' list.
    """

    def __init__(self, include = tuple(), exclude = tuple(), root_name = None, *a, **k):
        assert root_name is not None
        super(TagBrowserQuery, self).__init__(*a, **k)
        self.include = include
        self.exclude = exclude
        self.root_name = root_name

    def query(self, browser):
        return list(filter(lambda item: item.name not in self.exclude, sum(list(map(partial(self._extract_path, browser=browser), self.include)), tuple())))

    def _extract_path(self, path, items = None, browser = None):
        if isinstance(path, string_types):
            path = [path]
        if items is None:
            items = [getattr(browser, self.root_name)]
        if path:
            name = path[0]
            elem = find_if(lambda x: x.name == name, items)
            if elem:
                items = self._extract_path(path[1:], elem.children)
        return tuple(items)


class SourceBrowserQuery(TagBrowserQuery):
    u"""
    Like TagBrowserQuery, but adds a top-level source selection.
    """

    def __init__(self, *a, **k):
        super(SourceBrowserQuery, self).__init__(*a, **k)

    def query(self, browser):
        root = super(SourceBrowserQuery, self).query(browser)
        groups = dict()
        for item in root:
            groups.setdefault(item.source, []).append(item)

        return list(map(lambda k_g: VirtualBrowserItem(name=k_g[0] if k_g[0] is not None else u'', children_query=const(k_g[1])), sorted(list(groups.items()), key=first)))


class PlacesBrowserQuery(BrowserQuery):
    u"""
    Query that fetches all places of the browser
    """

    def __init__(self, *a, **k):
        super(PlacesBrowserQuery, self).__init__(*a, **k)

    def query(self, browser):
        return [browser.packs, browser.user_library] + [browser.current_project] + list(browser.user_folders)


class ColorTagsBrowserQuery(BrowserQuery):
    u"""
    Query that fetches all color (tags) of the browser
    """

    def __init__(self, *a, **k):
        super(ColorTagsBrowserQuery, self).__init__(*a, **k)

    def query(self, browser):
        return list(browser.colors)
