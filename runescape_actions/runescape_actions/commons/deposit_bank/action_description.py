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
    write_string_in_client,
)


# from common_action_framework.common_action_framework.common import send_enter_key_to_client

from runescape_actions.commons.enter_bank.action_description import action_ordered_steps as enter_bank
from runescape_actions.commons.leave_bank.action_description import action_ordered_steps as leave_bank 


from common_action_framework.common_action_framework.reuse_action import (
    update_action,
)
 
from runescape_actions.commons.enter_bank.action_description import action_ordered_steps as enter_bank
from runescape_actions.commons.leave_bank.action_description import action_ordered_steps as leave_bank


all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "deposit_bank"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


# wait until app starts up
#  wait till service is in a state such that the action can start should always be step 0



# Step 4: Right click on an item

step_4 = {
    "check": get_action_picture_by_name("bucket"), 
    "check_args": {
        "right_click": True
    },  
    "verify": get_action_picture_by_name("deposit_x"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_click_item"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_deposit_x")
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

# Step 5: Click on the deposit_X option
step_5 = {
    "check": get_action_picture_by_name("deposit_x"), 
    "verify": get_action_picture_by_name("enter_ammount"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_deposit_x"),  
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
    "id": "click_deposit_x",
}

step_5_1 = {
    "check": get_action_picture_by_name("deposit_all"), 
    "verify": get_action_picture_by_name("deposit_all"),
    "verify_args": {
        "reverse_verification": True,
    },  
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_deposit_x"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_deposit_x")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_deposit_x",
}


# Step 6: Type the ammount to deposit + enter 

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


def deposit_x(ammount, image, mock_image):
    updates = [
        {
            "id": "type_ammount",
            "check_args": {
                "write_string_in_client": {
                    "string_to_write": ammount
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
    action_ordered_steps = [
        step_4,
        step_5,
        step_6,
        final_step,
    ]
    action_ordered_steps = update_action(action_ordered_steps, updates)
    return copy.deepcopy(action_ordered_steps)


def deposit_all(image, mock_image=None):
    if mock_image is None:
        updates = [
            {
                "id": "right_click_item",
                "check": get_action_picture_by_name(image),
            }
        ]
    else:
        updates = [
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
    action_ordered_steps = [
        step_4,
        step_5_1,
    ]
    action_ordered_steps = action_ordered_steps + [final_step]
    action_ordered_steps = update_action(action_ordered_steps, updates)
    return copy.deepcopy(action_ordered_steps) 
 
 
def get_deposit_x(ammount, image, mock_image):
    depo = deposit_x(ammount, image, mock_image)
    action_ordered_steps = enter_bank + depo + leave_bank
    return copy.deepcopy(action_ordered_steps)

def get_deposit_all(image, mock_image=None):
    depo_all = deposit_all(image, mock_image)
    action_ordered_steps = enter_bank + depo_all + leave_bank + [final_step]
    return copy.deepcopy(action_ordered_steps)


def get_deposit_x_test():
    return deposit_x("28", "steel_bar", "test_deposit_steel_bar")

def get_deposit_all_test():
    return deposit_all("steel_bar", "test_deposit_steel_bar")



