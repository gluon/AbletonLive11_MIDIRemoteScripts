<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/default_skin.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 6117 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from .colors import BasicColors
from .skin import Skin

<<<<<<< HEAD
class DefaultColors:
=======
class DefaultSkin:
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    class DefaultButton:
        On = BasicColors.ON
        Off = BasicColors.OFF
        Disabled = BasicColors.OFF

    class TargetTrack:
        LockOn = BasicColors.ON
        LockOff = BasicColors.OFF

    class Transport:
        PlayOn = BasicColors.ON
        PlayOff = BasicColors.OFF
        ContinueOn = BasicColors.ON
        ContinueOff = BasicColors.OFF
        StopOn = BasicColors.ON
        StopOff = BasicColors.OFF
        ArrangementRecordingOn = BasicColors.ON
        ArrangementRecordingOff = BasicColors.OFF
<<<<<<< HEAD
        SessionRecordingOn = BasicColors.ON
        SessionRecordingTransition = BasicColors.ON
        SessionRecordingOff = BasicColors.OFF
        OverdubOn = BasicColors.ON
        OverdubOff = BasicColors.OFF
        AutomationArmOn = BasicColors.ON
        AutomationArmOff = BasicColors.OFF
=======
        OverdubOn = BasicColors.ON
        OverdubOff = BasicColors.OFF
        CaptureOn = BasicColors.ON
        CaptureOff = BasicColors.OFF
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        LoopOn = BasicColors.ON
        LoopOff = BasicColors.OFF
        MetronomeOn = BasicColors.ON
        MetronomeOff = BasicColors.OFF
        PunchOn = BasicColors.ON
        PunchOff = BasicColors.OFF
        TapTempoPressed = BasicColors.ON
        TapTempo = BasicColors.OFF
        NudgePressed = BasicColors.ON
        Nudge = BasicColors.OFF
        SeekPressed = BasicColors.ON
        Seek = BasicColors.OFF
<<<<<<< HEAD
        CanReEnableAutomation = BasicColors.ON
        CanCaptureMidi = BasicColors.ON
=======
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        CanJumpToCue = BasicColors.ON
        CannotJumpToCue = BasicColors.OFF
        SetCuePressed = BasicColors.ON
        SetCue = BasicColors.OFF

<<<<<<< HEAD
=======
    class Recording:
        On = BasicColors.ON
        Transition = BasicColors.ON
        Off = BasicColors.OFF

    class Automation:
        On = BasicColors.ON
        Off = BasicColors.OFF

>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    class UndoRedo:
        UndoPressed = BasicColors.ON
        Undo = BasicColors.OFF
        RedoPressed = BasicColors.ON
        Redo = BasicColors.OFF

    class ViewControl:
        TrackPressed = BasicColors.ON
        Track = BasicColors.ON
        ScenePressed = BasicColors.ON
        Scene = BasicColors.ON

    class ViewToggle:
        SessionOn = BasicColors.ON
        SessionOff = BasicColors.OFF
        DetailOn = BasicColors.ON
        DetailOff = BasicColors.OFF
        ClipOn = BasicColors.ON
        ClipOff = BasicColors.OFF
        BrowserOn = BasicColors.ON
        BrowserOff = BasicColors.OFF

    class Mixer:
        ArmOn = BasicColors.ON
        ArmOff = BasicColors.OFF
<<<<<<< HEAD
        ImplicitArmOn = BasicColors.ON
=======
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        MuteOn = BasicColors.ON
        MuteOff = BasicColors.OFF
        SoloOn = BasicColors.ON
        SoloOff = BasicColors.OFF
        Selected = BasicColors.ON
        NotSelected = BasicColors.OFF
        CrossfadeA = BasicColors.ON
        CrossfadeB = BasicColors.ON
        CrossfadeOff = BasicColors.OFF
