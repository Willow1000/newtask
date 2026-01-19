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
current_action_id = "cook_setup"
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

highlight_clerk = get_highlight_npc(updates)


# Step 2: Buy Logs (3) and Raw Tuna (78)

buy_items = buy_from_exchange([
    ("Logs", "3"), 
    ("Raw Tuna", "78")
    ])


# Step 3: Highlight_npc (banker)

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


# Step 4: Deposit (Logs)

deposit_logs = get_deposit_all("log", "test_inventory_after_buy")


# Step 5: Deposit (coins)

deposit_coins = get_deposit_all("coins", "test_inventory_after_buy")


# Step 6: Deposit (raw tuna)

deposit_fish = get_deposit_all("raw_tuna", "test_inventory_after_buy")


# Step 7: Withdraw (1) (logs)

withdraw_logs = get_withdraw_x("1", "log", "test_inventory_after_buy")

# Step 8: Withdraw (26) (raw tuna)

withdraw_fish = get_withdraw_x("26", "raw_tuna", "test_inventory_after_buy")

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


def get_cook_setup(fish_to_cook="Raw Tuna", quantity_to_buy="26"):
    fish_name = format_name(fish_to_cook)

    buy_items = buy_from_exchange([
    ("Logs", "3"), 
    (fish_to_cook, quantity_to_buy)
    ])

    deposit_fish = get_deposit_all(fish_name + "_after_buy", "test_inventory_after_buy")
    withdraw_fish = get_withdraw_x("26", fish_name, "test_inventory_after_buy")
    action_ordered_steps = []
    (
    [step_0] 
    + highlight_clerk 
    + buy_items 
    + highlight_banker 
    + deposit_logs 
    + deposit_coins 
    + deposit_fish 
    + withdraw_logs 
    + withdraw_fish 
    + [final_step]
)
    return copy.deepcopy(action_ordered_steps)
