# Avoid using tabs for indentation, use spaces.
# Don't use floats, they might break things.


# Combination Mode offsets
# ------------------------

TRACK_OFFSET = -1  # offset from the left of linked session origin; set to -1 for auto-joining of multiple instances
SCENE_OFFSET = 0  # offset from the top of linked session origin (no auto-join)

# Buttons / Pads
# -------------
# Valid Note/CC assignments are 0 to 127, or -1 for NONE
# Duplicate assignments are permitted

BUTTONCHANNEL = 0  # Channel assignment for all mapped buttons/pads; valid range is 0 to 15 ; 0=1, 1=2 etc.
MESSAGETYPE = 0  # Message type for buttons/pads; set to 0 for MIDI Notes, 1 for CCs.
# When using CCs for buttons/pads, set BUTTONCHANNEL and SLIDERCHANNEL to different values.


# Track selection box (aka that coloured box for scene/track launching)
TSB_X = 8   # Controls the horizontal value for the track selection box. Default value is 8
TSB_Y = 8   # Controls the horizontal value for the track selection box. Default value is 8

# General
PLAY = -1   # Global play
STOP = -1   # Global stop
REC = -1    # Global record
TAPTEMPO = -1   # Tap tempo
NUDGEUP = -1    # Tempo Nudge Up
NUDGEDOWN = -1  # Tempo Nudge Down
UNDO = -1   # Undo
REDO = -1   # Redo
LOOP = -1   # Loop on/off
PUNCHIN = -1    # Punch in
PUNCHOUT = -1   # Punch out
OVERDUB = -1     # Overdub on/off
METRONOME = -1   # Metronome on/off
RECQUANT = -1   # Record quantization on/off
DETAILVIEW = -1   # Detail view switch
CLIPTRACKVIEW = -1  # Clip/Track view switch

# Device Control
DEVICELOCK = -1  # Device Lock (lock "blue hand")
DEVICEONOFF = -1  # Device on/off
DEVICENAVLEFT = -1  # Device nav left
DEVICENAVRIGHT = -1  # Device nav right
DEVICEBANKNAVLEFT = -1  # Device bank nav left
DEVICEBANKNAVRIGHT = -1  # Device bank nav right
DEVICEBANK = (-1,  # Bank 1 #All 8 banks must be assigned to positive values in order for bank selection to work
              -1,  # Bank 2
              -1,  # Bank 3
              -1,  # Bank 4
              -1,  # Bank 5
              -1,  # Bank 6
              -1,  # Bank 7
              -1,  # Bank 8
              )

# Arrangement View Controls
SEEKFWD = -1  # Seek forward
SEEKRWD = -1  # Seek rewind

# Session Navigation (aka "red box")
SESSIONLEFT = -1  # Session left
SESSIONRIGHT = -1  # Session right
SESSIONUP = -1  # Session up
SESSIONDOWN = -1  # Session down
ZOOMUP = -1  # Session Zoom up
ZOOMDOWN = -1  # Session Zoom down
ZOOMLEFT = -1  # Session Zoom left
ZOOMRIGHT = -1  # Session Zoom right

# Track Navigation
TRACKLEFT = -1  # Track left
TRACKRIGHT = -1  # Track right

# Scene Navigation
SCENEUP = -1  # Scene down
SCENEDN = -1  # Scene up

# Scene Launch
SELSCENELAUNCH = -1  # Selected scene launch
SCENELAUNCH = (-1,  # Scene 1 Launch
               -1,  # Scene 2
               -1,  # Scene 3
               -1,  # Scene 4
               -1,  # Scene 5
               -1,  # Scene 6
               -1,  # Scene 7
               -1,  # Scene 8
               )

# Clip Launch / Stop
SELCLIPLAUNCH = -1  # Selected clip launch
STOPALLCLIPS = -1  # Stop all clips

# 8x8 Matrix note assignments
# Track no.:     1   2   3   4   5   6   7   8
CLIPNOTEMAP = ((-1, -1, -1, -1, -1, -1, -1, -1),  # Row 1
               (-1, -1, -1, -1, -1, -1, -1, -1),  # Row 2
               (-1, -1, -1, -1, -1, -1, -1, -1),  # Row 3
               (-1, -1, -1, -1, -1, -1, -1, -1),  # Row 4
               (-1, -1, -1, -1, -1, -1, -1, -1),  # Row 5
               (-1, -1, -1, -1, -1, -1, -1, -1),  # Row 6
               (-1, -1, -1, -1, -1, -1, -1, -1),  # Row 7
               (-1, -1, -1, -1, -1, -1, -1, -1),  # Row 8
               )

