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
from runescape_actions.commons.cook_fish.action_description import get_cook_fish
from runescape_actions.commons.deposit_bank.action_description import (
    get_deposit_all
)
from runescape_actions.commons.move_to.action_description import get_move_to as get_move_to
 
all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "cooking_raw_anchovies"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

# Step 1: Cook (raw anchovies)

updates = [
    {
        "id": "click_fish",
        "check": get_action_picture_by_name("raw_anchovies"),
        "verify": get_action_picture_by_name("raw_anchovies_selected"),
        "test": [
            {
            "mock_image": get_test_picture_by_name("test_anchovies"),  
            },
        ],
        "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_raw_anchovies_selected"),
            ],
        },
    },
    {
        "id": "click_fish_icon",
        "check": get_action_picture_by_name("raw_anchovies_icon"), 
        "test": [
            {
            "mock_image": get_test_picture_by_name("test_cook_menu"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
            },
        ],
    },
    ]

cook_raw_anchovies = get_cook_fish(updates)
action_ordered_steps = cook_raw_anchovies

#TODO tirar foto cook_menu

deposit_cooked_anchovies = get_deposit_all("cooked_anchovies", "test_anchovies")
action_ordered_steps += deposit_cooked_anchovies   

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
