#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Oxygen_Pro/skin.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import Color
LED_ON = Color(127)
LED_OFF = Color(0)

class Colors:

    class DefaultButton:
        On = LED_ON
        Off = LED_OFF
        Disabled = LED_OFF

    class Transport:
        PlayOn = LED_ON
        PlayOff = LED_OFF

    class Recording:
        On = LED_ON
        Transition = LED_ON
        Off = LED_OFF

    class Mixer:
        ArmOn = LED_ON
        ArmOff = LED_OFF

    class Session:
        ClipEmpty = LED_OFF
        ClipTriggeredPlay = LED_ON
        ClipTriggeredRecord = LED_ON
        ClipStopped = LED_ON
        ClipStarted = LED_ON
        ClipRecording = LED_ON
        RecordButton = LED_ON
        Scene = LED_OFF
        NoScene = LED_OFF
        SceneTriggered = LED_ON


skin = Skin(Colors)
