#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/colors.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from past.utils import old_div
from colorsys import rgb_to_hsv, hsv_to_rgb
import MidiRemoteScript
from ableton.v2.base import depends, in_range, listens, liveobj_valid, nop, old_round
from ableton.v2.control_surface.elements.color import DynamicColorBase, DynamicColorFactory
from pushbase.colors import Blink, FallbackColor, Pulse, PushColor, TransparentColor
from .device_util import find_chain_or_track
WHITE_MIDI_VALUE = 122
TRANSLATED_WHITE_INDEX = 7
WHITE_COLOR_INDEX_FROM_LIVE = 13
UNCOLORED_INDEX = WHITE_COLOR_INDEX_FROM_LIVE
HALFLIT_WHITE_MIDI = 14
DISPLAY_BUTTON_SHADE_LEVEL = 1

def make_pulsing_track_color(track, pulse_to_color):
    return Pulse(pulse_to_color, IndexedColor.from_live_index(track.color_index), 48)


def make_blinking_track_color(track, blink_to_color):
    return Blink(blink_to_color, IndexedColor.from_live_index(track.color_index), 24)


def determine_shaded_color_index(color_index, shade_level):
    assert in_range(color_index, 1, 27) or color_index == WHITE_MIDI_VALUE
    assert 0 <= shade_level <= 2
    if shade_level == 0:
        return color_index
    elif color_index == WHITE_MIDI_VALUE:
        return color_index + shade_level
    else:
        return (color_index - 1) * 2 + 64 + shade_level


class IndexedColor(PushColor):
    needs_rgb_interface = True
    midi_value = None

    def __init__(self, index = None, *a, **k):
        super(IndexedColor, self).__init__(midi_value=index, *a, **k)

    @staticmethod
    def from_push_index(index, shade_level = 0):
        return IndexedColor(determine_shaded_color_index(index, shade_level))

    @staticmethod
    def from_live_index(index, shade_level = 0):
        return IndexedColor(determine_shaded_color_index(translate_color_index(index), shade_level))


def translate_color_index(index):
    u"""
    Translates a color index coming from Live into the reduced color palette of Push
    """
    try:
        if index > -1:
            return COLOR_INDEX_TO_PUSH_INDEX[index]
        return TRANSLATED_WHITE_INDEX
    except:
        return TRANSLATED_WHITE_INDEX


def inverse_translate_color_index(translated_index):
    u"""
    Translates a color index coming with the reduced palette of Push [1..26] to the best
    matching color of Live [0..69].
    """
    assert 1 <= translated_index <= len(PUSH_INDEX_TO_COLOR_INDEX)
    return PUSH_INDEX_TO_COLOR_INDEX[translated_index - 1]


class SelectedDrumPadColor(DynamicColorBase):
    u"""
    Dynamic color that sets the color of the currently selected drum pad.
    The drum rack is used from the percussion_instrument_finder.
    """

    @depends(percussion_instrument_finder=nop)
    def __init__(self, song = None, percussion_instrument_finder = None, *a, **k):
        assert liveobj_valid(song)
        super(SelectedDrumPadColor, self).__init__(*a, **k)
        self.song = song
        if percussion_instrument_finder is not None:
            self.__on_selected_track_color_index_changed.subject = self.song.view
            self.__on_instrument_changed.subject = percussion_instrument_finder
            self.__on_instrument_changed()

    @listens(u'instrument')
    def __on_instrument_changed(self):
        drum_group = self.__on_instrument_changed.subject.drum_group
        if liveobj_valid(drum_group):
            self.__on_selected_drum_pad_chains_changed.subject = drum_group.view
            self.__on_selected_drum_pad_chains_changed()

    @listens(u'selected_drum_pad.chains')
    def __on_selected_drum_pad_chains_changed(self):
        drum_pad = self.__on_selected_drum_pad_chains_changed.subject.selected_drum_pad
        if liveobj_valid(drum_pad) and drum_pad.chains:
            self.__on_color_index_changed.subject = drum_pad.chains[0]
            self.__on_color_index_changed()
        else:
            self._update_midi_value(self.song.view.selected_track)

    @listens(u'color_index')
    def __on_color_index_changed(self):
        chain = self.__on_color_index_changed.subject
        self._update_midi_value(chain)

    @listens(u'selected_track.color_index')
    def __on_selected_track_color_index_changed(self):
        drum_group = self.__on_selected_drum_pad_chains_changed.subject
        drum_pad = drum_group.selected_drum_pad if liveobj_valid(drum_group) else None
        if not liveobj_valid(drum_pad) or not drum_pad.chains:
            self._update_midi_value(self.song.view.selected_track)


