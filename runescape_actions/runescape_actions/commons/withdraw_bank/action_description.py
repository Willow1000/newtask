import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)


from runescape_actions.commons.enter_bank.action_description import action_ordered_steps as enter_bank
from runescape_actions.commons.leave_bank.action_description import action_ordered_steps as leave_bank
from common_action_framework.common_action_framework.reuse_action import update_action
from common_action_framework.common_action_framework.common import write_string_in_client 


all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "withdraw_bank"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.



# Step 2: Click on the search icon

step_2 = {
    "check": get_action_picture_by_name("search_icon"), 
    "check_args": {
        "right_click": True
    },  
    "verify": none_step_verify, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_click_item"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_click_item")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_seach_icon",
}

# Step 3: Search for the item to withdraw

step_3 = {
    "check": write_string_in_client,
    "check_args": {
        "write_string_in_client": {
            "string_to_write": "Bucket", 
        },
    },
    "verify": get_action_picture_by_name("bucket"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_click_item"),
            "replay_input": {
                "replay_type": "keyboard",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_withdraw_x")
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

# Step 4: Right click on an item

step_4 = {
    "check": get_action_picture_by_name("bucket"), 
    "check_args": {
        "right_click": True
    },  
    "verify": get_action_picture_by_name("withdraw_x"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_click_item"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_withdraw_x")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "right_click_item",
}


# Step 5: Click on the withdraw_X option

step_5 = {
    "check": get_action_picture_by_name("withdraw_x"), 
    "verify": get_action_picture_by_name("enter_ammount"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_withdraw_x"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_type_ammount")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_withdraw_x",
}


# Step 6: Type the ammount to withdraw + enter 

step_6 = {
    "check": write_string_in_client,
    "check_args": {
        "write_string_in_client": {
            "string_to_write": "1", 
        },
    },
    "verify": get_action_picture_by_name("outside_enter_ammount"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_enter_ammount"),
            "replay_input": {
                "replay_type": "keyboard",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_click_item")
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

withdraw__bank = copy.deepcopy([step_2, step_3, step_4, step_5, step_6])
enter_bank = copy.deepcopy( enter_bank )
leave_bank = copy.deepcopy( leave_bank )

def get_withdraw_x(ammount, image, mock_image):
    updates = [
        {
        "id": "type_item_name",
        "check": write_string_in_client,
        "check_args": {
            "write_string_in_client": {
                "string_to_write": "Bucket", 
            },
        },
        "verify": get_action_picture_by_name(image),
        "extra_test_info": {
            "end_mock_image_list": [
                get_test_picture_by_name(mock_image)
            ],
        },
        },
        {
        "id": "type_ammount",
        "check_args": {
            "write_string_in_client": {
                "string_to_write": ammount, 
            },
            }
        },
        {
            "id": "right_click_item",
            "check": get_action_picture_by_name(image),
            "test": [
                {
                    "mock_image": get_test_picture_by_name(mock_image),  
                    "replay_input": {"replay_type": "mouse", "coords": None},
                },
            ],
        }
    ]

    action_ordered_steps = copy.deepcopy( enter_bank ) \
        + copy.deepcopy( withdraw__bank ) \
        + ( leave_bank ) + [final_step]
    action_ordered_steps = copy.deepcopy(action_ordered_steps)
    
    update_action(action_ordered_steps, updates)
    return copy.deepcopy(action_ordered_steps)

def get_withdraw_x_test():
    return get_withdraw_x("10", "bucket", "test_click_item")



