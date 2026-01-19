import copy 
 
from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)
from common_action_framework.common_action_framework.common import (
    left_click_highlighted,
)
from runescape_actions.commons.definitions.full_setup import map_colors


all_failure_elements = {
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "teleport"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


#TODO: everything



final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "enter_bank_final_step",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}

action_ordered_steps = [
    final_step,
]