class SelectedDrumPadColorFactory(DynamicColorFactory):

    def instantiate(self, song):
        return SelectedDrumPadColor(song=song, transformation=self._transform)


class SelectedDeviceChainColor(DynamicColorBase):

    @depends(device_provider=nop)
    def __init__(self, device_provider = None, *a, **k):
        super(SelectedDeviceChainColor, self).__init__(*a, **k)
        if device_provider is not None:
            self.__on_device_changed.subject = device_provider
            self.__on_device_changed()

    @listens(u'device')
    def __on_device_changed(self):
        device = self.__on_device_changed.subject.device
        chain = find_chain_or_track(device)
        self.__on_chain_color_index_changed.subject = chain
        self.__on_chain_color_index_changed()

    @listens(u'color_index')
    def __on_chain_color_index_changed(self):
        chain = self.__on_chain_color_index_changed.subject
        if liveobj_valid(chain):
            self._update_midi_value(chain)


class SelectedDeviceChainColorFactory(DynamicColorFactory):

    def instantiate(self, song):
        return SelectedDeviceChainColor(transformation=self._transform)


def make_color_factory_func(factory_class):

    def make_color_factory(shade_level = 0):
        return factory_class(transformation=lambda color_index: determine_shaded_color_index(translate_color_index(color_index), shade_level))

    return make_color_factory


class Rgb(object):
    AMBER = IndexedColor(3)
    AMBER_SHADE = IndexedColor(69)
    AMBER_SHADE_TWO = IndexedColor(70)
    YELLOW = IndexedColor(6)
    YELLOW_SHADE = IndexedColor(75)
    YELLOW_SHADE_TWO = IndexedColor(76)
    YELLOW_HIGHLIGHT = IndexedColor(40)
    PURPLE = IndexedColor(49)
    OCEAN = IndexedColor(33)
    DEEP_OCEAN = IndexedColor(95)
    SKY = IndexedColor(46)
    GREEN = IndexedColor(126)
    GREEN_SHADE = IndexedColor(32)
    RED = IndexedColor(127)
    RED_SHADE = IndexedColor(27)
    RED_SHADE_TWO = IndexedColor(66)
    BLUE = IndexedColor(125)
    LIGHT_GREY = IndexedColor(123)
    DARK_GREY = IndexedColor(124)
    BLACK = IndexedColor(0)
    WHITE = IndexedColor(WHITE_MIDI_VALUE)


class Basic(object):
    HALF = FallbackColor(Rgb.DARK_GREY, HALFLIT_WHITE_MIDI)
    OFF = FallbackColor(Rgb.BLACK, 0)
    ON = FallbackColor(Rgb.WHITE, 127)
    FULL_BLINK_SLOW = Blink(FallbackColor(Rgb.WHITE, 127), FallbackColor(Rgb.BLACK, 0), 24)
    FULL_PULSE_SLOW = Pulse(FallbackColor(Rgb.DARK_GREY, HALFLIT_WHITE_MIDI), FallbackColor(Rgb.WHITE, 127), 48)
    FAST_PULSE = Pulse(FallbackColor(Rgb.DARK_GREY, HALFLIT_WHITE_MIDI), FallbackColor(Rgb.WHITE, 127), 24)
    TRANSPARENT = TransparentColor()


