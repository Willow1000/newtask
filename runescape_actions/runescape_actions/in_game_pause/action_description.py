import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
    always_fail_verify,
    get_sleep_step,
)

from common_action_framework.common_action_framework.common import (
    send_user_name_to_replay_in_client,
    send_pw_to_replay_in_client,
    send_tab_key_to_client,
    send_enter_key_to_client,
    random_mouse_movement,
    verify_after_checking_once,
    StepManipulator,
)

from runescape_actions.commons.press_anywhere_in_menu.action_description import get_step_to_press_anything_in_menu_at_random

time_limit = None  # time limit for this action (in minutes)
current_action_id = "in_game_pause"
app_config_id = "initial-config"  # each action may require a different set of configs from the app itself
# the default that you should always use is: "initial-config" I will change this later if I must
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.
settings = {
    "reloaded": False,
}

all_failure_elements = {
}

forever_loop_step = {
    "jump": {
        # a conditional jump, an if-else condition, in this case, representing a while loop between
        # (it jumps if the condition in verify is false)
        "step_num": 0,
        "verify": none_step_verify,  # none_step_verify and reverse_verification: True will make it a forever loop
        "verify_mode": "verify_once",
        "reverse_verification": True,
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "pause_and_loop_forever",
}

final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "forever_in_game_pause_loop_end_step",
}

verify_fields = {
    "verify": none_step_verify, 
}

action_ordered_steps = get_step_to_press_anything_in_menu_at_random(verify_fields)
check_args = { "sleep_seconds_range": (240, 290) }  # close to 5 minutes (max time before being logged out)

verify_conditions = {
    "verify": verify_after_checking_once,
}
sleep_step = get_sleep_step(check_args, verify_conditions)
sleep_step = copy.deepcopy(sleep_step)
action_ordered_steps.append(sleep_step)
action_ordered_steps.append(forever_loop_step)
action_ordered_steps.append(final_step)

StepManipulator(
    action_ordered_steps, 
    current_action_id,
    app_config_id,
    context,
).initialize_step_ids()


