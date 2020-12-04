#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/skin_default.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.control_surface import Skin
from .colors import Basic, Rgb, Pulse, Blink, BiLed

class Colors(object):

    class Option(object):
        Selected = BiLed.AMBER
        Unselected = BiLed.YELLOW_HALF
        On = BiLed.YELLOW
        Off = BiLed.OFF
        Unused = BiLed.OFF

    class List(object):
        ScrollerOn = BiLed.AMBER
        ScrollerOff = BiLed.AMBER_HALF

    class DefaultButton(object):
        On = Basic.FULL
        Off = Basic.HALF
        Disabled = Basic.OFF
        Alert = Basic.FULL_BLINK_SLOW
        Transparent = Basic.TRANSPARENT

    class DefaultMatrix(object):
        On = Rgb.WHITE
        Off = Rgb.BLACK

    class Scales(object):
        Selected = BiLed.YELLOW
        Unselected = BiLed.GREEN_HALF
        FixedOn = BiLed.AMBER
        FixedOff = BiLed.YELLOW_HALF
        Diatonic = BiLed.AMBER
        Chromatic = BiLed.YELLOW_HALF

    class Instrument(object):
        NoteBase = Rgb.OCEAN
        NoteScale = Rgb.WHITE
        NoteNotScale = Rgb.BLACK
        NoteInvalid = Rgb.BLACK
        Feedback = Rgb.GREEN
        FeedbackRecord = Rgb.RED.shade(1)
        NoteAction = Rgb.RED
        SelectedNote = Rgb.TURQUOISE

    class Recording(object):
        On = Basic.FULL
        Off = Basic.HALF
        Transition = Basic.FULL_BLINK_FAST
        ArrangementRecordingOn = Basic.FULL_BLINK_SLOW
        FixedLengthRecordingOn = BiLed.YELLOW
        FixedLengthRecordingOff = BiLed.OFF

    class Automation(object):
        On = Basic.FULL
        Off = Basic.HALF

    class Session(object):
        Scene = BiLed.GREEN
        SceneTriggered = BiLed.GREEN_BLINK_FAST
        NoScene = BiLed.OFF
        ClipStopped = Rgb.AMBER
        ClipStarted = Pulse(Rgb.GREEN.shade(1), Rgb.GREEN, 48)
        ClipRecording = Pulse(Rgb.BLACK, Rgb.RED, 48)
        ClipTriggeredPlay = Blink(Rgb.GREEN, Rgb.BLACK, 24)
        ClipTriggeredRecord = Blink(Rgb.RED, Rgb.BLACK, 24)
        ClipEmpty = Rgb.BLACK
        RecordButton = Rgb.RED.shade(2)
        StopClip = Rgb.RED
        StopClipTriggered = Blink(Rgb.RED, Rgb.BLACK, 24)
        StoppedClip = Rgb.DARK_GREY

    class Zooming(object):
        Selected = Rgb.AMBER
        Stopped = Rgb.RED
        Playing = Rgb.GREEN
        Empty = Rgb.BLACK

    class TrackState(object):
        Common = Rgb.BLACK
        Stopped = Rgb.RED
        Disabled = Basic.OFF

    class DrumGroup(object):
        PadSelected = Rgb.OCEAN
        PadSelectedNotSoloed = Rgb.OCEAN
        PadFilled = Rgb.YELLOW
        PadEmpty = Rgb.YELLOW.shade(2)
        PadMuted = Rgb.AMBER.shade(1)
        PadMutedSelected = Rgb.OCEAN.shade(1)
        PadSoloed = Rgb.BLUE
        PadSoloedSelected = Rgb.OCEAN.highlight()
        PadInvisible = Rgb.BLACK
        PadAction = Rgb.RED

    class SlicedSimpler(object):
        SliceSelected = Rgb.OCEAN
        SliceUnselected = Rgb.YELLOW
        NoSlice = Rgb.YELLOW.shade(2)
        NextSlice = Pulse(Rgb.YELLOW.shade(2), Rgb.OCEAN.highlight(), 48)

    class LoopSelector(object):
        Playhead = Rgb.GREEN
        PlayheadRecord = Rgb.RED
        SelectedPage = Rgb.YELLOW.highlight()
        InsideLoopStartBar = Rgb.WHITE
        InsideLoop = Rgb.WHITE
        OutsideLoop = Rgb.BLACK

    class VelocityLevels(object):
        LowLevel = Rgb.DARK_GREY
        MidLevel = Rgb.GREY
        HighLevel = Rgb.WHITE
        SelectedLevel = Rgb.OCEAN

    class NoteEditor(object):

        class Step(object):
            Low = Rgb.SKY.highlight()
            High = Rgb.OCEAN
            Full = Rgb.BLUE
            Muted = Rgb.AMBER.shade(2)

        class StepEditing(object):
            Low = Rgb.YELLOW.highlight()
            High = Rgb.YELLOW
            Full = Rgb.AMBER
            Muted = Rgb.WHITE

        StepSelected = Rgb.WHITE
        StepEmpty = Rgb.BLACK
        StepDisabled = Rgb.RED.shade(2)
        Playhead = Rgb.GREEN
        PlayheadRecord = Rgb.RED
        QuantizationSelected = BiLed.GREEN
        QuantizationUnselected = BiLed.YELLOW
        NoteBase = Rgb.OCEAN.shade(2)
        NoteScale = Rgb.DARK_GREY
        NoteNotScale = Rgb.BLACK
        NoteInvalid = Rgb.RED.shade(2)

    class Melodic(object):
        Playhead = Rgb.GREEN.shade(1)
        PlayheadRecord = Rgb.RED.shade(1)

    class NoteRepeat(object):
        RateSelected = BiLed.RED
        RateUnselected = BiLed.YELLOW

    class Mixer(object):
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.DARK_GREY
        MuteOn = Rgb.DARK_GREY
        MuteOff = BiLed.YELLOW
        ArmSelected = BiLed.RED
        ArmUnselected = BiLed.RED_HALF

    class Browser(object):
        Load = BiLed.GREEN
        LoadNext = BiLed.YELLOW
        LoadNotPossible = BiLed.OFF
        Loading = BiLed.OFF
        Prehear = Rgb.BLUE
        PrehearOff = Rgb.WHITE

    class MessageBox(object):
        Cancel = BiLed.GREEN

    class Transport(object):
        PlayOn = Basic.FULL
        PlayOff = Basic.HALF

    class Metronome(object):
        On = Basic.FULL_BLINK_SLOW
        Off = Basic.FULL

    class FixedLength(object):
        On = Basic.FULL
        Off = Basic.HALF
        PhraseAlignedOn = BiLed.AMBER
        PhraseAlignedOff = BiLed.YELLOW_HALF

    class Accent(object):
        On = Basic.FULL
        Off = Basic.HALF


def make_default_skin():
    return Skin(Colors)
