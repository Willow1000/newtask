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


from common_action_framework.common_action_framework.common import shift_right_click

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
current_action_id = "object_markers"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


updates = [
    {"id": "type_plugin_name", 
     "check_args": {
        "write_string_in_client": {
            "string_to_write": "Object Markers", 
        },
    }},
    ]
toggle_plugin = update_action(toggle_plugin, updates).copy()


# Step 6: Click shift+right_click in coords (x,y) on the screen
step_6 = {
    "check": shift_right_click,
    "verify": get_action_picture_by_name("mark_object"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_mark_object"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_mark_object_on")
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

# Step 7: Click mark object
step_7 = {
    "check": get_action_picture_by_name("mark_object"),
    "verify": none_step_verify,
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_mark_object_box"),
            "replay_input": {"replay_type": "mouse", "coords": None}, 
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_object_marked")
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

#toggle plugin defined in line 71
cleanup_plugin = copy.deepcopy(cleanup_plugin)
mark_object = [step_6, step_7, final_step]

action_ordered_steps = copy.deepcopy(toggle_plugin) + copy.deepcopy(cleanup_plugin) + copy.deepcopy(mark_object)


