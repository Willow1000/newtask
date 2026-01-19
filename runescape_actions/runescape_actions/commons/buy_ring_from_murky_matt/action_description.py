import copy 
 
from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)

from common_action_framework.common_action_framework.common import (
    send_enter_key_to_client,
    shift_right_click,
    write_string_in_client,
)


all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "buy_ring_from_murky_matt"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.



# Step 1: Click Murky Matt

step_1 = {
    "check": shift_right_click, 
    "verify": get_action_picture_by_name("talk_to_murky_matt"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_initial"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_talk_to_matt")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_murky_matt",
}


# Step 2: Click "talk to murky matt"

step_2 = {
    "check": get_action_picture_by_name("continue"),
    "verify": get_action_picture_by_name("deal_option"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_continue_1"),
            "replay_input": {
                "replay_type": "mouse",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_options")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        }
    },
    "id": "click_talk", 
}


# Step 3: Click "Continue"

step_3 = {
    "check": get_action_picture_by_name("deal_option"), 
    "verify": get_action_picture_by_name("continue"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_options"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_continue_2")
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


# Step 4: Click "I heard you deal rings of forging"

step_4 = {
    "check": get_action_picture_by_name("continue"),
    "verify": get_action_picture_by_name("continue"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_continue_2"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_ring_option")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        }
    },
    "id": "click_deals", 
}


# Step 5: Click "Continue"
 
step_5 = {
    "check": get_action_picture_by_name("continue"), 
    "verify": get_action_picture_by_name("continue"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_continue_2"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_ring_option")
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


# Step 6: Click "Continue" 

step_6 = {
    "check": get_action_picture_by_name("continue"), 
    "verify": get_action_picture_by_name("ammount"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_ring_option"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_ammount")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "continue_3",
}


# Step 7: Type ((number of rings) + enter)

step_7 = {
    "check": [write_string_in_client, send_enter_key_to_client],
    "check_args": {
        "write_string_in_client": {
            "string_to_write": "1", 
        },
    },
    "verify": get_action_picture_by_name("ammount"),
    "verify_args": {
        "reverse_verification": True,
    }, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_ammont"),
            "replay_input": {
                "replay_type": "keyboard",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_continue_3")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "xdot_keyboard_processing",
            "verify": "template_match",
        }
    },
    "id": "type_ammount", 
}


# Step 8: Click continue to finish interaction

step_8 = {
    "check": get_action_picture_by_name("continue"), 
    "verify": get_action_picture_by_name("continue"), 
    "verify_args": {
        "reverse_verification": True,
    }, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_continue_3"),  
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
    "id": "continue_4",
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

action_ordered_steps = [
    step_1,
    step_2,
    step_3,
    step_4,
    step_5,
    step_6,
    step_7,
    step_8,
    final_step,
]