# Track Control
MASTERSEL = -1      # Master track select
SELTRACKREC = -1    # Arm Selected Track
SELTRACKSOLO = -1   # Solo Selected Track
SELTRACKMUTE = -1   # Mute Selected Track

TRACKSTOP = (-1,  # Track 1 Clip Stop
             -1,  # Track 2
             -1,  # Track 3
             -1,  # Track 4
             -1,  # Track 5
             -1,  # Track 6
             -1,  # Track 7
             -1,  # Track 8
             )

TRACKSEL = (-1,  # Track 1 Select
            -1,  # Track 2
            -1,  # Track 3
            -1,  # Track 4
            -1,  # Track 5
            -1,  # Track 6
            -1,  # Track 7
            -1,  # Track 8
            )

TRACKMUTE = (-1,  # Track 1 On/Off
             -1,  # Track 2
             -1,  # Track 3
             -1,  # Track 4
             -1,  # Track 5
             -1,  # Track 6
             -1,  # Track 7
             -1,  # Track 8
             )

TRACKSOLO = (-1,  # Track 1 Solo
             -1,  # Track 2
             -1,  # Track 3
             -1,  # Track 4
             -1,  # Track 5
             -1,  # Track 6
             -1,  # Track 7
             -1,  # Track 8
             )

TRACKREC = (-1,  # Track 1 Record
            -1,  # Track 2
            -1,  # Track 3
            -1,  # Track 4
            -1,  # Track 5
            -1,  # Track 6
            -1,  # Track 7
            -1,  # Track 8
            )


# Pad Translations for Drum Rack
PADCHANNEL = 0  # MIDI channel for Drum Rack notes
DRUM_PADS = (-1, -1, -1, -1,  # MIDI note numbers for 4 x 4 Drum Rack
             -1, -1, -1, -1,  # Mapping will be disabled if any notes are set to -1
             -1, -1, -1, -1,  # Notes will be "swallowed" if already mapped elsewhere
             -1, -1, -1, -1,
             )


# Sliders / Knobs
# ---------------
# Valid CC assignments are 0 to 127, or -1 for NONE
# Duplicate assignments will be ignored
SLIDERCHANNEL = 0  # Channel assignment for all mapped CCs; valid range is 0 to 15
TEMPO_TOP = 180.0  # Upper limit of tempo control in BPM (max is 999)
TEMPO_BOTTOM = 100.0  # Lower limit of tempo control in BPM (min is 0)

TEMPOCONTROL = -1  # Tempo control CC assignment; control range is set above
MASTERVOLUME = -1  # Master track volume
CUELEVEL = -1  # Cue level control
CROSSFADER = -1  # Crossfader control

TRACKVOL = (-1,  # Track 1 Volume
            -1,  # Track 2
            -1,  # Track 3
            -1,  # Track 4
            -1,  # Track 5
            -1,  # Track 6
            -1,  # Track 7
            -1,  # Track 8
            )

TRACKPAN = (-1,  # Track 1 Pan
            -1,  # Track 2
            -1,  # Track 3
            -1,  # Track 4
            -1,  # Track 5
            -1,  # Track 6
            -1,  # Track 7
            -1,  # Track 8
            )

TRACKSENDA = (-1,  # Track 1 Send A
              -1,  # Track 2
              -1,  # Track 3
              -1,  # Track 4
              -1,  # Track 5
              -1,  # Track 6
              -1,  # Track 7
              -1,  # Track 8
              )

TRACKSENDB = (-1,  # Track 1 Send B
              -1,  # Track 2
              -1,  # Track 3
              -1,  # Track 4
              -1,  # Track 5
              -1,  # Track 6
              -1,  # Track 7
              -1,  # Track 8
              )

TRACKSENDC = (-1,  # Track 1 Send C
              -1,  # Track 2
              -1,  # Track 3
              -1,  # Track 4
              -1,  # Track 5
              -1,  # Track 6
              -1,  # Track 7
              -1,  # Track 8
              )

PARAMCONTROL = (-1,  # Param 1 #All 8 params must be assigned to positive values in order for param control to work
                -1,  # Param 2
                -1,  # Param 3
                -1,  # Param 4
                -1,  # Param 5
                -1,  # Param 6
                -1,  # Param 7
                -1,  # Param 8
                )


