import copy

from runescape_actions.commons.move_to.action_logic.movementParser import parseFile


from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)

from runescape_actions.commons.definitions.full_setup import map_of_possible_movements

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
current_action_id = "move_to"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "leave_exchange_final_step",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}

#Mock function for now
def get_move_to(movement: str) -> list[dict]:
    #return map_of_possible_movements[movement]
    return [final_step,]

# Real function, but for now used only for testing
def get_move_to_test(movement: str) -> list[dict]:
    return map_of_possible_movements[movement]


action_ordered_steps = [final_step,]


