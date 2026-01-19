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
    format_name,
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
current_action_id = "craft_bracelet_setup"
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

highlight_clerk = copy.deepcopy(get_highlight_npc(updates))
action_ordered_steps += highlight_clerk


# Step 2: Buy Gold Bar (40)

buy_items = buy_from_exchange([
    ("Gold Bar", "40"), 
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

highlight_banker = copy.deepcopy(get_highlight_npc(updates))
action_ordered_steps += highlight_banker


# Step 4: Deposit (Gold Bar x 40)

deposit_bars = get_deposit_all("gold_bar", "test_inventory_after_buy")
action_ordered_steps += deposit_bars


# Step 5: Deposit (coins)

deposit_coins = get_deposit_all("coins", "test_inventory_after_buy")
action_ordered_steps += deposit_coins


# Step 6: Withdraw (Bracelet Mold x 1)

withdraw_bracelet_mold = get_withdraw_x("1", "bracelet_mold", "test_inventory_after_buy")
action_ordered_steps += withdraw_bracelet_mold


# Step 7: Withdraw (Gold Bar x 40)

withdraw_gold_bar = get_withdraw_x("40", "gold_bar", "test_inventory_after_buy")
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


def get_craft_bracelet_setup(bar):
    formated_bar = format_name(bar)

    buy_items = buy_from_exchange([
        (bar, "40"), 
        ])
    
    deposit_bars = get_deposit_all(formated_bar, "test_inventory_after_buy")
    withdraw_bars = get_withdraw_x("40", formated_bar, "test_inventory_after_buy")

    action_ordered_steps = [step_0,] + highlight_clerk + buy_items + highlight_banker \
    + deposit_bars + deposit_coins + withdraw_bracelet_mold + withdraw_bars + [final_step,]

    return copy.deepcopy(action_ordered_steps)
    
