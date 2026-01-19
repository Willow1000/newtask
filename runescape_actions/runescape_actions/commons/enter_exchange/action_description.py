import copy 

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)

from common_action_framework.common_action_framework.common import left_click_highlighted
from runescape_actions.commons.definitions.full_setup import map_colors
 

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "enter_exchange"
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

# Step 1: Click the clerk
step_1 = {
    "check": left_click_highlighted,
    "check_args": {
        "args_by_func": {
            "highlight_color": map_colors["clerk"]
        }
    },
    "verify": get_action_picture_by_name("continue"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_talk_to_clerk"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_clerk_continue")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_clerk",
}


# Step 2: Click the "continue" option
step_2 = {
    "check": get_action_picture_by_name("continue"),  
    "verify": get_action_picture_by_name("setup_trade_offers"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_clerk_continue"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_clerk_options")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "continue_1",
}


# Step 3: Click the "setup trade offers" option
step_3 = {
    "check": get_action_picture_by_name("setup_trade_offers"),  
    "verify": get_action_picture_by_name("continue"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_clerk_options"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_setup_trade_offers")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_setup_offer",
}

# Step 4: click on continute
step_4 = {
    "check": get_action_picture_by_name("continue"),   
    "verify": get_action_picture_by_name("inside_trade_offers"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_setup_trade_offers"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_exchange_options")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "continue_2",
}

final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "enter_exchange_final_step",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}

action_ordered_steps = [
    step_0,
    step_1,
    step_2,
    step_3,
    step_4,
    final_step,
]
