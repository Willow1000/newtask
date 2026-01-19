from PIL import ImageGrab
from PIL import Image
import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
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
from runescape_actions.commons.withdraw_bank.action_description import get_withdraw_x
from runescape_actions.commons.deposit_bank.action_description import get_deposit_all

from runescape_actions.commons.highlight_npc.action_description import get_action_ordered_steps as get_highlight_npc
from runescape_actions.commons.buy_from_grand_exchange.action_description import get_buy_from_exchange as get_buy_from_exchange
from runescape_actions.commons.buy_from_grand_exchange.action_description import get_action_ordered_steps as buy_from_exchange
from runescape_actions.commons.sell_from_grand_exchange.action_description import get_sell_from_exchange
from runescape_actions.commons.sell_from_grand_exchange.action_description import get_action_ordered_steps as sell_from_exchange
from runescape_actions.commons.deposit_bank.action_description import (
    get_deposit_all
)

from common_action_framework.common_action_framework.common import (
    get_common_args,
    random_mouse_movement,
    client_wait,
)

from common_action_framework.common_action_framework.basic_interaction import (
    ignore_processor,
) 


time_limit = None  # time limit for this action (in minutes)
current_action_id = "trade_at_exchange"
app_config_id = "buy_sell_config"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

all_failure_elements = {
}

settings = {
    "reloaded": False,
}


def grab_item_to_buy(trade_processing_client) -> tuple:
   """
   This function grabs the item to buy from the screen.
   It returns the item id, amount to buy, and price to buy.
   """
   trade_processing_client.send_trade_request()
   item_id = trade_processing_client.trade_info.item_id
   amount_to_buy = trade_processing_client.trade_info.amount_to_trade
   price_to_buy = trade_processing_client.trade_info.price_to_buy
   return ( item_id, amount_to_buy, price_to_buy )

 
def grab_item_id_current_trade(args) -> str:
   reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
   item_id = reference_of_client_of_class.grab_current_trade().item_id
   return item_id


def get_item_name(item):
    if item is not None:
        return item.lower().replace(' ', '_')

 
def get_item_name_composed(args) -> str:
    item_id = grab_item_id_current_trade(args)
    item_name_composed = get_action_picture_by_name(get_item_name(item_id))
    return item_name_composed


def get_item_name_composed_verify(args) -> str: 
    item_id = grab_item_id_current_trade(args)
    item_name_composed_verify = get_action_picture_by_name(get_item_name(item_id))
    return item_name_composed_verify


def get_item_name_composed_test(args) -> str:
    item_id = grab_item_id_current_trade(args)
    item_name_composed_test = get_test_picture_by_name(f"test_buy_{ get_item_name(item_id) }")
    return item_name_composed_test


def grab_amount_to_buy_current_trade(args) -> str:
   reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
   amount_to_buy = reference_of_client_of_class.grab_current_trade().amount_to_buy
   return amount_to_buy


def grab_item_price_current_trade(args) -> str:
   reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
   price_to_buy = reference_of_client_of_class.grab_current_trade().price_to_buy
   return price_to_buy


def grab_trade_type_current_trade(args) -> str:
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    trade_type = reference_of_client_of_class.grab_current_trade().trade_type
    return trade_type


def is_sell_trade(args) -> bool:
    return grab_trade_type_current_trade(args) == "sell" 


def generate_deposit_bought_in_exchange() -> list[dict]:
    action_ordered_steps = []
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
    # withdraw_combat_bracelet = get_withdraw_x("1", "combat_bracelet_bank", "test_bank_after_deposit")
    # action_ordered_steps += withdraw_combat_bracelet
    return action_ordered_steps


def generate_jump_to_buy_or_sell() -> dict:
    jump_to_buy_or_sell = {
        "jump": {
            "step_num": "step_in_between_sell_and_buy",
            "verify": is_sell_trade,
            "verify_mode": "verify_once",
            "reverse_verification": False,
        },
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "jump_to_buy_or_sell",
    }
    return jump_to_buy_or_sell


def go_to_next_trade(args) -> dict:
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    trades_of_interest_manager = reference_of_client_of_class.trades_of_interest_manager
    return trades_of_interest_manager.next_trade 
 
 
def generate_trade_at_exchange() -> list:
    """
    the purpose here is to generate action ordered steps for trading at exchange
    """
    jump_to_buy_or_sell = generate_jump_to_buy_or_sell()
    all_item_name_fields = (get_item_name_composed, get_item_name_composed_verify, get_item_name_composed_test)
    sell_items = get_sell_from_exchange(
       all_item_name_fields, grab_amount_to_buy_current_trade, grab_item_price_current_trade
    )
    buy_items = get_buy_from_exchange(
       all_item_name_fields, grab_amount_to_buy_current_trade, grab_item_price_current_trade
    )
    placeholder_step = {
        "check": none_step_verify,
        "verify": none_step_verify,
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "step_in_between_sell_and_buy",
    }
    action_ordered_steps = [jump_to_buy_or_sell] +  sell_items  + [placeholder_step]  +  buy_items
    action_ordered_steps += [{
     "check": go_to_next_trade,
     "processor_info": {
         "processor_type": {
             "check": "template_match",
             "verify": "template_match",
         },
     },
     "id": "go_to_next_trade",
    }]
    return copy.deepcopy( action_ordered_steps )

 
step_0 = {
    "check": none_step_verify,
    "verify": get_action_picture_by_name("all/dashboard/report"),
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

action_ordered_steps = [step_0,]
highlight_grand_exchange_clerk = get_highlight_npc(updates)
action_ordered_steps += highlight_grand_exchange_clerk
trade_at_exchange = generate_trade_at_exchange()
action_ordered_steps += trade_at_exchange
action_ordered_steps += [final_step,]

