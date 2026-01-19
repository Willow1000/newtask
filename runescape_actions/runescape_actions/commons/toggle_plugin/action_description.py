import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)
from common_action_framework.common_action_framework.image_matching_logic import (
    template_matching
)
from common_action_framework.common_action_framework.common import write_string_in_client 


all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "toggle_plugin"
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

# Step 1: Click the screwdriver icon
step_1 = {
    "check": get_action_picture_by_name("screwdriver"),
    "verify": get_action_picture_by_name("settings_menu_opened"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_screwdriver"),
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
    "id": "click_screwdriver_icon_step", 
}


# Step 2: Type plugin name in the search box
step_2 = {
    "check": write_string_in_client,
    "check_args": {
        "write_string_in_client": {
            "string_to_write": "Npc", 
        },
    },
    "verify": get_action_picture_by_name("plugin_inserted"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("ready_to_insert_plugin"),  # Mock image of the focused search box
            "replay_input": {
                "replay_type": "keyboard",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_plugin_inserted")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "xdot_keyboard_processing",
            "verify": "template_match",
        }
    },
    "id": "type_plugin_name",
}

# Step 3: Click the toggle plugin button
step_3 = {
    "check": get_action_picture_by_name("plugin_off"),  
    "verify": get_action_picture_by_name("plugin_on"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_plugin_off"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_plugin_on")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_gear_icon_step",
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
    step_3,
    final_step
]
