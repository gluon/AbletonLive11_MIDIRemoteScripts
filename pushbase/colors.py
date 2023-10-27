# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\colors.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 10907 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from past.utils import old_div
from itertools import repeat
from ableton.v2.control_surface.elements import Color, to_midi_value

class PushColor(Color):
    needs_rgb_interface = False

    def can_draw_on_interface(self, interface):
        return not self.needs_rgb_interface or interface.is_rgb

    def draw(self, interface):
        super(PushColor, self).draw(interface)


class RgbColor(PushColor):
    needs_rgb_interface = True
    _rgb_value = (0, 0, 0)

    def __init__(self, midi_value=None, rgb_value=None, *a, **k):
        (super(RgbColor, self).__init__)(a, midi_value=midi_value, **k)
        if rgb_value is not None:
            self._rgb_value = rgb_value

    def shade(self, shade_level):
        shade_factor = old_div(1.0, 2.0) * (2 - shade_level)
        return RgbColor(self.midi_value + shade_level, [a * b for a, b in zip(self._rgb_value, repeat(shade_factor))])

    def highlight(self):
        return RgbColor(self.midi_value - 1, [a * b for a, b in zip(self._rgb_value, repeat(1.5))])

    def __iter__(self):
        return iter(self._rgb_value)

    def __getitem__(self, index_or_slice):
        return self._rgb_value[index_or_slice]


class FallbackColor(PushColor):

    def __init__(self, default_color=None, fallback_color=None, *a, **k):
        (super(FallbackColor, self).__init__)(a, midi_value=to_midi_value(fallback_color), **k)
        self.default_color = default_color

    def draw(self, interface):
        if self.default_color.can_draw_on_interface(interface):
            self.default_color.draw(interface)
        else:
            super(FallbackColor, self).draw(interface)


class AnimatedColor(PushColor):

    @property
    def midi_value(self):
        return self.convert_to_midi_value()

    def __init__(self, color1=RgbColor(), color2=RgbColor(), channel2=7, *a, **k):
        (super(AnimatedColor, self).__init__)(*a, **k)
        self.color1 = color1
        self.color2 = color2
        self.channel2 = channel2

    def can_draw_on_interface(self, interface):
        return self.color1.can_draw_on_interface(interface) and self.color2.can_draw_on_interface(interface)

    def draw(self, interface):
        interface.send_value(self.color1.midi_value)
        interface.send_value((self.color2.midi_value), channel=(self.channel2))

    def convert_to_midi_value(self):
        raise NotImplementedError('Animations cannot be serialized')


class Pulse(AnimatedColor):

    def __init__(self, color1=RgbColor(), color2=RgbColor(), speed=6, *a, **k):
        channel2 = [4,6,12,24,48].index(speed) + 6
        (super(Pulse, self).__init__)(a, color1=color1, color2=color2, channel2=channel2, **k)


class Blink(AnimatedColor):

    def __init__(self, color1=0, color2=0, speed=6, *a, **k):
        channel2 = [
         4,6,12,24,48].index(speed) + 11
        (super(Blink, self).__init__)(a, color1=color1, color2=color2, channel2=channel2, **k)


class TransparentColor(object):

    def draw(self, interface):
        pass


class Rgb(object):
    BLACK = RgbColor(0)
    DARK_GREY = RgbColor(1)
    GREY = RgbColor(2)
    WHITE = RgbColor(3)
    RED = RgbColor(5)
    AMBER = RgbColor(9)
    YELLOW = RgbColor(13)
    LIME = RgbColor(17)
    GREEN = RgbColor(21)
    SPRING = RgbColor(25)
    TURQUOISE = RgbColor(29)
    CYAN = RgbColor(33)
    SKY = RgbColor(37)
    OCEAN = RgbColor(41)
    BLUE = RgbColor(45)
    ORCHID = RgbColor(49)
    MAGENTA = RgbColor(53)
    PINK = RgbColor(57)


class Basic(object):
    HALF = FallbackColor(Rgb.DARK_GREY, 1)
    HALF_BLINK_SLOW = FallbackColor(Blink(Rgb.DARK_GREY, Rgb.BLACK, 4), 2)
    HALF_BLINK_FAST = FallbackColor(Blink(Rgb.DARK_GREY, Rgb.BLACK, 24), 3)
    FULL = FallbackColor(Rgb.WHITE, 4)
    FULL_BLINK_SLOW = FallbackColor(Blink(Rgb.WHITE, Rgb.BLACK, 4), 5)
    FULL_BLINK_FAST = FallbackColor(Blink(Rgb.WHITE, Rgb.BLACK, 24), 6)
    OFF = FallbackColor(Rgb.BLACK, 0)
    ON = FallbackColor(Rgb.WHITE, 127)
    TRANSPARENT = TransparentColor()


