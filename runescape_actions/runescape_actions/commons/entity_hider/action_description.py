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

from runescape_actions.commons.cleanup_plugin.action_description import action_ordered_steps as cleanup_plugin

from runescape_actions.commons.toggle_plugin.action_description import action_ordered_steps as toggle_plugin

from common_action_framework.common_action_framework.reuse_action import (
    update_action,
    update_step,
    merge_dicts,
)

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
current_action_id = "entity_hider"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

# TODO: add plugin warning window verifications (step 1 and 2 images)


updates = [
    {"id": "type_plugin_name", 
     "check_args": {
        "write_string_in_client": {
            "string_to_write": "Entity Hider", 
        },
    }},
    ]


action_ordered_steps = update_action(toggle_plugin, updates)

#We dont include cleanup_plugin first step because it is to exit the plugin configurations (and we have not entered it)
step_4 = cleanup_plugin[1]
step_5 = cleanup_plugin[2]



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

    step_4,
    step_5,

    # always add final_step, this is for any need for an if-else statement
    final_step,
]

