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
from common_action_framework.common_action_framework.reuse_action import (
    update_action,
    update_step,
    merge_dicts,
)

from runescape_actions.commons.highlight_npc.action_description import action_ordered_steps as highlight_npc

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
current_action_id = "highlight_grand_exchange_clerk"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


updates = [
    {"id": "type_npc_name", 
     "check_args": {
        "write_string_in_client": {
            "string_to_write": "Grand Exchange Clerk", 
        },
    }}
    ]

action_ordered_steps = update_action(highlight_npc, updates)



