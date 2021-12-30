# Ableton Live Custom MIDI Remote Scripts

Scripts for creating custom MIDI Remote Scripts for Ableton Live.
Known to be working on Live 9 and 10, untested in 11.

---
### Background
This is an [in-depth tutorial](https://youtu.be/IgKwcCJsoz4) on how to use these scripts. 
When I made the video 5 years ago, I had next to no programming knowledge, and I created it with the intent 
that non-programmers would be able to make their own MIDI scripts to interface with Live. 30k views later... it probably
deserves an update. The video has more details about what to modify to get things working, but I'll add more comments
to the code as I figure out what each function does.

- Most of the code is from these [Behringer FCB1020 scripts](http://remotescripts.blogspot.com) by Hanz Petrov, if I 
  can find their git or another source to credit them appropriately then I will do so. Let me know here if the site is gone, I have archived it for
  posterity.
- For the Push 2, user [jzgdev](https://github.com/jzgdev/Push2UserModeScript) has a working Push 2 User Mode.
- [More information](https://structure-void.com/ableton-live-midi-remote-scripts/) on MIDI remote scripts, the Live API 
  documentation, Push scripts, and [decompiled scripts](https://github.com/gluon) for more current versions of Live by 
  Julien Bayle.

---
### Instructions

- Connect your MIDI device to your computer
- Open Live and navigate to `Preferences → Link MIDI → MIDI`
- Under either the Input or Output press the dropdown menu, note the exact name of your controller (if spaces are present in name, use underscores (e.g. "Arturia_Beatstep" 
  instead of "Arturia Beatstep").
- Close Live.
- Find and replace all instances in the scripts of `YourControllerName` folder with your controller's name.
  - There are three in `__init__.py`
  - and nine in `YourControllerName.py`
- Save everything
- Rename the YourControllerName folder and the `YourControllerName.py` with the same name.
- Open `MIDI_Map.py` and inspect what you want to control. Unless stated otherwise, `-1` is the idle/unused value for 
  each parameter. 
- You can use a third-party tool (see: [Downloads](#downloads)), or your device's user manual to figure out what MIDI
  channel, note or CC values each control on your device sends.
  I'd do this with pen and paper or [draw.io](https://draw.io).
- Once you know your layout, assign the values to the respective parameter in `MIDI_Map.py` and ensure you set 
`BUTTONCHANNEL` and `SLIDERCHANNEL` to the same MIDI channel as your buttons and pots/faders. 
- <b>Important</b>: you must use the value for decimal number when assigning MIDI notes/buttons, <u><b>DO NOT</u></b> 
  use note values like these C3, D4, A1 etc., they won't work. There are tables to work it out from the note, but the
  software is much more efficient and accurate.
- Save and close everything and make a backup of your edited version, Live 9 compiles your scripts on launch, so you
  won't be able to make edits after it has done that. You've been warned. Don't let that effort be for nothing.

MIDI Remote Scripts folder:
  - For Windows users: `\ProgramData\Ableton\Live x.x\Resources\MIDI Remote Scripts\`
  - For macOS users:
    - Locate the Live application in Finder (typically `/Applications/`), 
    - right click on it and select "Show Package Contents" in the context menu,
    - navigate to: `/Contents/App-Resources/MIDI Remote Scripts/`
- If you have multiple versions of Live installed, you will have to copy your scripts to each version individually.
- If you are replacing a pre-existing script with the same device name then make a copy of the original. 
  Otherwise, you will have to reinstall Live to get the default scripts back.
- Launch Live and head back to `Preferences → Link MIDI → MIDI`
- Under the `Control Surface` section, choose an empty slot and assign your newly created script.
- Set the Input and Output to your MIDI device.
- Under `MIDI Ports` check that `Remote` and `Track' are set to `On` for both the Input and the Output, or to 
your preference if you know what you're doing.
- Test it out.
- There is going to be a lot of trial and error here but it's pretty straightforward once you get an input working.   


---
### Troubleshooting:
- Make sure `YourControllerName` is changed everywhere, and you saved the script before placing it in the 
  `MIDI Remote Scripts` directory.
- Set the `BUTTONCHANNEL` and the `SLIDERCHANNEL` correctly. It won't work until you do that.
- If you have multiple versions of Live installed, you will have to copy your scripts to each version individually.
- Assign one control message (CC/Note) per parameter.
- Before you add to `MIDI Remote Scripts` folder just make sure you have the correct MIDI channels and renamed 
  YourControllerName in `__init__.py` and `YourControllerName.py`. Don't forget to change the folder and the file names
  as well.


---
### Updates
- Change the size of the track selection box (coloured box in Session view).
  - There are now two variables in MIDI_Map.py to modify the size of the box:
    - `TSB_X` is the horizontal count i.e. the number of tracks
    - `TSB_Y` is the vertical count which represents the number of scenes you want to control.
  - For this to work properly you must manually add or remove rows/columns for `SCENELAUNCH` and `CLIPNOTEMAP` 
  sections in [MIDI_Map.py](https://github.com/laidlaw42/Ableton-Live-MIDI-Remote-Scripts/blob/YourControllerName/YourControllerName/MIDI_Map.py).


---
### Downloads
- [MIDI Manager](https://www.snoize.com/midimonitor/) for macOS (preferred).
- [MIDI Tools](https://mountainutilities.eu/miditools) for Windows and macOS.
- [BCRManager](http://mountainutilities.eu/bcmanager) a GUI software solution for editing the Behringer BCR2000. 
- [Atom](https://atom.io) the code editor I mention in the video.
- [PyCharm](https://www.jetbrains.com/pycharm/) probably a better editor to use if you're going to get into Python.
