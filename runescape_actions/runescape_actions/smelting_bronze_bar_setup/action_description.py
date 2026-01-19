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

from common_action_framework.common_action_framework.utility import dictionary_readeable_print

from runescape_actions.commons.highlight_npc.action_description import get_action_ordered_steps as highlight_npc
from runescape_actions.commons.buy_from_grand_exchange.action_description import get_action_ordered_steps as buy_from_exchange
from runescape_actions.commons.deposit_bank.action_description import (
    get_deposit_x, 
    get_deposit_all
    )
from runescape_actions.commons.deposit_bank.action_description import get_deposit_all

from common_action_framework.common_action_framework.reuse_action import update_action
from runescape_actions.commons.move_to.action_description import get_move_to as get_move_to

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "smelting_bronze_bar_setup"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.



step_0 = {
    "check": none_step_verify,
    "verify": get_action_picture_by_name("report"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("not_in_game_lobby"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_lowbar")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "check_app_state_in_game_lobby", 
}

action_ordered_steps = [step_0,]

# Step 1: Highlight_npc (grand exchange clerk)

updates = [
    {
        "id": "type_npc_name",     
        "check_args": {
            "write_string_in_client": {
                "string_to_write": "Grand Exchange Clerk", 
            },
        },
        "verify": get_action_picture_by_name("clerk_inserted"), 
        "extra_test_info": {
            "end_mock_image_list": [
            get_test_picture_by_name("test_clerk_inserted")
            ],
        },
    },
]

highlight_clerk = copy.deepcopy( highlight_npc(updates) )
action_ordered_steps += copy.deepcopy( highlight_clerk )


# Step 2: Buy Tin Ore (800)
# Step 3: Buy Copper Ore (800)

buy_items = buy_from_exchange([
    ("Tin Ore", "800"), 
    ("Copper Ore", "800"),
    ])


action_ordered_steps += copy.deepcopy( buy_items )


# Step 4: Highlight Banker

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


# Step 5: Deposit (Tin Ore)

deposit_iron_ore = copy.deepcopy( get_deposit_all("tin_ore_inventory", "test_inventory_after_buy") )
action_ordered_steps += copy.deepcopy( deposit_iron_ore )


# Step 6: Deposit (coins)

deposit_coins = copy.deepcopy( get_deposit_all("coins", "test_inventory_after_buy") )
action_ordered_steps += copy.deepcopy( deposit_coins )


# Step 7: Deposit (Copper Ore )

deposit_coal = copy.deepcopy( get_deposit_all("copper_ore_inventory", "test_inventory_after_buy") )
action_ordered_steps += copy.deepcopy( deposit_coal )


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