<<<<<<< HEAD
        CycleSendIndexPressed = BasicColors.OFF
        CycleSendIndex = BasicColors.ON
        CycleSendIndexDisabled = BasicColors.OFF
        NoTrack = BasicColors.OFF

    class Session:
        Slot = BasicColors.OFF
        SlotRecordButton = BasicColors.OFF
        NoSlot = BasicColors.OFF
        ClipStopped = BasicColors.OFF
        ClipTriggeredPlay = BasicColors.ON
        ClipTriggeredRecord = BasicColors.ON
        ClipPlaying = BasicColors.ON
        ClipRecording = BasicColors.ON
        Scene = BasicColors.OFF
        SceneTriggered = BasicColors.ON
        NoScene = BasicColors.OFF
=======
        Empty = BasicColors.OFF
        CycleSendIndexPressed = BasicColors.OFF
        CycleSendIndex = BasicColors.ON
        CycleSendIndexDisabled = BasicColors.OFF

    class Session:
        ClipEmpty = BasicColors.OFF
        ClipStopped = BasicColors.OFF
        ClipTriggeredPlay = BasicColors.ON
        ClipTriggeredRecord = BasicColors.ON
        ClipStarted = BasicColors.ON
        ClipRecording = BasicColors.ON
        ClipRecordButton = BasicColors.OFF
        Scene = BasicColors.OFF
        SceneEmpty = BasicColors.OFF
        SceneTriggered = BasicColors.ON
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        StopClipTriggered = BasicColors.ON
        StopClip = BasicColors.OFF
        StopClipDisabled = BasicColors.OFF
        StopAllClipsPressed = BasicColors.ON
        StopAllClips = BasicColors.OFF
        NavigationPressed = BasicColors.ON
        Navigation = BasicColors.ON

    class Zooming:
        Selected = BasicColors.OFF
        Stopped = BasicColors.ON
        Playing = BasicColors.ON
        Empty = BasicColors.OFF

<<<<<<< HEAD
    class ClipActions:
        Delete = BasicColors.OFF
        DeletePressed = BasicColors.ON
        Double = BasicColors.OFF
        DoublePressed = BasicColors.ON
        Quantize = BasicColors.OFF
        QuantizedPressed = BasicColors.ON

=======
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
    class Device:
        On = BasicColors.ON
        Off = BasicColors.OFF
        LockOn = BasicColors.ON
        LockOff = BasicColors.OFF
        NavigationPressed = BasicColors.ON
        Navigation = BasicColors.OFF

        class Bank:
            Selected = BasicColors.ON
            NotSelected = BasicColors.OFF
            NavigationPressed = BasicColors.ON
            Navigation = BasicColors.ON

    class Accent:
        On = BasicColors.ON
        Off = BasicColors.OFF

    class DrumGroup:
        PadEmpty = BasicColors.OFF
        PadFilled = BasicColors.OFF
        PadSelected = BasicColors.ON
        PadMuted = BasicColors.ON
        PadMutedSelected = BasicColors.ON
        PadSoloed = BasicColors.ON
        PadSoloedSelected = BasicColors.ON
<<<<<<< HEAD
        PadAction = BasicColors.ON
        ScrollPressed = BasicColors.ON
        Scroll = BasicColors.ON

    class SlicedSimpler:
        NoSlice = BasicColors.OFF
        SliceNotSelected = BasicColors.OFF
        SliceSelected = BasicColors.ON
        NextSlice = BasicColors.ON
        PadAction = BasicColors.ON
        ScrollPressed = BasicColors.ON
        Scroll = BasicColors.ON

    class Translation:

        class Channel:
            Selected = BasicColors.ON
            NotSelected = BasicColors.OFF


default_skin = Skin(DefaultColors)
=======
        MutePressed = BasicColors.ON
        Mute = BasicColors.OFF
        SoloPressed = BasicColors.ON
        Solo = BasicColors.OFF
        ScrollPressed = BasicColors.ON
        Scroll = BasicColors.ON


default_skin = Skin(DefaultSkin)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
