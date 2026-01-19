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


from runescape_actions.commons.highlight_npc.action_description import get_action_ordered_steps as get_highlight_npc
from runescape_actions.commons.deposit_bank.action_description import (
    get_deposit_x,
    get_deposit_all
)
from runescape_actions.commons.withdraw_bank.action_description import (
    get_withdraw_x
)
from runescape_actions.commons.smelt_item.action_description import action_ordered_steps as smelt_item
from runescape_actions.smelting_steel_bar_setup.action_description import action_ordered_steps as smelt_steel_bar_setup
from common_action_framework.common_action_framework.reuse_action import update_action
from runescape_actions.commons.definitions.full_setup import map_colors


from runescape_actions.commons.move_to.action_description import get_move_to as move_to

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "smelting_steel_bar"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


# Step 1: Action Setup

action_ordered_steps = smelt_steel_bar_setup

#TODO verifies dos move_to
# Step 2: Move to (edgeville banker)

move_to_edgeville_banker = move_to("edgeville_banker")
action_ordered_steps += move_to_edgeville_banker

# Step 3: Highlight Banker

updates = [
    {
        "id": "type_npc_name",     
        "check_args": {
            "write_string_in_client": {
                "string_to_write": "banker", 
            },
        },
        "verify": get_action_picture_by_name("banker_inserted"), 
        "extra_test_info": {
            "end_mock_image_list": [
            get_test_picture_by_name("test_banker_inserted")
            ],
        },
    },
]

highlight_banker = copy.deepcopy(get_highlight_npc())
highlight_banker = update_action(highlight_banker, updates)
action_ordered_steps += highlight_banker


# Step 4: Withdraw Iron ore (9)

withdraw_iron_ore = get_withdraw_x("9", "iron_ore", "test_click_iron_ore")
action_ordered_steps += withdraw_iron_ore


# Step 5: Withdraw coal (18)

withdraw_coal = get_withdraw_x("18", "coal_bank", "test_click_coal")
action_ordered_steps += withdraw_coal


# Step 6: Walk to edgeville furnace

move_to_edgeville_furnace = move_to("edgeville_furnace")
action_ordered_steps += move_to_edgeville_furnace


# Step 7: Highlight Furnace

step_5 = {
    "check": left_click_highlighted,  
    "check_args": {
        "args_by_func": {
            "highlight_color": map_colors["fire"]
        }
    },  
    "verify": get_action_picture_by_name("all"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_furnace"),  
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
    "id": "click_furnace",
}


# Step 8: Smelt Iron Bar

updates = [
    {
        "id": "click_bar",     
        "check": get_action_picture_by_name("steel_bar"), 
    },
]

smelt_steel_bar = copy.deepcopy(smelt_item)
smelt_steel_bar = update_action(smelt_steel_bar, updates)
action_ordered_steps += smelt_steel_bar


# Step 9: Walk to banker

move_to_edgeville_banker = move_to("edgeville_banker")
action_ordered_steps += move_to_edgeville_banker

# Step 10: highlight (banker)

action_ordered_steps += highlight_banker


# Step 11: Deposit (steel bar)

deposit_steel_bar = get_deposit_x("28", "steel_bar", "test_deposit_steel_bar")
action_ordered_steps += deposit_steel_bar


# Now you can jump to step 14 if you want to loop

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
