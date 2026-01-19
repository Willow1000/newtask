import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)

from runescape_actions.commons.cleanup_plugin.action_description import action_ordered_steps as cleanup_plugin
from runescape_actions.commons.toggle_plugin.action_description import action_ordered_steps as toggle_plugin

from common_action_framework.common_action_framework.reuse_action import (
    update_action,
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
current_action_id = "ground_items"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

# TODO: add plugin warning window verifications (step 1 and 2 images)

# wait until app starts up
#  wait till service is in a state such that the action can start should always be step 0


updates = [
    {"id": "type_plugin_name", 
     "check_args": {
        "write_string_in_client": {
            "string_to_write": "Ground Items", 
        },
    }},
    ]
action_ordered_steps = update_action(toggle_plugin, updates)

# Step 3: Click the gear icon next to ground items
step_3 = {
    "check": get_action_picture_by_name("gear_icon"),  
    "verify": get_action_picture_by_name("ground_items_opened"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_ground_items"),  
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

# Step 4: Click the item name textbox
step_4 = {
    "check": left_click_template_match_for_step_by_click_type,  
    "check_args": {
        "template_match_for_step": {
            "image_to_find": get_action_picture_by_name("highlighted_items"), 
            "precision": 0.8,
            "offset": (0,17)
   
        },
    },
    "verify": none_step_verify,
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_existing_textbox"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_action_picture_by_name("test_existing_textbox")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_item_name_textbox",
}


# Step 5: Type "campfire" (or another item's name) in the textbox below NPCs to highlight
step_5 = {
    "check": write_string_in_client,  
    "check_args": {
        "write_string_in_client": {
            "string_to_write": "Campfire", 
        },
    },
    "verify": none_step_verify,  
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_ready_to_insert_item"),  # Mock image of the focused highlight textbox
            "replay_input": {
                "replay_type": "keyboard",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_item_inserted")
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


cleanup_plugin = update_action(cleanup_plugin, updates)

step_6 = cleanup_plugin[0]
step_7 = cleanup_plugin[1]
step_8 = cleanup_plugin[2]





# final step, always add a final step, this is for the if else cases
final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "ground_items_final_step",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}

action_ordered_steps += [
    step_3,
    step_4,
    step_5,
    step_6,
    step_7,
    step_8,
    # always add final_step, this is for any need for an if-else statement
    final_step,
]

