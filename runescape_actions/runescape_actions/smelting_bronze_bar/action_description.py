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


from runescape_actions.commons.highlight_npc.action_description import get_action_ordered_steps as highlight_npc
from runescape_actions.commons.deposit_bank.action_description import (
    get_deposit_all
)
from runescape_actions.commons.withdraw_bank.action_description import (
    get_withdraw_x
)
from runescape_actions.commons.smelt_item.action_description import action_ordered_steps as smelt_item
from common_action_framework.common_action_framework.reuse_action import update_action
from runescape_actions.commons.move_to.action_description import get_move_to as get_move_to
from runescape_actions.commons.definitions.full_setup import map_colors

time_limit = None  # time limit for this action (in minutes)
current_action_id = "smelting_bronze_bar"
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

highlight_banker = copy.deepcopy( highlight_npc(updates) )
action_ordered_steps += copy.deepcopy( highlight_banker )


# Step 4: Withdraw Tin ore (14)

withdraw_iron_ore = copy.deepcopy( get_withdraw_x("14", "tin_ore_bank", "test_bank_after_deposit") )
action_ordered_steps += copy.deepcopy( withdraw_iron_ore )


# Step 5: Withdraw Copper Ore (14)

withdraw_coal = copy.deepcopy( get_withdraw_x("14", "copper_ore_bank", "test_bank_after_deposit") )
action_ordered_steps += copy.deepcopy( withdraw_coal )   


# Step 6: Walk to edgeville furnace

move_to_edgeville_furnace = get_move_to("edgeville_furnace")
action_ordered_steps += move_to_edgeville_furnace


# Step 7: Click Highlighted Furnace

step_7 = {
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

action_ordered_steps += [step_7,]


# Step 8: Smelt Bronze Bar

updates = [
    {
        "id": "click_bar",     
        "check": get_action_picture_by_name("smelt_bronze_bar"), 
    },
]

smelt_bronze_bar = copy.deepcopy(smelt_item)
smelt_bronze_bar = copy.deepcopy( update_action(smelt_bronze_bar, updates) )
action_ordered_steps += copy.deepcopy( smelt_bronze_bar )


# Step 9: Walk to banker

move_to_banker = get_move_to("edgeville_banker")
action_ordered_steps += move_to_banker

# Step 10: highlight (banker)

action_ordered_steps += copy.deepcopy( highlight_banker )


# Step 11 Deposit (bronze bar)

deposit_bronze_bar = copy.deepcopy( get_deposit_all("bronze_bar", "test_deposit_bronze_bar") )
action_ordered_steps += copy.deepcopy( deposit_bronze_bar )


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
