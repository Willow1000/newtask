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


from runescape_actions.commons.highlight_npc.action_description import get_action_ordered_steps as highlight_npc
from runescape_actions.commons.deposit_bank.action_description import (
    get_deposit_all
)
from common_action_framework.common_action_framework.reuse_action import update_action
from runescape_actions.commons.move_to.action_description import get_move_to as get_move_to
from runescape_actions.commons.definitions.full_setup import map_colors

 
all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "cook_fish"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


# Step 1: Click (tinderbox)

step_1 = {
    "check": get_action_picture_by_name("tinderbox"),  
    "verify": none_step_verify, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_tinderbox"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_tinderbox")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_tinderbox",
}

action_ordered_steps = [step_1,]


# Step 2: Click (log)

step_2 = {
    "check": get_action_picture_by_name("log"),  
    "verify": get_action_picture_by_name("log"), 
    "verify_args": {
        "reverse_verification": True,
    }, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_tinderbox"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_tinderbox_used")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_log",
}

action_ordered_steps += [step_2,]

# Step 3 : Click (fish)

step_3 = {
    "check": get_action_picture_by_name("raw_tuna"),  
    "verify": get_action_picture_by_name("raw_tuna_selected"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_raw_tuna"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_raw_tuna")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_fish",
}

action_ordered_steps += [step_3,]

# Step 4: Click (fire)

step_4 = {
    "check": left_click_highlighted,  
    "check_args": {
        "args_by_func": {
            "highlight_color": map_colors["fire"]
        }
    },  
    "verify": get_action_picture_by_name("all"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_fire"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_cook_menu")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_fire",
}

action_ordered_steps += [step_4,]


# Step 5: Click (all)

step_5 = {
    "check": get_action_picture_by_name("all"),  
    "verify": none_step_verify, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_cook_menu"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_cook_menu")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_all",
}

action_ordered_steps += [step_5,]


# Step 6: Click (raw tuna icon)

step_6 = {
    "check": get_action_picture_by_name("raw_tuna_icon"),  
    "verify": get_action_picture_by_name("all"), 
    "verify_args": {
        "reverse_verification": True,
    },
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_cook_menu"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_cooking")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_fish_icon",
}

action_ordered_steps += [step_6,]

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

cook_fish = [step_1, step_2, step_3 ,step_4, step_5, step_6, step_6, final_step,]

def get_cook_fish(updates=None):
    if updates is not None:
        ordered_steps = copy.deepcopy(action_ordered_steps)
        updated_steps = update_action(ordered_steps, updates)
        return updated_steps
    return copy.deepcopy(action_ordered_steps)


