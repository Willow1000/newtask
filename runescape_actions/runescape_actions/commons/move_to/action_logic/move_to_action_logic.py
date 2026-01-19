import os
import sys


"""
every function should accept a dictionary argument as input with all the arguments
functions can return other functions to serve as verification for the step they are on
"""

"""
specific functions only to be used in this action
"""

from common_action_framework.common_action_framework.common import (
    get_common_args,
    random_mouse_movement,
    client_wait,
)
from common_action_framework.common_action_framework.basic_interaction import (
    ignore_processor,
) 
from common_action_framework.common_action_framework.image_matching_logic import (
    template_matching,
)
from common_action_framework.common_action_framework.basic_interaction import send_w
from common_action_framework.common_action_framework.common import left_click_highlighted

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)


# TODO por isto tudo a partir daqui dentro da class Movement

colors = []
finalColor = []
i = 0
j = 0

def add_color(color):
    colors.append(color)

def get_colors():
    return colors

def add_final_color(finalColor):
    finalColor.append(finalColor)

def get_final_color():
    if len(finalColor) == 0:
        return None
    return finalColor[0]

def get_next_color():
    global i  # Access the global variable i
    if colors:
        if i == 0:
            next_color = colors[0]
            i = (i + 1) % len(colors)
            return next_color
        i = (i + 1) % len(colors)
        next_color = colors[i]
        return next_color
    else:
        return None

def get_previous_color():
    global j  # Access the global variable j
    if colors:
        if j == 0:
            previous_color = colors[j]
            return previous_color
        previous_color = colors[j - 1]
        j = (j + 1) % len(colors)
        return previous_color
    else:
        return None

def click_next_color(args):
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    dict_args = {
        "args_by_func": {
            "highlight_color": get_next_color()
        }, 
        "input_from_previous_elements": input_from_previous_elements, 
    }
    left_click_highlighted(dict_args)

def cleanup():
    colors.clear()
    finalColor.clear()
    i = 0
    j = 0

def setup_default():
    colors = ["FFFF0026", "FF00FF0A", "FF0026FF"]  # red, green, blue
    finalColor = ["FF0026FF"] # blue
