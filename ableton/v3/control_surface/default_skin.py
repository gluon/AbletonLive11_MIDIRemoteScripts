from __future__ import absolute_import, print_function, unicode_literals
from .colors import BasicColors
from .skin import Skin

class DefaultColors:

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
        SessionRecordingOn = BasicColors.ON
        SessionRecordingTransition = BasicColors.ON
        SessionRecordingOff = BasicColors.OFF
        OverdubOn = BasicColors.ON
        OverdubOff = BasicColors.OFF
        AutomationArmOn = BasicColors.ON
        AutomationArmOff = BasicColors.OFF
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
        CanReEnableAutomation = BasicColors.ON
        CanCaptureMidi = BasicColors.ON
        CanJumpToCue = BasicColors.ON
        CannotJumpToCue = BasicColors.OFF
        SetCuePressed = BasicColors.ON
        SetCue = BasicColors.OFF

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
        ImplicitArmOn = BasicColors.ON
        MuteOn = BasicColors.ON
        MuteOff = BasicColors.OFF
        SoloOn = BasicColors.ON
        SoloOff = BasicColors.OFF
        Selected = BasicColors.ON
        NotSelected = BasicColors.OFF
        CrossfadeA = BasicColors.ON
        CrossfadeB = BasicColors.ON
        CrossfadeOff = BasicColors.OFF
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

    class ClipActions:
        Delete = BasicColors.OFF
        DeletePressed = BasicColors.ON
        Double = BasicColors.OFF
        DoublePressed = BasicColors.ON
        Quantize = BasicColors.OFF
        QuantizedPressed = BasicColors.ON

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