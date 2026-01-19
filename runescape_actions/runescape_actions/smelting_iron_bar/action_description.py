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

from runescape_actions.commons.move_to.action_description import get_move_to as get_move_to


from runescape_actions.commons.highlight_npc.action_description import get_action_ordered_steps as get_highlight_npc
from runescape_actions.commons.buy_from_grand_exchange.action_description import get_action_ordered_steps as buy_from_exchange
from runescape_actions.commons.deposit_bank.action_description import (get_deposit_all, get_deposit_x)
from runescape_actions.commons.withdraw_bank.action_description import get_withdraw_x
from runescape_actions.commons.buy_ring_from_murky_matt.action_description import action_ordered_steps as buy_ring_from_murky_matt
from runescape_actions.commons.smelt_item.action_description import action_ordered_steps as smelt_item
from runescape_actions.commons.definitions.full_setup import map_colors


from common_action_framework.common_action_framework.reuse_action import update_action

from common_action_framework.common_action_framework.common import (
    shift_right_click,
    double_click,
)

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "smelting_iron_bar"
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

highlight_clerk = get_highlight_npc(updates).copy()
action_ordered_steps += copy.deepcopy(highlight_clerk)


# Step 2: Buy Iron Ore (140)
# Step 3: Buy Ruby Ring

buy_items = buy_from_exchange([
    ("Iron Ore", "140"),
    ("Ruby Ring", "1") 
    ])


action_ordered_steps += copy.deepcopy(buy_items)


# Step 4: Walk to Tile FFFF00E7

walk_to_tile = get_move_to("FFFF00E7")
action_ordered_steps += walk_to_tile

# Step 5: Highlight Npc (murky matt (runes))

updates = [
    {
        "id": "type_npc_name",     
        "check_args": {
            "write_string_in_client": {
                "string_to_write": "Murky Matt (runes)", 
            },
        },
        "verify": get_action_picture_by_name("murky_matt_inserted"), 
        "extra_test_info": {
            "end_mock_image_list": [
            get_test_picture_by_name("test_murky_matt_inserted")
            ],
        },
    },
]

highlight_murky = get_highlight_npc(updates).copy()
action_ordered_steps += copy.deepcopy(highlight_murky)


# Step 6: Buy ring of forging from Murky Matt

buy_ring = copy.deepcopy(buy_ring_from_murky_matt)
action_ordered_steps += buy_ring


# Step 7: Equip (Ring of forging)

step_7 = {
    "check": double_click,
    "verify": get_action_picture_by_name("ring_of_forging"),
    "verify_args": {
        "reverse_verification": True,
    }, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_equip_ring_of_forging"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_ring_of_forging_equipped")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "equip_ring_of_forging", 
}

action_ordered_steps += [step_7,]

# Step 8: Move to Banker

move_to_banker = get_move_to("banker")
action_ordered_steps += move_to_banker

# Step 9: Highlight Banker

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

highlight_banker = get_highlight_npc(updates).copy()
action_ordered_steps += copy.deepcopy(highlight_banker)

# Step 10: Deposit (iron ore x 140)

deposit_iron_ore = get_deposit_x("140", "iron_ore_inventory", "test_click_iron_ore").copy()
action_ordered_steps += copy.deepcopy(deposit_iron_ore)


# Step 11: Deposit (coins)

deposit_coins= get_deposit_all("coins", "test_click_coins").copy()
action_ordered_steps += copy.deepcopy(deposit_coins)

# Step 12: Move to (edgeville banker)

move_to_edgeville_banker = get_move_to("edgeville_banker")
action_ordered_steps += move_to_edgeville_banker

# Step 13: Highlight Banker

action_ordered_steps += highlight_banker


# Step 14: Withdraw Iron ore (28)

withdraw_iron_ore = get_withdraw_x("28", "iron_ore", "test_click_iron_ore")
action_ordered_steps += withdraw_iron_ore


# Step 15: Walk to edgeville furnace

move_to_edgeville_furnace = get_move_to("edgeville_furnace")
action_ordered_steps += move_to_edgeville_furnace

# Step 16: Click Highlighted Furnace
step_16 = {
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

action_ordered_steps += [step_16,]

# Step 17: Smelt Iron Bar

smelt_iron_bar = copy.deepcopy(smelt_item)
smelt_iron_bar = update_action(smelt_iron_bar, updates)
action_ordered_steps += smelt_iron_bar


# Step 18: Walk to banker

move_to_banker_2 = get_move_to("edgeville_banker")
action_ordered_steps += move_to_banker_2

# Step 19: highlight (banker)

action_ordered_steps += highlight_banker

# Step 20 Deposit (iron bar)

deposit_iron_bar = get_deposit_all("iron_bar", "test_click_iron_bar")
action_ordered_steps += deposit_iron_bar


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


