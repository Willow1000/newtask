import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)
from common_action_framework.common_action_framework.common import (
    template_matching,
    left_click_template_match_for_step_by_click_type)
from common_action_framework.common_action_framework.common import (
    send_user_name_to_replay_in_client,
    send_pw_to_replay_in_client,
    send_tab_key_to_client,
    random_mouse_movement,
    verify_after_checking_once,
)

from runescape_actions.commons.toggle_plugin.action_description import action_ordered_steps as toggle_plugin
from runescape_actions.commons.cleanup_plugin.action_description import action_ordered_steps as cleanup_plugin


from common_action_framework.common_action_framework.reuse_action import (
    update_action,
    update_step,
    merge_dicts,
)

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "highlight_friends"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


updates = [
    {"id": "type_plugin_name", 
     "check_args": {
        "write_string_in_client": {
            "string_to_write": "Player Indicators", 
        },
    }},
    ]

action_ordered_steps = update_action(toggle_plugin, updates)

# Step 4: Click the gear icon next to ground items
step_4 = {
    "check": get_action_picture_by_name("gear_icon"),  
    "verify": get_action_picture_by_name("player_indicators_opened"), 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_player_indicators"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_player_indicators_opened")
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


# Step 5: Click the highlight friends name textbox
step_5 = {
    "check": left_click_template_match_for_step_by_click_type,  
    "check_args": {
        "template_match_for_step": {
            "image_to_find": get_action_picture_by_name("highlight_friends"), 
            "precision": 0.8,
            "offset": (122,0)
   
        },
    },
    "verify": get_action_picture_by_name("highlight_friends_options"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_existing_textbox"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_options_opened")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "press_highlight_friends",
}


# Step 6: Click the enable option (add the 40 px offset in the y axis)

step_6 = {
    "check": left_click_template_match_for_step_by_click_type,  
    "check_args": {
        "template_match_for_step": {
            "image_to_find": get_action_picture_by_name("highlight_friends"), 
            "precision": 0.8,
            "offset": (122,40)
   
        },
    },
    "verify": get_action_picture_by_name("highlight_friends_enabled"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_existing_textbox"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
           get_test_picture_by_name("test_highlight_friends_enabled")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "press_enable",
}

#step 7,8,9: cleanup the plugin search

step_7 = cleanup_plugin[0]
step_8 = cleanup_plugin[1]
step_9 = cleanup_plugin[2]




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

action_ordered_steps += [
    step_4,
    step_5,
    step_6,
    step_7,
    step_8,
    step_9,
    final_step,
]


