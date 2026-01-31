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
# from runescape_actions.commons.use_spell.action_description import action_ordered_steps as use_spell
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



# Open Inventory

step_0 = {
    "check": get_action_picture_by_name("inventory"),  
    "verify": get_action_picture_by_name("inventory"), 
    "verify_args": {
        "reverse_verification": True,
    }, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_inventory"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_inventory")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_inventory",
}


step_1 = {
    "check": get_action_picture_by_name("skill_tab"),
    "verify": get_action_picture_by_name("skill_tab"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_skill_tab"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_skill_tab")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "select_skill_tab", 
}


# Step 2: Select Spell

step_2 = {
    "check": get_action_picture_by_name("high_alch"),
    "verify": get_action_picture_by_name("high_alch"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_high_alch"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_high_alch")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "use_high_alch", 
}


# action_ordered_steps += [step_0,]
# updates = [
#     {
#         "id": "use_spell",     
#         "check": get_action_picture_by_name("high_alch"),
#         "verify": get_action_picture_by_name("high_alch"),
#         "verify_args": {
#             "reverse_verification": True,
#         },
#         "extra_test_info": {
#         "end_mock_image_list": [
#             get_test_picture_by_name("test_high_alch")
#         ],
#     },
#     },
# ]

# use_high_alch = copy.deepcopy( update_action(use_spell, updates) )
# action_ordered_steps +=  use_high_alch 


# Step 10: Click (nature_rune)

step_3 = {
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

action_ordered_steps = [step_0, step_1, step_2, step_3, final_step,]
highalching_nature_rune = [step_0, step_1, step_2, step_3, final_step,]