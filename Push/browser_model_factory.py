#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/browser_model_factory.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from .browser_model import filter_type_for_browser, EmptyBrowserModel, QueryingBrowserModel
from .browser_query import TagBrowserQuery, PathBrowserQuery, PlacesBrowserQuery, SourceBrowserQuery, ColorTagsBrowserQuery
FilterType = Live.Browser.FilterType
PLACES_LABEL = u'Places'

def make_plugins_query():
    return TagBrowserQuery(include=[u'Plug-Ins'], root_name=u'plugins', subfolder=u'Plug-Ins')


def make_midi_effect_browser_model(browser):
    midi_effects = TagBrowserQuery(include=[u'MIDI Effects'], root_name=u'midi_effects')
    max = TagBrowserQuery(include=[[u'Max for Live', u'Max MIDI Effect']], subfolder=u'Max for Live', root_name=u'max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[color_tags,
     midi_effects,
     max,
     plugins,
     places])


def make_audio_effect_browser_model(browser):
    audio_effects = TagBrowserQuery(include=[u'Audio Effects'], root_name=u'audio_effects')
    max = TagBrowserQuery(include=[[u'Max for Live', u'Max Audio Effect']], subfolder=u'Max for Live', root_name=u'max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[color_tags,
     audio_effects,
     max,
     plugins,
     places])


def make_instruments_browser_model(browser):
    instrument_rack = PathBrowserQuery(path=[u'Instruments', u'Instrument Rack'], root_name=u'instruments')
    drums = SourceBrowserQuery(include=[u'Drums'], exclude=[u'Drum Hits'], subfolder=u'Drum Rack', root_name=u'drums')
    instruments = TagBrowserQuery(include=[u'Instruments'], exclude=[u'Drum Rack', u'Instrument Rack'], root_name=u'instruments')
    drum_hits = TagBrowserQuery(include=[[u'Drums', u'Drum Hits']], subfolder=u'Drum Hits', root_name=u'drums')
    max = TagBrowserQuery(include=[[u'Max for Live', u'Max Instrument']], subfolder=u'Max for Live', root_name=u'max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[color_tags,
     instrument_rack,
     drums,
     instruments,
     max,
     drum_hits,
     plugins,
     places])


def make_drum_pad_browser_model(browser):
    drums = TagBrowserQuery(include=[[u'Drums', u'Drum Hits']], root_name=u'drums')
    samples = SourceBrowserQuery(include=[u'Samples'], subfolder=u'Samples', root_name=u'samples')
    instruments = TagBrowserQuery(include=[u'Instruments'], root_name=u'instruments')
    max = TagBrowserQuery(include=[[u'Max for Live', u'Max Instrument']], subfolder=u'Max for Live', root_name=u'max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[color_tags,
     drums,
     samples,
     instruments,
     max,
     plugins,
     places])


def make_fallback_browser_model(browser):
    return EmptyBrowserModel(browser=browser)


def make_browser_model(browser, filter_type = None):
    u"""
    Factory that returns an appropriate browser model depending on the
    browser filter type and hotswap target.
    """
    factories = {FilterType.instrument_hotswap: make_instruments_browser_model,
     FilterType.drum_pad_hotswap: make_drum_pad_browser_model,
     FilterType.audio_effect_hotswap: make_audio_effect_browser_model,
     FilterType.midi_effect_hotswap: make_midi_effect_browser_model}
    if filter_type == None:
        filter_type = filter_type_for_browser(browser)
    return factories.get(filter_type, make_fallback_browser_model)(browser)
