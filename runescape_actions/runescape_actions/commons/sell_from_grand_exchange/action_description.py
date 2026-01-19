import random
import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)
from common_action_framework.common_action_framework.image_matching_logic import (
    template_matching
)

from common_action_framework.common_action_framework.reuse_action import (
    update_action,
)

from runescape_actions.commons.enter_exchange.action_description import action_ordered_steps as enter_exchange
from runescape_actions.commons.buy_from_grand_exchange.action_description import get_action_ordered_steps as buy_from_exchange
from runescape_actions.commons.buy_from_grand_exchange.action_description import get_buy_from_exchange
from runescape_actions.commons.leave_exchange.action_description import action_ordered_steps as leave_exchange


time_limit = None  # time limit for this action (in minutes)
current_action_id = "sell_from_grand_exchange"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

# Step 5: Click one of the "Sell offer" Icons
step_5 = {
    "check": get_action_picture_by_name("sell"), 
    "verify": get_action_picture_by_name("all"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_exchange_options"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_trade_offer_menu")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "5_click_buy_sell",
}

def get_sell_from_exchange(item_name, quantity, price_to_buy) -> list[dict]:
    """
    ("item_name", "quantity", "price") all of them are strings,
    each of them can also be callables, in this case: item_name would become a tuple of 3 callables,
    for check, verify and test respectively, quantity and price would both be callables
    """
    # TODO: deposit items to bank (this requires being able to see the items on the inventory using the osrs api)
     # basically u know the items in ur inventory and u deposit them to bank
    action_ordered_steps = get_buy_from_exchange(item_name, quantity, price_to_buy)
    updates = [
        step_5,
    ]
    updated_steps = update_action(action_ordered_steps, updates)
    return copy.deepcopy( updated_steps )

def get_action_ordered_steps(items_to_sell):
    """
    :items_to_sell: a list of tuples in which each tuple is ("item_name", "quantity", "price") all of them are strings
    each of them can also be callables, in this case: item_name would become a tuple of 3 callables,
    for check, verify and test respectively, quantity and price would both be callables
    """
    action_ordered_steps = buy_from_exchange(items_to_sell)
    updates = [
        step_5,
    ]
    updated_steps = update_action(action_ordered_steps, updates)
    return copy.deepcopy( updated_steps )


def get_sell_from_exchange_test():
    price = str( random.randint(30, 100) )  # to ensure randomness in the test
    item = ("knife", "1", price)
    items = [item]
    return get_action_ordered_steps(items)


