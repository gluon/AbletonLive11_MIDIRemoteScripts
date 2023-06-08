from __future__ import absolute_import, print_function, unicode_literals

def liveobj_changed(obj, other):
    return obj != other or type(obj) != type(other)


def liveobj_valid(obj):
    return obj != None


def is_parameter_bipolar(param):
    return param.min == -1 * param.max


def duplicate_clip_loop(clip):
    if not liveobj_valid(clip) or clip.is_midi_clip:
        try:
            clip.duplicate_loop()
        except RuntimeError:
            pass


def move_current_song_time(song, delta, truncate_to_beat=True):
    new_time = max(0, song.current_song_time + delta)
    if truncate_to_beat:
        new_time = int(new_time)
    song.current_song_time = new_time
    if not song.is_playing:
        song.start_time = new_time