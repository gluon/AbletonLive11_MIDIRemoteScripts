# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK2\Skin.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1560 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
import _Framework.Skin as Skin
from .Colors import Rgb

class Colors(object):

    class Session(object):
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.BLACK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipEmpty = Rgb.BLACK
        RecordButton = Rgb.RED_HALF
        StopClip = Rgb.GREEN
        StopClipTriggered = Rgb.GREEN_BLINK
        StoppedClip = Rgb.GREEN_HALF
        Enabled = Rgb.YELLOW

    class Mode(object):
        DeviceMode = Rgb.PURPLE_HALF
        DeviceModeOn = Rgb.PURPLE
        PanMode = Rgb.ORANGE_HALF
        PanModeOn = Rgb.ORANGE
        Send0Mode = Rgb.DARK_BLUE_HALF
        Send0ModeOn = Rgb.BRIGHT_PURPLE
        Send1Mode = Rgb.BLUE_HALF
        Send1ModeOn = Rgb.BLUE
        Send2Mode = Rgb.LIGHT_BLUE_HALF
        Send2ModeOn = Rgb.LIGHT_BLUE
        Send3Mode = Rgb.MINT_HALF
        Send3ModeOn = Rgb.MINT
        Send4Mode = Rgb.DARK_YELLOW_HALF
        Send4ModeOn = Rgb.DARK_YELLOW
        Send5Mode = Rgb.YELLOW_HALF
        Send5ModeOn = Rgb.YELLOW
        Disabled = Rgb.BLACK

    class Device(object):
        Bank = Rgb.DARK_PURPLE
        BestOfBank = Rgb.PURPLE_HALF
        BankSelected = Rgb.PURPLE


def make_skin():
    return Skin(Colors)