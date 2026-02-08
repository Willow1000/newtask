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

from runescape_actions.commons.highlight_npc.action_description import get_action_ordered_steps as get_highlight_npc
from runescape_actions.commons.withdraw_bank.action_description import get_withdraw_x
from runescape_actions.commons.buy_from_grand_exchange.action_description import get_action_ordered_steps as buy_from_exchange
from runescape_actions.commons.deposit_bank.action_description import (
    get_deposit_x, 
    get_deposit_all
    )
from runescape_actions.commons.withdraw_bank.action_description import get_withdraw_x
from runescape_actions.commons.deposit_bank.action_description import get_deposit_all

from common_action_framework.common_action_framework.reuse_action import update_action

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "highalching_combat_bracelet_at_fountain_of_rune_setup"
app_config_id = "buy_sell_config"  # each action may require a different set of configs from the app itself
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
                "name": "Grand Exchange Clerk", 
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

highlight_clerk = get_highlight_npc(updates)
action_ordered_steps += highlight_clerk


# Step 2: Buy Combat Bracelet (1)

buy_items = buy_from_exchange([
    ("Combat Bracelet", "10"), 
    ])


action_ordered_steps += copy.deepcopy(buy_items)


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

highlight_banker = get_highlight_npc(updates)
action_ordered_steps += highlight_banker


# Step 4: Deposit (Combat Bracelet x 1)

deposit_combat_bracelet = get_deposit_all("combat_bracelet_inventory", "test_inventory_after_buy")
action_ordered_steps += deposit_combat_bracelet


# Step 5: Deposit (coins)

deposit_coins = get_deposit_all("coins", "test_inventory_after_buy")
action_ordered_steps += deposit_coins


# Step 6: Withdraw (combat bracelet)

withdraw_combat_bracelet = get_withdraw_x("1", "combat_bracelet_bank", "test_bank_after_deposit")
action_ordered_steps += withdraw_combat_bracelet

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

