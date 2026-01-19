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
from runescape_actions.commons.withdraw_bank.action_description import (
    get_withdraw_x
)
 
all_failure_elements = {
     
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "cooking_raw_swordfish"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


# Step 1: Cook (raw swordfish)

updates = [
    {
        "id": "click_fish",
        "check": get_action_picture_by_name("raw_swordfish"),
        "verify": get_action_picture_by_name("raw_swordfish_selected"),
        "test": [
            {
            "mock_image": get_test_picture_by_name("test_swordfish"),  
            },
        ],
        "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_swordfish_selected")
            ],
        },
    },
    {
        "id": "click_fish_icon",
        "check": get_action_picture_by_name("raw_swordfish_icon"), 
        "test": [
            {
            "mock_image": get_test_picture_by_name("test_swordfish"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
            },
        ],
    },
]

cook_raw_swordfish = get_cook_fish(updates)
action_ordered_steps = copy.deepcopy( cook_raw_swordfish )


# Step 8: Deposit cooked swordfish (all)

deposit_cooked_swordfish = get_deposit_all("cooked_swordfish", "test_swordfish")
action_ordered_steps += deposit_cooked_swordfish


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
