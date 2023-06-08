from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from .colors import Basic, Rgb

class Colors:

    class DefaultButton:
        On = Basic.ON
        Off = Basic.OFF
        Disabled = Basic.OFF

    class Transport:
        PlayOn = Basic.ON
        PlayOff = Basic.OFF

    class Recording:
        On = Basic.ON
        Transition = Basic.ON
        Off = Basic.OFF

    class Mixer:
        ArmOn = Basic.ON
        ArmOff = Basic.OFF
        MuteOn = Basic.ON
        MuteOff = Basic.OFF
        SoloOn = Basic.ON
        SoloOff = Basic.OFF
        EmptyTrack = Basic.OFF

    class Session:
        ClipEmpty = Rgb.WHITE
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipStopped = Rgb.AMBER
        ClipStarted = Rgb.GREEN
        ClipRecording = Rgb.RED
        RecordButton = Basic.OFF
        Scene = Basic.OFF
        NoScene = Basic.OFF
        SceneTriggered = Basic.ON


skin = Skin(Colors)