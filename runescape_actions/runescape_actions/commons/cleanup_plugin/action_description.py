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
current_action_id = "cleanup_plugin"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


#Step 0: Go back to all the plugin list
#You need to change the plugin name and plugin header for the correct ones of the plugin you are using
#and the verify too
step_0 = {
    "check": get_action_picture_by_name("go_back"),  
    "verify": get_action_picture_by_name("plugin_inserted"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_plugin_settings"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_plugin_inserted")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "back_to_plugin_search",
}

# Setp 1: Click the red cross to delete any text from plugin search box
step_1 = {
    "check": get_action_picture_by_name("red_cross"),
    "verify": get_action_picture_by_name("clean_search_bar"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_cleanup"),
            "replay_input": {"replay_type": "mouse", "coords": None}, 
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("ready_to_insert_plugin")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_cross_icon_step", 
}

# Step 2: Click the screwdriver icon to exit configurations
step_2 = {
    "check": get_action_picture_by_name("screwdriver_on"),
    "verify": get_action_picture_by_name("screwdriver"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_screwdriver_on"),
            "replay_input": {"replay_type": "mouse", "coords": None}, 
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_screwdriver")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_screwdriver_icon_step", 
}

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
    step_0,
    step_1,
    step_2,
    final_step,
]
