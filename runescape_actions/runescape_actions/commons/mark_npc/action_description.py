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

from common_action_framework.common_action_framework.common import shift_right_click

from runescape_actions.commons.pick_color.pick_color import action_ordered_steps as pick_color

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
current_action_id = "mark_npc"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

# wait until app starts up
#  wait till service is in a state such that the action can start should always be step 0
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

# Step 1: Click the npc to mark
step_1 = {
    "check": shift_right_click,
    "verify": get_action_picture_by_name("tag"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_mark_npc"),
            "replay_input": {"replay_type": "mouse", "coords": None}, 
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_click_npc")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_npc_to_mark", 
}

# Step 2: Click the tag button
step_2 = {
    "check": get_action_picture_by_name("tag"),
    "verify": none_step_verify,
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_click_npc"),
            "replay_input": {"replay_type": "mouse", "coords": None}, 
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_npc_marked")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_tag", 
}

# Step 3: Shift Click tagged Npc
step_3 = {
    "check": shift_right_click,
    "verify": get_action_picture_by_name("tag_color"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_npc_marked"),
            "replay_input": {"replay_type": "mouse", "coords": None}, 
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_tag_color")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_marked_npc", 
}

# Step 4: Hover Mouse to Tag color
step_4 = {
    "check": get_action_picture_by_name("tag_color"),
    "verify": get_action_picture_by_name("pick_color"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_tag_color"),
            "replay_input": {"replay_type": "mouse", "coords": None}, 
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_pick_color")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "hover_tag_color", 
}

# Step 5: Click Pick Color
step_5= {
    "check": get_action_picture_by_name("pick_color"),
    "verify": none_step_verify,
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_pick_color"),
            "replay_input": {"replay_type": "mouse", "coords": None}, 
        },
    ],

    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "click_pick_color", 
}


action_ordered_steps = [step_0, step_1, step_2, step_3, step_4, step_5]

action_ordered_steps += pick_color

# final step, always add a final step, this is for the if else cases
final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "mark_npc_final_step",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}

action_ordered_steps += [final_step]


