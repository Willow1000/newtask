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
from common_action_framework.common_action_framework.reuse_action import update_action
from runescape_actions.commons.move_to.action_description import get_move_to as get_move_to
from runescape_actions.commons.definitions.full_setup import map_colors

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "smelting_silver_bar"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.




#TODO verifies dos move_to
# Step 2: Move to (edgeville banker)

move_to_edgeville_banker = get_move_to("edgeville_banker")
action_ordered_steps = move_to_edgeville_banker

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


# Step 4: Withdraw Silver Ore (28)

withdraw_silver_ore = get_withdraw_x("28", "silver_ore", "test_click_silver_ore")
action_ordered_steps += withdraw_silver_ore


# Step 5: Walk to edgeville furnace

move_to_edgeville_furnace = get_move_to("edgeville_furnace")
action_ordered_steps += move_to_edgeville_furnace


# Step 6: Highlight Furnace

step_6 = {
    "check": left_click_highlighted,  
    "check_args": {
        "args_by_func": {
            "highlight_color": map_colors["furnace"]
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

action_ordered_steps += [step_6,]


# Step 7: Smelt Silver Bar

updates = [
    {
        "id": "click_bar",     
        "check": get_action_picture_by_name("smelt_silver_bar"), 
    },
]

smelt_silver_bar = copy.deepcopy(smelt_item)
smelt_silver_bar = update_action(smelt_silver_bar, updates)
action_ordered_steps += smelt_silver_bar


# Step 8: Walk to banker

move_to_banker_2 = get_move_to("edgeville_banker")
action_ordered_steps += move_to_banker_2

# Step 9: highlight (banker)

action_ordered_steps += highlight_banker


# Step 10 Deposit (silver bar)

deposit_silver_bar = get_deposit_all("silver_bar_inventory", "test_deposit_silver_bar")
action_ordered_steps += deposit_silver_bar


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
