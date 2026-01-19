import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)

from common_action_framework.common_action_framework.reuse_action import update_action
from common_action_framework.common_action_framework.common import shift_right_click


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
current_action_id = "smelt_item"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


# Step 0: Click the furnace

step_0 = {
    "check": shift_right_click,
    "verify": get_action_picture_by_name("smelt"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_inital"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_click_furnace")
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


# Step 1: Click the "smelt" option

step_1 = {
    "check": get_action_picture_by_name("smelt"),  
    "verify": get_action_picture_by_name("all"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_click_furnace"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_smelt_menu")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_smelt",
}


# Step 2: Click "all"

step_2 = {
    "check": get_action_picture_by_name("all"),  
    "verify": get_action_picture_by_name("all"),
    "verify_args": {
        "reverse_verification": True,
    },
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_smelt_menu"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_smelt_menu")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_all",
}


# Step 3: Click the bar you want to smelt

step_3 = {
    "check": get_action_picture_by_name("iron_bar"),  
    "verify": get_action_picture_by_name("all"),
    "verify_args": {
        "reverse_verification": True,
    },  
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_smelt_menu"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_initial")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_bar",
}

final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "smelt_item_final_step",
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

def smelt_item_test():
    updates = [
        {
        "id": "click_bar",
        "check": get_action_picture_by_name("iron_bar")
        },
    ]
    action_ordered_steps = [
        step_0,
        step_1,
        step_2,
        step_3,
        final_step,
    ]

    action_ordered_steps = update_action(action_ordered_steps, updates)
    return action_ordered_steps
