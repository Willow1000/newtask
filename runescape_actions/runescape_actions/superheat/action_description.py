import os
import sys
from PIL import ImageGrab
from PIL import Image
import copy

# ACTIONS_PROJECT_PATH: common action framework project
path = os.environ["ACTIONS_PROJECT_PATH"]
sys.path.append(path)

# CURRENT_ACTION_LIST_PROJECT_PATH: directory with all the actions to import
path = os.environ["CURRENT_ACTION_LIST_PROJECT_PATH"]
sys.path.append(path)

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)

# from common_action_framework.common_action_framework.common import send_enter_key_to_client
from common_action_framework.common_action_framework.reuse_action import (
    update_action,
)

from runescape_actions.commons.enter_exchange.action_description import action_ordered_steps as enter_exchange
from runescape_actions.commons.leave_exchange.action_description import action_ordered_steps as leave_exchange

from runescape_actions.commons.highlight_npc.action_description import get_action_ordered_steps as get_highlight_npc
from runescape_actions.commons.buy_from_grand_exchange.action_description import get_action_ordered_steps as buy_from_exchange
from runescape_actions.commons.deposit_bank.action_description import get_deposit_x as deposit_bank
from runescape_actions.commons.deposit_bank.action_description import get_deposit_all as deposit_bank_all
from runescape_actions.commons.withdraw_bank.action_description import get_withdraw_x as withdraw_bank
from runescape_actions.commons.use_spell.action_description import action_ordered_steps as use_spell

from common_action_framework.common_action_framework.reuse_action import update_action

# num_required_clients is the number of clients required to run this action (feature required for tests)
import copy

service_types_to_start = {
    "client": {
        "cnt": 1,
    }
}

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "superheating_iron_bar"
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

# Step 1: Equip Staff of Fire

step_1 = {
    "check": get_action_picture_by_name("staff_of_fire"),
    "verify": get_action_picture_by_name("staff_of_fire_equipped"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_equip_staff_of_fire"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_staff_of_fire_equipped")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "equip_staff_of_fire", 
}

action_ordered_steps = [step_0, step_1,]

# Step 2: Highlight_npc (grand exchange clerk)

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


# Step 3,4 : Buy 800 Nature Runes and 800 Iron Ore

buy_items = buy_from_exchange([("Iron Ore", "800"), ("Nature Rune", "800")])
action_ordered_steps += buy_items


# Step 5: Highlight Banker

updates = [
    {
        "id": "type_npc_name",     
        "check_args": {
            "write_string_in_client": {
                "string_to_write": "Banker", 
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


# Step 6: Deposit Coins

deposit_coins = deposit_bank_all("coins", "test_click_coins")
action_ordered_steps += deposit_coins


# Step 7: Deposit Iron Ore (100)

deposit_iron_ore = copy.deepcopy(deposit_bank("100", "iron_ore", "test_click_iron_ore" ))
action_ordered_steps += deposit_iron_ore

# Step 8: Withdraw Iron ore (27)

withdraw_iron_ore = copy.deepcopy(withdraw_bank("27", "iron_ore", "test_click_iron_ore"))
action_ordered_steps += withdraw_iron_ore


# Step 9: Use SuperHeat Spell

updates = [
    {
        "id": "use_spell",     
        "check": get_action_picture_by_name("superheat_item"),
        "verify": get_action_picture_by_name("iron_ore"),
        "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_superheat_iron_ore")
        ],
    },
    },
]

use_superheat = copy.deepcopy(use_spell)
use_superheat = update_action(use_superheat, updates)
action_ordered_steps += use_superheat


# Step 10: Click on Iron Ore to use the spell

step_10 = {
    "check": get_action_picture_by_name("iron_ore"),
    "verify": get_action_picture_by_name("superheat_item"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_superheat_iron_ore"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_skill_tab")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "use_superheat_spell", 
}

action_ordered_steps += [step_10,]

# Step 11:  Select the superheat spell again

action_ordered_steps += use_superheat


# Step 12: If there are still iron ores to smelt, jump to step 10

step_12 = {
    "jump": {
        "step_num": 10,
        "verify": get_action_picture_by_name("iron_ore"),
        "verify_mode": "verify_once",
        "reverse_verification": False,
    },
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_superheat_iron_ore"),
            "replay_input": {
                "replay_type": "NA",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "loop_info": {
            "num_iterations": 26,
            "img_after_loop": get_test_picture_by_name("test_all_superheated"),
        },
    },
    "processor_info": {
        "processor_type": {
            "check": "xdot_keyboard_processing",
            "verify": "template_match",
        },
    },
    "id": "check_if_already_on",
}

action_ordered_steps += [step_12,]

# Step 13: Deposit all iron bars

deposit_iron_bar = copy.deepcopy(deposit_bank_all("iron_bar", "test_click_iron_bar"))
action_ordered_steps += deposit_iron_bar

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

superheating_iron_bar = [step_0, step_1,  step_10, step_12, final_step]