class ScreenColor(object):
    u"""
    An RGB color intended for use on the Push 2 screen, with functions for
    creating the various shades that are used.
    """

    def __init__(self, red, green, blue):
        super(ScreenColor, self).__init__()
        self.red = red
        self.green = green
        self.blue = blue

    @staticmethod
    def from_hsv(*hsv):
        u"""
        Creates a ScreenColor from an hsv triplet.
        Each input component ranges from 0..1
        """
        return ScreenColor(*hsv_to_rgb(*hsv)).denormalise()

    def as_hsv(self):
        u"""
        Creates an hsv triplet from a ScreenColor.
        Each result component ranges from 0..1
        """
        return rgb_to_hsv(*self.normalise().as_tuple())

    def as_tuple(self):
        u"""
        Returns the red, green and blue components as a triple
        """
        return (self.red, self.green, self.blue)

    def as_remote_script_color(self, alpha = 255):
        u"""
        Creates a new C++ API color (internally a TColor)
        """
        return MidiRemoteScript.RgbaColor(self.red, self.green, self.blue, alpha)

    def map_channels(self, map_function):
        u"""
        Applies map_function to each of the rgb channels and returns
        a new color with the result
        """
        return ScreenColor(map_function(self.red), map_function(self.green), map_function(self.blue))

    def shade(self, amount):
        u"""
        Returns a new colour which is this colour mixed with an
        amount of black. When amount == 0, no black is mixed.
        When amount == 0.5, then the colours components are
        reduced by 50%. When amount == 1.0, then the result
        is black.
        """
        scale = 1.0 - amount
        return self.map_channels(lambda component: int(old_round(component * scale)))

    def normalise(self):
        u"""
        Returns a new colour with this color's components normalised
        with an assumed range 0..255
        """
        return self.map_channels(lambda component: old_div(float(component), 255.0))

    def denormalise(self):
        u"""
        Returns a new colour with this color's components denormalised
        to a range of 0..255
        """
        return self.map_channels(lambda component: int(old_round(255 * component)))

    def adjust_saturation(self, amount):
        u"""
        Returns a new colour which is this colour with its saturation increased
        by amount. If amount == 0, the saturation is not changed.
        If amount == -1.0, the saturation is reduced to 0.
        If amount == 0.5, the saturation is increased by 50%.
        """
        h, s, v = self.as_hsv()
        s *= 1.0 + amount
        return ScreenColor.from_hsv(h, s, v)


COLOR_INDEX_TO_PUSH_INDEX = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 7, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 5, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 22, 25, 17, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 21, 2, 4, 6, 8, 10, 12, 14, 20, 19, 18, 22, 23, 26, 6)
PUSH_INDEX_TO_SCREEN_COLOR = (ScreenColor(255, 255, 255),
 ScreenColor(237, 89, 56),
 ScreenColor(209, 23, 10),
 ScreenColor(255, 100, 0),
 ScreenColor(255, 50, 0),
 ScreenColor(128, 71, 19),
 ScreenColor(88, 35, 7),
 ScreenColor(237, 218, 60),
 ScreenColor(228, 194, 0),
 ScreenColor(148, 255, 24),
 ScreenColor(0, 230, 49),
 ScreenColor(0, 157, 50),
 ScreenColor(51, 158, 19),
 ScreenColor(0, 185, 85),
 ScreenColor(0, 113, 78),
 ScreenColor(0, 204, 137),
 ScreenColor(0, 187, 173),
 ScreenColor(0, 113, 164),
 ScreenColor(0, 106, 202),
 ScreenColor(73, 50, 179),
 ScreenColor(0, 90, 98),
 ScreenColor(82, 96, 221),
 ScreenColor(171, 80, 255),
 ScreenColor(225, 87, 227),
 ScreenColor(136, 66, 91),
 ScreenColor(255, 30, 50),
 ScreenColor(255, 74, 150))
COLOR_INDEX_TO_SCREEN_COLOR = tuple([ PUSH_INDEX_TO_SCREEN_COLOR[push_index] for push_index in COLOR_INDEX_TO_PUSH_INDEX ])
COLOR_INDEX_TO_SCREEN_COLOR_SHADES = [tuple([ color.shade(0.2) for color in COLOR_INDEX_TO_SCREEN_COLOR ]),
 tuple([ color.shade(0.5) for color in COLOR_INDEX_TO_SCREEN_COLOR ]),
 tuple([ color.shade(0.7) for color in COLOR_INDEX_TO_SCREEN_COLOR ]),
 tuple([ color.shade(0.7).adjust_saturation(-0.2) for color in COLOR_INDEX_TO_SCREEN_COLOR ]),
 tuple([ color.adjust_saturation(-0.7) for color in COLOR_INDEX_TO_SCREEN_COLOR ])]
