import copy


from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)
 

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "leave_bank"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

# Step 0: Click on the cross to leave bank
step_0 = {
    "check": get_action_picture_by_name("leave_bank"), 
    "verify": get_action_picture_by_name("leave_bank"), 
    "verify_args": {
        "reverse_verification": True,
    }, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_click_item"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_click_banker")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "leave_bank",
}

final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "leave_bank_final_step",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}

action_ordered_steps = [step_0, final_step]
