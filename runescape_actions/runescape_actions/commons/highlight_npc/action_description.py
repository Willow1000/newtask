import copy

from common_action_framework.common_action_framework.reuse_action import update_action

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)

from common_action_framework.common_action_framework.common import left_click_template_match_for_step_by_click_type, write_string_in_client 

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
current_action_id = "highlight_npc"
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
            get_test_picture_by_name("ready_to_insert_npc")
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


# Step 2: Type "Npc Indicators" in the search box
step_2 = {
    "check": write_string_in_client,
    "check_args": {
        "write_string_in_client": {
            "string_to_write": "Npc Indicators", 
        },
    },
    "verify": get_action_picture_by_name("plugin_name"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("ready_to_insert_npc"),  # Mock image of the focused search box
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
    "id": "type_npc_in_searchbox_step",  # ID indicating this is the type "npc" in searchbox step
}

# Step 3: Click the gear icon next to NPC indicators
step_3 = {
    "check": get_action_picture_by_name("gear_icon"),
    "verify": get_action_picture_by_name("npc_settings_opened"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_plugin_inserted"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_plugin_settings")
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

# Step 4: Click the npc name textbox
step_4 = {
    "check": left_click_template_match_for_step_by_click_type,  
    "check_args": {
        "template_match_for_step": {
            "image_to_find": get_action_picture_by_name("npc_to_highlight_textbox"), 
            "precision": 0.8,
            "offset": (0,18)
   
        },
    },
    "verify": get_action_picture_by_name("npc_textbox_focused"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_existing_textbox"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_action_picture_by_name("npc_textbox_focused")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_npc_textbox",
}


# Step 5: Type "Banker" in the textbox below NPCs to highlight
step_5 = {
    "check": write_string_in_client,  
    "check_args": {
        "write_string_in_client": {
            "string_to_write": "Banker", 
        },
    },
    "verify": none_step_verify,  # Verify "Banker" was written
    "test": [
        {
            "mock_image": get_test_picture_by_name("ready_to_insert_npc_name"),  # Mock image of the focused highlight textbox
            "replay_input": {
                "replay_type": "keyboard",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_action_picture_by_name("banker_inserted_confirmation")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "xdot_keyboard_processing",
            "verify": "template_match",
        }
    },
    "id": "type_npc_name",
}

# Step 6: Click on the button next to NPC indicator
#TODO acabar douvle click
step_6 = {
    "check": get_action_picture_by_name("npc_plugin_on"),
    "verify": get_action_picture_by_name("npc_plugin_on"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_plugin_settings"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_plugin_settings")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "toggle_plugin",
}

# final step, always add a final step, this is for the if else cases
final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "highlight_npc_final_step",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}



def get_action_ordered_steps(updates=None):
    action_ordered_steps = [
        step_0,
        step_1,
        step_2,
        step_3,
        step_4,
        step_5,
        step_6,
        final_step,
    ]

    if updates != None:
        return copy.deepcopy(update_action(action_ordered_steps, updates))
    else:
        return copy.deepcopy(action_ordered_steps)