class BiLed(object):
    GREEN = FallbackColor(RgbColor(122), 22)
    GREEN_HALF = FallbackColor(RgbColor(123), 19)
    GREEN_BLINK_SLOW = FallbackColor(Blink(RgbColor(122), Rgb.BLACK, 4), 23)
    GREEN_BLINK_FAST = FallbackColor(Blink(RgbColor(122), Rgb.BLACK, 24), 24)
    RED = FallbackColor(RgbColor(120), 4)
    RED_HALF = FallbackColor(RgbColor(121), 1)
    RED_BLINK_SLOW = FallbackColor(Blink(RgbColor(120), Rgb.BLACK, 4), 5)
    RED_BLINK_FAST = FallbackColor(Blink(RgbColor(120), Rgb.BLACK, 24), 6)
    YELLOW = FallbackColor(RgbColor(124), 16)
    YELLOW_HALF = FallbackColor(RgbColor(125), 13)
    YELLOW_BLINK_SLOW = FallbackColor(Blink(RgbColor(124), Rgb.BLACK, 4), 17)
    YELLOW_BLINK_FAST = FallbackColor(Blink(RgbColor(124), Rgb.BLACK, 24), 18)
    AMBER = FallbackColor(RgbColor(126), 10)
    AMBER_HALF = FallbackColor(RgbColor(127), 7)
    AMBER_BLINK_SLOW = FallbackColor(Blink(RgbColor(126), Rgb.BLACK, 4), 11)
    AMBER_BLINK_FAST = FallbackColor(Blink(RgbColor(126), Rgb.BLACK, 24), 12)
    OFF = FallbackColor(Rgb.BLACK, 0)
    ON = FallbackColor(Rgb.WHITE, 127)


LIVE_COLORS_TO_MIDI_VALUES = {10927616:74, 
 16149507:84, 
 4047616:76, 
 6441901:69, 
 14402304:99, 
 8754719:19, 
 16725558:5, 
 3947580:71, 
 10056267:15, 
 8237133:18, 
 12026454:11, 
 12565097:73, 
 13381230:58, 
 12243060:111, 
 16249980:13, 
 13013643:4, 
 10208397:88, 
 695438:65, 
 13821080:110, 
 3101346:46, 
 16749734:107, 
 8962746:102, 
 5538020:79, 
 13684944:117, 
 15064289:119, 
 14183652:94, 
 11442405:44, 
 13408551:100, 
 1090798:78, 
 11096369:127, 
 16753961:96, 
 1769263:87, 
 5480241:64, 
 1698303:90, 
 16773172:97, 
 7491393:126, 
 8940772:80, 
 14837594:10, 
 8912743:16, 
 10060650:105, 
 13872497:14, 
 16753524:108, 
 8092539:70, 
 2319236:39, 
 1716118:47, 
 12349846:59, 
 11481907:121, 
 15029152:57, 
 2490280:25, 
 11119017:112, 
 10701741:81, 
 15597486:8, 
 49071:77, 
 10851765:93, 
 12558270:48, 
 32192:43, 
 8758722:103, 
 10204100:104, 
 11958214:55, 
 8623052:66, 
 16726484:95, 
 12581632:86, 
 13958625:28, 
 12173795:115, 
 13482980:116, 
 16777215:Rgb.WHITE, 
 6094824:33, 
 13496824:114, 
 9611263:92, 
 9160191:36}
RGB_COLOR_TABLE = ((0, 0), (1, 1973790), (2, 8355711), (3, 16777215), (4, 16731212),
                   (5, 16711680), (6, 5832704), (7, 1638400), (8, 16760172), (9, 16733184),
                   (10, 5840128), (11, 2562816), (12, 16777036), (13, 16776960),
                   (14, 5855488), (15, 1644800), (16, 8978252), (17, 5570304), (18, 1923328),
                   (19, 1321728), (20, 5046092), (21, 65280), (22, 22784), (23, 6400),
                   (24, 5046110), (25, 65305), (26, 22797), (27, 6402), (28, 5046152),
                   (29, 65365), (30, 22813), (31, 7954), (32, 5046199), (33, 65433),
                   (34, 22837), (35, 6418), (36, 5030911), (37, 43519), (38, 16722),
                   (39, 4121), (40, 5015807), (41, 22015), (42, 7513), (43, 2073),
                   (44, 5000447), (45, 255), (46, 89), (47, 25), (48, 8867071), (49, 5505279),
                   (50, 1638500), (51, 983088), (52, 16731391), (53, 16711935), (54, 5832793),
                   (55, 1638425), (56, 16731271), (57, 16711764), (58, 5832733),
                   (59, 2228243), (60, 16717056), (61, 10040576), (62, 7950592),
                   (63, 4416512), (64, 211200), (65, 22325), (66, 21631), (67, 255),
                   (68, 17743), (69, 2425036), (70, 8355711), (71, 2105376), (72, 16711680),
                   (73, 12451629), (74, 11529478), (75, 6618889), (76, 1084160),
                   (77, 65415), (78, 43519), (79, 11007), (80, 4129023), (81, 7995647),
                   (82, 11672189), (83, 4202752), (84, 16730624), (85, 8970502),
                   (86, 7536405), (87, 65280), (88, 3931942), (89, 5898097), (90, 3735500),
                   (91, 5999359), (92, 3232198), (93, 8880105), (94, 13835775), (95, 16711773),
                   (96, 16744192), (97, 12169216), (98, 9502464), (99, 8609031),
                   (100, 3746560), (101, 1330192), (102, 872504), (103, 1381674),
                   (104, 1450074), (105, 6896668), (106, 11010058), (107, 14569789),
                   (108, 14182940), (109, 16769318), (110, 10412335), (111, 6796559),
                   (112, 1973808), (113, 14483307), (114, 8454077), (115, 10131967),
                   (116, 9332479), (117, 4210752), (118, 7697781), (119, 14745599),
                   (120, 10485760), (121, 3473408), (122, 1757184), (123, 475648),
                   (124, 12169216), (125, 4141312), (126, 11755264), (127, 4920578))