PUSH_INDEX_TO_COLOR_INDEX = (0, 14, 1, 15, 2, 16, 3, 17, 4, 18, 5, 19, 6, 20, 7, 21, 8, 22, 9, 23, 10, 24, 11, 25, 12, 26)
COLOR_TABLE = ((0, 0, 0),
 (1, 16728114, 2),
 (2, 8389632, 4),
 (3, 13188096, 6),
 (4, 11280128, 8),
 (5, 9195544, 10),
 (6, 4790276, 12),
 (7, 16440379, 14),
 (8, 16762134, 16),
 (9, 11992846, 18),
 (10, 7995160, 20),
 (11, 3457558, 22),
 (12, 5212676, 24),
 (13, 6487893, 26),
 (14, 2719059, 28),
 (15, 2530930, 30),
 (16, 3255807, 32),
 (17, 3564540, 34),
 (18, 1717503, 36),
 (19, 1838310, 38),
 (20, 1391001, 40),
 (21, 3749887, 42),
 (22, 5710591, 44),
 (23, 9907199, 46),
 (24, 8724856, 48),
 (25, 16715826, 50),
 (26, 16722900, 52),
 (27, 10892321, 54),
 (28, 10049064, 56),
 (29, 8873728, 58),
 (30, 9470495, 60),
 (31, 4884224, 62),
 (32, 32530, 64),
 (33, 1594290, 66),
 (34, 6441901, 68),
 (35, 7551591, 70),
 (36, 16301231, 72),
 (37, 16751478, 74),
 (38, 16760671, 76),
 (39, 14266225, 78),
 (40, 16774272, 80),
 (41, 12565097, 80),
 (42, 12373128, 81),
 (43, 11468697, 81),
 (44, 8183199, 82),
 (45, 9024637, 82),
 (46, 8451071, 83),
 (47, 8048380, 83),
 (48, 6857171, 84),
 (49, 8753090, 85),
 (50, 12298994, 85),
 (51, 13482980, 86),
 (52, 15698864, 86),
 (53, 8756620, 87),
 (54, 7042414, 87),
 (55, 8687771, 88),
 (56, 6975605, 88),
 (57, 8947101, 89),
 (58, 7105141, 90),
 (59, 10323356, 90),
 (60, 7629428, 91),
 (61, 10263941, 91),
 (62, 7632234, 92),
 (63, 10323076, 92),
 (64, 7694954, 93),
 (65, 6691092, 93),
 (66, 2164742, 94),
 (67, 4588288, 94),
 (68, 2621440, 95),
 (69, 6100736, 96),
 (70, 2100480, 96),
 (71, 4656128, 97),
 (72, 1837056, 97),
 (73, 3877652, 98),
 (74, 1839882, 98),
 (75, 2428421, 99),
 (76, 853506, 99),
 (77, 6576151, 100),
 (78, 2104327, 101),
 (79, 6704648, 101),
 (80, 2169090, 102),
 (81, 4744709, 102),
 (82, 1515777, 103),
 (83, 3171849, 103),
 (84, 991491, 104),
 (85, 1330440, 104),
 (86, 399618, 105),
 (87, 2045697, 106),
 (88, 659712, 106),
 (89, 2582050, 107),
 (90, 794891, 107),
 (91, 1326633, 108),
 (92, 530704, 108),
 (93, 19766, 109),
 (94, 6158, 109),
 (95, 1262950, 110),
 (96, 398881, 110),
 (97, 1386340, 111),
 (98, 461856, 112),
 (99, 660582, 112),
 (100, 198177, 113),
 (101, 722012, 113),
 (102, 196893, 114),
 (103, 662604, 114),
 (104, 264990, 115),
 (105, 1447526, 115),
 (106, 460577, 116),
 (107, 2231654, 117),
 (108, 721953, 117),
 (109, 3936614, 118),
 (110, 1246497, 118),
 (111, 3476784, 119),
 (112, 1115151, 119),
 (113, 6686228, 120),
 (114, 2163206, 120),
 (115, 6689108, 121),
 (116, 2163995, 122),
 (117, 0, 122),
 (118, 5855577, 123),
 (119, 1710618, 123),
 (120, 16777215, 124),
 (121, 5855577, 124),
 (122, 13421772, 125),
 (123, 4210752, 125),
 (124, 1315860, 126),
 (125, 255, 126),
 (126, 65280, 127),
 (127, 16711680, 127))
