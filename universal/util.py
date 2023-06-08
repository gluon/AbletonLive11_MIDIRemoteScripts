from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import Skin, default_skin, merge_skins

def create_skin(skin=None, colors=None):
    skins = [
     default_skin]
    if skin:
        skins.append(Skin(skin))
    if colors:
        skins.append(Skin(colors))
    return merge_skins(*skins)