import copy 
 
from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)
from common_action_framework.common_action_framework.common import (
    left_click_highlighted,
)
from runescape_actions.commons.definitions.full_setup import map_colors

all_failure_elements = {
    "send_creds": [
        # for example this failure element is meant to be checked in case the step_11 fails
        # so, after step_12 fails, the system will look for this image, and go back to step_11
        # this is not meant to be used instead of a while loop, in this case this is used as an example,
        # but, a while loop as shown in the commented step_12 would have been better in this case
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "enter_bank"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


step_0 = {
    "check": none_step_verify,
    "verify": get_action_picture_by_name("all/dashboard/menu/enter_bank/action/report"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("all/dashboard/menu/enter_bank/test/not_in_game_lobby"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("all/dashboard/menu/enter_bank/test/test_lowbar")
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

# Step 1: Click the banker
step_1 = {
    "check": left_click_highlighted,
    "check_args": {
        "args_by_func": {
            "highlight_color": [ map_colors["banker"], map_colors["default_blue"] ],
        }
    },
    "verify": get_action_picture_by_name("all/dashboard/menu/enter_bank/action/continue"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("all/dashboard/menu/enter_bank/test/test_click_banker_general_highlight"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
        { 
            # 2 values are tested here, cause the banker can be one color or the other
            "mock_image": get_test_picture_by_name("all/dashboard/menu/enter_bank/test/test_click_banker_blue_highlight"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("all/dashboard/menu/enter_bank/test/test_talk_banker")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_banker",
}


# Step 2: Click the "continue" option
step_2 = {
    "check": get_action_picture_by_name("all/dashboard/menu/enter_bank/action/continue"),  
    "verify": get_action_picture_by_name("all/dashboard/menu/enter_bank/action/access_bank_account"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("all/dashboard/menu/enter_bank/test/test_talk_banker"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("all/dashboard/menu/enter_bank/test/test_banker_options")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_continue",
}


# Step 3: Click the "access my bank account option
step_3 = {
    "check": get_action_picture_by_name("all/dashboard/menu/enter_bank/action/access_bank_account"),  
    "verify": get_action_picture_by_name("all/dashboard/menu/enter_bank/action/verify_inside_bank_account"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("all/dashboard/menu/enter_bank/test/test_banker_options"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("all/dashboard/menu/enter_bank/test/test_click_item")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "access_bank_account",
}

final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "enter_bank_final_step",
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
    final_step,
]
