#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/visualisation_settings.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from past.utils import old_div
from builtins import object
import math
from .colors import COLOR_INDEX_TO_SCREEN_COLOR, COLOR_INDEX_TO_SCREEN_COLOR_SHADES

class VisualisationSettings(object):
    base_colors = COLOR_INDEX_TO_SCREEN_COLOR
    shade1_colors = COLOR_INDEX_TO_SCREEN_COLOR_SHADES[0]
    shade2_colors = COLOR_INDEX_TO_SCREEN_COLOR_SHADES[1]
    shade3_colors = COLOR_INDEX_TO_SCREEN_COLOR_SHADES[2]
    shade4_colors = COLOR_INDEX_TO_SCREEN_COLOR_SHADES[3]
    shade5_colors = COLOR_INDEX_TO_SCREEN_COLOR_SHADES[4]
    button_left = 4
    light_left = 14
    light_right = 100
    button_right = 110
    row_top = 1
    body_top = 5
    body_bottom = 15
    row_bottom = 19
    button_spacing = 121
    row_spacing = 20
    body_height = body_bottom - body_top
    body_margin = body_top - row_top
    button_light_margin = light_left - button_left
    button_gap = button_spacing - (button_right - button_left)
    row_height = row_bottom - row_top
    row_gap = row_spacing - row_height
    screen_width = 960
    screen_height = 160
    visualisation_left = button_left
    visualisation_top = row_spacing * 3 + row_top


class VisualisationGuides(object):

    @staticmethod
    def _guide_x(index, origin_x, guide_type):
        if origin_x == None:
            origin_x = VisualisationSettings.visualisation_left
        origin_column = int(math.floor(old_div(origin_x, VisualisationSettings.button_spacing)))
        return origin_column * VisualisationSettings.button_spacing + guide_type + index * VisualisationSettings.button_spacing - origin_x

    @staticmethod
    def _guide_y(index, origin_y, guide_type):
        if origin_y == None:
            origin_y = VisualisationSettings.visualisation_top
        origin_row = int(math.floor(old_div(origin_y, VisualisationSettings.row_spacing)))
        return origin_row * VisualisationSettings.row_spacing + guide_type + index * VisualisationSettings.row_spacing - origin_y

    @staticmethod
    def button_left_x(index, origin_x = None):
        return VisualisationGuides._guide_x(index, origin_x, VisualisationSettings.button_left)

    @staticmethod
    def light_left_x(index, origin_x = None):
        return VisualisationGuides._guide_x(index, origin_x, VisualisationSettings.light_left)

    @staticmethod
    def light_right_x(index, origin_x = None):
        return VisualisationGuides._guide_x(index, origin_x, VisualisationSettings.light_right)

    @staticmethod
    def button_right_x(index, origin_x = None):
        return VisualisationGuides._guide_x(index, origin_x, VisualisationSettings.button_right)

    @staticmethod
    def row_top_y(index, origin_y = None):
        return VisualisationGuides._guide_y(index, origin_y, VisualisationSettings.row_top)

    @staticmethod
    def body_top_y(index, origin_y = None):
        return VisualisationGuides._guide_y(index, origin_y, VisualisationSettings.body_top)

    @staticmethod
    def body_bottom_y(index, origin_y = None):
        return VisualisationGuides._guide_y(index, origin_y, VisualisationSettings.body_bottom)

    @staticmethod
    def row_bottom_y(index, origin_y = None):
        return VisualisationGuides._guide_y(index, origin_y, VisualisationSettings.row_bottom)
