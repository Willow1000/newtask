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

from common_action_framework.common_action_framework.common import (
    left_click_template_match_for_step_by_click_type, 
    shift_right_click,
    )

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "ground_markers"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


updates = [
    {"id": "type_plugin_name", 
     "check_args": {
        "write_string_in_client": {
            "string_to_write": "Ground Markers", 
        },
    }},
    ]

action_ordered_steps = update_action(toggle_plugin, updates)

step_4 = cleanup_plugin[1]
step_5 = cleanup_plugin[2]

# Step 6: Click shift+right_click in coords (x,y) on the screen
step_6 = {
    "check": shift_right_click,
    "verify": get_action_picture_by_name("mark_tile"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_mark_tile"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_mark_tile_on")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "shift_right_click",
}

# Step 7: Click mark tile
step_7 = {
    "check": get_action_picture_by_name("mark_tile"),
    "verify": get_action_picture_by_name("marked_tile"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_mark_tile_on"),
            "replay_input": {"replay_type": "mouse", "coords": None}, 
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_marked_tile")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_mark_object_step", 
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

action_ordered_steps += [
    step_4,
    step_5,
    step_6,
    step_7,
    final_step,
]


