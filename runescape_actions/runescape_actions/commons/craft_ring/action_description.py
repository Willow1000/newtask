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


from runescape_actions.commons.deposit_bank.action_description import (
    get_deposit_x,
    get_deposit_all
)
from runescape_actions.commons.withdraw_bank.action_description import (
    get_withdraw_x
)
from runescape_actions.commons.move_to.action_description import get_move_to as get_move_to
from runescape_actions.commons.definitions.full_setup import map_colors

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "craft_ring"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.



# Step 1: Move to (edgeville furnace)

move_to_edgeville_banker = get_move_to("edgeville_furnace")
action_ordered_steps = move_to_edgeville_banker

# Step 2: Click Highlighted Furnace

step_2 = {
    "check": left_click_highlighted,  
    "check_args": {
        "args_by_func": {
            "highlight_color": map_colors["furnace"]
        }
    }, 
    "verify": get_action_picture_by_name("ring_menu"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_furnace"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_furnace_menu")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_furnace",
}

action_ordered_steps += [step_2, ]


# Step 3: Click All

step_3 = {
    "check": get_action_picture_by_name("all"),   
    "verify": none_step_verify, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_furnace_menu"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_furnace_menu")
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


# Step 4: Click Gold Bracelet

step_4 = {
    "check": get_action_picture_by_name("ring_menu"),   
    "verify": get_action_picture_by_name("ring_menu"), 
    "verify_args": {
        "reverse_verification": True,
    }, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_furnace_menu"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_furnace")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_gold_ring",
}


# Step 5: Walk to banker

move_to_banker = get_move_to("edgeville_banker")
action_ordered_steps += move_to_banker


# Step 5: Deposit (Gold Bracelet)

deposit_gold_ring = get_deposit_all("gold_ring", "test_deposit")
action_ordered_steps += deposit_gold_ring


# Step 6: Withdraw (Gold Bar)

withdraw_gold_bar = get_withdraw_x("26", "gold_bar", "test_withdraw")
action_ordered_steps += withdraw_gold_bar

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

craft_ring = [step_2, step_3, step_4]

def get_craft_ring(ring, bar, menu_image="ring_menu"):
    deposit_gold_ring = get_deposit_all(ring, "test_deposit")
    withdraw_gold_bar = get_withdraw_x("26", bar, "test_withdraw")

    step_2 = {
        "check": left_click_highlighted,  
        "check_args": {
            "args_by_func": {
                "highlight_color": map_colors["furnace"]
            }
        }, 
        "verify": get_action_picture_by_name(menu_image), 
        "test": [
            {
                "mock_image": get_test_picture_by_name("test_furnace"),  
                "replay_input": {"replay_type": "mouse", "coords": None},
            },
        ],
        "extra_test_info": {
            "end_mock_image_list": [
                get_test_picture_by_name("test_furnace_menu")
            ],
        },
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "click_furnace",
    }

    step_3 = {
        "check": get_action_picture_by_name("all"),   
        "verify": none_step_verify, 
        "test": [
            {
                "mock_image": get_test_picture_by_name("test_furnace_menu"),  
                "replay_input": {"replay_type": "mouse", "coords": None},
            },
        ],
        "extra_test_info": {
            "end_mock_image_list": [
                get_test_picture_by_name("test_furnace_menu")
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

    step_4 = {
        "check": get_action_picture_by_name(ring),   
        "verify": get_action_picture_by_name(ring), 
        "verify_args": {
            "reverse_verification": True,
        }, 
        "test": [
            {
                "mock_image": get_test_picture_by_name("test_furnace_menu"),  
                "replay_input": {"replay_type": "mouse", "coords": None},
            },
        ],
        "extra_test_info": {
            "end_mock_image_list": [
            get_test_picture_by_name("test_furnace")
            ],
        },
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": f"click_{ring}",
    }

    action_ordered_steps = move_to_edgeville_banker + [step_2, step_3, step_4] \
    + move_to_banker + deposit_gold_ring + withdraw_gold_bar + [final_step,]

    return copy.deepcopy(action_ordered_steps)
