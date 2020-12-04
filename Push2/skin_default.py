#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/skin_default.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import SelectedClipColorFactory, SelectedTrackColorFactory
from pushbase.colors import Blink, FallbackColor, Pulse
from pushbase.skin_default import Colors as ColorsBase
from .colors import Basic, DISPLAY_BUTTON_SHADE_LEVEL, Rgb, SelectedDeviceChainColorFactory, SelectedDrumPadColorFactory, make_color_factory_func
make_selected_track_color = make_color_factory_func(SelectedTrackColorFactory)
make_selected_drum_pad_color = make_color_factory_func(SelectedDrumPadColorFactory)
make_selected_device_chain_color = make_color_factory_func(SelectedDeviceChainColorFactory)
make_selected_clip_color = make_color_factory_func(SelectedClipColorFactory)
TRACK_SOLOED_COLOR = Rgb.OCEAN
RECORDING_COLOR = Rgb.RED
CLIP_PLAYING_COLOR = Rgb.GREEN
UNLIT_COLOR = Rgb.BLACK
SELECTION_PULSE_SPEED = 48

class Colors(ColorsBase):

    class DefaultButton(object):
        On = Basic.ON
        Off = Basic.HALF
        Disabled = Basic.OFF
        Alert = Basic.FULL_PULSE_SLOW
        Transparent = Basic.TRANSPARENT

    class Instrument(object):
        NoteBase = make_selected_track_color()
        NoteScale = Rgb.WHITE
        NoteNotScale = Rgb.BLACK
        NoteInvalid = Rgb.BLACK
        Feedback = Rgb.GREEN
        FeedbackRecord = Rgb.RED
        NoteAction = Rgb.RED
        SelectedNote = make_selected_track_color(shade_level=2)

    class DrumGroup(object):
        PadSelected = Rgb.WHITE
        PadSelectedNotSoloed = Rgb.WHITE
        PadFilled = make_selected_track_color()
        PadEmpty = Rgb.DARK_GREY
        PadMuted = Rgb.LIGHT_GREY
        PadMutedSelected = Rgb.WHITE
        PadSoloed = Rgb.BLUE
        PadSoloedSelected = Rgb.WHITE
        PadInvisible = Rgb.BLACK
        PadAction = Rgb.WHITE
        PadHotswapping = Pulse(Rgb.WHITE, Rgb.LIGHT_GREY, 48)

    class SlicedSimpler(object):
        SliceSelected = Rgb.WHITE
        SliceUnselected = make_selected_track_color()
        NoSlice = make_selected_track_color(shade_level=2)

    class Melodic(object):
        Playhead = Rgb.GREEN
        PlayheadRecord = RECORDING_COLOR

    class LoopSelector(object):
        Playhead = Rgb.GREEN
        PlayheadRecord = RECORDING_COLOR
        SelectedPage = Rgb.WHITE
        InsideLoopStartBar = Rgb.LIGHT_GREY
        InsideLoop = Rgb.LIGHT_GREY
        OutsideLoop = Rgb.BLACK

    class VelocityLevels(object):
        LowLevel = Rgb.DARK_GREY
        MidLevel = Rgb.LIGHT_GREY
        HighLevel = Rgb.WHITE
        SelectedLevel = make_selected_track_color()

    class DrumGroupVelocityLevels(VelocityLevels):
        SelectedLevel = make_selected_drum_pad_color()

    class NoteEditor(object):

        class Step(object):
            Low = make_selected_clip_color(shade_level=2)
            High = make_selected_clip_color(shade_level=1)
            Full = make_selected_clip_color(shade_level=0)
            Muted = Rgb.LIGHT_GREY

        class StepEditing(object):
            Low = Pulse(Rgb.WHITE, Rgb.LIGHT_GREY, 48)
            High = Pulse(Rgb.WHITE, Rgb.LIGHT_GREY, 48)
            Full = Pulse(Rgb.WHITE, Rgb.LIGHT_GREY, 48)
            Muted = Rgb.WHITE

        StepSelected = Rgb.WHITE
        StepEmpty = Rgb.DARK_GREY
        StepDisabled = Rgb.BLACK
        Playhead = Rgb.GREEN
        PlayheadRecord = RECORDING_COLOR
        QuantizationSelected = Rgb.WHITE
        QuantizationUnselected = Rgb.DARK_GREY
        NoteBase = Rgb.LIGHT_GREY
        NoteScale = Rgb.DARK_GREY
        NoteNotScale = Rgb.BLACK
        NoteInvalid = Rgb.BLACK

    class DrumGroupNoteEditor(NoteEditor):

        class Step(object):
            Low = make_selected_drum_pad_color(shade_level=2)
            High = make_selected_drum_pad_color(shade_level=1)
            Full = make_selected_drum_pad_color(shade_level=0)
            Muted = Rgb.LIGHT_GREY

    class SlicingNoteEditor(NoteEditor):
        pass

    class Option(object):
        Selected = Rgb.WHITE
        Unselected = Rgb.DARK_GREY
        On = Rgb.WHITE
        Off = Rgb.DARK_GREY
        Unused = Rgb.BLACK

    class Mixer(object):
        TrackSelected = Rgb.WHITE
        NoTrack = Rgb.BLACK
        MutedTrack = Rgb.DARK_GREY
        FrozenChain = Rgb.DARK_GREY
        MuteOn = Rgb.YELLOW_SHADE
        MuteOff = Rgb.YELLOW
        SoloOn = TRACK_SOLOED_COLOR
        SoloOff = Rgb.DEEP_OCEAN
        LockedMuteMode = Pulse(Rgb.BLACK, Rgb.YELLOW, 48)
        LockedSoloMode = Pulse(Rgb.BLACK, TRACK_SOLOED_COLOR, 48)

    class MixerControlView(object):
        SectionSelected = Rgb.WHITE
        SectionUnSelected = Rgb.DARK_GREY

    class TrackControlView(object):
        ButtonOn = Rgb.WHITE
        ButtonOff = Rgb.DARK_GREY
        ButtonDisabled = Rgb.BLACK

    class MixOrRoutingChooser(object):
        ModeActive = Rgb.WHITE
        ModeInactive = make_selected_track_color(DISPLAY_BUTTON_SHADE_LEVEL)

    class ItemNavigation(object):
        ItemSelected = Rgb.WHITE
        NoItem = Rgb.BLACK
        ItemNotSelected = make_selected_track_color(DISPLAY_BUTTON_SHADE_LEVEL)

    class EditModeOptions(ItemNavigation):
        ItemNotSelected = make_selected_device_chain_color(DISPLAY_BUTTON_SHADE_LEVEL)

    class BankSelection(ItemNavigation):
        ItemNotSelected = make_selected_device_chain_color(DISPLAY_BUTTON_SHADE_LEVEL)

    class Browser(object):
        Navigation = FallbackColor(Rgb.WHITE, Basic.ON)
        NavigationDisabled = FallbackColor(Rgb.DARK_GREY, Basic.OFF)
        Option = Rgb.WHITE
        OptionDisabled = Rgb.DARK_GREY

    class Scales(object):
        Navigation = FallbackColor(Rgb.WHITE, Basic.ON)
        NavigationDisabled = FallbackColor(Rgb.DARK_GREY, Basic.OFF)
        OptionOn = Rgb.WHITE
        OptionOff = Rgb.DARK_GREY
        NoOption = Rgb.BLACK
        Close = Rgb.WHITE

    class Clip(object):
        Option = Rgb.WHITE
        OptionDisabled = Rgb.DARK_GREY
        Action = make_selected_clip_color()

    class Transport(object):
        PlayOn = Rgb.GREEN
        PlayOff = Rgb.WHITE

    class Recording(object):
        On = RECORDING_COLOR
        Off = Rgb.WHITE
        Transition = Blink(RECORDING_COLOR, Rgb.BLACK, 48)
        ArrangementRecordingOn = Pulse(RECORDING_COLOR, Rgb.BLACK, 48)
        FixedLengthRecordingOn = Rgb.WHITE
        FixedLengthRecordingOff = Rgb.DARK_GREY

    class Automation(object):
        On = Rgb.RED
        Off = Rgb.WHITE

    class Session(object):
        Scene = Rgb.GREEN
        SceneTriggered = FallbackColor(Blink(Rgb.GREEN, Rgb.BLACK, 24), 24)
        NoScene = Rgb.BLACK
        ClipStopped = Rgb.AMBER
        ClipTriggeredRecord = Blink(Rgb.RED, Rgb.BLACK, 24)
        ClipEmpty = Rgb.BLACK
        EmptySlotTriggeredPlay = Blink(Rgb.GREEN, Rgb.BLACK, 24)
        RecordButton = Rgb.RED_SHADE
        StopClip = Rgb.RED
        StopClipTriggered = Blink(Rgb.RED, Rgb.BLACK, 24)
        StoppedClip = Rgb.DARK_GREY

    class StopClips(object):
        SoloedTrack = Pulse(Rgb.BLACK, TRACK_SOLOED_COLOR, 48)
        MutedTrack = Pulse(Rgb.BLACK, Rgb.DARK_GREY, 48)
        LockedStopMode = Pulse(Rgb.BLACK, Rgb.RED, 48)

    class Zooming(object):
        Selected = Rgb.WHITE
        Stopped = Rgb.LIGHT_GREY
        Playing = Pulse(Rgb.GREEN_SHADE, Rgb.GREEN, 48)
        Empty = Rgb.BLACK

    class NoteRepeat(object):
        RateSelected = Rgb.GREEN
        RateUnselected = Rgb.WHITE

    class Metronome(object):
        On = Basic.FAST_PULSE
        Off = Basic.ON

    class FixedLength(object):
        On = Basic.FULL_PULSE_SLOW
        Off = Basic.ON
        PhraseAlignedOn = Rgb.WHITE
        PhraseAlignedOff = Rgb.DARK_GREY

    class Accent(object):
        On = Basic.FULL_PULSE_SLOW
        Off = Basic.ON


def make_default_skin():
    return Skin(Colors)
