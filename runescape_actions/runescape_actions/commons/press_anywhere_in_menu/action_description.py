import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
    always_fail_verify,
)


from common_action_framework.common_action_framework.reuse_action import (
    update_action,
    update_step,
    merge_dicts,
)
 
from runescape_actions.commons.deposit_bank.action_description import (
    get_deposit_x, 
    get_deposit_all
)
from runescape_actions.commons.withdraw_bank.action_description import get_withdraw_x
from runescape_actions.commons.deposit_bank.action_description import get_deposit_all

from runescape_actions.commons.highlight_npc.action_description import get_action_ordered_steps as get_highlight_npc
from runescape_actions.commons.buy_from_grand_exchange.action_description import get_buy_from_exchange as get_buy_from_exchange
from runescape_actions.commons.buy_from_grand_exchange.action_description import get_action_ordered_steps as buy_from_exchange
from runescape_actions.commons.sell_from_grand_exchange.action_description import get_sell_from_exchange
from runescape_actions.commons.sell_from_grand_exchange.action_description import get_action_ordered_steps as sell_from_exchange
from runescape_actions.commons.deposit_bank.action_description import (
    get_deposit_all
)

from common_action_framework.common_action_framework.common import (
    get_common_args,
    random_mouse_movement,
    client_wait,
)

from common_action_framework.common_action_framework.basic_interaction import (
    ignore_processor,
) 

time_limit = None  # time limit for this action (in minutes)
current_action_id = "press_anywhere_in_menu"
app_config_id = "press_anywhere_in_menu"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

all_failure_elements = {
}

settings = {
    "reloaded": False,
}


# this action will work together with session_metadata, is_looping_in_action=true
# this examplifies how to use several "check" fields and pick one randomly
# check_resolution_type randomly picks one of the checks to run, this is useful for actions that have several possible checks
#  check_resolution_type can be "random", "ordered", the default is "ordered", notice that all the check fields will still 
#   be processed sequentally  (only until the first one is found)
step_to_press_anything_in_menu_at_random = {
    "check": get_action_picture_by_name("all/dashboard/menu/account_management"),
    "check2": get_action_picture_by_name("all/dashboard/menu/character_summary"),
    "check3": get_action_picture_by_name("all/dashboard/menu/chat_channel"),
    "check4": get_action_picture_by_name("all/dashboard/menu/combat_options"),
    "check5": get_action_picture_by_name("all/dashboard/menu/emotes"),
    "check6": get_action_picture_by_name("all/dashboard/menu/friends_list"),
    "check7": get_action_picture_by_name("all/dashboard/menu/inventory"),
    "check8": get_action_picture_by_name("all/dashboard/menu/magic"),
    "check9": get_action_picture_by_name("all/dashboard/menu/music_player"),
    "check10": get_action_picture_by_name("all/dashboard/menu/settings"),
    "check11": get_action_picture_by_name("all/dashboard/menu/skills"),
    "check12": get_action_picture_by_name("all/dashboard/menu/worn_equipment"),
    "check13": get_action_picture_by_name("all/dashboard/menu/prayer"),
    "check_resolution_type": "random",
    "check_resolution_method": "once",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "replay_info": {
        "click_info": {
            "click_type": "click",
            "number_clicks": 1,
        },
    },
    "id": "in_game_pause_loop",
}

 
# final step, always add a final step, this is for the if else cases
final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "in_game_pause_final_step",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}
 
 
def get_step_to_press_anything_in_menu_at_random(verify_fields: dict) -> list[dict]:
    """
    returns action ordered steps
    """
    ordered_steps = []
    step = copy.deepcopy(step_to_press_anything_in_menu_at_random)
    for verify_key, verify_value in verify_fields.items():
        step[verify_key] = verify_value
    ordered_steps.append(step)
    ordered_steps.append(copy.deepcopy(final_step))
    return ordered_steps

