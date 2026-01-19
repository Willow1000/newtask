import copy

from common_action_framework.common_action_framework.reuse_action import update_action
from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)
from common_action_framework.common_action_framework.image_matching_logic import ( 
    template_matching
)

from common_action_framework.common_action_framework.common import (
    send_enter_key_to_client,
    write_string_in_client,
)


from runescape_actions.commons.enter_exchange.action_description import action_ordered_steps as enter_exchange
from runescape_actions.commons.leave_exchange.action_description import action_ordered_steps as leave_exchange
from common_action_framework.common_action_framework.common import left_click_template_match_for_step_by_click_type

time_limit = None  # time limit for this action (in minutes)
current_action_id = "buy_from_grand_exchange"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

# Step 5: Click one of the "Buy offer" Icons

step_5 = {
    "check": get_action_picture_by_name("buy"), 
    "verify": get_action_picture_by_name("+1k"), 
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


# Step 6: Type the item name + Enter

step_6 = {
    "check": [write_string_in_client, send_enter_key_to_client],
    "check_args": {
        "write_string_in_client": {
            "string_to_write": "Bucket", 
        },
    },
    "verify": get_action_picture_by_name("selected_bucket"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_trade_offer_menu"),
            "replay_input": {
                "replay_type": "keyboard",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_item_selected")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "xdot_keyboard_processing",
            "verify": "template_match",
        }
    },
    "id": "type_item_name", 
}


# Step 7: Click the "..." to set quantity

step_7 = {
    "check": left_click_template_match_for_step_by_click_type, 
    "check_args": {
        "template_match_for_step": {
            # this means find +1k and press the ...
            "image_to_find": get_action_picture_by_name("+1k"), 
            "precision": 0.8,
            "offset": (44,0)
   
        },
    },
    "verify": get_action_picture_by_name("ammount_to_buy"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_item_selected"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_ammount_to_buy")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "ammount_to_buy",
}


# Step 8: Type the item quantity + enter

step_8 = {
    "check": [write_string_in_client, send_enter_key_to_client],
    "check_args": {
        "write_string_in_client": {
            "string_to_write": "1", 
        },
    },
    # "verify": get_action_picture_by_name("hand"), #TODO: this is wrong
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_ammount_to_buy"),
            "replay_input": {
                "replay_type": "keyboard",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_item_selected")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "xdot_keyboard_processing",
            "verify": "template_match",
        }
    },
    "id": "type_quantity", 
}


# Step 9: Click the "..." to set price

step_9 = {
    "check": left_click_template_match_for_step_by_click_type, 
    "check_args": {
        "template_match_for_step": {
            "image_to_find": get_action_picture_by_name("hand"), 
            "precision": 0.8,
            "offset": (44,0)
   
        },
    },
    "verify": get_action_picture_by_name("set_price"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_item_selected"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_set_price")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "set_price",
}


# Step 10: Type the item price + enter

step_10 = {
    "check": [write_string_in_client, send_enter_key_to_client],
    "check_args": {
        "write_string_in_client": {
            "string_to_write": "6", 
        },
    },
    "verify": get_action_picture_by_name("confirm"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_set_price"),
            "replay_input": {
                "replay_type": "keyboard",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_item_selected")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "xdot_keyboard_processing",
            "verify": "template_match",
        }
    },
    "id": "type_price", 
}


# Step 11: Click one of the "Buy offer" Icons

step_11 = {
    "check": get_action_picture_by_name("confirm"), 
    "verify": get_action_picture_by_name("confirm"), 
    "verify_args": {
        "reverse_verification" : True,
    },
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_item_selected"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_offer_created")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_confirm",
}

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

def get_item_name(item):
    if item is not None:
        return item.lower().replace(' ', '_')


def get_base_action_ordered_steps():
    """
    :returns must return deep copy
    """
    buy_from_exchange = [
        step_5,
        step_6,
        step_7,
        step_8,
        step_9,
        step_10,
        step_11,
        final_step,
    ]
    return copy.deepcopy(buy_from_exchange)


def get_buy_from_exchange(item_name, quantity, price_to_buy) -> list[dict]:
    """
    ("item_name", "quantity", "price") all of them are strings,
     each of them can also be callables, in this case: item_name would become a tuple of 3 callables,
      for check, verify and test respectively, quantity and price would both be callables
    """
    # TODO: withdraw items from bank (this requires being able to see the items on the inventory using the osrs api)
     # basically u always know all the items u have in ur inventory
    # TODO: at the end need to deposit the remaining gold? (if u still have anything in the inventory)
    buy_from_exchange = get_base_action_ordered_steps()
    if isinstance(item_name, str):
        item_name_composed = get_action_picture_by_name(get_item_name(item_name))
        item_name_composed_verify = get_action_picture_by_name(get_item_name(item_name))
        item_name_composed_test = get_test_picture_by_name(f"test_buy_{ get_item_name(item_name) }")
    elif isinstance(item_name, tuple):
        item_name_composed, item_name_composed_verify, item_name_composed_test = item_name 
    else:
        raise ValueError(f"item_name must be a string or a tuple containing the item name and its verify and test images, item name is: {item_name}")
     
    if not callable(quantity):
        quantity_composed = str( quantity )
    else:
        quantity_composed = quantity

    if not callable(price_to_buy):
        price_to_buy_composed = str( price_to_buy )
    else:
        price_to_buy_composed = price_to_buy
         
     
    updates = [
        {
            "id": "type_item_name",     
            "check_args": {
                "write_string_in_client": {
                    "string_to_write": item_name_composed, 
                },
            },
            "verify": item_name_composed_verify,
            "extra_test_info": {
                "end_mock_image_list": [
                    item_name_composed_test
                ],
            },
        },
        {
            "id": "type_quantity",
            "check_args": {
                "write_string_in_client": {
                    "string_to_write": quantity_composed,
                },
            },
        },
        { 
            "id": "type_price",
            "check_args": {
                "write_string_in_client": {
                    "string_to_write": price_to_buy_composed ,
                } 
            } 
        }
    ]
    updated_buy_steps = update_action(buy_from_exchange, updates)

    return copy.deepcopy( updated_buy_steps )

def get_action_ordered_steps(items_to_buy):
    """
    :items_to_buy: a list of tuples in which each tuple is ("item_name", "quantity", "price") all of them are strings
     each of them can also be callables, in this case: item_name would become a tuple of 3 callables,
      for check, verify and test respectively, quantity and price would both be callables
    """
    # items_to_buy should be a list of tuples in wich each tuple is ("item_name", "quantity")
    action_ordered_steps = copy.deepcopy(enter_exchange)

    for item in items_to_buy:
        item_name, quantity, price = item
        item_buy_steps = get_buy_from_exchange(item_name, quantity, price).copy()
        action_ordered_steps += copy.deepcopy(item_buy_steps)

    action_ordered_steps += copy.deepcopy(leave_exchange) 

    return copy.deepcopy( action_ordered_steps )

def get_buy_from_exchange_test():
    return get_buy_from_exchange("Bucket", "1", "6")



