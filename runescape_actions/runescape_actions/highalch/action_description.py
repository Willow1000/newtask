from PIL import ImageGrab
from PIL import Image
import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)
from common_action_framework.common_action_framework.image_matching_logic import (
    template_matching
)
from common_action_framework.common_action_framework.common import (
    left_click_highlighted,
    send_user_name_to_replay_in_client,
    send_pw_to_replay_in_client,
    send_tab_key_to_client,
    send_enter_key_to_client,
    random_mouse_movement,
    verify_after_checking_once,
)

from common_action_framework.common_action_framework.reuse_action import (
    update_action,
    update_step,
    merge_dicts,
)

from common_action_framework.common_action_framework.reuse_action import update_action
from runescape_actions.commons.move_to.action_description import get_move_to as get_move_to
from runescape_actions.commons.use_spell.action_description import action_ordered_steps as use_spell
from runescape_actions.commons.definitions.full_setup import map_colors

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "highalching_combat_bracelet_at_fountain_of_rune"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.



# Step 1,2,3,4: Move to (underwall tunnel), click underwall tunnel, wilderness ditch)

# move_to_underwall_tunnel = get_move_to("wilderness_ditch")
# action_ordered_steps = move_to_underwall_tunnel


# # Step 5: Click (wilderness ditch)

# step_5 = {
#     "check": left_click_highlighted,
#     "check_args": {
#         "args_by_func": {
#             "highlight_color": map_colors["wilderness_ditch"]
#         }
#     },
#     "verify": get_action_picture_by_name("cross_ditch"),
#     "test": [
#         {
#             "mock_image": get_test_picture_by_name("test_wilderness_ditch"),  
#             "replay_input": {"replay_type": "mouse", "coords": None},
#         },
#     ],
#     "extra_test_info": {
#         "end_mock_image_list": [
#               get_test_picture_by_name("test_cross_ditch")
#         ],
#     },
#     "processor_info": {
#         "processor_type": {
#             "check": "template_match",
#             "verify": "template_match",
#         },
#     },
#     "id": "click_wilderness_ditch",
# }

# # Step 6: Click (cross ditch)

# step_6 = {
#     "check": get_action_picture_by_name("cross_ditch"),
#     "verify": get_action_picture_by_name("enter_wilderness"),
#     "test": [
#         {
#             "mock_image": get_test_picture_by_name("test_cross_ditch"),  
#             "replay_input": {"replay_type": "mouse", "coords": None},
#         },
#     ],
#     "extra_test_info": {
#         "end_mock_image_list": [
#               get_test_picture_by_name("test_enter_wilderness")
#         ],
#     },
#     "processor_info": {
#         "processor_type": {
#             "check": "template_match",
#             "verify": "template_match",
#         },
#     },
#     "id": "click_cross_ditch",
# }


# # Step 7: Click (enter wilderness)

# step_7 = {
#     "check": get_action_picture_by_name("enter_wilderness"),
#     "verify": get_action_picture_by_name("enter_wilderness"),
#     "verify_args": {
#         "reverse_verification": True,
#     }, 
#     "test": [
#         {
#             "mock_image": get_test_picture_by_name("test_enter_wilderness"),  
#             "replay_input": {"replay_type": "mouse", "coords": None},
#         },
#     ],
#     "extra_test_info": {
#         "end_mock_image_list": [
#               get_test_picture_by_name("test_enter_wilderness")
#         ],
#     },
#     "processor_info": {
#         "processor_type": {
#             "check": "template_match",
#             "verify": "template_match",
#         },
#     },
#     "id": "click_enter_wilderness",
# }

# action_ordered_steps += [step_5, step_6, step_7]

# # Step 8: Move to (fountain of rune)

# move_to_fountain_of_rune = get_move_to("fountain_of_rune")
# action_ordered_steps += move_to_fountain_of_rune

# Step 9: Use spell (high alch)

action_ordered_steps = []
updates = [
    {
        "id": "use_spell",     
        "check": get_action_picture_by_name("high_alch"),
        "verify": get_action_picture_by_name("high_alch"),
        "verify_args": {
            "reverse_verification": True,
        },
        "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_high_alch")
        ],
    },
    },
]

use_high_alch = copy.deepcopy( update_action(use_spell, updates) )
action_ordered_steps +=  use_high_alch 


# Step 10: Click (nature_rune)

step_10 = {
    "check": get_action_picture_by_name("nature_rune"),  
    "verify": get_action_picture_by_name("nature_rune"), 
    "verify_args": {
        "reverse_verification": True,
    }, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_nature_rune"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_nature_rune")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_nature_rune",
}

action_ordered_steps += [step_10,]


# final step, always add a final step, this is for the if else cases
final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "object_markers_final_step",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}

action_ordered_steps += [final_step,]
highalching_nature_rune = [step_10, final_step]