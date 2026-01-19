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
    random_mouse_movement,
    verify_after_checking_once,
)

"""
how does the action_ordered_steps format work?
 check RunningBotStatus class doc
"""


all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "toggle_run"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

step_0 = {
    "jump": {
        "step_num": 2,
        "verify": get_action_picture_by_name("boots_on"),
        "verify_mode": "verify_once",
        "reverse_verification": False,
    },
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_run"),
            "replay_input": {
                "replay_type": "NA",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "loop_info": {
            "num_iterations": 2,
            "img_after_loop": get_test_picture_by_name("test_run_on"),
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
# Step 1: Click the boots to run
step_1 = {
    "check": get_action_picture_by_name("boots"),  
    "verify": get_action_picture_by_name("boots_on"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_run"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_run_on")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_boots",
}

#blank step for the jump to be able to jump here
step_2 = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "blank_step_for_jump",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
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
    final_step,
]


